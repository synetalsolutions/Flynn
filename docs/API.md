# Flynn API Reference

This document details the tools and prompts available in Flynn.

## Tools

### `create-container`
Creates and starts a standalone container.

**Input Schema:**
```json
{
  "image": "string (required)",
  "name": "string (optional)",
  "ports": {
    "host_port": "container_port"
  },
  "environment": {
    "KEY": "VALUE"
  }
}
```

### `deploy-compose`
Deploys a multi-container stack using Docker Compose.

**Input Schema:**
```json
{
  "project_name": "string (required)",
  "compose_yaml": "string (required)"
}
```

### `get-logs`
Retrieves logs from a container.

**Input Schema:**
```json
{
  "container_name": "string (required)",
  "tail": "integer (default: 100)"
}
```

### `list-containers`
Lists all containers on the system.

**Input Schema:**
```json
{
  "all": "boolean (default: true)"
}
```

### `stop-container`
Stops a running container.

**Input Schema:**
```json
{
  "container_name": "string (required)"
}
```

### `remove-container`
Removes a container.

**Input Schema:**
```json
{
  "container_name": "string (required)",
  "force": "boolean (default: false)"
}
```

## Prompts

### `deploy-stack`
Guides the AI in collecting requirements and generating a deployment.

**Arguments:**
- `requirements`: Description of what to deploy
- `project_name`: Name for the project

### `analyze-containers`
Analyzes the state of running containers.

**Arguments:**
- `focus`: Focus area (performance, logs, health, all)
