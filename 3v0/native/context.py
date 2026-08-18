"""Native context assembly — SOUL + native memory -> system prompt.

Pure helpers (files passed in, nothing touched) PLUS the retrieval-chosen
injection path (ADR-0004): the runtime's working set comes out of the canonical
SQLite store (memory.db) behind ONE seam, core/retrieval.inject — ranked by
keyword+recency+feedback, budget-shaped, spelling feedback back so injection
learns. No Hermes import.
"""
from __future__ import annotations

import json
from pathlib import Path


def read_soul(path: Path | str) -> str:
    p = Path(path)
    return p.read_text() if p.is_file() else ""


def read_active_memories(store: Path | str) -> list[str]:
    """Contents of non-superseded native-memory facts from the LEGACY JSON store,
    in store order. Kept for backward-compat + the JSON->SQLite migration; the
    runtime's live injection now uses build_system_from_store (SQLite seam)."""
    p = Path(store)
    if not p.is_file():
        return []
    try:
        data = json.loads(p.read_text())
    except Exception:
        return []
    if isinstance(data, dict):
        facts = data.get("facts", [])
    elif isinstance(data, list):
        facts = data
    else:
        facts = []
    out = []
    for f in facts:
        if isinstance(f, dict) and not f.get("superseded_by"):
            c = f.get("content")
            if isinstance(c, str) and c.strip():
                out.append(c.strip())
    return out


def _import_retrieval():
    """core.retrieval, robust to direct native/ script execution."""
    try:
        from core import retrieval          # normal: from 3v0/ root
    except ImportError:
        import core.retrieval as retrieval  # fallback if core isn't a package root
    return retrieval


def build_system_from_store(soul_text: str, conn=None, *,
                            domains=("3v0",), kind=None, budget_chars: int = 6000,
                            touch: bool = True, query_terms: tuple = (),
                            sep: str = "\n§\n") -> str:
    """Compose a system prompt from the soul + a RETRIEVAL-CHOSEN working set
    (ADR-0004). Opens the canonical memory.db when no conn is given; ranks the
    working set by keyword+recency+feedback and, when touch=True, writes the
    feedback counters so future injection reinforces what is actually pulled in.
    Returns the rendered prompt; len of the memory block <= budget_chars.
    """
    retrieval = _import_retrieval()
    own = conn is None
    if own:
        from core import memdb
        conn = memdb.connect()
    try:
        inj = retrieval.inject(
            conn, domains=domains, kind=kind, query_terms=query_terms,
            budget_chars=budget_chars, touch=touch, sep=sep,
        )
    finally:
        if own:
            conn.close()
    parts = []
    if soul_text.strip():
        parts.append(soul_text.strip())
    if inj.text:
        parts.append("[NATIVE MEMORY — retrieval-chosen working set]"
                     "\n-" + "\n- ".join(" " + x for x in inj.text.split(sep)))
    return "\n\n".join(parts)


def build_system(soul_text: str, memories: list[str], *, max_mem_chars: int = 6000) -> str:
    """Compose a system prompt from the soul plus active memory facts.

    Memory is trimmed to max_mem_chars so the prompt stays within a sane
    budget even as the store grows.
    """
    parts = []
    if soul_text.strip():
        parts.append(soul_text.strip())
    if memories:
        acc: list[str] = []
        used = 0
        for m in memories:
            if used + len(m) > max_mem_chars:
                break
            acc.append(m)
            used += len(m)
        parts.append("[NATIVE MEMORY — active facts]\n-" + "\n- ".join(" " + x for x in acc))
    return "\n\n".join(parts)
