"""FL Studio MCP Server - Model Context Protocol server for FL Studio via Flapi.

This package provides an MCP server that enables AI assistants to control FL Studio
through:
- Flapi: A bridge to FL Studio's internal Python API via MIDI
- Direct MIDI: For sending notes, CC, and other MIDI messages
"""

from fruityloops_mcp.flapi_bridge import FLStudioBridge, get_bridge
from fruityloops_mcp.midi_interface import MIDIInterface
from fruityloops_mcp.server import FLStudioMCPServer, main

__version__ = "1.1.0"

__all__ = [
    "FLStudioMCPServer",
    "FLStudioBridge",
    "MIDIInterface",
    "get_bridge",
    "main",
]
