# Using Flynn with Antigravity

This guide explains how to configure Flynn as an MCP server within the Antigravity IDE ecosystem.

## Setup Instructions

### 1. Prerequisites
- **Flynn** installed via `uv` or accessible in your project.
- **Docker Desktop** or **Docker Engine** running.

### 2. Configuration
Add Flynn to your `mcp_servers` configuration in Antigravity settings or your workspace configuration.

#### Using `uvx` (Recommended)
This method runs the latest version of Flynn directly from PyPI without manual installation.

```json
{
  "mcpServers": {
    "flynn": {
      "command": "uvx",
      "args": ["flynn-mcp"]
    }
  }
}
```

#### Using Local Installation
If you have cloned the repository locally:

```json
{
  "mcpServers": {
    "flynn": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/Flynn",
        "flynn"
      ]
    }
  }
}
```

### 3. Verification
Once configured, reload your Antigravity window. You should see Flynn initialized in the available servers list.

You can test it by asking Antigravity:
> "List my running Docker containers"
> "Deploy a new Nginx container"

## Troubleshooting

- **Socket Issues**: Ensure Docker is running and the socket is accessible at the standard location.
- **Permissions**: Verify Antigravity has permission to execute `uv` or `uvx` commands.
