

# # Example Resource: Note Templates
# class NoteTemplate(BaseModel):
#     """A note template resource."""

#     id: str = Field(description="Unique identifier for the template")
#     name: str = Field(description="Name of the template")
#     content: str = Field(description="Template content with placeholders")
#     category: str = Field(description="Category of the template")
#     created_at: str = Field(description="Creation timestamp")


# @mcp.resource("data://note_templates")
# async def get_note_templates() -> List[NoteTemplate]:
#     """Get available note templates."""
#     templates = [
#         NoteTemplate(
#             id="meeting-notes",
#             name="Meeting Notes Template",
#             content="# Meeting Notes\n\n## 📅 Date: {{date}}\n## 👥 Attendees: {{attendees}}\n## 📋 Agenda: {{agenda}}\n\n## 📝 Notes:\n\n## ✅ Action Items:\n- [ ] \n\n## 🔄 Follow-up:\n",
#             category="meetings",
#             created_at=datetime.now().isoformat(),
#         ),
#         NoteTemplate(
#             id="daily-reflection",
#             name="Daily Reflection Template",
#             content="# Daily Reflection - {{date}}\n\n## 🎯 Today's Goals:\n1. \n2. \n3. \n\n## ✅ Accomplishments:\n\n## 🤔 Challenges:\n\n## 📚 Learnings:\n\n## 🎯 Tomorrow's Focus:\n",
#             category="personal",
#             created_at=datetime.now().isoformat(),
#         ),
#     ]
#     return templates




# # Example Tool: Note Analysis
# class NoteAnalysisRequest(BaseModel):
#     """Request model for note analysis."""

#     content: str = Field(description="Note content to analyze")
#     analysis_type: str = Field(
#         description="Type of analysis: 'summary', 'action_items', 'key_points'"
#     )

# class NoteAnalysisResponse(BaseModel):
#     """Response model for note analysis."""

#     analysis: str = Field(description="Analysis result")
#     confidence: float = Field(description="Confidence score (0-1)")
#     metadata: Dict[str, Any] = Field(description="Additional metadata")


# # Example Prompt: Note Generation
# class NoteGenerationRequest(BaseModel):
#     """Request model for note generation."""
#     topic: str = Field(description="Topic for the note")
#     style: str = Field(description="Writing style: 'formal', 'casual', 'bullet_points'")
#     length: str = Field(description="Desired length: 'short', 'medium', 'long'")

# class NoteGenerationResponse(BaseModel):
#     """Response model for note generation."""
#     content: str = Field(description="Generated note content")
#     template_used: str = Field(description="Template that was used")

# @mcp.tool("analyze_note")
# async def analyze_note(request: NoteAnalysisRequest) -> NoteAnalysisResponse:
#     """Analyze note content and extract insights."""
#     content = request.content.lower()

# @mcp.prompt("generate_note")
# async def generate_note(request: NoteGenerationRequest) -> NoteGenerationResponse:
#     """Generate a note based on the given topic and style."""




## Example Usage

Once integrated with any of the CLI tools, you can use the server's capabilities:

### Using Resources
```python
# Get available note templates
templates = await get_note_templates()
for template in templates:
    print(f"Template: {template.name}")
```

### Using Tools
```python
# Analyze a note
analysis = await analyze_note({
    "content": "Meeting notes with action items...",
    "analysis_type": "action_items"
})
print(f"Analysis: {analysis.analysis}")
```

### Using Prompts
```python
# Generate a note
note = await generate_note({
    "topic": "Project Planning",
    "style": "bullet_points",
    "length": "medium"
})
print(f"Generated note: {note.content}")
```