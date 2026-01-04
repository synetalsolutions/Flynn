"""
Flynn - A powerful MCP server for Docker operations.

Community-driven, open source Docker management through AI.
Part of the Synetal Solutions open source ecosystem.
"""

from . import server
import asyncio

__version__ = "1.0.0"
__author__ = "Synetal Solutions Community"


def main():
    """Main entry point for the Flynn MCP server."""
    asyncio.run(server.main())


__all__ = ['main', 'server', '__version__']