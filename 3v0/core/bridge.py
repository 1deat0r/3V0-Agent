"""Map 3V0 memory-tool operations onto the native store.

The 3V0 ``memory`` tool writes MEMORY.md / USER.md directly; the bridge
replays those same add/replace/remove operations against the native store so
the store stays the canonical origin and the profile remains a derived view.

The bridge is the store side of the store-first memory loop (see
``3v0/EVOLUTION_LOOP.md``). It is called by ``scripts/ingest.py``, which is
itself invoked as a best-effort subprocess by the ``native-store-bridge``
profile plugin's ``post_tool_call`` hook.

Mapping:

- ``add``      -> ``store.add(content, kind, source)`` if not already active
                  (idempotent).
- ``replace``  -> supersede the **exactly one** active fact containing
                  ``old_text`` (via ``record``, linking old -> new). Zero or
                  multiple matches -> plain ``add`` of the new content (never
                  a guessed supersession link).
- ``remove``   -> retract the **exactly one** active fact containing
                  ``old_text``. Zero or multiple -> skip.

Skipped/ambiguous operations self-heal at the next wake sync, which reconciles
store and profile idempotently — the only cost is that provenance degrades to
``profile-import`` instead of the exact origin.
"""

from __future__ import annotations

from .memory import PROFILE_KINDS, MemoryStore
from .profile_io import contains_separator
from .record import RecordError, record


def _active_contents(store: MemoryStore, kind: str) -> set[str]:
    return {f.content for f in store.active(kind=kind)}


def apply_ops(
    store: MemoryStore,
    target: str,
    ops: list[dict],
    source: str,
) -> int:
    """Replay memory-tool operations against the store. Returns count applied.

    Each op is applied independently; a bad op (unknown action, missing field,
    separator-containing content) is skipped without failing the rest.
    """
    if target not in PROFILE_KINDS:
        raise ValueError(f"target must be one of {sorted(PROFILE_KINDS)}, got {target!r}")
    kind = target
    applied = 0

    for op in ops or []:
        if not isinstance(op, dict):
            continue
        action = op.get("action")
        # The 3V0 memory tool accepts `new_text` as an alias for `content`
        # (both in the single-op and batch `operations` shapes). Honor both so
        # a `replace`/`add` carrying the alias is not silently dropped (which
        # would degrade to a duplicate at the next wake sync).
        content = (op.get("content") or op.get("new_text") or "").strip()
        old_text = (op.get("old_text") or "").strip()

        try:
            if action == "add":
                if (
                    content
                    and not contains_separator(content)
                    and content not in _active_contents(store, kind)
                ):
                    store.add(content, kind, source)
                    applied += 1

            elif action == "replace":
                if not content:
                    continue
                if old_text:
                    matches = store.matching(kind, old_text)
                    if len(matches) == 1:
                        record(store, content, kind, source, supersede_id=matches[0].id)
                        applied += 1
                        continue
                    if len(matches) > 1:
                        # Ambiguous: never guess which fact to supersede. Skip;
                        # the wake sync reconciles store<->profile idempotently.
                        continue
                # No old_text, or zero matches -> plain add of the new content.
                if (
                    not contains_separator(content)
                    and content not in _active_contents(store, kind)
                ):
                    store.add(content, kind, source)
                    applied += 1

            elif action == "remove":
                if not old_text:
                    continue
                matches = store.matching(kind, old_text)
                if len(matches) == 1:
                    store.retract(matches[0].id, source=source)
                    applied += 1

            # unknown action -> ignore (never fail the whole batch)
        except (RecordError, ValueError):
            # e.g. separator-containing content refused by record(); skip and
            # let the wake sync reconcile.
            continue

    return applied
