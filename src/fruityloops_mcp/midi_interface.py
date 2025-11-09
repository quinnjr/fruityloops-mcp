"""MIDI interface for FL Studio MCP server using mido library."""

import logging
from typing import Any

import mido

logger = logging.getLogger(__name__)


class MIDIInterface:
    """Interface for MIDI communication using mido library."""

    def __init__(self, port_name: str = "FLStudio_MIDI"):
        """Initialize MIDI interface.

        Args:
            port_name: Name of the MIDI port to connect to
        """
        self.port_name = port_name
        self._output_port: mido.ports.BaseOutput | None = None
        self._input_port: mido.ports.BaseInput | None = None
        self._is_connected = False

    @property
    def is_connected(self) -> bool:
        """Check if MIDI ports are connected."""
        return self._is_connected

    def connect(self) -> bool:
        """Connect to MIDI ports.

        Returns:
            True if connection successful, False otherwise
        """
        if self._is_connected:
            return True

        try:
            # Check if port exists in available ports
            output_ports = mido.get_output_names()
            input_ports = mido.get_input_names()

            if self.port_name not in output_ports:
                logger.warning(
                    f"Output port '{self.port_name}' not found. Available: {output_ports}"
                )
                return False

            if self.port_name not in input_ports:
                logger.warning(f"Input port '{self.port_name}' not found. Available: {input_ports}")
                return False

            # Open ports
            self._output_port = mido.open_output(self.port_name)
            self._input_port = mido.open_input(self.port_name)
            self._is_connected = True
            logger.info(f"Connected to MIDI port: {self.port_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to MIDI port: {e}")
            return False

    def disconnect(self) -> None:
        """Disconnect from MIDI ports."""
        if not self._is_connected:
            return

        try:
            if self._output_port:
                self._output_port.close()
                self._output_port = None

            if self._input_port:
                self._input_port.close()
                self._input_port = None

            self._is_connected = False
            logger.info(f"Disconnected from MIDI port: {self.port_name}")

        except Exception as e:
            logger.error(f"Error disconnecting from MIDI port: {e}")

    def send_note_on(self, note: int, velocity: int = 64, channel: int = 0) -> bool:
        """Send MIDI note on message.

        Args:
            note: MIDI note number (0-127)
            velocity: Note velocity (0-127)
            channel: MIDI channel (0-15)

        Returns:
            True if message sent successfully, False otherwise
        """
        if not self._is_connected or not self._output_port:
            logger.warning("Cannot send note_on: MIDI not connected")
            return False

        try:
            msg = mido.Message("note_on", note=note, velocity=velocity, channel=channel)
            self._output_port.send(msg)
            return True
        except mido.ports.PortNotOpenError:
            self._is_connected = False
            logger.error("MIDI port is not open")
            return False
        except Exception as e:
            logger.error(f"Error sending note_on: {e}")
            return False

    def send_note_off(self, note: int, velocity: int = 64, channel: int = 0) -> bool:
        """Send MIDI note off message.

        Args:
            note: MIDI note number (0-127)
            velocity: Note velocity (0-127)
            channel: MIDI channel (0-15)

        Returns:
            True if message sent successfully, False otherwise
        """
        if not self._is_connected or not self._output_port:
            logger.warning("Cannot send note_off: MIDI not connected")
            return False

        try:
            msg = mido.Message("note_off", note=note, velocity=velocity, channel=channel)
            self._output_port.send(msg)
            return True
        except mido.ports.PortNotOpenError:
            self._is_connected = False
            logger.error("MIDI port is not open")
            return False
        except Exception as e:
            logger.error(f"Error sending note_off: {e}")
            return False

    def send_control_change(self, control: int, value: int, channel: int = 0) -> bool:
        """Send MIDI control change message.

        Args:
            control: Control number (0-127)
            value: Control value (0-127)
            channel: MIDI channel (0-15)

        Returns:
            True if message sent successfully, False otherwise
        """
        if not self._is_connected or not self._output_port:
            logger.warning("Cannot send control_change: MIDI not connected")
            return False

        try:
            msg = mido.Message("control_change", control=control, value=value, channel=channel)
            self._output_port.send(msg)
            return True
        except Exception as e:
            logger.error(f"Error sending control_change: {e}")
            return False

    def send_program_change(self, program: int, channel: int = 0) -> bool:
        """Send MIDI program change message.

        Args:
            program: Program number (0-127)
            channel: MIDI channel (0-15)

        Returns:
            True if message sent successfully, False otherwise
        """
        if not self._is_connected or not self._output_port:
            logger.warning("Cannot send program_change: MIDI not connected")
            return False

        try:
            msg = mido.Message("program_change", program=program, channel=channel)
            self._output_port.send(msg)
            return True
        except Exception as e:
            logger.error(f"Error sending program_change: {e}")
            return False

    def send_pitch_bend(self, pitch: int, channel: int = 0) -> bool:
        """Send MIDI pitch bend message.

        Args:
            pitch: Pitch bend value (-8192 to 8191)
            channel: MIDI channel (0-15)

        Returns:
            True if message sent successfully, False otherwise
        """
        if not self._is_connected or not self._output_port:
            logger.warning("Cannot send pitch_bend: MIDI not connected")
            return False

        try:
            msg = mido.Message("pitchwheel", pitch=pitch, channel=channel)
            self._output_port.send(msg)
            return True
        except Exception as e:
            logger.error(f"Error sending pitch_bend: {e}")
            return False

    def list_ports(self) -> dict[str, list[str]]:
        """List available MIDI ports.

        Returns:
            Dictionary with 'input' and 'output' keys containing lists of port names
        """
        return {"input": mido.get_input_names(), "output": mido.get_output_names()}

    def __enter__(self) -> "MIDIInterface":
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.disconnect()
