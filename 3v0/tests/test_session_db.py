"""Tests for core.session_db — the named-column session-DB read adapter.

The adapter's whole point is order-independence: a column added or reordered
must never shift a read (the positional-index code it replaced misread ``cwd``
as ``last_activity_at``). These tests build fixtures with the ``sessions``
table in a NON-canonical column order and assert the named reads stay correct.
"""

from __future__ import annotations

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.session_db import candidate_rows, load_session, session_columns  # noqa: E402


def _make_db(path: Path, column_order: list[str]) -> None:
    conn = sqlite3.connect(str(path))
    cols_sql = ", ".join(column_order)
    conn.execute(f"CREATE TABLE sessions (id TEXT PRIMARY KEY, {cols_sql})")
    conn.execute(
        "CREATE TABLE messages (id INTEGER PRIMARY KEY, session_id TEXT, "
        "role TEXT, content TEXT, tool_name TEXT, active INTEGER DEFAULT 1)"
    )
    conn.commit()
    conn.close()


def _insert(path: Path, column_order: list[str], session_id: str, **values) -> None:
    conn = sqlite3.connect(str(path))
    cols = ["id"] + list(column_order)
    vals = [session_id] + [values.get(c) for c in column_order]
    ph = ", ".join("?" for _ in cols)
    conn.execute(f"INSERT INTO sessions ({', '.join(cols)}) VALUES ({ph})", vals)
    conn.commit()
    conn.close()


class TestSessionColumns(unittest.TestCase):
    def test_missing_db_returns_empty_set(self):
        self.assertEqual(session_columns(Path("/nonexistent/3v0-state.db")), set())


class TestLoadSessionNamed(unittest.TestCase):
    def test_column_order_does_not_matter(self):
        # cwd placed BEFORE ended_at — the positional code would misread this.
        order = ["source", "title", "last_activity_at", "cwd", "ended_at"]
        d = tempfile.mkdtemp()
        db = Path(d) / "state.db"
        _make_db(db, order)
        _insert(db, order, "sess1", source="tui", title="T",
                last_activity_at=100.0, cwd="/home/x", ended_at=200.0)
        s = load_session(db, "sess1")
        self.assertEqual(s["source"], "tui")
        self.assertEqual(s["title"], "T")
        self.assertEqual(s["cwd"], "/home/x")
        self.assertEqual(s["ended"], True)
        self.assertEqual(s["as_of"], 200.0)  # ended_at wins over last_activity_at

    def test_as_of_falls_back_to_last_activity(self):
        order = ["source", "title", "ended_at", "last_activity_at", "cwd"]
        d = tempfile.mkdtemp()
        db = Path(d) / "state.db"
        _make_db(db, order)
        _insert(db, order, "sess2", source="tui", title="T",
                ended_at=None, last_activity_at=123.0, cwd="/c")
        s = load_session(db, "sess2")
        self.assertEqual(s["ended"], False)   # ended_at is NULL
        self.assertEqual(s["as_of"], 123.0)   # last_activity_at fallback

    def test_missing_row_returns_none(self):
        d = tempfile.mkdtemp()
        db = Path(d) / "state.db"
        _make_db(db, ["source", "title"])
        self.assertIsNone(load_session(db, "does-not-exist"))


class TestCandidateRowsNamed(unittest.TestCase):
    def test_returns_named_dicts_and_excludes_live(self):
        order = ["source", "title", "ended_at", "parent_session_id",
                 "hidden", "archived", "cwd"]
        d = tempfile.mkdtemp()
        db = Path(d) / "state.db"
        _make_db(db, order)
        _insert(db, order, "aaa", source="tui", title="T1", ended_at=1,
                cwd="/home", hidden=0, archived=0)
        _insert(db, order, "bbb", source="tui", title="T2", ended_at=None,
                hidden=0, archived=0)  # live (ended_at NULL) — excluded
        rows = candidate_rows(db, session_columns(db))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], "aaa")
        self.assertEqual(rows[0]["source"], "tui")
        self.assertEqual(rows[0]["cwd"], "/home")


if __name__ == "__main__":
    unittest.main()
