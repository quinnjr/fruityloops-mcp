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
# Use custom MIDI port name for direct MIDI control
server = FLStudioMCPServer(midi_port="MyCustomPort")
```

## Available Tools

### Flapi Connection Tools

- `flapi_connect` - Connect to FL Studio via Flapi
- `flapi_disconnect` - Disconnect from Flapi
- `flapi_status` - Get Flapi connection status

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

### FL Studio Tools (via Flapi)

These tools require a Flapi connection to FL Studio.

**Transport:**

- `transport_start` - Start playback
- `transport_stop` - Stop playback
- `transport_record` - Toggle recording
- `transport_get_song_pos` - Get song position
- `transport_set_song_pos` - Set song position
- `transport_get_bpm` - Get current tempo
- `transport_set_bpm` - Set tempo

**Mixer:**

- `mixer_get_track_volume` - Get track volume
- `mixer_set_track_volume` - Set track volume
- `mixer_get_track_name` - Get track name
- `mixer_set_track_name` - Set track name
- `mixer_get_track_pan` - Get track pan
- `mixer_set_track_pan` - Set track pan
- `mixer_mute_track` - Mute/unmute track
- `mixer_solo_track` - Solo/unsolo track

**Channels:**

- `channels_channel_count` - Get channel count
- `channels_get_channel_name` - Get channel name
- `channels_set_channel_volume` - Set channel volume
- `channels_mute_channel` - Mute/unmute channel
- `channels_get_channel_color` - Get channel color
- `channels_set_channel_color` - Set channel color

**Patterns:**

- `patterns_pattern_count` - Get pattern count
- `patterns_get_pattern_name` - Get pattern name
- `patterns_set_pattern_name` - Set pattern name
- `patterns_get_pattern_length` - Get pattern length
- `patterns_jump_to_pattern` - Jump to pattern

**Playlist:**

- `playlist_get_track_name` - Get playlist track name
- `playlist_set_track_name` - Set playlist track name

**General:**

- `general_get_project_title` - Get project title
- `general_get_version` - Get FL Studio version
- `general_save_project` - Save current project
- `general_undo` - Undo last action

**UI:**

- `ui_show_window` - Show FL Studio window
- `ui_get_visible` - Check window visibility

## See Also

- [Flapi Bridge API](flapi_bridge.md)
- [MIDI Interface API](midi.md)
- [Usage Guide](../usage.md)
- [FL Studio Integration](../fl-studio-integration.md)
