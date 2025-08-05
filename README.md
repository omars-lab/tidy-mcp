# tidy-mcp
My own personal MCP to help keep me clean and organized.


# MCP Server for Note Taking Companion

This directory contains a Model Context Protocol (MCP) server built with the Python `fastmcp` library. The server provides resources, tools, and prompts for note-taking workflows.

## Features

- **Resources**: Note templates for different use cases
- **Tools**: Note analysis and content processing
- **Prompts**: Note generation with different styles and lengths

## Installation

### Option 1: Using Makefile (Recommended)

1. Create conda environment and install dependencies:
```bash
make setup-env
```

2. Run the server:
```bash
make run
```

3. Run tests:
```bash
make test
```

### Option 2: Manual Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python server.py
```

## Server Components

### Resources
- `note_templates`: Provides pre-defined note templates for meetings, daily reflections, etc.

### Tools
- `analyze_note`: Analyzes note content and extracts insights like word count, action items, and key points

### Prompts
- `generate_note`: Generates notes based on topic, style, and length preferences

## Integration with AI CLI Tools

### Amazon Q CLI

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
    "note-taking-companion": {
      "command": "python",
      "args": ["/path/to/your/src/notes_mcp/server.py"],
"env": {
  "PYTHONPATH": "/path/to/your/src/notes_mcp"
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

### Gemini CLI

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
      "note-taking": {
        "command": "python",
        "args": ["/path/to/your/src/notes_mcp/server.py"],
"cwd": "/path/to/your/src/notes_mcp"
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

### Claude Code CLI

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
    "note-taking-companion": {
      "command": "python",
      "args": ["/path/to/your/src/notes_mcp/server.py"],
"workingDirectory": "/path/to/your/src/notes_mcp"
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

## Makefile Commands

The Makefile provides convenient commands for managing the MCP server:

- `make setup-env` - Create conda environment 'mcp' and install dependencies
- `make install` - Install requirements in existing mcp environment
- `make test` - Run the test suite
- `make run` - Run the MCP server
- `make clean` - Remove conda environment
- `make info` - Show environment information
- `make help` - Show all available commands

## Configuration Options

- **Templates**: Add new note templates in the `get_note_templates()` function
- **Analysis Logic**: Enhance the `analyze_note()` function with more sophisticated analysis
- **Generation Styles**: Add new note generation styles in the `generate_note()` function

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed:
```bash
# Using conda environment
make install

# Or manually
conda run -n mcp pip install -r requirements.txt
```

2. **Conda Environment Issues**: If the environment doesn't exist:
```bash
make setup-env
```

3. **Permission Issues**: Make sure the server file is executable:
```bash
chmod +x server.py
```

4. **Path Issues**: Use absolute paths in CLI configurations

5. **Port Conflicts**: The server runs on the default MCP port. Ensure no other MCP servers are using the same port.

### Debug Mode

Run the server in debug mode for more verbose output:
```bash
python -u server.py --debug
```

## Contributing

To extend the server functionality:

1. Add new resources by creating functions decorated with `@app.resource()`
2. Add new tools by creating functions decorated with `@app.tool()`
3. Add new prompts by creating functions decorated with `@app.prompt()`
4. Update the README with new features

## License

This project is part of the genai-companion-note-taking repository and follows the same license terms. 