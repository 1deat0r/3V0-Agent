"""Deterministic tests for the native config seam (env / .env resolution)."""
import os
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from native import config
except ImportError:
    import config  # direct-run fallback (mirrors the module pattern)


class ParseTest(unittest.TestCase):
    def test_parse_bare_export_comment_quotes(self):
        d = config._parse(
            "PLAIN=abc\n"
            "export EXPORTED=xyz\n"
            "QUOTED=\"double\"\n"
            "SINGLE='single'\n"
            "WITHHASH=abc#def\n"
            "COMMENTED=val # trailing comment\n"
            "# full line comment\n"
            " \n"
            "NOEQ no equals\n"
        )
        self.assertEqual(d["PLAIN"], "abc")
        self.assertEqual(d["EXPORTED"], "xyz")
        self.assertEqual(d["QUOTED"], "double")
        self.assertEqual(d["SINGLE"], "single")
        self.assertEqual(d["WITHHASH"], "abc#def")   # # inside value, no space before -> kept
        self.assertEqual(d["COMMENTED"], "val")      # space-# -> comment stripped
        self.assertNotIn("NOEQ", d)
        self.assertNotIn("# full line comment", d)

    def test_parse_empty(self):
        self.assertEqual(config._parse(""), {})
        self.assertEqual(config._parse("#only\n\n"), {})


class EnvPrecedenceTest(unittest.TestCase):
    def setUp(self):
        self._saved = {}
        for k in ("CFG_TEST_A", "CFG_TEST_B", "CFG_TEST_C"):
            self._saved[k] = os.environ.pop(k, None)
        config.clear_cache()

    def tearDown(self):
        for k, v in self._saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        config.clear_cache()

    def test_process_env_wins_over_dotenv(self):
        os.environ["CFG_TEST_A"] = "from-env"
        with tempfile.NamedTemporaryFile("w", suffix=".env", delete=False) as f:
            f.write("CFG_TEST_A=from-file\n")
            p = f.name
        try:
            self.assertEqual(config.get("CFG_TEST_A", env_file=p), "from-env")
        finally:
            os.unlink(p)

    def test_dotenv_fallback_and_default(self):
        with tempfile.NamedTemporaryFile("w", suffix=".env", delete=False) as f:
            f.write("CFG_TEST_B=from-file\n")
            p = f.name
        try:
            self.assertEqual(config.get("CFG_TEST_B", env_file=p), "from-file")
            # absent name -> default; absent name without default -> None
            self.assertEqual(config.get("CFG_TEST_ABSENT", "dflt", env_file=p), "dflt")
            self.assertIsNone(config.get("CFG_TEST_ABSENT", env_file=p))
        finally:
            os.unlink(p)

    def test_require_raises_when_absent(self):
        with tempfile.NamedTemporaryFile("w", suffix=".env", delete=False) as f:
            f.write("UNRELATED=1\n")
            p = f.name
        try:
            with self.assertRaises(RuntimeError):
                config.require("CFG_TEST_C", env_file=p)
        finally:
            os.unlink(p)

    def test_require_returns_env_value(self):
        os.environ["CFG_TEST_C"] = "req"
        try:
            self.assertEqual(config.require("CFG_TEST_C"), "req")
        finally:
            os.environ.pop("CFG_TEST_C", None)

    def test_cache_and_clear(self):
        with tempfile.NamedTemporaryFile("w", suffix=".env", delete=False) as f:
            f.write("CFG_TEST_A=one\n")
            p = f.name
        try:
            config.load(p)
            self.assertEqual(config.get("CFG_TEST_A", env_file=p), "one")
            # rewrite the underlying file; memoized load should NOT see it
            Path(p).write_text("CFG_TEST_A=two\n")
            self.assertEqual(config.get("CFG_TEST_A", env_file=p), "one")
            # after clear_cache, the new value is seen
            config.clear_cache()
            self.assertEqual(config.get("CFG_TEST_A", env_file=p), "two")
        finally:
            os.unlink(p)


if __name__ == "__main__":
    unittest.main(verbosity=2)
