#!/usr/bin/env python3
"""
MCP Server for keeping things tidy!
Provides resources, tools, and prompts for my personal workflow management.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path
from fastmcp import FastMCP
from .plantuml import tool_generate_plantuml_image_url, tool_download_plantuml_image, prompt_iterate_on_plantuml_diagram

def main(mcp: FastMCP):
    mcp.tool("generate_plantuml_image_url")(tool_generate_plantuml_image_url)
    mcp.tool("download_plantuml_image")(tool_download_plantuml_image)
    mcp.prompt("iterate_on_plantuml_diagram")(prompt_iterate_on_plantuml_diagram)
    """Main entry point for the MCP server."""
    mcp.run()

# Initialize FastMCP server
mcp = FastMCP("tidy-mcp")

if __name__ == "__main__":
    # Run the server
    main(mcp)