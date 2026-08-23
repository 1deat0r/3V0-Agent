"""ENV-FUNNEL bridge: prod ``env_compat`` loads the native-core resolver.

The bridge must expose the REAL chain contract (3V0_* first, legacy EV0_*
second, first truthy wins) — and it must be the native core's own function,
not a copy (the whole point of ticket #19/#20's single-source-of-truth).
"""

import os

import env_compat


def _scrub(monkeypatch):
    for k in ("3V0_BRIDGE_PROBE", "EV0_BRIDGE_PROBE"):
        monkeypatch.delenv(k, raising=False)


def test_canonical_wins_over_legacy_through_bridge(monkeypatch):
    _scrub(monkeypatch)
    monkeypatch.setenv("3V0_BRIDGE_PROBE", "canonical")
    monkeypatch.setenv("EV0_BRIDGE_PROBE", "legacy")
    assert env_compat.branded_env("BRIDGE_PROBE") == "canonical"


def test_legacy_fallback_through_bridge(monkeypatch):
    _scrub(monkeypatch)
    monkeypatch.setenv("EV0_BRIDGE_PROBE", "legacy")
    assert env_compat.branded_env("BRIDGE_PROBE") == "legacy"


def test_default_passthrough_when_unset(monkeypatch):
    _scrub(monkeypatch)
    assert env_compat.branded_env("BRIDGE_PROBE", "dflt") == "dflt"
    assert env_compat.branded_env("BRIDGE_PROBE") is None


def test_empty_canonical_falls_through_to_legacy(monkeypatch):
    _scrub(monkeypatch)
    monkeypatch.setenv("3V0_BRIDGE_PROBE", "")
    monkeypatch.setenv("EV0_BRIDGE_PROBE", "legacy")
    assert env_compat.branded_env("BRIDGE_PROBE") == "legacy"


def test_bridge_is_the_native_core_function_not_a_copy():
    # Loaded by path from 3v0/core/env_compat.py under its spec name —
    # if this ever regresses to a duplicated implementation, drift between
    # the native core and the prod funnel becomes possible again.
    assert env_compat.branded_env.__module__ == "_threev0_core_env_compat"
