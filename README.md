# 🎹 FL Studio MCP Server

[![CI](https://github.com/quinnjr/fruityloops-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/quinnjr/fruityloops-mcp/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/quinnjr/fruityloops-mcp/branch/main/graph/badge.svg)](https://codecov.io/gh/quinnjr/fruityloops-mcp)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server for FL Studio (Fruity Loops), enabling AI assistants to interact with FL Studio's Python API and MIDI interfaces.

## ✨ Features

- **FL Studio API Integration**: Control transport, mixer, channels, patterns, and more
- **MIDI Interface**: Send MIDI messages to FL Studio via loopMIDI
- **MCP Protocol**: Standard interface for AI assistants
- **Comprehensive Testing**: 94% test coverage with unit and integration tests
- **Type Safe**: Full type hints and validation
- **Well Documented**: Complete API documentation with examples

## 📦 Installation

For detailed installation instructions, see [INSTALL.md](INSTALL.md).

### Quick Start

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

## 🎛️ MIDI Controls

The server provides comprehensive MIDI control through the loopMIDI virtual MIDI port:

### Available MIDI Tools

- `midi_connect` - Connect to MIDI port
- `midi_disconnect` - Disconnect from MIDI port
- `midi_list_ports` - List available MIDI ports
- `midi_send_note` - Send note with duration (note on + wait + note off)
- `midi_send_note_on` - Send note on message
- `midi_send_note_off` - Send note off message
- `midi_send_cc` - Send control change message
- `midi_send_program_change` - Send program change message
- `midi_send_pitch_bend` - Send pitch bend message

### MIDI Setup

1. Install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
2. Create a virtual MIDI port named `FLStudio_MIDI`
3. In FL Studio: Options → MIDI Settings → Enable the loopMIDI port
4. Connect the MCP server - MIDI tools work independently of FL Studio API

## 🚀 Usage

### With Claude Desktop

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

### With Other MCP Clients

The server uses stdio transport and works with any MCP-compatible client.

## 🛠️ Development

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- FL Studio (for FL Studio API features)
- loopMIDI (for MIDI features)

### Setup

```bash
# Clone repository
git clone https://github.com/quinnjr/fruityloops-mcp.git
cd fruityloops-mcp

# Install dependencies
uv sync --all-extras

# Install git hooks
./install-hooks.sh  # On Unix/Linux/macOS
./install-hooks.ps1  # On Windows
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

### Docker Testing

Test the CI/CD pipeline locally:

```bash
# Run full CI simulation
docker-compose run ci

# Interactive testing
docker-compose run test

# Test git hooks
docker-compose run test /app/test-git-hooks.sh
```

See [docker-test-README.md](docker-test-README.md) for details.

## 📖 Documentation

- **[Installation Guide](INSTALL.md)** - Detailed installation instructions
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- **[Usage Examples](USAGE_EXAMPLES.md)** - Practical examples
- **[API Documentation](https://quinnjr.github.io/fruityloops-mcp/)** - Auto-generated API docs

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit with conventional commits
6. Push and create a pull request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Joseph Quinn

## 🙏 Acknowledgments

- [FL Studio Python API](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) by Tobias Erichsen

## 🐛 Troubleshooting

For troubleshooting help, see the [Installation Guide](INSTALL.md#troubleshooting) or [open an issue](https://github.com/quinnjr/fruityloops-mcp/issues).

## 📊 Status

- **Build**: ![CI Status](https://github.com/quinnjr/fruityloops-mcp/actions/workflows/ci.yml/badge.svg)
- **Coverage**: ![Coverage](https://codecov.io/gh/quinnjr/fruityloops-mcp/branch/main/graph/badge.svg)
- **Version**: 1.0.0
- **Python**: 3.10+

---

Made with ❤️ for the FL Studio and AI community

