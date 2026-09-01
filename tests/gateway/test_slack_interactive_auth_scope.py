"""Profile-scope coverage for the Slack interactive-authorization env reads.

``SlackAdapter._is_interactive_user_authorized``'s env-only fallback builds
its allowlist / allow-all verdict through a local ``_env`` helper. Under
``gateway.multiplex_profiles`` that read must follow the fail-closed secret
scope contract (AGENTS.md Profiles rule 7, #86905 class): a scope miss
returns the default — it must NOT borrow ``os.environ``, which under the
multiplexer holds the PRIMARY profile's values. A leaked primary allowlist
silently admits/denies the wrong users on a secondary profile.

Unscoped single-profile deployments keep the legacy ``os.environ`` behavior.
"""

from __future__ import annotations

import pytest

from agent import secret_scope as ss
from gateway.config import PlatformConfig
from plugins.platforms.slack.adapter import SlackAdapter


@pytest.fixture(autouse=True)
def _reset_scope_state(monkeypatch):
    for key in (
        "SLACK_ALLOWED_USERS",
        "SLACK_ALLOW_ALL_USERS",
        "GATEWAY_ALLOWED_USERS",
        "GATEWAY_ALLOW_ALL_USERS",
    ):
        monkeypatch.delenv(key, raising=False)
    ss.set_multiplex_active(False)
    yield
    ss.set_multiplex_active(False)


def _adapter() -> SlackAdapter:
    # No _message_handler → the auth check takes its env-only fallback path,
    # which is where the _env closure under test lives.
    a = SlackAdapter(PlatformConfig(enabled=True, token="xoxb-fake"))
    return a


class TestInteractiveAuthScope:
    def test_scope_does_not_inherit_environ_allowlist(self, monkeypatch):
        # PRIMARY profile's environ allowlists user-1; the secondary profile's
        # scope does not. user-1 must NOT be authorized on the secondary.
        monkeypatch.setenv("SLACK_ALLOWED_USERS", "user-1")
        a = _adapter()
        ss.set_multiplex_active(True)
        tok = ss.set_secret_scope({})
        try:
            assert a._is_interactive_user_authorized("user-1") is False
        finally:
            ss.reset_secret_scope(tok)

    def test_scoped_allowlist_authorizes_its_own_users(self, monkeypatch):
        # The secondary profile's own scope lists user-9 — it must win even
        # though os.environ lists somebody else.
        monkeypatch.setenv("SLACK_ALLOWED_USERS", "user-1")
        a = _adapter()
        ss.set_multiplex_active(True)
        tok = ss.set_secret_scope({"SLACK_ALLOWED_USERS": "user-9"})
        try:
            assert a._is_interactive_user_authorized("user-9") is True
            assert a._is_interactive_user_authorized("user-1") is False
        finally:
            ss.reset_secret_scope(tok)

    def test_scope_does_not_inherit_environ_allow_all(self, monkeypatch):
        monkeypatch.setenv("SLACK_ALLOW_ALL_USERS", "true")
        a = _adapter()
        ss.set_multiplex_active(True)
        tok = ss.set_secret_scope({})
        try:
            assert a._is_interactive_user_authorized("user-1") is False
        finally:
            ss.reset_secret_scope(tok)

    def test_single_profile_environ_unchanged(self, monkeypatch):
        # Multiplex inactive, no scope: legacy os.environ behavior preserved.
        monkeypatch.setenv("SLACK_ALLOWED_USERS", "user-1")
        a = _adapter()
        assert a._is_interactive_user_authorized("user-1") is True
        assert a._is_interactive_user_authorized("user-2") is False
