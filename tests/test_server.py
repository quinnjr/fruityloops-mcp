"""Tests for the FL Studio MCP server."""

import pytest
from unittest.mock import Mock, patch, AsyncMock

from fruityloops_mcp.server import FLStudioMCPServer, FL_STUDIO_AVAILABLE


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
    async def test_call_tool_unknown_tool(self):
        """Test calling an unknown tool."""
        server = FLStudioMCPServer()
        result = await server.call_tool("unknown_tool", {})
        assert len(result) == 1
        assert "Error" in result[0].text or "Unknown tool" in result[0].text

    @pytest.mark.asyncio
    @patch("fruityloops_mcp.server.FL_STUDIO_AVAILABLE", False)
    async def test_fl_tools_unavailable(self):
        """Test that FL Studio tools report unavailability when FL not running."""
        server = FLStudioMCPServer()
        result = await server.call_tool("transport_start", {})
        assert "not available" in result[0].text or "cannot be executed" in result[0].text

