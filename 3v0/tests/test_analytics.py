from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))
sys.path.insert(0, str(REPO_ROOT / "3v0" / "core"))

from core.analytics import (  # noqa: E402
    aggregate_tools,
    classify_tool_result,
    daily_buckets,
    health,
    model_mix,
    session_totals,
    summarize,
)


class TestClassifyToolResult(unittest.TestCase):
    def test_success_json(self):
        self.assertEqual(classify_tool_result('{"success": true}'), "success")
        self.assertEqual(classify_tool_result('{"success": false}'), "failure")

    def test_exit_code(self):
        self.assertEqual(classify_tool_result('{"exit_code": 0, "output": "ok"}'), "success")
        self.assertEqual(classify_tool_result('{"exit_code": 1, "output": "boom"}'), "failure")

    def test_error_field(self):
        self.assertEqual(classify_tool_result('{"error": "no such file"}'), "failure")

    def test_embedded_content_not_failed(self):
        # regression: content-bearing tools must not be failed by the word
        # "error" appearing inside the content they returned
        self.assertEqual(
            classify_tool_result('{"content": "if err != nil: return error", "total_lines": 5}'),
            "success",
        )

    def test_leading_error_text(self):
        self.assertEqual(classify_tool_result("Traceback (most recent call last): ..."), "failure")
        self.assertEqual(classify_tool_result("Error: something broke"), "failure")
        self.assertEqual(classify_tool_result("connection refused"), "failure")

    def test_plain_text_no_error(self):
        self.assertEqual(classify_tool_result("plain output, nothing wrong"), "success")

    def test_unknown(self):
        self.assertEqual(classify_tool_result(None), "unknown")


class TestAggregateTools(unittest.TestCase):
    def test_counts_and_rate(self):
        events = [
            {"name": "terminal", "latency_ms": 100.0, "status": "success"},
            {"name": "terminal", "latency_ms": 200.0, "status": "success"},
            {"name": "terminal", "latency_ms": 300.0, "status": "failure"},
            {"name": "read_file", "latency_ms": 50.0, "status": "unknown"},
        ]
        out = aggregate_tools(events)
        by_name = {r["name"]: r for r in out}
        self.assertEqual(by_name["terminal"]["count"], 3)
        self.assertEqual(by_name["terminal"]["success"], 2)
        self.assertEqual(by_name["terminal"]["failure"], 1)
        self.assertEqual(by_name["terminal"]["success_rate"], round(2 / 3, 3))
        self.assertIsNone(by_name["read_file"]["success_rate"])

    def test_latency_percentiles(self):
        events = [{"name": "t", "latency_ms": float(i), "status": "success"} for i in range(1, 101)]
        r = aggregate_tools(events)[0]
        self.assertEqual(r["latency_median_ms"], 50.5)
        self.assertEqual(r["latency_p95_ms"], 95.0)
        self.assertEqual(r["latency_avg_ms"], 50.5)

    def test_sorted_by_count(self):
        events = [
            {"name": "rare", "latency_ms": None, "status": "unknown"},
            {"name": "common", "latency_ms": None, "status": "unknown"},
            {"name": "common", "latency_ms": None, "status": "unknown"},
        ]
        out = aggregate_tools(events)
        self.assertEqual(out[0]["name"], "common")


class TestSessionTotals(unittest.TestCase):
    def test_totals(self):
        sessions = [
            {"started_at": 1700000000, "message_count": 10, "tool_call_count": 5,
             "api_call_count": 3, "input_tokens": 100, "output_tokens": 50,
             "cache_read_tokens": 20, "reasoning_tokens": 5, "estimated_cost_usd": 0.1},
            {"started_at": 1700086400, "message_count": 20, "tool_call_count": 7,
             "api_call_count": 4, "input_tokens": 200, "output_tokens": 100,
             "cache_read_tokens": 30, "reasoning_tokens": 10, "estimated_cost_usd": 0.2},
        ]
        t = session_totals(sessions)
        self.assertEqual(t["sessions"], 2)
        self.assertEqual(t["messages"], 30)
        self.assertEqual(t["tool_calls"], 12)
        self.assertEqual(t["input_tokens"], 300)
        self.assertEqual(t["estimated_cost_usd"], 0.3)
        self.assertEqual(t["active_days"], 2)


class TestModelMix(unittest.TestCase):
    def test_aggregation(self):
        usage = [
            {"model": "deepseek-v4-pro", "api_call_count": 2, "input_tokens": 100,
             "output_tokens": 50, "estimated_cost_usd": 1.5},
            {"model": "deepseek-v4-flash", "api_call_count": 1, "input_tokens": 10,
             "output_tokens": 5, "estimated_cost_usd": 0.05},
        ]
        out = model_mix(usage)
        self.assertEqual(out[0]["model"], "deepseek-v4-pro")
        self.assertEqual(out[0]["estimated_cost_usd"], 1.5)


class TestDailyBuckets(unittest.TestCase):
    def test_bucketing(self):
        sessions = [
            {"started_at": 1700000000, "message_count": 1, "tool_call_count": 2,
             "input_tokens": 10, "output_tokens": 5, "estimated_cost_usd": 0.01},
            {"started_at": 1700000001, "message_count": 1, "tool_call_count": 3,
             "input_tokens": 20, "output_tokens": 5, "estimated_cost_usd": 0.02},
        ]
        out = daily_buckets(sessions)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["tool_calls"], 5)
        self.assertEqual(out[0]["estimated_cost_usd"], 0.03)


class TestHealth(unittest.TestCase):
    def test_health(self):
        sessions = [
            {"end_reason": "compacted", "rewind_count": 1,
             "compression_failure_error": "boom", "compression_ineffective_count": 2,
             "compression_fallback_streak": 3},
            {"end_reason": "completed", "rewind_count": 0,
             "compression_failure_error": None, "compression_ineffective_count": 0,
             "compression_fallback_streak": 0},
        ]
        h = health(sessions)
        self.assertEqual(h["compression_failure_errors"], 1)
        self.assertEqual(h["compression_ineffective_count"], 2)
        self.assertEqual(h["compression_fallback_streak_max"], 3)
        self.assertEqual(h["rewinds"], 1)
        self.assertEqual(h["end_reasons"], {"compacted": 1, "completed": 1})


class TestSummarize(unittest.TestCase):
    def test_shape(self):
        report = summarize([], [], [])
        for key in ("generated_at", "totals", "models", "tools", "daily", "health", "notes"):
            self.assertIn(key, report)


if __name__ == "__main__":
    unittest.main()
