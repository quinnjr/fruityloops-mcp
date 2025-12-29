"""Client for communicating with FL Studio Bridge."""

import contextlib
import json
import logging
import socket

logger = logging.getLogger(__name__)


class FLBridgeClient:
    """Client for communicating with the FL Studio Bridge script."""

    def __init__(self, host: str = "127.0.0.1", port: int = 25100):
        """Initialize the bridge client.

        Args:
            host: Host address of the FL Studio Bridge
            port: Port number of the FL Studio Bridge
        """
        self.host = host
        self.port = port
        self.socket: socket.socket | None = None
        self.connected = False

    def connect(self) -> bool:
        """Connect to the FL Studio Bridge.

        Returns:
            True if connection successful, False otherwise
        """
        if self.connected:
            return True

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0)
            self.socket.connect((self.host, self.port))
            self.connected = True
            logger.info(f"Connected to FL Studio Bridge at {self.host}:{self.port}")

            # Test connection with ping
            result = self.send_command("ping")
            if result and result.get("success"):
                logger.info("FL Studio Bridge connection verified")
                return True
            else:
                logger.warning("FL Studio Bridge connection test failed")
                self.disconnect()
                return False

        except (TimeoutError, OSError) as e:
            logger.warning(f"Failed to connect to FL Studio Bridge: {e}")
            self.connected = False
            if self.socket:
                with contextlib.suppress(Exception):
                    self.socket.close()
                self.socket = None
            return False

    def disconnect(self):
        """Disconnect from the FL Studio Bridge."""
        if self.socket:
            with contextlib.suppress(Exception):
                self.socket.close()
            self.socket = None
        self.connected = False
        logger.info("Disconnected from FL Studio Bridge")

    def send_command(self, action: str, params: dict = None) -> dict | None:
        """Send a command to the FL Studio Bridge.

        Args:
            action: The action to perform
            params: Parameters for the action

        Returns:
            Response dict from the bridge, or None if failed
        """
        if not self.connected and not self.connect():
            return None

        command = {"action": action, "params": params or {}}

        try:
            # Send command
            message = json.dumps(command).encode("utf-8")
            self.socket.sendall(message)

            # Receive response
            data = self.socket.recv(4096)
            if not data:
                logger.warning("FL Studio Bridge closed connection")
                self.disconnect()
                return None

            response = json.loads(data.decode("utf-8"))
            return response

        except (TimeoutError, OSError, json.JSONDecodeError) as e:
            logger.error(f"FL Studio Bridge communication error: {e}")
            self.disconnect()
            return None

    def is_available(self) -> bool:
        """Check if FL Studio Bridge is available.

        Returns:
            True if bridge is connected and responding
        """
        if not self.connected:
            return self.connect()
        return True

    # Transport methods
    def transport_start(self) -> str | None:
        """Start FL Studio playback."""
        result = self.send_command("transport.start")
        return result.get("result") if result and result.get("success") else None

    def transport_stop(self) -> str | None:
        """Stop FL Studio playback."""
        result = self.send_command("transport.stop")
        return result.get("result") if result and result.get("success") else None

    def transport_record(self) -> str | None:
        """Toggle recording in FL Studio."""
        result = self.send_command("transport.record")
        return result.get("result") if result and result.get("success") else None

    def transport_get_song_pos(self) -> int | None:
        """Get current song position."""
        result = self.send_command("transport.getSongPos")
        return result.get("result") if result and result.get("success") else None

    def transport_set_song_pos(self, position: int) -> str | None:
        """Set song position."""
        result = self.send_command("transport.setSongPos", {"position": position})
        return result.get("result") if result and result.get("success") else None

    # Mixer methods
    def mixer_get_track_volume(self, track: int) -> float | None:
        """Get mixer track volume."""
        result = self.send_command("mixer.getTrackVolume", {"track": track})
        return result.get("result") if result and result.get("success") else None

    def mixer_set_track_volume(self, track: int, volume: float) -> str | None:
        """Set mixer track volume."""
        result = self.send_command("mixer.setTrackVolume", {"track": track, "volume": volume})
        return result.get("result") if result and result.get("success") else None

    def mixer_get_track_name(self, track: int) -> str | None:
        """Get mixer track name."""
        result = self.send_command("mixer.getTrackName", {"track": track})
        return result.get("result") if result and result.get("success") else None

    def mixer_set_track_name(self, track: int, name: str) -> str | None:
        """Set mixer track name."""
        result = self.send_command("mixer.setTrackName", {"track": track, "name": name})
        return result.get("result") if result and result.get("success") else None

    # Channels methods
    def channels_channel_count(self) -> int | None:
        """Get total number of channels."""
        result = self.send_command("channels.channelCount")
        return result.get("result") if result and result.get("success") else None

    def channels_get_channel_name(self, channel: int) -> str | None:
        """Get channel name."""
        result = self.send_command("channels.getChannelName", {"channel": channel})
        return result.get("result") if result and result.get("success") else None

    def channels_set_channel_volume(self, channel: int, volume: float) -> str | None:
        """Set channel volume."""
        result = self.send_command(
            "channels.setChannelVolume", {"channel": channel, "volume": volume}
        )
        return result.get("result") if result and result.get("success") else None

    def channels_mute_channel(self, channel: int, mute: bool) -> str | None:
        """Mute or unmute a channel."""
        result = self.send_command(
            "channels.muteChannel", {"channel": channel, "mute": 1 if mute else 0}
        )
        return result.get("result") if result and result.get("success") else None

    # Patterns methods
    def patterns_pattern_count(self) -> int | None:
        """Get total number of patterns."""
        result = self.send_command("patterns.patternCount")
        return result.get("result") if result and result.get("success") else None

    def patterns_get_pattern_name(self, pattern: int) -> str | None:
        """Get pattern name."""
        result = self.send_command("patterns.getPatternName", {"pattern": pattern})
        return result.get("result") if result and result.get("success") else None

    def patterns_set_pattern_name(self, pattern: int, name: str) -> str | None:
        """Set pattern name."""
        result = self.send_command("patterns.setPatternName", {"pattern": pattern, "name": name})
        return result.get("result") if result and result.get("success") else None

    # General methods
    def general_get_version(self) -> int | None:
        """Get FL Studio version."""
        result = self.send_command("general.getVersion")
        return result.get("result") if result and result.get("success") else None

    def general_get_project_title(self) -> str | None:
        """Get project title."""
        result = self.send_command("general.getProjectTitle")
        return result.get("result") if result and result.get("success") else None

    # UI methods
    def ui_show_window(self, window: int) -> str | None:
        """Show a specific FL Studio window."""
        result = self.send_command("ui.showWindow", {"window": window})
        return result.get("result") if result and result.get("success") else None

    # Playlist methods
    def playlist_get_track_name(self, track: int) -> str | None:
        """Get playlist track name."""
        result = self.send_command("playlist.getTrackName", {"track": track})
        return result.get("result") if result and result.get("success") else None
