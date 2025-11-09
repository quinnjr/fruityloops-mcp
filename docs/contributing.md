# Contributing

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) in the repository root for full guidelines.

## Quick Links

- [Code of Conduct](../CONTRIBUTING.md#code-of-conduct)
- [Development Setup](development.md)
- [Testing Guide](testing.md)
- [Git Workflow](git-workflow.md)

## Quick Start

```bash
# Clone and setup
git clone https://github.com/quinnjr/fruityloops-mcp.git
cd fruityloops-mcp
uv sync --all-extras
./install-hooks.sh  # or install-hooks.ps1 on Windows

# Make changes
git checkout -b feature/your-feature
# ... make changes ...

# Test
uv run pytest
uv run ruff check .

# Commit and push
git commit -m "feat: your feature"
git push origin feature/your-feature
```

## Contribution Types

- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation
- ✅ Tests
- ♻️ Refactoring
- ⚡ Performance improvements

All contributions welcome!

