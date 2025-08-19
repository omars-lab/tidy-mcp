ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
GIT_IGNORE_CONTEXT=${ROOT_DIR}/context/.gitignore

# Include the MCP Makefile
include $(ROOT_DIR)/Makefile-mcp

# Default target - show help
.DEFAULT_GOAL := help
.PHONY: help
help:
	@echo "Notes MCP Server - Available Commands:"
	@echo ""
	@echo "🔧 Setup & Installation:"
	@echo "  setup-env    - Create conda environment and install package in editable mode"
	@echo "  install      - Install package in editable mode in existing environment"
	@echo "  install-dev  - Install package with development dependencies"
	@echo "  uninstall    - Uninstall the package from the environment"
	@echo ""
	@echo "🚀 Development:"
	@echo "  run          - Run the MCP server"
	@echo "  run-cli      - Run the MCP server using the CLI tool"
	@echo "  run-module   - Run the MCP server as a Python module"
	@echo "  dev          - Run the server in development mode with auto-reload"
	@echo ""
	@echo "🧪 Testing & Quality:"
	@echo "  test         - Run the test suite"
	@echo "  test-verbose - Run tests with verbose output"
	@echo "  lint         - Run code linting with flake8"
	@echo "  format       - Format code with black"
	@echo "  check        - Run all quality checks (lint + format + test)"
	@echo ""
	@echo "📦 Building & Distribution:"
	@echo "  build        - Build the package distribution"
	@echo "  clean-build  - Clean build artifacts"
	@echo "  dist         - Create distribution packages"
	@echo ""
	@echo "🧹 Maintenance:"
	@echo "  clean        - Remove conda environment and clean build artifacts"
	@echo "  clean-env    - Remove only the conda environment"
	@echo "  info         - Show environment and package information"
	@echo "  deps         - Show installed dependencies"
	@echo ""
	@echo "🔗 Integration:"
	@echo "  configure-gemini - Configure Gemini slash commands"
	@echo "  simulate-mcp     - Simulate MCP note-taking workflow"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  docs         - Generate documentation"
	@echo "  readme       - Update README with current package info"
	@echo ""
	@echo "🎯 Project-Specific:"
	@echo "  prompt              - Test gemini prompt"
	@echo "  generate-weekly-report - Generate weekly report using gemini"
	@echo "  configure-context   - Set up context links and gitignore"
	@echo "  extract-key-points  - Extract key points using gemini"
	@echo "  check-resume        - Check resume using gemini"
	@echo "  setup-knowledge     - Set up knowledge base links"

prompt:
	echo what tools do you have access to | gemini --prompt

generate-weekly-report:
	gemini -y --prompt prompts/commands/noteplan/generate-weekly-summary.toml 
	
configure-context:
	@ test -L ${ROOT_DIR}/context/NotePlan3 \
		|| ln -s "${HOME}/Library/Containers/co.noteplan.NotePlan3/Data/Library/Application Support/co.noteplan.NotePlan3" \
			 "${ROOT_DIR}/context/NotePlan3"
	@ (test -f ${GIT_IGNORE_CONTEXT} && grep -q NotePlan3 ${GIT_IGNORE_CONTEXT}) \
		|| echo "context/NotePlan3" >> ${GIT_IGNORE_CONTEXT}
	@ test -L ${ROOT_DIR}/context/personalbook \
		|| ln -s "${HOME}/Workspace/git/personalbook" \
			 "${ROOT_DIR}/context/personalbook"
	@ (test -f ${GIT_IGNORE_CONTEXT} && grep -q personalbook ${GIT_IGNORE_CONTEXT}) \
		|| echo "context/personalbook" >> ${GIT_IGNORE_CONTEXT}

# Test target that reuses the MCP test target
.PHONY: tst
tst: test

# Add instrucitons to add dates based on file location ...
# Only add date to root todo
# Teach it about themes ...

extract-key-points:
	cat prompts/point-extraction.prompt.md | gemini -p

check-resume:
	cat prompts/check-resume.prompt.md | gemini -p

setup-knowledge:
	mkdir -p knowledge
	test -L knowledge/promo-doc.md || \
		(ln -s "/Users/omareid/Library/Containers/co.noteplan.NotePlan3/Data/Library/Application Support/co.noteplan.NotePlan3/Notes/🎩 Role/2023 Promo.txt" knowledge/promo-doc.md)
