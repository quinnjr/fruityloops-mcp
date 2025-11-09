"""Integration tests for the FL Studio MCP server."""

from unittest.mock import AsyncMock, patch

import pytest

from fruityloops_mcp.server import FLStudioMCPServer


@pytest.fixture
def mock_fl_modules():
    """Mock FL Studio API modules."""
    with (
        patch("fruityloops_mcp.server.transport") as mock_transport,
        patch("fruityloops_mcp.server.mixer") as mock_mixer,
        patch("fruityloops_mcp.server.channels") as mock_channels,
        patch("fruityloops_mcp.server.patterns") as mock_patterns,
        patch("fruityloops_mcp.server.general") as mock_general,
        patch("fruityloops_mcp.server.ui") as mock_ui,
        patch("fruityloops_mcp.server.playlist") as mock_playlist,
        patch("fruityloops_mcp.server.FL_STUDIO_AVAILABLE", True),
    ):
        yield {
            "transport": mock_transport,
            "mixer": mock_mixer,
            "channels": mock_channels,
            "patterns": mock_patterns,
            "general": mock_general,
            "ui": mock_ui,
            "playlist": mock_playlist,
        }


@pytest.fixture
def mock_midi():
    """Mock MIDI interface."""
    with patch("fruityloops_mcp.server.MIDIInterface") as MockMIDI:
        mock_instance = MockMIDI.return_value
        mock_instance.connect.return_value = True
        mock_instance.disconnect.return_value = None
        mock_instance.send_note_on.return_value = True
        mock_instance.send_note_off.return_value = True
        mock_instance.list_ports.return_value = {"input": [], "output": []}
        yield mock_instance


class TestIntegration:
    """Integration tests for the server."""

    @pytest.mark.asyncio
    async def test_server_full_workflow(self, mock_fl_modules, mock_midi):
        """Test a complete workflow with FL Studio and MIDI."""
        server = FLStudioMCPServer()

        # Test MIDI connection
        result = await server._execute_tool("midi_connect", {})
        assert "Connected" in result
        mock_midi.connect.assert_called_once()

        # Test FL Studio transport
        result = await server._execute_tool("transport_start", {})
        assert "started" in result
        mock_fl_modules["transport"].start.assert_called_once()

        # Test sending MIDI note
        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await server._execute_tool("midi_send_note", {"note": 60})
            assert "Sent MIDI note" in result

        # Test MIDI disconnect
        result = await server._execute_tool("midi_disconnect", {})
        assert "Disconnected" in result
        mock_midi.disconnect.assert_called_once()

    @pytest.mark.asyncio
    async def test_multiple_tools_execution(self, mock_fl_modules, mock_midi):
        """Test executing multiple tools in sequence."""
        server = FLStudioMCPServer()

        # Execute multiple transport commands
        await server._execute_tool("transport_start", {})
        await server._execute_tool("transport_stop", {})
        await server._execute_tool("transport_record", {})

        mock_fl_modules["transport"].start.assert_called_once()
        mock_fl_modules["transport"].stop.assert_called_once()
        mock_fl_modules["transport"].record.assert_called_once()


class TestEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.mark.asyncio
    async def test_long_name(self, mock_fl_modules, mock_midi):
        """Test with very long names."""
        server = FLStudioMCPServer()
        long_name = "A" * 1000

        result = await server._execute_tool(
            "mixer_set_track_name", {"track_num": 0, "name": long_name}
        )
        assert "set to" in result
        mock_fl_modules["mixer"].setTrackName.assert_called_once_with(0, long_name)

    @pytest.mark.asyncio
    async def test_zero_values(self, mock_fl_modules, mock_midi):
        """Test with zero values."""
        server = FLStudioMCPServer()

        result = await server._execute_tool(
            "mixer_set_track_volume", {"track_num": 0, "volume": 0.0}
        )
        assert "set to" in result
        mock_fl_modules["mixer"].setTrackVolume.assert_called_once_with(0, 0.0)
