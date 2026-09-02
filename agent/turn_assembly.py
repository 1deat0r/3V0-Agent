"""Turn-agent assembly — shared derivations for the three turn runners.

The classic CLI (``cli.py``), the messaging gateway (``gateway/run.py``),
and the TUI/desktop backend (``tui_gateway/server.py``) each build an
``AIAgent`` per turn from the same ``config.yaml`` decisions. This module
owns those shared derivations as pure functions over the loaded config;
each runner layers its surface-specific policy (agent cache, callbacks,
session binding) on top.

Owned here (previously hand-copied across the runners — ticket #18):

- :func:`provider_routing_kwargs` — the OpenRouter ``provider_routing``
  section → ``AIAgent`` constructor kwargs (gateway ×2, TUI, CLI).
- :func:`service_tier_from_raw` / :func:`service_tier_from_cfg` — the
  ``agent.service_tier`` normalization (gateway + TUI carried identical
  copies; the CLI an equivalent parser).
- :func:`checkpoint_agent_kwargs` — the ``checkpoints:`` section →
  constructor args (moved from ``gateway/run.py``; the gateway reads raw
  YAML, so the ``DEFAULT_CONFIG`` defaults live with the transform).

Not owned here (per-surface policy, deliberately): the gateway's
cached-vs-fresh agent decision (agent-cache signature, dead-session and
cross-process eviction guards), callback wiring, and session-state sync.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

_SERVICE_TIER_NEUTRAL = {"normal", "default", "standard", "off", "none"}
_SERVICE_TIER_PRIORITY = {"fast", "priority", "on"}


def provider_routing_kwargs(provider_routing: Optional[dict]) -> Dict[str, Any]:
    """Map the ``provider_routing`` config section onto AIAgent kwargs.

    Single home for the OpenRouter provider-routing transform that was
    hand-copied across the three turn runners. Unknown keys in the section
    are ignored; absent keys yield the constructor defaults.
    """
    pr = provider_routing or {}
    return {
        "providers_allowed": pr.get("only"),
        "providers_ignored": pr.get("ignore"),
        "providers_order": pr.get("order"),
        "provider_sort": pr.get("sort"),
        "provider_require_parameters": pr.get("require_parameters", False),
        "provider_data_collection": pr.get("data_collection"),
    }


def service_tier_from_raw(raw: Any) -> Optional[str]:
    """Normalize a persisted ``agent.service_tier`` preference.

    ``"fast"``/``"priority"``/``"on"`` → ``"priority"``; unset, neutral
    (``normal``/``default``/``standard``/``off``/``none``), or unknown →
    ``None`` (unknown values warn once here rather than in each runner).
    """
    value = str(raw or "").strip().lower()
    if not value or value in _SERVICE_TIER_NEUTRAL:
        return None
    if value in _SERVICE_TIER_PRIORITY:
        return "priority"
    logger.warning("Unknown service_tier '%s', ignoring", raw)
    return None


def service_tier_from_cfg(cfg: Optional[dict]) -> Optional[str]:
    """:func:`service_tier_from_raw` over ``cfg["agent"]["service_tier"]``."""
    agent = (cfg or {}).get("agent") or {}
    return service_tier_from_raw(agent.get("service_tier", ""))


def checkpoint_agent_kwargs(config: Optional[dict]) -> Dict[str, Any]:
    """Translate the ``checkpoints:`` config section into AIAgent args.

    Callers that read raw YAML (the gateway) don't go through
    ``load_config()``, so the ``DEFAULT_CONFIG`` checkpoint defaults must be
    supplied here. Legacy ``checkpoints: true`` shapes keep working.
    """
    cp_cfg = config.get("checkpoints", {}) if isinstance(config, dict) else {}
    if isinstance(cp_cfg, bool):
        cp_cfg = {"enabled": cp_cfg}
    elif not isinstance(cp_cfg, dict):
        cp_cfg = {}

    from threev0_cli.config import DEFAULT_CONFIG

    defaults = DEFAULT_CONFIG["checkpoints"]
    return {
        "checkpoints_enabled": cp_cfg.get("enabled", defaults["enabled"]),
        "checkpoint_max_snapshots": cp_cfg.get(
            "max_snapshots", defaults["max_snapshots"],
        ),
        "checkpoint_max_total_size_mb": cp_cfg.get(
            "max_total_size_mb", defaults["max_total_size_mb"],
        ),
        "checkpoint_max_file_size_mb": cp_cfg.get(
            "max_file_size_mb", defaults["max_file_size_mb"],
        ),
    }
