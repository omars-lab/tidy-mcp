#!/usr/bin/env python3
"""
MCP Server for Note Taking Companion
Provides resources, tools, and prompts for note-taking workflows.
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path

from fastmcp import FastMCP
from pydantic import BaseModel, Field


# Initialize FastMCP server
mcp = FastMCP("oeid-notes-mcp")

# Example Resource: Note Templates
class NoteTemplate(BaseModel):
    """A note template resource."""
    id: str = Field(description="Unique identifier for the template")
    name: str = Field(description="Name of the template")
    content: str = Field(description="Template content with placeholders")
    category: str = Field(description="Category of the template")
    created_at: str = Field(description="Creation timestamp")


@mcp.resource("data://note_templates")
async def get_note_templates() -> List[NoteTemplate]:
    """Get available note templates."""
    templates = [
        NoteTemplate(
            id="meeting-notes",
            name="Meeting Notes Template",
            content="# Meeting Notes\n\n## 📅 Date: {{date}}\n## 👥 Attendees: {{attendees}}\n## 📋 Agenda: {{agenda}}\n\n## 📝 Notes:\n\n## ✅ Action Items:\n- [ ] \n\n## 🔄 Follow-up:\n",
            category="meetings",
            created_at=datetime.now().isoformat()
        ),
        NoteTemplate(
            id="daily-reflection",
            name="Daily Reflection Template",
            content="# Daily Reflection - {{date}}\n\n## 🎯 Today's Goals:\n1. \n2. \n3. \n\n## ✅ Accomplishments:\n\n## 🤔 Challenges:\n\n## 📚 Learnings:\n\n## 🎯 Tomorrow's Focus:\n",
            category="personal",
            created_at=datetime.now().isoformat()
        )
    ]
    return templates

# Example Tool: Note Analysis
class NoteAnalysisRequest(BaseModel):
    """Request model for note analysis."""
    content: str = Field(description="Note content to analyze")
    analysis_type: str = Field(description="Type of analysis: 'summary', 'action_items', 'key_points'")


class NoteAnalysisResponse(BaseModel):
    """Response model for note analysis."""
    analysis: str = Field(description="Analysis result")
    confidence: float = Field(description="Confidence score (0-1)")
    metadata: Dict[str, Any] = Field(description="Additional metadata")


@mcp.tool("analyze_note")
async def analyze_note(request: NoteAnalysisRequest) -> NoteAnalysisResponse:
    """Analyze note content and extract insights."""
    content = request.content.lower()
    
    # Simple analysis logic (in a real implementation, this would use AI)
    word_count = len(content.split())
    has_action_items = any(word in content for word in ['todo', 'action', 'task', 'follow-up'])
    has_dates = any(char.isdigit() for char in content)
    
    if request.analysis_type == "summary":
        analysis = f"Note contains {word_count} words. "
        if has_action_items:
            analysis += "Contains action items. "
        if has_dates:
            analysis += "Contains dates/timestamps."
        confidence = 0.8
    elif request.analysis_type == "action_items":
        analysis = "Action items detected: " + ("Yes" if has_action_items else "No")
        confidence = 0.9 if has_action_items else 0.7
    else:  # key_points
        analysis = f"Key metrics: {word_count} words, {'has' if has_action_items else 'no'} action items"
        confidence = 0.75
    
    return NoteAnalysisResponse(
        analysis=analysis,
        confidence=confidence,
        metadata={
            "word_count": word_count,
            "has_action_items": has_action_items,
            "has_dates": has_dates
        }
    )

# Example Prompt: Note Generation
class NoteGenerationRequest(BaseModel):
    """Request model for note generation."""
    topic: str = Field(description="Topic for the note")
    style: str = Field(description="Writing style: 'formal', 'casual', 'bullet_points'")
    length: str = Field(description="Desired length: 'short', 'medium', 'long'")


class NoteGenerationResponse(BaseModel):
    """Response model for note generation."""
    content: str = Field(description="Generated note content")
    template_used: str = Field(description="Template that was used")


@mcp.prompt("generate_note")
async def generate_note(request: NoteGenerationRequest) -> NoteGenerationResponse:
    """Generate a note based on the given topic and style."""
    
    # Simple template-based generation
    if request.style == "bullet_points":
        template = f"""# {request.topic}

## Key Points:
• 
• 
• 

## Notes:
• 
• 

## Action Items:
• 
"""
    elif request.style == "formal":
        template = f"""# {request.topic}

## Overview
[Provide a brief overview of the topic]

## Details
[Include relevant details and context]

## Conclusion
[Summarize key takeaways]
"""
    else:  # casual
        template = f"""# {request.topic}

Hey there! Here's what I learned about {request.topic}:

## What I found:
- 
- 

## My thoughts:
[Share personal insights and reflections]

## Next steps:
- 
"""
    
    # Adjust length based on request
    if request.length == "short":
        template = template.replace("\n\n", "\n")
    elif request.length == "long":
        template += "\n\n## Additional Notes:\n[Expand with more details]\n"
    
    return NoteGenerationResponse(
        content=template,
        template_used=f"{request.style}_{request.length}"
    )


if __name__ == "__main__":
    # Run the server
    mcp.run() 