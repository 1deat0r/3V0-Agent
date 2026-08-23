"""SkillForge — synthesize reusable skill *proposals* from the body's own core.

SkillForge (arXiv 2608.18933, kernel #6 of the 08-22 research digest) is the
"create half" of the skill axis: the agent proactively acquires project-
specific knowledge by distilling reusable skills from the codebase it actually
owns, rather than waiting for a real-task failure. In 3V0 this runs against the
3V0 body's own ``core/`` — a module whose public API encodes a proven method is
the seed for a durable skill.

This module is the pure, deterministic front half: given a module's public
surface (its ``__doc__`` and one-line docstrings for callables), it produces a
*proposal* — the metadata + outline a model would flesh into a real SKILL.md.
It does NOT author final content or write the store; the driver passes the
proposal to the review/forge model for the actual SKILL.md (gated, like
curation). No I/O, no LLM, deterministic.
"""

from __future__ import annotations

import ast
import hashlib
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def load_module_public_api(source_path: Path):
    """Return the module's public top-level callables ``(name, doc)``.

    Pure and deterministic: we PARSE the file with ``ast`` and collect top-
    level ``def``/``async def``/``class`` nodes whose name does not start with
    ``_``, along with their immediately-following docstring (as the first S3
    token). This never imports or execs the module — no side effects, no
    module-registration traps (dataclass ``cls.__module__`` resolution, stale
    ``sys.modules``), and no risk from running arbitrary body code during a
    pure synthesis. Returns [] on any failure (e.g. non-Python file).
    """
    try:
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
    except Exception:
        return []
    out: List[Tuple[str, Optional[str]]] = []
    # Walk MODULE-LEVEL definitions only (not nested methods/properties) —
    # "public callables" means the module's own surface.
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if node.name.startswith("_"):
            continue
        doc = ast.get_docstring(node)
        out.append((node.name, doc))
    return out


def _slugify(name: str) -> str:
    """A kebab-case slug for a skill name from a module identifier."""
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "skill"


def _category_from_path(source_path: Path) -> str:
    """A skill category from the source module's location (e.g. core -> core)."""
    return source_path.parent.name or "general"


def overview_from_doc(doc: Optional[str], limit: int = 900) -> str:
    """The first paragraph of a docstring, normalized, as the skill's overview."""
    if not doc:
        return ""
    text = doc.strip().split("\n\n", 1)[0].strip()
    return text[:limit]


def synthesize_proposal(
    source_path: Path,
    *,
    name: Optional[str] = None,
    category: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Build a skill *proposal* from a module's public API.

    Returns a dict with ``name``, ``category``, ``description``, ``overview``,
    and a deterministically-derived ``proposal_id`` (so a driver can dedupe /
    skip already-distilled modules). Returns None when the module has no
    public callables to distill, or when loading/parsing fails.
    """
    api = load_module_public_api(source_path)
    if not api:
        return None
    names = [n for n, _ in api]
    docs = [d.strip().split("\n", 1)[0] for _, d in api if d]

    # A human-description line: the module docstring, else the first callable
    # docstring's first line. AST-parsed (never imports the module).
    mod_doc = ""
    try:
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        mod_doc = ast.get_docstring(tree) or ""
    except Exception:
        pass

    first_line = (
        (mod_doc.strip().split("\n", 1)[0] if mod_doc else "")
        or (docs[0] if docs else "")
        or f"Reusable method from {source_path.parent.name} core"
    )
    description = first_line[:120]

    digest = hashlib.sha256(
        str(source_path.resolve()).encode() + b"\x00" + "\n".join(names).encode()
    ).hexdigest()[:12]

    return {
        "name": name or _slugify(source_path.stem),
        "category": category or _category_from_path(source_path),
        "description": description,
        "overview": overview_from_doc(mod_doc),
        "public_callables": names,
        "callable_docs": {n: d for n, d in api},
        "proposal_id": f"forge-{_slugify(source_path.stem)}-{digest}",
    }