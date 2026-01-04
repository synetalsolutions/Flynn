"""
Flynn MCP Server - Docker operations through Model Context Protocol.

This module provides the main MCP server implementation for Flynn,
enabling AI assistants to manage Docker containers and compose stacks.
"""

import asyncio
import signal
import sys
from typing import List, Dict, Any
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
from .handlers import DockerHandlers

# Initialize the Flynn MCP server
server = Server("flynn")


@server.list_prompts()
async def handle_list_prompts() -> List[types.Prompt]:
    """List available prompts for Docker operations."""
    return [
        types.Prompt(
            name="deploy-stack",
            description="Generate and deploy a Docker stack based on requirements",
            arguments=[
                types.PromptArgument(
                    name="requirements",
                    description="Description of the desired Docker stack",
                    required=True
                ),
                types.PromptArgument(
                    name="project_name",
                    description="Name for the Docker Compose project",
                    required=True
                )
            ]
        ),
        types.Prompt(
            name="analyze-containers",
            description="Analyze running containers and provide insights",
            arguments=[
                types.PromptArgument(
                    name="focus",
                    description="What to focus on: performance, logs, health, or all",
                    required=False
                )
            ]
        )
    ]


@server.get_prompt()
async def handle_get_prompt(name: str, arguments: Dict[str, str] | None) -> types.GetPromptResult:
    """Get a specific prompt by name."""
    if name == "deploy-stack":
        return _get_deploy_stack_prompt(arguments)
    elif name == "analyze-containers":
        return _get_analyze_containers_prompt(arguments)
    else:
        raise ValueError(f"Unknown prompt: {name}")


def _get_deploy_stack_prompt(arguments: Dict[str, str] | None) -> types.GetPromptResult:
    """Generate the deploy-stack prompt."""
    if not arguments or "requirements" not in arguments or "project_name" not in arguments:
        raise ValueError("Missing required arguments: requirements, project_name")

    system_message = (
        "You are Flynn, a Docker deployment specialist powered by the Synetal Solutions community. "
        "Generate appropriate Docker Compose YAML or container configurations based on user "
        "requirements. For simple single-container deployments, use the create-container tool. "
        "For multi-container deployments, generate a docker-compose.yml and use the deploy-compose "
        "tool. To access logs, first use the list-containers tool to discover running containers, "
        "then use the get-logs tool to retrieve logs for a specific container."
    )

    user_message = f"""Please help me deploy the following stack:
Requirements: {arguments['requirements']}
Project name: {arguments['project_name']}

Analyze if this needs a single container or multiple containers. Then:
1. For single container: Use the create-container tool with format:
{{
    "image": "image-name",
    "name": "container-name",
    "ports": {{"80": "80"}},
    "environment": {{"ENV_VAR": "value"}}
}}

2. For multiple containers: Use the deploy-compose tool with format:
{{
    "project_name": "example-stack",
    "compose_yaml": "version: '3.8'\\nservices:\\n  service1:\\n    image: image1:latest\\n    ports:\\n      - '8080:80'"
}}"""

    return types.GetPromptResult(
        description="Generate and deploy a Docker stack",
        messages=[
            types.PromptMessage(
                role="system",
                content=types.TextContent(type="text", text=system_message)
            ),
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=user_message)
            )
        ]
    )


def _get_analyze_containers_prompt(arguments: Dict[str, str] | None) -> types.GetPromptResult:
    """Generate the analyze-containers prompt."""
    focus = arguments.get("focus", "all") if arguments else "all"
    
    system_message = (
        "You are Flynn, a Docker analysis specialist. Analyze the running containers and provide "
        "actionable insights about their status, resource usage, and potential issues."
    )

    user_message = f"""Please analyze my Docker containers with focus on: {focus}

Use the list-containers tool first to see all containers, then use get-logs on any containers 
that appear to have issues. Provide a summary of:
1. Container health status
2. Any error patterns in logs
3. Recommendations for optimization"""

    return types.GetPromptResult(
        description="Analyze Docker containers and provide insights",
        messages=[
            types.PromptMessage(
                role="system",
                content=types.TextContent(type="text", text=system_message)
            ),
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=user_message)
            )
        ]
    )


@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List all available Docker management tools."""
    return [
        types.Tool(
            name="create-container",
            description="Create and start a new standalone Docker container",
            inputSchema={
                "type": "object",
                "properties": {
                    "image": {
                        "type": "string",
                        "description": "Docker image to use (e.g., 'nginx:latest')"
                    },
                    "name": {
                        "type": "string",
                        "description": "Name for the container"
                    },
                    "ports": {
                        "type": "object",
                        "description": "Port mappings (host:container)",
                        "additionalProperties": {"type": "string"}
                    },
                    "environment": {
                        "type": "object",
                        "description": "Environment variables",
                        "additionalProperties": {"type": "string"}
                    }
                },
                "required": ["image"]
            }
        ),
        types.Tool(
            name="deploy-compose",
            description="Deploy a multi-container application using Docker Compose",
            inputSchema={
                "type": "object",
                "properties": {
                    "compose_yaml": {
                        "type": "string",
                        "description": "Docker Compose YAML content"
                    },
                    "project_name": {
                        "type": "string",
                        "description": "Name for the Docker Compose project"
                    }
                },
                "required": ["compose_yaml", "project_name"]
            }
        ),
        types.Tool(
            name="get-logs",
            description="Retrieve logs from a Docker container",
            inputSchema={
                "type": "object",
                "properties": {
                    "container_name": {
                        "type": "string",
                        "description": "Name or ID of the container"
                    },
                    "tail": {
                        "type": "integer",
                        "description": "Number of lines to retrieve (default: 100)",
                        "default": 100
                    }
                },
                "required": ["container_name"]
            }
        ),
        types.Tool(
            name="list-containers",
            description="List all Docker containers (running and stopped)",
            inputSchema={
                "type": "object",
                "properties": {
                    "all": {
                        "type": "boolean",
                        "description": "Include stopped containers (default: true)",
                        "default": True
                    }
                }
            }
        ),
        types.Tool(
            name="stop-container",
            description="Stop a running Docker container",
            inputSchema={
                "type": "object",
                "properties": {
                    "container_name": {
                        "type": "string",
                        "description": "Name or ID of the container to stop"
                    }
                },
                "required": ["container_name"]
            }
        ),
        types.Tool(
            name="remove-container",
            description="Remove a Docker container",
            inputSchema={
                "type": "object",
                "properties": {
                    "container_name": {
                        "type": "string",
                        "description": "Name or ID of the container to remove"
                    },
                    "force": {
                        "type": "boolean",
                        "description": "Force removal of running container",
                        "default": False
                    }
                },
                "required": ["container_name"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any] | None) -> List[types.TextContent]:
    """Handle tool calls for Docker operations."""
    if not arguments and name not in ["list-containers"]:
        raise ValueError("Missing arguments")

    try:
        match name:
            case "create-container":
                return await DockerHandlers.handle_create_container(arguments)
            case "deploy-compose":
                return await DockerHandlers.handle_deploy_compose(arguments)
            case "get-logs":
                return await DockerHandlers.handle_get_logs(arguments)
            case "list-containers":
                return await DockerHandlers.handle_list_containers(arguments or {})
            case "stop-container":
                return await DockerHandlers.handle_stop_container(arguments)
            case "remove-container":
                return await DockerHandlers.handle_remove_container(arguments)
            case _:
                raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"❌ Error: {str(e)}\n📋 Arguments: {arguments}"
        )]


async def main():
    """Main entry point for the Flynn MCP server."""
    # Set up graceful shutdown handlers
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    print("🚀 Flynn MCP Server starting...", file=sys.stderr)
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="flynn",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def handle_shutdown(signum, frame):
    """Handle graceful shutdown."""
    print("\n👋 Flynn shutting down gracefully...", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
