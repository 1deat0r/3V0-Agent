"""Store -> profile projection — the derived view is written here, once.

The "profile is a derived view" write (emit MEMORY.md / USER.md from the
store's active facts) used to be re-implemented across four scripts, one of
which (export_to_profile.py) bypassed ``core.sync.profile_text`` and called
``join_entries`` directly — so a change to the projection would silently miss
one path. This module is that projection's single owner.
"""

from __future__ import annotations

from pathlib import Path

from .memory import MemoryStore
from .sync import profile_text

_KIND_FILE = {"memory": "MEMORY.md", "user": "USER.md"}


def project_memory(store: MemoryStore, profile_dir: Path) -> list[str]:
    """Write MEMORY.md / USER.md as the store's derived view.

    Returns the written filenames (memory, user order). Creates the profile
    dir if missing.
    """
    profile_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for kind, fname in _KIND_FILE.items():
        (profile_dir / fname).write_text(profile_text(store, kind), encoding="utf-8")
        written.append(fname)
    return written
