"""Generic provider registry primitive (architecture-review pass 4, C2).

Four registries — ``agent/browser_registry.py``, ``agent/web_search_registry.py``,
``agent/image_gen_registry.py``, ``agent/secret_sources/registry.py`` — used to
hand-copy the same mechanical core:

- ``_providers`` / ``_scoped_providers`` dicts guarded by a ``threading.Lock``
- ``register_provider`` (type-checked) / ``list_providers`` (sorted) /
  ``get_provider`` (scoped-first, global fallback) /
  ``snapshot_registration`` / ``restore_registration`` (identity-guarded) /
  ``registry_generation`` /
  ``_reset_for_tests``

That copied core drifted: web_search grew ``capability`` and disabled-plugin
handling the others lack. This module provides the generic, tested-once core;
each registry becomes a thin adapter that keeps its *resolution policy* (the
part that genuinely differs: selection precedence, capability routing,
config keys) and delegates the mechanical shape here.

The registry is intentionally untyped at the provider level: it stores
arbitrary provider objects passed by the adapter, which enforces its own
type guard. ``type_check`` is an optional callable applied in
``register_provider`` so the adapter keeps the same fail-fast behavior
it had inlined.
"""

from __future__ import annotations

import logging
import threading
from typing import Callable, Dict, List, Optional

from threev0_constants import threev0_home_key

logger = logging.getLogger(__name__)


class ProviderRegistry:
    """Thread-safe provider registration map with scoped snapshots.

    ``scope=None`` targets the global map; a named scope targets the
    per-profile map (keyed by the canonical home key so a provider installed
    for another profile never leaks into this one).
    """

    def __init__(
        self,
        *,
        family: str,
        type_check: Optional[Callable[[object], bool]] = None,
    ) -> None:
        self._family = family
        self._type_check = type_check
        self._providers: Dict[str, object] = {}
        self._scoped_providers: Dict[str, Dict[str, object]] = {}
        self._generation = 0
        self._scoped_generations: Dict[str, int] = {}
        self._lock = threading.Lock()

    def _target(self, scope: Optional[str], *, create: bool = False) -> Dict[str, object]:
        if scope is None:
            return self._providers
        if create:
            return self._scoped_providers.setdefault(scope, {})
        return self._scoped_providers.get(scope, {})

    def register_provider(self, provider: object, *, scope: Optional[str] = None) -> None:
        """Register a provider; re-registration overwrites and logs."""
        if self._type_check is not None and not self._type_check(provider):
            raise TypeError(
                f"register_provider() on {self._family} expects a valid "
                f"provider instance, got {type(provider).__name__}"
            )
        raw_name = getattr(provider, "name", None)
        if not isinstance(raw_name, str) or not raw_name.strip():
            raise ValueError(f"{self._family} provider .name must be a non-empty string")
        name = raw_name.strip()
        with self._lock:
            target = self._target(scope, create=True)
            existing = target.get(name)
            target[name] = provider
            if scope is None:
                self._generation += 1
            else:
                self._scoped_generations[scope] = self._scoped_generations.get(scope, 0) + 1
        if existing is not None:
            logger.debug(
                "%s provider '%s' re-registered (was %r)",
                self._family, name, type(existing).__name__,
            )
        else:
            logger.debug(
                "Registered %s provider '%s' (%s)",
                self._family, name, type(provider).__name__,
            )

    def list_providers(self, *, scope: Optional[str] = None) -> List[object]:
        """Return all registered providers, sorted by name.

        Merges the global map with the scoped map (defaulting to the
        canonical home key, matching the historic registries' semantics:
        ``scope or threev0_home_key()`` for lookup).
        """
        scoped_key = scope or threev0_home_key()
        with self._lock:
            merged = dict(self._providers)
            merged.update(self._scoped_providers.get(scoped_key, {}))
            items = list(merged.values())
        return sorted(items, key=lambda p: getattr(p, "name", ""))

    def get_provider(self, name: str, *, scope: Optional[str] = None) -> Optional[object]:
        """Return the provider registered under *name*, or None.

        Scoped lookup first (default home key), then the global map — the
        historic precedence.
        """
        if not isinstance(name, str):
            return None
        scoped_key = scope or threev0_home_key()
        with self._lock:
            key = name.strip()
            scoped = self._scoped_providers.get(scoped_key, {}).get(key)
            if scoped is not None:
                return scoped
            return self._providers.get(key)

    def snapshot_registration(self, name: str, *, scope: Optional[str] = None) -> Optional[object]:
        """Return the currently-registered provider (for plugin unload)."""
        with self._lock:
            return self._target(scope).get(name.strip())

    def restore_registration(
        self,
        name: str,
        current: object,
        previous: Optional[object],
        *,
        scope: Optional[str] = None,
    ) -> bool:
        """Restore *previous* only when *current* is still installed."""
        key = name.strip()
        with self._lock:
            target = self._target(scope, create=True)
            if target.get(key) is not current:
                return False
            if previous is None:
                target.pop(key, None)
            else:
                target[key] = previous
            # A restore is a registration change: bump generation so
            # generation-keyed cache fingerprints observe it (browser_registry
            # did this historically; the generic must too).
            if scope is None:
                self._generation += 1
            else:
                self._scoped_generations[scope] = self._scoped_generations.get(scope, 0) + 1
            if scope is not None and not target:
                self._scoped_providers.pop(scope, None)
        return True

    def snapshot_all(self) -> Dict[str, object]:
        """Return the merged (global + canonical-home-scoped) provider map.

        Used by resolution policies that need a consistent point-in-time
        view without touching module internals.
        """
        scoped_key = threev0_home_key()
        with self._lock:
            merged = dict(self._providers)
            merged.update(self._scoped_providers.get(scoped_key, {}))
            return merged

    def registry_generation(self, *, scope: Optional[str] = None) -> tuple:
        """Return a (global, scoped) generation counter for change detection."""
        with self._lock:
            return (
                self._generation,
                self._scoped_generations.get(scope or threev0_home_key(), 0),
            )

    def reset_for_tests(self) -> None:
        """Clear all registrations (test seam).

        Bumps the global generation (instead of zeroing it) to preserve the
        historic monotonic contract: cache fingerprints must observe the
        reset, so later generations differ from any generated before it.
        """
        with self._lock:
            self._providers.clear()
            self._scoped_providers.clear()
            self._scoped_generations.clear()
            self._generation += 1