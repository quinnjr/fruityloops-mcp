# 📦 Installation Guide

Complete installation guide for FL Studio MCP Server.

## Prerequisites

- **Python 3.10 or higher**
- **[uv](https://github.com/astral-sh/uv)** package manager (recommended)
- **FL Studio** (version 20.7+ for MIDI scripting support)
- **[loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)** (Windows only - for virtual MIDI ports)

## Quick Start

```bash
# Install and run the MCP server
uvx fruityloops-mcp

# Install Flapi for FL Studio API access
pip install flapi
flapi install
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

## Flapi Setup (Required for FL Studio API)

[Flapi](https://github.com/MaddyGuthridge/Flapi) is a bridge that allows external Python code to control FL Studio's internal Python API via MIDI. This is **required** for the FL Studio API tools (transport, mixer, channels, patterns, etc.) to work.

### Step 1: Install Flapi

```bash
pip install flapi
```

### Step 2: Install Flapi Script to FL Studio

```bash
flapi install
```

If you've moved your FL Studio user data folder, specify the path:

```bash
flapi install --user-data-folder "C:\Users\YourName\Documents\Image-Line\FL Studio"
```

### Step 3: Create Virtual MIDI Ports (Windows)

1. Download and install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
2. Launch loopMIDI
3. Create **three** virtual MIDI ports:
   - `FLStudio_MIDI` - For sending MIDI notes to FL Studio
   - `Flapi Request` - For Flapi API requests
   - `Flapi Response` - For Flapi API responses

Click the `+` button and enter each name, then click "Create".

### Step 4: Configure FL Studio MIDI Settings

1. Start FL Studio
2. Go to **Options → MIDI Settings**

#### For Flapi (API Access):

In the **Output** section:
- Find `Flapi Request` and `Flapi Response`
- Assign **unique port numbers** to each (e.g., Port 1 and Port 2)

In the **Input** section:
- Find `Flapi Request` and `Flapi Response`
- Set the **same port numbers** as their corresponding outputs
- For `Flapi Request` input: Click the "Script" dropdown and select **"Flapi Request"**
- For `Flapi Response` input: Click the "Script" dropdown and select **"Flapi Response"**

#### For Direct MIDI Control:

In the **Input** section:
- Find `FLStudio_MIDI`
- Enable it (red indicator should appear)
- Set it to control your desired channel or use "Generic Controller"

### Step 5: Verify Flapi Installation

1. Restart FL Studio after making MIDI settings changes
2. Look for the Flapi script in the MIDI scripts panel
3. Run the MCP server and use `flapi_status` to test connectivity

## loopMIDI Setup (Detailed)

### Installation

1. Download [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
2. Run the installer (admin rights required)
3. Launch loopMIDI from the Start menu

### Create Virtual Ports

1. In the loopMIDI window, find "New port-name" field
2. Enter port name and click `+`:
   - `FLStudio_MIDI` (for direct MIDI)
   - `Flapi Request` (for Flapi)
   - `Flapi Response` (for Flapi)
3. Ensure loopMIDI runs at startup (enable in settings)

### Verify Ports

```bash
# In your MCP client, use:
midi_list_ports
# Should show all three ports in both Input and Output lists
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

Or if installed via pip:

```json
{
  "mcpServers": {
    "fruityloops": {
      "command": "fruityloops-mcp"
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
./install-hooks.ps1  # Windows
./install-hooks.sh   # Unix/Linux/macOS
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

## Verification

### Test the Installation

1. **Start FL Studio** with the Flapi script enabled
2. **Run the MCP server**: `fruityloops-mcp`
3. **Connect your MCP client** (e.g., Claude Desktop)

### Verify Flapi Connection

In your MCP client:
```
1. Use "flapi_connect" - Should connect to FL Studio
2. Use "flapi_status" - Should show "FL Studio connection: OK"
3. Use "transport_start" - Should start playback in FL Studio
```

### Verify MIDI Connection

```
1. Use "midi_list_ports" - Should show FLStudio_MIDI
2. Use "midi_connect" - Should connect successfully
3. Use "midi_send_note" with note=60 - Should play middle C
```

## Troubleshooting

### Flapi Issues

**Issue**: "Flapi not available"
**Solution**: Install Flapi:
```bash
pip install flapi
```

**Issue**: "Failed to connect to FL Studio via Flapi"
**Solution**:
1. Verify loopMIDI ports `Flapi Request` and `Flapi Response` exist
2. Run `flapi install` to install the script
3. Restart FL Studio
4. Configure FL Studio MIDI settings (see Step 4 above)
5. Check that the Flapi scripts are assigned to the correct ports

**Issue**: "FL Studio connection test failed"
**Solution**:
1. Make sure FL Studio is running
2. Verify the Flapi script is loaded (check MIDI scripts panel in FL Studio)
3. Try restarting FL Studio

### MIDI Issues

**Issue**: MIDI port not found
**Solution**:
1. Verify loopMIDI is running
2. Check port name matches `FLStudio_MIDI`
3. List ports with `midi_list_ports` tool

**Issue**: No sound when sending MIDI
**Solution**:
1. Ensure FL Studio has the MIDI port enabled in MIDI Settings
2. Route the MIDI input to a channel with an instrument loaded
3. Check FL Studio isn't muted or the channel isn't muted

### General Issues

**Issue**: "Module not found" errors
**Solution**: Ensure you're using Python 3.10+
```bash
python --version
```

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

### Flapi

```bash
flapi uninstall
pip uninstall flapi
```

### loopMIDI

Remove the virtual MIDI ports from loopMIDI, then uninstall via Windows Settings.

## System Requirements

- **OS**: Windows 10+, macOS 10.15+, Linux (any recent distribution)
- **Python**: 3.10, 3.11, 3.12, or 3.13
- **FL Studio**: Version 20.7+ (for MIDI scripting support)
- **RAM**: 256MB minimum
- **Disk**: 50MB for installation

## Next Steps

1. ✅ Installation complete
2. 📖 Read the [README](README.md) for usage examples
3. 🎹 Set up FL Studio, loopMIDI, and Flapi
4. 🤖 Configure your MCP client
5. 🎵 Connect to FL Studio with `flapi_connect`
6. 🚀 Start creating music with AI!

---

Need help? [Open an issue](https://github.com/quinnjr/fruityloops-mcp/issues) or check the [documentation](https://quinnjr.github.io/fruityloops-mcp/).
