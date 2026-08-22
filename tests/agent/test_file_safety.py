"""Tests for agent/file_safety.py read guards — env file blocking.

Run with:  python -m pytest tests/agent/test_file_safety.py -v
"""

import os
from unittest.mock import patch

import pytest

from agent.file_safety import (
    _BLOCKED_PROJECT_ENV_BASENAMES,
    get_read_block_error,
)


# ---------------------------------------------------------------------------
# Project-local .env file blocking (issue #20734)
# ---------------------------------------------------------------------------


class TestEnvFileReadBlocking:
    """Secret-bearing .env files must be blocked by get_read_block_error."""

    @pytest.mark.parametrize("basename", [
        ".env",
        ".env.local",
        ".env.development",
        ".env.production",
        ".env.test",
        ".env.staging",
        ".envrc",
    ])
    def test_blocked_env_basenames(self, basename):
        """All secret-bearing .env basenames are blocked regardless of directory."""
        path = f"/tmp/project/{basename}"
        error = get_read_block_error(path)
        assert error is not None, f"{basename} should be blocked"
        assert "Access denied" in error
        assert "secret-bearing" in error.lower() or "environment file" in error.lower()


    @pytest.mark.parametrize("basename", [
        ".ENV",
        ".Env.Local",
        ".ENV.PRODUCTION",
        ".ENVRC",
    ])
    def test_blocked_env_basenames_case_insensitive(self, basename):
        """Secret-bearing .env basenames are blocked regardless of case."""
        error = get_read_block_error(f"/tmp/project/{basename}")
        assert error is not None, f"{basename} should be blocked"
        assert "Access denied" in error
        assert "environment file" in error.lower()


    def test_allowed_env_example(self):
        """"The .env.example file is explicitly allowed — it's documentation, not a secret."""
        error = get_read_block_error("/tmp/project/.env.example")
        assert error is None






# ---------------------------------------------------------------------------
# Existing cache-file blocking (regression — must still work)
# ---------------------------------------------------------------------------


class TestCacheFileReadBlocking:
    """Internal 3V0 cache files must remain blocked."""

    def test_hub_index_cache_blocked(self, tmp_path):
        """Hub index-cache reads are blocked."""
        threev0_home = tmp_path / ".3V0"
        cache = threev0_home / "skills" / ".hub" / "index-cache" / "data.json"
        cache.parent.mkdir(parents=True)
        cache.write_text("{}")

        with patch("agent.file_safety._threev0_home_path", return_value=threev0_home):
            error = get_read_block_error(str(cache))
            assert error is not None
            assert "internal 3V0 cache" in error

    def test_hub_directory_blocked(self, tmp_path):
        """Hub directory reads are blocked."""
        threev0_home = tmp_path / ".3V0"
        hub = threev0_home / "skills" / ".hub" / "metadata.json"
        hub.parent.mkdir(parents=True)
        hub.write_text("{}")

        with patch("agent.file_safety._threev0_home_path", return_value=threev0_home):
            error = get_read_block_error(str(hub))
            assert error is not None


# ---------------------------------------------------------------------------
# Combined: env guard + cache guard don't interfere
# ---------------------------------------------------------------------------


class TestCombinedGuards:
    """Both guards should work independently without interference."""

    def test_env_guard_works_regardless_of_threev0_home(self, tmp_path):
        """The env basename guard does not depend on EV0_HOME resolution."""
        threev0_home = tmp_path / ".3V0"
        threev0_home.mkdir()

        with patch("agent.file_safety._threev0_home_path", return_value=threev0_home):
            # Regular project .env should still be blocked
            error = get_read_block_error("/workspace/.env")
            assert error is not None

            # .env.example should still be allowed
            error = get_read_block_error("/workspace/.env.example")
            assert error is None

    def test_cache_guard_still_works_with_env_guard(self, tmp_path):
        """Cache file blocking still works when env guard is active."""
        threev0_home = tmp_path / ".3V0"
        cache = threev0_home / "skills" / ".hub" / "index-cache" / "x"
        cache.parent.mkdir(parents=True)
        cache.write_text("")

        with patch("agent.file_safety._threev0_home_path", return_value=threev0_home):
            error = get_read_block_error(str(cache))
            assert error is not None
            assert "internal 3V0 cache" in error


class TestCredentialStoreClassifier:
    """is_credential_store_path is the single source of credential-store
    shapes. It feeds both get_read_block_error (per-location) and the
    reference-expansion guard (home-spelled) — a shape added here must be
    recognized everywhere so the #86213 drift class can't return."""

    def test_classifies_credential_files(self):
        from agent.file_safety import is_credential_store_path

        for name in (
            "auth.json",
            "auth.lock",
            ".anthropic_oauth.json",
            "webhook_subscriptions.json",
        ):
            assert is_credential_store_path(f"/any/.3v0/{name}")
            assert is_credential_store_path(f"/home/user/.3V0/{name}")

    def test_classifies_mcp_tokens_dir(self):
        from agent.file_safety import is_credential_store_path

        assert is_credential_store_path("/tmp/x/mcp-tokens/github.json")
        assert is_credential_store_path("/tmp/x/.3v0/mcp-tokens/github.json")

    def test_classifies_auth_google_oauth_path(self):
        from agent.file_safety import is_credential_store_path

        assert is_credential_store_path("/home/user/.3V0/auth/google_oauth.json")

    def test_does_not_classify_arbitrary_project_files(self):
        from agent.file_safety import is_credential_store_path

        # A project-local auth.json IS credential-shaped (the classifier is
        # shape-only); the per-location decision (allowed outside home/root)
        # is get_read_block_error's job. Only non-credential files are not
        # classified at all.
        assert not is_credential_store_path("/home/user/.ssh/config")
        assert not is_credential_store_path("/tmp/project/README.md")
        assert not is_credential_store_path("/workspace/src/main.py")
