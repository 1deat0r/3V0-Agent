from __future__ import annotations

import sqlite3
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))
sys.path.insert(0, str(REPO_ROOT / "3v0" / "core"))

from core.memdb import (  # noqa: E402
    DEFAULT_PATH,
    add_fact,
    connect,
    migrate_from_json,
    rank,
    render,
    retrieve,
    valid_facts,
)

NOW = 1_800_000_000.0


class MemDBTest(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        self.addCleanup(self.conn.close)


class TestAddAndValid(MemDBTest):
    def test_add_and_list(self):
        add_fact(self.conn, "3v0", "model", "deepseek-v4-pro", domain="env", now=NOW)
        facts = valid_facts(self.conn, now=NOW)
        self.assertEqual(len(facts), 1)
        self.assertEqual(facts[0]["subject"], "3v0")
        self.assertEqual(facts[0]["object"], "deepseek-v4-pro")

    def test_supersession_closes_old(self):
        a = add_fact(self.conn, "3v0", "version", "1.0", now=NOW)
        b = add_fact(self.conn, "3v0", "version", "2.0", supersedes=a, now=NOW + 10)
        valid = valid_facts(self.conn, now=NOW + 10)
        self.assertEqual([f["id"] for f in valid], [b])
        row = self.conn.execute("SELECT valid_to FROM facts WHERE id=?", (a,)).fetchone()
        self.assertIsNotNone(row["valid_to"])

    def test_supersede_bad_fk_rejected(self):
        # FK must be enforced: a supersedes id that doesn't exist must fail,
        # not insert silently (regression for the missing PRAGMA foreign_keys).
        with self.assertRaises(sqlite3.IntegrityError):
            add_fact(self.conn, "3v0", "version", "2.0", supersedes=999999, now=NOW)

    def test_domain_scoping(self):
        add_fact(self.conn, "3v0", "repo", "3V0 Agent", domain="3v0", now=NOW)
        add_fact(self.conn, "axiom", "repo", "axiom-agent", domain="axiom", now=NOW)
        self.assertEqual(len(valid_facts(self.conn, domain="axiom", now=NOW)), 1)
        self.assertEqual(len(valid_facts(self.conn, now=NOW)), 2)


class TestRank(MemDBTest):
    def test_keyword_match_scores_higher(self):
        facts = [
            {"subject": "a", "predicate": "p", "object": "deepseek api", "content": "", "created_at": NOW, "access_count": 0, "last_accessed": None},
            {"subject": "b", "predicate": "p", "object": "unrelated", "content": "", "created_at": NOW, "access_count": 0, "last_accessed": None},
        ]
        self.assertEqual(rank(facts, query_terms=["deepseek"], now=NOW)[0]["subject"], "a")

    def test_recency_scores_higher(self):
        facts = [
            {"subject": "old", "predicate": "p", "object": "x", "content": "", "created_at": NOW - 86400 * 30, "access_count": 0, "last_accessed": NOW - 86400 * 30},
            {"subject": "new", "predicate": "p", "object": "x", "content": "", "created_at": NOW, "access_count": 0, "last_accessed": NOW},
        ]
        self.assertEqual(rank(facts, now=NOW)[0]["subject"], "new")

    def test_frequency_scores_higher(self):
        facts = [
            {"subject": "rare", "predicate": "p", "object": "x", "content": "", "created_at": NOW, "access_count": 0, "last_accessed": None},
            {"subject": "hot", "predicate": "p", "object": "x", "content": "", "created_at": NOW, "access_count": 100, "last_accessed": NOW},
        ]
        self.assertEqual(rank(facts, now=NOW)[0]["subject"], "hot")


class TestRetrieve(MemDBTest):
    def test_retrieve_caps_and_touches(self):
        for i in range(5):
            add_fact(self.conn, f"s{i}", "p", "v", now=NOW)
        out = retrieve(self.conn, limit=2, now=NOW)
        self.assertEqual(len(out), 2)
        total = self.conn.execute("SELECT SUM(access_count) FROM facts").fetchone()[0]
        self.assertEqual(total, 2)


class TestMigrate(MemDBTest):
    def test_migrate_tolerant(self):
        legacy = [
            {"content": "Fork 1deat0r/hermes-agent", "source": "session-1"},
            {"text": "DeepSeek V4-Pro", "source": "session-2", "domain": "env"},
        ]
        self.assertEqual(migrate_from_json(self.conn, legacy, now=NOW), 2)
        self.assertEqual(len(valid_facts(self.conn, now=NOW)), 2)


class TestDefaultPath(MemDBTest):
    def test_default_path_is_absolute(self):
        self.assertTrue(str(DEFAULT_PATH).startswith("/"))
        self.assertTrue(str(DEFAULT_PATH).endswith("3v0/data/memory.db"))


class TestRender(MemDBTest):
    def test_render(self):
        facts = [{"subject": "3v0", "predicate": "model", "object": "deepseek-v4-pro", "content": "the LLM substrate"}]
        text = render(facts)
        self.assertIn("3v0 model deepseek-v4-pro", text)
        self.assertIn("the LLM substrate", text)


if __name__ == "__main__":
    unittest.main()
