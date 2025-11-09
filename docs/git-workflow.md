# Git Workflow

Git workflow and branching strategy for FL Studio MCP Server.

## Overview

We use git-flow with Conventional Commits.

## Branch Types

### Main Branches

- `main` - Production code
- `develop` - Development integration

### Supporting Branches

- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Production fixes
- `release/*` - Release preparation

## Creating Branches

### Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/add-new-tool
```

### Bugfix Branch

```bash
git checkout develop
git pull origin develop
git checkout -b bugfix/fix-connection-issue
```

### Hotfix Branch

```bash
git checkout main
git pull origin main
git checkout -b hotfix/critical-security-fix
```

## Commit Messages

### Format

```
type(scope): description

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance
- `perf`: Performance
- `ci`: CI/CD

### Examples

```bash
git commit -m "feat: add pitch bend support"
git commit -m "fix(midi): resolve connection timeout"
git commit -m "docs: update installation guide"
git commit -m "test: add edge case tests"
```

## Merging Strategy

### Feature → Develop

```bash
# From feature branch
git push origin feature/my-feature
# Create PR to develop on GitHub
```

### Bugfix → Develop

```bash
# From bugfix branch
git push origin bugfix/my-fix
# Create PR to develop on GitHub
```

### Hotfix → Main

```bash
# From hotfix branch
git push origin hotfix/critical-fix
# Create PR to main on GitHub
# Then merge back to develop
```

### Release → Main + Develop

```bash
# From release branch
git push origin release/v1.1.0
# Create PR to main on GitHub
# Then merge to develop
```

## Git Hooks

### Install Hooks

```bash
./install-hooks.sh  # Unix/Linux/macOS
./install-hooks.ps1  # Windows
```

### Hooks

- `commit-msg` - Validates commit format
- `pre-commit` - Runs linter/formatter
- `pre-push` - Validates branch and runs tests
- `prepare-commit-msg` - Helps format messages

## Pull Requests

### PR Title

Must follow Conventional Commits:

```
feat: add new MIDI tool
fix(server): resolve timeout
docs: update README
```

### PR Description

Use the template, include:

- Description of changes
- Related issues
- Testing performed
- Breaking changes (if any)

### PR Review

- At least 1 approval required
- All CI checks must pass
- Coverage must not decrease

## Protected Branches

### Main/Master

- No direct pushes
- Requires PR
- Requires passing CI
- Requires approval

### Develop

- No direct pushes
- Requires PR
- Requires passing CI

## Release Process

### Version Bumping

```bash
# Update version in:
# - pyproject.toml
# - src/fruityloops_mcp/__init__.py

git add pyproject.toml src/fruityloops_mcp/__init__.py
git commit -m "chore: bump version to 1.1.0"
```

### Creating Release

```bash
# Create and push tag
git tag v1.1.0
git push origin v1.1.0

# GitHub Actions will:
# - Build package
# - Create GitHub release
# - Publish to PyPI
```

## Common Workflows

### Starting New Feature

```bash
git checkout develop
git pull origin develop
git checkout -b feature/my-feature
# Make changes
git add .
git commit -m "feat: add my feature"
git push origin feature/my-feature
# Create PR on GitHub
```

### Fixing a Bug

```bash
git checkout develop
git pull origin develop
git checkout -b bugfix/fix-issue
# Fix bug
git add .
git commit -m "fix: resolve issue"
git push origin bugfix/fix-issue
# Create PR on GitHub
```

### Hot-fixing Production

```bash
git checkout main
git pull origin main
git checkout -b hotfix/critical-fix
# Fix critical issue
git add .
git commit -m "fix: critical security issue"
git push origin hotfix/critical-fix
# Create PR to main
# After merge, backport to develop
```

## Tips

### Keeping Up to Date

```bash
# Update your branch with develop
git checkout feature/my-feature
git fetch origin
git rebase origin/develop
```

### Resolving Conflicts

```bash
# If conflicts during rebase
git status  # See conflicted files
# Edit files to resolve
git add <resolved-files>
git rebase --continue
```

### Amending Commits

```bash
# Fix last commit
git add <files>
git commit --amend --no-edit
git push --force-with-lease
```

## Resources

- [Git-flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

