# name=FL Studio Bridge
# url=https://github.com/quinnjr/fruityloops-mcp
# supportedDevices=FL Studio Bridge

r"""
FL Studio Bridge Script - MCP Integration

This script runs inside FL Studio's Python environment and acts as a bridge
between the external MCP server and FL Studio's Python API.

Installation:
1. Copy this file to: <User Data Folder>/Settings/Hardware/
2. In FL Studio: Options -> MIDI Settings
3. Find "FL Studio Bridge" in the controller list
4. Enable it
5. The bridge server will start automatically

Usage:
- Automatically starts socket server on port 25100
- MCP server connects and sends commands
- Commands execute using FL Studio's API
- Results returned to MCP server
"""

import contextlib
import json
import socket
import threading
import time

# Import FL Studio API modules
try:
    import channels
    import general
    import mixer
    import patterns
    import playlist
    import transport
    import ui

    FL_STUDIO_AVAILABLE = True
    print("FL Studio Bridge: FL Studio API modules loaded successfully")
except ImportError:
    FL_STUDIO_AVAILABLE = False
    print("FL Studio Bridge: ERROR - FL Studio API modules not available!")
    print("Make sure this script is running inside FL Studio!")

# Configuration
HOST = "127.0.0.1"
PORT = 25100
BUFFER_SIZE = 4096


class FLStudioBridge:
    """Bridge between external MCP server and FL Studio's Python API."""

    def __init__(self):
        """Initialize the bridge."""
        self.server_socket = None
        self.running = False
        self.server_thread = None

    def start(self):
        """Start the bridge server."""
        if not FL_STUDIO_AVAILABLE:
            print("FL Studio Bridge: Cannot start - FL Studio API not available")
            return False

        if self.running:
            print("FL Studio Bridge: Already running")
            return True

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen(1)
            self.running = True

            # Start server in a separate thread
            self.server_thread = threading.Thread(target=self._server_loop, daemon=True)
            self.server_thread.start()

            print(f"FL Studio Bridge: Server started on {HOST}:{PORT}")
            return True
        except Exception as e:
            print(f"FL Studio Bridge: Failed to start server - {e}")
            return False

    def stop(self):
        """Stop the bridge server."""
        self.running = False
        if self.server_socket:
            with contextlib.suppress(Exception):
                self.server_socket.close()
        print("FL Studio Bridge: Server stopped")

    def _server_loop(self):
        """Main server loop - handles client connections."""
        print("FL Studio Bridge: Waiting for connections...")

        while self.running:
            try:
                # Accept connection with timeout
                self.server_socket.settimeout(1.0)
                try:
                    client_socket, address = self.server_socket.accept()
                    print(f"FL Studio Bridge: Client connected from {address}")
                except TimeoutError:
                    continue

                # Handle client
                self._handle_client(client_socket)

            except Exception as e:
                if self.running:
                    print(f"FL Studio Bridge: Server error - {e}")
                break

    def _handle_client(self, client_socket):
        """Handle a client connection."""
        try:
            client_socket.settimeout(30.0)

            while self.running:
                # Receive command
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break

                try:
                    # Parse command
                    command = json.loads(data.decode("utf-8"))
                    print(f"FL Studio Bridge: Received command - {command.get('action')}")

                    # Execute command
                    result = self._execute_command(command)

                    # Send response
                    response = json.dumps(result)
                    client_socket.sendall(response.encode("utf-8"))

                except json.JSONDecodeError:
                    error_response = json.dumps({"error": "Invalid JSON"})
                    client_socket.sendall(error_response.encode("utf-8"))
                except Exception as e:
                    error_response = json.dumps({"error": str(e)})
                    client_socket.sendall(error_response.encode("utf-8"))

        except Exception as e:
            print(f"FL Studio Bridge: Client handler error - {e}")
        finally:
            client_socket.close()
            print("FL Studio Bridge: Client disconnected")

    def _execute_command(self, command):
        """Execute a FL Studio API command."""
        action = command.get("action")
        params = command.get("params", {})

        try:
            # Transport commands
            if action == "transport.start":
                transport.start()
                return {"success": True, "result": "Started"}
            elif action == "transport.stop":
                transport.stop()
                return {"success": True, "result": "Stopped"}
            elif action == "transport.record":
                transport.record()
                return {"success": True, "result": "Recording toggled"}
            elif action == "transport.getSongPos":
                pos = transport.getSongPos(0)  # 0 = absolute position
                return {"success": True, "result": pos}
            elif action == "transport.setSongPos":
                transport.setSongPos(params.get("position", 0), 0)
                return {"success": True, "result": "Position set"}

            # Mixer commands
            elif action == "mixer.getTrackVolume":
                vol = mixer.getTrackVolume(params.get("track"))
                return {"success": True, "result": vol}
            elif action == "mixer.setTrackVolume":
                mixer.setTrackVolume(params.get("track"), params.get("volume"))
                return {"success": True, "result": "Volume set"}
            elif action == "mixer.getTrackName":
                name = mixer.getTrackName(params.get("track"))
                return {"success": True, "result": name}
            elif action == "mixer.setTrackName":
                mixer.setTrackName(params.get("track"), params.get("name"))
                return {"success": True, "result": "Name set"}

            # Channels commands
            elif action == "channels.channelCount":
                count = channels.channelCount()
                return {"success": True, "result": count}
            elif action == "channels.getChannelName":
                name = channels.getChannelName(params.get("channel"))
                return {"success": True, "result": name}
            elif action == "channels.setChannelVolume":
                channels.setChannelVolume(params.get("channel"), params.get("volume"))
                return {"success": True, "result": "Volume set"}
            elif action == "channels.muteChannel":
                channels.muteChannel(params.get("channel"), params.get("mute", 1))
                return {"success": True, "result": "Mute toggled"}

            # Patterns commands
            elif action == "patterns.patternCount":
                count = patterns.patternCount()
                return {"success": True, "result": count}
            elif action == "patterns.getPatternName":
                name = patterns.getPatternName(params.get("pattern"))
                return {"success": True, "result": name}
            elif action == "patterns.setPatternName":
                patterns.setPatternName(params.get("pattern"), params.get("name"))
                return {"success": True, "result": "Name set"}

            # General commands
            elif action == "general.getVersion":
                version = general.getVersion()
                return {"success": True, "result": version}
            elif action == "general.getProjectTitle":
                title = general.getProjectTitle()
                return {"success": True, "result": title}

            # UI commands
            elif action == "ui.showWindow":
                ui.showWindow(params.get("window"))
                return {"success": True, "result": "Window shown"}

            # Playlist commands
            elif action == "playlist.getTrackName":
                name = playlist.getTrackName(params.get("track"))
                return {"success": True, "result": name}

            # Ping command for testing connection
            elif action == "ping":
                return {"success": True, "result": "pong"}

            else:
                return {"success": False, "error": f"Unknown action: {action}"}

        except Exception as e:
            return {"success": False, "error": str(e)}


# Global bridge instance
_bridge = FLStudioBridge()


def OnInit():
    """Called when FL Studio loads the script."""
    print("=" * 60)
    print("FL Studio Bridge Script - Initializing")
    print("=" * 60)
    _bridge.start()


def OnDeInit():
    """Called when FL Studio unloads the script."""
    print("FL Studio Bridge Script - Shutting down")
    _bridge.stop()


def OnIdle():
    """Called regularly by FL Studio."""
    # Keep the script alive
    pass


def OnMidiIn(event):
    """Called when MIDI input is received."""
    # We don't need to handle MIDI events in this bridge
    pass


# For testing outside FL Studio
if __name__ == "__main__":
    print("FL Studio Bridge - Test Mode")
    print("Note: This should be run inside FL Studio for full functionality")

    if FL_STUDIO_AVAILABLE:
        print("FL Studio API is available")
        bridge = FLStudioBridge()
        bridge.start()

        try:
            print("Press Ctrl+C to stop")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping...")
            bridge.stop()
    else:
        print("FL Studio API is NOT available - run this inside FL Studio")
