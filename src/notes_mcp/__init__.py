"""
MCP Server for Note Taking Companion

A Model Context Protocol (MCP) server that provides resources, tools, and prompts
for note-taking workflows and personal knowledge management.
"""

__version__ = "0.1.0"
__author__ = "Omar Eid"
__email__ = "omareid@example.com"
__description__ = "MCP Server for Note Taking Companion"

from .server import mcp, NoteTemplate, NoteAnalysisRequest, NoteAnalysisResponse, main

__all__ = [
    "mcp",
    "NoteTemplate",
    "NoteAnalysisRequest",
    "NoteAnalysisResponse",
    "main",
    "__version__",
    "__author__",
    "__email__",
    "__description__",
]
