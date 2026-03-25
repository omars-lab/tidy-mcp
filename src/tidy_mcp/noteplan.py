"""
Tools for working with NotePlan files and generating x-callback-url links.

This module provides MCP tools to convert NotePlan files into shareable
x-callback-url links that can open notes in the NotePlan app.
"""

import re
from pathlib import Path
from typing import Annotated, Optional
from pydantic import Field
from urllib.parse import quote


# Regex pattern for daily plan files (YYYY-MM-DD.md or similar)
DAILY_PLAN_PATTERN = re.compile(r"(\d{4})-(\d{2})-(\d{2})")


def _extract_note_title(file_path: str) -> str:
    """
    Extract the note title from a file path for use in x-callback-url.
    
    For daily plans (YYYY-MM-DD.md), returns the date in YYYY-MM-DD format.
    For other notes, returns the filename without extension.
    
    Args:
        file_path: Path to the NotePlan file (can be relative or absolute)
        
    Returns:
        Note title string suitable for x-callback-url
    """
    path = Path(file_path)
    
    # Check if it's a daily plan file
    match = DAILY_PLAN_PATTERN.search(path.stem)
    if match:
        # For daily plans, use the date format (YYYY-MM-DD)
        year, month, day = match.groups()
        return f"{year}-{month}-{day}"
    
    # For other notes, use the filename without extension
    return path.stem


def _generate_x_callback_url(
    note_title: str, 
    is_daily_plan: bool = False,
    heading: Optional[str] = None
) -> str:
    """
    Generate a NotePlan x-callback-url for a given note title.
    
    Args:
        note_title: The title of the note (date for daily plans, filename for others)
        is_daily_plan: Whether this is a daily plan (uses noteDate instead of noteTitle)
        heading: Optional heading within the document to link to
        
    Returns:
        Complete x-callback-url string
    """
    action = "openNote"  # Always use openNote action
    
    if is_daily_plan:
        # For daily plans, use noteDate format: YYYYMMDD (no dashes)
        # note_title should be in YYYY-MM-DD format, convert to YYYYMMDD
        date_str = note_title.replace("-", "")
        url = f"noteplan://x-callback-url/{action}?noteDate={date_str}"
    else:
        # For regular notes, use noteTitle
        encoded_title = quote(note_title, safe='')
        url = f"noteplan://x-callback-url/{action}?noteTitle={encoded_title}"
    
    # Add heading parameter if provided
    if heading:
        encoded_heading = quote(heading, safe='')
        url += f"&heading={encoded_heading}"
    
    return url


def derive_xcallback_url_from_noteplan_file(
    file_path: Annotated[
        str,
        Field(description="Path to the NotePlan file (e.g., '2025-11-13.md' or 'notes/project-ideas.md'). Can be relative or absolute.")
    ],
    heading: Annotated[
        Optional[str],
        Field(description="Optional heading within the document to link to. If provided, the link will jump to this heading in the note.")
    ] = None,
) -> dict:
    """
    Derive an x-callback-url link from a NotePlan file path.
    
    This tool converts a NotePlan file path into a shareable x-callback-url link
    that will open the note in the NotePlan app when clicked. Optionally, it can
    link to a specific heading within the document.
    
    For daily plans (YYYY-MM-DD.md), the link uses noteDate format (YYYYMMDD).
    For other notes, the link uses noteTitle (filename without extension).
    The action is always 'openNote'.
    
    Examples:
    - File: "2025-11-13.md" → noteplan://x-callback-url/openNote?noteDate=20251113
    - File: "2025-11-13.md", heading: "Tasks" → noteplan://x-callback-url/openNote?noteDate=20251113&heading=Tasks
    - File: "notes/project-ideas.md" → noteplan://x-callback-url/openNote?noteTitle=project-ideas
    - File: "notes/project-ideas.md", heading: "Implementation" → noteplan://x-callback-url/openNote?noteTitle=project-ideas&heading=Implementation
    
    Returns:
        Dictionary containing the x-callback-url link and metadata.
    """
    try:
        # Extract note title from file path
        note_title = _extract_note_title(file_path)
        
        # Determine if it's a daily plan
        path = Path(file_path)
        match = DAILY_PLAN_PATTERN.search(path.stem)
        is_daily_plan = match is not None
        
        # Generate x-callback-url with heading support (always uses openNote action)
        url = _generate_x_callback_url(note_title, is_daily_plan, heading)
        
        return {
            "success": True,
            "x_callback_url": url,
            "note_title": note_title,
            "file_path": file_path,
            "is_daily_plan": is_daily_plan,
            "heading": heading,
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "url_generation_failed"
        }

