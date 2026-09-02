"""Brand-compatible environment resolver (native core).

The body retains a legacy ``EV0_*`` runtime contract (gateway/launcher/profiles
set EV0_HOME today) while the canonical brand namespace is ``3V0_*`` (see
3v0/docs/adr/0006-env-compat-brand-namespace.md).

For a logical setting ``<NAME>`` this resolves, in order:
    3V0_<NAME>  ->  EV0_<NAME>
(first truthy wins; ``THREEV0_*`` has no production writer since the
ADR-0006 env collapse), so new code can adopt the brand namespace
immediately without breaking the live runtime, which still speaks the
legacy vars.

New native-core code SHOULD use :func:`branded_env` instead of reading
``os.environ.get("EV0_*")`` directly, and :func:`set_branded_env` /
:func:`pop_branded_env` instead of writing/popping either spelling — the
helpers keep the canonical and legacy aliases in lockstep (ticket #21
contract: env_compat is the only sanctioned env access path).
"""

from __future__ import annotations

import os
from typing import Optional

# Order matters: canonical brand first, legacy compat last.
_PREFIXES = ("3V0_", "EV0_")


def branded_env(name: str, default: Optional[str] = None) -> Optional[str]:
    """Return the first truthy value of ``3V0_<name>``, then legacy ``EV0_<name>``.

    ``name`` is the logical suffix, e.g. ``branded_env("HOME")`` resolves
    ``3V0_HOME``, then legacy ``EV0_HOME``. Only *truthy* values win (an
    empty string falls through to the next leg). ``THREEV0_*`` is NOT
    consulted — per ADR-0006 the namespace is exactly two spellings:
    ``3V0_`` (canonical) and ``EV0_`` (legacy read-compat).
    """
    for prefix in _PREFIXES:
        value = os.environ.get(f"{prefix}{name}")
        if value:
            return value
    return default


def set_branded_env(name: str, value: str) -> None:
    """Set a branded env var under BOTH spellings (the sanctioned write path).

    Writers must not pick a spelling: the canonical ``3V0_<name>`` and the
    legacy ``EV0_<name>`` alias are set together, so every reader resolves
    the same value regardless of which leg it consumes — in-tree readers
    via :func:`branded_env`, spawned processes and raw ``os.environ``
    readers via the legacy alias (contract: ticket #21). ``value`` must be
    a ``str`` (``os.environ`` requirement, unchanged).
    """
    os.environ[f"3V0_{name}"] = value
    os.environ[f"EV0_{name}"] = value


def pop_branded_env(name: str) -> None:
    """Remove a branded env var under BOTH spellings (counterpart to
    :func:`set_branded_env`). Missing keys are fine."""
    os.environ.pop(f"3V0_{name}", None)
    os.environ.pop(f"EV0_{name}", None)