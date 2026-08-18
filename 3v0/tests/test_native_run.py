"""Deterministic test for the native serve entrypoint — importing must not start a server."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


class RunEntrypointTest(unittest.TestCase):
    def test_import_does_not_start_a_server(self):
        from native import run  # noqa: F401

        # engine.server must NOT be invoked at import time.
        self.assertTrue(callable(run.serve))


if __name__ == "__main__":
    unittest.main(verbosity=2)
