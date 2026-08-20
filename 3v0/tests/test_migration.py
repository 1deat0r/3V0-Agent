"""Migration: legacy JSON store payload -> memdb triple store (rewire slice).

The live memory.json is a Fact-shaped payload: hex ids, kind, source, ISO
created_at, supersedes lists, superseded_by links (hex or the 'retracted'
sentinel). migrate_from_json must land it in the triple store with temporal
validity and recoverable lineage — nothing erased, nothing silently dropped.

Run directly:
  python3 3v0/tests/test_migration.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))
sys.path.insert(0, str(REPO_ROOT / "3v0" / "core"))

from core.memdb import connect, migrate_from_json, valid_facts  # noqa: E402


def t(iso: str) -> float:
    import calendar
    import time
    return float(calendar.timegm(time.strptime(iso, "%Y-%m-%dT%H:%M:%SZ")))


class MigrationTest(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        self.addCleanup(self.conn.close)

    def test_migrates_fact_shaped_payload_with_links(self):
        payload = [
            {
                "id": "aaaaaaaaaaaa", "content": "gh account is mustbearnold",
                "kind": "memory", "source": "foreground",
                "created_at": "2026-08-10T00:00:00Z",
                "supersedes": [], "superseded_by": "bbbbbbbbbbbb", "note": "",
            },
            {
                "id": "bbbbbbbbbbbb", "content": "gh account is 1deat0r",
                "kind": "memory", "source": "operator",
                "created_at": "2026-08-12T00:00:00Z",
                "supersedes": ["aaaaaaaaaaaa"], "superseded_by": "", "note": "",
            },
        ]
        n = migrate_from_json(self.conn, payload)
        self.assertEqual(n, 2)

        rows = {r["object"]: r for r in self.conn.execute("SELECT * FROM facts")}
        new_row = rows["gh account is 1deat0r"]
        old_row = rows["gh account is mustbearnold"]
        self.assertNotEqual(new_row["id"], old_row["id"])  # both got real row ids

        # temporal validity: the superseded fact stopped being true exactly
        # when its successor was created
        self.assertEqual(old_row["valid_to"], t("2026-08-12T00:00:00Z"))
        self.assertIsNone(new_row["valid_to"])
        # lineage: the FK link points at the successor's predecessor
        self.assertEqual(new_row["supersedes"], old_row["id"])
        # kinds survive
        self.assertEqual(old_row["kind"], "memory")

        # only the successor is valid now
        valid = valid_facts(self.conn, now=t("2026-08-13T00:00:00Z"))
        self.assertEqual([f["object"] for f in valid], ["gh account is 1deat0r"])

    def test_retracted_fact_is_a_tombstone_not_lost(self):
        payload = [
            {
                "id": "cccccccccccc", "content": "dead fact", "kind": "memory",
                "source": "test", "created_at": "2026-08-11T00:00:00Z",
                "supersedes": [], "superseded_by": "retracted",
                "note": "retracted by operator",
            },
        ]
        migrate_from_json(self.conn, payload)
        rows = self.conn.execute("SELECT * FROM facts").fetchall()
        self.assertEqual(len(rows), 1)
        # never valid at any time >= creation: the row exists for audit only
        self.assertEqual(rows[0]["valid_to"], t("2026-08-11T00:00:00Z"))
        self.assertEqual(rows[0]["note"], "retracted by operator")

    def test_loose_dicts_still_tolerant(self):
        legacy = [
            {"content": "Fork 1deat0r/3v0-agent", "source": "session-1"},
            {"text": "DeepSeek V4-Pro", "source": "session-2", "domain": "env"},
        ]
        self.assertEqual(migrate_from_json(self.conn, legacy), 2)
        self.assertEqual(len(valid_facts(self.conn)), 2)

    def test_kind_defaults_to_memory(self):
        migrate_from_json(self.conn, [{"content": "x", "source": "s"}])
        row = self.conn.execute("SELECT kind FROM facts").fetchone()
        self.assertEqual(row["kind"], "memory")


if __name__ == "__main__":
    unittest.main()
