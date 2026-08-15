"""3V0 core decide — the write half of 3V0's own actuator surface.

Direction 3 (own capabilities/tools) completes here. ``query.py`` is the read
half (views over the stores); this is the write half (decisions applied to the
memory store). A decision is a store-first mutation — record a fact (optionally
superseding an old one) or retract one — applied under the caller's
cross-process lock, returning a JSON-safe result the ``threev0_record`` tool
hands back to the agent.

Store-only by construction: ``decide()`` mutates ``MemoryStore`` and never
touches the profile. The CLI (``scripts/record.py``) re-exports the derived
view after a successful write, exactly as the store-first path has always done.
The skill axis is deliberately out of scope here — skill changes are
operational (they edit the SKILL.md Hermes actually loads) and go through
``skill_manage`` + the bridge; a store-first *skill* decision is a separate,
later stone.

Never raises: invalid input returns ``{"error": ...}`` so the tool surfaces a
refusal instead of crashing the subprocess. ``persist=False`` is the dry-run
mode (mutations land in memory only, nothing written to disk).
"""

from __future__ import annotations

from .memory import MemoryStore
from .query import fact_dict
from .record import RecordError, record

_VALID_KINDS = ("memory", "user", "identity", "directive")


def _record(store: MemoryStore, d: dict, source: str, persist: bool) -> dict:
    kind = (d.get("kind") or "").strip()
    content = (d.get("content") or "").strip()
    if kind not in _VALID_KINDS:
        return {"error": f"kind must be one of {list(_VALID_KINDS)}, got {kind!r}"}
    if not content:
        return {"error": "content is required for action='record'"}

    supersede_id = (d.get("fact_id") or "").strip() or None
    supersede_contains = (d.get("supersedes") or "").strip() or None
    try:
        result = record(
            store,
            content,
            kind,
            source,
            supersede_id=supersede_id,
            supersede_contains=supersede_contains,
            persist=persist,
        )
    except RecordError as e:
        return {"error": str(e)}

    return {
        "ok": True,
        "action": "record",
        "fact": fact_dict(result.fact),
        "superseded_ids": result.superseded_ids,
        "chain": [fact_dict(f) for f in result.chain],
    }


def _retract(store: MemoryStore, d: dict, source: str, persist: bool) -> dict:
    fact_id = (d.get("fact_id") or "").strip()
    if not fact_id:
        return {"error": "fact_id is required for action='retract'"}
    existing = store.get(fact_id)
    if existing is None:
        return {"error": f"no fact with id {fact_id!r}"}
    if not existing.active:
        return {
            "error": f"fact {fact_id!r} is already inactive "
            "(superseded or retracted); nothing to retract",
        }
    retracted = store.retract(fact_id, source=source, persist=persist)
    if retracted is None:  # pragma: no cover - guarded by the active check above
        return {"error": f"could not retract {fact_id!r}"}
    return {
        "ok": True,
        "action": "retract",
        "fact": fact_dict(retracted),
        "chain": [fact_dict(f) for f in store.history(fact_id)],
    }


def decide(store: MemoryStore, decision: dict, persist: bool = True) -> dict:
    """Apply one store-first decision and return a JSON-safe result.

    decision:
      action: "record" | "retract"
        record  -> kind (required), content (required); optionally supersede
                   via fact_id (exact id) or supersedes (exactly-one substring)
        retract -> fact_id (required)
      source  -> optional provenance label (default "foreground")

    The caller holds the cross-process lock (``store.mutate()``). Nothing is
    ever destroyed: superseded/retracted facts stay recoverable via
    ``history()``. ``persist=False`` computes the result without writing disk.
    """
    action = (decision.get("action") or "").strip()
    source = (decision.get("source") or "").strip() or "foreground"

    if action == "record":
        return _record(store, decision, source, persist)
    if action == "retract":
        return _retract(store, decision, source, persist)
    return {"error": f"unknown action {action!r} (expected 'record' or 'retract')"}
