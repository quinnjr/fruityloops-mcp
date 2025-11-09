# FL Studio Integration

Guide to integrating with FL Studio's Python API.

## Overview

FL Studio provides a Python API for scripting and automation. This server exposes that API through the MCP protocol.

## Requirements

- FL Studio installed and running
- Python API enabled (automatic in recent versions)
- MIDI ports configured (optional, for MIDI features)

## Python API Setup

FL Studio's Python API is automatically available when FL Studio is running. No additional installation required.

### Verifying API Access

Test if the API is available:

```python
# In your MCP client
general_get_version()
# Should return: "FL Studio version: XX.X.X"
```

If this fails, the FL Studio API is not available (but MIDI will still work).

## Available APIs

### Transport Control

Control playback and recording:

```python
# Start/stop playback
transport_start()
transport_stop()

# Toggle recording
transport_record()

# Position control
pos = transport_get_song_pos()
transport_set_song_pos(position=1920)  # 1 bar at 960 PPQ
```

### Mixer Control

Control mixer tracks:

```python
# Get/set volume (0.0 to 1.0)
vol = mixer_get_track_volume(track_num=0)
mixer_set_track_volume(track_num=0, volume=0.8)

# Track naming
name = mixer_get_track_name(track_num=1)
mixer_set_track_name(track_num=1, name="Drums")
```

### Channel Control

Control generator channels:

```python
# Channel info
count = channels_channel_count()
name = channels_get_channel_name(channel_num=0)

# Channel settings
channels_set_channel_volume(channel_num=0, volume=0.9)
channels_mute_channel(channel_num=0, mute=True)
```

### Pattern Control

Manage patterns:

```python
# Pattern info
count = patterns_pattern_count()
name = patterns_get_pattern_name(pattern_num=0)

# Rename patterns
patterns_set_pattern_name(pattern_num=0, name="Intro")
```

### Project Information

Get project details:

```python
# Project title
title = general_get_project_title()

# FL Studio version
version = general_get_version()
```

### UI Control

Control FL Studio windows:

```python
# Show specific windows
ui_show_window(window_id=0)  # Mixer
ui_show_window(window_id=1)  # Playlist
```

### Playlist Control

Manage playlist tracks:

```python
# Get track name
name = playlist_get_track_name(track_num=0)
```

## API Limitations

### Read-Only Operations

Some operations are read-only. You can get values but not set them:

- Project title (read-only)
- FL Studio version (read-only)
- Playlist track names (currently read-only)

### Timing

API calls are synchronous and may block briefly. For real-time applications, use MIDI instead.

### Availability

The API is only available when:

1. FL Studio is running
2. The server can import FL Studio modules
3. You're running on the same machine as FL Studio

## Best Practices

### Error Handling

Always check if FL Studio is available:

```python
try:
    version = general_get_version()
    print(f"FL Studio {version} detected")
except:
    print("FL Studio not available, using MIDI only")
```

### Position Values

Song positions are in ticks:

- Default: 960 PPQ (parts per quarter note)
- 1 bar (4/4) = 3840 ticks
- 1 beat = 960 ticks
- 1 bar (3/4) = 2880 ticks

```python
# Calculate position
beats = 8
position = beats * 960
transport_set_song_pos(position=position)
```

### Track Numbering

- Track 0 = Master
- Track 1+ = Mixer inserts
- Channels start at 0

### Volume Ranges

- API volume: 0.0 to 1.0 (float)
- MIDI velocity: 0 to 127 (int)

Convert between them:

```python
# MIDI to API
api_volume = midi_velocity / 127.0

# API to MIDI
midi_velocity = int(api_volume * 127)
```

## Troubleshooting

### API Not Available

If FL Studio API calls fail:

1. **Check FL Studio is running**
2. **Verify you're on Windows** (FL Studio is Windows-only)
3. **Use MIDI as alternative** (works without FL Studio API)

### Import Errors

The server gracefully handles missing FL Studio modules:

- Returns stub modules when FL Studio not available
- MIDI features continue to work
- Error messages indicate unavailability

### Permission Issues

FL Studio API requires:

- Same user account as FL Studio
- No elevated privileges needed

## Advanced Usage

### Workflow Automation

```python
# Complete project setup
def setup_project():
    # Stop playback
    transport_stop()
    transport_set_song_pos(position=0)
    
    # Name mixer tracks
    mixer_set_track_name(track_num=1, name="Drums")
    mixer_set_track_name(track_num=2, name="Bass")
    mixer_set_track_name(track_num=3, name="Lead")
    
    # Set initial volumes
    mixer_set_track_volume(track_num=1, volume=0.8)
    mixer_set_track_volume(track_num=2, volume=0.7)
    mixer_set_track_volume(track_num=3, volume=0.6)
    
    # Name patterns
    patterns_set_pattern_name(pattern_num=0, name="Intro")
    patterns_set_pattern_name(pattern_num=1, name="Verse")
    patterns_set_pattern_name(pattern_num=2, name="Chorus")

setup_project()
```

### Combining with MIDI

Use FL Studio API for project structure and MIDI for note data:

```python
# Setup structure via API
mixer_set_track_name(track_num=1, name="Melody")
patterns_set_pattern_name(pattern_num=0, name="Main")

# Send notes via MIDI
midi_connect()
for note in [60, 64, 67, 72]:
    midi_send_note(note=note, velocity=80, duration=0.25)
```

## Reference

### FL Studio API Documentation

- [Official FL Studio Python API Docs](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm)
- [FL Studio API Stubs](https://pypi.org/project/fl-studio-api-stubs/)

### Window IDs

Common window IDs for `ui_show_window()`:

- 0: Mixer
- 1: Playlist
- 2: Channel Rack
- 3: Browser

## Next Steps

- [MIDI Integration](midi-integration.md)
- [Usage Examples](usage.md)
- [API Reference](api/server.md)

