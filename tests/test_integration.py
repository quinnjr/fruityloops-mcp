"""Integration tests for the FL Studio MCP server."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from fruityloops_mcp.server import FLStudioMCPServer


@pytest.fixture
def mock_flapi_bridge():
    """Mock the Flapi bridge for testing."""
    with patch("fruityloops_mcp.server.get_bridge") as mock_get_bridge:
        mock_bridge = MagicMock()
        # Set up default return values for FL Studio methods
        mock_bridge.transport_start.return_value = "FL Studio playback started"
        mock_bridge.transport_stop.return_value = "FL Studio playback stopped"
        mock_bridge.transport_record.return_value = "FL Studio recording toggled"
        mock_bridge.mixer_set_track_name.return_value = "Track 0 name set to: Test"
        mock_bridge.mixer_set_track_volume.return_value = "Track 0 volume set to: 0.0"
        mock_get_bridge.return_value = mock_bridge
        yield mock_bridge


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
        mock_instance.port_name = "FLStudio_MIDI"
        yield mock_instance


class TestIntegration:
    """Integration tests for the server."""

    @pytest.mark.asyncio
    async def test_server_full_workflow(self, mock_flapi_bridge, mock_midi):
        """Test a complete workflow with FL Studio and MIDI."""
        server = FLStudioMCPServer()

        # Test MIDI connection
        result = await server._execute_tool("midi_connect", {})
        assert "Connected" in result
        mock_midi.connect.assert_called_once()

        # Test FL Studio transport via Flapi
        result = await server._execute_tool("transport_start", {})
        assert "started" in result
        mock_flapi_bridge.transport_start.assert_called_once()

        # Test sending MIDI note
        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await server._execute_tool("midi_send_note", {"note": 60})
            assert "Sent MIDI note" in result

        # Test MIDI disconnect
        result = await server._execute_tool("midi_disconnect", {})
        assert "Disconnected" in result
        mock_midi.disconnect.assert_called_once()

    @pytest.mark.asyncio
    async def test_multiple_tools_execution(self, mock_flapi_bridge, mock_midi):
        """Test executing multiple tools in sequence."""
        server = FLStudioMCPServer()

        # Execute multiple transport commands via Flapi
        await server._execute_tool("transport_start", {})
        await server._execute_tool("transport_stop", {})
        await server._execute_tool("transport_record", {})

        mock_flapi_bridge.transport_start.assert_called_once()
        mock_flapi_bridge.transport_stop.assert_called_once()
        mock_flapi_bridge.transport_record.assert_called_once()


class TestEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.mark.asyncio
    async def test_long_name(self, mock_flapi_bridge, mock_midi):
        """Test with very long names."""
        server = FLStudioMCPServer()
        long_name = "A" * 1000

        result = await server._execute_tool(
            "mixer_set_track_name", {"track_num": 0, "name": long_name}
        )
        assert "set to" in result
        mock_flapi_bridge.mixer_set_track_name.assert_called_once_with(0, long_name)

    @pytest.mark.asyncio
    async def test_zero_values(self, mock_flapi_bridge, mock_midi):
        """Test with zero values."""
        server = FLStudioMCPServer()

        result = await server._execute_tool(
            "mixer_set_track_volume", {"track_num": 0, "volume": 0.0}
        )
        assert "set to" in result
        mock_flapi_bridge.mixer_set_track_volume.assert_called_once_with(0, 0.0)
