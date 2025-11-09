# Usage Guide

Comprehensive usage guide for FL Studio MCP Server.

## Basic Usage

### Connecting to MIDI

```python
# List available ports
midi_list_ports()

# Connect to default port
midi_connect()

# Check connection
# Returns: "Connected to MIDI port: FLStudio_MIDI"
```

### Sending MIDI Notes

```python
# Simple note (default: velocity=64, duration=0.5s)
midi_send_note(note=60)

# Custom parameters
midi_send_note(note=60, velocity=100, duration=1.0, channel=0)

# Manual control
midi_send_note_on(note=60, velocity=100)
# ... do something ...
midi_send_note_off(note=60)
```

### MIDI Control Changes

```python
# Volume (CC 7)
midi_send_cc(control=7, value=100)

# Pan (CC 10)
midi_send_cc(control=10, value=64)  # Center

# Custom CC
midi_send_cc(control=74, value=80, channel=0)
```

## FL Studio Control

**Note**: FL Studio must be running for these features.

### Transport

```python
# Playback control
transport_start()
transport_stop()
transport_record()

# Position control
transport_get_song_pos()  # Get current position
transport_set_song_pos(position=1920)  # Set position (in ticks)
```

### Mixer

```python
# Volume control
mixer_get_track_volume(track_num=0)
mixer_set_track_volume(track_num=0, volume=0.8)

# Track naming
mixer_get_track_name(track_num=1)
mixer_set_track_name(track_num=1, name="Drums")
```

### Channels

```python
# Get channel info
channels_channel_count()
channels_get_channel_name(channel_num=0)

# Control channels
channels_set_channel_volume(channel_num=0, volume=0.9)
channels_mute_channel(channel_num=0, mute=True)
```

### Patterns

```python
# Pattern info
patterns_pattern_count()
patterns_get_pattern_name(pattern_num=0)

# Rename pattern
patterns_set_pattern_name(pattern_num=0, name="Verse")
```

## Advanced Usage

### Creating a Melody

```python
# C major scale
notes = [60, 62, 64, 65, 67, 69, 71, 72]
for note in notes:
    midi_send_note(note=note, velocity=80, duration=0.25)
```

### Multi-Channel Setup

```python
# Drums on channel 10
midi_send_note(note=36, velocity=127, channel=9)  # Kick

# Bass on channel 1
midi_send_note(note=40, velocity=100, channel=0)

# Melody on channel 2
midi_send_note(note=64, velocity=80, channel=1)
```

### Automation

```python
# Fade in
for value in range(0, 128, 4):
    midi_send_cc(control=7, value=value)
    # Add delay if needed in your workflow
```

### Complete Workflow

```python
# 1. Setup
transport_stop()
transport_set_song_pos(position=0)

# 2. Configure mixer
mixer_set_track_name(track_num=1, name="Drums")
mixer_set_track_name(track_num=2, name="Bass")
mixer_set_track_volume(track_num=1, volume=0.8)

# 3. Setup patterns
patterns_set_pattern_name(pattern_num=0, name="Intro")
patterns_set_pattern_name(pattern_num=1, name="Verse")

# 4. Start playback
transport_start()
```

## MIDI Reference

### Note Numbers

| Note | Number | Octave |
|------|--------|--------|
| C0   | 12     | 0      |
| C1   | 24     | 1      |
| C2   | 36     | 2      |
| C3   | 48     | 3      |
| C4   | 60     | Middle |
| C5   | 72     | 5      |
| C6   | 84     | 6      |

### Control Change Messages

| CC  | Function        |
|-----|-----------------|
| 0   | Bank Select     |
| 1   | Modulation      |
| 7   | Volume          |
| 10  | Pan             |
| 11  | Expression      |
| 64  | Sustain Pedal   |
| 74  | Filter Cutoff   |
| 91  | Reverb Level    |
| 93  | Chorus Level    |

### Velocity Values

- **0**: Note off (or very soft)
- **1-31**: Pianissimo (pp)
- **32-63**: Piano (p)
- **64-95**: Mezzo-forte (mf)
- **96-127**: Fortissimo (ff)

## Error Handling

All tools return text responses. Check for error messages:

```python
result = midi_connect()
if "Failed" in result:
    print("Connection failed!")
    # Troubleshoot
    midi_list_ports()
else:
    print("Connected!")
```

## Best Practices

### MIDI

1. **Always connect first**
   ```python
   midi_connect()
   midi_send_note(note=60)
   ```

2. **Use appropriate durations**
   - Fast notes: 0.1-0.25s
   - Normal notes: 0.5s
   - Long notes: 1.0s+

3. **Check port availability**
   ```python
   midi_list_ports()
   ```

### FL Studio

1. **Keep FL Studio running** for API features
2. **Use descriptive names** for tracks and patterns
3. **Be careful with positions** - values are in ticks (typically 960 PPQ)

## Troubleshooting

### MIDI Not Working

```python
# Check ports
midi_list_ports()

# Verify loopMIDI is running
# Ensure FL Studio has port enabled
```

### FL Studio API Unavailable

```python
# Check if FL Studio is running
general_get_version()

# MIDI still works without FL Studio
midi_connect()
midi_send_note(note=60)
```

## Next Steps

- [FL Studio Integration](fl-studio-integration.md)
- [MIDI Integration](midi-integration.md)
- [API Reference](api/server.md)

