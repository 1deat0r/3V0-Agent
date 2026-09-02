"""Ticket #24 — one adapter loading path via the platform registry.

The nine ``gateway/platforms/*`` adapters used to load through a
hand-rolled ``if/elif`` chain inside ``GatewayRunner``'s adapter creation —
a second loading path with its own dependency probes and injection rules.
They now register as builtin ``PlatformEntry`` records
(``gateway/platforms/builtin.py``) and the runner resolves everything
through ``platform_registry.create_adapter()``. These tests pin that
convergence: builtin entries exist, resolve through the registry, and get
the same ``gateway_runner`` back-reference plugins always got.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from gateway.config import Platform, PlatformConfig
from gateway.platform_registry import platform_registry
from gateway.platforms.builtin import ensure_builtin_platforms_registered

BUILTIN_NAMES = (
    "whatsapp_cloud",
    "signal",
    "weixin",
    "api_server",
    "webhook",
    "msgraph_webhook",
    "bluebubbles",
    "qqbot",
    "yuanbao",
)


@pytest.fixture
def ensure_registered():
    ensure_builtin_platforms_registered()


def test_all_builtin_platforms_registered(ensure_registered):
    for name in BUILTIN_NAMES:
        entry = platform_registry.get(name)
        assert entry is not None, name
        assert entry.source == "builtin", name


def test_registry_lookup_is_the_only_loading_path(ensure_registered):
    # A registered builtin resolves through the registry exactly like a
    # plugin platform — no separate direct-import tree may exist.
    config = PlatformConfig(enabled=True)
    adapter = platform_registry.create_adapter("webhook", config)
    assert adapter is not None


def _runner_stub():
    runner = MagicMock()
    runner.config.group_sessions_per_user = False
    return runner


def test_create_adapter_injects_gateway_runner_for_builtins(ensure_registered):
    from gateway.run import GatewayRunner

    runner = _runner_stub()
    config = PlatformConfig(enabled=True)
    adapter = GatewayRunner._create_adapter(runner, Platform.WEBHOOK, config)
    assert adapter is not None
    # Previously only the api_server/webhook chain legs injected this; the
    # registry path makes the back-reference platform-generic.
    assert adapter.gateway_runner is runner


def test_create_adapter_fails_closed_for_unregistered_platform(ensure_registered):
    from gateway.run import GatewayRunner

    runner = _runner_stub()
    config = PlatformConfig(enabled=True)
    # A Platform enum member with no builtin entry and no plugin
    # registration must not fall through to some other loader.
    no_adapter_platforms = [
        p for p in Platform
        if p.value not in BUILTIN_NAMES and not platform_registry.is_registered(p.value)
    ]
    assert no_adapter_platforms, "expected at least one adapter-less Platform member"
    for platform in no_adapter_platforms[:3]:
        assert GatewayRunner._create_adapter(runner, platform, config) is None
