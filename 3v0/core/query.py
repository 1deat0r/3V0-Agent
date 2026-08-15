"""3V0 core query — read-only views over the native stores.

Direction 3 (own capabilities/tools) begins here: the *read* half of 3V0's own
actuator surface. The memory and skill stores are canonical and lineage-bearing,
but at runtime 3V0 only ever sees the derived profile projection (MEMORY.md /
USER.md, the live SKILL.md files) — the supersession history, provenance, and
curator states are invisible except by shelling out through the terminal tool.
This module exposes them as plain, JSON-serializable dicts so the
``native-store-bridge`` profile plugin can serve them as a first-class tool
(``threev0_store``).

Read-only by construction: it imports ``MemoryStore`` / ``SkillStore`` and calls
only their query methods. Nothing here mutates either store, so it is safe to
call at any time, including mid-turn.

Design mirrors the rest of the core: stdlib only, no profile I/O (the stores'
JSON files are opened by the stores themselves, exactly as ``sync.py`` /
``record.py`` do), and the ``§`` wire format is never touched here.
"""

from __future__ import annotations

from .memory import MemoryStore
from .skills import SkillStore

# Cap on inline content in list/history views. The stores record full SKILL.md
# content per version; surfacing all of it would flood context. Longer content
# is truncated and flagged so the caller can read_file() the live copy when it
# needs the actual text. Facts are short and always returned in full.
CONTENT_CAP = 2000


def fact_dict(f) -> dict:
    """A JSON-safe view of one fact (memory axis)."""
    return {
        "id": f.id,
        "kind": f.kind,
        "content": f.content,
        "source": f.source,
        "created_at": f.created_at,
        "supersedes": list(f.supersedes),
        "superseded_by": f.superseded_by,
        "active": f.active,
        "note": f.note,
    }


def _content_view(content: str) -> dict:
    """A bounded view of (potentially large) skill content."""
    if len(content) <= CONTENT_CAP:
        return {"content": content, "truncated": False}
    return {
        "content": content[:CONTENT_CAP],
        "truncated": True,
        "content_len": len(content),
    }


def version_dict(v, include_content: bool) -> dict:
    """A JSON-safe view of one skill version (skill axis).

    ``include_content`` is False for list views (metadata only, keeps context
    light) and True for a targeted ``skill_history`` of one named skill.
    """
    d = {
        "id": v.id,
        "name": v.name,
        "action": v.action,
        "category": v.category,
        "file_path": v.file_path,
        "source": v.source,
        "created_at": v.created_at,
        "supersedes": list(v.supersedes),
        "superseded_by": v.superseded_by,
        "absorbed_into": v.absorbed_into,
        "active": v.active,
        "terminal": v.terminal,
        "note": v.note,
        "content_len": len(v.content),
    }
    if include_content:
        d.update(_content_view(v.content))
    return d


def summary(mem: MemoryStore, skl: SkillStore) -> dict:
    """Overview of both stores: fact counts by kind, skill/version counts,
    and each active skill's current curator state."""
    by_kind: dict[str, int] = {}
    for f in mem.active():
        by_kind[f.kind] = by_kind.get(f.kind, 0) + 1
    active_skills = skl.active()
    return {
        "facts": by_kind,
        "fact_versions": len(mem.facts),  # includes superseded (the audit trail)
        "active_skills": len(active_skills),
        "skill_versions": len(skl.skills),
        "skill_states": {s.name: skl.state(s.name) for s in active_skills},
    }


def facts(mem: MemoryStore, kind: str | None = None) -> list[dict]:
    """Active facts, optionally restricted to one kind (memory/user/identity/directive)."""
    return [fact_dict(f) for f in mem.active(kind=kind)]


def fact_history(mem: MemoryStore, fact_id: str) -> list[dict]:
    """The full supersession lineage of one fact, oldest -> newest (empty if unknown)."""
    return [fact_dict(f) for f in mem.history(fact_id)]


def skills(skl: SkillStore, name: str | None = None) -> list[dict]:
    """Active skills (one per live name), metadata-only, each with its curator state.

    Pass ``name`` to restrict to a single skill.
    """
    active = skl.active()
    if name:
        active = [s for s in active if s.name == name]
    out = []
    for s in active:
        d = version_dict(s, include_content=False)
        d["state"] = skl.state(s.name)
        out.append(d)
    return out


def skill_history(skl: SkillStore, name: str) -> list[dict]:
    """The full recorded version lineage of one skill, oldest first, with content."""
    return [version_dict(v, include_content=True) for v in skl.history(name)]
