# Configuration

Configuration options for FL Studio MCP Server.

## Server Configuration

### MIDI Port Name

By default, the server uses `FLStudio_MIDI` as the MIDI port name. To use a different port:

```python
# When initializing the server
from fruityloops_mcp.server import FLStudioMCPServer

server = FLStudioMCPServer(midi_port="MyCustomPort")
```

### MCP Client Configuration

#### Claude Desktop

Location of config file:

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

Basic configuration:

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

With custom port:

```json
{
  "mcpServers": {
    "fruityloops": {
      "command": "uv",
      "args": ["run", "fruityloops-mcp"],
      "env": {
        "MIDI_PORT": "MyCustomPort"
      }
    }
  }
}
```

## FL Studio Configuration

### MIDI Settings

1. Open FL Studio
2. Options → MIDI Settings
3. Enable your MIDI port (e.g., `FLStudio_MIDI`)
4. Set as:
   - **Input**: Enabled
   - **Output**: Enabled
   - **Controller type**: Generic Controller

### Python API

The Python API is automatically available in FL Studio. No additional configuration needed.

## loopMIDI Configuration

### Port Settings

- **Port name**: `FLStudio_MIDI` (must match server configuration)
- **Autostart**: Enabled (optional)

### Multiple Ports

You can create multiple virtual MIDI ports for different purposes:

```
FLStudio_MIDI  - Main control
FLStudio_Drums - Drum sequencer
FLStudio_Synth - Synthesizer control
```

Then connect to specific ports as needed.

## Environment Variables

### MIDI_PORT

Set default MIDI port name:

```bash
export MIDI_PORT=MyCustomPort
```

### LOG_LEVEL

Set logging level:

```bash
export LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR
```

## Advanced Configuration

### Custom Server Script

Create a custom script to configure the server:

```python
#!/usr/bin/env python
import asyncio
import logging
from fruityloops_mcp.server import FLStudioMCPServer

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create server with custom port
server = FLStudioMCPServer(midi_port="MyPort")

# Run server
asyncio.run(server.run())
```

Make executable and use in MCP config:

```json
{
  "mcpServers": {
    "fruityloops": {
      "command": "/path/to/custom_server.py"
    }
  }
}
```

## Configuration Files

The server doesn't use configuration files by default. All configuration is done through:

1. Command-line arguments
2. Environment variables
3. MCP client configuration

## Troubleshooting

### Port Not Found

If you get "Port not found" errors:

1. Check loopMIDI is running
2. Verify port name matches exactly
3. List available ports with `midi_list_ports()`

### Permission Issues

On some systems, you may need additional permissions for MIDI access.

**Linux**:
```bash
sudo usermod -a -G audio $USER
```

**macOS**: Grant MIDI permissions in System Preferences

## Next Steps

- [Usage Examples](usage.md)
- [FL Studio Integration](fl-studio-integration.md)
- [MIDI Integration](midi-integration.md)

