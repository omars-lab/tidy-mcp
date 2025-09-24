#!/usr/bin/env python3
"""
MCP Server for keeping things tidy!
Provides resources, tools, and prompts for my personal workflow management.
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path

from fastmcp import FastMCP
from pydantic import BaseModel, Field


# Initialize FastMCP server
mcp = FastMCP("oeid-tidy-mcp")

def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    # Run the server
    main()
