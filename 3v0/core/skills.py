"""3V0 core skill store — a provenance-aware, versioned skill-lineage store.

The memory store (``core/memory.py``) made 3V0's *facts* canonical and
recoverable. This is the same lesson applied to the next axis of the evolution
loop: *skills*. Every time a skill is created, rewritten, patched, or
decommissioned, that event is recorded as a version with provenance, and
replacement links the old version to its successor. Nothing is ever destroyed —
the lineage (which skill superseded which, which skill absorbed which) is the
point.

Design mirrors ``MemoryStore``:

- A ``SkillVersion`` carries the skill name, the ``skill_manage`` action that
  produced it, the content that action carried (full SKILL.md for create/edit,
  file content for write_file), provenance, and supersession links.
- A new version of a skill SUPERSEDES the previous active version of the same
  name: the old version is marked inactive and linked forward, recoverable via
  ``history()``.
- Decommissioning has two shapes, both recoverable terminals:
    - ``retract`` — a delete with no successor (pure prune). ``superseded_by``
      is set to the ``RETRACTED`` sentinel.
    - ``absorb`` — a delete with ``absorbed_into=<umbrella>`` (consolidation).
      ``superseded_by`` is set to ``ABSORBED`` and ``absorbed_into`` records
      which skill swallowed it.
- Plain JSON on disk (stdlib only), with the same cross-process ``flock``
  ``mutate()`` contract as ``MemoryStore`` so the background review fork's
  ingest subprocess and a foreground writer serialize.

Like the memory store, this is the *canonical record of 3V0's own evolution*,
not (yet) the mechanism that drives the profile's SKILL.md files — the profile
remains the operational system and the store the auditable mirror, exactly the
posture stone 1 took for memory.
"""

from __future__ import annotations

import json
import time
import uuid
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .lineage import RETRACTED, iso_time, retraction_note, validate_enum
from .memory import locked

ACTIONS = ("create", "patch", "edit", "write_file", "remove_file", "delete")  # canonical skill_manage actions
_VALID_ACTIONS = set(ACTIONS)  # set for O(1) membership + sorted() in the error message

# Reserved keys under SkillVersion.meta — the usage-feedback vocabulary. Never
# repurpose a reserved key for a custom field; the resolver (ranking/demotion)
# depends on these exact names, so they act as a frozen contract.
META_USES = "uses"              # int  — total retrieval/load count
META_LAST_USED = "last_used"    # str  — ISO-8601 timestamp of the last use
META_RANK_MODE = "rank_mode"    # str  — display posture: "by_usage" | default
_STANDARD_META_KEYS = {META_USES, META_LAST_USED, META_RANK_MODE}

# Operational (curator) states, tracked alongside content lineage. Orthogonal to
# ``SkillVersion.active``: an archived skill still has an active content version
# (it was never retracted/absorbed), but is not live in the profile.
STATE_ACTIVE = "active"
STATE_STALE = "stale"
STATE_ARCHIVED = "archived"
_VALID_STATES = {STATE_ACTIVE, STATE_STALE, STATE_ARCHIVED}

# Terminal (decommissioned) sentinels, distinct from a real version id, so
# ``active()`` excludes them and ``history()`` can still surface them as the
# end of a lineage. RETRACTED is shared with the memory axis (core.lineage);
# ABSORBED is skill-specific (no memory analogue).
ABSORBED = "absorbed"     # deleted with absorbed_into=<umbrella> (consolidation)


@dataclass
class SkillVersion:
    id: str
    name: str
    action: str                 # create | patch | edit | write_file | remove_file | delete
    # OVERLOAD (mitigated): `content` is the full SKILL.md for create/edit but
    # the supporting *file* content for write_file. Sync special-cases this via
    # SkillStore.latest_content_head, which looks past write_file/remove_file to
    # the latest create/edit/patch — a supporting-file head can no longer
    # masquerade as a body edit.
    content: str                # full SKILL.md (create/edit), file content (write_file), else ""
    category: str = ""          # skills/<category> subdirectory, when known
    file_path: str = ""         # for write_file / remove_file
    source: str = ""            # e.g. "background_review", "assistant_tool", "profile-import"
    created_at: str = ""
    supersedes: list[str] = field(default_factory=list)
    superseded_by: str = ""     # "" active | version id | RETRACTED | ABSORBED
    absorbed_into: str = ""     # umbrella name when superseded_by == ABSORBED
    note: str = ""
    # Usage/meta feedback record (evolving, attached to the active head —
    # see touch_skill / set_skill_meta). Freer-form than `states` so the
    # culture/rank layer stays unconstrained; standard keys are pinned above.
    meta: dict[str, object] = field(default_factory=dict)

    @property
    def active(self) -> bool:
        return not self.superseded_by

    @property
    def terminal(self) -> bool:
        return self.superseded_by in (RETRACTED, ABSORBED)


class SkillStore:
    """Append-only skill lineage with supersession (no silent overwrite)."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.skills: list[SkillVersion] = []
        self.states: dict[str, dict] = {}
        if self.path.exists():
            self._load()

    # -- persistence -------------------------------------------------------
    def _load(self) -> None:
        if not self.path.exists():
            self.skills = []
            self.states = {}
            return
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.skills = [SkillVersion(**s) for s in raw.get("skills", [])]
        self.states = raw.get("states", {})

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": 1,
            "skills": [asdict(s) for s in self.skills],
            "states": self.states,
        }
        self.path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    # -- queries -----------------------------------------------------------
    def versions(self, name: str) -> list[SkillVersion]:
        """All recorded versions of a skill, in append (creation) order."""
        return [s for s in self.skills if s.name == name]

    def latest_active(self, name: str) -> SkillVersion | None:
        """The currently-active version of ``name``, if one exists.

        The invariant "each new non-terminal version supersedes the previous
        active version of the same name" means at most one active version per
        name: the head of the chain. A retracted/absorbed skill has none.
        """
        for s in reversed(self.versions(name)):
            if s.active:
                return s
        return None

    def latest_content_head(self, name: str) -> SkillVersion | None:
        """The skill-body head for reconciliation (see ``sync_skills``).

        A ``write_file``/``remove_file`` version carries a *supporting file's*
        content, not SKILL.md — and it supersedes the preceding ``create``/``edit``
        — so the body head is the latest ``create``/``edit``/``patch``, looking
        past supporting-file ops. Returns None when the skill has no active
        version (decommissioned or never seen).
        """
        if self.latest_active(name) is None:
            return None
        for s in reversed(self.versions(name)):
            if s.action in ("create", "edit", "patch"):
                return s
        return None  # unreachable: an active head implies an earlier create

    def active(self) -> list[SkillVersion]:
        """One active version per currently-live skill (chain heads)."""
        seen: set[str] = set()
        out: list[SkillVersion] = []
        for s in reversed(self.skills):
            if s.name in seen:
                continue
            seen.add(s.name)
            if s.active:
                out.append(s)
        return list(reversed(out))

    def active_names(self) -> set[str]:
        return {s.name for s in self.active()}

    def absorbed_by(self, name: str) -> list[str]:
        """Skills whose latest decommission was an absorb into ``name``."""
        out: list[str] = []
        for s in self.skills:
            if s.superseded_by == ABSORBED and s.absorbed_into == name:
                out.append(s.name)
        return sorted(set(out))

    def history(self, name: str) -> list[SkillVersion]:
        """The full recorded lineage of a skill (audit trail, oldest first).

        Append order IS the lineage order: supersession links walk forward
        through versions of the same name, but a skill retracted and later
        re-created starts a second chain — both chains are still returned here
        so nothing is lost.
        """
        return self.versions(name)

    # -- mutations ---------------------------------------------------------
    def add(
        self,
        name: str,
        action: str,
        source: str,
        content: str = "",
        category: str = "",
        file_path: str = "",
        note: str = "",
        supersedes: list[str] | None = None,
        persist: bool = True,
    ) -> SkillVersion:
        """Append a version, superseding the current active version of ``name``.

        ``supersedes`` is filled automatically from the current active version
        unless the caller supplies it explicitly (the bridge may want to link a
        non-head predecessor, but that is rare).
        """
        validate_enum(action, _VALID_ACTIONS, "action")
        if action == "delete":
            raise ValueError("delete is terminal; use retract()/absorb() instead")

        version = SkillVersion(
            id=uuid.uuid4().hex[:12],
            name=name,
            action=action,
            content=content,
            category=category,
            file_path=file_path,
            source=source,
            created_at=iso_time(time.time()),
            supersedes=list(supersedes) if supersedes else [],
            note=note,
        )

        if not version.supersedes:
            head = self.latest_active(name)
            if head is not None:
                version.supersedes = [head.id]

        self.skills.append(version)
        for target_id in version.supersedes:
            for old in self.skills:
                if old.id == target_id and old.active:
                    old.superseded_by = version.id
        if persist:
            self._save()
        return version

    def _decommission(
        self,
        name: str,
        sentinel: str,
        source: str = "",
        absorbed_into: str = "",
        persist: bool = True,
    ) -> SkillVersion | None:
        """Mark the active version of ``name`` as a terminal (retract/absorb)."""
        head = self.latest_active(name)
        if head is None:
            return None
        head.superseded_by = sentinel
        if absorbed_into:
            head.absorbed_into = absorbed_into
        if source:
            what = "absorbed into " + absorbed_into if absorbed_into else "retracted"
            head.note = retraction_note(head.note, source, what=what)
        if persist:
            self._save()
        return head

    def retract(self, name: str, source: str = "", persist: bool = True) -> SkillVersion | None:
        """Decommission ``name`` with no successor (pure prune). Recoverable."""
        return self._decommission(name, RETRACTED, source=source, persist=persist)

    def absorb(
        self,
        name: str,
        absorbed_into: str,
        source: str = "",
        persist: bool = True,
    ) -> SkillVersion | None:
        """Decommission ``name`` because its content was folded into ``absorbed_into``."""
        return self._decommission(
            name, ABSORBED, source=source, absorbed_into=absorbed_into, persist=persist
        )

    # -- operational (curator) state ---------------------------------------
    def state(self, name: str) -> str:
        """The current operational state of ``name`` (active/stale/archived).

        This is the *curator* state axis, orthogonal to content-lineage
        ``active``: an archived skill still has an active content version (it
        was never retracted/absorbed) but is not live in the profile. Defaults
        to ``active`` for a skill with no recorded state.
        """
        rec = self.states.get(name)
        return rec.get("current", STATE_ACTIVE) if rec else STATE_ACTIVE

    def state_history(self, name: str) -> list[dict]:
        """The append-only transition log for ``name``'s operational state."""
        rec = self.states.get(name)
        return list(rec.get("history", [])) if rec else []

    def set_state(
        self,
        name: str,
        new_state: str,
        source: str = "",
        persist: bool = True,
    ) -> dict | None:
        """Record a transition of ``name`` to ``new_state`` (append-only).

        Idempotent: recording the state a skill already has is a no-op. Returns
        the recorded event (``{"from", "state", "at", "source"}``) or None when
        no change occurred.
        """
        validate_enum(new_state, _VALID_STATES, "state")
        old = self.state(name)
        if new_state == old:
            return None
        rec = self.states.get(name)
        history = list(rec.get("history", [])) if rec else []
        event = {
            "from": old,
            "state": new_state,
            "at": iso_time(time.time()),
            "source": source,
        }
        history.append(event)
        self.states[name] = {"current": new_state, "history": history}
        if persist:
            self._save()
        return event

    # -- usage feedback (retrieval-culture metadata) -----------------------
    #
    # Usage is recorded on the *latest active version* (the live head of the
    # chain). It is annotated read feedback — an evolving counter that rides the
    # current version without creating new lineage versions. This is the
    # memory-axis analogue of the retrieval store's access_count/last_accessed:
    # the skill axis's own "used" signal, so ranking can reward what earns its
    # keep and demote what never fires.
    def skill_meta(self, name: str) -> dict[str, object]:
        """The usage/meta record for ``name``'s active head ({} when none).

        Defaults to empty for a missing skill or one with no recorded meta. The
        standard keys are the pinned ``META_*`` constants; callers may store
        extra fields via ``set_skill_meta``, but must not reuse a reserved key
        for a different type (the ranker treats it as e.g. an int counter).
        """
        head = self.latest_active(name)
        if head is None:
            return {}
        return dict(head.meta)

    def set_skill_meta(self, name: str, persist: bool = True, **fields: object) -> dict[str, object]:
        """Merge ``fields`` into the active head's meta (no new version).

        Returns the head's full meta after the merge, or {} when the skill has
        no active head. An empty-field call is a read-only no-op (same cost as
        ``skill_meta``). This is the display/retrieval-culture actuator used by
        ``skill_promote`` / ``skill_demote``; it never supersedes or
        decommissions.
        """
        head = self.latest_active(name)
        if head is None:
            return {}
        head.meta.update(fields)
        if persist:
            self._save()
        return dict(head.meta)

    def touch_skill(self, name: str, source: str = "", persist: bool = True) -> dict[str, object] | None:
        """Record a use of ``name`` (bump ``uses``, refresh ``last_used``).

        The canonical read feedback call — the resolver invokes it when the
        model loads a skill via ``skill_view`` (or the /skill-name fast path),
        so "actually needed and fetched" is the signal, never a mere listing.
        Returns the head's meta after the touch, or None when the skill has no
        active head (missing or decommissioned). ``source`` is recorded as a
        retire time for diagnosis; it is not a lineage version.
        """
        head = self.latest_active(name)
        if head is None:
            return None
        now = iso_time(time.time())
        meta = head.meta
        meta[META_USES] = int(meta.get(META_USES, 0)) + 1
        meta[META_LAST_USED] = now
        if source:
            meta["last_used_source"] = source
        if persist:
            self._save()
        return dict(meta)

    # -- concurrency -------------------------------------------------------
    def reload(self) -> None:
        self._load()

    @contextmanager
    def mutate(self):
        """Cross-process lock + reload, mirroring ``MemoryStore.mutate()``."""
        with locked(self.path):
            self.reload()
            yield self
