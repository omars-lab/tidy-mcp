"""
MCP Server to keep things tidy!

A Model Context Protocol (MCP) server that provides resources, tools, and prompts
personal workflow management.
"""

__version__ = "0.1.0"
__author__ = "Omar Eid"
__email__ = "omar@bytesofpurpose.com"
__description__ = "MCP Server to keep things tidy!"

from .server import mcp, main

__all__ = [
    "mcp",
    "main",
    "__version__",
    "__author__",
    "__email__",
    "__description__",
]
