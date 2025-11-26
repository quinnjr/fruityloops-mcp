"""Tests for the FL Studio MCP server."""

from unittest.mock import MagicMock, patch

import pytest

from fruityloops_mcp.server import FLStudioMCPServer


@pytest.fixture
def mock_flapi_bridge():
    """Mock the Flapi bridge for testing."""
    with patch("fruityloops_mcp.server.get_bridge") as mock_get_bridge:
        mock_bridge = MagicMock()
        mock_get_bridge.return_value = mock_bridge
        yield mock_bridge


class TestFLStudioMCPServer:
    """Test the FL Studio MCP server."""

    def test_server_initialization(self, mock_flapi_bridge):
        """Test that server initializes correctly."""
        server = FLStudioMCPServer()
        assert server.server is not None
        assert server.midi is not None
        assert server.flapi_bridge is not None

    def test_server_with_custom_midi_port(self, mock_flapi_bridge):
        """Test server initialization with custom MIDI port."""
        server = FLStudioMCPServer(midi_port="CustomPort")
        assert server.midi.port_name == "CustomPort"

    @pytest.mark.asyncio
    async def test_execute_tool_unknown_tool(self, mock_flapi_bridge):
        """Test calling an unknown tool."""
        server = FLStudioMCPServer()
        with pytest.raises((KeyError, ValueError, AttributeError)):
            await server._execute_tool("unknown_tool", {})

    @pytest.mark.asyncio
    @patch("fruityloops_mcp.server.MIDIInterface")
    async def test_midi_tools_always_available(self, mock_midi_class, mock_flapi_bridge):
        """Test that MIDI tools work regardless of Flapi status."""
        mock_midi = mock_midi_class.return_value
        mock_midi.list_ports.return_value = {"input": [], "output": []}

        server = FLStudioMCPServer()
        result = await server._execute_tool("midi_list_ports", {})
        assert "MIDI ports" in result or "input" in result
