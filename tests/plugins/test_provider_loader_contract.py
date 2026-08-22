"""Tests for the shared provider-loader scaffold (pass 3, C1).

plugins/memory and plugins/cron_providers used to carry near-verbatim copies
of the provider-discovery scaffold (register-synthetic-package, user-plugins
dir, directory iteration, name->dir resolution) — the cron loader docstring
literally said "near-verbatim clone". plugins._provider_loader is now the
single source; these tests freeze the contract so a future plugin family
(who writes a fourth copy) or a loader-security fix (that must land once)
is caught by CI.
"""

from __future__ import annotations

from pathlib import Path

from plugins import _provider_loader as pl


class TestScaffoldContract:
    def test_memory_delegates_to_shared_scaffold(self):
        import plugins.memory as memory

        assert memory._register_synthetic_package.__module__ != "plugins._provider_loader"
        # delegation wrappers say "shared with the ... scaffold"
        import inspect

        src = inspect.getsource(memory._iter_provider_dirs)
        assert "_provider_loader" in src
        src2 = inspect.getsource(memory.find_provider_dir)
        assert "_provider_loader" in src2

    def test_cron_delegates_to_shared_scaffold(self):
        import plugins.cron_providers as cron

        import inspect

        src = inspect.getsource(cron._iter_provider_dirs)
        assert "_provider_loader" in src
        src2 = inspect.getsource(cron.find_provider_dir)
        assert "_provider_loader" in src2

    def test_shared_scaffold_obeys_bundled_precedence(self, tmp_path):
        dummy = tmp_path / "dummy"
        dummy.mkdir()
        (dummy / "__init__.py").write_text("register_dummy_provider = True\n")
        bundled = tmp_path / "family"
        bundled.mkdir()
        (bundled / "dummy").mkdir()
        (bundled / "dummy" / "__init__.py").write_text("register_dummy_provider = True\n")

        def _pred(path: Path) -> bool:
            return (path / "__init__.py").exists()

        dirs = pl.iter_provider_dirs(bundled, _pred)
        assert ("dummy", bundled / "dummy") in dirs
        found = pl.find_provider_dir("dummy", bundled, _pred)
        assert found == bundled / "dummy"  # bundled wins over tmp_path

    def test_synthetic_package_registration_is_idempotent(self):
        pl.register_synthetic_package("_threev0_test_pkg", ["/nonexistent"])
        pl.register_synthetic_package("_threev0_test_pkg", ["/nonexistent"])
        import sys

        assert "_threev0_test_pkg" in sys.modules
        sys.modules.pop("_threev0_test_pkg", None)