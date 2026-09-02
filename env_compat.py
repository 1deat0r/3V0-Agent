"""Prod-tree access to the canonical brand-env resolver (ADR-0006).

Single source of truth lives in ``3v0/core/env_compat.py``. The native core
is deliberately self-contained (``3v0/scripts`` put ONLY ``3v0/`` on
``sys.path``), so it cannot become an import dependency of prod code — and
``import 3v0.core`` is a SyntaxError regardless (identifiers cannot start
with a digit). This bridge loads the canonical file BY PATH and re-exports
its API, so prod consumers get the real resolver with no duplicated logic,
no ``sys.path`` mutation, and no generic top-level names.

ENV-FUNNEL consumers (#19/#20):

    from env_compat import branded_env

    timeout = float(branded_env("TUI_SLASH_TIMEOUT_S") or "45")

Note: unlike ``os.environ.get``, only TRUTHY values win — an empty-string
canonical value falls through to the legacy spelling, then to ``default``
(the canonical module's documented contract).
"""

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "_threev0_core_env_compat",
    Path(__file__).resolve().parent / "3v0" / "core" / "env_compat.py",
)
if _spec is None or _spec.loader is None:  # pragma: no cover - broken checkout
    raise ImportError("cannot locate 3v0/core/env_compat.py next to this bridge")
_loader = _spec.loader
_module = importlib.util.module_from_spec(_spec)
_loader.exec_module(_module)

branded_env = _module.branded_env
set_branded_env = _module.set_branded_env
pop_branded_env = _module.pop_branded_env

__all__ = ["branded_env", "set_branded_env", "pop_branded_env"]
