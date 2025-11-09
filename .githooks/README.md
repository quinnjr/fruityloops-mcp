# Git Hooks

This directory contains custom git hooks for the FL Studio MCP Server project.

## Available Hooks

### commit-msg

**Purpose**: Enforce Conventional Commits format

**Checks**:
- Commit message follows pattern: `type(scope): description`
- Valid types: feat, fix, docs, style, refactor, test, chore, perf, ci, build

**Example**:
```bash
✓ feat: add MIDI support
✓ fix(server): resolve connection issue
✗ Added new feature  # Invalid format
```

### pre-commit

**Purpose**: Run code quality checks before committing

**Checks**:
- Ruff linting (`ruff check .`)
- Ruff formatting (`ruff format --check .`)

**Skip**: Set `SKIP_PRECOMMIT=1` to bypass (not recommended)

### pre-push

**Purpose**: Enforce git-flow workflow and prevent direct pushes to protected branches

**Checks**:
- Prevent direct pushes to `main`, `master`, or `develop`
- Validate branch name follows git-flow conventions
- Run tests before pushing

**Valid branch names**:
- `feature/*`
- `bugfix/*`
- `hotfix/*`
- `release/*`

### prepare-commit-msg

**Purpose**: Help format commit messages

**Features**:
- Adds commit message template for conventional commits
- Extracts issue number from branch name if present

## Installation

### Automatic Installation

Run the installation script for your OS:

**Unix/Linux/macOS**:
```bash
./install-hooks.sh
```

**Windows (PowerShell)**:
```powershell
.\install-hooks.ps1
```

### Manual Installation

Configure git to use this hooks directory:

```bash
git config core.hooksPath .githooks
```

Make hooks executable (Unix/Linux/macOS):
```bash
chmod +x .githooks/*
```

## Uninstalling

To disable custom hooks:

```bash
git config --unset core.hooksPath
```

Git will revert to using `.git/hooks/` directory.

## Bypassing Hooks

### Skip All Hooks

```bash
git commit --no-verify -m "message"
git push --no-verify
```

**⚠️ Warning**: Only bypass hooks when absolutely necessary. CI will still enforce these rules.

### Skip Specific Checks

Set environment variables:

```bash
# Skip pre-commit linting
SKIP_PRECOMMIT=1 git commit -m "message"

# Skip pre-push tests
SKIP_TESTS=1 git push
```

## Troubleshooting

### Hooks Not Running

**Issue**: Hooks aren't being executed

**Solution**:
```bash
# Check hooks path
git config core.hooksPath

# Should show: .githooks

# If not set, run install script again
./install-hooks.sh  # or install-hooks.ps1 on Windows
```

### Permission Denied (Unix/Linux/macOS)

**Issue**: `Permission denied` when executing hooks

**Solution**:
```bash
# Make hooks executable
chmod +x .githooks/*
```

### Commit Message Rejected

**Issue**: Valid commit message is being rejected

**Solution**:
```bash
# Check your commit message format
# Must be: type(scope): description

# Valid examples:
git commit -m "feat: add new feature"
git commit -m "fix(api): resolve bug"
git commit -m "docs: update README"

# Invalid examples:
git commit -m "Added feature"  # Missing type
git commit -m "feat add feature"  # Missing colon
```

### Pre-commit Failing on Linting

**Issue**: Linting errors prevent commit

**Solution**:
```bash
# Auto-fix linting issues
uv run ruff check --fix .

# Format code
uv run ruff format .

# Try commit again
git commit
```

### Pre-push Blocking Protected Branch

**Issue**: Cannot push to main/develop

**Solution**:
```bash
# This is intentional! Create a feature branch:
git checkout -b feature/my-feature
git push origin feature/my-feature

# Then create a Pull Request on GitHub
```

### Hooks Failing in CI/CD

**Issue**: Hooks work locally but fail in CI

**Solution**:
- Hooks are client-side only
- CI uses GitHub Actions workflows (`.github/workflows/`)
- Ensure your code passes both hooks and CI checks

## Development

### Testing Hooks

Test hooks without committing:

```bash
# Test commit-msg hook
echo "test: commit message" | .githooks/commit-msg /dev/stdin

# Test pre-commit hook
.githooks/pre-commit

# Test pre-push hook
.githooks/pre-push
```

### Modifying Hooks

1. Edit hook files in `.githooks/`
2. Test changes locally
3. Commit hook changes
4. Other developers run `./install-hooks.sh` to update

## Best Practices

1. **Always install hooks** when cloning the repository
2. **Don't bypass hooks** without good reason
3. **Keep hooks fast** - slow hooks frustrate developers
4. **Test hooks locally** before pushing changes
5. **Document new hooks** in this README

## Resources

- [Git Hooks Documentation](https://git-scm.com/docs/githooks)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git-flow Workflow](https://nvie.com/posts/a-successful-git-branching-model/)

## Support

If hooks are causing issues, reach out:
- [Open an issue](https://github.com/quinnjr/fruityloops-mcp/issues)
- [Discussions](https://github.com/quinnjr/fruityloops-mcp/discussions)

