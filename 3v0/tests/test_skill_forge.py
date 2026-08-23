"""Tests for the SkillForge synthesis core (3V0 create-half).

Run directly:
  python3 3v0/tests/test_skill_forge.py
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
DRIVER = REPO_ROOT / "3v0" / "scripts" / "run_skill_forge.py"

def _run_driver(*args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(DRIVER), *args], capture_output=True, text=True, timeout=120,
    )

def _json_out(proc: subprocess.CompletedProcess):
    out = proc.stdout.strip()
    return json.loads(out) if out else {}

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "3v0"))

from core.skill_forge import (  # noqa: E402
    load_module_public_api,
    synthesize_proposal,
    _slugify,
)
from core.forge_skill import build_skill_md  # noqa: E402


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


class TestForgeSkillMd(unittest.TestCase):
    def _prop(self, name="mymod", desc="Compute averages.", callables=("avg", "sma")) -> dict:
        return {
            "name": name,
            "category": "core",
            "description": desc,
            "overview": "Compute moving averages deterministically.",
            "public_callables": list(callables),
            "callable_docs": {"avg": "Rolling average.", "sma": "Alias."},
            "proposal_id": "forge-mymod-abc",
            "source": "3v0/core/mymod.py",
        }

    def test_builds_frontmatter_and_body(self) -> None:
        md = build_skill_md(self._prop())
        self.assertIn("name: mymod", md)
        self.assertIn('description: "Compute averages."', md)
        self.assertIn("## Method", md)
        self.assertIn("- avg — Rolling average.", md)
        self.assertIn("- sma — Alias.", md)
        self.assertIn("## References", md)
        self.assertIn("Source: `3v0/core/mymod.py`", md)

    def test_bare_name_and_empty_description(self) -> None:
        md = build_skill_md(self._prop(name="some/category/mymod", desc=""))
        # nested category path stripped to the bare name
        self.assertIn("name: mymod", md)
        self.assertIn("description: ''", md)

    def test_no_callables_degrades_gracefully(self) -> None:
        prop = self._prop(callables=())
        md = build_skill_md(prop)
        self.assertIn("complete the method by hand", md)


class TestForgeDriverVerify(unittest.TestCase):
    """The --verify keep/revise gate (the authoring half's ground-truth check)."""

    def test_verify_keep_for_module_with_passing_tests(self) -> None:
        proc = _run_driver("--verify", "3v0/core/safe_evolve.py")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        d = _json_out(proc)
        self.assertEqual(d.get("verdict"), "keep")
        self.assertEqual(d.get("tests"), "test_safe_evolve.py")

    def test_verify_no_tests_for_forge_module(self) -> None:
        # skill_forge has a test file BUT is the module under test here; a
        # sibling module without a dedicated test reports no_tests. Use a temp
        # module outside the tests tree.
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "standalone.py"
            p.write_text('"""Standalone."""\ndef work():\n    """Do."""\n    return 2\n')
            proc = _run_driver("--verify", str(p))
            self.assertEqual(proc.returncode, 0)
            d = _json_out(proc)
            self.assertEqual(d.get("verdict"), "no_tests")


if __name__ == "__main__":
    unittest.main(verbosity=2)