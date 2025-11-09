# 📦 Installation Guide

Complete installation guide for FL Studio MCP Server.

## Prerequisites

- **Python 3.10 or higher**
- **[uv](https://github.com/astral-sh/uv)** package manager (recommended)
- **FL Studio** (for FL Studio API features)
- **[loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)** (for MIDI features)

## Quick Start

```bash
# Install and run with uvx (easiest method)
uvx fruityloops-mcp
```

## Installation Methods

### Method 1: Using uvx (Recommended)

The fastest way to run the server without installation:

```bash
uvx fruityloops-mcp
```

### Method 2: Using uv tool

Install as a uv tool for persistent use:

```bash
# Install
uv tool install fruityloops-mcp

# Run
uv tool run fruityloops-mcp

# Or just
fruityloops-mcp
```

### Method 3: Using pip

Traditional pip installation:

```bash
# Install
pip install fruityloops-mcp

# Run
fruityloops-mcp
```

### Method 4: From Source

For development or the latest features:

```bash
# Clone repository
git clone https://github.com/quinnjr/fruityloops-mcp.git
cd fruityloops-mcp

# Install with uv
uv sync

# Run
uv run fruityloops-mcp
```

## FL Studio Integration

### Python API Setup

1. **Enable Python API in FL Studio**:
   - Options → MIDI Settings
   - Enable "Script output" for your controller
   - Select "Generic Controller" as the controller type

2. **Verify API Access**:
   - FL Studio must be running for API features to work
   - MIDI features work independently of FL Studio

## loopMIDI Setup

### Installation

1. Download [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
2. Run the installer
3. Launch loopMIDI

### Configuration

1. **Create Virtual Port**:
   - Click the `+` button in loopMIDI
   - Name: `FLStudio_MIDI`
   - Click "Create"

2. **Configure FL Studio**:
   - Options → MIDI Settings
   - Enable the `FLStudio_MIDI` port under "Input"
   - Enable the port under "Output"

3. **Test Connection**:
   ```bash
   # List available ports
   uvx fruityloops-mcp
   # Then use midi_list_ports tool
   ```

## MCP Client Setup

### Claude Desktop

Add to `claude_desktop_config.json`:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fruityloops": {
      "command": "uvx",
      "args": ["fruityloops-mcp"]
    }
  }
}
```

### Other MCP Clients

The server uses stdio transport and works with any MCP-compatible client.

## Development Installation

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/quinnjr/fruityloops-mcp.git
cd fruityloops-mcp

# Install all dependencies including dev and docs
uv sync --all-extras

# Install git hooks (optional but recommended)
./install-hooks.sh  # Unix/Linux/macOS
./install-hooks.ps1  # Windows
```

### Run Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest tests/test_midi.py
```

### Linting and Formatting

```bash
# Check linting
uv run ruff check .

# Fix linting issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

## Docker Installation

For testing in an isolated environment:

```bash
# Build and run
docker-compose up

# Run CI tests
docker-compose run ci

# Interactive shell
docker-compose run test
```

See [docker-test-README.md](docker-test-README.md) for details.

## Verification

### Test the Installation

```bash
# Run the server
fruityloops-mcp

# In another terminal, test with an MCP client
# or configure your MCP client to use the server
```

### Verify MIDI Connection

```bash
# In your MCP client, try:
# 1. midi_list_ports - Should show FLStudio_MIDI
# 2. midi_connect - Should connect successfully
# 3. midi_send_note - Should send a MIDI note
```

### Verify FL Studio Integration

1. Start FL Studio
2. Connect the MCP server
3. Try FL Studio commands (transport_start, etc.)

## Troubleshooting

### Common Issues

**Issue**: "Module not found" errors
**Solution**: Ensure you're using Python 3.10+
```bash
python --version
```

**Issue**: MIDI port not found
**Solution**:
1. Verify loopMIDI is running
2. Check port name matches `FLStudio_MIDI`
3. List ports with `midi_list_ports` tool

**Issue**: FL Studio API not available
**Solution**:
1. Ensure FL Studio is running
2. MIDI features still work without FL Studio
3. Check Python API is enabled in FL Studio settings

**Issue**: uv command not found
**Solution**: Install uv:
```bash
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Issue**: Permission denied on hooks
**Solution**: Make scripts executable:
```bash
chmod +x install-hooks.sh
chmod +x .githooks/*
```

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/quinnjr/fruityloops-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/quinnjr/fruityloops-mcp/discussions)
- **Documentation**: [Full Documentation](https://quinnjr.github.io/fruityloops-mcp/)

## Uninstallation

### uv tool

```bash
uv tool uninstall fruityloops-mcp
```

### pip

```bash
pip uninstall fruityloops-mcp
```

## System Requirements

- **OS**: Windows 10+, macOS 10.15+, Linux (any recent distribution)
- **Python**: 3.10, 3.11, 3.12, or 3.13
- **RAM**: 256MB minimum
- **Disk**: 50MB for installation

## Next Steps

1. ✅ Installation complete
2. 📖 Read the [README](README.md) for usage examples
3. 🎹 Set up FL Studio and loopMIDI
4. 🤖 Configure your MCP client
5. 🚀 Start creating music with AI!

---

Need help? [Open an issue](https://github.com/quinnjr/fruityloops-mcp/issues) or check the [documentation](https://quinnjr.github.io/fruityloops-mcp/).

