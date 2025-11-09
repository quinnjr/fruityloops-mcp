"""Tests for git hooks validation logic."""


class TestBranchNameValidation:
    """Test branch name validation."""

    def test_valid_feature_branch(self):
        """Test valid feature branch names."""
        valid_branches = [
            "feature/add-midi-support",
            "feature/123-add-feature",
            "feature/user-auth",
        ]
        for branch in valid_branches:
            assert self._is_valid_branch(branch)

    def test_valid_bugfix_branch(self):
        """Test valid bugfix branch names."""
        valid_branches = [
            "bugfix/fix-memory-leak",
            "bugfix/123-fix-crash",
            "bugfix/error-handling",
        ]
        for branch in valid_branches:
            assert self._is_valid_branch(branch)

    def test_valid_hotfix_branch(self):
        """Test valid hotfix branch names."""
        valid_branches = [
            "hotfix/security-patch",
            "hotfix/123-critical-fix",
            "hotfix/prod-issue",
        ]
        for branch in valid_branches:
            assert self._is_valid_branch(branch)

    def test_valid_release_branch(self):
        """Test valid release branch names."""
        valid_branches = [
            "release/1.0.0",
            "release/v2.1.3",
            "release/2024-Q1",
        ]
        for branch in valid_branches:
            assert self._is_valid_branch(branch)

    def test_protected_branches(self):
        """Test that protected branches are allowed."""
        protected_branches = ["main", "master", "develop"]
        for branch in protected_branches:
            assert self._is_valid_branch(branch)

    def test_invalid_branch_names(self):
        """Test invalid branch names."""
        invalid_branches = [
            "random-branch",
            "feat/something",  # Should be "feature"
            "fix/something",  # Should be "bugfix"
            "feature",  # Missing slash
            "feature/",  # Empty name after slash
        ]
        for branch in invalid_branches:
            assert not self._is_valid_branch(branch)

    @staticmethod
    def _is_valid_branch(branch: str) -> bool:
        """Check if branch name is valid."""
        # Protected branches
        if branch in ["main", "master", "develop"]:
            return True

        # Valid prefixes
        valid_prefixes = ["feature/", "bugfix/", "hotfix/", "release/"]
        for prefix in valid_prefixes:
            if branch.startswith(prefix) and len(branch) > len(prefix):
                return True

        return False


class TestCommitMessageValidation:
    """Test commit message validation."""

    def test_valid_commit_types(self):
        """Test valid conventional commit types."""
        valid_commits = [
            "feat: add new feature",
            "fix: resolve bug",
            "docs: update documentation",
            "style: format code",
            "refactor: restructure code",
            "test: add tests",
            "chore: update dependencies",
            "perf: improve performance",
            "ci: update CI configuration",
            "build: update build system",
        ]
        for commit in valid_commits:
            assert self._is_valid_commit_message(commit)

    def test_valid_commit_with_scope(self):
        """Test commits with scope."""
        valid_commits = [
            "feat(api): add endpoint",
            "fix(server): resolve crash",
            "docs(readme): update install section",
        ]
        for commit in valid_commits:
            assert self._is_valid_commit_message(commit)

    def test_valid_commit_with_breaking_change(self):
        """Test commits with breaking change indicator."""
        valid_commits = [
            "feat!: breaking API change",
            "feat(api)!: remove endpoint",
        ]
        for commit in valid_commits:
            assert self._is_valid_commit_message(commit)

    def test_invalid_commit_messages(self):
        """Test invalid commit messages."""
        invalid_commits = [
            "random commit message",
            "Fix: wrong case",
            "feat add feature",  # Missing colon
            "feat:",  # No description
            "feat: ",  # Empty description
            "invalid: type not recognized",
        ]
        for commit in invalid_commits:
            assert not self._is_valid_commit_message(commit)

    @staticmethod
    def _is_valid_commit_message(message: str) -> bool:
        """Check if commit message follows conventional commits."""
        import re

        pattern = (
            r"^(feat|fix|docs|style|refactor|test|chore|perf|ci|build)(\([a-z0-9-]+\))?!?: .+$"
        )
        return bool(re.match(pattern, message))


class TestGitFlowRules:
    """Test git-flow workflow rules."""

    def test_feature_branch_merges_to_develop(self):
        """Test that feature branches should merge to develop."""
        assert self._can_merge_to("feature/test", "develop")
        assert not self._can_merge_to("feature/test", "main")
        assert not self._can_merge_to("feature/test", "master")

    def test_bugfix_branch_merges_to_develop(self):
        """Test that bugfix branches should merge to develop."""
        assert self._can_merge_to("bugfix/test", "develop")
        assert not self._can_merge_to("bugfix/test", "main")
        assert not self._can_merge_to("bugfix/test", "master")

    def test_hotfix_branch_merges_to_main(self):
        """Test that hotfix branches should merge to main/master."""
        assert self._can_merge_to("hotfix/test", "main")
        assert self._can_merge_to("hotfix/test", "master")
        assert not self._can_merge_to("hotfix/test", "develop")

    def test_release_branch_merges(self):
        """Test that release branches can merge to main/master or develop."""
        assert self._can_merge_to("release/1.0.0", "main")
        assert self._can_merge_to("release/1.0.0", "master")
        assert self._can_merge_to("release/1.0.0", "develop")

    def test_direct_push_to_protected_branches_blocked(self):
        """Test that direct pushes to protected branches should be blocked."""
        protected_branches = ["main", "master", "develop"]
        for branch in protected_branches:
            assert not self._can_direct_push(branch)

    @staticmethod
    def _can_merge_to(source_branch: str, target_branch: str) -> bool:
        """Check if source branch can merge to target branch."""
        if source_branch.startswith("feature/") or source_branch.startswith("bugfix/"):
            return target_branch == "develop"
        elif source_branch.startswith("hotfix/"):
            return target_branch in ["main", "master"]
        elif source_branch.startswith("release/"):
            return target_branch in ["main", "master", "develop"]
        return False

    @staticmethod
    def _can_direct_push(branch: str) -> bool:
        """Check if direct push is allowed to branch."""
        protected_branches = ["main", "master", "develop"]
        return branch not in protected_branches
