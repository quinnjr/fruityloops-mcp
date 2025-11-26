"""Tests to improve server coverage."""

from unittest.mock import MagicMock, patch

import pytest

from fruityloops_mcp.server import FLStudioMCPServer


@pytest.fixture
def mock_flapi_bridge():
    """Mock the Flapi bridge for testing FL Studio tools."""
    with patch("fruityloops_mcp.server.get_bridge") as mock_get_bridge:
        mock_bridge = MagicMock()
        mock_get_bridge.return_value = mock_bridge
        yield mock_bridge


@pytest.fixture
def server(mock_flapi_bridge):
    """Fixture for a server instance with mocked Flapi bridge."""
    return FLStudioMCPServer()


class TestFlapiConnectionTools:
    """Tests for Flapi connection tools."""

    @pytest.mark.asyncio
    async def test_flapi_connect_success(self, server, mock_flapi_bridge):
        """Test successful Flapi connection."""
        mock_flapi_bridge.enable.return_value = True
        result = await server._execute_tool("flapi_connect", {})
        assert "Connected to FL Studio via Flapi" in result
        mock_flapi_bridge.enable.assert_called_once()

    @pytest.mark.asyncio
    async def test_flapi_connect_failure(self, server, mock_flapi_bridge):
        """Test failed Flapi connection."""
        mock_flapi_bridge.enable.return_value = False
        result = await server._execute_tool("flapi_connect", {})
        assert "Failed to connect" in result

    @pytest.mark.asyncio
    async def test_flapi_disconnect(self, server, mock_flapi_bridge):
        """Test Flapi disconnection."""
        result = await server._execute_tool("flapi_disconnect", {})
        assert "Disconnected" in result
        mock_flapi_bridge.disable.assert_called_once()

    @pytest.mark.asyncio
    async def test_flapi_status(self, server, mock_flapi_bridge):
        """Test Flapi status check."""
        mock_flapi_bridge.is_available = True
        mock_flapi_bridge.is_enabled = True
        mock_flapi_bridge.test_connection.return_value = True
        result = await server._execute_tool("flapi_status", {})
        assert "Flapi library available: True" in result
        assert "Flapi enabled: True" in result


class TestTransportTools:
    """Test all transport control tools via Flapi bridge."""

    @pytest.mark.asyncio
    async def test_transport_start(self, server, mock_flapi_bridge):
        """Test transport start."""
        mock_flapi_bridge.transport_start.return_value = "FL Studio playback started"
        result = await server._execute_tool("transport_start", {})
        assert "started" in result
        mock_flapi_bridge.transport_start.assert_called_once()

    @pytest.mark.asyncio
    async def test_transport_stop(self, server, mock_flapi_bridge):
        """Test transport stop."""
        mock_flapi_bridge.transport_stop.return_value = "FL Studio playback stopped"
        result = await server._execute_tool("transport_stop", {})
        assert "stopped" in result
        mock_flapi_bridge.transport_stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_transport_record(self, server, mock_flapi_bridge):
        """Test transport record toggle."""
        mock_flapi_bridge.transport_record.return_value = "FL Studio recording toggled"
        result = await server._execute_tool("transport_record", {})
        assert "toggled" in result
        mock_flapi_bridge.transport_record.assert_called_once()

    @pytest.mark.asyncio
    async def test_transport_get_song_pos(self, server, mock_flapi_bridge):
        """Test getting song position."""
        mock_flapi_bridge.transport_get_song_pos.return_value = "Current song position: 100"
        result = await server._execute_tool("transport_get_song_pos", {})
        assert "100" in result

    @pytest.mark.asyncio
    async def test_transport_set_song_pos(self, server, mock_flapi_bridge):
        """Test setting song position."""
        mock_flapi_bridge.transport_set_song_pos.return_value = "Song position set to: 200"
        result = await server._execute_tool("transport_set_song_pos", {"position": 200})
        assert "200" in result
        mock_flapi_bridge.transport_set_song_pos.assert_called_once_with(200)

    @pytest.mark.asyncio
    async def test_transport_get_bpm(self, server, mock_flapi_bridge):
        """Test getting BPM."""
        mock_flapi_bridge.transport_get_bpm.return_value = "Current tempo: 120 BPM"
        result = await server._execute_tool("transport_get_bpm", {})
        assert "120" in result

    @pytest.mark.asyncio
    async def test_transport_set_bpm(self, server, mock_flapi_bridge):
        """Test setting BPM."""
        mock_flapi_bridge.transport_set_bpm.return_value = "Tempo set to: 140 BPM"
        result = await server._execute_tool("transport_set_bpm", {"bpm": 140})
        assert "140" in result
        mock_flapi_bridge.transport_set_bpm.assert_called_once_with(140)


class TestMixerTools:
    """Test all mixer control tools via Flapi bridge."""

    @pytest.mark.asyncio
    async def test_mixer_get_track_volume(self, server, mock_flapi_bridge):
        """Test getting mixer track volume."""
        mock_flapi_bridge.mixer_get_track_volume.return_value = "Track 1 volume: 0.5"
        result = await server._execute_tool("mixer_get_track_volume", {"track_num": 1})
        assert "0.5" in result

    @pytest.mark.asyncio
    async def test_mixer_set_track_volume(self, server, mock_flapi_bridge):
        """Test setting mixer track volume."""
        mock_flapi_bridge.mixer_set_track_volume.return_value = "Track 1 volume set to: 0.7"
        result = await server._execute_tool(
            "mixer_set_track_volume", {"track_num": 1, "volume": 0.7}
        )
        assert "0.7" in result
        mock_flapi_bridge.mixer_set_track_volume.assert_called_once_with(1, 0.7)

    @pytest.mark.asyncio
    async def test_mixer_get_track_name(self, server, mock_flapi_bridge):
        """Test getting mixer track name."""
        mock_flapi_bridge.mixer_get_track_name.return_value = "Track 1 name: Kick"
        result = await server._execute_tool("mixer_get_track_name", {"track_num": 1})
        assert "Kick" in result

    @pytest.mark.asyncio
    async def test_mixer_set_track_name(self, server, mock_flapi_bridge):
        """Test setting mixer track name."""
        mock_flapi_bridge.mixer_set_track_name.return_value = "Track 1 name set to: Snare"
        result = await server._execute_tool(
            "mixer_set_track_name", {"track_num": 1, "name": "Snare"}
        )
        assert "Snare" in result
        mock_flapi_bridge.mixer_set_track_name.assert_called_once_with(1, "Snare")

    @pytest.mark.asyncio
    async def test_mixer_get_track_pan(self, server, mock_flapi_bridge):
        """Test getting mixer track pan."""
        mock_flapi_bridge.mixer_get_track_pan.return_value = "Track 1 pan: 0.0"
        result = await server._execute_tool("mixer_get_track_pan", {"track_num": 1})
        assert "pan" in result

    @pytest.mark.asyncio
    async def test_mixer_set_track_pan(self, server, mock_flapi_bridge):
        """Test setting mixer track pan."""
        mock_flapi_bridge.mixer_set_track_pan.return_value = "Track 1 pan set to: -0.5"
        await server._execute_tool("mixer_set_track_pan", {"track_num": 1, "pan": -0.5})
        mock_flapi_bridge.mixer_set_track_pan.assert_called_once_with(1, -0.5)

    @pytest.mark.asyncio
    async def test_mixer_mute_track(self, server, mock_flapi_bridge):
        """Test muting mixer track."""
        mock_flapi_bridge.mixer_mute_track.return_value = "Track 1 muted"
        result = await server._execute_tool("mixer_mute_track", {"track_num": 1, "mute": True})
        assert "muted" in result
        mock_flapi_bridge.mixer_mute_track.assert_called_once_with(1, True)

    @pytest.mark.asyncio
    async def test_mixer_solo_track(self, server, mock_flapi_bridge):
        """Test soloing mixer track."""
        mock_flapi_bridge.mixer_solo_track.return_value = "Track 1 soloed"
        result = await server._execute_tool("mixer_solo_track", {"track_num": 1, "solo": True})
        assert "soloed" in result
        mock_flapi_bridge.mixer_solo_track.assert_called_once_with(1, True)


class TestChannelTools:
    """Test all channel control tools via Flapi bridge."""

    @pytest.mark.asyncio
    async def test_channels_channel_count(self, server, mock_flapi_bridge):
        """Test getting channel count."""
        mock_flapi_bridge.channels_count.return_value = "Total channels: 10"
        result = await server._execute_tool("channels_channel_count", {})
        assert "10" in result

    @pytest.mark.asyncio
    async def test_channels_get_channel_name(self, server, mock_flapi_bridge):
        """Test getting channel name."""
        mock_flapi_bridge.channels_get_name.return_value = "Channel 0 name: Synth"
        result = await server._execute_tool("channels_get_channel_name", {"channel_num": 0})
        assert "Synth" in result

    @pytest.mark.asyncio
    async def test_channels_set_channel_volume(self, server, mock_flapi_bridge):
        """Test setting channel volume."""
        mock_flapi_bridge.channels_set_volume.return_value = "Channel 0 volume set to: 0.8"
        result = await server._execute_tool(
            "channels_set_channel_volume", {"channel_num": 0, "volume": 0.8}
        )
        assert "0.8" in result
        mock_flapi_bridge.channels_set_volume.assert_called_once_with(0, 0.8)

    @pytest.mark.asyncio
    async def test_channels_mute_channel(self, server, mock_flapi_bridge):
        """Test muting channel."""
        mock_flapi_bridge.channels_mute.return_value = "Channel 0 muted"
        result = await server._execute_tool(
            "channels_mute_channel", {"channel_num": 0, "mute": True}
        )
        assert "muted" in result
        mock_flapi_bridge.channels_mute.assert_called_once_with(0, True)

    @pytest.mark.asyncio
    async def test_channels_get_channel_color(self, server, mock_flapi_bridge):
        """Test getting channel color."""
        mock_flapi_bridge.channels_get_color.return_value = "Channel 0 color: 16711680"
        result = await server._execute_tool("channels_get_channel_color", {"channel_num": 0})
        assert "color" in result

    @pytest.mark.asyncio
    async def test_channels_set_channel_color(self, server, mock_flapi_bridge):
        """Test setting channel color."""
        mock_flapi_bridge.channels_set_color.return_value = "Channel 0 color set to: 255"
        await server._execute_tool("channels_set_channel_color", {"channel_num": 0, "color": 255})
        mock_flapi_bridge.channels_set_color.assert_called_once_with(0, 255)


class TestPatternTools:
    """Test all pattern control tools via Flapi bridge."""

    @pytest.mark.asyncio
    async def test_patterns_pattern_count(self, server, mock_flapi_bridge):
        """Test getting pattern count."""
        mock_flapi_bridge.patterns_count.return_value = "Total patterns: 5"
        result = await server._execute_tool("patterns_pattern_count", {})
        assert "5" in result

    @pytest.mark.asyncio
    async def test_patterns_get_pattern_name(self, server, mock_flapi_bridge):
        """Test getting pattern name."""
        mock_flapi_bridge.patterns_get_name.return_value = "Pattern 0 name: Intro"
        result = await server._execute_tool("patterns_get_pattern_name", {"pattern_num": 0})
        assert "Intro" in result

    @pytest.mark.asyncio
    async def test_patterns_set_pattern_name(self, server, mock_flapi_bridge):
        """Test setting pattern name."""
        mock_flapi_bridge.patterns_set_name.return_value = "Pattern 0 name set to: Verse"
        result = await server._execute_tool(
            "patterns_set_pattern_name", {"pattern_num": 0, "name": "Verse"}
        )
        assert "Verse" in result
        mock_flapi_bridge.patterns_set_name.assert_called_once_with(0, "Verse")

    @pytest.mark.asyncio
    async def test_patterns_get_pattern_length(self, server, mock_flapi_bridge):
        """Test getting pattern length."""
        mock_flapi_bridge.patterns_get_length.return_value = "Pattern 0 length: 16 beats"
        result = await server._execute_tool("patterns_get_pattern_length", {"pattern_num": 0})
        assert "16" in result

    @pytest.mark.asyncio
    async def test_patterns_jump_to_pattern(self, server, mock_flapi_bridge):
        """Test jumping to pattern."""
        mock_flapi_bridge.patterns_jump_to.return_value = "Jumped to pattern 2"
        result = await server._execute_tool("patterns_jump_to_pattern", {"pattern_num": 2})
        assert "2" in result
        mock_flapi_bridge.patterns_jump_to.assert_called_once_with(2)


class TestPlaylistTools:
    """Test playlist control tools via Flapi bridge."""

    @pytest.mark.asyncio
    async def test_playlist_get_track_name(self, server, mock_flapi_bridge):
        """Test getting playlist track name."""
        mock_flapi_bridge.playlist_get_track_name.return_value = "Playlist track 0 name: Lead"
        result = await server._execute_tool("playlist_get_track_name", {"track_num": 0})
        assert "Lead" in result

    @pytest.mark.asyncio
    async def test_playlist_set_track_name(self, server, mock_flapi_bridge):
        """Test setting playlist track name."""
        mock_flapi_bridge.playlist_set_track_name.return_value = (
            "Playlist track 0 name set to: Bass"
        )
        await server._execute_tool("playlist_set_track_name", {"track_num": 0, "name": "Bass"})
        mock_flapi_bridge.playlist_set_track_name.assert_called_once_with(0, "Bass")


class TestGeneralTools:
    """Test general control tools via Flapi bridge."""

    @pytest.mark.asyncio
    async def test_general_get_project_title(self, server, mock_flapi_bridge):
        """Test getting project title."""
        mock_flapi_bridge.general_get_project_title.return_value = "Project title: My Song"
        result = await server._execute_tool("general_get_project_title", {})
        assert "My Song" in result

    @pytest.mark.asyncio
    async def test_general_get_version(self, server, mock_flapi_bridge):
        """Test getting FL Studio version."""
        mock_flapi_bridge.general_get_version.return_value = "FL Studio version: 21.0.0"
        result = await server._execute_tool("general_get_version", {})
        assert "21.0.0" in result

    @pytest.mark.asyncio
    async def test_general_save_project(self, server, mock_flapi_bridge):
        """Test saving project."""
        mock_flapi_bridge.general_save_project.return_value = "Project saved"
        result = await server._execute_tool("general_save_project", {})
        assert "saved" in result

    @pytest.mark.asyncio
    async def test_general_undo(self, server, mock_flapi_bridge):
        """Test undo."""
        mock_flapi_bridge.general_undo.return_value = "Undo performed"
        result = await server._execute_tool("general_undo", {})
        assert "Undo" in result


class TestUITools:
    """Test UI control tools via Flapi bridge."""

    @pytest.mark.asyncio
    async def test_ui_show_window(self, server, mock_flapi_bridge):
        """Test showing window."""
        mock_flapi_bridge.ui_show_window.return_value = "Showing window: 0"
        result = await server._execute_tool("ui_show_window", {"window_id": 0})
        assert "window" in result
        mock_flapi_bridge.ui_show_window.assert_called_once_with(0)

    @pytest.mark.asyncio
    async def test_ui_get_visible(self, server, mock_flapi_bridge):
        """Test checking window visibility."""
        mock_flapi_bridge.ui_get_visible.return_value = "Window 0 visible: True"
        result = await server._execute_tool("ui_get_visible", {"window_id": 0})
        assert "visible" in result
        mock_flapi_bridge.ui_get_visible.assert_called_once_with(0)


class TestServerInitialization:
    """Test server initialization paths."""

    def test_server_creates_mcp_server(self, mock_flapi_bridge):
        """Test that server creates MCP Server instance."""
        server = FLStudioMCPServer()
        assert server.server is not None
        assert server.server.name == "fruityloops-mcp"

    def test_server_creates_midi_interface(self, mock_flapi_bridge):
        """Test that server creates MIDI interface."""
        server = FLStudioMCPServer()
        assert server.midi is not None

    def test_server_creates_flapi_bridge(self, mock_flapi_bridge):
        """Test that server creates Flapi bridge."""
        server = FLStudioMCPServer()
        assert server.flapi_bridge is not None

    def test_server_initialization_with_default_midi_port(self, mock_flapi_bridge):
        """Test server initialization uses default MIDI port name."""
        with patch("fruityloops_mcp.server.MIDIInterface") as MockMIDI:
            mock_instance = MockMIDI.return_value
            mock_instance.port_name = "FLStudio_MIDI"
            FLStudioMCPServer()
            MockMIDI.assert_called_once_with(port_name="FLStudio_MIDI")

    def test_server_initialization_with_custom_midi_port(self, mock_flapi_bridge):
        """Test server initialization uses custom MIDI port name."""
        custom_port = "MyCustomPort"
        with patch("fruityloops_mcp.server.MIDIInterface") as MockMIDI:
            mock_instance = MockMIDI.return_value
            mock_instance.port_name = custom_port
            FLStudioMCPServer(midi_port=custom_port)
            MockMIDI.assert_called_once_with(port_name=custom_port)


class TestUnknownTool:
    """Test handling of unknown tools."""

    @pytest.mark.asyncio
    async def test_unknown_tool_raises_error(self, server, mock_flapi_bridge):
        """Test that unknown tool raises ValueError."""
        with pytest.raises(ValueError, match="Unknown tool"):
            await server._execute_tool("nonexistent_tool", {})
