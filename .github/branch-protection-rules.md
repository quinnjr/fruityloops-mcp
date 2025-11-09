## Branch Protection Rules

Recommended branch protection settings for this repository.

### Main/Master Branch

Navigate to: `Settings` → `Branches` → `Add rule` for `main`/`master`

#### Required Settings

- ✅ **Require a pull request before merging**
  - ✅ Require approvals: **1**
  - ✅ Dismiss stale pull request approvals when new commits are pushed
  - ✅ Require review from Code Owners

- ✅ **Require status checks to pass before merging**
  - ✅ Require branches to be up to date before merging
  - **Required status checks:**
    - `test (ubuntu-latest, 3.12)`
    - `test (windows-latest, 3.12)`
    - `test (macos-latest, 3.12)`
    - `build`
    - `validate-branch-name`
    - `validate-pr-title`
    - `enforce-git-flow`

- ✅ **Require conversation resolution before merging**

- ✅ **Require signed commits** (optional but recommended)

- ✅ **Require linear history** (optional)

- ✅ **Do not allow bypassing the above settings**

- ✅ **Restrict who can push to matching branches**
  - Add: GitHub Actions (for automated releases)
  - Add: Repository admins only

#### Optional but Recommended

- ✅ **Require deployments to succeed before merging**
- ✅ **Lock branch** (for additional protection)

### Develop Branch

Navigate to: `Settings` → `Branches` → `Add rule` for `develop`

#### Required Settings

- ✅ **Require a pull request before merging**
  - ✅ Require approvals: **1**
  - ✅ Dismiss stale pull request approvals when new commits are pushed

- ✅ **Require status checks to pass before merging**
  - ✅ Require branches to be up to date before merging
  - **Required status checks:**
    - `test (ubuntu-latest, 3.12)`
    - `build`
    - `validate-branch-name`
    - `enforce-git-flow`

- ✅ **Require conversation resolution before merging**

- ✅ **Do not allow bypassing the above settings**

### Release Branches

Navigate to: `Settings` → `Branches` → `Add rule` for `release/*`

#### Required Settings

- ✅ **Require a pull request before merging**
  - ✅ Require approvals: **2**

- ✅ **Require status checks to pass before merging**
  - All tests must pass
  - Coverage checks must pass

- ✅ **Require conversation resolution before merging**

## Rulesets (Alternative Approach)

GitHub's newer "Rulesets" feature provides more flexible branch protection.

### Create Ruleset

Navigate to: `Settings` → `Rules` → `Rulesets` → `New ruleset`

#### Ruleset: Protected Branches

**Target branches:**
- Include: `main`, `master`, `develop`

**Rules:**
- ✅ Restrict deletions
- ✅ Restrict force pushes
- ✅ Require pull request before merging
  - Required approvals: 1
  - Dismiss stale reviews: Yes
- ✅ Require status checks
  - Status checks: (list all CI jobs)
- ✅ Require signed commits
- ✅ Block force pushes

**Bypass list:**
- None (or GitHub Actions for automation)

## Status Check Configuration

The following CI jobs should be configured as required status checks:

### Required for All PRs

1. **Test Suite**
   - `test (ubuntu-latest, 3.10)`
   - `test (ubuntu-latest, 3.11)`
   - `test (ubuntu-latest, 3.12)`
   - `test (ubuntu-latest, 3.13)`
   - `test (windows-latest, 3.12)`
   - `test (macos-latest, 3.12)`

2. **Build**
   - `build`

3. **Linting**
   - Runs as part of test job

4. **Branch Validation**
   - `validate-branch-name`
   - `validate-pr-title`

5. **Merge Rules**
   - `enforce-git-flow`

### Required for Production Merges (main/master)

6. **Coverage Check**
   - `coverage-check`

7. **Security Scan**
   - `CodeQL`

## Setting Up Status Checks

1. Make initial PRs to trigger workflows
2. Once workflows run, they appear in branch protection settings
3. Select required workflows from the list
4. Save branch protection rules

## Verification

After configuration, test with a PR:

```bash
# Create test branch
git checkout -b feature/test-branch-protection

# Make a small change
echo "# Test" >> README.md

# Commit and push
git add README.md
git commit -m "test: verify branch protection"
git push origin feature/test-branch-protection

# Create PR via GitHub UI
# Verify:
# - Cannot merge without approval
# - Cannot merge without passing checks
# - Cannot force push to protected branches
```

## Troubleshooting

### Status Checks Not Appearing

- Ensure workflows have run at least once
- Check workflow triggers include pull_request events
- Verify workflow names match exactly

### Admins Can Bypass Protection

- Disable "Allow administrators to bypass" in branch protection settings
- Use rulesets for stricter enforcement

### Force Push Blocked

- This is expected for protected branches
- Use `git pull --rebase` and regular push instead
- Or create a new branch with corrected history

## Additional Security

### CODEOWNERS File

Create `.github/CODEOWNERS`:

```
# Global owners
* @quinnjr

# Workflows require admin approval
/.github/workflows/ @quinnjr

# Documentation
/docs/ @quinnjr
*.md @quinnjr
```

### Required Workflows

Configure required workflows in Settings → Actions → General

- Select workflows that must pass for all PRs
- Cannot be bypassed even by admins

## References

- [GitHub Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [GitHub Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets)
- [Status Checks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/about-status-checks)

