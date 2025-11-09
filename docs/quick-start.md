# Quick Start Guide

Get up and running with FL Studio MCP Server in minutes.

## Step 1: Install

```bash
uvx fruityloops-mcp
```

## Step 2: Set Up loopMIDI

1. Download and install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
2. Create a port named `FLStudio_MIDI`
3. In FL Studio: Options → MIDI Settings → Enable the port

## Step 3: Configure Claude Desktop

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

## Step 4: Test MIDI

In Claude:

```python
# List available ports
midi_list_ports()

# Connect
midi_connect()

# Play middle C
midi_send_note(note=60, velocity=100, duration=0.5)
```

## Step 5: Control FL Studio

Start FL Studio, then in Claude:

```python
# Start playback
transport_start()

# Set mixer volume
mixer_set_track_volume(track_num=0, volume=0.8)

# Get project info
general_get_project_title()
```

## Common Tasks

### Send a Melody

```python
notes = [60, 64, 67, 72]  # C major arpeggio
for note in notes:
    midi_send_note(note=note, velocity=80, duration=0.25)
```

### Adjust Mix

```python
# Set volumes
mixer_set_track_volume(track_num=0, volume=0.8)  # Master
mixer_set_track_volume(track_num=1, volume=0.6)  # Drums

# Name tracks
mixer_set_track_name(track_num=1, name="Drums")
mixer_set_track_name(track_num=2, name="Bass")
```

### Control Transport

```python
# Start at beginning
transport_set_song_pos(position=0)
transport_start()

# Stop after 4 bars
# (position is in ticks, typically 960 PPQ)
transport_set_song_pos(position=3840)
transport_stop()
```

## Next Steps

- Explore [Usage Examples](usage.md)
- Read the [Full Installation Guide](installation.md)
- Check the [API Reference](api/server.md)

## Troubleshooting

### MIDI Not Working

1. Verify loopMIDI is running
2. Check port name matches `FLStudio_MIDI`
3. Run `midi_list_ports()` to see available ports

### FL Studio API Not Working

1. Ensure FL Studio is running
2. Check Python API is enabled in FL Studio settings
3. MIDI will still work even if FL Studio API is unavailable

## Help

- [GitHub Issues](https://github.com/quinnjr/fruityloops-mcp/issues)
- [Discussions](https://github.com/quinnjr/fruityloops-mcp/discussions)
- [Full Documentation](index.md)

