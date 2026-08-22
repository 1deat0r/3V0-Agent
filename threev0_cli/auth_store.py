"""Owned storage seam for the auth.json credential store (ticket #14).

3V0's credential system reads/writes ``auth.json`` (and provider state inside
it) from several places: the auth module itself, the credential pool
(``agent/credential_pool.py``), and the credential-source removal contract
(``agent/credential_sources.py``). Historically those external callers reached
for underscore-private functions in ``threev0_cli.auth`` — a de-facto public
boundary owned by no seam.

This module is that seam. It re-exports the auth-store primitives under
stable public names. The implementations stay in ``threev0_cli.auth`` (they
depend on auth-internal locking, path resolution, and config state); this
module only owns the NAMES so callers outside auth/ stop importing privates
and the storage boundary can evolve without breaking them.

Stable surface:

- ``auth_store_lock``   — cross-process advisory lock for one read/write txn
- ``load_auth_store``   — read auth.json (fail-loud on unreadable store)
- ``save_auth_store``   — write auth.json (atomic, credential-safe)
- ``load_provider_state`` / ``save_provider_state`` / ``store_provider_state``
- ``global_auth_file_path``
"""
from __future__ import annotations

from threev0_cli.auth import (
    _auth_store_lock as auth_store_lock,
    _global_auth_file_path as global_auth_file_path,
    _load_auth_store as load_auth_store,
    _load_provider_state as load_provider_state,
    _save_auth_store as save_auth_store,
    _save_provider_state as save_provider_state,
    _store_provider_state as store_provider_state,
    _load_provider_state_with_source as load_provider_state_with_source,
)

__all__ = [
    "auth_store_lock",
    "global_auth_file_path",
    "load_auth_store",
    "load_provider_state",
    "load_provider_state_with_source",
    "save_auth_store",
    "save_provider_state",
    "store_provider_state",
]