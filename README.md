# Notes MCP Server

A Model Context Protocol (MCP) server for note-taking workflows and personal knowledge management.

## Features

- **Note Templates**: Pre-built templates for meetings, daily reflections, and more
- **Note Analysis**: Analyze note content for action items, key points, and summaries
- **Note Generation**: Generate notes based on topics and writing styles
- **MCP Integration**: Full Model Context Protocol compliance

## Installation

### Development Installation (Recommended)

For development, install in editable mode using the Makefile:

```bash
# Setup complete development environment
make setup-env

# Or install with development dependencies
make install-dev
```

### Manual Installation

```bash
# Using pip
pip install -e .

# Production installation
pip install notes-mcp
```

## Usage

### Quick Start

```bash
# Setup environment and run server
make setup-env
make run

# Or run as a module
make run-module

# Or run directly
python -m notes_mcp
```

### As a Python Package

```python
from notes_mcp import mcp, NoteTemplate

# Access the MCP server
server = mcp

# Use note templates
templates = await get_note_templates()
```

### As a Command Line Tool

After installation, you can run the MCP server directly:

```bash
notes-mcp
```

### As a Python Module

You can also run the MCP server as a Python module:

```bash
python -m notes_mcp
```

### Using the Makefile

The project includes a comprehensive Makefile with many useful commands:

#### 🔧 Setup & Installation
```bash
make setup-env      # Create conda environment and install package
make install        # Install package in existing environment
make install-dev    # Install with development dependencies
make uninstall      # Uninstall the package
```

#### 🚀 Development
```bash
make run            # Run the MCP server
make run-cli        # Run using the CLI tool
make run-module     # Run as a Python module
make dev            # Run in development mode
```

#### 🧪 Testing & Quality
```bash
make test           # Run the test suite
make test-verbose   # Run tests with verbose output
make lint           # Run code linting
make format         # Format code with black
make check          # Run all quality checks
```

#### 📦 Building & Distribution
```bash
make build          # Build the package
make dist           # Create distribution packages
make clean-build    # Clean build artifacts
```

#### 🧹 Maintenance
```bash
make clean          # Remove environment and clean build artifacts
make clean-env      # Remove only the conda environment
make info           # Show environment and package information
make deps           # Show installed dependencies
```

#### 🔗 Integration
```bash
make configure-gemini  # Configure Gemini slash commands
make simulate-mcp      # Simulate MCP note-taking workflow
```

#### 📚 Documentation
```bash
make docs            # Generate documentation
make readme          # Update README with package info
```

#### 🆘 Help
```bash
make help            # Show all available commands
```

## Development

### Project Structure

```
src/
├── notes_mcp/
│   ├── __init__.py      # Package metadata
│   └── server.py        # MCP server implementation
tst/
└── notes_mcp/
    └── test_server.py   # Test suite
```

### Development Workflow

The Makefile provides a complete development workflow:

```bash
# Setup development environment
make setup-env

# Run quality checks
make check

# Start development server
make dev

# Run tests
make test
```

### Code Quality

This project uses several tools for code quality:

- **Black**: Code formatting
- **Flake8**: Linting
- **Pytest**: Testing

Run all quality checks:

```bash
make check
```

Or run individual checks:

```bash
make format    # Format code
make lint      # Run linting
make test      # Run tests
```

### Building and Distribution

```bash
# Build the package
make build

# Create distribution packages
make dist

# Clean build artifacts
make clean-build
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## MCP Protocol

This server implements the Model Context Protocol (MCP) and provides:

- **Resources**: Note templates and metadata
- **Tools**: Note analysis and processing
- **Prompts**: Note generation and formatting

For more information about MCP, visit: https://modelcontextprotocol.io/ 