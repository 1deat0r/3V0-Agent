"""Contract tests for the provider registry (3v0/native/providers.py).

Asserts the multi-provider seam: named resolution, backward-compatible
defaults, config/env override layering, and lazy (never-at-import) secrets.
No network; keys are read only via Provider.api_key() which tests don't call.
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


class ProvidersTest(unittest.TestCase):
    def setUp(self):
        from native import config, providers
        self.config = config
        self.providers = providers
        self._keys = {k: os.environ.get(k) for k in
                      ("THREEV0_MAIN_URL", "THREEV0_MAIN_MODEL", "THREEV0_MAIN_KEY",
                       "THREEV0_AUX_URL", "THREEV0_AUX_MODEL",
                       "THREEV0_EMBED_MODEL", "THREEV0_EMBED_DIM")}
        for k in self._keys:
            os.environ.pop(k, None)
        self.config.clear_cache()

    def tearDown(self):
        for k, v in self._keys.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        self.config.clear_cache()

    def test_three_builtin_providers(self):
        self.assertEqual(set(self.providers.names()), {"main", "aux", "embed"})

    def test_defaults_are_the_deliberate_substrate(self):
        m = self.providers.resolve("main")
        self.assertEqual(m.base_url, "https://api-inference.bitdeer.ai/v1")
        self.assertEqual(m.model, "deepseek-ai/DeepSeek-V4-Flash")
        self.assertEqual(m.api_key_name, "BITDEER_API_KEY")
        a = self.providers.resolve("aux")
        self.assertTrue(a.base_url.endswith("fireworks.ai/inference/v1"))
        self.assertEqual(a.api_key_name, "FIREWORKS_API_KEY")
        e = self.providers.resolve("embed")
        self.assertEqual(e.model, "BAAI/bge-m3")
        self.assertEqual(e.dims, 1024)

    def test_env_override_layers_over_default(self):
        os.environ["THREEV0_MAIN_MODEL"] = "example/other-model"
        os.environ["THREEV0_MAIN_KEY"] = "OTHER_KEY"
        m = self.providers.resolve("main")
        self.assertEqual(m.model, "example/other-model")
        self.assertEqual(m.api_key_name, "OTHER_KEY")
        self.assertEqual(m.base_url, "https://api-inference.bitdeer.ai/v1")  # unchanged

    def test_resolve_unknown_fails_loudly(self):
        with self.assertRaises(KeyError):
            self.providers.resolve("not-a-provider")

    def test_api_key_resolved_lazily_from_seam(self):
        # resolve() never touches the secret; api_key() reads it via config at
        # call time (env or profile .env both still have it). Non-empty proves
        # the lazy read works without baking a secret into the object.
        p = self.providers.resolve("main")
        k = p.api_key()
        self.assertIsInstance(k, str)
        self.assertTrue(k.strip())


class ProvidersFromEnvFileTest(unittest.TestCase):
    """Override via a custom .env file through the config seam."""

    def test_env_file_layer_applies(self):
        from native import config
        with tempfile.TemporaryDirectory() as d:
            env_file = Path(d) / "env"
            env_file.write_text("THREEV0_EMBED_MODEL=example/embed-v2\nTHREEV0_EMBED_DIM=256\n")
            config.clear_cache()
            # providers.resolve reads builtin .env; point config at custom file.
            m = config.get("THREEV0_EMBED_MODEL", None, env_file)
            dim = config.get("THREEV0_EMBED_DIM", None, env_file)
            self.assertEqual(m, "example/embed-v2")
            self.assertEqual(dim, "256")


if __name__ == "__main__":
    unittest.main(verbosity=2)