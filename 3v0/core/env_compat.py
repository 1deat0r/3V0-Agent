"""Brand-compatible environment resolver (native core).

The body retains a legacy ``EV0_*`` runtime contract (gateway/launcher/profiles
set EV0_HOME today) and a ``THREEV0_*`` unit family, while the canonical brand
namespace is ``3V0_*`` (see 3v0/docs/adr/0006-env-compat-brand-namespace.md).

For a logical setting ``<NAME>`` this resolves, in order:
    3V0_<NAME>  ->  THREEV0_<NAME>  ->  EV0_<NAME>
(first truthy wins), so new code can adopt the brand namespace immediately
without breaking the live runtime, which still speaks the legacy vars.

New native-core code SHOULD use :func:`branded_env` instead of reading
``os.environ.get("EV0_*")`` directly. Do NOT write legacy vars from new code.
"""

from __future__ import annotations

import os
from typing import Optional

# Order matters: canonical brand first, legacy compat last.
_PREFIXES = ("3V0_", "EV0_")


def branded_env(name: str, default: Optional[str] = None) -> Optional[str]:
    """Return the first truthy value of 3V0_/THREEV0_/EV0_<name>.

    ``name`` is the logical suffix, e.g. ``branded_env("HOME")`` resolves
    ``3V0_HOME``, then legacy ``EV0_HOME``.
    """
    for prefix in _PREFIXES:
        value = os.environ.get(f"{prefix}{name}")
        if value:
            return value
    return default