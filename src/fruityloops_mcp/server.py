"""Main MCP server implementation for FL Studio API via Flapi.

This server provides MCP tools for controlling FL Studio through:
1. Flapi - A bridge that forwards FL Studio API calls to FL Studio via MIDI
2. Direct MIDI - For sending MIDI notes, CC, and other MIDI messages

Architecture:
    Claude Desktop → MCP Server → Flapi → FL Studio (internal Python)
                              ↘ MIDI Interface → FL Studio (MIDI input)
"""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from fruityloops_mcp.flapi_bridge import FLStudioBridge, get_bridge
from fruityloops_mcp.midi_interface import MIDIInterface

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FLStudioMCPServer:
    """MCP Server for FL Studio Python API integration via Flapi."""

    def __init__(self, midi_port: str = "FLStudio_MIDI"):
        """Initialize the FL Studio MCP server.

        Args:
            midi_port: Name of the MIDI port to use for direct MIDI interface
        """
        self.server = Server("fruityloops-mcp")
        self.midi = MIDIInterface(port_name=midi_port)
        self.flapi_bridge: FLStudioBridge = get_bridge()
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Set up request handlers for the MCP server."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools."""
            tools = [
                # =========================================================
                # Flapi Connection Tools
                # =========================================================
                Tool(
                    name="flapi_connect",
                    description="Connect to FL Studio via Flapi. Must be called before using FL Studio API tools. Requires Flapi to be installed in FL Studio and virtual MIDI ports configured.",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="flapi_disconnect",
                    description="Disconnect from FL Studio via Flapi",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="flapi_status",
                    description="Get Flapi connection status and test connectivity to FL Studio",
                    inputSchema={"type": "object", "properties": {}},
                ),
                # =========================================================
                # MIDI Tools (always available via loopMIDI)
                # =========================================================
                Tool(
                    name="midi_connect",
                    description="Connect to MIDI port for sending MIDI messages",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="midi_disconnect",
                    description="Disconnect from MIDI port",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="midi_list_ports",
                    description="List available MIDI input and output ports",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="midi_send_note",
                    description="Send a MIDI note with specified duration (note on + wait + note off)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "note": {
                                "type": "integer",
                                "description": "MIDI note number (0-127). Middle C is 60.",
                                "minimum": 0,
                                "maximum": 127,
                            },
                            "velocity": {
                                "type": "integer",
                                "description": "Note velocity (0-127)",
                                "default": 64,
                                "minimum": 0,
                                "maximum": 127,
                            },
                            "duration": {
                                "type": "number",
                                "description": "Note duration in seconds",
                                "default": 0.5,
                                "minimum": 0,
                            },
                            "channel": {
                                "type": "integer",
                                "description": "MIDI channel (0-15)",
                                "default": 0,
                                "minimum": 0,
                                "maximum": 15,
                            },
                        },
                        "required": ["note"],
                    },
                ),
                Tool(
                    name="midi_send_note_on",
                    description="Send a MIDI note on message",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "note": {
                                "type": "integer",
                                "description": "MIDI note number (0-127)",
                                "minimum": 0,
                                "maximum": 127,
                            },
                            "velocity": {
                                "type": "integer",
                                "description": "Note velocity (0-127)",
                                "default": 64,
                                "minimum": 0,
                                "maximum": 127,
                            },
                            "channel": {
                                "type": "integer",
                                "description": "MIDI channel (0-15)",
                                "default": 0,
                                "minimum": 0,
                                "maximum": 15,
                            },
                        },
                        "required": ["note"],
                    },
                ),
                Tool(
                    name="midi_send_note_off",
                    description="Send a MIDI note off message",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "note": {
                                "type": "integer",
                                "description": "MIDI note number (0-127)",
                                "minimum": 0,
                                "maximum": 127,
                            },
                            "velocity": {
                                "type": "integer",
                                "description": "Note velocity (0-127)",
                                "default": 64,
                                "minimum": 0,
                                "maximum": 127,
                            },
                            "channel": {
                                "type": "integer",
                                "description": "MIDI channel (0-15)",
                                "default": 0,
                                "minimum": 0,
                                "maximum": 15,
                            },
                        },
                        "required": ["note"],
                    },
                ),
                Tool(
                    name="midi_send_cc",
                    description="Send a MIDI control change message",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "control": {
                                "type": "integer",
                                "description": "Control number (0-127)",
                                "minimum": 0,
                                "maximum": 127,
                            },
                            "value": {
                                "type": "integer",
                                "description": "Control value (0-127)",
                                "minimum": 0,
                                "maximum": 127,
                            },
                            "channel": {
                                "type": "integer",
                                "description": "MIDI channel (0-15)",
                                "default": 0,
                                "minimum": 0,
                                "maximum": 15,
                            },
                        },
                        "required": ["control", "value"],
                    },
                ),
                Tool(
                    name="midi_send_program_change",
                    description="Send a MIDI program change message to switch instruments/patches",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "program": {
                                "type": "integer",
                                "description": "Program number (0-127)",
                                "minimum": 0,
                                "maximum": 127,
                            },
                            "channel": {
                                "type": "integer",
                                "description": "MIDI channel (0-15)",
                                "default": 0,
                                "minimum": 0,
                                "maximum": 15,
                            },
                        },
                        "required": ["program"],
                    },
                ),
                Tool(
                    name="midi_send_pitch_bend",
                    description="Send a MIDI pitch bend message",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pitch": {
                                "type": "integer",
                                "description": "Pitch bend value (-8192 to 8191, 0 is center)",
                                "minimum": -8192,
                                "maximum": 8191,
                            },
                            "channel": {
                                "type": "integer",
                                "description": "MIDI channel (0-15)",
                                "default": 0,
                                "minimum": 0,
                                "maximum": 15,
                            },
                        },
                        "required": ["pitch"],
                    },
                ),
                # =========================================================
                # FL Studio Transport Controls (via Flapi)
                # =========================================================
                Tool(
                    name="transport_start",
                    description="Start FL Studio playback. Requires Flapi connection.",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="transport_stop",
                    description="Stop FL Studio playback. Requires Flapi connection.",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="transport_record",
                    description="Toggle recording in FL Studio. Requires Flapi connection.",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="transport_get_song_pos",
                    description="Get current song position. Requires Flapi connection.",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="transport_set_song_pos",
                    description="Set song position. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "position": {
                                "type": "integer",
                                "description": "Song position in ticks",
                            }
                        },
                        "required": ["position"],
                    },
                ),
                Tool(
                    name="transport_get_bpm",
                    description="Get current tempo (BPM). Requires Flapi connection.",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="transport_set_bpm",
                    description="Set tempo (BPM). Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "bpm": {
                                "type": "number",
                                "description": "Tempo in beats per minute",
                                "minimum": 10,
                                "maximum": 522,
                            }
                        },
                        "required": ["bpm"],
                    },
                ),
                # =========================================================
                # FL Studio Mixer Controls (via Flapi)
                # =========================================================
                Tool(
                    name="mixer_get_track_volume",
                    description="Get mixer track volume. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "track_num": {
                                "type": "integer",
                                "description": "Mixer track number (0 is master)",
                            }
                        },
                        "required": ["track_num"],
                    },
                ),
                Tool(
                    name="mixer_set_track_volume",
                    description="Set mixer track volume. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "track_num": {
                                "type": "integer",
                                "description": "Mixer track number",
                            },
                            "volume": {
                                "type": "number",
                                "description": "Volume level (0.0-1.0)",
                                "minimum": 0,
                                "maximum": 1,
                            },
                        },
                        "required": ["track_num", "volume"],
                    },
                ),
                Tool(
                    name="mixer_get_track_name",
                    description="Get mixer track name. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "track_num": {
                                "type": "integer",
                                "description": "Mixer track number",
                            }
                        },
                        "required": ["track_num"],
                    },
                ),
                Tool(
                    name="mixer_set_track_name",
                    description="Set mixer track name. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "track_num": {
                                "type": "integer",
                                "description": "Mixer track number",
                            },
                            "name": {"type": "string", "description": "Track name"},
                        },
                        "required": ["track_num", "name"],
                    },
                ),
                Tool(
                    name="mixer_get_track_pan",
                    description="Get mixer track pan. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "track_num": {
                                "type": "integer",
                                "description": "Mixer track number",
                            }
                        },
                        "required": ["track_num"],
                    },
                ),
                Tool(
                    name="mixer_set_track_pan",
                    description="Set mixer track pan. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "track_num": {
                                "type": "integer",
                                "description": "Mixer track number",
                            },
                            "pan": {
                                "type": "number",
                                "description": "Pan value (-1.0 left to 1.0 right, 0 center)",
                                "minimum": -1,
                                "maximum": 1,
                            },
                        },
                        "required": ["track_num", "pan"],
                    },
                ),
                Tool(
                    name="mixer_mute_track",
                    description="Mute or unmute a mixer track. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "track_num": {
                                "type": "integer",
                                "description": "Mixer track number",
                            },
                            "mute": {
                                "type": "boolean",
                                "description": "True to mute, False to unmute",
                            },
                        },
                        "required": ["track_num", "mute"],
                    },
                ),
                Tool(
                    name="mixer_solo_track",
                    description="Solo or unsolo a mixer track. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "track_num": {
                                "type": "integer",
                                "description": "Mixer track number",
                            },
                            "solo": {
                                "type": "boolean",
                                "description": "True to solo, False to unsolo",
                            },
                        },
                        "required": ["track_num", "solo"],
                    },
                ),
                # =========================================================
                # FL Studio Channel Controls (via Flapi)
                # =========================================================
                Tool(
                    name="channels_channel_count",
                    description="Get total number of channels. Requires Flapi connection.",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="channels_get_channel_name",
                    description="Get channel name. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "channel_num": {
                                "type": "integer",
                                "description": "Channel number",
                            }
                        },
                        "required": ["channel_num"],
                    },
                ),
                Tool(
                    name="channels_set_channel_volume",
                    description="Set channel volume. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "channel_num": {
                                "type": "integer",
                                "description": "Channel number",
                            },
                            "volume": {
                                "type": "number",
                                "description": "Volume level (0.0-1.0)",
                                "minimum": 0,
                                "maximum": 1,
                            },
                        },
                        "required": ["channel_num", "volume"],
                    },
                ),
                Tool(
                    name="channels_mute_channel",
                    description="Mute or unmute a channel. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "channel_num": {
                                "type": "integer",
                                "description": "Channel number",
                            },
                            "mute": {
                                "type": "boolean",
                                "description": "True to mute, False to unmute",
                            },
                        },
                        "required": ["channel_num", "mute"],
                    },
                ),
                Tool(
                    name="channels_get_channel_color",
                    description="Get channel color as integer. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "channel_num": {
                                "type": "integer",
                                "description": "Channel number",
                            }
                        },
                        "required": ["channel_num"],
                    },
                ),
                Tool(
                    name="channels_set_channel_color",
                    description="Set channel color. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "channel_num": {
                                "type": "integer",
                                "description": "Channel number",
                            },
                            "color": {
                                "type": "integer",
                                "description": "Color as integer (RGB)",
                            },
                        },
                        "required": ["channel_num", "color"],
                    },
                ),
                # =========================================================
                # FL Studio Pattern Controls (via Flapi)
                # =========================================================
                Tool(
                    name="patterns_pattern_count",
                    description="Get total number of patterns. Requires Flapi connection.",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="patterns_get_pattern_name",
                    description="Get pattern name. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pattern_num": {
                                "type": "integer",
                                "description": "Pattern number",
                            }
                        },
                        "required": ["pattern_num"],
                    },
                ),
                Tool(
                    name="patterns_set_pattern_name",
                    description="Set pattern name. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pattern_num": {
                                "type": "integer",
                                "description": "Pattern number",
                            },
                            "name": {"type": "string", "description": "Pattern name"},
                        },
                        "required": ["pattern_num", "name"],
                    },
                ),
                Tool(
                    name="patterns_get_pattern_length",
                    description="Get pattern length in beats. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pattern_num": {
                                "type": "integer",
                                "description": "Pattern number",
                            }
                        },
                        "required": ["pattern_num"],
                    },
                ),
                Tool(
                    name="patterns_jump_to_pattern",
                    description="Jump to a specific pattern. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pattern_num": {
                                "type": "integer",
                                "description": "Pattern number to jump to",
                            }
                        },
                        "required": ["pattern_num"],
                    },
                ),
                # =========================================================
                # FL Studio Playlist Controls (via Flapi)
                # =========================================================
                Tool(
                    name="playlist_get_track_name",
                    description="Get playlist track name. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "track_num": {
                                "type": "integer",
                                "description": "Playlist track number",
                            }
                        },
                        "required": ["track_num"],
                    },
                ),
                Tool(
                    name="playlist_set_track_name",
                    description="Set playlist track name. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "track_num": {
                                "type": "integer",
                                "description": "Playlist track number",
                            },
                            "name": {"type": "string", "description": "Track name"},
                        },
                        "required": ["track_num", "name"],
                    },
                ),
                # =========================================================
                # FL Studio General / Project Controls (via Flapi)
                # =========================================================
                Tool(
                    name="general_get_project_title",
                    description="Get the current project title. Requires Flapi connection.",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="general_get_version",
                    description="Get FL Studio version. Requires Flapi connection.",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="general_save_project",
                    description="Save the current project. Requires Flapi connection.",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="general_undo",
                    description="Undo the last action. Requires Flapi connection.",
                    inputSchema={"type": "object", "properties": {}},
                ),
                # =========================================================
                # FL Studio UI Controls (via Flapi)
                # =========================================================
                Tool(
                    name="ui_show_window",
                    description="Show a specific FL Studio window. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "window_id": {
                                "type": "integer",
                                "description": "Window ID (0=Mixer, 1=Channel Rack, 2=Piano Roll, 3=Browser, 4=Playlist)",
                            }
                        },
                        "required": ["window_id"],
                    },
                ),
                Tool(
                    name="ui_get_visible",
                    description="Check if a window is visible. Requires Flapi connection.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "window_id": {
                                "type": "integer",
                                "description": "Window ID to check",
                            }
                        },
                        "required": ["window_id"],
                    },
                ),
            ]

            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            """Execute a tool by name with given arguments."""
            try:
                result = await self._execute_tool(name, arguments)
                return [TextContent(type="text", text=result)]
            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}")
                return [TextContent(type="text", text=f"Error: {e}")]

    async def _execute_tool(self, name: str, args: dict[str, Any]) -> str:
        """Execute a specific tool with arguments.

        Args:
            name: Tool name
            args: Tool arguments

        Returns:
            Result string

        Raises:
            ValueError: If tool name is unknown
        """
        # =================================================================
        # Flapi Connection Tools
        # =================================================================
        if name == "flapi_connect":
            success = self.flapi_bridge.enable()
            if success:
                return "Connected to FL Studio via Flapi. FL Studio API tools are now available."
            else:
                return (
                    "Failed to connect to FL Studio via Flapi. "
                    "Make sure:\n"
                    "1. Flapi is installed: pip install flapi && flapi install\n"
                    "2. Virtual MIDI ports 'Flapi Request' and 'Flapi Response' are created (use loopMIDI on Windows)\n"
                    "3. FL Studio is running with the Flapi script enabled\n"
                    "4. FL Studio MIDI settings are configured for Flapi ports"
                )
        elif name == "flapi_disconnect":
            self.flapi_bridge.disable()
            return "Disconnected from FL Studio via Flapi"
        elif name == "flapi_status":
            status_parts = [
                f"Flapi library available: {self.flapi_bridge.is_available}",
                f"Flapi enabled: {self.flapi_bridge.is_enabled}",
            ]
            if self.flapi_bridge.is_enabled:
                connected = self.flapi_bridge.test_connection()
                status_parts.append(f"FL Studio connection: {'OK' if connected else 'FAILED'}")
            return "\n".join(status_parts)

        # =================================================================
        # MIDI Tools
        # =================================================================
        elif name == "midi_connect":
            success = self.midi.connect()
            return (
                f"Connected to MIDI port: {self.midi.port_name}"
                if success
                else f"Failed to connect to MIDI port: {self.midi.port_name}"
            )
        elif name == "midi_disconnect":
            self.midi.disconnect()
            return f"Disconnected from MIDI port: {self.midi.port_name}"
        elif name == "midi_list_ports":
            ports = self.midi.list_ports()
            return f"Available MIDI ports:\nInput: {ports['input']}\nOutput: {ports['output']}"
        elif name == "midi_send_note":
            note = args["note"]
            velocity = args.get("velocity", 64)
            duration = args.get("duration", 0.5)
            channel = args.get("channel", 0)

            self.midi.send_note_on(note, velocity, channel)
            await asyncio.sleep(duration)
            self.midi.send_note_off(note, velocity, channel)
            return f"Sent MIDI note {note} with velocity {velocity} for {duration}s on channel {channel}"
        elif name == "midi_send_note_on":
            note = args["note"]
            velocity = args.get("velocity", 64)
            channel = args.get("channel", 0)
            success = self.midi.send_note_on(note, velocity, channel)
            return (
                f"Sent MIDI note_on: note={note}, velocity={velocity}, channel={channel}"
                if success
                else f"Failed to send MIDI note_on: note={note}"
            )
        elif name == "midi_send_note_off":
            note = args["note"]
            velocity = args.get("velocity", 64)
            channel = args.get("channel", 0)
            success = self.midi.send_note_off(note, velocity, channel)
            return (
                f"Sent MIDI note_off: note={note}, velocity={velocity}, channel={channel}"
                if success
                else f"Failed to send MIDI note_off: note={note}"
            )
        elif name == "midi_send_cc":
            control = args["control"]
            value = args["value"]
            channel = args.get("channel", 0)
            success = self.midi.send_control_change(control, value, channel)
            return (
                f"Sent MIDI CC: control={control}, value={value}, channel={channel}"
                if success
                else f"Failed to send MIDI CC: control={control}"
            )
        elif name == "midi_send_program_change":
            program = args["program"]
            channel = args.get("channel", 0)
            success = self.midi.send_program_change(program, channel)
            return (
                f"Sent MIDI program change: program={program}, channel={channel}"
                if success
                else f"Failed to send MIDI program change: program={program}"
            )
        elif name == "midi_send_pitch_bend":
            pitch = args["pitch"]
            channel = args.get("channel", 0)
            success = self.midi.send_pitch_bend(pitch, channel)
            return (
                f"Sent MIDI pitch bend: pitch={pitch}, channel={channel}"
                if success
                else f"Failed to send MIDI pitch bend: pitch={pitch}"
            )

        # =================================================================
        # FL Studio Transport Tools (via Flapi)
        # =================================================================
        elif name == "transport_start":
            return self.flapi_bridge.transport_start()
        elif name == "transport_stop":
            return self.flapi_bridge.transport_stop()
        elif name == "transport_record":
            return self.flapi_bridge.transport_record()
        elif name == "transport_get_song_pos":
            return self.flapi_bridge.transport_get_song_pos()
        elif name == "transport_set_song_pos":
            position = args["position"]
            return self.flapi_bridge.transport_set_song_pos(position)
        elif name == "transport_get_bpm":
            return self.flapi_bridge.transport_get_bpm()
        elif name == "transport_set_bpm":
            bpm = args["bpm"]
            return self.flapi_bridge.transport_set_bpm(bpm)

        # =================================================================
        # FL Studio Mixer Tools (via Flapi)
        # =================================================================
        elif name == "mixer_get_track_volume":
            track_num = args["track_num"]
            return self.flapi_bridge.mixer_get_track_volume(track_num)
        elif name == "mixer_set_track_volume":
            track_num = args["track_num"]
            volume = args["volume"]
            return self.flapi_bridge.mixer_set_track_volume(track_num, volume)
        elif name == "mixer_get_track_name":
            track_num = args["track_num"]
            return self.flapi_bridge.mixer_get_track_name(track_num)
        elif name == "mixer_set_track_name":
            track_num = args["track_num"]
            name_str = args["name"]
            return self.flapi_bridge.mixer_set_track_name(track_num, name_str)
        elif name == "mixer_get_track_pan":
            track_num = args["track_num"]
            return self.flapi_bridge.mixer_get_track_pan(track_num)
        elif name == "mixer_set_track_pan":
            track_num = args["track_num"]
            pan = args["pan"]
            return self.flapi_bridge.mixer_set_track_pan(track_num, pan)
        elif name == "mixer_mute_track":
            track_num = args["track_num"]
            mute = args["mute"]
            return self.flapi_bridge.mixer_mute_track(track_num, mute)
        elif name == "mixer_solo_track":
            track_num = args["track_num"]
            solo = args["solo"]
            return self.flapi_bridge.mixer_solo_track(track_num, solo)

        # =================================================================
        # FL Studio Channel Tools (via Flapi)
        # =================================================================
        elif name == "channels_channel_count":
            return self.flapi_bridge.channels_count()
        elif name == "channels_get_channel_name":
            channel_num = args["channel_num"]
            return self.flapi_bridge.channels_get_name(channel_num)
        elif name == "channels_set_channel_volume":
            channel_num = args["channel_num"]
            volume = args["volume"]
            return self.flapi_bridge.channels_set_volume(channel_num, volume)
        elif name == "channels_mute_channel":
            channel_num = args["channel_num"]
            mute = args["mute"]
            return self.flapi_bridge.channels_mute(channel_num, mute)
        elif name == "channels_get_channel_color":
            channel_num = args["channel_num"]
            return self.flapi_bridge.channels_get_color(channel_num)
        elif name == "channels_set_channel_color":
            channel_num = args["channel_num"]
            color = args["color"]
            return self.flapi_bridge.channels_set_color(channel_num, color)

        # =================================================================
        # FL Studio Pattern Tools (via Flapi)
        # =================================================================
        elif name == "patterns_pattern_count":
            return self.flapi_bridge.patterns_count()
        elif name == "patterns_get_pattern_name":
            pattern_num = args["pattern_num"]
            return self.flapi_bridge.patterns_get_name(pattern_num)
        elif name == "patterns_set_pattern_name":
            pattern_num = args["pattern_num"]
            name_str = args["name"]
            return self.flapi_bridge.patterns_set_name(pattern_num, name_str)
        elif name == "patterns_get_pattern_length":
            pattern_num = args["pattern_num"]
            return self.flapi_bridge.patterns_get_length(pattern_num)
        elif name == "patterns_jump_to_pattern":
            pattern_num = args["pattern_num"]
            return self.flapi_bridge.patterns_jump_to(pattern_num)

        # =================================================================
        # FL Studio Playlist Tools (via Flapi)
        # =================================================================
        elif name == "playlist_get_track_name":
            track_num = args["track_num"]
            return self.flapi_bridge.playlist_get_track_name(track_num)
        elif name == "playlist_set_track_name":
            track_num = args["track_num"]
            name_str = args["name"]
            return self.flapi_bridge.playlist_set_track_name(track_num, name_str)

        # =================================================================
        # FL Studio General / Project Tools (via Flapi)
        # =================================================================
        elif name == "general_get_project_title":
            return self.flapi_bridge.general_get_project_title()
        elif name == "general_get_version":
            return self.flapi_bridge.general_get_version()
        elif name == "general_save_project":
            return self.flapi_bridge.general_save_project()
        elif name == "general_undo":
            return self.flapi_bridge.general_undo()

        # =================================================================
        # FL Studio UI Tools (via Flapi)
        # =================================================================
        elif name == "ui_show_window":
            window_id = args["window_id"]
            return self.flapi_bridge.ui_show_window(window_id)
        elif name == "ui_get_visible":
            window_id = args["window_id"]
            return self.flapi_bridge.ui_get_visible(window_id)

        else:
            raise ValueError(f"Unknown tool: {name}")

    async def run(self) -> None:
        """Run the MCP server using stdio transport."""
        try:
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options(),
                )
        except Exception as e:
            logger.error(f"Error running MCP server: {e}")


def main() -> None:
    """Main entry point for the FL Studio MCP server."""
    logger.info("FL Studio MCP Server starting...")
    logger.info("Using Flapi for FL Studio API communication")
    server = FLStudioMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
