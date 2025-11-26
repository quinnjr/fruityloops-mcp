"""Additional tests to boost code coverage to 90%+."""

import contextlib
from unittest.mock import MagicMock, Mock, patch

import pytest

from fruityloops_mcp.midi_interface import MIDIInterface
from fruityloops_mcp.server import FLStudioMCPServer


class TestMIDICoverageBoost:
    """Tests to cover MIDI interface error paths."""

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_connect_exception_during_open(self, mock_mido):
        """Test connection failure when opening ports raises exception."""
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_mido.open_output.side_effect = Exception("Failed to open output")

        midi = MIDIInterface()
        result = midi.connect()

        assert result is False
        assert not midi.is_connected

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_disconnect_when_not_connected(self, mock_mido):
        """Test disconnecting when not connected does nothing."""
        midi = MIDIInterface()
        # Should not raise, just return early
        midi.disconnect()
        assert not midi.is_connected

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_send_control_change(self, mock_mido):
        """Test sending control change messages."""
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_output = Mock()
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = Mock()

        midi = MIDIInterface()
        midi.connect()

        assert midi.send_control_change(7, 127, 0) is True
        mock_output.send.assert_called()

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_send_program_change(self, mock_mido):
        """Test sending program change messages."""
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_output = Mock()
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = Mock()

        midi = MIDIInterface()
        midi.connect()

        assert midi.send_program_change(10, 0) is True
        mock_output.send.assert_called()

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_send_pitch_bend(self, mock_mido):
        """Test sending pitch bend messages."""
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_output = Mock()
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = Mock()

        midi = MIDIInterface()
        midi.connect()

        assert midi.send_pitch_bend(1000, 0) is True
        mock_output.send.assert_called()

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_send_control_change_when_disconnected(self, mock_mido):
        """Test sending control change when not connected."""
        midi = MIDIInterface()
        assert midi.send_control_change(7, 127, 0) is False

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_send_program_change_when_disconnected(self, mock_mido):
        """Test sending program change when not connected."""
        midi = MIDIInterface()
        assert midi.send_program_change(10, 0) is False

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_send_pitch_bend_when_disconnected(self, mock_mido):
        """Test sending pitch bend when not connected."""
        midi = MIDIInterface()
        assert midi.send_pitch_bend(1000, 0) is False

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_disconnect_error_handling(self, mock_mido):
        """Test disconnect error handling."""
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_output = Mock()
        mock_output.close.side_effect = Exception("Close failed")
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = Mock()

        midi = MIDIInterface()
        midi.connect()
        # Disconnect with error should not raise, just log
        # and state remains connected since close failed
        midi.disconnect()
        assert midi.is_connected  # Remains connected after error

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_list_ports(self, mock_mido):
        """Test listing MIDI ports."""
        mock_mido.get_input_names.return_value = ["Input1", "Input2"]
        mock_mido.get_output_names.return_value = ["Output1", "Output2"]

        midi = MIDIInterface()
        ports = midi.list_ports()

        assert ports["input"] == ["Input1", "Input2"]
        assert ports["output"] == ["Output1", "Output2"]


@pytest.fixture
def mock_flapi_bridge():
    """Mock the Flapi bridge for testing."""
    with patch("fruityloops_mcp.server.get_bridge") as mock_get_bridge:
        mock_bridge = MagicMock()
        mock_get_bridge.return_value = mock_bridge
        yield mock_bridge


class TestServerCoverageBoost:
    """Tests to cover server tool execution paths."""

    @pytest.mark.asyncio
    @patch("fruityloops_mcp.server.MIDIInterface")
    async def test_execute_all_midi_tools(self, mock_midi_class, mock_flapi_bridge):
        """Test executing all MIDI tools to increase coverage."""
        mock_midi = mock_midi_class.return_value
        mock_midi.list_ports.return_value = {"input": ["test"], "output": ["test"]}
        mock_midi.connect.return_value = True
        mock_midi.send_note_on.return_value = True
        mock_midi.send_note_off.return_value = True
        mock_midi.send_control_change.return_value = True
        mock_midi.send_program_change.return_value = True
        mock_midi.send_pitch_bend.return_value = True

        server = FLStudioMCPServer()

        # Test all MIDI tools
        await server._execute_tool("midi_connect", {})
        await server._execute_tool("midi_disconnect", {})
        await server._execute_tool("midi_send_note_on", {"note": 60})
        await server._execute_tool("midi_send_note_off", {"note": 60})
        await server._execute_tool("midi_send_cc", {"control": 7, "value": 100})
        await server._execute_tool("midi_send_program_change", {"program": 10})
        await server._execute_tool("midi_send_pitch_bend", {"pitch": 1000})

    @pytest.mark.asyncio
    @patch("fruityloops_mcp.server.MIDIInterface")
    async def test_execute_failed_midi_operations(self, mock_midi_class, mock_flapi_bridge):
        """Test MIDI operations that fail."""
        mock_midi = mock_midi_class.return_value
        mock_midi.connect.return_value = False
        mock_midi.send_note_on.return_value = False
        mock_midi.send_note_off.return_value = False
        mock_midi.send_control_change.return_value = False
        mock_midi.send_program_change.return_value = False
        mock_midi.send_pitch_bend.return_value = False

        server = FLStudioMCPServer()

        # Test failed operations
        result = await server._execute_tool("midi_connect", {})
        assert "Failed" in result

        result = await server._execute_tool("midi_send_note_on", {"note": 60})
        assert "Failed" in result

        result = await server._execute_tool("midi_send_note_off", {"note": 60})
        assert "Failed" in result

        result = await server._execute_tool("midi_send_cc", {"control": 7, "value": 100})
        assert "Failed" in result

        result = await server._execute_tool("midi_send_program_change", {"program": 10})
        assert "Failed" in result

        result = await server._execute_tool("midi_send_pitch_bend", {"pitch": 1000})
        assert "Failed" in result


class TestServerMIDINoteHandler:
    """Test the async MIDI note handler."""

    @pytest.mark.asyncio
    @patch("fruityloops_mcp.server.MIDIInterface")
    @patch("fruityloops_mcp.server.asyncio.sleep")
    async def test_midi_send_note_success(self, mock_sleep, mock_midi_class, mock_flapi_bridge):
        """Test successful MIDI note send with duration."""
        mock_midi = mock_midi_class.return_value
        mock_midi.send_note_on.return_value = True
        mock_midi.send_note_off.return_value = True

        server = FLStudioMCPServer()
        result = await server._execute_tool(
            "midi_send_note", {"note": 60, "velocity": 100, "duration": 0.5, "channel": 1}
        )

        assert "Sent MIDI note 60" in result
        mock_sleep.assert_called_once_with(0.5)
        mock_midi.send_note_on.assert_called_once_with(60, 100, 1)
        mock_midi.send_note_off.assert_called_once_with(60, 100, 1)


class TestFlapiBridge:
    """Test the Flapi bridge module."""

    def test_flapi_bridge_creation(self):
        """Test creating a FLStudioBridge."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        bridge = FLStudioBridge()
        assert bridge is not None
        assert not bridge.is_enabled

    def test_flapi_bridge_properties(self):
        """Test FLStudioBridge properties."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        bridge = FLStudioBridge()
        # Check initial state
        assert bridge.is_enabled is False
        assert bridge.is_connected is False

    def test_get_bridge_singleton(self):
        """Test get_bridge returns same instance."""
        from fruityloops_mcp.flapi_bridge import get_bridge

        bridge1 = get_bridge()
        bridge2 = get_bridge()
        assert bridge1 is bridge2


class TestServerRunMethod:
    """Test the server run() method."""

    @pytest.mark.asyncio
    @patch("fruityloops_mcp.server.stdio_server")
    async def test_run_method_success(self, mock_stdio, mock_flapi_bridge):
        """Test successful run of the server."""
        mock_read = Mock()
        mock_write = Mock()
        mock_stdio.return_value.__aenter__.return_value = (mock_read, mock_write)
        mock_stdio.return_value.__aexit__.return_value = None

        server = FLStudioMCPServer()
        server.server.run = Mock(side_effect=KeyboardInterrupt())  # Exit gracefully

        with contextlib.suppress(KeyboardInterrupt):
            await server.run()

        mock_stdio.assert_called_once()

    @pytest.mark.asyncio
    @patch("fruityloops_mcp.server.stdio_server")
    async def test_run_method_exception_handling(self, mock_stdio, mock_flapi_bridge):
        """Test run() method handles exceptions."""
        mock_stdio.return_value.__aenter__.side_effect = Exception("Server error")

        server = FLStudioMCPServer()

        # Should log error but not raise
        await server.run()
        mock_stdio.assert_called_once()


class TestAdditionalMIDICoverage:
    """Additional tests to push coverage over 90%."""

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_send_note_on_with_defaults(self, mock_mido):
        """Test send_note_on with default values."""
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_output = Mock()
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = Mock()

        midi = MIDIInterface()
        midi.connect()

        # Test with all defaults
        midi.send_note_on(60)
        assert mock_output.send.called

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_send_note_off_with_defaults(self, mock_mido):
        """Test send_note_off with default values."""
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_output = Mock()
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = Mock()

        midi = MIDIInterface()
        midi.connect()

        # Test with all defaults
        midi.send_note_off(60)
        assert mock_output.send.called

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_output_port_not_found(self, mock_mido):
        """Test when output port is not found."""
        mock_mido.get_output_names.return_value = ["Other_Port"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]

        midi = MIDIInterface()
        result = midi.connect()

        # Should fail when output port not found
        assert result is False

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_input_port_not_found(self, mock_mido):
        """Test when input port is not found."""
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["Other_Port"]

        midi = MIDIInterface()
        result = midi.connect()

        # Should fail when input port not found
        assert result is False

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_send_note_on_generic_exception(self, mock_mido):
        """Test send_note_on with generic exception."""

        # Create a proper exception class for PortNotOpenError
        class MockPortNotOpenError(Exception):
            pass

        mock_mido.ports = Mock()
        mock_mido.ports.PortNotOpenError = MockPortNotOpenError
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_output = Mock()
        mock_output.send.side_effect = RuntimeError("Generic error")
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = Mock()

        midi = MIDIInterface()
        midi.connect()
        result = midi.send_note_on(60)

        assert result is False

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_send_note_off_generic_exception(self, mock_mido):
        """Test send_note_off with generic exception."""

        # Create a proper exception class for PortNotOpenError
        class MockPortNotOpenError(Exception):
            pass

        mock_mido.ports = Mock()
        mock_mido.ports.PortNotOpenError = MockPortNotOpenError
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_output = Mock()
        mock_output.send.side_effect = RuntimeError("Generic error")
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = Mock()

        midi = MIDIInterface()
        midi.connect()
        result = midi.send_note_off(60)

        assert result is False

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_send_control_change_exception(self, mock_mido):
        """Test send_control_change with exception."""
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_output = Mock()
        mock_output.send.side_effect = Exception("Generic error")
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = Mock()

        midi = MIDIInterface()
        midi.connect()
        result = midi.send_control_change(7, 100)

        assert result is False

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_send_program_change_exception(self, mock_mido):
        """Test send_program_change with exception."""
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_output = Mock()
        mock_output.send.side_effect = Exception("Generic error")
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = Mock()

        midi = MIDIInterface()
        midi.connect()
        result = midi.send_program_change(10)

        assert result is False

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_send_pitch_bend_exception(self, mock_mido):
        """Test send_pitch_bend with exception."""
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_output = Mock()
        mock_output.send.side_effect = Exception("Generic error")
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = Mock()

        midi = MIDIInterface()
        midi.connect()
        result = midi.send_pitch_bend(1000)

        assert result is False
