"""Tests for the SkillForge synthesis core (3V0 create-half).

Run directly:
  python3 3v0/tests/test_skill_forge.py
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "3v0"))

from core.skill_forge import (  # noqa: E402
    load_module_public_api,
    synthesize_proposal,
    _slugify,
)


def _write_module(tmp: Path, code: str) -> Path:
    p = tmp / "mymod.py"
    p.write_text(code, encoding="utf-8")
    return p


class TestLoadPublicApi(unittest.TestCase):
    def test_returns_public_callables_with_docs(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            p = _write_module(Path(td), '"""A useful module."""\ndef do_thing(x):\n    """Do the thing."""\n    return x\n\ndef _hidden():\n    return 1\n')
            api = load_module_public_api(p)
            names = [n for n, _ in api]
            self.assertIn("do_thing", names)
            self.assertNotIn("_hidden", names)
            d = dict(api)
            self.assertEqual(d["do_thing"], 'Do the thing.')

    def test_missing_module_returns_empty(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(load_module_public_api(Path(td) / "nope.py"), [])

    def test_broken_module_returns_empty(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            p = _write_module(Path(td), "this is not python")
            self.assertEqual(load_module_public_api(p), [])


class TestSynthesizeProposal(unittest.TestCase):
    def test_builds_proposal_from_module(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            p = _write_module(
                Path(td),
                '"""Compute moving averages deterministically."""\n'
                "def moving_average(xs, n=3):\n"
                '    """Rolling mean over a window."""\n'
                "    return []\n"
                "def sma(xs):\n"
                '    """Simple moving average alias."""\n'
                "    return []\n",
            )
            prop = synthesize_proposal(p)
            self.assertIsNotNone(prop)
            self.assertEqual(prop["name"], "mymod")  # slug from stem
            self.assertEqual(prop["category"], td.split("/")[-1] or "general")
            self.assertIn("moving", prop["description"])
            self.assertIn("moving_average", prop["public_callables"])
            self.assertTrue(prop["proposal_id"].startswith("forge-mymod-"))

    def test_returns_none_for_module_with_no_public_callables(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            p = _write_module(Path(td), '"""Only private."""\ndef _hidden():\n    return 1\n')
            self.assertIsNone(synthesize_proposal(p))

    def test_slugify(self) -> None:
        self.assertEqual(_slugify("My_Module"), "my-module")
        self.assertEqual(_slugify("core.memdb"), "core-memdb")
        self.assertEqual(_slugify(""), "skill")


if __name__ == "__main__":
    unittest.main(verbosity=2)