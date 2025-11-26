# 🎹 FL Studio MCP Server

[![CI](https://github.com/quinnjr/fruityloops-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/quinnjr/fruityloops-mcp/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/quinnjr/fruityloops-mcp/branch/main/graph/badge.svg)](https://codecov.io/gh/quinnjr/fruityloops-mcp)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server for FL Studio (Fruity Loops), enabling AI assistants like Claude to compose music and control FL Studio through natural language.

## ✨ Features

- **FL Studio API Integration via Flapi**: Control transport, mixer, channels, patterns, and more
- **MIDI Interface**: Send MIDI notes and messages to FL Studio via loopMIDI
- **MCP Protocol**: Standard interface for AI assistants (Claude, etc.)
- **Dual Communication**: Uses both Flapi (for API calls) and MIDI (for notes/CC)
- **Type Safe**: Full type hints and validation

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Claude Desktop │────▶│   MCP Server    │────▶│    FL Studio    │
│  (AI Assistant) │     │   (External)    │     │   (Internal)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │                        ▲
                               │                        │
                        ┌──────┴──────┐                 │
                        │             │                 │
                        ▼             ▼                 │
                  ┌──────────┐ ┌────────────┐          │
                  │  Flapi   │ │    MIDI    │          │
                  │  Bridge  │ │  Interface │          │
                  └────┬─────┘ └─────┬──────┘          │
                       │             │                  │
                       │    MIDI     │                  │
                       └─────────────┴──────────────────┘
```

- **Flapi Bridge**: Forwards FL Studio API calls (transport, mixer, channels) via MIDI to FL Studio's internal Python
- **MIDI Interface**: Sends MIDI notes, CC, program changes directly to FL Studio

## 📦 Installation

### Prerequisites

1. **Python 3.10+**
2. **FL Studio** (version 20.7+ for MIDI scripting support)
3. **loopMIDI** (Windows) - [Download](https://www.tobias-erichsen.de/software/loopmidi.html)

### Quick Start

```bash
# Install the MCP server
pip install fruityloops-mcp

# Install Flapi for FL Studio API access
pip install flapi
flapi install
```

### Virtual MIDI Port Setup (Windows)

1. Install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
2. Create these virtual MIDI ports:
   - `FLStudio_MIDI` - For sending MIDI notes/CC to FL Studio
   - `Flapi Request` - For Flapi API requests
   - `Flapi Response` - For Flapi API responses

### FL Studio Configuration

#### For MIDI Control:
1. Open FL Studio → Options → MIDI Settings
2. Enable the `FLStudio_MIDI` port as an input
3. Route the MIDI input to your desired channel/instrument

#### For Flapi (API Access):
1. Run `flapi install` to install the Flapi script
2. Restart FL Studio
3. Go to Options → MIDI Settings
4. In the **Output** section, assign unique port numbers to `Flapi Request` and `Flapi Response`
5. In the **Input** section, set the same port numbers for the corresponding inputs
6. Assign `Flapi Request` input to the "Flapi Request" script
7. Assign `Flapi Response` input to the "Flapi Response" script

## 🚀 Usage

### With Claude Desktop

Add to your Claude Desktop configuration (`%APPDATA%\Claude\claude_desktop_config.json` on Windows):

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

Or using pip:

```json
{
  "mcpServers": {
    "fruityloops": {
      "command": "fruityloops-mcp"
    }
  }
}
```

### First Steps in Claude

1. **Connect to FL Studio**:
   ```
   "Connect to FL Studio via Flapi"
   ```

2. **Check connection**:
   ```
   "What's the Flapi connection status?"
   ```

3. **Start composing**:
   ```
   "Start playback in FL Studio"
   "Set the tempo to 120 BPM"
   "Play a C major chord"
   ```

## 🎛️ Available Tools

### Flapi Connection
- `flapi_connect` - Connect to FL Studio via Flapi
- `flapi_disconnect` - Disconnect from Flapi
- `flapi_status` - Check connection status

### MIDI Tools
- `midi_connect` - Connect to MIDI port
- `midi_disconnect` - Disconnect from MIDI port
- `midi_list_ports` - List available MIDI ports
- `midi_send_note` - Send note with duration
- `midi_send_note_on` / `midi_send_note_off` - Note messages
- `midi_send_cc` - Control change messages
- `midi_send_program_change` - Program change
- `midi_send_pitch_bend` - Pitch bend

### Transport Controls
- `transport_start` / `transport_stop` - Playback control
- `transport_record` - Toggle recording
- `transport_get_bpm` / `transport_set_bpm` - Tempo control
- `transport_get_song_pos` / `transport_set_song_pos` - Position control

### Mixer Controls
- `mixer_get_track_volume` / `mixer_set_track_volume`
- `mixer_get_track_name` / `mixer_set_track_name`
- `mixer_get_track_pan` / `mixer_set_track_pan`
- `mixer_mute_track` / `mixer_solo_track`

### Channel Controls
- `channels_channel_count` - Get number of channels
- `channels_get_channel_name` - Get channel name
- `channels_set_channel_volume` - Set volume
- `channels_mute_channel` - Mute/unmute
- `channels_get_channel_color` / `channels_set_channel_color`

### Pattern Controls
- `patterns_pattern_count` - Get number of patterns
- `patterns_get_pattern_name` / `patterns_set_pattern_name`
- `patterns_get_pattern_length`
- `patterns_jump_to_pattern`

### Playlist Controls
- `playlist_get_track_name` / `playlist_set_track_name`

### General Controls
- `general_get_version` - FL Studio version
- `general_get_project_title`
- `general_save_project`
- `general_undo`

### UI Controls
- `ui_show_window` - Show FL Studio windows (Mixer, Channel Rack, Piano Roll, etc.)
- `ui_get_visible` - Check window visibility

## 🛠️ Development

### Setup

```bash
# Clone repository
git clone https://github.com/quinnjr/fruityloops-mcp.git
cd fruityloops-mcp

# Install dependencies
uv sync --all-extras

# Install git hooks
./install-hooks.ps1  # On Windows
./install-hooks.sh   # On Unix/macOS
```

### Testing

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

## 🐛 Troubleshooting

### Flapi Connection Issues

1. **"Flapi not available"**: Run `pip install flapi`
2. **"Failed to connect"**:
   - Ensure loopMIDI ports `Flapi Request` and `Flapi Response` exist
   - Restart FL Studio after installing Flapi
   - Check FL Studio MIDI settings are configured correctly
3. **"FL Studio connection test failed"**:
   - Verify FL Studio is running
   - Check the Flapi script is loaded (look for it in the MIDI scripts panel)

### MIDI Issues

1. **"MIDI port not found"**: Create `FLStudio_MIDI` port in loopMIDI
2. **"Failed to send MIDI"**: Ensure MIDI port is connected first using `midi_connect`
3. **No sound**: Check FL Studio has the MIDI port enabled and routed to an instrument

## 📖 Documentation

- **[Installation Guide](INSTALL.md)** - Detailed installation instructions
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- **[Usage Examples](USAGE_EXAMPLES.md)** - Practical examples
- **[API Documentation](https://quinnjr.github.io/fruityloops-mcp/)** - Auto-generated API docs

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Joseph Quinn

## 🙏 Acknowledgments

- [Flapi](https://github.com/MaddyGuthridge/Flapi) by Maddy Guthridge - FL Studio remote control
- [FL Studio Python API](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) by Tobias Erichsen

---

Made with ❤️ for the FL Studio and AI community
