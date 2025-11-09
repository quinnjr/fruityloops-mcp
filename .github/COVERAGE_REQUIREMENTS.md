# Coverage Requirements

This project maintains high code coverage standards to ensure quality and reliability.

## Requirements

- **Minimum Coverage**: 90%
- **Coverage Check**: Runs on all pull requests
- **Enforcement**: PRs that decrease coverage will fail CI

## Coverage Workflows

### 1. Coverage Check (PR)

**Workflow**: `.github/workflows/coverage-check.yml`

**Triggers**: Pull requests to `main` or `develop`

**What it does**:
1. Runs tests on PR branch and measures coverage
2. Runs tests on base branch and measures coverage
3. Compares the two and fails if coverage decreased
4. Posts a detailed report as a PR comment

**Example Report**:
```markdown
## ✅ Coverage Report

| Branch | Coverage |
|--------|----------|
| Base (`main`) | 94.2% |
| PR (`feature/new-tool`) | 94.5% |
| **Difference** | **+0.3%** |

✨ Coverage maintained or improved!
```

### 2. Coverage Report (Push)

**Workflow**: `.github/workflows/coverage-report.yml`

**Triggers**: Push to `main`, `master`, or `develop`

**What it does**:
1. Runs tests and measures coverage
2. Creates a coverage badge (requires gist setup)
3. Posts coverage as a commit comment

## Running Coverage Locally

### Basic Coverage Report

```bash
# Run tests with coverage
uv run pytest --cov=src/fruityloops_mcp --cov-report=term-missing

# Output shows covered/missed lines
```

### HTML Coverage Report

```bash
# Generate HTML report
uv run pytest --cov=src/fruityloops_mcp --cov-report=html

# Open in browser
# Windows
start htmlcov/index.html

# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html
```

### JSON Coverage Report

```bash
# Generate JSON report (used by CI)
uv run pytest --cov=src/fruityloops_mcp --cov-report=json

# View total coverage
python -c "import json; print(json.load(open('coverage.json'))['totals']['percent_covered'])"
```

## Adding Tests for New Code

When adding new features, ensure adequate test coverage:

### 1. Unit Tests

Test individual functions and classes:

```python
# tests/test_new_feature.py
def test_new_function():
    result = new_function(arg)
    assert result == expected
```

### 2. Integration Tests

Test components working together:

```python
# tests/test_integration.py
@pytest.mark.asyncio
async def test_new_workflow():
    server = FLStudioMCPServer()
    result = await server._execute_tool("new_tool", {})
    assert "expected" in result
```

### 3. Edge Cases

Test boundary conditions and error handling:

```python
# tests/test_edge_cases.py
def test_invalid_input():
    with pytest.raises(ValueError):
        function_with_validation(invalid_input)

def test_empty_input():
    result = function(empty_value)
    assert result == default_value
```

## Coverage Best Practices

### What to Test

✅ **Do test:**
- All public APIs
- Error handling paths
- Edge cases and boundary conditions
- Integration between components
- Configuration options
- Different parameter combinations

❌ **Don't need 100% coverage for:**
- `__repr__` and `__str__` methods
- Type checking code (handled by type checker)
- Defensive assertions that should never trigger
- Code that's impossible to reach

### Excluding Code from Coverage

Use `# pragma: no cover` sparingly:

```python
def debug_function():  # pragma: no cover
    """Only used during development."""
    pass
```

**Valid exclusions:**
- Debug-only code
- Platform-specific code that can't be tested in CI
- Code that requires specific hardware/software

## Troubleshooting

### Coverage Dropped But I Added Tests

**Possible causes:**
1. New code added without tests
2. Tests not actually executing (check with `-v` flag)
3. Mocked code preventing actual execution

**Solutions:**
```bash
# Check which lines are missing
uv run pytest --cov=src/fruityloops_mcp --cov-report=term-missing

# Run with verbose output
uv run pytest -v --cov=src/fruityloops_mcp

# Check specific test file
uv run pytest tests/test_myfile.py -v
```

### Tests Pass Locally But Fail in CI

**Possible causes:**
1. Platform-specific behavior
2. Missing dependencies
3. Environment differences

**Solutions:**
```bash
# Test in Docker (matches CI environment)
docker-compose run test

# Check CI logs for specific failures
# Fix platform-specific code with conditionals
```

### Coverage Report Shows Wrong Files

**Check pytest configuration:**
```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src/fruityloops_mcp --cov-report=term-missing"
```

### PR Fails Coverage Check

**Steps to fix:**

1. **Check the PR comment** for coverage comparison
2. **Identify missing coverage:**
   ```bash
   git checkout your-branch
   uv run pytest --cov=src/fruityloops_mcp --cov-report=term-missing
   ```
3. **Add tests** for uncovered lines
4. **Verify coverage improved:**
   ```bash
   uv run pytest --cov=src/fruityloops_mcp --cov-report=json
   python -c "import json; print(json.load(open('coverage.json'))['totals']['percent_covered'])"
   ```
5. **Push changes** and check CI

## Coverage Metrics

### Current Coverage: 94%

**Breakdown by module:**
- `server.py`: 90%
- `midi_interface.py`: 96%
- `__init__.py`: 100%
- `__main__.py`: 100%

**Goal**: Maintain >90% overall coverage

## Coverage Badge

Add to README:

```markdown
[![codecov](https://codecov.io/gh/quinnjr/fruityloops-mcp/branch/main/graph/badge.svg)](https://codecov.io/gh/quinnjr/fruityloops-mcp)
```

## References

- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Codecov](https://codecov.io/)

