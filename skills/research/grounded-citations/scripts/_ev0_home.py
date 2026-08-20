"""Resolve EV0_HOME for standalone skill scripts.

Skill scripts may run outside the 3V0 process (system Python, nix env,
CI) where ``ev0_constants`` is not importable.  This module provides the
same ``get_ev0_home()`` contract without requiring it on ``sys.path``.

When ``ev0_constants`` IS available it is used directly so profile
resolution and any future enhancements are picked up automatically.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from ev0_constants import get_ev0_home as get_ev0_home
except (ModuleNotFoundError, ImportError):

    def get_ev0_home() -> Path:
        """Return the 3V0 home directory (default: ``~/.3V0``)."""
        val = os.environ.get("EV0_HOME", "").strip()
        return Path(val) if val else Path.home() / ".3V0"
