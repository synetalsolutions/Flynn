<div align="center">

# 🚀 Flynn

**A powerful MCP server for Docker operations**

*Community-driven • Open Source • AI-Powered*

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-orange.svg)](https://github.com/astral-sh/ruff)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-purple.svg)](https://modelcontextprotocol.io)

[Features](#-features) • [Quick Start](#-quick-start) • [Tools](#-available-tools) • [Contributing](#-contributing) • [Community](#-community) • [Antigravity Setup](docs/ANTIGRAVITY_SETUP.md)

</div>

---

## 🎯 What is Flynn?

Flynn is a **Model Context Protocol (MCP)** server that enables AI assistants like Claude, Gemini, and others to manage Docker containers and compose stacks seamlessly. Built by the [Synetal Solutions](https://github.com/synetalsolutions) open source community, Flynn makes container management as simple as having a conversation.

### Why Flynn?

- 🤖 **AI-Native**: Designed from the ground up for AI assistants
- 🐳 **Full Docker Support**: Containers, Compose stacks, logs, and more
- ⚡ **Zero Configuration**: Works out of the box with any MCP-compatible client
- 🌍 **Community Driven**: Open source and built by developers, for developers

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📦 **Container Management** | Create, start, stop, and remove containers |
| 🎼 **Compose Stacks** | Deploy multi-container applications with Docker Compose |
| 📋 **Log Retrieval** | Fetch and analyze container logs |
| 📊 **Status Monitoring** | List and monitor all containers |
| 🔌 **Port Mapping** | Full support for TCP/UDP port mappings |
| 🌍 **Environment Variables** | Configure containers with env vars |

---

## 🚀 Quick Start

### Option 1: Using uvx (Recommended)

Add Flynn to your MCP client configuration:

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

### Option 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/synetalsolutions/Flynn.git
cd Flynn

# Install with uv
uv sync

# Run Flynn
uv run flynn
```

### Configuration Locations

| Platform | Config File Location |
|----------|---------------------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%/Claude/claude_desktop_config.json` |
| **Linux** | `~/.config/claude/claude_desktop_config.json` |

---

## 📦 Prerequisites

- **Python 3.12+**
- **Docker Desktop** or **Docker Engine**
- **uv** package manager (recommended) or pip
- An MCP-compatible AI client (Claude Desktop, etc.)

---

## 🛠️ Available Tools

Flynn provides the following tools to AI assistants:

### `create-container`
Create and start a new Docker container.

```json
{
  "image": "nginx:latest",
  "name": "my-nginx",
  "ports": {"80": "8080"},
  "environment": {"NGINX_HOST": "localhost"}
}
```

### `deploy-compose`
Deploy a Docker Compose stack.

```json
{
  "project_name": "my-stack",
  "compose_yaml": "version: '3.8'\nservices:\n  web:\n    image: nginx:latest\n    ports:\n      - '80:80'"
}
```

### `list-containers`
List all Docker containers (running and stopped).

```json
{}
```

### `get-logs`
Retrieve logs from a container.

```json
{
  "container_name": "my-nginx",
  "tail": 100
}
```

### `stop-container`
Stop a running container.

```json
{
  "container_name": "my-nginx"
}
```

### `remove-container`
Remove a container.

```json
{
  "container_name": "my-nginx",
  "force": true
}
```

---

## 🔍 Debugging

Use the MCP Inspector to debug Flynn:

```bash
npx @modelcontextprotocol/inspector uv run flynn
```

This opens a web interface where you can test all tools interactively.

---

## 🤝 Contributing

We love contributions! Flynn is built by the community, for the community.

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Flynn.git
cd Flynn

# Install dev dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run linting
uv run ruff check .
```

---

## 🌍 Community

Flynn is part of the **Synetal Solutions** open source ecosystem.

- 💬 [Discussions](https://github.com/synetalsolutions/Flynn/discussions)
- 🐛 [Issue Tracker](https://github.com/synetalsolutions/Flynn/issues)
- 📧 Email: support@synetalsolutions.com

---

## 📜 License

Flynn is open source software licensed under the [MIT License](LICENSE).

---



<div align="center">

**Made with ❤️ by the Synetal Solutions Community**

[⬆ Back to Top](#-flynn)

</div>
