# Contributing to FL Studio MCP Server

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv)
- FL Studio (for testing FL Studio API features)
- [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) (for MIDI features)
- Git

### Development Setup

```bash
# Clone the repository
git clone https://github.com/quinnjr/fruityloops-mcp.git
cd fruityloops-mcp

# Install dependencies
uv sync --all-extras

# Install git hooks
./install-hooks.sh  # Unix/Linux/macOS
./install-hooks.ps1  # Windows
```

## Development Workflow

### 1. Create a Branch

Follow git-flow conventions:

```bash
# For new features
git checkout -b feature/your-feature-name

# For bug fixes
git checkout -b bugfix/issue-description

# For hotfixes (production issues)
git checkout -b hotfix/critical-fix
```

### 2. Make Changes

- Write clean, readable code
- Follow existing code style
- Add docstrings to functions and classes
- Update tests for your changes

### 3. Test Your Changes

```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run linting
uv run ruff check .

# Run formatting
uv run ruff format .
```

### 4. Commit Your Changes

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format: type(scope): description
git commit -m "feat: add new MIDI tool"
git commit -m "fix(server): resolve connection issue"
git commit -m "docs: update installation guide"
```

**Valid types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes
- `perf`: Performance improvements
- `ci`: CI/CD changes

### 5. Push and Create Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name

# Create PR on GitHub
# - Fill out the PR template
# - Link related issues
# - Wait for CI checks to pass
# - Request review
```

## Pull Request Guidelines

### PR Title

Must follow Conventional Commits format:

```
feat: add MIDI velocity control
fix(api): resolve timeout issue
docs: update README with examples
```

### PR Description

Use the provided template and include:

- Clear description of changes
- Related issue numbers
- Testing performed
- Screenshots (if applicable)

### PR Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Linting passes
- [ ] Formatting passes
- [ ] All tests pass
- [ ] Coverage maintained/improved
- [ ] Conventional commit format

## Coding Standards

### Python Style

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use Ruff for linting and formatting

### Documentation

- Add docstrings to all public functions/classes
- Use Google-style docstrings
- Keep README and docs up to date

### Testing

- Write tests for new features
- Maintain >90% coverage
- Test edge cases and error handling
- Use pytest fixtures for common setup

## Project Structure

```
fruityloops-mcp/
├── src/fruityloops_mcp/    # Source code
│   ├── __init__.py
│   ├── __main__.py
│   ├── server.py           # MCP server
│   └── midi_interface.py   # MIDI interface
├── tests/                  # Test files
├── docs/                   # Documentation
├── .github/                # GitHub config
│   ├── workflows/          # CI/CD
│   └── ISSUE_TEMPLATE/     # Issue templates
├── .githooks/              # Git hooks
└── pyproject.toml          # Project config
```

## Testing

### Running Tests

```bash
# All tests
uv run pytest

# Specific test file
uv run pytest tests/test_midi.py

# Specific test function
uv run pytest tests/test_midi.py::test_connect_success

# With verbose output
uv run pytest -v

# With coverage
uv run pytest --cov=src/fruityloops_mcp --cov-report=html
```

### Writing Tests

```python
import pytest
from unittest.mock import Mock, patch

def test_feature():
    """Test description."""
    # Arrange
    ...

    # Act
    result = function_under_test()

    # Assert
    assert result == expected
```

## Documentation

### Building Documentation

```bash
# Install docs dependencies
uv sync --extra docs

# Build documentation
uv run mkdocs build

# Serve locally
uv run mkdocs serve
# Visit http://localhost:8000
```

### Writing Documentation

- Use Markdown
- Add code examples
- Keep it concise and clear
- Update API docs when changing code

## Release Process

Releases are automated via GitHub Actions:

1. Update version in `pyproject.toml` and `src/fruityloops_mcp/__init__.py`
2. Update `CHANGELOG.md`
3. Create and push a tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
4. GitHub Actions will:
   - Build the package
   - Create a GitHub release
   - Publish to PyPI

## Getting Help

- [GitHub Discussions](https://github.com/quinnjr/fruityloops-mcp/discussions)
- [Open an issue](https://github.com/quinnjr/fruityloops-mcp/issues)
- Read the [documentation](https://quinnjr.github.io/fruityloops-mcp/)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to ask questions in:
- GitHub Discussions
- GitHub Issues
- Pull Request comments

Thank you for contributing! 🎉

