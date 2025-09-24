# Tidy MCP Server - Repository Guidelines

## Project Structure & Module Organization

- **Source Code**: Located in `src/tidy_mcp/` directory. Organized as a Python package.
- **Tests**: Found in `tst/tidy_mcp/` directory. Mirrors the src structure.
- **Configuration**: `pyproject.toml` for package configuration and dependencies.
- **Documentation**: `README.md` for comprehensive project documentation.

## Package Structure

```
src/
├── tidy_mcp/
│   ├── __init__.py      # Package metadata and exports
│   ├── __main__.py      # Module entry point (python -m tidy_mcp)
│   └── server.py        # MCP server implementation
tst/
└── tidy_mcp/
    └── test_server.py   # Test suite
```

## Build, Test, and Development Commands

The project uses a comprehensive Makefile for all development tasks:

### 🔧 Setup & Installation
```bash
make setup-env      # Create conda environment and install package
make install        # Install package in existing environment
make install-dev    # Install with development dependencies
make uninstall      # Uninstall the package
```

### 🚀 Development
```bash
make run            # Run the MCP server
make run-cli        # Run using the CLI tool
make run-module     # Run as a Python module
make dev            # Run in development mode
```

### 🧪 Testing & Quality
```bash
make test           # Run the test suite
make test-verbose   # Run tests with verbose output
make lint           # Run code linting with flake8
make format         # Format code with black
make check          # Run all quality checks
```

### 📦 Building & Distribution
```bash
make build          # Build the package
make dist           # Create distribution packages
make clean-build    # Clean build artifacts
```

### 🧹 Maintenance
```bash
make clean          # Remove environment and clean build artifacts
make clean-env      # Remove only the conda environment
make info           # Show environment and package information
make deps           # Show installed dependencies
```

### 🔗 Integration
```bash
make configure-gemini  # Configure Gemini slash commands
make simulate-mcp      # Simulate MCP note-taking workflow
```

### 📚 Documentation
```bash
make docs            # Generate documentation
make readme          # Update README with package info
```

### 🆘 Help
```bash
make help            # Show all available commands
```

## Multiple Execution Methods

The MCP server can be run in several ways:

1. **Direct Python script**: `python src/tidy_mcp/server.py`
2. **CLI tool**: `tidy-mcp`
3. **Python module**: `python -m tidy_mcp`
4. **Makefile commands**: `make run`, `make run-cli`, `make run-module`

## Coding Style & Naming Conventions

- **Indentation**: Use 4 spaces for Python (PEP 8).
- **Linting**: flake8 configured for code consistency.
- **Formatting**: Black for automatic code formatting.
- **Naming**: Use snake_case for variables and functions, PascalCase for classes.
- **Type Hints**: Use type hints for function parameters and return values.

## Testing Guidelines

- **Framework**: pytest for Python testing.
- **Coverage**: Aim for 80% coverage on new code.
- **Naming**: Test files should end with `test_*.py`.
- **Structure**: Tests mirror the source code structure.

## Quality Assurance

The project includes several quality tools:

- **Black**: Code formatting with 88 character line length
- **Flake8**: Linting with PEP 8 compliance
- **Pytest**: Testing framework
- **Build**: Package building and distribution

Run all quality checks with:
```bash
make check
```

## Package Management

- **Dependencies**: Managed through `pyproject.toml`
- **Development Dependencies**: Include testing and formatting tools
- **Installation**: Editable install for development (`pip install -e .`)
- **Distribution**: Build wheel and source distributions

## Environment Management

- **Conda Environment**: `tidy-mcp` for isolated development
- **Python Version**: 3.12+
- **Package Isolation**: All dependencies managed in conda environment

## Commit & Pull Request Guidelines

- **Commit Messages**: Use imperative mood, e.g., "Add feature", "Fix bug"
- **Pull Requests**: Include a clear description and link to relevant issues
- **Code Review**: Ensure all quality checks pass before merging
- **Documentation**: Update README.md for new features or changes

## Development Workflow

1. **Setup**: `make setup-env`
2. **Development**: Make changes in `src/tidy_mcp/`
3. **Quality**: `make check` (format, lint, test)
4. **Testing**: `make test` or `make test-verbose`
5. **Building**: `make build` to verify package builds correctly
6. **Documentation**: Update README.md as needed

## MCP Protocol Integration

This server implements the Model Context Protocol (MCP) and provides:

- **Resources**: Note templates and metadata
- **Tools**: Note analysis and processing
- **Prompts**: Note generation and formatting

For more information about MCP, visit: https://modelcontextprotocol.io/
