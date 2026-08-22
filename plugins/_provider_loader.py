"""Generic provider-plugin discovery loader (architecture-review pass 3, C1).

Bundled/platform plugin families (memory, cron_providers, ...) each need the
same discovery scaffold: register a synthetic package shell so user-installed
plugins can import, scan bundled → user → project directories for provider
directories, and resolve a provider name to its directory. Before this module
existed, ``plugins/memory/__init__.py`` and ``plugins/cron_providers/__init__.py``
carried near-verbatim copies of these functions (the cron loader's own docstring
said "near-verbatim clone"), and the two copies had already drifted.

This module is the single source for the generic scaffold. Each plugin family
keeps its own *predicate* (what makes a directory a provider of its kind) and
its own *loaders* (how an instance is extracted); those are passed in as
arguments so behavior stays family-specific. Loader security fixes and
directory-scan policy changes land here once.

Design (deep module): the interface is small — four functions, each taking the
family's bundled dir + predicate — while the scan/precedence/import-safety
mechanics stay inside. Callers get leverage (one scaffold, N families);
maintainers get locality (scan policy in one place).
"""

from __future__ import annotations

import importlib
import importlib.machinery
import importlib.util
import sys
from pathlib import Path
from typing import Callable, List, Optional, Tuple

# A predicate deciding whether a directory is a provider of the given family.
ProviderDirPredicate = Callable[[Path], bool]


def register_synthetic_package(name: str, search_locations: List[str]) -> None:
    """Register an empty package shell in sys.modules.

    User-installed providers import under a synthetic package root (e.g.
    ``_threev0_user_memory.<name>``), a dotted name whose parents exist
    nowhere on disk. Unless those parents are present in ``sys.modules``,
    any relative import inside the plugin (``from . import config``) fails
    with ``ModuleNotFoundError`` — the same reason the loader also registers
    the plugin family's bundled package.
    """
    if name in sys.modules:
        return
    spec = importlib.machinery.ModuleSpec(name, None, is_package=True)
    spec.submodule_search_locations = search_locations
    sys.modules[name] = importlib.util.module_from_spec(spec)


def get_user_plugins_dir() -> Optional[Path]:
    """Return ``$3V0_HOME/plugins/`` or None if unavailable."""
    try:
        from threev0_constants import get_threev0_home

        d = get_threev0_home() / "plugins"
        return d if d.is_dir() else None
    except Exception:
        return None


def iter_provider_dirs(
    bundled_dir: Path,
    is_provider_dir: ProviderDirPredicate,
    *,
    project_dir: Optional[Callable[[], Optional[Path]]] = None,
) -> List[Tuple[str, Path]]:
    """Yield ``(name, path)`` for all discovered provider directories.

    Scans bundled, then user-installed (``$3V0_HOME/plugins/``), then
    project-local when a ``project_dir`` provider is given. Bundled takes
    precedence on name collisions (first-seen wins via ``seen`` set).
    """
    seen: set = set()
    dirs: List[Tuple[str, Path]] = []

    # 1. Bundled providers (plugins/<family>/<name>/)
    if bundled_dir.is_dir():
        for child in sorted(bundled_dir.iterdir()):
            if not child.is_dir() or child.name.startswith(("_", ".")):
                continue
            if not (child / "__init__.py").exists():
                continue
            seen.add(child.name)
            dirs.append((child.name, child))

    # 2. User-installed providers ($3V0_HOME/plugins/<name>/)
    # 3. Project-local providers (./.3V0/plugins/<name>/), opt-in
    for source_dir in (get_user_plugins_dir(), project_dir() if project_dir else None):
        if not source_dir:
            continue
        for child in sorted(source_dir.iterdir()):
            if not child.is_dir() or child.name.startswith(("_", ".")):
                continue
            if child.name in seen:
                continue  # earlier source wins
            if not is_provider_dir(child):
                continue  # skip non-family plugins
            seen.add(child.name)
            dirs.append((child.name, child))

    return dirs


def find_provider_dir(
    name: str,
    bundled_dir: Path,
    is_provider_dir: ProviderDirPredicate,
    *,
    project_dir: Optional[Callable[[], Optional[Path]]] = None,
    extra_resolver: Optional[Callable[[str], Optional[Path]]] = None,
) -> Optional[Path]:
    """Resolve a provider name to its directory.

    Checks bundled first, then user-installed, then (optionally) project-local
    and an ``extra_resolver`` (e.g. pip entry-point resolution). Bundled takes
    precedence on name collisions.
    """
    bundled = bundled_dir / name
    if bundled.is_dir() and (bundled / "__init__.py").exists():
        return bundled
    for source_dir in (get_user_plugins_dir(), project_dir() if project_dir else None):
        if not source_dir:
            continue
        candidate = source_dir / name
        if candidate.is_dir() and is_provider_dir(candidate):
            return candidate
    if extra_resolver is not None:
        return extra_resolver(name)
    return None