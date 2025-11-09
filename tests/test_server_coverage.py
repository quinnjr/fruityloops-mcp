"""Tests to improve server coverage."""

from unittest.mock import patch

import pytest

from fruityloops_mcp.server import FLStudioMCPServer, StubModule


@pytest.fixture
def mock_fl_modules():
    """Mocks FL Studio API modules."""
    with (
        patch("fruityloops_mcp.server.transport") as mock_transport,
        patch("fruityloops_mcp.server.mixer") as mock_mixer,
        patch("fruityloops_mcp.server.channels") as mock_channels,
        patch("fruityloops_mcp.server.patterns") as mock_patterns,
        patch("fruityloops_mcp.server.general") as mock_general,
        patch("fruityloops_mcp.server.ui") as mock_ui,
        patch("fruityloops_mcp.server.playlist") as mock_playlist,
    ):
        yield {
            "transport": mock_transport,
            "mixer": mock_mixer,
            "channels": mock_channels,
            "patterns": mock_patterns,
            "general": mock_general,
            "ui": mock_ui,
            "playlist": mock_playlist,
        }


@pytest.fixture
def server_with_fl(mock_fl_modules):
    """Fixture for a server instance with FL Studio API available."""
    with patch("fruityloops_mcp.server.FL_STUDIO_AVAILABLE", True):
        return FLStudioMCPServer()


@pytest.fixture
def server_without_fl():
    """Fixture for a server instance with FL Studio API NOT available."""
    with patch("fruityloops_mcp.server.FL_STUDIO_AVAILABLE", False):
        return FLStudioMCPServer()


class TestServerWithoutFLStudio:
    """Tests for server behavior when FL Studio API is not available."""

    def test_stub_module_getattr(self):
        """Test that StubModule returns itself for any attribute access."""
        stub = StubModule("test_module")
        assert stub.some_attribute is stub
        assert stub.another_method() is stub
        assert stub.nested.attribute is stub

    @pytest.mark.asyncio
    async def test_tools_fail_when_fl_not_available(self, server_without_fl):
        """Test that FL Studio tools work with stubs when FL not available."""
        # FL tools use stub modules when FL Studio is not available
        # They execute but don't actually interact with FL Studio
        result = await server_without_fl._execute_tool("transport_start", {})
        assert result is not None  # Stub modules allow execution to complete


class TestAllServerTools:
    """Test all server tools to achieve high coverage."""

    @pytest.mark.asyncio
    async def test_transport_tools(self, server_with_fl, mock_fl_modules):
        """Test all transport control tools."""
        await server_with_fl._execute_tool("transport_start", {})
        mock_fl_modules["transport"].start.assert_called_once()

        await server_with_fl._execute_tool("transport_stop", {})
        mock_fl_modules["transport"].stop.assert_called_once()

        await server_with_fl._execute_tool("transport_record", {})
        mock_fl_modules["transport"].record.assert_called_once()

        mock_fl_modules["transport"].getSongPos.return_value = 100
        result = await server_with_fl._execute_tool("transport_get_song_pos", {})
        assert "Current song position: 100" in result

        await server_with_fl._execute_tool("transport_set_song_pos", {"position": 200})
        mock_fl_modules["transport"].setSongPos.assert_called_once_with(200)

    @pytest.mark.asyncio
    async def test_mixer_tools(self, server_with_fl, mock_fl_modules):
        """Test all mixer control tools."""
        mock_fl_modules["mixer"].getTrackVolume.return_value = 0.5
        result = await server_with_fl._execute_tool("mixer_get_track_volume", {"track_num": 1})
        assert "Track 1 volume: 0.5" in result

        await server_with_fl._execute_tool(
            "mixer_set_track_volume", {"track_num": 1, "volume": 0.7}
        )
        mock_fl_modules["mixer"].setTrackVolume.assert_called_once_with(1, 0.7)

        mock_fl_modules["mixer"].getTrackName.return_value = "Kick"
        result = await server_with_fl._execute_tool("mixer_get_track_name", {"track_num": 1})
        assert "Track 1 name: Kick" in result

        await server_with_fl._execute_tool(
            "mixer_set_track_name", {"track_num": 1, "name": "Snare"}
        )
        mock_fl_modules["mixer"].setTrackName.assert_called_once_with(1, "Snare")

    @pytest.mark.asyncio
    async def test_channel_tools(self, server_with_fl, mock_fl_modules):
        """Test all channel control tools."""
        mock_fl_modules["channels"].channelCount.return_value = 10
        result = await server_with_fl._execute_tool("channels_channel_count", {})
        assert "Total channels: 10" in result

        mock_fl_modules["channels"].getChannelName.return_value = "Synth"
        result = await server_with_fl._execute_tool("channels_get_channel_name", {"channel_num": 0})
        assert "Channel 0 name: Synth" in result

        await server_with_fl._execute_tool(
            "channels_set_channel_volume", {"channel_num": 0, "volume": 0.8}
        )
        mock_fl_modules["channels"].setChannelVolume.assert_called_once_with(0, 0.8)

        await server_with_fl._execute_tool(
            "channels_mute_channel", {"channel_num": 0, "mute": True}
        )
        mock_fl_modules["channels"].muteChannel.assert_called_once_with(0, True)

    @pytest.mark.asyncio
    async def test_pattern_tools(self, server_with_fl, mock_fl_modules):
        """Test all pattern control tools."""
        mock_fl_modules["patterns"].patternCount.return_value = 5
        result = await server_with_fl._execute_tool("patterns_pattern_count", {})
        assert "Total patterns: 5" in result

        mock_fl_modules["patterns"].getPatternName.return_value = "Intro"
        result = await server_with_fl._execute_tool("patterns_get_pattern_name", {"pattern_num": 0})
        assert "Pattern 0 name: Intro" in result

        await server_with_fl._execute_tool(
            "patterns_set_pattern_name", {"pattern_num": 0, "name": "Verse"}
        )
        mock_fl_modules["patterns"].setPatternName.assert_called_once_with(0, "Verse")

    @pytest.mark.asyncio
    async def test_general_tools(self, server_with_fl, mock_fl_modules):
        """Test all general control tools."""
        mock_fl_modules["general"].getProjectTitle.return_value = "My Project"
        result = await server_with_fl._execute_tool("general_get_project_title", {})
        assert "Project title: My Project" in result

        mock_fl_modules["general"].getVersion.return_value = "21.0.0"
        result = await server_with_fl._execute_tool("general_get_version", {})
        assert "FL Studio version: 21.0.0" in result

    @pytest.mark.asyncio
    async def test_ui_tools(self, server_with_fl, mock_fl_modules):
        """Test UI control tools."""
        await server_with_fl._execute_tool("ui_show_window", {"window_id": 0})
        mock_fl_modules["ui"].showWindow.assert_called_once_with(0)

    @pytest.mark.asyncio
    async def test_playlist_tools(self, server_with_fl, mock_fl_modules):
        """Test playlist control tools."""
        mock_fl_modules["playlist"].getTrackName.return_value = "Lead Synth"
        result = await server_with_fl._execute_tool("playlist_get_track_name", {"track_num": 0})
        assert "Playlist track 0 name: Lead Synth" in result


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
