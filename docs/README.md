# Documentation

FL Studio MCP Server documentation source files.

## Overview

This directory contains the source files for the project documentation, built with [MkDocs](https://www.mkdocs.org/) and the [Material theme](https://squidfunk.github.io/mkdocs-material/).

## Building Documentation

### Install Dependencies

```bash
uv sync --extra docs
```

### Local Development

```bash
# Serve documentation locally
uv run mkdocs serve

# Visit http://localhost:8000
```

### Building Static Site

```bash
# Build documentation
uv run mkdocs build

# Output is in site/ directory
```

## Documentation Structure

```
docs/
├── index.md                    # Home page
├── installation.md             # Installation guide
├── quick-start.md              # Quick start guide
├── configuration.md            # Configuration options
├── usage.md                    # Usage guide
├── fl-studio-integration.md    # FL Studio integration
├── midi-integration.md         # MIDI integration
├── mcp-client-setup.md         # MCP client setup
├── contributing.md             # Contributing guide
├── development.md              # Development setup
├── testing.md                  # Testing guide
├── git-workflow.md             # Git workflow
├── license.md                  # License information
├── changelog.md                # Version history
├── api/                        # API reference
│   ├── server.md               # Server API
│   └── midi.md                 # MIDI interface API
└── stylesheets/                # Custom styles
    └── extra.css               # Extra CSS
```

## Writing Documentation

### Markdown Files

Documentation is written in Markdown with extensions:

- **Code blocks**: \`\`\`python
- **Admonitions**: !!! note "Title"
- **Tabs**: === "Tab 1"
- **Tables**: Standard Markdown tables

### Auto-Generated API Docs

API reference is auto-generated from docstrings using mkdocstrings:

```markdown
::: fruityloops_mcp.server.FLStudioMCPServer
```

### Adding New Pages

1. Create a new `.md` file in `docs/`
2. Add to navigation in `mkdocs.yml`:

```yaml
nav:
  - New Section:
      - New Page: new-page.md
```

## Deployment

Documentation is automatically deployed to GitHub Pages via `.github/workflows/docs.yml` on pushes to `main`.

**Live Documentation**: https://quinnjr.github.io/fruityloops-mcp/

## Style Guide

- Use clear, concise language
- Include code examples where helpful
- Link to related pages
- Keep navigation logical
- Test all code examples
- Use proper heading hierarchy (h1 → h2 → h3)

## Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [mkdocstrings](https://mkdocstrings.github.io/)

