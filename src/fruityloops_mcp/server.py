"""Main MCP server implementation for FL Studio API."""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from fruityloops_mcp.midi_interface import MIDIInterface

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create stub module class for when FL Studio API is not available
class StubModule:
    """A stub module that returns itself for any attribute access or call."""

    def __init__(self, name: str) -> None:
        self._name = name

    def __getattr__(self, item: str) -> "StubModule":
        return self

    def __call__(self, *_args: Any, **_kwargs: Any) -> "StubModule":
        return self


# Import FL Studio API modules (these will only work when FL Studio is running)
try:
    import channels
    import general
    import mixer
    import patterns
    import playlist
    import transport
    import ui

    FL_STUDIO_AVAILABLE = True
except ImportError:
    logger.warning("FL Studio API not available. Running in stub mode.")
    FL_STUDIO_AVAILABLE = False

    # Create stub modules that return themselves for any attribute access
    transport = StubModule("transport")
    mixer = StubModule("mixer")
    channels = StubModule("channels")
    patterns = StubModule("patterns")
    general = StubModule("general")
    ui = StubModule("ui")
    playlist = StubModule("playlist")


class FLStudioMCPServer:
    """MCP Server for FL Studio Python API integration."""

    def __init__(self, midi_port: str = "FLStudio_MIDI"):
        """Initialize the FL Studio MCP server.

        Args:
            midi_port: Name of the MIDI port to use for MIDI interface
        """
        self.server = Server("fruityloops-mcp")
        self.midi = MIDIInterface(port_name=midi_port)
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Set up request handlers for the MCP server."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools."""
            tools = [
                # MIDI Tools (always available)
                Tool(
                    name="midi_connect",
                    description="Connect to MIDI port",
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
                    description="Send a MIDI note with specified duration",
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
                    description="Send a MIDI program change message",
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
                                "description": "Pitch bend value (-8192 to 8191)",
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
            ]

            # FL Studio tools (only if FL Studio is available)
            if FL_STUDIO_AVAILABLE:
                fl_tools = [
                    # Transport controls
                    Tool(
                        name="transport_start",
                        description="Start FL Studio playback",
                        inputSchema={"type": "object", "properties": {}},
                    ),
                    Tool(
                        name="transport_stop",
                        description="Stop FL Studio playback",
                        inputSchema={"type": "object", "properties": {}},
                    ),
                    Tool(
                        name="transport_record",
                        description="Toggle recording in FL Studio",
                        inputSchema={"type": "object", "properties": {}},
                    ),
                    Tool(
                        name="transport_get_song_pos",
                        description="Get current song position",
                        inputSchema={"type": "object", "properties": {}},
                    ),
                    Tool(
                        name="transport_set_song_pos",
                        description="Set song position",
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
                    # Mixer controls
                    Tool(
                        name="mixer_get_track_volume",
                        description="Get mixer track volume",
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
                        name="mixer_set_track_volume",
                        description="Set mixer track volume",
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
                                },
                            },
                            "required": ["track_num", "volume"],
                        },
                    ),
                    Tool(
                        name="mixer_get_track_name",
                        description="Get mixer track name",
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
                        description="Set mixer track name",
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
                    # Channel controls
                    Tool(
                        name="channels_channel_count",
                        description="Get total number of channels",
                        inputSchema={"type": "object", "properties": {}},
                    ),
                    Tool(
                        name="channels_get_channel_name",
                        description="Get channel name",
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
                        description="Set channel volume",
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
                                },
                            },
                            "required": ["channel_num", "volume"],
                        },
                    ),
                    Tool(
                        name="channels_mute_channel",
                        description="Mute or unmute a channel",
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
                    # Pattern controls
                    Tool(
                        name="patterns_pattern_count",
                        description="Get total number of patterns",
                        inputSchema={"type": "object", "properties": {}},
                    ),
                    Tool(
                        name="patterns_get_pattern_name",
                        description="Get pattern name",
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
                        description="Set pattern name",
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
                    # General controls
                    Tool(
                        name="general_get_project_title",
                        description="Get the current project title",
                        inputSchema={"type": "object", "properties": {}},
                    ),
                    Tool(
                        name="general_get_version",
                        description="Get FL Studio version",
                        inputSchema={"type": "object", "properties": {}},
                    ),
                    # UI controls
                    Tool(
                        name="ui_show_window",
                        description="Show a specific FL Studio window",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "window_id": {
                                    "type": "integer",
                                    "description": "Window ID to show",
                                }
                            },
                            "required": ["window_id"],
                        },
                    ),
                    # Playlist controls
                    Tool(
                        name="playlist_get_track_name",
                        description="Get playlist track name",
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
                ]
                tools.extend(fl_tools)

            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            """Execute a tool by name with given arguments."""
            try:
                # Check if FL Studio tool is being called without FL Studio available
                if not name.startswith("midi_") and not FL_STUDIO_AVAILABLE:
                    return [
                        TextContent(
                            type="text",
                            text=f"FL Studio API not available. Tool '{name}' cannot be executed.",
                        )
                    ]

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
        # MIDI Tools
        if name == "midi_connect":
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

        # FL Studio Transport Tools
        elif name == "transport_start":
            transport.start()
            return "FL Studio playback started"
        elif name == "transport_stop":
            transport.stop()
            return "FL Studio playback stopped"
        elif name == "transport_record":
            transport.record()
            return "FL Studio recording toggled"
        elif name == "transport_get_song_pos":
            pos = transport.getSongPos()
            return f"Current song position: {pos}"
        elif name == "transport_set_song_pos":
            position = args["position"]
            transport.setSongPos(position)
            return f"Song position set to: {position}"

        # FL Studio Mixer Tools
        elif name == "mixer_get_track_volume":
            track_num = args["track_num"]
            volume = mixer.getTrackVolume(track_num)
            return f"Track {track_num} volume: {volume}"
        elif name == "mixer_set_track_volume":
            track_num = args["track_num"]
            volume = args["volume"]
            mixer.setTrackVolume(track_num, volume)
            return f"Track {track_num} volume set to: {volume}"
        elif name == "mixer_get_track_name":
            track_num = args["track_num"]
            name_str = mixer.getTrackName(track_num)
            return f"Track {track_num} name: {name_str}"
        elif name == "mixer_set_track_name":
            track_num = args["track_num"]
            name_str = args["name"]
            mixer.setTrackName(track_num, name_str)
            return f"Track {track_num} name set to: {name_str}"

        # FL Studio Channel Tools
        elif name == "channels_channel_count":
            count = channels.channelCount()
            return f"Total channels: {count}"
        elif name == "channels_get_channel_name":
            channel_num = args["channel_num"]
            name_str = channels.getChannelName(channel_num)
            return f"Channel {channel_num} name: {name_str}"
        elif name == "channels_set_channel_volume":
            channel_num = args["channel_num"]
            volume = args["volume"]
            channels.setChannelVolume(channel_num, volume)
            return f"Channel {channel_num} volume set to: {volume}"
        elif name == "channels_mute_channel":
            channel_num = args["channel_num"]
            mute = args["mute"]
            channels.muteChannel(channel_num, mute)
            return f"Channel {channel_num} {'muted' if mute else 'unmuted'}"

        # FL Studio Pattern Tools
        elif name == "patterns_pattern_count":
            count = patterns.patternCount()
            return f"Total patterns: {count}"
        elif name == "patterns_get_pattern_name":
            pattern_num = args["pattern_num"]
            name_str = patterns.getPatternName(pattern_num)
            return f"Pattern {pattern_num} name: {name_str}"
        elif name == "patterns_set_pattern_name":
            pattern_num = args["pattern_num"]
            name_str = args["name"]
            patterns.setPatternName(pattern_num, name_str)
            return f"Pattern {pattern_num} name set to: {name_str}"

        # FL Studio General Tools
        elif name == "general_get_project_title":
            title = general.getProjectTitle()
            return f"Project title: {title}"
        elif name == "general_get_version":
            version = general.getVersion()
            return f"FL Studio version: {version}"

        # FL Studio UI Tools
        elif name == "ui_show_window":
            window_id = args["window_id"]
            ui.showWindow(window_id)
            return f"Showing window: {window_id}"

        # FL Studio Playlist Tools
        elif name == "playlist_get_track_name":
            track_num = args["track_num"]
            name_str = playlist.getTrackName(track_num)
            return f"Playlist track {track_num} name: {name_str}"

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
    server = FLStudioMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
