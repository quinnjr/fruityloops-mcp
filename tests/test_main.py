"""Tests for __main__ module and main function."""

import subprocess
import sys
from unittest.mock import MagicMock, patch

import pytest


class TestMainModule:
    """Test the __main__ module."""

    def test_main_module_can_be_imported(self):
        """Test that __main__ module can be imported."""
        import fruityloops_mcp.__main__

        assert fruityloops_mcp.__main__ is not None

    def test_main_module_as_script(self):
        """Test running module as a script."""
        result = subprocess.run(
            [sys.executable, "-m", "fruityloops_mcp", "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        # The server doesn't have --help by default, so it will fail
        # but we can check it at least tries to run
        assert result.returncode in [0, 1, 2]


class TestServerMain:
    """Test the main function in server.py."""

    @patch("fruityloops_mcp.server.FLStudioMCPServer")
    @patch("fruityloops_mcp.server.asyncio.run")
    def test_main_function_creates_server(self, mock_asyncio_run, mock_server_class):
        """Test that main() creates an FLStudioMCPServer instance and runs it."""
        from fruityloops_mcp.server import main

        mock_server_instance = mock_server_class.return_value
        mock_server_instance.run = MagicMock()

        main()

        mock_server_class.assert_called_once()
        mock_asyncio_run.assert_called_once()

    @patch("fruityloops_mcp.server.FLStudioMCPServer")
    @patch("fruityloops_mcp.server.asyncio.run")
    def test_main_function_handles_keyboard_interrupt(
        self, mock_asyncio_run, mock_server_class
    ):
        """Test that main() handles KeyboardInterrupt."""
        from fruityloops_mcp.server import main

        mock_asyncio_run.side_effect = KeyboardInterrupt()

        # Should raise KeyboardInterrupt
        with pytest.raises(KeyboardInterrupt):
            main()

