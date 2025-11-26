"""Flapi bridge for FL Studio communication.

This module provides a bridge between the external MCP server and FL Studio's
internal Python environment using Flapi. Flapi uses virtual MIDI ports to
communicate with FL Studio, allowing external Python code to execute FL Studio
API functions.

Setup Requirements:
1. Install loopMIDI (Windows) and create ports "Flapi Request" and "Flapi Response"
2. Run `flapi install` to install the Flapi server script into FL Studio
3. Configure FL Studio MIDI settings to use the Flapi ports
4. Restart FL Studio with the Flapi script enabled
"""

import logging
from contextlib import contextmanager
from typing import Any, Generator

logger = logging.getLogger(__name__)

# Track Flapi availability and state
_flapi_available = False
_flapi_enabled = False

try:
    import flapi

    _flapi_available = True
except ImportError:
    logger.warning("Flapi not available. FL Studio API features will be disabled.")
    flapi = None


class FLStudioBridge:
    """Bridge for communicating with FL Studio via Flapi.

    This class manages the Flapi connection and provides methods to execute
    FL Studio API calls through the Flapi bridge.
    """

    def __init__(self) -> None:
        """Initialize the FL Studio bridge."""
        self._enabled = False
        self._connected = False

    @property
    def is_available(self) -> bool:
        """Check if Flapi library is available."""
        return _flapi_available

    @property
    def is_enabled(self) -> bool:
        """Check if Flapi is currently enabled."""
        return self._enabled

    @property
    def is_connected(self) -> bool:
        """Check if connected to FL Studio via Flapi."""
        return self._connected

    def enable(self) -> bool:
        """Enable Flapi connection to FL Studio.

        This must be called before any FL Studio API calls can be made.
        Flapi modifies the FL Studio API stubs to forward calls to FL Studio
        via MIDI.

        Returns:
            True if Flapi was enabled successfully, False otherwise.
        """
        if not _flapi_available:
            logger.error("Cannot enable Flapi: library not installed")
            return False

        if self._enabled:
            logger.debug("Flapi already enabled")
            return True

        try:
            flapi.enable()
            self._enabled = True
            self._connected = True
            logger.info("Flapi enabled - FL Studio API calls will be forwarded to FL Studio")
            return True
        except Exception as e:
            logger.error(f"Failed to enable Flapi: {e}")
            self._enabled = False
            self._connected = False
            return False

    def disable(self) -> None:
        """Disable Flapi connection.

        After calling this, FL Studio API calls will no longer be forwarded
        to FL Studio.
        """
        if not _flapi_available:
            return

        if not self._enabled:
            return

        try:
            flapi.disable()
            self._enabled = False
            self._connected = False
            logger.info("Flapi disabled")
        except Exception as e:
            logger.error(f"Error disabling Flapi: {e}")

    def test_connection(self) -> bool:
        """Test if the connection to FL Studio is working.

        Returns:
            True if connected and able to communicate with FL Studio.
        """
        if not self._enabled:
            return False

        try:
            # Try to get FL Studio version as a connection test
            import general

            version = general.getVersion()
            logger.info(f"Connected to FL Studio version: {version}")
            return True
        except Exception as e:
            logger.warning(f"FL Studio connection test failed: {e}")
            self._connected = False
            return False

    @contextmanager
    def connection(self) -> Generator["FLStudioBridge", None, None]:
        """Context manager for Flapi connection.

        Usage:
            with bridge.connection() as bridge:
                # FL Studio API calls here
                pass

        Yields:
            The FLStudioBridge instance.
        """
        try:
            self.enable()
            yield self
        finally:
            self.disable()

    # =========================================================================
    # Transport Controls
    # =========================================================================

    def transport_start(self) -> str:
        """Start FL Studio playback."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import transport

            transport.start()
            return "FL Studio playback started"
        except Exception as e:
            return f"Error starting playback: {e}"

    def transport_stop(self) -> str:
        """Stop FL Studio playback."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import transport

            transport.stop()
            return "FL Studio playback stopped"
        except Exception as e:
            return f"Error stopping playback: {e}"

    def transport_record(self) -> str:
        """Toggle FL Studio recording."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import transport

            transport.record()
            return "FL Studio recording toggled"
        except Exception as e:
            return f"Error toggling recording: {e}"

    def transport_get_song_pos(self) -> str:
        """Get current song position."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import transport

            pos = transport.getSongPos()
            return f"Current song position: {pos}"
        except Exception as e:
            return f"Error getting song position: {e}"

    def transport_set_song_pos(self, position: int) -> str:
        """Set song position."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import transport

            transport.setSongPos(position)
            return f"Song position set to: {position}"
        except Exception as e:
            return f"Error setting song position: {e}"

    def transport_get_bpm(self) -> str:
        """Get current tempo (BPM)."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import transport

            bpm = transport.getTempo()
            return f"Current tempo: {bpm} BPM"
        except Exception as e:
            return f"Error getting tempo: {e}"

    def transport_set_bpm(self, bpm: float) -> str:
        """Set tempo (BPM)."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import transport

            transport.setTempo(bpm)
            return f"Tempo set to: {bpm} BPM"
        except Exception as e:
            return f"Error setting tempo: {e}"

    # =========================================================================
    # Mixer Controls
    # =========================================================================

    def mixer_get_track_volume(self, track_num: int) -> str:
        """Get mixer track volume."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import mixer

            volume = mixer.getTrackVolume(track_num)
            return f"Track {track_num} volume: {volume}"
        except Exception as e:
            return f"Error getting track volume: {e}"

    def mixer_set_track_volume(self, track_num: int, volume: float) -> str:
        """Set mixer track volume."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import mixer

            mixer.setTrackVolume(track_num, volume)
            return f"Track {track_num} volume set to: {volume}"
        except Exception as e:
            return f"Error setting track volume: {e}"

    def mixer_get_track_name(self, track_num: int) -> str:
        """Get mixer track name."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import mixer

            name = mixer.getTrackName(track_num)
            return f"Track {track_num} name: {name}"
        except Exception as e:
            return f"Error getting track name: {e}"

    def mixer_set_track_name(self, track_num: int, name: str) -> str:
        """Set mixer track name."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import mixer

            mixer.setTrackName(track_num, name)
            return f"Track {track_num} name set to: {name}"
        except Exception as e:
            return f"Error setting track name: {e}"

    def mixer_get_track_pan(self, track_num: int) -> str:
        """Get mixer track pan."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import mixer

            pan = mixer.getTrackPan(track_num)
            return f"Track {track_num} pan: {pan}"
        except Exception as e:
            return f"Error getting track pan: {e}"

    def mixer_set_track_pan(self, track_num: int, pan: float) -> str:
        """Set mixer track pan."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import mixer

            mixer.setTrackPan(track_num, pan)
            return f"Track {track_num} pan set to: {pan}"
        except Exception as e:
            return f"Error setting track pan: {e}"

    def mixer_mute_track(self, track_num: int, mute: bool) -> str:
        """Mute or unmute a mixer track."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import mixer

            mixer.muteTrack(track_num, int(mute))
            return f"Track {track_num} {'muted' if mute else 'unmuted'}"
        except Exception as e:
            return f"Error muting track: {e}"

    def mixer_solo_track(self, track_num: int, solo: bool) -> str:
        """Solo or unsolo a mixer track."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import mixer

            mixer.soloTrack(track_num, int(solo))
            return f"Track {track_num} {'soloed' if solo else 'unsoloed'}"
        except Exception as e:
            return f"Error soloing track: {e}"

    # =========================================================================
    # Channel Controls
    # =========================================================================

    def channels_count(self) -> str:
        """Get total number of channels."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import channels

            count = channels.channelCount()
            return f"Total channels: {count}"
        except Exception as e:
            return f"Error getting channel count: {e}"

    def channels_get_name(self, channel_num: int) -> str:
        """Get channel name."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import channels

            name = channels.getChannelName(channel_num)
            return f"Channel {channel_num} name: {name}"
        except Exception as e:
            return f"Error getting channel name: {e}"

    def channels_set_volume(self, channel_num: int, volume: float) -> str:
        """Set channel volume."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import channels

            channels.setChannelVolume(channel_num, volume)
            return f"Channel {channel_num} volume set to: {volume}"
        except Exception as e:
            return f"Error setting channel volume: {e}"

    def channels_mute(self, channel_num: int, mute: bool) -> str:
        """Mute or unmute a channel."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import channels

            channels.muteChannel(channel_num, int(mute))
            return f"Channel {channel_num} {'muted' if mute else 'unmuted'}"
        except Exception as e:
            return f"Error muting channel: {e}"

    def channels_get_color(self, channel_num: int) -> str:
        """Get channel color."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import channels

            color = channels.getChannelColor(channel_num)
            return f"Channel {channel_num} color: {color}"
        except Exception as e:
            return f"Error getting channel color: {e}"

    def channels_set_color(self, channel_num: int, color: int) -> str:
        """Set channel color."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import channels

            channels.setChannelColor(channel_num, color)
            return f"Channel {channel_num} color set to: {color}"
        except Exception as e:
            return f"Error setting channel color: {e}"

    # =========================================================================
    # Pattern Controls
    # =========================================================================

    def patterns_count(self) -> str:
        """Get total number of patterns."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import patterns

            count = patterns.patternCount()
            return f"Total patterns: {count}"
        except Exception as e:
            return f"Error getting pattern count: {e}"

    def patterns_get_name(self, pattern_num: int) -> str:
        """Get pattern name."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import patterns

            name = patterns.getPatternName(pattern_num)
            return f"Pattern {pattern_num} name: {name}"
        except Exception as e:
            return f"Error getting pattern name: {e}"

    def patterns_set_name(self, pattern_num: int, name: str) -> str:
        """Set pattern name."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import patterns

            patterns.setPatternName(pattern_num, name)
            return f"Pattern {pattern_num} name set to: {name}"
        except Exception as e:
            return f"Error setting pattern name: {e}"

    def patterns_get_length(self, pattern_num: int) -> str:
        """Get pattern length in beats."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import patterns

            length = patterns.getPatternLength(pattern_num)
            return f"Pattern {pattern_num} length: {length} beats"
        except Exception as e:
            return f"Error getting pattern length: {e}"

    def patterns_jump_to(self, pattern_num: int) -> str:
        """Jump to a specific pattern."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import patterns

            patterns.jumpToPattern(pattern_num)
            return f"Jumped to pattern {pattern_num}"
        except Exception as e:
            return f"Error jumping to pattern: {e}"

    # =========================================================================
    # Playlist Controls
    # =========================================================================

    def playlist_get_track_name(self, track_num: int) -> str:
        """Get playlist track name."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import playlist

            name = playlist.getTrackName(track_num)
            return f"Playlist track {track_num} name: {name}"
        except Exception as e:
            return f"Error getting playlist track name: {e}"

    def playlist_set_track_name(self, track_num: int, name: str) -> str:
        """Set playlist track name."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import playlist

            playlist.setTrackName(track_num, name)
            return f"Playlist track {track_num} name set to: {name}"
        except Exception as e:
            return f"Error setting playlist track name: {e}"

    # =========================================================================
    # General / Project Controls
    # =========================================================================

    def general_get_version(self) -> str:
        """Get FL Studio version."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import general

            version = general.getVersion()
            return f"FL Studio version: {version}"
        except Exception as e:
            return f"Error getting FL Studio version: {e}"

    def general_get_project_title(self) -> str:
        """Get current project title."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import general

            # Try to get project info - the API varies by FL Studio version
            try:
                title = general.getProjectTitle()
            except AttributeError:
                # Fallback for older API
                title = "Unknown"
            return f"Project title: {title}"
        except Exception as e:
            return f"Error getting project title: {e}"

    def general_save_project(self) -> str:
        """Save the current project."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import general

            general.saveProject()
            return "Project saved"
        except Exception as e:
            return f"Error saving project: {e}"

    def general_undo(self) -> str:
        """Undo the last action."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import general

            general.undoUp()
            return "Undo performed"
        except Exception as e:
            return f"Error performing undo: {e}"

    # =========================================================================
    # UI Controls
    # =========================================================================

    def ui_show_window(self, window_id: int) -> str:
        """Show a specific FL Studio window."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import ui

            ui.showWindow(window_id)
            return f"Showing window: {window_id}"
        except Exception as e:
            return f"Error showing window: {e}"

    def ui_get_visible(self, window_id: int) -> str:
        """Check if a window is visible."""
        if not self._ensure_enabled():
            return "Error: Flapi not connected to FL Studio"
        try:
            import ui

            visible = ui.getVisible(window_id)
            return f"Window {window_id} visible: {visible}"
        except Exception as e:
            return f"Error checking window visibility: {e}"

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _ensure_enabled(self) -> bool:
        """Ensure Flapi is enabled, attempting to enable if not.

        Returns:
            True if Flapi is enabled, False otherwise.
        """
        if self._enabled:
            return True

        # Try to enable
        return self.enable()


# Global bridge instance
_bridge: FLStudioBridge | None = None


def get_bridge() -> FLStudioBridge:
    """Get the global FLStudioBridge instance.

    Returns:
        The global FLStudioBridge instance.
    """
    global _bridge
    if _bridge is None:
        _bridge = FLStudioBridge()
    return _bridge

