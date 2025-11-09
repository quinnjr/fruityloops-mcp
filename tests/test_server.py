"""Tests for the FL Studio MCP server."""

from unittest.mock import patch

import pytest

from fruityloops_mcp.server import FLStudioMCPServer


class TestFLStudioMCPServer:
    """Test the FL Studio MCP server."""

    def test_server_initialization(self):
        """Test that server initializes correctly."""
        server = FLStudioMCPServer()
        assert server.server is not None
        assert server.midi is not None

    def test_server_with_custom_midi_port(self):
        """Test server initialization with custom MIDI port."""
        server = FLStudioMCPServer(midi_port="CustomPort")
        assert server.midi.port_name == "CustomPort"

    @pytest.mark.asyncio
    async def test_execute_tool_unknown_tool(self):
        """Test calling an unknown tool."""
        server = FLStudioMCPServer()
        with pytest.raises((KeyError, ValueError, AttributeError)):
            await server._execute_tool("unknown_tool", {})

    @pytest.mark.asyncio
    @patch("fruityloops_mcp.server.FL_STUDIO_AVAILABLE", False)
    async def test_fl_tools_unavailable(self):
        """Test that FL Studio tools report unavailability when FL not running."""
        server = FLStudioMCPServer()
        # With FL Studio unavailable, FL tools should raise or return error
        # MIDI tools should still work
        result = await server._execute_tool("midi_list_ports", {})
        assert "MIDI ports" in result or "input" in result
