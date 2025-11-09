# Release Process

Proper git-flow release process for FL Studio MCP Server.

## Overview

This document outlines the correct release process following git-flow conventions.

## Release Workflow

### 1. Create Release Branch

Create a release branch from `develop` when ready to release:

```bash
git checkout develop
git pull origin develop
git checkout -b release/vX.Y.Z
```

### 2. Prepare Release

On the release branch, make final preparations:

#### Update Version Numbers

```bash
# Update pyproject.toml
[project]
version = "X.Y.Z"

# Update src/fruityloops_mcp/__init__.py
__version__ = "X.Y.Z"
```

#### Update Changelog

Edit `docs/changelog.md`:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing features

### Fixed
- Bug fixes
```

#### Run Final Tests

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

#### Commit Changes

```bash
git add pyproject.toml src/fruityloops_mcp/__init__.py docs/changelog.md
git commit -m "chore: prepare release vX.Y.Z"
```

### 3. Push Release Branch

```bash
git push origin release/vX.Y.Z
```

### 4. Create Pull Request to Main

1. Go to GitHub: https://github.com/quinnjr/fruityloops-mcp/pulls
2. Create PR: `release/vX.Y.Z` → `main`
3. Title: `Release vX.Y.Z`
4. Wait for CI checks to pass
5. Get approval (if required)
6. **Merge the PR** (use merge commit, not squash or rebase)

### 5. Tag the Release

After merging to main:

```bash
git checkout main
git pull origin main
git tag -a vX.Y.Z -m "Release vX.Y.Z

Features:
- Feature 1
- Feature 2

Changes:
- Change 1
- Change 2

Fixes:
- Fix 1
- Fix 2
"
git push origin vX.Y.Z
```

This will trigger the release workflow which will:
- Build the package
- Create a GitHub release
- Publish to PyPI

### 6. Merge Back to Develop

Create PR: `release/vX.Y.Z` → `develop` or:

```bash
git checkout develop
git pull origin develop
git merge release/vX.Y.Z
git push origin develop
```

### 7. Clean Up

Delete the release branch:

```bash
git branch -d release/vX.Y.Z
git push origin --delete release/vX.Y.Z
```

## Hotfix Workflow

For critical production fixes:

### 1. Create Hotfix Branch

```bash
git checkout main
git pull origin main
git checkout -b hotfix/vX.Y.Z
```

### 2. Fix the Issue

Make the necessary fixes:

```bash
git add .
git commit -m "fix: critical issue description"
```

### 3. Update Version

```bash
# Bump patch version in pyproject.toml and __init__.py
git add pyproject.toml src/fruityloops_mcp/__init__.py
git commit -m "chore: bump version to X.Y.Z"
```

### 4. Push and Create PR to Main

```bash
git push origin hotfix/vX.Y.Z
```

Create PR: `hotfix/vX.Y.Z` → `main`

### 5. Tag After Merge

```bash
git checkout main
git pull origin main
git tag -a vX.Y.Z -m "Hotfix vX.Y.Z

Critical fix for [issue description]
"
git push origin vX.Y.Z
```

### 6. Merge to Develop

```bash
git checkout develop
git pull origin develop
git merge hotfix/vX.Y.Z
git push origin develop
```

### 7. Clean Up

```bash
git branch -d hotfix/vX.Y.Z
git push origin --delete hotfix/vX.Y.Z
```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **Major (X.0.0)**: Breaking changes
- **Minor (x.Y.0)**: New features, backward compatible
- **Patch (x.y.Z)**: Bug fixes, backward compatible

## Release Checklist

Before creating a release:

- [ ] All tests pass
- [ ] Code coverage maintained/improved
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version numbers updated
- [ ] No open critical issues
- [ ] CI/CD checks pass

## GitHub Release Automation

The `.github/workflows/release.yml` workflow automatically:

1. **Builds** the package with `uv build`
2. **Creates** a GitHub release with:
   - Auto-generated release notes
   - Built wheel and source distribution
3. **Publishes** to PyPI (requires `PYPI_API_TOKEN` secret)

## PyPI Setup

To enable automatic PyPI publishing:

1. Create a PyPI API token at https://pypi.org/manage/account/token/
2. Add it as a GitHub secret named `PYPI_API_TOKEN`
3. Future releases will automatically publish to PyPI

## Troubleshooting

### Release Workflow Failed

Check the GitHub Actions logs:
https://github.com/quinnjr/fruityloops-mcp/actions/workflows/release.yml

Common issues:
- **PyPI token not set**: Add `PYPI_API_TOKEN` secret
- **Version already exists**: Bump version number
- **Tests failing**: Fix tests before releasing

### Tag Already Exists

Delete and recreate:

```bash
git tag -d vX.Y.Z
git push origin :refs/tags/vX.Y.Z
git tag -a vX.Y.Z -m "Release message"
git push origin vX.Y.Z
```

## Historical Note

**v1.0.0 Process**: The initial v1.0.0 release was tagged directly on main without a release branch. This document establishes the correct process for all future releases (v1.1.0 and beyond) to follow proper git-flow conventions.

## Resources

- [Git-flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

