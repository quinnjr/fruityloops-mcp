"""Edge case and antipattern tests for MIDI interface."""

import asyncio
from unittest.mock import MagicMock, Mock, patch

import pytest

from fruityloops_mcp.midi_interface import MIDIInterface


class TestMIDIEdgeCases:
    """Test edge cases for MIDI interface."""

    @pytest.fixture
    def midi(self):
        """Create MIDI interface instance."""
        return MIDIInterface(port_name="FLStudio_MIDI")

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_double_connect(self, mock_mido, midi):
        """Test calling connect multiple times."""
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_mido.open_output.return_value = Mock()
        mock_mido.open_input.return_value = Mock()

        assert midi.connect() is True
        assert midi.connect() is True  # Second call should also return True
        mock_mido.open_output.assert_called_once()  # Should only open once

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_double_disconnect(self, mock_mido, midi):
        """Test calling disconnect multiple times."""
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_output = Mock()
        mock_input = Mock()
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = mock_input

        midi.connect()
        midi.disconnect()
        midi.disconnect()  # Second call should not error
        mock_output.close.assert_called_once()  # Should only close once

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_send_note_off_exception(self, mock_mido, midi):
        """Test send_note_off when an exception occurs during send."""

        # Create a mock PortNotOpenError exception class
        class MockPortNotOpenError(Exception):
            pass

        # Set up mock BEFORE calling connect
        mock_mido.ports = Mock()
        mock_mido.ports.PortNotOpenError = MockPortNotOpenError
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_output = Mock()
        mock_output.send.side_effect = Exception("Send error")
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = Mock()

        midi.connect()
        assert midi.send_note_off(60) is False

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_context_manager_exception_on_connect(self, mock_mido, midi):
        """Test context manager when connect has issues."""
        mock_mido.get_output_names.return_value = ["OtherPort"]  # Port not found
        mock_mido.get_input_names.return_value = ["OtherPort"]

        with midi as m:
            # Should still work but not be connected
            assert not m.is_connected

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_context_manager_exception_on_disconnect(self, mock_mido, midi):
        """Test context manager when disconnect has issues."""
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_output = Mock()
        mock_output.close.side_effect = Exception("Close error")
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = Mock()

        # Disconnect errors are logged but don't propagate in context manager
        with midi as m:
            assert m.is_connected
        # When close() raises an exception, is_connected remains True
        # because the flag is set AFTER the close operations
        assert midi.is_connected

    def test_send_operations_with_none_port(self, midi):
        """Test send operations when port is None."""
        midi._is_connected = True
        midi._output_port = None  # Manually set to None

        assert midi.send_note_on(60) is False
        assert midi.send_note_off(60) is False
        assert midi.send_control_change(7, 100) is False
        assert midi.send_program_change(0) is False
        assert midi.send_pitch_bend(0) is False


class TestMIDIAntipatterns:
    """Test antipatterns and misuse."""

    @pytest.fixture
    def midi(self):
        """Create MIDI interface instance."""
        return MIDIInterface(port_name="FLStudio_MIDI")

    def test_send_before_connect(self, midi):
        """Antipattern: Sending MIDI messages before connecting."""
        assert not midi.is_connected
        assert midi.send_note_on(60) is False
        assert midi.send_note_off(60) is False
        assert midi.send_control_change(7, 100) is False

    @pytest.mark.parametrize(
        "note, velocity, channel, pitch",
        [
            (128, 128, 16, 8192),  # Out of range high
            (-1, -1, -1, -8193),  # Out of range low
        ],
    )
    @patch("fruityloops_mcp.midi_interface.mido")
    def test_extreme_values(self, mock_mido, midi, note, velocity, channel, pitch):
        """Antipattern: Sending extreme out-of-range values."""
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_mido.open_output.return_value = Mock()
        mock_mido.open_input.return_value = Mock()

        midi.connect()
        # mido itself handles value clamping, so these should still return True
        assert midi.send_note_on(note, velocity, channel) is True
        assert midi.send_note_off(note, velocity, channel) is True
        assert midi.send_control_change(note, velocity, channel) is True
        assert midi.send_program_change(note, channel) is True
        assert midi.send_pitch_bend(pitch, channel) is True

    @pytest.mark.asyncio
    @patch("fruityloops_mcp.midi_interface.mido")
    async def test_concurrent_sends(self, mock_mido, midi):
        """Antipattern: Sending many messages concurrently."""
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_output = Mock()
        mock_output.send = MagicMock()
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = Mock()

        midi.connect()

        tasks = [
            asyncio.create_task(asyncio.to_thread(midi.send_note_on, 60 + i)) for i in range(100)
        ]
        results = await asyncio.gather(*tasks)

        assert all(results)
        assert mock_output.send.call_count == 100

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_port_disconnected_during_send(self, mock_mido, midi):
        """Edge case: Port becomes disconnected between is_connected check and send."""

        # Create a mock PortNotOpenError exception class
        class MockPortNotOpenError(Exception):
            pass

        # Set up mock BEFORE calling connect
        mock_mido.ports = Mock()
        mock_mido.ports.PortNotOpenError = MockPortNotOpenError
        mock_mido.get_output_names.return_value = ["FLStudio_MIDI"]
        mock_mido.get_input_names.return_value = ["FLStudio_MIDI"]
        mock_output = Mock()
        mock_output.send.side_effect = MockPortNotOpenError("Port closed")
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = Mock()

        midi.connect()
        assert midi.send_note_on(60) is False
        assert not midi.is_connected  # Should reflect the disconnected state


class TestMIDIBoundaryConditions:
    """Test boundary conditions."""

    @pytest.fixture
    def midi(self):
        """Create MIDI interface instance with mocked connection."""
        midi_instance = MIDIInterface(port_name="FLStudio_MIDI")
        midi_instance._output_port = Mock()
        midi_instance._is_connected = True
        return midi_instance

    @pytest.mark.parametrize("note", [0, 64, 127])
    def test_note_boundary_values(self, midi, note):
        """Test note_on/off with boundary values."""
        assert midi.send_note_on(note) is True
        assert midi.send_note_off(note) is True

    @pytest.mark.parametrize("velocity", [0, 1, 127])
    def test_velocity_boundary_values(self, midi, velocity):
        """Test velocity with boundary values."""
        assert midi.send_note_on(60, velocity) is True
        assert midi.send_note_off(60, velocity) is True

    @pytest.mark.parametrize("channel", [0, 15])
    def test_channel_boundary_values(self, midi, channel):
        """Test channel with boundary values."""
        assert midi.send_note_on(60, 64, channel) is True
        assert midi.send_control_change(7, 100, channel) is True
        assert midi.send_program_change(0, channel) is True
        assert midi.send_pitch_bend(0, channel) is True
