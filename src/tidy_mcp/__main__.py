#!/usr/bin/env python3
"""
Entry point for running the tidy_mcp package as a module.

Usage:
    python -m tidy_mcp
    python -m tidy_mcp --help
"""

import sys
from .server import mcp, main

if __name__ == "__main__":
    main(mcp)
