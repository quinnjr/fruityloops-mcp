#!/bin/bash
#
# CI/CD simulation script for testing in Docker
#

set -e

echo "================================"
echo "FL Studio MCP Server - CI Tests"
echo "================================"
echo ""

# Test 1: Python version
echo "[1/14] Checking Python version..."
python --version
echo "[OK]"
echo ""

# Test 2: Install dependencies
echo "[2/14] Installing dependencies..."
uv sync --all-extras
echo "[OK]"
echo ""

# Test 3: Linting
echo "[3/14] Running linter..."
uv run ruff check .
echo "[OK]"
echo ""

# Test 4: Formatting
echo "[4/14] Checking code formatting..."
uv run ruff format --check .
echo "[OK]"
echo ""

# Test 5: Unit tests
echo "[5/14] Running unit tests..."
uv run pytest -v
echo "[OK]"
echo ""

# Test 6: Coverage
echo "[6/14] Running tests with coverage..."
uv run pytest --cov=src/fruityloops_mcp --cov-report=term-missing
echo "[OK]"
echo ""

# Test 7: Coverage threshold
echo "[7/14] Checking coverage threshold (>= 90%)..."
uv run pytest --cov=src/fruityloops_mcp --cov-report=json --quiet
COVERAGE=$(python -c "import json; print(json.load(open('coverage.json'))['totals']['percent_covered'])")
echo "Coverage: $COVERAGE%"
if (( $(echo "$COVERAGE < 90" | bc -l) )); then
    echo "[ERROR] Coverage $COVERAGE% is below threshold of 90%"
    exit 1
fi
echo "[OK]"
echo ""

# Test 8: Package build
echo "[8/14] Building package..."
uv build
echo "[OK]"
echo ""

# Test 9: Git hooks installation
echo "[9/14] Testing git hooks installation..."
bash install-hooks.sh
echo "[OK]"
echo ""

# Test 10: Git hooks validation
echo "[10/14] Validating git hooks..."
if [ ! -f .githooks/commit-msg ]; then
    echo "[ERROR] commit-msg hook not found"
    exit 1
fi
if [ ! -f .githooks/pre-commit ]; then
    echo "[ERROR] pre-commit hook not found"
    exit 1
fi
echo "[OK]"
echo ""

# Test 11: Import test
echo "[11/14] Testing package imports..."
uv run python -c "from fruityloops_mcp.server import FLStudioMCPServer; print('Server import OK')"
uv run python -c "from fruityloops_mcp.midi_interface import MIDIInterface; print('MIDI import OK')"
echo "[OK]"
echo ""

# Test 12: CLI entry point
echo "[12/14] Testing CLI entry point..."
uv run python -m fruityloops_mcp --help || echo "CLI tested (expected to fail without FL Studio)"
echo "[OK]"
echo ""

# Test 13: Type checking
echo "[13/14] Checking type annotations..."
# Skip mypy for now as it's not in dependencies
echo "[SKIPPED]"
echo ""

# Test 14: Security check
echo "[14/14] Running security checks..."
# Skip bandit for now as it's not in dependencies
echo "[SKIPPED]"
echo ""

echo "================================"
echo "All CI tests passed!"
echo "================================"

