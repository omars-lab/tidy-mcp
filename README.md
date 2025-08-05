# tidy-mcp

A personal Model Context Protocol (MCP) server built with Python `fastmcp` to help keep me clean and organized. This server provides resources, tools, and prompts for personal note-taking and organization workflows.

## Features

- **Resources**: Note templates for different personal use cases
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
python src/notes_mcp/server.py
```

## Server Components

### Resources
- `note_templates`: Provides pre-defined note templates for meetings, daily reflections, etc.

### Tools
- `analyze_note`: Analyzes note content and extracts insights like word count, action items, and key points

### Prompts
- `generate_note`: Generates notes based on topic, style, and length preferences

## CLI Integration

For detailed instructions on integrating this MCP server with various AI CLI tools (Amazon Q CLI, Gemini CLI, Claude Code CLI), see the [CLI Integration Guide](docs/cli-integration.md).

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
chmod +x src/notes_mcp/server.py
```

4. **Port Conflicts**: The server runs on the default MCP port. Ensure no other MCP servers are using the same port.

### Debug Mode

Run the server in debug mode for more verbose output:
```bash
python -u src/notes_mcp/server.py --debug
```

For CLI integration troubleshooting, see the [CLI Integration Guide](docs/cli-integration.md).

## Contributing

To extend the server functionality:

1. Add new resources by creating functions decorated with `@app.resource()`
2. Add new tools by creating functions decorated with `@app.tool()`
3. Add new prompts by creating functions decorated with `@app.prompt()`
4. Update the README with new features

## License

This project is licensed under the MIT License. 