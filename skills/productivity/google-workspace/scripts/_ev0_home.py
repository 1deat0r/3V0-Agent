"""Resolve EV0_HOME for standalone skill scripts.

Skill scripts may run outside the 3V0 process (e.g. system Python,
nix env, CI) where ``threev0_constants`` is not importable.  This module
provides the same ``get_ev0_home()`` and ``display_threev0_home()``
contracts as ``threev0_constants`` without requiring it on ``sys.path``.

When ``threev0_constants`` IS available it is used directly so that any
future enhancements (profile resolution, Docker detection, etc.) are
picked up automatically.  The fallback path replicates the core logic
from ``threev0_constants.py`` using only the stdlib.

All scripts under ``google-workspace/scripts/`` should import from here
instead of duplicating the ``EV0_HOME = Path(os.getenv(...))`` pattern.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from threev0_constants import display_threev0_home as display_threev0_home
    from threev0_constants import get_threev0_home as get_threev0_home
except (ModuleNotFoundError, ImportError):

    def get_threev0_home() -> Path:
        """Return the 3V0 home directory (default: ~/.3V0).

        Mirrors ``threev0_constants.get_ev0_home()``."""
        val = os.environ.get("EV0_HOME", "").strip()
        return Path(val) if val else Path.home() / ".3V0"

    def display_threev0_home() -> str:
        """Return a user-friendly ``~/``-shortened display string.

        Mirrors ``threev0_constants.display_threev0_home()``."""
        home = get_threev0_home()
        try:
            return "~/" + str(home.relative_to(Path.home()))
        except ValueError:
            return str(home)
