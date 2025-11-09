# Install git hooks for FL Studio MCP Server (PowerShell)

Write-Host "Installing git hooks..." -ForegroundColor Cyan

try {
    # Configure git to use .githooks directory
    git config core.hooksPath .githooks

    Write-Host "[OK] Git hooks installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Installed hooks:" -ForegroundColor Yellow
    Write-Host "  - commit-msg: Enforce Conventional Commits"
    Write-Host "  - pre-commit: Run linting and formatting"
    Write-Host "  - pre-push: Enforce git-flow and run tests"
    Write-Host "  - prepare-commit-msg: Help with commit messages"
    Write-Host ""
    Write-Host "To uninstall: git config --unset core.hooksPath" -ForegroundColor Gray

    exit 0
}
catch {
    Write-Host "[ERROR] Failed to install git hooks: $_" -ForegroundColor Red
    exit 1
}

