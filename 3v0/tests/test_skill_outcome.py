"""Tests for the skill outcome-capture module (3V0 read-feedback closure).

Run directly:
  python3 3v0/tests/test_skill_outcome.py
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest

REPO_ROOT = Path = __import__("pathlib").Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.skill_outcome import (  # noqa: E402
    extract_loaded_skills,
    mark_skill_outcome,
    VALID_OUTCOMES,
    _MAX_OUTCOME_HISTORY,
)
from core.skills import SkillStore  # noqa: E402


def _skill_view_msg(name: str, resolved: str = "") -> dict:
    content = {"success": True, "name": resolved or name}
    return {
        "role": "assistant",
        "content": __import__("json").dumps(content),
        "tool_name": "skill_view",
    }


def _other_msg(tool: str = "read_file") -> dict:
    return {"role": "assistant", "content": "{}", "tool_name": tool}


def _store() -> tuple[SkillStore, str]:
    path = os.path.join(tempfile.mkdtemp(), "skills.json")
    s = SkillStore(path)
    s.add("foo", "create", "a", content="---\nname: foo\n")
    s.add("bar", "create", "a", content="---\nname: bar\n")
    return s, path


class TestExtractLoadedSkills(unittest.TestCase):
    def test_extracts_skill_view_in_order(self) -> None:
        msgs = [
            _other_msg(),
            _skill_view_msg("axolotl"),
            _skill_view_msg("cookbook"),
            _other_msg(),
        ]
        self.assertEqual(extract_loaded_skills(msgs), ["axolotl", "cookbook"])

    def test_dedupes_repeated_views(self) -> None:
        msgs = [
            _skill_view_msg("axolotl"),
            _skill_view_msg("axolotl"),
            _skill_view_msg("cookbook"),
        ]
        self.assertEqual(extract_loaded_skills(msgs), ["axolotl", "cookbook"])

    def test_resolved_qualified_name_wins(self) -> None:
        # A qualified 'plugin:skill' resolves in the payload to the canonical
        # name; the extraction normalizes the plugin form.
        msgs = [
            _skill_view_msg("superpowers:writing-plans", resolved="writing-plans"),
            _skill_view_msg("local:notes", resolved="Local Notes"),
        ]
        loaded = extract_loaded_skills(msgs)
        self.assertEqual(loaded, ["writing-plans", "Local Notes"])

    def test_ignores_non_skill_tools_and_non_json(self) -> None:
        msgs = [
            _other_msg("read_file"),
            _other_msg("skill_manage"),  # a write, not a load
            {"role": "assistant", "content": "not-json", "tool_name": "skill_view"},
        ]
        self.assertEqual(extract_loaded_skills(msgs), [])

    def test_plugin_form_normalizes_to_last_segment(self) -> None:
        msgs = [_skill_view_msg("myplugin:explore", resolved="myplugin:explore")]
        self.assertEqual(extract_loaded_skills(msgs), ["explore"])


class TestMarkSkillOutcome(unittest.TestCase):
    def test_writes_outcome_to_active_head(self) -> None:
        s, path = _store()
        res = mark_skill_outcome(s, "sess-1", {"foo": "success"}, source="review_session")
        self.assertIn("foo", res)
        meta = s.skill_meta("foo")
        self.assertEqual(meta["last_outcome"], "success")
        self.assertIn("last_outcome_at", meta)
        self.assertEqual(meta["outcome_source"], "review_session")
        hist = meta["outcome_history"]
        self.assertEqual(len(hist), 1)
        self.assertEqual(hist[0]["outcome"], "success")
        self.assertEqual(hist[0]["session"], "sess-1")

    def test_history_is_bounded_and_recent_first(self) -> None:
        s, path = _store()
        # Push more than the cap; only the newest survive, oldest dropped.
        for i in range(_MAX_OUTCOME_HISTORY + 3):
            mark_skill_outcome(
                s, f"sess-{i}", {"foo": "success" if i % 2 == 0 else "failure"}
            )
        meta = s.skill_meta("foo")
        history = meta["outcome_history"]
        self.assertEqual(len(history), _MAX_OUTCOME_HISTORY)
        self.assertEqual(history[0]["session"], f"sess-{_MAX_OUTCOME_HISTORY + 2}")
        # recovery: head is still the single create (append-only)
        self.assertEqual(len(s.versions("foo")), 1)

    def test_skips_invalid_outcome_and_missing_skill(self) -> None:
        s, path = _store()
        res = mark_skill_outcome(s, "s1", {"foo": "banana", "nope": "success"})
        self.assertEqual(res, {})
        self.assertNotIn("last_outcome", s.skill_meta("foo"))
        self.assertEqual(s.skill_meta("nope"), {})

    def test_empty_outcomes_is_noop(self) -> None:
        s, path = _store()
        self.assertEqual(mark_skill_outcome(s, "s1", {}), {})


if __name__ == "__main__":
    unittest.main(verbosity=2)