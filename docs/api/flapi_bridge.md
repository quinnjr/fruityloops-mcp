# Flapi Bridge API Reference

Auto-generated API documentation for the Flapi Bridge module.

## Overview

The Flapi Bridge provides communication between the external MCP server and FL Studio's internal Python environment using [Flapi](https://github.com/MaddyGuthridge/Flapi). Flapi uses virtual MIDI ports to forward Python API calls to FL Studio.

## FLStudioBridge

::: fruityloops_mcp.flapi_bridge.FLStudioBridge
    options:
      show_source: true
      heading_level: 3
      members:
        - __init__
        - is_available
        - is_enabled
        - is_connected
        - enable
        - disable
        - test_connection
        - connection

## Helper Functions

::: fruityloops_mcp.flapi_bridge.get_bridge
    options:
      show_source: true
      heading_level: 3

## Usage Example

```python
from fruityloops_mcp.flapi_bridge import get_bridge

# Get the global bridge instance
bridge = get_bridge()

# Enable Flapi connection
if bridge.enable():
    print("Connected to FL Studio!")

    # Control FL Studio
    print(bridge.transport_start())
    print(bridge.transport_get_bpm())

    # Disconnect when done
    bridge.disable()
```

## Context Manager Usage

```python
from fruityloops_mcp.flapi_bridge import FLStudioBridge

bridge = FLStudioBridge()

with bridge.connection():
    # FL Studio API calls here
    bridge.transport_start()
    bridge.mixer_set_track_volume(1, 0.8)
```

## Transport Methods

- `transport_start()` - Start playback
- `transport_stop()` - Stop playback
- `transport_record()` - Toggle recording
- `transport_get_song_pos()` - Get current position
- `transport_set_song_pos(position)` - Set position
- `transport_get_bpm()` - Get tempo
- `transport_set_bpm(bpm)` - Set tempo

## Mixer Methods

- `mixer_get_track_volume(track_num)` - Get volume
- `mixer_set_track_volume(track_num, volume)` - Set volume
- `mixer_get_track_name(track_num)` - Get name
- `mixer_set_track_name(track_num, name)` - Set name
- `mixer_get_track_pan(track_num)` - Get pan
- `mixer_set_track_pan(track_num, pan)` - Set pan
- `mixer_mute_track(track_num, mute)` - Mute/unmute
- `mixer_solo_track(track_num, solo)` - Solo/unsolo

## Channel Methods

- `channels_count()` - Get channel count
- `channels_get_name(channel_num)` - Get name
- `channels_set_volume(channel_num, volume)` - Set volume
- `channels_mute(channel_num, mute)` - Mute/unmute
- `channels_get_color(channel_num)` - Get color
- `channels_set_color(channel_num, color)` - Set color

## Pattern Methods

- `patterns_count()` - Get pattern count
- `patterns_get_name(pattern_num)` - Get name
- `patterns_set_name(pattern_num, name)` - Set name
- `patterns_get_length(pattern_num)` - Get length
- `patterns_jump_to(pattern_num)` - Jump to pattern

## Playlist Methods

- `playlist_get_track_name(track_num)` - Get track name
- `playlist_set_track_name(track_num, name)` - Set track name

## General Methods

- `general_get_version()` - Get FL Studio version
- `general_get_project_title()` - Get project title
- `general_save_project()` - Save project
- `general_undo()` - Undo last action

## UI Methods

- `ui_show_window(window_id)` - Show window
- `ui_get_visible(window_id)` - Check visibility

## Setup Requirements

1. Install loopMIDI (Windows) and create ports:
   - `Flapi Request`
   - `Flapi Response`

2. Install Flapi:
   ```bash
   pip install flapi
   flapi install
   ```

3. Configure FL Studio MIDI settings for Flapi ports

4. Restart FL Studio with Flapi script enabled

## See Also

- [Server API](server.md)
- [MIDI Interface API](midi.md)
- [FL Studio Integration Guide](../fl-studio-integration.md)

