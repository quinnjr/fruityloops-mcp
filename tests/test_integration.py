"""Integration tests for the FL Studio MCP server."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from fruityloops_mcp.server import FLStudioMCPServer


@pytest.fixture
def mock_fl_bridge():
    """Mock FL Studio Bridge client."""
    with patch("fruityloops_mcp.server.FLBridgeClient") as MockBridge:
        mock_bridge_instance = MagicMock()
        mock_bridge_instance.is_available.return_value = True
        # Setup transport methods
        mock_bridge_instance.transport_start.return_value = "Started"
        mock_bridge_instance.transport_stop.return_value = "Stopped"
        mock_bridge_instance.transport_record.return_value = "Recording toggled"
        # Setup mixer methods
        mock_bridge_instance.mixer_set_track_name.return_value = "Name set"
        mock_bridge_instance.mixer_set_track_volume.return_value = "Volume set"
        MockBridge.return_value = mock_bridge_instance
        yield mock_bridge_instance


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
    async def test_server_full_workflow(self, mock_fl_bridge, mock_midi):
        """Test a complete workflow with FL Studio and MIDI."""
        with patch("fruityloops_mcp.server.FL_STUDIO_AVAILABLE", True):
            server = FLStudioMCPServer()
            server.fl_bridge = mock_fl_bridge

            # Test MIDI connection
            result = await server._execute_tool("midi_connect", {})
            assert "Connected" in result
            mock_midi.connect.assert_called_once()

            # Test FL Studio transport
            result = await server._execute_tool("transport_start", {})
            assert "started" in result.lower()
            mock_fl_bridge.transport_start.assert_called_once()

            # Test sending MIDI note
            with patch("asyncio.sleep", new_callable=AsyncMock):
                result = await server._execute_tool("midi_send_note", {"note": 60})
                assert "Sent MIDI note" in result

            # Test MIDI disconnect
            result = await server._execute_tool("midi_disconnect", {})
            assert "Disconnected" in result
            mock_midi.disconnect.assert_called_once()

    @pytest.mark.asyncio
    async def test_multiple_tools_execution(self, mock_fl_bridge, mock_midi):
        """Test executing multiple tools in sequence."""
        with patch("fruityloops_mcp.server.FL_STUDIO_AVAILABLE", True):
            server = FLStudioMCPServer()
            server.fl_bridge = mock_fl_bridge

            # Execute multiple transport commands
            await server._execute_tool("transport_start", {})
            await server._execute_tool("transport_stop", {})
            await server._execute_tool("transport_record", {})

            mock_fl_bridge.transport_start.assert_called_once()
            mock_fl_bridge.transport_stop.assert_called_once()
            mock_fl_bridge.transport_record.assert_called_once()


class TestEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.mark.asyncio
    async def test_long_name(self, mock_fl_bridge, mock_midi):
        """Test with very long names."""
        with patch("fruityloops_mcp.server.FL_STUDIO_AVAILABLE", True):
            server = FLStudioMCPServer()
            server.fl_bridge = mock_fl_bridge
            long_name = "A" * 1000

            result = await server._execute_tool(
                "mixer_set_track_name", {"track_num": 0, "name": long_name}
            )
            assert "set to" in result.lower() or long_name in result
            mock_fl_bridge.mixer_set_track_name.assert_called_once_with(0, long_name)

    @pytest.mark.asyncio
    async def test_zero_values(self, mock_fl_bridge, mock_midi):
        """Test with zero values."""
        with patch("fruityloops_mcp.server.FL_STUDIO_AVAILABLE", True):
            server = FLStudioMCPServer()
            server.fl_bridge = mock_fl_bridge

            result = await server._execute_tool(
                "mixer_set_track_volume", {"track_num": 0, "volume": 0.0}
            )
            assert "set to" in result.lower() or "0.0" in result
            mock_fl_bridge.mixer_set_track_volume.assert_called_once_with(0, 0.0)
