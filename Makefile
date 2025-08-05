ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
GIT_IGNORE_CONTEXT=${ROOT_DIR}/context/.gitignore

# Include the MCP Makefile
include $(ROOT_DIR)/Makefile-mcp

# Default target - show help
.DEFAULT_GOAL := help
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  prompt              - Test gemini prompt"
	@echo "  generate-weekly-report - Generate weekly report using gemini"
	@echo "  configure-context   - Set up context links and gitignore"
	@echo "  tst                 - Run tests (uses MCP test target)"
	@echo "  setup-env           - Create conda environment 'mcp' and install dependencies"
	@echo "  install             - Install requirements in the mcp environment"
	@echo "  test                - Run the MCP server test suite"
	@echo "  run                 - Run the MCP server"
	@echo "  clean               - Remove conda environment"
	@echo "  info                - Show conda environment info"

prompt:
	echo what tools do you have access to | gemini --prompt

generate-weekly-report:
	gemini -y --prompt prompts/generate-weekly-summary.md 
	
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
