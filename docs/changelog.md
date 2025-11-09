# Changelog

All notable changes to FL Studio MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-09

### Added

- Initial release of FL Studio MCP Server
- FL Studio Python API integration
  - Transport controls (play, stop, record, position)
  - Mixer controls (volume, track naming)
  - Channel controls (volume, mute)
  - Pattern controls (count, naming)
  - Project information (title, version)
  - UI controls (window management)
  - Playlist controls (track names)
- MIDI integration via mido
  - Connect/disconnect to MIDI ports
  - Send notes with duration
  - Manual note on/off
  - Control change messages
  - Program changes
  - Pitch bend
- MCP protocol implementation
  - Stdio transport
  - Tool listing
  - Tool execution
  - Error handling
- Comprehensive testing
  - 94% code coverage
  - Unit tests
  - Integration tests
  - Edge case tests
  - Antipattern tests
- Complete documentation
  - Installation guide
  - Quick start guide
  - Usage examples
  - API reference
  - Development guide
- Development tools
  - Git hooks for code quality
  - GitHub Actions CI/CD
  - Docker test environment
  - Linting with Ruff
  - Type hints throughout
- GitHub automation
  - Automated testing on multiple OS/Python versions
  - Security scanning with CodeQL
  - Branch protection workflows
  - PR quality checks
  - Coverage tracking
  - Automatic documentation deployment
  - Automated releases to PyPI

### Changed

- N/A (initial release)

### Deprecated

- N/A (initial release)

### Removed

- N/A (initial release)

### Fixed

- N/A (initial release)

### Security

- N/A (initial release)

## [Unreleased]

### Planned

- Additional FL Studio API coverage
- More MIDI message types
- Enhanced error handling
- Performance optimizations
- Additional examples and tutorials

---

[1.0.0]: https://github.com/quinnjr/fruityloops-mcp/releases/tag/v1.0.0
[Unreleased]: https://github.com/quinnjr/fruityloops-mcp/compare/v1.0.0...HEAD

