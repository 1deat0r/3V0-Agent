"""Reconcile the native skill store with the profile's SKILL.md files.

The skill axis of the store-first evolution loop, mirroring ``core/sync.py`` for
memory: the store is the canonical record of 3V0's own skill evolution, the
profile's SKILL.md files are the operational view. ``sync_skills`` converges the
two without ever destroying store history:

- A profile skill the store has never seen that qualifies as 3V0's own
  (``created_by == "agent"`` in ``.usage.json``) is imported as a ``create``
  version (source="profile-import").
- A *tracked* skill whose profile SKILL.md differs from the store's active head
  is imported as a new ``edit`` version (the profile is the live truth; this
  heals writes the bridge missed). Content-less patch heads are left
  unresolved.
- A store-decommissioned skill (retracted/absorbed) still present in the profile
  is dropped from the profile (the store's decommission decision is canonical —
  the only removal, and it is gated on an explicit terminal).
- A store-active skill with full content that is missing from the profile is
  exported (its SKILL.md is rewritten).

In addition, the **curator's operational state** (active/stale/archived from
``.usage.json``) is folded into the store as an append-only transition log
(``store.set_state``). State is orthogonal to content lineage: an *archived*
skill is not live in the profile (its directory lives under ``.archive/``), so
the reconciler must not treat it as "missing" and re-export it.

The store never overwrites a live profile skill whose content differs: where the
profile disagrees with the store, the profile wins (it is imported); the store
only *removes* what it has explicitly decommissioned and *adds* what the profile
lacks. This is the same asymmetric, loss-free resolution as memory's sync.

Decision-pure / collection-at-edges: ``diff_skills`` is the pure per-name
classifier (mirroring memory's ``diff_kind``); ``sync_skills`` only collects the
inputs and *applies* the classified actions (mutation + projection).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .skill_io import remove_skill, skill_index, write_skill_md
from .skills import STATE_ARCHIVED, SkillStore

# The reconcile action vocabulary (the classification ``diff_skills`` returns).
IMPORT = "import"        # unseen agent skill -> create version
EDIT = "edit"            # profile diverged from head -> new edit version
DROP = "drop"            # store-decommissioned but still in profile -> remove
EXPORT = "export"        # store has it, profile lost it -> rewrite SKILL.md
UNRESOLVED = "unresolved"  # content-less head, cannot compare/project
NOOP = "noop"            # in agreement (or not tracked)


@dataclass
class SkillSyncReport:
    imported: list[str] = field(default_factory=list)    # new create versions
    edited: list[str] = field(default_factory=list)      # new edit versions (bridge-missed)
    dropped: list[str] = field(default_factory=list)     # profile skills removed (decommissioned)
    exported: list[str] = field(default_factory=list)    # SKILL.md rewritten from store
    unresolved: list[str] = field(default_factory=list)  # content-less heads (not projectable)
    state_changes: list[str] = field(default_factory=list)  # "name: old->new" curator transitions

    @property
    def clean(self) -> bool:
        return not (
            self.imported or self.edited or self.dropped or self.exported
            or self.unresolved or self.state_changes
        )


def diff_skills(*, head_content, has_terminals, profile_content, in_agent_created,
                curator_state, old_state):
    """Pure: classify one skill name's reconcile action + state transition.

    Returns ``(action, state_changed)``. ``head_content`` is ``None`` when the
    skill has no active version, else the head's ``content`` (possibly ``""``);
    ``profile_content`` is ``None`` when the profile has no SKILL.md for the
    name. The classification is the decision layer; the caller applies the
    resulting mutation + projection (see ``sync_skills``).
    """
    state_changed = old_state != curator_state
    if head_content is None:
        if has_terminals:
            action = DROP if profile_content is not None else NOOP
        elif profile_content is not None and in_agent_created:
            action = IMPORT
        else:
            action = NOOP
    elif profile_content is None:
        if curator_state == STATE_ARCHIVED:
            action = NOOP  # archived, not lost — do not re-materialize
        elif head_content:
            action = EXPORT
        else:
            action = UNRESOLVED
    elif not head_content:
        action = UNRESOLVED
    elif head_content.strip() != profile_content.strip():
        action = EDIT
    else:
        action = NOOP
    return action, state_changed


def sync_skills(
    store: SkillStore,
    skills_dir: Path,
    agent_created: set[str],
    write: bool,
    curator_states: dict[str, str] | None = None,
) -> SkillSyncReport:
    """Diff store vs profile skills; with write=True, converge them.

    ``agent_created`` is the set of skill names whose ``.usage.json`` entry has
    ``created_by == "agent"`` — the skills 3V0 is *defined* to track. Store-known
    names are reconciled regardless of that set (they are already 3V0's own).
    ``curator_states`` maps skill name -> ``.usage.json`` state (active/stale/
    archived); missing entries default to ``active``.
    """
    report = SkillSyncReport()
    curator_states = curator_states or {}
    live_skills = skill_index(skills_dir)  # excludes .archive/

    store_names = {s.name for s in store.skills}
    domain = store_names | agent_created

    for name in sorted(domain):
        curator_state = curator_states.get(name, "active")
        old_state = store.state(name)
        head = store.latest_active(name)
        profile = live_skills.get(name)

        action, state_changed = diff_skills(
            head_content=head.content if head is not None else None,
            has_terminals=any(s.terminal for s in store.versions(name)),
            profile_content=profile.content if profile is not None else None,
            in_agent_created=name in agent_created,
            curator_state=curator_state,
            old_state=old_state,
        )

        # 1. Fold the curator's operational state (append-only transitions).
        if state_changed:
            if write:
                store.set_state(name, curator_state, "curator")
            report.state_changes.append(f"{name}: {old_state}->{curator_state}")

        # 2. Apply the content-reconciliation action.
        if action == DROP:
            if write:
                remove_skill(skills_dir, name)
            report.dropped.append(name)
        elif action == IMPORT:
            assert profile is not None  # diff_skills returns IMPORT only with a profile
            if write:
                store.add(
                    name, "create", "profile-import",
                    content=profile.content, category=profile.category,
                    note="reconciled from profile",
                )
            report.imported.append(name)
        elif action == EXPORT:
            assert head is not None  # EXPORT only when the head carries content
            if write:
                write_skill_md(skills_dir, name, head.content, head.category)
            report.exported.append(name)
        elif action == EDIT:
            assert profile is not None  # EDIT only when the profile diverged
            if write:
                store.add(
                    name, "edit", "profile-import",
                    content=profile.content, category=profile.category,
                    note="reconciled from profile (content differed from store head)",
                )
            report.edited.append(name)
        elif action == UNRESOLVED:
            report.unresolved.append(name)
        # NOOP: in agreement (or not tracked) — nothing to do.

    return report
