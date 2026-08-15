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
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .skill_io import remove_skill, skill_index, write_skill_md
from .skills import STATE_ARCHIVED, SkillStore


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

        # 1. Fold the curator's operational state (append-only transitions).
        old_state = store.state(name)
        if old_state != curator_state:
            if write:
                store.set_state(name, curator_state, "curator")
            report.state_changes.append(f"{name}: {old_state}->{curator_state}")

        # 2. Content reconciliation (archive-aware).
        head = store.latest_active(name)
        profile = live_skills.get(name)
        terminals = [s for s in store.versions(name) if s.terminal]

        if head is None:
            if terminals:
                # The store decommissioned this skill; any live profile presence
                # is stale (the decommission decision is canonical).
                if profile is not None:
                    if write:
                        remove_skill(skills_dir, name)
                    report.dropped.append(name)
                # else: already absent from the profile — nothing to do.
            elif profile is not None and name in agent_created:
                # Unseen 3V0-authored skill — import the live content.
                if write:
                    store.add(
                        name, "create", "profile-import",
                        content=profile.content, category=profile.category,
                        note="reconciled from profile",
                    )
                report.imported.append(name)
            # else: not a tracked skill, or absent everywhere — nothing to do.
        else:
            if profile is None:
                if curator_state == STATE_ARCHIVED:
                    # Archived, not lost: the curator moved it to .archive/. The
                    # store's content is still the record; do not re-materialize.
                    pass
                elif head.content:
                    # Store has it, profile lost it. Re-materialize when we hold
                    # full content; otherwise nothing faithful to write.
                    if write:
                        write_skill_md(skills_dir, name, head.content, head.category)
                    report.exported.append(name)
                else:
                    report.unresolved.append(name)
            elif not head.content:
                # Content-less head (e.g. a legacy patch) — can't compare or
                # project; leave the profile as the operational truth.
                report.unresolved.append(name)
            elif head.content.strip() != profile.content.strip():
                # Profile diverged from the store head: the profile is the live
                # truth (the bridge missed a write). Import it as a new version.
                if write:
                    store.add(
                        name, "edit", "profile-import",
                        content=profile.content, category=profile.category,
                        note="reconciled from profile (content differed from store head)",
                    )
                report.edited.append(name)
            # else: in agreement — nothing to do.

    return report
