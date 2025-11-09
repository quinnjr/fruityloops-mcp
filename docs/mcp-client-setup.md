# MCP Client Setup

Guide to configuring MCP clients to use FL Studio MCP Server.

## Claude Desktop

### Configuration File Location

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Basic Configuration

```json
{
  "mcpServers": {
    "fruityloops": {
      "command": "uvx",
      "args": ["fruityloops-mcp"]
    }
  }
}
```

### Using uv

```json
{
  "mcpServers": {
    "fruityloops": {
      "command": "uv",
      "args": ["tool", "run", "fruityloops-mcp"]
    }
  }
}
```

### From Source

```json
{
  "mcpServers": {
    "fruityloops": {
      "command": "uv",
      "args": ["run", "fruityloops-mcp"],
      "cwd": "/path/to/fruityloops-mcp"
    }
  }
}
```

### Reloading Configuration

After editing the configuration:

1. Quit Claude Desktop completely
2. Relaunch Claude Desktop
3. The server will start automatically

## Other MCP Clients

The server uses stdio transport and works with any MCP-compatible client.

### Generic Configuration

```json
{
  "command": "uvx fruityloops-mcp",
  "transport": "stdio"
}
```

## Verification

Test the server is working:

1. Open your MCP client
2. Try a simple command:
   ```python
   midi_list_ports()
   ```
3. You should see available MIDI ports listed

## Troubleshooting

### Server Not Starting

Check Claude Desktop logs:

- **Windows**: `%APPDATA%\Claude\logs\`
- **macOS**: `~/Library/Logs/Claude/`
- **Linux**: `~/.local/share/Claude/logs/`

### Command Not Found

Ensure uvx/uv is in PATH:

```bash
which uvx  # Unix
where uvx  # Windows
```

## Next Steps

- [Quick Start](quick-start.md)
- [Usage Guide](usage.md)

