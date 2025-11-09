"""Tests for the MIDI interface."""

import pytest
from unittest.mock import Mock, patch

from fruityloops_mcp.midi_interface import MIDIInterface


class TestMIDIInterface:
    """Test the MIDI interface."""

    def test_midi_initialization(self):
        """Test MIDI interface initializes correctly."""
        midi = MIDIInterface(port_name="TestPort")
        assert midi.port_name == "TestPort"
        assert not midi.is_connected

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_connect_success(self, mock_mido):
        """Test successful MIDI connection."""
        mock_mido.get_output_names.return_value = ["TestPort"]
        mock_mido.get_input_names.return_value = ["TestPort"]
        mock_mido.open_output.return_value = Mock()
        mock_mido.open_input.return_value = Mock()

        midi = MIDIInterface(port_name="TestPort")
        assert midi.connect() is True
        assert midi.is_connected

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_connect_port_not_found(self, mock_mido):
        """Test connection fails when port not found."""
        mock_mido.get_output_names.return_value = ["OtherPort"]
        mock_mido.get_input_names.return_value = ["OtherPort"]

        midi = MIDIInterface(port_name="TestPort")
        assert midi.connect() is False
        assert not midi.is_connected

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_disconnect(self, mock_mido):
        """Test MIDI disconnection."""
        mock_mido.get_output_names.return_value = ["TestPort"]
        mock_mido.get_input_names.return_value = ["TestPort"]
        mock_output = Mock()
        mock_input = Mock()
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = mock_input

        midi = MIDIInterface(port_name="TestPort")
        midi.connect()
        midi.disconnect()

        mock_output.close.assert_called_once()
        mock_input.close.assert_called_once()
        assert not midi.is_connected

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_send_note_on(self, mock_mido):
        """Test sending note on message."""
        mock_mido.get_output_names.return_value = ["TestPort"]
        mock_mido.get_input_names.return_value = ["TestPort"]
        mock_output = Mock()
        mock_mido.open_output.return_value = mock_output
        mock_mido.open_input.return_value = Mock()

        midi = MIDIInterface(port_name="TestPort")
        midi.connect()
        result = midi.send_note_on(60, 100, 0)

        assert result is True
        mock_output.send.assert_called_once()

    def test_send_note_on_not_connected(self):
        """Test sending note on when not connected."""
        midi = MIDIInterface(port_name="TestPort")
        result = midi.send_note_on(60)
        assert result is False

    @patch("fruityloops_mcp.midi_interface.mido")
    def test_list_ports(self, mock_mido):
        """Test listing available ports."""
        mock_mido.get_input_names.return_value = ["Input1", "Input2"]
        mock_mido.get_output_names.return_value = ["Output1", "Output2"]

        midi = MIDIInterface()
        ports = midi.list_ports()

        assert ports["input"] == ["Input1", "Input2"]
        assert ports["output"] == ["Output1", "Output2"]

