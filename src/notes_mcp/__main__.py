#!/usr/bin/env python3
"""
Entry point for running the notes_mcp package as a module.

Usage:
    python -m notes_mcp
    python -m notes_mcp --help
"""

import sys
from .server import main

if __name__ == "__main__":
    main()
