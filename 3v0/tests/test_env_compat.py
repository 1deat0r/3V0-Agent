"""Contract tests for the brand-compatible env resolver (ADR-0006).

Pins the declared read chain — ``3V0_<NAME>`` first, legacy ``EV0_<NAME>``
second, first TRUTHY value wins — so the migrate phase (#20) can re-route
callers onto :func:`branded_env` without silently changing semantics.
"""
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import env_compat  # noqa: E402

SUFFIX = "ENVCOMPAT_PROBE"
CANON = f"3V0_{SUFFIX}"
LEGACY = f"EV0_{SUFFIX}"
# ADR-0006: the namespace is exactly two spellings; THREEV0_* is NOT a
# production env spelling (it is the Python-identifier family only).
THIRD = f"THREEV0_{SUFFIX}"


class BrandedEnvTest(unittest.TestCase):
    def setUp(self):
        self._saved = {k: os.environ.get(k) for k in (CANON, LEGACY, THIRD)}
        for k in (CANON, LEGACY, THIRD):
            os.environ.pop(k, None)

    def tearDown(self):
        for k, v in self._saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_canonical_wins_over_legacy(self):
        os.environ[CANON] = "canonical"
        os.environ[LEGACY] = "legacy"
        self.assertEqual(env_compat.branded_env(SUFFIX), "canonical")

    def test_canonical_alone_is_returned(self):
        os.environ[CANON] = "canonical"
        self.assertEqual(env_compat.branded_env(SUFFIX), "canonical")

    def test_legacy_fallback_when_no_canonical(self):
        os.environ[LEGACY] = "legacy"
        self.assertEqual(env_compat.branded_env(SUFFIX), "legacy")

    def test_threev0_spelling_is_not_consulted(self):
        os.environ[THIRD] = "third"
        self.assertIsNone(env_compat.branded_env(SUFFIX))
        os.environ[LEGACY] = "legacy"  # still wins over the THIRD leg
        self.assertEqual(env_compat.branded_env(SUFFIX), "legacy")

    def test_empty_canonical_falls_through_to_legacy(self):
        # "first truthy wins": an empty canonical value must never shadow
        # a set legacy value.
        os.environ[CANON] = ""
        os.environ[LEGACY] = "legacy"
        self.assertEqual(env_compat.branded_env(SUFFIX), "legacy")

    def test_empty_everywhere_returns_default(self):
        os.environ[CANON] = ""
        os.environ[LEGACY] = ""
        self.assertEqual(env_compat.branded_env(SUFFIX, "dflt"), "dflt")

    def test_default_none_when_unset(self):
        self.assertIsNone(env_compat.branded_env(SUFFIX))

    def test_default_passthrough_when_unset(self):
        self.assertEqual(env_compat.branded_env(SUFFIX, "/tmp/x"), "/tmp/x")
        self.assertEqual(env_compat.branded_env(SUFFIX, ""), "")

    def test_read_only_no_environ_mutation(self):
        os.environ[CANON] = "v"
        before = set(os.environ)
        self.assertEqual(env_compat.branded_env(SUFFIX), "v")
        env_compat.branded_env(SUFFIX, "dflt")  # unset suffix path too
        self.assertEqual(set(os.environ), before)


class WireEnvTest(unittest.TestCase):
    """wire_env — the bare-fallback accessor for unprefixed wire vars.

    Resolution: 3V0_<bare> -> EV0_<bare> -> <bare> (the documented wire
    name last, forever). Decision record: the unprefixed wire-var follow-up
    to tickets #20/#21 — platform settings (IRC_SERVER, NTFY_TOPIC, ...)
    ride the brand chain while keeping their wire spelling working.
    """

    def setUp(self):
        self.bare = "IRC_SERVER"
        self._saved = {
            k: os.environ.get(k)
            for k in ("3V0_IRC_SERVER", "EV0_IRC_SERVER", "IRC_SERVER")
        }
        for k in ("3V0_IRC_SERVER", "EV0_IRC_SERVER", "IRC_SERVER"):
            os.environ.pop(k, None)

    def tearDown(self):
        for k, v in self._saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_bare_name_still_resolves(self):
        os.environ["IRC_SERVER"] = "irc.example.com"
        self.assertEqual(env_compat.wire_env("IRC_SERVER"), "irc.example.com")

    def test_legacy_spelling_wins_over_bare(self):
        os.environ["IRC_SERVER"] = "wire"
        os.environ["EV0_IRC_SERVER"] = "legacy"
        self.assertEqual(env_compat.wire_env("IRC_SERVER"), "legacy")

    def test_canonical_wins_over_both(self):
        os.environ["IRC_SERVER"] = "wire"
        os.environ["EV0_IRC_SERVER"] = "legacy"
        os.environ["3V0_IRC_SERVER"] = "canonical"
        self.assertEqual(env_compat.wire_env("IRC_SERVER"), "canonical")

    def test_default_passthrough_when_unset(self):
        self.assertEqual(env_compat.wire_env("IRC_SERVER", "fallback"), "fallback")
        self.assertIsNone(env_compat.wire_env("IRC_SERVER"))

    def test_empty_bare_value_falls_through(self):
        os.environ["IRC_SERVER"] = ""
        self.assertIsNone(env_compat.wire_env("IRC_SERVER"))


if __name__ == "__main__":
    unittest.main()
