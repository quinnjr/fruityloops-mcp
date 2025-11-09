# Testing Guide

Comprehensive testing guide for FL Studio MCP Server.

## Running Tests

### Basic Test Run

```bash
# All tests
uv run pytest

# Verbose output
uv run pytest -v

# Stop on first failure
uv run pytest -x
```

### Coverage

```bash
# Run with coverage
uv run pytest --cov=src/fruityloops_mcp

# HTML report
uv run pytest --cov=src/fruityloops_mcp --cov-report=html
open htmlcov/index.html

# Coverage requirement (90%)
uv run pytest --cov=src/fruityloops_mcp --cov-fail-under=90
```

### Specific Tests

```bash
# Single file
uv run pytest tests/test_midi.py

# Single test
uv run pytest tests/test_midi.py::test_connect_success

# Pattern matching
uv run pytest -k "midi"
```

## Test Structure

### Test Files

- `test_server.py` - Server tests
- `test_midi.py` - MIDI interface tests
- `test_integration.py` - Integration tests
- `test_main.py` - Entry point tests
- `test_midi_edge_cases.py` - Edge cases
- `test_server_midi.py` - MIDI server tools
- `test_server_coverage.py` - Coverage improvements
- `test_git_hooks.py` - Git hooks validation

### Test Organization

```python
import pytest
from unittest.mock import Mock, patch

class TestFeature:
    """Test suite for a feature."""
    
    def test_basic_case(self):
        """Test basic functionality."""
        result = function()
        assert result == expected
    
    def test_edge_case(self):
        """Test edge case."""
        # ...
```

## Writing Tests

### Unit Tests

```python
def test_midi_connect():
    """Test MIDI connection."""
    midi = MIDIInterface()
    with patch("fruityloops_mcp.midi_interface.mido") as mock_mido:
        mock_mido.get_output_names.return_value = ["TestPort"]
        assert midi.connect() is True
```

### Async Tests

```python
@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await async_function()
    assert result is not None
```

### Fixtures

```python
@pytest.fixture
def midi():
    """Fixture providing MIDI interface."""
    return MIDIInterface(port_name="Test")

def test_with_fixture(midi):
    """Test using fixture."""
    assert midi.port_name == "Test"
```

### Mocking

```python
@patch("module.function")
def test_with_mock(mock_function):
    """Test with mocked function."""
    mock_function.return_value = "mocked"
    result = call_function()
    mock_function.assert_called_once()
```

## Coverage Requirements

### Minimum Coverage

- Overall: 90%
- New code: Should maintain or improve coverage

### Checking Coverage

```bash
# Generate JSON report
uv run pytest --cov=src/fruityloops_mcp --cov-report=json

# Check total
python -c "import json; print(json.load(open('coverage.json'))['totals']['percent_covered'])"
```

### Coverage in CI

Pull requests that decrease coverage will fail. See `.github/workflows/coverage-check.yml`.

## Test Categories

### Unit Tests

Test individual functions/classes in isolation.

### Integration Tests

Test components working together.

### Edge Cases

Test boundary conditions and unusual inputs.

### Antipatterns

Test misuse and error conditions.

## Docker Testing

```bash
# Run all CI tests
docker-compose run ci

# Interactive testing
docker-compose run test bash
uv run pytest
```

## Continuous Integration

Tests run automatically on:

- Pull requests
- Pushes to main/develop
- Multiple OS (Ubuntu, Windows, macOS)
- Multiple Python versions (3.10-3.13)

## Troubleshooting

### Test Failures

```bash
# Show output
uv run pytest -v -s

# Show locals on failure
uv run pytest -l

# Debug with pdb
uv run pytest --pdb
```

### Import Errors

```bash
# Reinstall dependencies
uv sync --all-extras
```

### Flaky Tests

If tests pass sometimes:

1. Check for timing issues
2. Look for uninitialized state
3. Add retries if needed

## Best Practices

1. **One assert per test** (when possible)
2. **Clear test names** describing what's tested
3. **Arrange-Act-Assert** pattern
4. **Mock external dependencies**
5. **Test edge cases** and error conditions
6. **Keep tests fast** (< 1s each)
7. **Clean up** resources in fixtures

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [Coverage Requirements](../.github/COVERAGE_REQUIREMENTS.md)
- [CI Workflow](../.github/workflows/ci.yml)

