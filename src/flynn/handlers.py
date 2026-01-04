"""
Flynn Docker Handlers - Implementation of Docker operations.

This module contains all the handler functions for Docker container
and compose stack management.
"""

from typing import List, Dict, Any
import asyncio
import os
import yaml
import platform
from python_on_whales import DockerClient
from mcp.types import TextContent
from .docker_executor import DockerComposeExecutor

# Initialize Docker client
docker_client = DockerClient()


async def parse_port_mapping(host_key: str, container_port: str | int) -> tuple:
    """Parse port mapping with protocol support."""
    if '/' in str(host_key):
        host_port, protocol = host_key.split('/')
        if protocol.lower() == 'udp':
            return (str(host_port), str(container_port), 'udp')
        return (str(host_port), str(container_port))

    if isinstance(container_port, str) and '/' in container_port:
        port, protocol = container_port.split('/')
        if protocol.lower() == 'udp':
            return (str(host_key), port, 'udp')
        return (str(host_key), port)

    return (str(host_key), str(container_port))


class DockerHandlers:
    """Handlers for Docker operations."""
    
    TIMEOUT_AMOUNT = 200

    @staticmethod
    async def handle_create_container(arguments: Dict[str, Any]) -> List[TextContent]:
        """Create and start a new Docker container."""
        try:
            image = arguments["image"]
            container_name = arguments.get("name")
            ports = arguments.get("ports", {})
            environment = arguments.get("environment", {})

            if not image:
                raise ValueError("Image name cannot be empty")

            port_mappings = []
            for host_key, container_port in ports.items():
                mapping = await parse_port_mapping(host_key, container_port)
                port_mappings.append(mapping)

            async def pull_and_run():
                if not docker_client.image.exists(image):
                    await asyncio.to_thread(docker_client.image.pull, image)

                container = await asyncio.to_thread(
                    docker_client.container.run,
                    image,
                    name=container_name,
                    publish=port_mappings,
                    envs=environment,
                    detach=True
                )
                return container

            container = await asyncio.wait_for(
                pull_and_run(),
                timeout=DockerHandlers.TIMEOUT_AMOUNT
            )
            
            return [TextContent(
                type="text",
                text=f"✅ Container created successfully!\n"
                     f"📦 Name: {container.name}\n"
                     f"🆔 ID: {container.id[:12]}\n"
                     f"🖼️ Image: {image}"
            )]
        except asyncio.TimeoutError:
            return [TextContent(
                type="text",
                text=f"⏱️ Operation timed out after {DockerHandlers.TIMEOUT_AMOUNT} seconds"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error creating container: {str(e)}"
            )]

    @staticmethod
    async def handle_deploy_compose(arguments: Dict[str, Any]) -> List[TextContent]:
        """Deploy a Docker Compose stack."""
        debug_info = []
        try:
            compose_yaml = arguments.get("compose_yaml")
            project_name = arguments.get("project_name")

            if not compose_yaml or not project_name:
                raise ValueError("Missing required compose_yaml or project_name")

            yaml_content = DockerHandlers._process_yaml(compose_yaml, debug_info)
            compose_path = DockerHandlers._save_compose_file(yaml_content, project_name)

            try:
                result = await DockerHandlers._deploy_stack(
                    compose_path, project_name, debug_info
                )
                return [TextContent(type="text", text=result)]
            finally:
                DockerHandlers._cleanup_files(compose_path)

        except Exception as e:
            debug_output = "\n".join(debug_info)
            return [TextContent(
                type="text",
                text=f"❌ Error deploying compose stack: {str(e)}\n\n"
                     f"📋 Debug Information:\n{debug_output}"
            )]

    @staticmethod
    def _process_yaml(compose_yaml: str, debug_info: List[str]) -> dict:
        """Process and validate YAML content."""
        debug_info.append("=== Original YAML ===")
        debug_info.append(compose_yaml)

        try:
            yaml_content = yaml.safe_load(compose_yaml)
            debug_info.append("\n=== Loaded YAML Structure ===")
            debug_info.append(str(yaml_content))
            return yaml_content
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {str(e)}")

    @staticmethod
    def _save_compose_file(yaml_content: dict, project_name: str) -> str:
        """Save compose YAML to a temporary file."""
        compose_dir = os.path.join(os.getcwd(), "docker_compose_files")
        os.makedirs(compose_dir, exist_ok=True)

        compose_yaml = yaml.safe_dump(
            yaml_content, default_flow_style=False, sort_keys=False
        )
        compose_path = os.path.join(compose_dir, f"{project_name}-docker-compose.yml")

        with open(compose_path, 'w', encoding='utf-8') as f:
            f.write(compose_yaml)
            f.flush()
            if platform.system() != 'Windows':
                os.fsync(f.fileno())

        return compose_path

    @staticmethod
    async def _deploy_stack(
        compose_path: str,
        project_name: str,
        debug_info: List[str]
    ) -> str:
        """Deploy the Docker Compose stack."""
        compose = DockerComposeExecutor(compose_path, project_name)

        for command in [compose.down, compose.up]:
            try:
                code, out, err = await command()
                debug_info.extend([
                    f"\n=== {command.__name__.capitalize()} Command ===",
                    f"Return Code: {code}",
                    f"Stdout: {out}",
                    f"Stderr: {err}"
                ])

                if code != 0 and command == compose.up:
                    raise Exception(f"Deploy failed with code {code}: {err}")
            except Exception as e:
                if command != compose.down:
                    raise e
                debug_info.append(f"Warning during {command.__name__}: {str(e)}")

        code, out, err = await compose.ps()
        service_info = out if code == 0 else "Unable to list services"

        return (
            f"✅ Successfully deployed compose stack '{project_name}'\n\n"
            f"📊 Running services:\n{service_info}"
        )

    @staticmethod
    def _cleanup_files(compose_path: str) -> None:
        """Clean up temporary compose files."""
        try:
            if os.path.exists(compose_path):
                os.remove(compose_path)
            compose_dir = os.path.dirname(compose_path)
            if os.path.exists(compose_dir) and not os.listdir(compose_dir):
                os.rmdir(compose_dir)
        except Exception as e:
            print(f"Warning during cleanup: {str(e)}")

    @staticmethod
    async def handle_get_logs(arguments: Dict[str, Any]) -> List[TextContent]:
        """Retrieve logs from a Docker container."""
        try:
            container_name = arguments.get("container_name")
            tail = arguments.get("tail", 100)
            
            if not container_name:
                raise ValueError("Missing required container_name")

            logs = await asyncio.to_thread(
                docker_client.container.logs,
                container_name,
                tail=tail
            )

            return [TextContent(
                type="text",
                text=f"📋 Logs for container '{container_name}':\n\n{logs}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error retrieving logs: {str(e)}"
            )]

    @staticmethod
    async def handle_list_containers(arguments: Dict[str, Any]) -> List[TextContent]:
        """List all Docker containers."""
        try:
            show_all = arguments.get("all", True)
            containers = await asyncio.to_thread(
                docker_client.container.list,
                all=show_all
            )

            if not containers:
                return [TextContent(
                    type="text",
                    text="📦 No Docker containers found."
                )]

            container_lines = []
            for c in containers:
                status_emoji = "🟢" if c.state.status == "running" else "🔴"
                container_lines.append(
                    f"{status_emoji} {c.name} ({c.id[:12]}) - {c.state.status}"
                )

            container_list = "\n".join(container_lines)
            return [TextContent(
                type="text",
                text=f"📦 Docker Containers:\n\n{container_list}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error listing containers: {str(e)}"
            )]

    @staticmethod
    async def handle_stop_container(arguments: Dict[str, Any]) -> List[TextContent]:
        """Stop a running Docker container."""
        try:
            container_name = arguments.get("container_name")
            if not container_name:
                raise ValueError("Missing required container_name")

            await asyncio.to_thread(
                docker_client.container.stop,
                container_name
            )

            return [TextContent(
                type="text",
                text=f"⏹️ Container '{container_name}' stopped successfully."
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error stopping container: {str(e)}"
            )]

    @staticmethod
    async def handle_remove_container(arguments: Dict[str, Any]) -> List[TextContent]:
        """Remove a Docker container."""
        try:
            container_name = arguments.get("container_name")
            force = arguments.get("force", False)
            
            if not container_name:
                raise ValueError("Missing required container_name")

            await asyncio.to_thread(
                docker_client.container.remove,
                container_name,
                force=force
            )

            return [TextContent(
                type="text",
                text=f"🗑️ Container '{container_name}' removed successfully."
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error removing container: {str(e)}"
            )]
