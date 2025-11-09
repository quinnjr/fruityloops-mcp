# Installation Guide

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
uv sync --all-extras

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

See the [main installation guide](../INSTALL.md) for detailed troubleshooting.

## Next Steps

- Read the [Quick Start Guide](quick-start.md)
- Try [Usage Examples](usage.md)
- Explore the [API Reference](api/server.md)

