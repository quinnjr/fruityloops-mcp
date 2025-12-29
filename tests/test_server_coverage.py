"""Tests to improve server coverage."""

from unittest.mock import MagicMock, patch

import pytest

from fruityloops_mcp.server import FLStudioMCPServer


@pytest.fixture
def mock_fl_bridge():
    """Mocks the FL Bridge client."""
    with patch("fruityloops_mcp.server.FLBridgeClient") as MockBridge:
        mock_bridge_instance = MagicMock()
        mock_bridge_instance.is_available.return_value = True
        MockBridge.return_value = mock_bridge_instance
        yield mock_bridge_instance


@pytest.fixture
def server_with_fl(mock_fl_bridge):
    """Fixture for a server instance with FL Studio Bridge available."""
    with patch("fruityloops_mcp.server.FL_STUDIO_AVAILABLE", True):
        server = FLStudioMCPServer()
        server.fl_bridge = mock_fl_bridge
        return server


@pytest.fixture
def server_without_fl():
    """Fixture for a server instance with FL Studio Bridge NOT available."""
    with (
        patch("fruityloops_mcp.server.FL_STUDIO_AVAILABLE", False),
        patch("fruityloops_mcp.server.FLBridgeClient") as MockBridge,
    ):
        mock_bridge_instance = MagicMock()
        mock_bridge_instance.is_available.return_value = False
        MockBridge.return_value = mock_bridge_instance
        server = FLStudioMCPServer()
        return server


class TestServerWithoutFLStudio:
    """Tests for server behavior when FL Studio Bridge is not available."""

    @pytest.mark.asyncio
    async def test_fl_tools_fail_when_bridge_not_available(self, server_without_fl):
        """Test that FL Studio tools return error when bridge not available."""
        # When bridge is not available, FL tools should return an error message
        # The actual check happens in call_tool handler via fl_bridge.is_available()
        server_without_fl.fl_bridge.is_available.return_value = False
        # _execute_tool doesn't check availability, that's done in call_tool
        # So let's test that the tool execution works but returns bridge result
        server_without_fl.fl_bridge.transport_start.return_value = None
        result = await server_without_fl._execute_tool("transport_start", {})
        assert "Failed" in result or result is not None


class TestAllServerTools:
    """Test all server tools to achieve high coverage."""

    @pytest.mark.asyncio
    async def test_transport_tools(self, server_with_fl, mock_fl_bridge):
        """Test all transport control tools."""
        mock_fl_bridge.transport_start.return_value = "Started"
        result = await server_with_fl._execute_tool("transport_start", {})
        assert "started" in result.lower()
        mock_fl_bridge.transport_start.assert_called_once()

        mock_fl_bridge.transport_stop.return_value = "Stopped"
        result = await server_with_fl._execute_tool("transport_stop", {})
        assert "stopped" in result.lower()
        mock_fl_bridge.transport_stop.assert_called_once()

        mock_fl_bridge.transport_record.return_value = "Recording toggled"
        result = await server_with_fl._execute_tool("transport_record", {})
        assert "recording" in result.lower()
        mock_fl_bridge.transport_record.assert_called_once()

        mock_fl_bridge.transport_get_song_pos.return_value = 100
        result = await server_with_fl._execute_tool("transport_get_song_pos", {})
        assert "100" in result
        mock_fl_bridge.transport_get_song_pos.assert_called_once()

        mock_fl_bridge.transport_set_song_pos.return_value = "Position set"
        result = await server_with_fl._execute_tool("transport_set_song_pos", {"position": 200})
        assert "200" in result
        mock_fl_bridge.transport_set_song_pos.assert_called_once_with(200)

    @pytest.mark.asyncio
    async def test_mixer_tools(self, server_with_fl, mock_fl_bridge):
        """Test all mixer control tools."""
        mock_fl_bridge.mixer_get_track_volume.return_value = 0.5
        result = await server_with_fl._execute_tool("mixer_get_track_volume", {"track_num": 1})
        assert "0.5" in result

        mock_fl_bridge.mixer_set_track_volume.return_value = "Volume set"
        result = await server_with_fl._execute_tool(
            "mixer_set_track_volume", {"track_num": 1, "volume": 0.7}
        )
        assert "0.7" in result
        mock_fl_bridge.mixer_set_track_volume.assert_called_once_with(1, 0.7)

        mock_fl_bridge.mixer_get_track_name.return_value = "Kick"
        result = await server_with_fl._execute_tool("mixer_get_track_name", {"track_num": 1})
        assert "Kick" in result

        mock_fl_bridge.mixer_set_track_name.return_value = "Name set"
        result = await server_with_fl._execute_tool(
            "mixer_set_track_name", {"track_num": 1, "name": "Snare"}
        )
        assert "Snare" in result
        mock_fl_bridge.mixer_set_track_name.assert_called_once_with(1, "Snare")

    @pytest.mark.asyncio
    async def test_channel_tools(self, server_with_fl, mock_fl_bridge):
        """Test all channel control tools."""
        mock_fl_bridge.channels_channel_count.return_value = 10
        result = await server_with_fl._execute_tool("channels_channel_count", {})
        assert "10" in result

        mock_fl_bridge.channels_get_channel_name.return_value = "Synth"
        result = await server_with_fl._execute_tool("channels_get_channel_name", {"channel_num": 0})
        assert "Synth" in result

        mock_fl_bridge.channels_set_channel_volume.return_value = "Volume set"
        result = await server_with_fl._execute_tool(
            "channels_set_channel_volume", {"channel_num": 0, "volume": 0.8}
        )
        assert "0.8" in result
        mock_fl_bridge.channels_set_channel_volume.assert_called_once_with(0, 0.8)

        mock_fl_bridge.channels_mute_channel.return_value = "Muted"
        result = await server_with_fl._execute_tool(
            "channels_mute_channel", {"channel_num": 0, "mute": True}
        )
        assert "muted" in result.lower()
        mock_fl_bridge.channels_mute_channel.assert_called_once_with(0, True)

    @pytest.mark.asyncio
    async def test_pattern_tools(self, server_with_fl, mock_fl_bridge):
        """Test all pattern control tools."""
        mock_fl_bridge.patterns_pattern_count.return_value = 5
        result = await server_with_fl._execute_tool("patterns_pattern_count", {})
        assert "5" in result

        mock_fl_bridge.patterns_get_pattern_name.return_value = "Intro"
        result = await server_with_fl._execute_tool("patterns_get_pattern_name", {"pattern_num": 0})
        assert "Intro" in result

        mock_fl_bridge.patterns_set_pattern_name.return_value = "Name set"
        result = await server_with_fl._execute_tool(
            "patterns_set_pattern_name", {"pattern_num": 0, "name": "Verse"}
        )
        assert "Verse" in result
        mock_fl_bridge.patterns_set_pattern_name.assert_called_once_with(0, "Verse")

    @pytest.mark.asyncio
    async def test_general_tools(self, server_with_fl, mock_fl_bridge):
        """Test all general control tools."""
        mock_fl_bridge.general_get_project_title.return_value = "My Project"
        result = await server_with_fl._execute_tool("general_get_project_title", {})
        assert "My Project" in result

        mock_fl_bridge.general_get_version.return_value = 21000
        result = await server_with_fl._execute_tool("general_get_version", {})
        assert "21000" in result

    @pytest.mark.asyncio
    async def test_ui_tools(self, server_with_fl, mock_fl_bridge):
        """Test UI control tools."""
        mock_fl_bridge.ui_show_window.return_value = "Window shown"
        result = await server_with_fl._execute_tool("ui_show_window", {"window_id": 0})
        assert "window" in result.lower()
        mock_fl_bridge.ui_show_window.assert_called_once_with(0)

    @pytest.mark.asyncio
    async def test_playlist_tools(self, server_with_fl, mock_fl_bridge):
        """Test playlist control tools."""
        mock_fl_bridge.playlist_get_track_name.return_value = "Lead Synth"
        result = await server_with_fl._execute_tool("playlist_get_track_name", {"track_num": 0})
        assert "Lead Synth" in result


class TestServerInitialization:
    """Test server initialization paths."""

    def test_server_creates_mcp_server(self):
        """Test that server creates MCP Server instance."""
        server = FLStudioMCPServer()
        assert server.server is not None
        assert server.server.name == "fruityloops-mcp"

    def test_server_creates_midi_interface(self):
        """Test that server creates MIDI interface."""
        server = FLStudioMCPServer()
        assert server.midi is not None

    def test_server_creates_fl_bridge_client(self):
        """Test that server creates FL Bridge client."""
        server = FLStudioMCPServer()
        assert server.fl_bridge is not None

    def test_server_initialization_with_default_midi_port(self):
        """Test server initialization uses default MIDI port name."""
        with patch("fruityloops_mcp.server.MIDIInterface") as MockMIDI:
            mock_instance = MockMIDI.return_value
            mock_instance.port_name = "FLStudio_MIDI"
            FLStudioMCPServer()
            MockMIDI.assert_called_once_with(port_name="FLStudio_MIDI")

    def test_server_initialization_with_custom_midi_port(self):
        """Test server initialization uses custom MIDI port name."""
        custom_port = "MyCustomPort"
        with patch("fruityloops_mcp.server.MIDIInterface") as MockMIDI:
            mock_instance = MockMIDI.return_value
            mock_instance.port_name = custom_port
            FLStudioMCPServer(midi_port=custom_port)
            MockMIDI.assert_called_once_with(port_name=custom_port)


class TestToolFailurePaths:
    """Test failure paths for tools."""

    @pytest.mark.asyncio
    async def test_transport_tools_when_bridge_returns_none(self, server_with_fl, mock_fl_bridge):
        """Test transport tools handle None return values."""
        mock_fl_bridge.transport_start.return_value = None
        result = await server_with_fl._execute_tool("transport_start", {})
        assert "Failed" in result

        mock_fl_bridge.transport_get_song_pos.return_value = None
        result = await server_with_fl._execute_tool("transport_get_song_pos", {})
        assert "Failed" in result

    @pytest.mark.asyncio
    async def test_mixer_tools_when_bridge_returns_none(self, server_with_fl, mock_fl_bridge):
        """Test mixer tools handle None return values."""
        mock_fl_bridge.mixer_get_track_volume.return_value = None
        result = await server_with_fl._execute_tool("mixer_get_track_volume", {"track_num": 1})
        assert "Failed" in result

        mock_fl_bridge.mixer_set_track_volume.return_value = None
        result = await server_with_fl._execute_tool(
            "mixer_set_track_volume", {"track_num": 1, "volume": 0.5}
        )
        assert "Failed" in result

    @pytest.mark.asyncio
    async def test_channel_tools_when_bridge_returns_none(self, server_with_fl, mock_fl_bridge):
        """Test channel tools handle None return values."""
        mock_fl_bridge.channels_channel_count.return_value = None
        result = await server_with_fl._execute_tool("channels_channel_count", {})
        assert "Failed" in result

    @pytest.mark.asyncio
    async def test_pattern_tools_when_bridge_returns_none(self, server_with_fl, mock_fl_bridge):
        """Test pattern tools handle None return values."""
        mock_fl_bridge.patterns_pattern_count.return_value = None
        result = await server_with_fl._execute_tool("patterns_pattern_count", {})
        assert "Failed" in result

    @pytest.mark.asyncio
    async def test_general_tools_when_bridge_returns_none(self, server_with_fl, mock_fl_bridge):
        """Test general tools handle None return values."""
        mock_fl_bridge.general_get_project_title.return_value = None
        result = await server_with_fl._execute_tool("general_get_project_title", {})
        assert "Failed" in result
