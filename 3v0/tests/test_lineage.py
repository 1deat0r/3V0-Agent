"""Direct tests for core.lineage — the shared pure lineage semantics.

The lineage module is the single owner of fact *meaning* (kinds, retraction
tagging, the supersession walk, the export grouping) shared by the JSON
``MemoryStore`` and the SQLite ``SQLStore``. These tests drive it directly, so
a drift in either backend's delegation is caught without a DB.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))
sys.path.insert(0, str(REPO_ROOT / "3v0" / "core"))

from core.lineage import (  # noqa: E402
    KINDS,
    RETRACTED,
    export_shape,
    history_chain,
    iso_time,
    retraction_note,
    validate_kind,
)
from core.memory import Fact  # noqa: E402


def _fact(fid, supersedes=None, superseded_by=""):
    return Fact(id=fid, content=f"fact {fid}", kind="memory", source="test",
                created_at="2026-08-18T00:00:00Z",
                supersedes=list(supersedes or []), superseded_by=superseded_by)


class TestKindAndTime(unittest.TestCase):
    def test_validate_kind_accepts_canonical(self):
        for k in KINDS:
            self.assertEqual(validate_kind(k), k)

    def test_validate_kind_rejects_unknown(self):
        with self.assertRaises(ValueError):
            validate_kind("bogus")

    def test_iso_time_is_utc_iso8601(self):
        self.assertEqual(iso_time(0.0), "1970-01-01T00:00:00Z")


class TestRetractionNote(unittest.TestCase):
    def test_no_source_leaves_note_untouched(self):
        self.assertEqual(retraction_note("existing note", ""), "existing note")
        self.assertEqual(retraction_note("", ""), "")

    def test_tag_appended(self):
        self.assertEqual(retraction_note("", "bg_review"), "retracted by bg_review")
        self.assertEqual(retraction_note("existing", "bg_review"),
                         "existing retracted by bg_review")


class TestHistoryChain(unittest.TestCase):
    def _get(self, facts):
        return {f.id: f for f in facts}.get

    def test_walks_oldest_to_newest(self):
        a, b, c = _fact("a"), _fact("b"), _fact("c")
        b.supersedes = ["a"]
        c.supersedes = ["b"]
        a.superseded_by = "b"
        b.superseded_by = "c"
        chain = history_chain(self._get([a, b, c]), "a")
        self.assertEqual([f.id for f in chain], ["a", "b", "c"])

    def test_any_link_recovers_full_thread(self):
        a, b, c = _fact("a"), _fact("b"), _fact("c")
        b.supersedes = ["a"]
        c.supersedes = ["b"]
        a.superseded_by = "b"
        b.superseded_by = "c"
        self.assertEqual([f.id for f in history_chain(self._get([a, b, c]), "b")],
                         ["a", "b", "c"])

    def test_retracted_is_terminal(self):
        a = _fact("a", superseded_by=RETRACTED)
        self.assertEqual([f.id for f in history_chain(self._get([a]), "a")], ["a"])

    def test_dangling_successor_terminates(self):
        a = _fact("a", superseded_by="missing-id")
        self.assertEqual([f.id for f in history_chain(self._get([a]), "a")], ["a"])

    def test_cycle_is_guarded(self):
        a, b = _fact("a"), _fact("b")
        b.supersedes = ["a"]
        a.superseded_by = "b"
        b.superseded_by = "a"
        # Must terminate (not infinite-loop) and return a bounded chain.
        chain = history_chain(self._get([a, b]), "a")
        self.assertEqual(len(chain), 1)

    def test_missing_start_is_empty(self):
        self.assertEqual(history_chain(self._get([]), "nope"), [])


class TestExportShape(unittest.TestCase):
    def test_groups_by_kind_and_omits_empty(self):
        def active(kind):
            return [_fact("a"), _fact("b")] if kind == "memory" else []
        self.assertEqual(export_shape(KINDS, active), {"memory": ["fact a", "fact b"]})


if __name__ == "__main__":
    unittest.main()
