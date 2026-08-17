from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))
sys.path.insert(0, str(REPO_ROOT / "3v0" / "core"))

from core.insights import (  # noqa: E402
    aux_routing,
    burn_outliers,
    cache_health,
    compression_health,
    detect,
    memory_health,
    model_mix_findings,
    tool_reliability,
)


def _tool(name, count, rate, p95):
    return {"name": name, "count": count, "success_rate": rate,
            "failure": 0, "unknown": 0, "latency_p95_ms": p95}


class TestToolReliability(unittest.TestCase):
    def test_low_success_flagged(self):
        report = {"tools": [_tool("patch", 50, 0.66, 100.0)]}
        out = tool_reliability(report)
        self.assertTrue(any(f["category"] == "tool_reliability" for f in out))

    def test_low_count_not_flagged(self):
        report = {"tools": [_tool("rare", 5, 0.10, 100.0)]}
        self.assertEqual(tool_reliability(report), [])

    def test_high_latency_flagged(self):
        report = {"tools": [_tool("terminal", 200, 0.99, 12000.0)]}
        out = tool_reliability(report)
        self.assertTrue(any(f["category"] == "tool_latency" for f in out))

    def test_long_running_tool_latency_not_flagged(self):
        # process/browser_exec/delegate_task are wall-clock waits, not defects
        report = {"tools": [_tool("process", 200, 0.99, 180000.0)]}
        self.assertEqual(tool_reliability(report), [])

    def test_long_running_tool_still_checks_success(self):
        # the latency carve-out must NOT hide a genuine reliability problem
        report = {"tools": [_tool("process", 200, 0.66, 180000.0)]}
        out = tool_reliability(report)
        self.assertTrue(any(f["category"] == "tool_reliability" for f in out))

    def test_healthy_tool_not_flagged(self):
        report = {"tools": [_tool("read_file", 100, 0.99, 200.0)]}
        self.assertEqual(tool_reliability(report), [])


class TestCacheHealth(unittest.TestCase):
    def test_low_ratio_flagged(self):
        report = {"totals": {"cache_hit_ratio": 0.75}}
        out = cache_health(report)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["category"], "cache")
        self.assertEqual(out[0]["severity"], "high")

    def test_healthy_ratio_not_flagged(self):
        report = {"totals": {"cache_hit_ratio": 0.98}}
        self.assertEqual(cache_health(report), [])

    def test_no_ratio_not_flagged(self):
        self.assertEqual(cache_health({"totals": {}}), [])


class TestAuxRouting(unittest.TestCase):
    def test_aux_on_primary_flagged(self):
        report = {"tasks": [{"task": "compression", "model": "deepseek-v4-pro",
                             "estimated_cost_usd": 0.09}]}
        out = aux_routing(report)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["category"], "aux_routing")

    def test_aux_on_flash_ok(self):
        report = {"tasks": [{"task": "compression", "model": "deepseek-v4-flash",
                             "estimated_cost_usd": 0.01}]}
        self.assertEqual(aux_routing(report), [])

    def test_main_task_not_flagged(self):
        report = {"tasks": [{"task": "main", "model": "deepseek-v4-pro",
                             "estimated_cost_usd": 1.0}]}
        self.assertEqual(aux_routing(report), [])

    def test_zero_cost_aux_not_flagged(self):
        report = {"tasks": [{"task": "compression", "model": "deepseek-v4-pro",
                             "estimated_cost_usd": 0.0}]}
        self.assertEqual(aux_routing(report), [])


class TestBurnOutliers(unittest.TestCase):
    def test_over_cap_flagged(self):
        report = {"daily": [{"date": "2026-08-15", "estimated_cost_usd": 6.42, "tool_calls": 100}]}
        out = burn_outliers(report)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["category"], "burn")

    def test_under_cap_not_flagged(self):
        report = {"daily": [{"date": "2026-08-15", "estimated_cost_usd": 0.84, "tool_calls": 10}]}
        self.assertEqual(burn_outliers(report), [])


class TestModelMix(unittest.TestCase):
    def test_unintended_model_flagged(self):
        report = {"models": [{"model": "gpt-4o", "estimated_cost_usd": 2.0, "api_calls": 10}]}
        out = model_mix_findings(report)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["category"], "model_mix")

    def test_flash_aux_not_flagged(self):
        # deepseek-v4-flash is the policy-mandated aux model — not a violation
        report = {"models": [{"model": "deepseek-v4-flash", "estimated_cost_usd": 2.0, "api_calls": 10}]}
        self.assertEqual(model_mix_findings(report), [])

    def test_primary_not_flagged(self):
        report = {"models": [{"model": "deepseek-v4-pro", "estimated_cost_usd": 2.0, "api_calls": 10}]}
        self.assertEqual(model_mix_findings(report), [])

    def test_cheap_unintended_not_flagged(self):
        report = {"models": [{"model": "gpt-4o", "estimated_cost_usd": 0.01, "api_calls": 10}]}
        self.assertEqual(model_mix_findings(report), [])


class TestMemoryHealth(unittest.TestCase):
    def test_low_memory_success(self):
        report = {"tools": [_tool("memory", 50, 0.66, 100.0)]}
        out = memory_health(report)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["category"], "memory_health")

    def test_healthy_memory(self):
        report = {"tools": [_tool("memory", 50, 0.99, 100.0)]}
        self.assertEqual(memory_health(report), [])


class TestCompressionHealth(unittest.TestCase):
    def test_failures_flagged(self):
        report = {"health": {"compression_failure_errors": 3}}
        self.assertEqual(len(compression_health(report)), 1)

    def test_no_failures(self):
        report = {"health": {"compression_failure_errors": 0}}
        self.assertEqual(compression_health(report), [])


class TestDetect(unittest.TestCase):
    def test_ranking_high_before_low(self):
        report = {
            "tools": [_tool("memory", 50, 0.66, 100.0),
                      _tool("terminal", 200, 0.99, 12000.0)],
            "models": [{"model": "claude-3-opus", "estimated_cost_usd": 2.0, "api_calls": 10}],
            "daily": [],
            "health": {"compression_failure_errors": 0},
        }
        out = detect(report)
        sev = [f["severity"] for f in out]
        # 'high' findings must precede 'medium'/'low'
        self.assertTrue(sev.index("high") < sev.index("medium"))
        self.assertTrue(sev.index("medium") < sev.index("low"))

    def test_memory_not_double_flagged(self):
        report = {
            "tools": [_tool("memory", 50, 0.66, 100.0)],
            "models": [], "daily": [], "health": {},
        }
        out = detect(report)
        memory_findings = [f for f in out if "memory" in f["message"].lower()]
        self.assertEqual(len(memory_findings), 1)

    def test_empty_report_no_findings(self):
        self.assertEqual(detect({"tools": [], "models": [], "daily": [], "health": {}}), [])


if __name__ == "__main__":
    unittest.main()
