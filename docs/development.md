# Development Setup

Guide to setting up a development environment.

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv)
- Git
- FL Studio (optional, for testing FL Studio features)
- loopMIDI (optional, for testing MIDI features)

## Setup

```bash
# Clone repository
git clone https://github.com/quinnjr/fruityloops-mcp.git
cd fruityloops-mcp

# Install dependencies
uv sync --all-extras

# Install git hooks
./install-hooks.sh  # Unix/Linux/macOS
./install-hooks.ps1  # Windows
```

## Project Structure

```
fruityloops-mcp/
├── src/fruityloops_mcp/    # Source code
│   ├── server.py           # MCP server
│   ├── midi_interface.py   # MIDI interface
│   ├── __init__.py
│   └── __main__.py
├── tests/                  # Test files
├── docs/                   # Documentation
├── .github/                # GitHub config
│   └── workflows/          # CI/CD
├── .githooks/              # Git hooks
└── pyproject.toml          # Project config
```

## Development Workflow

### Running Locally

```bash
# Run server
uv run fruityloops-mcp

# Run with Python
uv run python -m fruityloops_mcp
```

### Testing

```bash
# Run all tests
uv run pytest

# Run specific test
uv run pytest tests/test_midi.py

# With coverage
uv run pytest --cov

# Watch mode (requires pytest-watch)
uv run ptw
```

### Linting

```bash
# Check code
uv run ruff check .

# Fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

### Documentation

```bash
# Install docs dependencies
uv sync --extra docs

# Serve docs locally
uv run mkdocs serve
# Visit http://localhost:8000

# Build docs
uv run mkdocs build
```

## Docker Development

```bash
# Build container
docker-compose build

# Run tests
docker-compose run ci

# Interactive shell
docker-compose run test
```

## Making Changes

1. Create a branch: `git checkout -b feature/your-feature`
2. Make changes
3. Run tests: `uv run pytest`
4. Lint code: `uv run ruff check .`
5. Commit: `git commit -m "feat: your feature"`
6. Push: `git push origin feature/your-feature`
7. Create Pull Request

## Debugging

### Server Debugging

```python
# Add to server.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### MIDI Debugging

```python
# List ports
from fruityloops_mcp.midi_interface import MIDIInterface
midi = MIDIInterface()
print(midi.list_ports())
```

## Common Tasks

### Adding a New Tool

1. Add tool definition in `server.py` `list_tools()`
2. Add handler in `_execute_tool()`
3. Add tests in `tests/test_server.py`
4. Update documentation

### Adding Dependencies

```bash
# Runtime dependency
uv add package-name

# Dev dependency
uv add --dev package-name

# Docs dependency
uv add --group docs package-name
```

## Resources

- [Testing Guide](testing.md)
- [Git Workflow](git-workflow.md)
- [API Reference](api/server.md)

