from __future__ import annotations

import json
import os
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))
sys.path.insert(0, str(REPO_ROOT / "3v0" / "core"))

from core.analytics_collect import build_events  # noqa: E402


class TestBuildEvents(unittest.TestCase):
    """Cover the latency-matching logic that lived untested in the script."""

    def setUp(self):
        fd, self.db = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        conn = sqlite3.connect(self.db)
        conn.execute("""
            CREATE TABLE messages (
                role TEXT, tool_name TEXT, tool_call_id TEXT,
                tool_calls TEXT, content TEXT, timestamp REAL
            )
        """)
        conn.commit()
        conn.close()

    def tearDown(self):
        os.unlink(self.db)

    def _insert(self, role, *, tool_name=None, tool_call_id=None,
                tool_calls=None, content=None, timestamp=100.0):
        conn = sqlite3.connect(self.db)
        conn.execute(
            "INSERT INTO messages (role, tool_name, tool_call_id, tool_calls, content, timestamp) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (role, tool_name, tool_call_id, tool_calls, content, timestamp),
        )
        conn.commit()
        conn.close()

    def test_latency_matching(self):
        self._insert("assistant", tool_calls=json.dumps([{"id": "abc", "name": "terminal"}]), timestamp=100.0)
        self._insert("tool", tool_name="terminal", tool_call_id="abc", content='{"success": true}', timestamp=100.5)
        events = build_events(self.db)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["name"], "terminal")
        self.assertEqual(events[0]["latency_ms"], 500.0)
        self.assertEqual(events[0]["status"], "success")

    def test_call_id_fallback(self):
        # assistant emits `call_id` (not `id`) — still matched
        self._insert("assistant", tool_calls=json.dumps([{"call_id": "xyz", "name": "read_file"}]), timestamp=10.0)
        self._insert("tool", tool_name="read_file", tool_call_id="xyz", content="ok", timestamp=11.0)
        events = build_events(self.db)
        self.assertEqual(events[0]["name"], "read_file")
        self.assertEqual(events[0]["latency_ms"], 1000.0)

    def test_negative_latency_guard(self):
        # tool result timestamp BEFORE the call → latency None (clock skew)
        self._insert("assistant", tool_calls=json.dumps([{"id": "abc", "name": "terminal"}]), timestamp=200.0)
        self._insert("tool", tool_name="terminal", tool_call_id="abc", content="ok", timestamp=100.0)
        events = build_events(self.db)
        self.assertEqual(len(events), 1)
        self.assertIsNone(events[0]["latency_ms"])

    def test_malformed_tool_calls_skipped(self):
        self._insert("assistant", tool_calls="not-json", timestamp=100.0)
        self._insert("tool", tool_name="terminal", tool_call_id="abc", content="ok", timestamp=101.0)
        events = build_events(self.db)
        # malformed assistant row is skipped; the tool row has no matching call → latency None
        self.assertEqual(len(events), 1)
        self.assertIsNone(events[0]["latency_ms"])

    def test_unmatched_tool_result(self):
        self._insert("tool", tool_name="terminal", tool_call_id="nope", content='{"exit_code": 1}', timestamp=100.0)
        events = build_events(self.db)
        self.assertEqual(len(events), 1)
        self.assertIsNone(events[0]["latency_ms"])
        self.assertEqual(events[0]["status"], "failure")

    def test_unknown_name(self):
        self._insert("tool", tool_call_id="nope", content="ok", timestamp=100.0)
        events = build_events(self.db)
        self.assertEqual(events[0]["name"], "unknown")


if __name__ == "__main__":
    unittest.main()
