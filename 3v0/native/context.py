"""Native context assembly — SOUL + native memory -> system prompt.

Pure functions (files passed in, nothing touched), deterministic, testable.
No Hermes import. The native memory store (3v0/data/memory.json) is canonical.
"""
from __future__ import annotations

import json
from pathlib import Path


def read_soul(path: Path | str) -> str:
    p = Path(path)
    return p.read_text() if p.is_file() else ""


def read_active_memories(store: Path | str) -> list[str]:
    """Contents of non-superseded native-memory facts, in store order."""
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
