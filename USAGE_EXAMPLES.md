# Usage Examples

Practical examples for using the FL Studio MCP Server.

## Table of Contents

- [Basic Setup](#basic-setup)
- [MIDI Controls](#midi-controls)
- [FL Studio API](#fl-studio-api)
- [Advanced Usage](#advanced-usage)

## Basic Setup

### Starting the Server

```bash
# Using uvx (recommended)
uvx fruityloops-mcp

# Using uv
uv tool run fruityloops-mcp

# From source
uv run fruityloops-mcp
```

### Claude Desktop Configuration

Add to `claude_desktop_config.json`:

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

## MIDI Controls

### Connecting to MIDI Port

```python
# In Claude or any MCP client
midi_connect()
# Response: "Connected to MIDI port: FLStudio_MIDI"
```

### Listing Available Ports

```python
midi_list_ports()
# Response:
# "Available MIDI ports:
# Input: ['FLStudio_MIDI', 'Other Port']
# Output: ['FLStudio_MIDI', 'Other Port']"
```

### Sending MIDI Notes

#### Simple Note

```python
# Send middle C (60) for 0.5 seconds
midi_send_note(note=60)
```

#### Custom Velocity and Duration

```python
# Send note 64 (E) with velocity 100 for 1 second
midi_send_note(note=64, velocity=100, duration=1.0)
```

#### Specific MIDI Channel

```python
# Send note on channel 2 (drums)
midi_send_note(note=36, velocity=127, duration=0.25, channel=1)
```

### Manual Note On/Off

```python
# Start note
midi_send_note_on(note=60, velocity=100)

# ... do something else ...

# Stop note
midi_send_note_off(note=60)
```

### Control Change Messages

```python
# Set volume (CC 7) to 100
midi_send_cc(control=7, value=100)

# Set pan (CC 10) to center (64)
midi_send_cc(control=10, value=64, channel=0)

# Modulation wheel (CC 1)
midi_send_cc(control=1, value=80)
```

### Program Changes

```python
# Switch to program 5
midi_send_program_change(program=5)

# On specific channel
midi_send_program_change(program=10, channel=1)
```

### Pitch Bend

```python
# Bend up (positive value)
midi_send_pitch_bend(pitch=2000)

# Bend down (negative value)
midi_send_pitch_bend(pitch=-2000)

# Reset to center
midi_send_pitch_bend(pitch=0)
```

## FL Studio API

**Note**: FL Studio must be running for these to work.

### Transport Controls

```python
# Start playback
transport_start()

# Stop playback
transport_stop()

# Toggle recording
transport_record()

# Get current position
transport_get_song_pos()
# Response: "Current song position: 0"

# Set position
transport_set_song_pos(position=1920)  # 1 bar at 960 PPQ
```

### Mixer Controls

```python
# Get track volume
mixer_get_track_volume(track_num=0)
# Response: "Track 0 volume: 0.8"

# Set track volume
mixer_set_track_volume(track_num=0, volume=0.75)

# Get track name
mixer_get_track_name(track_num=1)
# Response: "Track 1 name: Kick"

# Set track name
mixer_set_track_name(track_num=1, name="Bass")
```

### Channel Controls

```python
# Get total channels
channels_channel_count()
# Response: "Total channels: 16"

# Get channel name
channels_get_channel_name(channel_num=0)
# Response: "Channel 0 name: Synth"

# Set channel volume
channels_set_channel_volume(channel_num=0, volume=0.9)

# Mute channel
channels_mute_channel(channel_num=0, mute=True)

# Unmute channel
channels_mute_channel(channel_num=0, mute=False)
```

### Pattern Controls

```python
# Get pattern count
patterns_pattern_count()
# Response: "Total patterns: 8"

# Get pattern name
patterns_get_pattern_name(pattern_num=0)
# Response: "Pattern 0 name: Intro"

# Set pattern name
patterns_set_pattern_name(pattern_num=0, name="Verse")
```

### Project Information

```python
# Get project title
general_get_project_title()
# Response: "Project title: My Song"

# Get FL Studio version
general_get_version()
# Response: "FL Studio version: 21.0.0"
```

### Playlist Controls

```python
# Get playlist track name
playlist_get_track_name(track_num=0)
# Response: "Playlist track 0 name: Melody"
```

### UI Controls

```python
# Show mixer window (window ID 0)
ui_show_window(window_id=0)

# Show playlist window (window ID 1)
ui_show_window(window_id=1)
```

## Advanced Usage

### Sequencing MIDI Notes

Create a simple melody:

```python
notes = [60, 64, 67, 72]  # C, E, G, C
for note in notes:
    midi_send_note(note=note, velocity=80, duration=0.5)
```

### Automation with Control Changes

Fade in:

```python
for value in range(0, 128, 8):
    midi_send_cc(control=7, value=value)  # Volume
    # Wait between steps (implemented in your logic)
```

### Multi-Channel Setup

```python
# Drums on channel 10
midi_send_note(note=36, velocity=127, channel=9)  # Kick

# Bass on channel 1
midi_send_note(note=40, velocity=100, channel=0)  # E1

# Melody on channel 2
midi_send_note(note=64, velocity=80, channel=1)  # E4
```

### FL Studio Workflow

Complete workflow example:

```python
# 1. Start fresh
transport_stop()
transport_set_song_pos(position=0)

# 2. Set up mixer
mixer_set_track_name(track_num=0, name="Master")
mixer_set_track_name(track_num=1, name="Drums")
mixer_set_track_volume(track_num=1, volume=0.8)

# 3. Set up patterns
patterns_set_pattern_name(pattern_num=0, name="Drums")
patterns_set_pattern_name(pattern_num=1, name="Melody")

# 4. Start playback
transport_start()
```

### Error Handling

All tools return text responses. Check for error messages:

```python
result = midi_connect()
if "Failed" in result:
    print("Connection failed!")
    # Try listing ports
    midi_list_ports()
else:
    print("Connected successfully!")
```

## Tips and Best Practices

### MIDI

1. **Always connect before sending MIDI**:
   ```python
   midi_connect()
   midi_send_note(note=60)
   ```

2. **Use note_on/note_off for sustained notes**:
   ```python
   midi_send_note_on(note=60)
   # ... play chord ...
   midi_send_note_off(note=60)
   ```

3. **Check available ports if connection fails**:
   ```python
   midi_list_ports()
   ```

### FL Studio

1. **FL Studio must be running** for API calls to work
2. **MIDI works independently** of FL Studio
3. **Use descriptive names** for tracks and patterns
4. **Set positions carefully** - values are in ticks (typically 960 PPQ)

### Performance

1. **Batch MIDI operations** when possible
2. **Use appropriate note durations** for your tempo
3. **Don't send too many CC messages** too quickly

## Troubleshooting

### MIDI Port Not Found

```python
# Check available ports
midi_list_ports()

# Ensure loopMIDI is running
# Ensure port name matches (default: "FLStudio_MIDI")
```

### FL Studio API Not Working

```python
# Verify FL Studio is running
general_get_version()

# If this fails, FL Studio API is not available
# MIDI will still work
```

### Notes Not Playing

```python
# Check connection
midi_connect()

# Verify FL Studio receives MIDI:
# Options → MIDI Settings → Enable FLStudio_MIDI input
```

## More Examples

For more examples, see:
- [README.md](README.md) - Quick start guide
- [Documentation](https://quinnjr.github.io/fruityloops-mcp/) - Full API reference
- [GitHub Issues](https://github.com/quinnjr/fruityloops-mcp/issues) - Community examples

## Contributing Examples

Have a cool example? [Submit a PR](CONTRIBUTING.md) or [open a discussion](https://github.com/quinnjr/fruityloops-mcp/discussions)!

