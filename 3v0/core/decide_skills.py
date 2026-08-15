"""3V0 core decide_skills — the store-first skill decision layer (Stone 8).

The skill half of 3V0's own actuator surface. ``decide.py`` made *facts*
writable store-first; this does the same for *skills*. A decision is a
store-first mutation applied to the ``SkillStore`` — append a content version
(``skill_update``, superseding the active one), decommission with no successor
(``skill_retract``), or fold into an umbrella (``skill_absorb``) — returning a
JSON-safe result the ``threev0_record`` tool and the session-end review driver
hand back to the agent.

Store-only by construction: ``decide_skill()`` mutates ``SkillStore`` and never
touches the profile. The CLI (``scripts/record_skills.py``) projects the
derived view — writes the SKILL.md for an update, removes the skill directory
for a decommission — after a successful write, exactly as ``scripts/record.py``
does for memory. Nothing is ever destroyed: superseded/retracted/absorbed
versions stay recoverable via ``history()``.

Never raises: invalid input returns ``{"error": ...}`` so the tool surfaces a
refusal instead of crashing the subprocess. ``persist=False`` is the dry-run
mode (mutations land in memory only, nothing written to disk).
"""

from __future__ import annotations

from .query import version_dict
from .skills import SkillStore

_VALID_ACTIONS = ("skill_update", "skill_retract", "skill_absorb")


def _update(store: SkillStore, d: dict, source: str, persist: bool) -> dict:
    name = (d.get("name") or "").strip()
    content = (d.get("content") or "").strip()
    if not name:
        return {"error": "name is required for action='skill_update'"}
    if not content:
        return {"error": "content (full SKILL.md) is required for action='skill_update'"}

    category = (d.get("category") or "").strip()
    note = (d.get("note") or "").strip()
    version = store.add(
        name,
        "edit",
        source,
        content=content,
        category=category,
        note=note,
        persist=persist,
    )
    return {
        "ok": True,
        "action": "skill_update",
        "skill": version_dict(version, include_content=True),
        "superseded_ids": list(version.supersedes),
        "chain": [version_dict(v, include_content=True) for v in store.history(name)],
    }


def _retract(store: SkillStore, d: dict, source: str, persist: bool) -> dict:
    name = (d.get("name") or "").strip()
    if not name:
        return {"error": "name is required for action='skill_retract'"}
    if store.latest_active(name) is None:
        return {"error": f"no active skill named {name!r} to retract"}
    retracted = store.retract(name, source=source, persist=persist)
    if retracted is None:  # pragma: no cover - guarded by the active check above
        return {"error": f"could not retract {name!r}"}
    return {
        "ok": True,
        "action": "skill_retract",
        "skill": version_dict(retracted, include_content=True),
        "chain": [version_dict(v, include_content=True) for v in store.history(name)],
    }


def _absorb(store: SkillStore, d: dict, source: str, persist: bool) -> dict:
    name = (d.get("name") or "").strip()
    absorbed_into = (d.get("absorbed_into") or "").strip()
    if not name:
        return {"error": "name is required for action='skill_absorb'"}
    if not absorbed_into:
        return {"error": "absorbed_into is required for action='skill_absorb'"}
    if store.latest_active(name) is None:
        return {"error": f"no active skill named {name!r} to absorb"}
    absorbed = store.absorb(name, absorbed_into, source=source, persist=persist)
    if absorbed is None:  # pragma: no cover - guarded by the active check above
        return {"error": f"could not absorb {name!r}"}
    return {
        "ok": True,
        "action": "skill_absorb",
        "skill": version_dict(absorbed, include_content=True),
        "absorbed_into": absorbed_into,
        "chain": [version_dict(v, include_content=True) for v in store.history(name)],
    }


def decide_skill(store: SkillStore, decision: dict, persist: bool = True) -> dict:
    """Apply one store-first skill decision and return a JSON-safe result.

    decision:
      action: "skill_update" | "skill_retract" | "skill_absorb"
        skill_update -> name + content (full SKILL.md) required; optional
                        category (subdir for a new skill) and note
        skill_retract-> name required (decommission with no successor)
        skill_absorb -> name + absorbed_into required (fold into an umbrella)
      source  -> optional provenance label (default "foreground")

    The caller holds the cross-process lock (``store.mutate()``). Nothing is
    ever destroyed: superseded/retracted/absorbed versions stay recoverable via
    ``history()``. ``persist=False`` computes the result without writing disk.
    """
    action = (decision.get("action") or "").strip()
    source = (decision.get("source") or "").strip() or "foreground"

    if action == "skill_update":
        return _update(store, decision, source, persist)
    if action == "skill_retract":
        return _retract(store, decision, source, persist)
    if action == "skill_absorb":
        return _absorb(store, decision, source, persist)
    return {
        "error": (
            f"unknown action {action!r} (expected one of {list(_VALID_ACTIONS)})"
        )
    }
