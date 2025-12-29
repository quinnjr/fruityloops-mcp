# FL Studio Bridge Setup Guide

The FL Studio Bridge connects the external MCP server to FL Studio's internal Python environment, enabling full API access.

## How It Works

```
┌─────────────────┐        Socket        ┌──────────────────┐
│   MCP Server    │ ◄─────────────────► │  FL Studio       │
│   (External)    │   Port 25100         │  Bridge Script   │
│                 │                      │  (Inside FL)     │
└─────────────────┘                      └──────────────────┘
                                                   │
                                                   ▼
                                         ┌──────────────────┐
                                         │  FL Studio API   │
                                         │  (transport,     │
                                         │   mixer, etc)    │
                                         └──────────────────┘
```

## Installation Steps

### 1. Locate FL Studio's MIDI Scripts Folder

The location depends on your FL Studio installation:

**Default location:**
```
C:\Users\<YourUsername>\Documents\Image-Line\FL Studio\Settings\Hardware\
```

**Alternative locations:**
- Check FL Studio: Options → File Settings → "Browser extra search folders"
- Look in: `%USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware\`

If the folder doesn't exist, create it.

### 2. Copy the Bridge Script

Copy `device_fl_studio_bridge.py` to the Hardware folder:

**Important:** The script MUST be named with the `device_` prefix for FL Studio to recognize it!

```powershell
# From your project directory
Copy-Item "F:\Projects\fruityloops-mcp\device_fl_studio_bridge.py" `
  "C:\Users\<YourUsername>\Documents\Image-Line\FL Studio\Settings\Hardware\"
```

### 3. Configure FL Studio

1. **Open FL Studio**

2. **Open MIDI Settings:**
   - Go to: `Options` → `MIDI Settings` (or press `F10`)

3. **Add the Bridge Script:**
   - In the "Input" section, scroll through the list
   - Look for: `FL Studio Bridge` (should appear automatically after restart)
   - Make sure the "Enable" checkbox is **checked** ✓
   - The script will start automatically when enabled

4. **Apply Settings:**
   - Click "Apply" or just close the window
   - FL Studio will load the script

### 4. Verify Bridge is Running

Check the FL Studio console output (if visible) or logs. You should see:

```
============================================================
FL Studio Bridge Script - Initializing
============================================================
FL Studio Bridge: FL Studio API modules loaded successfully
FL Studio Bridge: Server started on 127.0.0.1:25100
FL Studio Bridge: Waiting for connections...
```

### 5. Restart Cursor

After the bridge is loaded in FL Studio:

1. **Completely quit Cursor**
2. **Restart Cursor**
3. The MCP server will now connect to the bridge automatically

## Testing the Connection

After setup, test the FL Studio API connection:

### Test 1: Check FL Studio Version

Ask Cursor:
```
"What version of FL Studio is running?"
```

Expected response:
```
FL Studio version: 21
```
(or your FL Studio version number)

### Test 2: Get Channel Count

Ask Cursor:
```
"How many channels are in my FL Studio project?"
```

### Test 3: Control Transport

Ask Cursor:
```
"Start FL Studio playback"
```

FL Studio should start playing!

## Troubleshooting

### Bridge Script Not Loading

**Symptoms:**
- Script doesn't appear in FL Studio MIDI Settings as "FL Studio Bridge"
- No console output from bridge

**Solutions:**
1. **Check file location and naming:**
   ```powershell
   Test-Path "C:\Users\<YourUsername>\Documents\Image-Line\FL Studio\Settings\Hardware\device_fl_studio_bridge.py"
   ```
   **Critical:** The filename MUST start with `device_` for FL Studio to recognize it!

2. **Verify file permissions:**
   - Right-click `device_fl_studio_bridge.py` → Properties
   - Make sure it's not blocked (Unblock if needed)

3. **Check FL Studio version:**
   - Requires FL Studio 20.8 or later for Python 3 support

4. **Restart FL Studio:**
   - Completely quit and reopen FL Studio

### Bridge Server Not Starting

**Symptoms:**
- Script loads but no "Server started" message
- Connection errors in MCP logs

**Solutions:**
1. **Check port availability:**
   ```powershell
   netstat -an | findstr "25100"
   ```
   - If port is in use, close the application using it

2. **Check Windows Firewall:**
   - Allow Python/FL Studio through firewall for local connections

3. **View FL Studio Console:**
   - In FL Studio: Help → Check for Updates → View log
   - Look for Python errors

### MCP Server Can't Connect

**Symptoms:**
- "FL Studio Bridge not available" errors
- Connection timeout

**Solutions:**
1. **Verify bridge is running in FL Studio:**
   - Check MIDI Settings → Script should be enabled
   - Look for console output

2. **Test connection manually:**
   ```powershell
   Test-NetConnection -ComputerName 127.0.0.1 -Port 25100
   ```

3. **Restart both applications:**
   - Close Cursor completely
   - Close FL Studio completely
   - Start FL Studio first
   - Then start Cursor

### Commands Not Working

**Symptoms:**
- Bridge connects but commands fail
- Error responses from API calls

**Solutions:**
1. **Check FL Studio project:**
   - Make sure a project is loaded
   - Some commands require content (channels, patterns, etc.)

2. **Try simple commands first:**
   - `general_get_version` (always works)
   - `transport_get_song_pos` (works with any project)

3. **Check bridge logs:**
   - View FL Studio console for error messages
   - Look for Python exceptions

## Advanced Configuration

### Change Bridge Port

Edit `fl_studio_bridge.py`:

```python
# Configuration
HOST = '127.0.0.1'
PORT = 25100  # Change this to your desired port
```

Also update the MCP server in `fl_bridge_client.py`:

```python
def __init__(self, host: str = '127.0.0.1', port: int = 25100):  # Match the port
```

### Enable Debug Logging

Edit `fl_studio_bridge.py` and add more print statements:

```python
def _execute_command(self, command):
    action = command.get('action')
    print(f"DEBUG: Executing {action} with params {command.get('params')}")
    # ... rest of method
```

### Multiple FL Studio Instances

If running multiple FL Studio instances, use different ports:

```python
# Instance 1
PORT = 25100

# Instance 2
PORT = 25101
```

## Uninstalling

1. **Remove from FL Studio:**
   - Options → MIDI Settings
   - Disable/remove `FL Studio Bridge` entry

2. **Delete bridge script:**
   ```powershell
   Remove-Item "C:\Users\<YourUsername>\Documents\Image-Line\FL Studio\Settings\Hardware\device_fl_studio_bridge.py"
   ```

3. **Restart FL Studio**

## Performance Notes

- **Low Overhead:** Bridge uses minimal CPU when idle
- **Command Latency:** ~1-5ms for most API calls
- **No Audio Impact:** Bridge doesn't affect audio processing
- **Thread-Safe:** Uses separate thread for socket communication

## Security Notes

- **Local Only:** Bridge only accepts connections from localhost (127.0.0.1)
- **No Authentication:** Bridge doesn't require authentication (local use only)
- **Single Client:** Only one MCP server can connect at a time
- **Auto-Reconnect:** MCP server reconnects automatically if connection drops

## Next Steps

- [Usage Examples](USAGE_EXAMPLES.md)
- [FL Studio API Documentation](docs/fl-studio-integration.md)
- [MIDI Integration](docs/midi-integration.md)

## Support

If you encounter issues:

1. Check FL Studio console for error messages
2. Check Cursor logs for connection errors
3. Try the troubleshooting steps above
4. Open an issue on GitHub with:
   - FL Studio version
   - Python version (in FL Studio)
   - Bridge console output
   - Error messages

