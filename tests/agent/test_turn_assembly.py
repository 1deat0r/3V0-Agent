"""Contract tests for the shared turn-assembly frame (ticket #18).

The three turn runners (cli, gateway, tui) build their per-turn ``AIAgent``
kwargs from the same ``config.yaml`` decisions. ``agent/turn_assembly.py``
owns those derivations once; these tests pin the contract each runner
depends on.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

REPO_ROOT = str(Path(__file__).resolve().parents[2])
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from agent.turn_assembly import (  # noqa: E402
    checkpoint_agent_kwargs,
    provider_routing_kwargs,
    service_tier_from_cfg,
    service_tier_from_raw,
)


class TestProviderRoutingKwargs:
    def test_maps_only_ignore_order_sort(self):
        kwargs = provider_routing_kwargs({
            "only": ["openrouter/a"],
            "ignore": ["openrouter/b"],
            "order": ["openrouter/a", "openrouter/b"],
            "sort": "price",
        })
        assert kwargs == {
            "providers_allowed": ["openrouter/a"],
            "providers_ignored": ["openrouter/b"],
            "providers_order": ["openrouter/a", "openrouter/b"],
            "provider_sort": "price",
            "provider_require_parameters": False,
            "provider_data_collection": None,
        }

    def test_require_parameters_and_data_collection_pass_through(self):
        kwargs = provider_routing_kwargs({
            "require_parameters": True,
            "data_collection": "deny",
        })
        assert kwargs["provider_require_parameters"] is True
        assert kwargs["provider_data_collection"] == "deny"

    def test_none_and_empty_section_yield_defaults(self):
        empty = provider_routing_kwargs(None)
        assert empty == provider_routing_kwargs({})
        assert empty["providers_allowed"] is None
        assert empty["provider_require_parameters"] is False


class TestServiceTier:
    def test_priority_aliases(self):
        for raw in ("fast", "priority", "on", " PRIORITY "):
            assert service_tier_from_raw(raw) == "priority", raw

    def test_neutral_values_are_none(self):
        for raw in ("", None, "normal", "default", "standard", "off", "none"):
            assert service_tier_from_raw(raw) is None, raw

    def test_unknown_warns_and_is_none(self, caplog):
        with caplog.at_level(logging.WARNING):
            assert service_tier_from_raw("turbo") is None
        assert any("turbo" in r.message for r in caplog.records)

    def test_from_cfg_reads_agent_section(self):
        assert service_tier_from_cfg({"agent": {"service_tier": "fast"}}) == "priority"
        assert service_tier_from_cfg({}) is None
        assert service_tier_from_cfg(None) is None


class TestCheckpointKwargs:
    def test_dict_section_overrides_defaults(self):
        kwargs = checkpoint_agent_kwargs({
            "checkpoints": {
                "enabled": True,
                "max_snapshots": 9,
                "max_total_size_mb": 500,
                "max_file_size_mb": 50,
            }
        })
        assert kwargs == {
            "checkpoints_enabled": True,
            "checkpoint_max_snapshots": 9,
            "checkpoint_max_total_size_mb": 500,
            "checkpoint_max_file_size_mb": 50,
        }

    def test_legacy_bool_shape(self):
        assert checkpoint_agent_kwargs({"checkpoints": True})["checkpoints_enabled"] is True
        assert checkpoint_agent_kwargs({"checkpoints": False})["checkpoints_enabled"] is False

    def test_defaults_apply_when_section_missing(self):
        kwargs = checkpoint_agent_kwargs({})
        # Defaults come from DEFAULT_CONFIG["checkpoints"] — assert the
        # relationship, not the literal values (change-detector rule).
        assert isinstance(kwargs["checkpoints_enabled"], bool)
        assert isinstance(kwargs["checkpoint_max_snapshots"], int)
        assert kwargs["checkpoint_max_snapshots"] >= 1

    def test_non_dict_config_is_tolerated(self):
        kwargs = checkpoint_agent_kwargs(None)
        assert set(kwargs) == {
            "checkpoints_enabled", "checkpoint_max_snapshots",
            "checkpoint_max_total_size_mb", "checkpoint_max_file_size_mb",
        }
