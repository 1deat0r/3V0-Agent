"""Direct tests for core.forget — the forgetting policy (Stone 24, ADR-0005).

The pure ``is_stale`` rule is exercised without a DB; ``forget`` runs against
a temp store and asserts archive-not-delete (valid_to set, fact recoverable).
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))
sys.path.insert(0, str(REPO_ROOT / "3v0" / "core"))

from core.forget import forget, is_stale  # noqa: E402
from core.memdb import add_fact, connect, valid_facts  # noqa: E402

NOW = 1_800_000_000.0
OLD = NOW - 40 * 86400.0  # 40 days ago


class TestIsStale(unittest.TestCase):
    def test_stale_never_used_old_memory(self):
        f = {"kind": "memory", "access_count": 0, "last_projected": None,
             "created_at": OLD}
        self.assertTrue(is_stale(f, 30, NOW))

    def test_identity_is_permanent(self):
        f = {"kind": "identity", "access_count": 0, "last_projected": None,
             "created_at": OLD}
        self.assertFalse(is_stale(f, 30, NOW))

    def test_directive_is_permanent(self):
        f = {"kind": "directive", "access_count": 0, "last_projected": None,
             "created_at": OLD}
        self.assertFalse(is_stale(f, 30, NOW))

    def test_retrieved_is_not_stale(self):
        f = {"kind": "memory", "access_count": 1, "last_projected": None,
             "created_at": OLD}
        self.assertFalse(is_stale(f, 30, NOW))

    def test_projected_is_not_stale(self):
        f = {"kind": "memory", "access_count": 0, "last_projected": NOW - 10,
             "created_at": OLD}
        self.assertFalse(is_stale(f, 30, NOW))

    def test_young_is_not_stale(self):
        f = {"kind": "memory", "access_count": 0, "last_projected": None,
             "created_at": NOW - 5 * 86400}
        self.assertFalse(is_stale(f, 30, NOW))


class TestForget(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        self.addCleanup(self.conn.close)

    def test_forget_archives_stale_only(self):
        # old, never used -> stale (archived)
        add_fact(self.conn, "3v0", "note", "stale fact", content="stale fact",
                 now=OLD)
        # old, but retrieved -> kept
        rid = add_fact(self.conn, "3v0", "note", "used fact", content="used fact",
                       now=OLD)
        self.conn.execute("UPDATE facts SET access_count = 1 WHERE id = ?", (rid,))
        self.conn.commit()
        # young -> kept
        add_fact(self.conn, "3v0", "note", "fresh fact", content="fresh fact",
                 now=NOW - 5 * 86400)

        self.assertEqual(forget(self.conn, 30, now=NOW), 1)

        active = {f["object"] for f in valid_facts(self.conn, now=NOW)}
        self.assertEqual(active, {"used fact", "fresh fact"})
        # the forgotten fact is archived (valid_to set), not deleted
        row = self.conn.execute(
            "SELECT valid_to, note FROM facts WHERE object = 'stale fact'").fetchone()
        self.assertIsNotNone(row["valid_to"])
        self.assertIn("forgotten", row["note"])

    def test_forget_respects_projection(self):
        # projected (last_projected set) but never retrieved -> kept
        pid = add_fact(self.conn, "3v0", "note", "projected fact",
                       content="projected fact", now=OLD)
        self.conn.execute("UPDATE facts SET last_projected = ? WHERE id = ?",
                          (NOW - 10, pid))
        self.conn.commit()
        self.assertEqual(forget(self.conn, 30, now=NOW), 0)

    def test_forget_noop_when_nothing_stale(self):
        self.assertEqual(forget(self.conn, 30, now=NOW), 0)


if __name__ == "__main__":
    unittest.main()
