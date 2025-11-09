# MIDI Integration

Guide to using MIDI features with FL Studio MCP Server.

## Overview

The server provides MIDI communication through the `mido` library, allowing you to send MIDI messages to FL Studio via virtual MIDI ports.

## Requirements

- [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) (Windows)
- FL Studio with MIDI port enabled
- No FL Studio API required - MIDI works independently

## loopMIDI Setup

### Installation

1. Download loopMIDI from [Tobias Erichsen's website](https://www.tobias-erichsen.de/software/loopmidi.html)
2. Run the installer
3. Launch loopMIDI

### Creating a Port

1. In loopMIDI, click the `+` button
2. Enter port name: `FLStudio_MIDI`
3. Click "Create"
4. The port appears in the list

### FL Studio Configuration

1. Open FL Studio
2. Options → MIDI Settings
3. Find `FLStudio_MIDI` in the list
4. Enable:
   - **Input**: ✓ Enabled
   - **Output**: ✓ Enabled
   - **Controller type**: Generic Controller

## MIDI Operations

### Connecting

```python
# List available ports
midi_list_ports()
# Output: Available MIDI ports:
#   Input: ['FLStudio_MIDI', ...]
#   Output: ['FLStudio_MIDI', ...]

# Connect to port
midi_connect()
# Output: Connected to MIDI port: FLStudio_MIDI
```

### Disconnecting

```python
midi_disconnect()
# Output: Disconnected from MIDI port: FLStudio_MIDI
```

### Sending Notes

#### Simple Notes

```python
# Send middle C for 0.5 seconds
midi_send_note(note=60)

# Custom velocity and duration
midi_send_note(note=64, velocity=100, duration=1.0)

# Specific channel
midi_send_note(note=60, velocity=80, duration=0.25, channel=1)
```

#### Manual Note Control

```python
# Note on
midi_send_note_on(note=60, velocity=100)

# Note off (later)
midi_send_note_off(note=60)
```

### Control Changes

```python
# Volume (CC 7)
midi_send_cc(control=7, value=100)

# Pan (CC 10)
midi_send_cc(control=10, value=64)  # Center
midi_send_cc(control=10, value=0)   # Hard left
midi_send_cc(control=10, value=127) # Hard right

# Modulation (CC 1)
midi_send_cc(control=1, value=80)

# Sustain pedal (CC 64)
midi_send_cc(control=64, value=127)  # On
midi_send_cc(control=64, value=0)    # Off
```

### Program Changes

```python
# Switch to program/preset 1
midi_send_program_change(program=0)

# Program 10 on channel 2
midi_send_program_change(program=9, channel=1)
```

### Pitch Bend

```python
# Bend up
midi_send_pitch_bend(pitch=2000)

# Bend down
midi_send_pitch_bend(pitch=-2000)

# Center (no bend)
midi_send_pitch_bend(pitch=0)
```

## MIDI Reference

### Note Numbers

Middle C = 60

```
C0 = 12   C#0 = 13  ...
C1 = 24   C#1 = 25  ...
C2 = 36   C#2 = 37  ...
C3 = 48   C#3 = 49  ...
C4 = 60   C#4 = 61  ...  (Middle C)
C5 = 72   C#5 = 73  ...
C6 = 84   C#6 = 85  ...
C7 = 96   C#7 = 97  ...
C8 = 108  C#8 = 109 ...
```

### Velocity Values

- 0: Note off (or silent)
- 1-31: Very soft (pp)
- 32-63: Soft (p)
- 64-95: Medium (mf)
- 96-127: Loud (ff)

### Common Control Changes

| CC  | Control          | Range   |
|-----|------------------|---------|
| 0   | Bank Select MSB  | 0-127   |
| 1   | Modulation Wheel | 0-127   |
| 7   | Volume           | 0-127   |
| 10  | Pan              | 0-127   |
| 11  | Expression       | 0-127   |
| 64  | Sustain Pedal    | 0-127   |
| 71  | Resonance        | 0-127   |
| 74  | Filter Cutoff    | 0-127   |
| 91  | Reverb Level     | 0-127   |
| 93  | Chorus Level     | 0-127   |

### MIDI Channels

- 0-15 (16 channels total)
- Channel 9 (index) = Channel 10 (display) = Drums (GM standard)

### Pitch Bend Range

- -8192 to 8191
- 0 = no bend
- Positive = bend up
- Negative = bend down

## Advanced Usage

### Chord Progression

```python
# Cmaj chord
midi_send_note_on(note=60, velocity=80)  # C
midi_send_note_on(note=64, velocity=80)  # E
midi_send_note_on(note=67, velocity=80)  # G

# Hold...
import time
time.sleep(1.0)

# Release
midi_send_note_off(note=60)
midi_send_note_off(note=64)
midi_send_note_off(note=67)
```

### Drum Pattern

```python
# Channel 9 = drums (GM standard)
drum_channel = 9

# Kick
midi_send_note(note=36, velocity=127, duration=0.1, channel=drum_channel)

# Snare
midi_send_note(note=38, velocity=100, duration=0.1, channel=drum_channel)

# Hi-hat
midi_send_note(note=42, velocity=80, duration=0.05, channel=drum_channel)
```

### Automation Curve

```python
# Fade in over time
for i in range(128):
    value = i
    midi_send_cc(control=7, value=value)  # Volume
    time.sleep(0.01)  # Adjust timing
```

### Multi-Channel Setup

```python
# Bass on channel 1
midi_send_note(note=36, velocity=100, channel=0)

# Pad on channel 2
midi_send_note(note=60, velocity=60, channel=1)
midi_send_note(note=64, velocity=60, channel=1)
midi_send_note(note=67, velocity=60, channel=1)

# Lead on channel 3
midi_send_note(note=72, velocity=90, channel=2)
```

## Troubleshooting

### Port Not Found

```python
# Check available ports
midi_list_ports()

# Verify loopMIDI is running
# Check port name matches exactly
```

### FL Studio Not Receiving

1. Options → MIDI Settings
2. Verify port is enabled
3. Check "Input" is ticked
4. Try test in FL Studio's MIDI monitor

### Timing Issues

For precise timing:

- Use `midi_send_note_on` / `midi_send_note_off`
- Control timing in your application
- Consider FL Studio's internal timing

### Note Stuck

If notes don't stop:

```python
# Send note off for all notes on a channel
for note in range(128):
    midi_send_note_off(note=note, channel=0)

# Or disconnect and reconnect
midi_disconnect()
midi_connect()
```

## Best Practices

### Always Connect

```python
# Connect before sending
midi_connect()
midi_send_note(note=60)
```

### Use Context Manager (in Python code)

```python
from fruityloops_mcp.midi_interface import MIDIInterface

with MIDIInterface() as midi:
    midi.send_note_on(60, 100)
    # Automatically disconnects
```

### Appropriate Durations

- Fast notes: 0.05-0.1s
- Normal notes: 0.25-0.5s
- Long notes: 1.0s+
- Sustained: Use note on/off

### Channel Organization

- 0-8: Melodic instruments
- 9: Drums (GM standard)
- 10-15: Additional instruments

## Integration with FL Studio

### Routing in FL Studio

1. MIDI input goes to selected channel
2. Use MIDI Out plugin to route between channels
3. Configure in Channel Settings → MIDI

### Recording MIDI

1. Enable recording on a channel
2. Use `transport_record()` via API
3. Send MIDI notes
4. MIDI is recorded to pattern

## Platform Notes

### Windows

- loopMIDI is the recommended virtual MIDI solution
- Works with all MIDI-enabled applications

### macOS / Linux

- Use system virtual MIDI ports
- Configure port name to match server
- May require additional setup

## Next Steps

- [FL Studio Integration](fl-studio-integration.md)
- [Usage Examples](usage.md)
- [API Reference](api/midi.md)

