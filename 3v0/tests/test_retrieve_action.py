"""The runtime retrieve action — the seam's second adapter (ADR-0004).

``threev0_store action='retrieve'`` shells out to ``scripts/query.py
--action retrieve`` and returns the working set the same seam selects for the
profile view, with real feedback (touch) — a mid-turn retrieval IS evidence
the facts were pulled into context, unlike a wake export.

Run directly:
  python3 3v0/tests/test_retrieve_action.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.memdb import add_fact, connect  # noqa: E402

QUERY_SCRIPT = REPO_ROOT / "3v0" / "scripts" / "query.py"


def run_query(db_path: str, *argv: str) -> dict:
    env = os.environ.copy()
    env["THREEV0_STORE"] = db_path
    proc = subprocess.run(
        [sys.executable, str(QUERY_SCRIPT), *argv],
        capture_output=True, text=True, timeout=60, env=env,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


class RetrieveActionTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.db = os.path.join(self.dir, "mem.db")
        conn = connect(self.db)
        for content in ("deepseek model pin", "fiverr gig live", "solana wallet"):
            add_fact(conn, "3v0", "note", content, content=content)
        conn.close()

    def test_retrieve_returns_working_set(self):
        out = run_query(self.db, "--action", "retrieve", "--query", "model")
        self.assertIn("facts", out)
        self.assertIn("text", out)
        self.assertTrue(any("deepseek model pin" in f["content"] for f in out["facts"]))
        self.assertIn("deepseek model pin", out["text"])

    def test_retrieve_touches_feedback_only_for_chosen(self):
        out = run_query(self.db, "--action", "retrieve", "--query", "model",
                        "--budget", "40")
        conn = connect(self.db)
        total = conn.execute("SELECT SUM(access_count) FROM facts").fetchone()[0]
        conn.close()
        # budget 40 admits two of three facts; feedback touches exactly the
        # chosen working set, not everything in the store
        self.assertEqual(len(out["facts"]), 2)
        self.assertEqual(total, 2)

    def test_retrieve_respects_budget(self):
        out = run_query(self.db, "--action", "retrieve", "--budget", "30")
        self.assertLessEqual(len(out["text"]), 30)


if __name__ == "__main__":
    unittest.main()
