"""Map Hermes skill_manage operations onto the native skill store.

The Hermes ``skill_manage`` tool writes SKILL.md / supporting files into the
profile; the bridge replays those same operations against the native skill
store so the store stays the auditable record of 3V0's skill evolution and
the profile remains the operational system. This is the skill half of the
store-first evolution loop (see ``3v0/EVOLUTION_LOOP.md``), mirroring
``core/bridge.py`` for memory.

Mapping (``action`` -> store effect):

- ``create``     -> append a version (full SKILL.md), starting/continuing the
                    lineage. Idempotent: a create whose content already equals
                    the active version is skipped (double-observation guard).
- ``patch``      -> append a version. The ``note`` records the old->new snippet
                    so the lineage shows the edit; if the caller supplies the
                    resulting SKILL.md as ``content`` (the ingest script reads
                    it from the profile after the patch), the version carries
                    full content too and is projectable.
- ``edit``       -> append a version with the full new SKILL.md.
- ``write_file`` -> append a version carrying the supporting file's content
                    and path (references/, scripts/, templates/).
- ``remove_file``-> append a version recording the removed file.
- ``delete``     -> terminal. With ``absorbed_into`` -> ``absorb`` (consolidation);
                    without -> ``retract`` (pure prune). Both recoverable.

Every non-terminal action supersedes the current active version of the skill
(if any); a first write to a skill the store has never seen simply starts a
lineage (no supersession link). Nothing is destroyed.
"""

from __future__ import annotations

from typing import Any

from .skills import ACTIONS, SkillStore
_TERMINAL = "delete"


def _truncate(text: Any, limit: int = 200) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def apply_skill_op(store: SkillStore, args: Any, source: str) -> int:
    """Replay one skill_manage write against the store. Returns 1 if applied, 0 if skipped."""
    if not isinstance(args, dict):
        return 0
    action = args.get("action")
    name = (args.get("name") or "").strip()
    if not name or action not in ACTIONS:
        return 0

    if action == _TERMINAL:
        absorbed_into = (args.get("absorbed_into") or "").strip()
        if absorbed_into:
            return 1 if store.absorb(name, absorbed_into, source=source) else 0
        return 1 if store.retract(name, source=source) else 0

    category = (args.get("category") or "").strip()
    file_path = (args.get("file_path") or "").strip()
    content = ""
    note = ""

    if action in ("create", "edit"):
        content = (args.get("content") or "").strip()
    elif action == "write_file":
        content = (args.get("file_content") or "").strip()
        note = f"write_file {file_path}".strip()
    elif action == "remove_file":
        note = f"remove_file {file_path}".strip()
    elif action == "patch":
        old = _truncate(args.get("old_string"))
        new = _truncate(args.get("new_string"))
        note = f"patch {old!r} -> {new!r}" if old or new else "patch"
        # The resulting SKILL.md may be supplied (the ingest script reads it
        # from the profile after the patch) so the version is projectable;
        # callers without it still record note-only.
        content = (args.get("content") or "").strip()

    # Double-observation guard: a create whose content is already the active
    # version is a no-op (the fork and foreground can both observe a write).
    if action == "create":
        head = store.latest_active(name)
        if head is not None and head.action == "create" and head.content == content:
            return 0

    store.add(
        name,
        action,
        source,
        content=content,
        category=category,
        file_path=file_path,
        note=note,
    )
    return 1
