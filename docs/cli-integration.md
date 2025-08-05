# CLI Integration Guide

This guide explains how to integrate the tidy-mcp server with various AI CLI tools.

## Amazon Q CLI

Amazon Q CLI supports MCP servers through its configuration. To integrate this server:

1. **Install Amazon Q CLI** (if not already installed):
```bash
# Follow Amazon's official installation guide
```

2. **Configure MCP Server**:
Create or edit your Amazon Q configuration file (typically `~/.amazon-q/config.json`):

```json
{
  "mcpServers": {
    "tidy-mcp": {
      "command": "python",
      "args": ["/path/to/tidy-mcp/src/notes_mcp/server.py"],
      "env": {
        "PYTHONPATH": "/path/to/tidy-mcp/src/notes_mcp"
      }
    }
  }
}
```

3. **Usage**:
```bash
# Start Amazon Q CLI
amazon-q

# The server will be available for note-taking operations
```

## Gemini CLI

Gemini CLI supports MCP servers for enhanced functionality:

1. **Install Gemini CLI**:
```bash
# Follow Google's official installation guide
```

2. **Configure MCP Server**:
Create a configuration file for Gemini CLI (typically `~/.gemini/settings.json`):

```json
{
  "mcp": {
    "servers": {
      "tidy-mcp": {
        "command": "python",
        "args": ["/path/to/tidy-mcp/src/notes_mcp/server.py"],
        "cwd": "/path/to/tidy-mcp/src/notes_mcp"
      }
    }
  }
}
```

3. **Usage**:
```bash
# Start Gemini CLI with MCP support
gemini --mcp

# Access note-taking features through Gemini
```

## Claude Code CLI

Claude Code CLI can integrate with MCP servers for enhanced development workflows:

1. **Install Claude Code CLI**:
```bash
# Follow Anthropic's official installation guide
```

2. **Configure MCP Server**:
Create a configuration file for Claude Code CLI (typically `~/.claude/config.json`):

```json
{
  "mcpServers": {
    "tidy-mcp": {
      "command": "python",
      "args": ["/path/to/tidy-mcp/src/notes_mcp/server.py"],
      "workingDirectory": "/path/to/tidy-mcp/src/notes_mcp"
    }
  }
}
```

3. **Usage**:
```bash
# Start Claude Code CLI
claude-code

# The note-taking server will be available for documentation and note generation
```

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

## Troubleshooting

### Common Issues

1. **Path Issues**: Use absolute paths in CLI configurations
2. **Port Conflicts**: The server runs on the default MCP port. Ensure no other MCP servers are using the same port.
3. **Permission Issues**: Make sure the server file is executable:
```bash
chmod +x src/notes_mcp/server.py
```

### Debug Mode

Run the server in debug mode for more verbose output:
```bash
python -u src/notes_mcp/server.py --debug
``` 