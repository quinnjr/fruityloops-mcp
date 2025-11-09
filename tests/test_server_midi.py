"""Tests for MIDI-related server tools."""

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from fruityloops_mcp.server import FLStudioMCPServer


@pytest.fixture
def mock_midi_interface():
    """Fixture to mock the MIDIInterface."""
    with patch("fruityloops_mcp.server.MIDIInterface") as MockMIDI:
        mock_instance = MockMIDI.return_value
        mock_instance.connect.return_value = True
        mock_instance.disconnect.return_value = None
        mock_instance.list_ports.return_value = {"input": ["MockIn"], "output": ["MockOut"]}
        mock_instance.send_note_on.return_value = True
        mock_instance.send_note_off.return_value = True
        mock_instance.send_control_change.return_value = True
        mock_instance.send_program_change.return_value = True
        mock_instance.send_pitch_bend.return_value = True
        mock_instance.port_name = "FLStudio_MIDI"
        yield mock_instance


@pytest.fixture
def server(mock_midi_interface):
    """Fixture for a server instance with mocked MIDI."""
    with patch("fruityloops_mcp.server.FL_STUDIO_AVAILABLE", True):
        return FLStudioMCPServer()


class TestServerMIDITools:
    """Test MIDI-related server tools."""

    @pytest.mark.asyncio
    async def test_midi_connect_success(self, server, mock_midi_interface):
        """Test midi_connect tool success."""
        result = await server._execute_tool("midi_connect", {})
        mock_midi_interface.connect.assert_called_once()
        assert "Connected to MIDI port" in result

    @pytest.mark.asyncio
    async def test_midi_connect_failure(self, server, mock_midi_interface):
        """Test midi_connect tool failure."""
        mock_midi_interface.connect.return_value = False
        result = await server._execute_tool("midi_connect", {})
        mock_midi_interface.connect.assert_called_once()
        assert "Failed to connect to MIDI port" in result

    @pytest.mark.asyncio
    async def test_midi_disconnect(self, server, mock_midi_interface):
        """Test midi_disconnect tool."""
        result = await server._execute_tool("midi_disconnect", {})
        mock_midi_interface.disconnect.assert_called_once()
        assert "Disconnected from MIDI port" in result

    @pytest.mark.asyncio
    async def test_midi_list_ports(self, server, mock_midi_interface):
        """Test midi_list_ports tool."""
        result = await server._execute_tool("midi_list_ports", {})
        mock_midi_interface.list_ports.assert_called_once()
        assert "Available MIDI ports" in result
        assert "MockIn" in result
        assert "MockOut" in result

    @pytest.mark.asyncio
    @patch("asyncio.sleep", new_callable=AsyncMock)
    async def test_midi_send_note(self, mock_sleep, server, mock_midi_interface):
        """Test midi_send_note tool."""
        args = {"note": 60, "velocity": 100, "duration": 0.1, "channel": 1}
        result = await server._execute_tool("midi_send_note", args)
        mock_midi_interface.send_note_on.assert_called_once_with(60, 100, 1)
        mock_sleep.assert_called_once_with(0.1)
        mock_midi_interface.send_note_off.assert_called_once_with(60, 100, 1)
        assert "Sent MIDI note 60" in result

    @pytest.mark.asyncio
    @patch("asyncio.sleep", new_callable=AsyncMock)
    async def test_midi_send_note_with_defaults(self, mock_sleep, server, mock_midi_interface):
        """Test midi_send_note tool with default values."""
        args = {"note": 60}
        result = await server._execute_tool("midi_send_note", args)
        mock_midi_interface.send_note_on.assert_called_once_with(60, 64, 0)
        mock_sleep.assert_called_once_with(0.5)
        mock_midi_interface.send_note_off.assert_called_once_with(60, 64, 0)
        assert "Sent MIDI note 60" in result

    @pytest.mark.asyncio
    async def test_midi_send_note_on(self, server, mock_midi_interface):
        """Test midi_send_note_on tool."""
        args = {"note": 60, "velocity": 100, "channel": 1}
        result = await server._execute_tool("midi_send_note_on", args)
        mock_midi_interface.send_note_on.assert_called_once_with(60, 100, 1)
        assert "Sent MIDI note_on" in result

    @pytest.mark.asyncio
    async def test_midi_send_note_on_failure(self, server, mock_midi_interface):
        """Test midi_send_note_on tool failure."""
        mock_midi_interface.send_note_on.return_value = False
        args = {"note": 60}
        result = await server._execute_tool("midi_send_note_on", args)
        assert "Failed to send MIDI note_on" in result

    @pytest.mark.asyncio
    async def test_midi_send_cc(self, server, mock_midi_interface):
        """Test midi_send_cc tool."""
        args = {"control": 7, "value": 100, "channel": 1}
        result = await server._execute_tool("midi_send_cc", args)
        mock_midi_interface.send_control_change.assert_called_once_with(7, 100, 1)
        assert "Sent MIDI CC" in result

    @pytest.mark.asyncio
    async def test_midi_tools_work_without_fl_studio(self, mock_midi_interface):
        """Test that MIDI tools can be executed even if FL Studio API is not available."""
        with patch("fruityloops_mcp.server.FL_STUDIO_AVAILABLE", False):
            server = FLStudioMCPServer()
            result = await server._execute_tool("midi_connect", {})
            assert "Connected to MIDI port" in result
            mock_midi_interface.connect.assert_called_once()


class TestServerMIDIEdgeCases:
    """Test edge cases for MIDI server tools."""

    @pytest.fixture
    def mock_midi_interface(self):
        """Fixture to mock the MIDIInterface."""
        with patch("fruityloops_mcp.server.MIDIInterface") as MockMIDI:
            mock_instance = MockMIDI.return_value
            mock_instance.connect.return_value = True
            mock_instance.disconnect.return_value = None
            mock_instance.list_ports.return_value = {"input": ["MockIn"], "output": ["MockOut"]}
            mock_instance.send_note_on.return_value = True
            mock_instance.send_note_off.return_value = True
            mock_instance.send_control_change.return_value = True
            mock_instance.send_program_change.return_value = True
            mock_instance.send_pitch_bend.return_value = True
            mock_instance.port_name = "FLStudio_MIDI"
            yield mock_instance

    @pytest.fixture
    def server(self, mock_midi_interface):
        """Fixture for a server instance with mocked MIDI."""
        with patch("fruityloops_mcp.server.FL_STUDIO_AVAILABLE", True):
            return FLStudioMCPServer()

    @pytest.mark.asyncio
    @patch("asyncio.sleep", new_callable=AsyncMock)
    async def test_midi_send_note_with_zero_duration(self, mock_sleep, server, mock_midi_interface):
        """Test midi_send_note with zero duration."""
        args = {"note": 60, "duration": 0}
        result = await server._execute_tool("midi_send_note", args)
        mock_midi_interface.send_note_on.assert_called_once_with(60, 64, 0)
        mock_sleep.assert_called_once_with(0)
        mock_midi_interface.send_note_off.assert_called_once_with(60, 64, 0)
        assert "Sent MIDI note" in result

    @pytest.mark.asyncio
    @patch("asyncio.sleep", new_callable=AsyncMock)
    async def test_midi_send_note_with_long_duration(self, mock_sleep, server, mock_midi_interface):
        """Test midi_send_note with a very long duration."""
        args = {"note": 60, "duration": 1000}
        result = await server._execute_tool("midi_send_note", args)
        mock_midi_interface.send_note_on.assert_called_once_with(60, 64, 0)
        mock_sleep.assert_called_once_with(1000)
        mock_midi_interface.send_note_off.assert_called_once_with(60, 64, 0)
        assert "Sent MIDI note" in result

    @pytest.mark.asyncio
    async def test_midi_port_name_in_server_init(self):
        """Test that the midi_port name is passed correctly to MIDIInterface."""
        custom_port_name = "MyCustomMIDI"
        with patch("fruityloops_mcp.server.MIDIInterface") as MockMIDI:
            mock_instance = MockMIDI.return_value
            mock_instance.port_name = custom_port_name
            FLStudioMCPServer(midi_port=custom_port_name)
            MockMIDI.assert_called_once_with(port_name=custom_port_name)

    @pytest.mark.asyncio
    async def test_concurrent_midi_operations(self, server, mock_midi_interface):
        """Test concurrent MIDI operations through the server."""
        tasks = [server._execute_tool("midi_send_note_on", {"note": 60 + i}) for i in range(10)]
        results = await asyncio.gather(*tasks)
        assert all("Sent MIDI note_on" in r for r in results)
        assert mock_midi_interface.send_note_on.call_count == 10
