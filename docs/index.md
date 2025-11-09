# FL Studio MCP Server

A Model Context Protocol (MCP) server for FL Studio (Fruity Loops), enabling AI assistants to interact with FL Studio's Python API and MIDI interfaces.

## Overview

FL Studio MCP Server provides a bridge between AI assistants and FL Studio, allowing you to:

- **Control FL Studio** via Python API (transport, mixer, channels, patterns)
- **Send MIDI messages** to FL Studio via loopMIDI
- **Automate workflows** with AI-powered assistance
- **Create music** collaboratively with AI

## Features

### 🎛️ FL Studio API Integration

- Transport controls (play, stop, record, position)
- Mixer controls (volume, pan, routing)
- Channel controls (volume, mute, solo)
- Pattern controls (naming, selection)
- Project information
- UI controls

### 🎹 MIDI Controls

- Connect/disconnect to MIDI ports
- Send notes (note on/off with duration)
- Control change messages
- Program changes
- Pitch bend
- Works independently of FL Studio

### ⚙️ Developer Friendly

- Comprehensive testing (94% coverage)
- Type hints throughout
- Full documentation
- Docker support for testing
- Git hooks for code quality

## Quick Start

### Installation

```bash
# Using uvx (recommended)
uvx fruityloops-mcp

# Using uv
uv tool install fruityloops-mcp
uv tool run fruityloops-mcp

# Using pip
pip install fruityloops-mcp
fruityloops-mcp
```

### Claude Desktop Setup

Add to your Claude Desktop configuration:

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

### Basic Usage

```python
# Connect to MIDI
midi_connect()

# Send a note
midi_send_note(note=60, velocity=100, duration=0.5)

# Control FL Studio (requires FL Studio running)
transport_start()
mixer_set_track_volume(track_num=0, volume=0.8)
```

## Requirements

- Python 3.10 or higher
- FL Studio (for FL Studio API features)
- loopMIDI (for MIDI features)
- MCP-compatible client (Claude Desktop, etc.)

## Documentation

- [Installation Guide](installation.md) - Detailed setup instructions
- [Quick Start](quick-start.md) - Get up and running quickly
- [Usage Examples](usage.md) - Practical examples
- [API Reference](api/server.md) - Complete API documentation

## Project Status

- ✅ **Stable**: Core functionality complete
- ✅ **Tested**: 94% code coverage
- ✅ **Documented**: Comprehensive docs
- ✅ **Production Ready**: v1.0.0 released

## Support

- [GitHub Issues](https://github.com/quinnjr/fruityloops-mcp/issues)
- [Discussions](https://github.com/quinnjr/fruityloops-mcp/discussions)
- [Documentation](https://quinnjr.github.io/fruityloops-mcp/)

## License

MIT License - see [LICENSE](license.md) for details.

## Contributing

Contributions welcome! See [Contributing Guide](contributing.md).

---

Made with ❤️ for the FL Studio and AI community

