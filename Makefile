# AGENTS: Guidelines for maintaining this Makefile
# ================================================
# 
# When adding new targets:
# 1. Follow the pattern: target-name: ## Description of what the target does
# 2. Use .PHONY declarations for all targets that don't create files
# 3. Keep targets focused on single responsibilities
# 4. Use composable targets (e.g., target1 target2) for complex workflows
# 5. Always include a description after ## for the help target
# 6. Test new targets with 'make help' to ensure they appear correctly
# 7. ALWAYS run 'make help' after making any changes to verify the Makefile works
#
# CRITICAL: Indentation Rules
# - Commands under targets MUST be indented with TABS, not spaces
# - Use 'make -n <target>' to test syntax before running
# - If targets don't work, check indentation with: sed -n 'X,Yp' Makefile | cat -e
# - Replace spaces with tabs: sed -i '' 's/^    /\t/' Makefile
#
# Target naming conventions:
# - Use kebab-case for target names
# - Prefix with action: commit-, push-, update-, etc.
# - Use descriptive names that indicate the target's purpose
#
# Submodule considerations:
# - Always use 'git add .' to stage submodule reference changes
# - Submodule updates require committing the reference change in parent repo
# - Use 'git submodule update --remote <submodule>' to update submodules
#
# Example of good target structure:
# target-name: dependency1 dependency2 ## Clear description of what this does
# 	@echo "Starting action..."
# 	command1
# 	command2
# 	@echo "Action completed successfully!"

# All targets that don't create files should be declared as .PHONY
.PHONY: help prompt generate-weekly-report configure-context tst extract-key-points check-resume setup-knowledge update-prompts enable-submodule-status enable-recursive-push fix-submodule-detached-head commit-submodule-updates push-with-submodules commit push commit-push

# Standard Makefile Variables (include these in all Makefiles)
SHELL := /bin/bash
MAKEFILE_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

# Project-specific variables
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
	@echo ""
	@echo "📁 Submodule Management:"
	@echo "  update-prompts      - Pull latest changes from the prompts submodule"
	@echo "  enable-submodule-status - Enable submodule status in git status output"
	@echo "  enable-recursive-push - Enable recursive submodule pushes"
	@echo "  fix-submodule-detached-head - Fix detached HEAD in prompts submodule"
	@echo "  commit-submodule-updates - Commit submodule reference changes"
	@echo "  push-with-submodules - Push commits and submodules recursively"
	@echo ""
	@echo "🔧 Git Operations:"
	@echo "  commit              - Stage and commit changes (interactive message)"
	@echo "  push                - Push committed changes to remote"
	@echo "  commit-push         - Commit and push changes (interactive message)"

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

# =============================================================================
# Submodule Support Targets
# =============================================================================

update-prompts: ## Pull latest changes from the prompts submodule
	@echo "Updating prompts submodule..."
	git submodule update --remote prompts
	@echo "Prompts submodule updated successfully!"

enable-submodule-status: ## Enable submodule status in git status output
	@if [ "$$(git config --get status.submodulesummary)" != "1" ]; then \
		echo "Enabling submodule status in git status..."; \
		git config status.submodulesummary 1; \
		echo "Submodule status enabled! Run 'git status' to see submodule details."; \
	else \
		echo "Submodule status is already enabled."; \
	fi

enable-recursive-push: ## Enable recursive submodule pushes
	@if [ "$$(git config --get push.recurseSubmodules)" != "on-demand" ]; then \
		echo "Enabling recursive submodule pushes..."; \
		git config --global push.recurseSubmodules on-demand; \
		echo "Recursive submodule pushes enabled!"; \
	else \
		echo "Recursive submodule pushes are already enabled."; \
	fi

fix-submodule-detached-head: ## Fix detached HEAD in prompts submodule
	@echo "Fixing detached HEAD in prompts submodule..."
	cd prompts && git checkout -b main origin/main 2>/dev/null || git checkout main
	@echo "Submodule HEAD fixed!"

commit-submodule-updates: ## Commit submodule reference changes
	@echo "Committing submodule reference changes..."
	git add prompts
	@if [ -n "$$(git status --porcelain)" ]; then \
		git commit -m "Update prompts submodule"; \
		echo "Submodule updates committed successfully!"; \
	else \
		echo "No submodule changes to commit."; \
	fi

push-with-submodules: ## Push commits and submodules recursively
	@echo "Pushing commits and submodules..."
	git push --recurse-submodules=on-demand
	@echo "Push completed successfully!"

# =============================================================================
# Basic Git Operations
# =============================================================================

commit: ## Stage and commit changes (interactive message)
	@echo "Staging all changes..."
	git add .
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "Enter commit message:"; \
		read -r commit_msg; \
		git commit -m "$$commit_msg"; \
		echo "Changes committed successfully!"; \
	else \
		echo "No changes to commit."; \
	fi

push: ## Push committed changes to remote
	@echo "Pushing to remote..."
	git push
	@echo "Changes pushed successfully!"

commit-push: commit push ## Commit and push changes (interactive message)
