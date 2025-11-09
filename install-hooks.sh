#!/bin/bash
#
# Install git hooks for FL Studio MCP Server
#

set -e

echo "Installing git hooks..."

# Configure git to use .githooks directory
git config core.hooksPath .githooks

# Make hooks executable
chmod +x .githooks/commit-msg
chmod +x .githooks/pre-commit
chmod +x .githooks/pre-push
chmod +x .githooks/prepare-commit-msg

echo "[OK] Git hooks installed successfully!"
echo ""
echo "Installed hooks:"
echo "  - commit-msg: Enforce Conventional Commits"
echo "  - pre-commit: Run linting and formatting"
echo "  - pre-push: Enforce git-flow and run tests"
echo "  - prepare-commit-msg: Help with commit messages"
echo ""
echo "To uninstall: git config --unset core.hooksPath"

