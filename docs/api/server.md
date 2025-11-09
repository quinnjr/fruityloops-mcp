# Server API Reference

Auto-generated API documentation for the FL Studio MCP Server.

## FLStudioMCPServer

::: fruityloops_mcp.server.FLStudioMCPServer
    options:
      show_source: true
      heading_level: 3
      members:
        - __init__
        - run
        - call_tool
        - _execute_tool

## StubModule

::: fruityloops_mcp.server.StubModule
    options:
      show_source: true
      heading_level: 3

## Constants

### FL_STUDIO_AVAILABLE

Boolean indicating if FL Studio API modules are available.

```python
from fruityloops_mcp.server import FL_STUDIO_AVAILABLE

if FL_STUDIO_AVAILABLE:
    # FL Studio API features are available
    pass
else:
    # Running in stub mode
    pass
```

## Usage Example

```python
import asyncio
from fruityloops_mcp.server import FLStudioMCPServer

# Create server
server = FLStudioMCPServer()

# Run server
asyncio.run(server.run())
```

## Custom MIDI Port

```python
# Use custom MIDI port name
server = FLStudioMCPServer(midi_port="MyCustomPort")
```

## Tool Execution

```python
# Execute a tool directly
result = await server._execute_tool("midi_connect", {})
print(result)  # "Connected to MIDI port: FLStudio_MIDI"
```

## Available Tools

### MIDI Tools

- `midi_connect` - Connect to MIDI port
- `midi_disconnect` - Disconnect from MIDI port
- `midi_list_ports` - List available MIDI ports
- `midi_send_note` - Send a MIDI note with duration
- `midi_send_note_on` - Send note on message
- `midi_send_note_off` - Send note off message
- `midi_send_cc` - Send control change message
- `midi_send_program_change` - Send program change
- `midi_send_pitch_bend` - Send pitch bend

### FL Studio Tools

(Only available when FL_STUDIO_AVAILABLE is True)

**Transport:**
- `transport_start` - Start playback
- `transport_stop` - Stop playback
- `transport_record` - Toggle recording
- `transport_get_song_pos` - Get song position
- `transport_set_song_pos` - Set song position

**Mixer:**
- `mixer_get_track_volume` - Get track volume
- `mixer_set_track_volume` - Set track volume
- `mixer_get_track_name` - Get track name
- `mixer_set_track_name` - Set track name

**Channels:**
- `channels_channel_count` - Get channel count
- `channels_get_channel_name` - Get channel name
- `channels_set_channel_volume` - Set channel volume
- `channels_mute_channel` - Mute/unmute channel

**Patterns:**
- `patterns_pattern_count` - Get pattern count
- `patterns_get_pattern_name` - Get pattern name
- `patterns_set_pattern_name` - Set pattern name

**General:**
- `general_get_project_title` - Get project title
- `general_get_version` - Get FL Studio version

**UI:**
- `ui_show_window` - Show FL Studio window

**Playlist:**
- `playlist_get_track_name` - Get playlist track name

## See Also

- [MIDI Interface API](midi.md)
- [Usage Guide](../usage.md)
- [FL Studio Integration](../fl-studio-integration.md)

