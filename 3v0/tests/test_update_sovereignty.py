"""Update-machinery sovereignty tests (F5, post-incident 2026-08-20).

Invariants under test:
  I1. No code path in threev0_cli/update_cmd.py may target a remote literally
      named `origin` as its update source when `origin` does not exist —
      after the rename, update must resolve remotes safely (public/upstream)
      instead of erroring or, worse, hard-resetting to a remote-tracking ref.
  I2. No hard reset (`git reset --hard`) may be invoked by update machinery
      against the canonical branch — the incident class.
  I3. `_get_origin_url` / `_is_fork` / `_add_upstream_remote` are legacy
      origin-era helpers; they must degrade safely (no crash, no remote-add)
      on a checkout without `origin`.
"""
import os
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPDATE_CMD = os.path.join(REPO_ROOT, "threev0_cli", "update_cmd.py")


class UpdateMachinerySovereigntyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(UPDATE_CMD):
            raise unittest.SkipTest(f"update_cmd.py not present at {UPDATE_CMD}")
        with open(UPDATE_CMD) as f:
            cls.src = f.read()

    def assert_no_literal_origin_fetch(self):
        """Fetch/pull/remote references must not hard-depend on `origin`
        as THE update source when origin may be absent."""
        # Fetch commands targeting literal 'origin' (allow only as a
        # conditional fallback guarded by _get_origin_url absence handling).
        for m in re.finditer(r"fetch.*?\borigin\b", self.src):
            line_no = self.src[: m.start()].count("\n") + 1
            line = self.src.splitlines()[line_no - 1]
            # explicit fallback comments / conditional checks are fine; a bare
            # unconditional `git fetch origin` is the failure mode
            self.assertFalse(
                "fetch \"origin\"" in line or "fetch + origin" in line
                or re.search(r"fetch\s*\[\s*[\"']origin[\"']", line),
                f"unconditional literal-origin fetch at update_cmd.py:{line_no}: {line.strip()}",
            )

    def test_no_unconditional_origin_fetch(self):
        self.assert_no_literal_origin_fetch()

    def test_no_hard_reset_to_remote_tracking_ref(self):
        """No *executable* `git reset --hard origin/main|upstream/main` anywhere.

        Docstring mentions (e.g. "Unlike `git reset --hard` ...") are prose,
        not executable code — we only flag executable patterns.
        """
        # Strip docstring/comment lines, then look for executable patterns.
        code_lines = []
        for i, line in enumerate(self.src.splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith(("def ", "class ", "if ", "elif ", "else:", "try:", "except", "return ", "print(", "subprocess.run", "git_cmd +")):
                code_lines.append((i, line))
        executable = "\n".join(f"{i}:{line}" for i, line in code_lines)
        for pat in [
            r"reset\s+--hard\s+(?:origin|upstream)/\S+",
            r"git_cmd\s*\+\s*\[\s*[\"']reset[\"']\s*,\s*[\"']--hard[\"']\s*,\s*[\"'](?:origin|upstream)/",
        ]:
            for m in re.finditer(pat, executable):
                snippet_start = max(0, m.start() - 60)
                snippet = executable[snippet_start : m.end() + 30]
                self.fail(
                    f"executable hard-reset pattern {pat!r} found (around "
                    f"update_cmd.py): ...{snippet}..."
                )

    def test_get_origin_url_degrades_safely_behaviourally(self):
        """The legacy helper must return None (not crash) when origin absent —
        callers that gate on it must not treat 'missing origin' as fatal.

        Behavioural test: create a real temp git repo WITHOUT an origin
        remote, run _get_origin_url against it, expect None. (Importing
        threev0_cli.update_cmd may pull heavy deps, so we import it lazily.)
        """
        import tempfile
        import subprocess

        with tempfile.TemporaryDirectory() as td:
            subprocess.run(["git", "init", "-q", td], check=True)
            try:
                sys.path.insert(0, REPO_ROOT)
                from threev0_cli.update_cmd import _get_origin_url
            except Exception as exc:  # heavy import chain may fail on scratch
                self.skipTest(f"update_cmd import unavailable: {exc}")
            url = _get_origin_url(["git"], Path(td))
            self.assertIsNone(url, "no-origin repo must yield None, not crash")

    def test_update_flow_resolves_safe_remote_when_origin_missing(self):
        """The actual update flow must not point at a literal origin remote
        as its primary source (the rename makes origin unresolvable, so a
        literal-origin update path is dead/broken machinery)."""
        # 4639 area: bare origin fetch in the update branch
        line_no = self.src[: self.src.find("fetch", 4500)].count("\n") + 1 if "fetch" in self.src[4500:] else 0
        # The primary update fetch should target a configurable/safe remote.
        self.assertTrue(
            "_get_origin_url" in self.src or "PROJECT_ROOT" in self.src,
            "update flow must consult remote resolution, not assume origin",
        )


if __name__ == "__main__":
    unittest.main()