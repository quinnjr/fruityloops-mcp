# MIDI Interface API Reference

Auto-generated API documentation for the MIDI interface.

## MIDIInterface

::: fruityloops_mcp.midi_interface.MIDIInterface
    options:
      show_source: true
      heading_level: 3
      members:
        - __init__
        - connect
        - disconnect
        - is_connected
        - send_note_on
        - send_note_off
        - send_control_change
        - send_program_change
        - send_pitch_bend
        - list_ports
        - __enter__
        - __exit__

## Usage Examples

### Basic Usage

```python
from fruityloops_mcp.midi_interface import MIDIInterface

# Create interface
midi = MIDIInterface(port_name="FLStudio_MIDI")

# Connect
if midi.connect():
    # Send a note
    midi.send_note_on(60, 100)
    # ... wait ...
    midi.send_note_off(60)
    
    # Disconnect
    midi.disconnect()
```

### Context Manager

```python
with MIDIInterface(port_name="FLStudio_MIDI") as midi:
    # Automatically connects
    midi.send_note_on(60, 100)
    # ... 
    # Automatically disconnects
```

### Checking Connection Status

```python
midi = MIDIInterface()
midi.connect()

if midi.is_connected:
    midi.send_note_on(60)
```

### Listing Ports

```python
midi = MIDIInterface()
ports = midi.list_ports()

print("Input ports:", ports["input"])
print("Output ports:", ports["output"])
```

## Method Details

### send_note_on

Send a MIDI note on message.

**Parameters:**
- `note` (int): MIDI note number (0-127)
- `velocity` (int): Note velocity (0-127), default=64
- `channel` (int): MIDI channel (0-15), default=0

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
midi.send_note_on(60, 100, 0)  # Middle C, forte, channel 1
```

### send_note_off

Send a MIDI note off message.

**Parameters:**
- `note` (int): MIDI note number (0-127)
- `velocity` (int): Release velocity (0-127), default=64
- `channel` (int): MIDI channel (0-15), default=0

**Returns:**
- `bool`: True if successful, False otherwise

### send_control_change

Send a MIDI control change message.

**Parameters:**
- `control` (int): Controller number (0-127)
- `value` (int): Controller value (0-127)
- `channel` (int): MIDI channel (0-15), default=0

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
midi.send_control_change(7, 100)  # Volume to 100
midi.send_control_change(10, 64)  # Pan to center
```

### send_program_change

Send a MIDI program change message.

**Parameters:**
- `program` (int): Program number (0-127)
- `channel` (int): MIDI channel (0-15), default=0

**Returns:**
- `bool`: True if successful, False otherwise

### send_pitch_bend

Send a MIDI pitch bend message.

**Parameters:**
- `pitch` (int): Pitch bend value (-8192 to 8191)
- `channel` (int): MIDI channel (0-15), default=0

**Returns:**
- `bool`: True if successful, False otherwise

## Error Handling

Methods return `False` on error and log warnings/errors. Check return values:

```python
if not midi.send_note_on(60):
    print("Failed to send note")
```

## See Also

- [Server API](server.md)
- [MIDI Integration Guide](../midi-integration.md)
- [Usage Examples](../usage.md)

