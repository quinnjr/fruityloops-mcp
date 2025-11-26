"""Tests for the Flapi bridge module."""

from unittest.mock import patch


class TestFLStudioBridgeInit:
    """Test FLStudioBridge initialization and properties."""

    def test_bridge_initialization(self):
        """Test bridge initializes with correct default state."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        bridge = FLStudioBridge()
        assert bridge._enabled is False
        assert bridge._connected is False

    def test_is_enabled_property(self):
        """Test is_enabled property."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        bridge = FLStudioBridge()
        assert bridge.is_enabled is False
        bridge._enabled = True
        assert bridge.is_enabled is True

    def test_is_connected_property(self):
        """Test is_connected property."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        bridge = FLStudioBridge()
        assert bridge.is_connected is False
        bridge._connected = True
        assert bridge.is_connected is True

    def test_is_available_property(self):
        """Test is_available property reflects flapi availability."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        bridge = FLStudioBridge()
        # is_available depends on whether flapi is installed
        assert isinstance(bridge.is_available, bool)


class TestFLStudioBridgeEnable:
    """Test FLStudioBridge enable/disable functionality."""

    @patch("fruityloops_mcp.flapi_bridge._flapi_available", False)
    def test_enable_when_flapi_not_available(self):
        """Test enable returns False when Flapi not installed."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        bridge = FLStudioBridge()
        result = bridge.enable()
        assert result is False
        assert bridge.is_enabled is False

    @patch("fruityloops_mcp.flapi_bridge._flapi_available", True)
    @patch("fruityloops_mcp.flapi_bridge.flapi")
    def test_enable_success(self, mock_flapi):
        """Test successful enable."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        bridge = FLStudioBridge()
        result = bridge.enable()
        assert result is True
        assert bridge.is_enabled is True
        assert bridge.is_connected is True
        mock_flapi.enable.assert_called_once()

    @patch("fruityloops_mcp.flapi_bridge._flapi_available", True)
    @patch("fruityloops_mcp.flapi_bridge.flapi")
    def test_enable_already_enabled(self, mock_flapi):
        """Test enable when already enabled."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        bridge = FLStudioBridge()
        bridge._enabled = True
        result = bridge.enable()
        assert result is True
        mock_flapi.enable.assert_not_called()

    @patch("fruityloops_mcp.flapi_bridge._flapi_available", True)
    @patch("fruityloops_mcp.flapi_bridge.flapi")
    def test_enable_exception(self, mock_flapi):
        """Test enable handles exception."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_flapi.enable.side_effect = Exception("Connection failed")
        bridge = FLStudioBridge()
        result = bridge.enable()
        assert result is False
        assert bridge.is_enabled is False
        assert bridge.is_connected is False


class TestFLStudioBridgeDisable:
    """Test FLStudioBridge disable functionality."""

    @patch("fruityloops_mcp.flapi_bridge._flapi_available", False)
    def test_disable_when_flapi_not_available(self):
        """Test disable does nothing when Flapi not available."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        bridge = FLStudioBridge()
        bridge.disable()  # Should not raise

    @patch("fruityloops_mcp.flapi_bridge._flapi_available", True)
    def test_disable_when_not_enabled(self):
        """Test disable does nothing when not enabled."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        bridge = FLStudioBridge()
        bridge.disable()  # Should not raise

    @patch("fruityloops_mcp.flapi_bridge._flapi_available", True)
    @patch("fruityloops_mcp.flapi_bridge.flapi")
    def test_disable_success(self, mock_flapi):
        """Test successful disable."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        bridge = FLStudioBridge()
        bridge._enabled = True
        bridge._connected = True
        bridge.disable()
        assert bridge.is_enabled is False
        assert bridge.is_connected is False
        mock_flapi.disable.assert_called_once()

    @patch("fruityloops_mcp.flapi_bridge._flapi_available", True)
    @patch("fruityloops_mcp.flapi_bridge.flapi")
    def test_disable_exception(self, mock_flapi):
        """Test disable handles exception."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_flapi.disable.side_effect = Exception("Disconnect failed")
        bridge = FLStudioBridge()
        bridge._enabled = True
        bridge.disable()  # Should not raise


class TestFLStudioBridgeTestConnection:
    """Test FLStudioBridge test_connection functionality."""

    def test_test_connection_when_not_enabled(self):
        """Test test_connection returns False when not enabled."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        bridge = FLStudioBridge()
        result = bridge.test_connection()
        assert result is False

    @patch("fruityloops_mcp.flapi_bridge.general")
    def test_test_connection_success(self, mock_general):
        """Test successful connection test."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_general.getVersion.return_value = "21.0.0"
        bridge = FLStudioBridge()
        bridge._enabled = True
        result = bridge.test_connection()
        assert result is True

    @patch("fruityloops_mcp.flapi_bridge.general")
    def test_test_connection_exception(self, mock_general):
        """Test connection test handles exception."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_general.getVersion.side_effect = Exception("Not connected")
        bridge = FLStudioBridge()
        bridge._enabled = True
        bridge._connected = True
        result = bridge.test_connection()
        assert result is False
        assert bridge._connected is False


class TestFLStudioBridgeContextManager:
    """Test FLStudioBridge context manager."""

    @patch("fruityloops_mcp.flapi_bridge._flapi_available", True)
    @patch("fruityloops_mcp.flapi_bridge.flapi")
    def test_connection_context_manager(self, mock_flapi):
        """Test connection context manager."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        bridge = FLStudioBridge()
        with bridge.connection() as ctx:
            assert ctx is bridge
            assert bridge.is_enabled is True
        assert bridge.is_enabled is False


class TestFLStudioBridgeEnsureEnabled:
    """Test FLStudioBridge _ensure_enabled method."""

    def test_ensure_enabled_when_enabled(self):
        """Test _ensure_enabled returns True when already enabled."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        bridge = FLStudioBridge()
        bridge._enabled = True
        result = bridge._ensure_enabled()
        assert result is True

    @patch("fruityloops_mcp.flapi_bridge._flapi_available", False)
    def test_ensure_enabled_tries_to_enable(self):
        """Test _ensure_enabled tries to enable when not enabled."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        bridge = FLStudioBridge()
        result = bridge._ensure_enabled()
        assert result is False  # Will fail because flapi not available


class TestFLStudioBridgeTransportMethods:
    """Test FLStudioBridge transport control methods."""

    def test_transport_start_not_enabled(self):
        """Test transport_start when not enabled."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=False):
            bridge = FLStudioBridge()
            result = bridge.transport_start()
            assert "Error" in result

    @patch("fruityloops_mcp.flapi_bridge.transport")
    def test_transport_start_success(self, mock_transport):
        """Test successful transport_start."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.transport_start()
            assert "started" in result
            mock_transport.start.assert_called_once()

    @patch("fruityloops_mcp.flapi_bridge.transport")
    def test_transport_start_exception(self, mock_transport):
        """Test transport_start handles exception."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_transport.start.side_effect = Exception("Error")
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.transport_start()
            assert "Error" in result

    @patch("fruityloops_mcp.flapi_bridge.transport")
    def test_transport_stop_success(self, mock_transport):
        """Test successful transport_stop."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.transport_stop()
            assert "stopped" in result

    @patch("fruityloops_mcp.flapi_bridge.transport")
    def test_transport_record_success(self, mock_transport):
        """Test successful transport_record."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.transport_record()
            assert "toggled" in result

    @patch("fruityloops_mcp.flapi_bridge.transport")
    def test_transport_get_song_pos_success(self, mock_transport):
        """Test successful transport_get_song_pos."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_transport.getSongPos.return_value = 1000
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.transport_get_song_pos()
            assert "1000" in result

    @patch("fruityloops_mcp.flapi_bridge.transport")
    def test_transport_set_song_pos_success(self, mock_transport):
        """Test successful transport_set_song_pos."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.transport_set_song_pos(500)
            assert "500" in result
            mock_transport.setSongPos.assert_called_once_with(500)

    @patch("fruityloops_mcp.flapi_bridge.transport")
    def test_transport_get_bpm_success(self, mock_transport):
        """Test successful transport_get_bpm."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_transport.getTempo.return_value = 120.0
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.transport_get_bpm()
            assert "120" in result

    @patch("fruityloops_mcp.flapi_bridge.transport")
    def test_transport_set_bpm_success(self, mock_transport):
        """Test successful transport_set_bpm."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.transport_set_bpm(140.0)
            assert "140" in result
            mock_transport.setTempo.assert_called_once_with(140.0)


class TestFLStudioBridgeMixerMethods:
    """Test FLStudioBridge mixer control methods."""

    @patch("fruityloops_mcp.flapi_bridge.mixer")
    def test_mixer_get_track_volume_success(self, mock_mixer):
        """Test successful mixer_get_track_volume."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_mixer.getTrackVolume.return_value = 0.8
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.mixer_get_track_volume(1)
            assert "0.8" in result

    @patch("fruityloops_mcp.flapi_bridge.mixer")
    def test_mixer_set_track_volume_success(self, mock_mixer):
        """Test successful mixer_set_track_volume."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.mixer_set_track_volume(1, 0.5)
            assert "0.5" in result

    @patch("fruityloops_mcp.flapi_bridge.mixer")
    def test_mixer_get_track_name_success(self, mock_mixer):
        """Test successful mixer_get_track_name."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_mixer.getTrackName.return_value = "Drums"
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.mixer_get_track_name(1)
            assert "Drums" in result

    @patch("fruityloops_mcp.flapi_bridge.mixer")
    def test_mixer_set_track_name_success(self, mock_mixer):
        """Test successful mixer_set_track_name."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.mixer_set_track_name(1, "Bass")
            assert "Bass" in result

    @patch("fruityloops_mcp.flapi_bridge.mixer")
    def test_mixer_get_track_pan_success(self, mock_mixer):
        """Test successful mixer_get_track_pan."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_mixer.getTrackPan.return_value = -0.5
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.mixer_get_track_pan(1)
            assert "-0.5" in result

    @patch("fruityloops_mcp.flapi_bridge.mixer")
    def test_mixer_set_track_pan_success(self, mock_mixer):
        """Test successful mixer_set_track_pan."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.mixer_set_track_pan(1, 0.25)
            assert "0.25" in result

    @patch("fruityloops_mcp.flapi_bridge.mixer")
    def test_mixer_mute_track_success(self, mock_mixer):
        """Test successful mixer_mute_track."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.mixer_mute_track(1, True)
            assert "muted" in result

    @patch("fruityloops_mcp.flapi_bridge.mixer")
    def test_mixer_unmute_track_success(self, mock_mixer):
        """Test successful mixer unmute."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.mixer_mute_track(1, False)
            assert "unmuted" in result

    @patch("fruityloops_mcp.flapi_bridge.mixer")
    def test_mixer_solo_track_success(self, mock_mixer):
        """Test successful mixer_solo_track."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.mixer_solo_track(1, True)
            assert "soloed" in result

    @patch("fruityloops_mcp.flapi_bridge.mixer")
    def test_mixer_unsolo_track_success(self, mock_mixer):
        """Test successful mixer unsolo."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.mixer_solo_track(1, False)
            assert "unsoloed" in result


class TestFLStudioBridgeChannelMethods:
    """Test FLStudioBridge channel control methods."""

    @patch("fruityloops_mcp.flapi_bridge.channels")
    def test_channels_count_success(self, mock_channels):
        """Test successful channels_count."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_channels.channelCount.return_value = 16
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.channels_count()
            assert "16" in result

    @patch("fruityloops_mcp.flapi_bridge.channels")
    def test_channels_get_name_success(self, mock_channels):
        """Test successful channels_get_name."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_channels.getChannelName.return_value = "Synth"
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.channels_get_name(0)
            assert "Synth" in result

    @patch("fruityloops_mcp.flapi_bridge.channels")
    def test_channels_set_volume_success(self, mock_channels):
        """Test successful channels_set_volume."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.channels_set_volume(0, 0.7)
            assert "0.7" in result

    @patch("fruityloops_mcp.flapi_bridge.channels")
    def test_channels_mute_success(self, mock_channels):
        """Test successful channels_mute."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.channels_mute(0, True)
            assert "muted" in result

    @patch("fruityloops_mcp.flapi_bridge.channels")
    def test_channels_get_color_success(self, mock_channels):
        """Test successful channels_get_color."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_channels.getChannelColor.return_value = 16711680
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.channels_get_color(0)
            assert "16711680" in result

    @patch("fruityloops_mcp.flapi_bridge.channels")
    def test_channels_set_color_success(self, mock_channels):
        """Test successful channels_set_color."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.channels_set_color(0, 255)
            assert "255" in result


class TestFLStudioBridgePatternMethods:
    """Test FLStudioBridge pattern control methods."""

    @patch("fruityloops_mcp.flapi_bridge.patterns")
    def test_patterns_count_success(self, mock_patterns):
        """Test successful patterns_count."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_patterns.patternCount.return_value = 8
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.patterns_count()
            assert "8" in result

    @patch("fruityloops_mcp.flapi_bridge.patterns")
    def test_patterns_get_name_success(self, mock_patterns):
        """Test successful patterns_get_name."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_patterns.getPatternName.return_value = "Intro"
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.patterns_get_name(0)
            assert "Intro" in result

    @patch("fruityloops_mcp.flapi_bridge.patterns")
    def test_patterns_set_name_success(self, mock_patterns):
        """Test successful patterns_set_name."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.patterns_set_name(0, "Verse")
            assert "Verse" in result

    @patch("fruityloops_mcp.flapi_bridge.patterns")
    def test_patterns_get_length_success(self, mock_patterns):
        """Test successful patterns_get_length."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_patterns.getPatternLength.return_value = 16
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.patterns_get_length(0)
            assert "16" in result

    @patch("fruityloops_mcp.flapi_bridge.patterns")
    def test_patterns_jump_to_success(self, mock_patterns):
        """Test successful patterns_jump_to."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.patterns_jump_to(2)
            assert "2" in result


class TestFLStudioBridgePlaylistMethods:
    """Test FLStudioBridge playlist control methods."""

    @patch("fruityloops_mcp.flapi_bridge.playlist")
    def test_playlist_get_track_name_success(self, mock_playlist):
        """Test successful playlist_get_track_name."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_playlist.getTrackName.return_value = "Lead"
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.playlist_get_track_name(0)
            assert "Lead" in result

    @patch("fruityloops_mcp.flapi_bridge.playlist")
    def test_playlist_set_track_name_success(self, mock_playlist):
        """Test successful playlist_set_track_name."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.playlist_set_track_name(0, "Bass")
            assert "Bass" in result


class TestFLStudioBridgeGeneralMethods:
    """Test FLStudioBridge general control methods."""

    @patch("fruityloops_mcp.flapi_bridge.general")
    def test_general_get_version_success(self, mock_general):
        """Test successful general_get_version."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_general.getVersion.return_value = "21.0.0"
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.general_get_version()
            assert "21.0.0" in result

    @patch("fruityloops_mcp.flapi_bridge.general")
    def test_general_get_project_title_success(self, mock_general):
        """Test successful general_get_project_title."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_general.getProjectTitle.return_value = "My Song"
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.general_get_project_title()
            assert "My Song" in result

    @patch("fruityloops_mcp.flapi_bridge.general")
    def test_general_get_project_title_fallback(self, mock_general):
        """Test general_get_project_title with AttributeError fallback."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_general.getProjectTitle.side_effect = AttributeError("Not found")
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.general_get_project_title()
            assert "Unknown" in result

    @patch("fruityloops_mcp.flapi_bridge.general")
    def test_general_save_project_success(self, mock_general):
        """Test successful general_save_project."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.general_save_project()
            assert "saved" in result

    @patch("fruityloops_mcp.flapi_bridge.general")
    def test_general_undo_success(self, mock_general):
        """Test successful general_undo."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.general_undo()
            assert "Undo" in result


class TestFLStudioBridgeUIMethods:
    """Test FLStudioBridge UI control methods."""

    @patch("fruityloops_mcp.flapi_bridge.ui")
    def test_ui_show_window_success(self, mock_ui):
        """Test successful ui_show_window."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.ui_show_window(0)
            assert "0" in result
            mock_ui.showWindow.assert_called_once_with(0)

    @patch("fruityloops_mcp.flapi_bridge.ui")
    def test_ui_get_visible_success(self, mock_ui):
        """Test successful ui_get_visible."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_ui.getVisible.return_value = True
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.ui_get_visible(0)
            assert "True" in result


class TestGetBridge:
    """Test get_bridge function."""

    def test_get_bridge_returns_singleton(self):
        """Test that get_bridge returns the same instance."""
        # Reset global bridge for clean test
        import fruityloops_mcp.flapi_bridge as fb

        fb._bridge = None

        bridge1 = fb.get_bridge()
        bridge2 = fb.get_bridge()
        assert bridge1 is bridge2

    def test_get_bridge_creates_instance(self):
        """Test that get_bridge creates instance if none exists."""
        import fruityloops_mcp.flapi_bridge as fb

        fb._bridge = None
        bridge = fb.get_bridge()
        assert bridge is not None
        assert isinstance(bridge, fb.FLStudioBridge)


class TestFLStudioBridgeErrorPaths:
    """Test error paths for all methods."""

    @patch("fruityloops_mcp.flapi_bridge.transport")
    def test_transport_stop_exception(self, mock_transport):
        """Test transport_stop handles exception."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_transport.stop.side_effect = Exception("Error")
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.transport_stop()
            assert "Error" in result

    @patch("fruityloops_mcp.flapi_bridge.transport")
    def test_transport_record_exception(self, mock_transport):
        """Test transport_record handles exception."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_transport.record.side_effect = Exception("Error")
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.transport_record()
            assert "Error" in result

    @patch("fruityloops_mcp.flapi_bridge.mixer")
    def test_mixer_mute_track_exception(self, mock_mixer):
        """Test mixer_mute_track handles exception."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_mixer.muteTrack.side_effect = Exception("Error")
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.mixer_mute_track(1, True)
            assert "Error" in result

    @patch("fruityloops_mcp.flapi_bridge.channels")
    def test_channels_count_exception(self, mock_channels):
        """Test channels_count handles exception."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_channels.channelCount.side_effect = Exception("Error")
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.channels_count()
            assert "Error" in result

    @patch("fruityloops_mcp.flapi_bridge.patterns")
    def test_patterns_count_exception(self, mock_patterns):
        """Test patterns_count handles exception."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_patterns.patternCount.side_effect = Exception("Error")
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.patterns_count()
            assert "Error" in result

    @patch("fruityloops_mcp.flapi_bridge.ui")
    def test_ui_show_window_exception(self, mock_ui):
        """Test ui_show_window handles exception."""
        from fruityloops_mcp.flapi_bridge import FLStudioBridge

        mock_ui.showWindow.side_effect = Exception("Error")
        with patch.object(FLStudioBridge, "_ensure_enabled", return_value=True):
            bridge = FLStudioBridge()
            result = bridge.ui_show_window(0)
            assert "Error" in result
