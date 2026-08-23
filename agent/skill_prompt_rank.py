"""Pure skill-index ranking for the usage-aware skill prompt.

Reads the usage telemetry produced by ``tools/skill_usage.py`` (the sidecar
``.usage.json``) and decides which skills get full description entries vs.
a names-only tail line in ``<available_skills>`` — under a *fix token budget*.

The shape is deliberately narrow: this module is a pure function of the
visible skill entries + a usage lookup. It has no I/O, no hidden state, and
no fallback — the caller (``prompt_builder.build_skills_system_prompt``)
decides whether to apply it at all.

Rules (each is a direct, auditable decision):

1. **Ranking by usage recency.** Used skills sort most-recently-used first,
   so the highest-signal entries sit at the top of their category where the
   model reads first. Used skills that are NEVER used sink to the bottom of
   the used block.
2. **Names-only tail for "never used".** A skill with zero recorded uses still
   appears — as a single names-only line at the tail — so every skill name
   stays visible and loadable (memory-anchored recall keeps working, exactly
   the existing demotion contract). Nothing is ever hidden.
3. **The used/never-used split is per category.** An unused skill in a
   category where the user actively works stays prominent enough to be seen,
   but the full-description budget goes to the skills that earn it.
4. **Deterministic.** No randomness; ties break alphabetically.

``should_apply`` is the caller's opt-in gate — a config self-earned by the
sidecar recording a use. It consults only the usage map keys (absence of an
entry = not used), so a skill with garbage meta can never claim ``by_usage``.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

# The sidecar's recorded fields (tools/skill_usage.py).
KEY_USE_COUNT = "use_count"
KEY_LAST_USED = "last_used_at"

# Result shapes for the ranker.
RankedEntry = Dict[str, object]   # {name, description, usage} for a used skill
NamesOnlyLine = Tuple[str, str]   # (names_joined, note) rendered as a tail
CategoryEntries = List[Dict[str, object]]  # visible skill entries (dicts from snapshot)


def should_apply(usage: Dict[str, Dict[str, object]]) -> bool:
    """Whether the usage map justifies ``by_usage`` ranking.

    True only when at least one skill has a recorded use. All-or-nothing:
    a config that ignores ``by_usage`` when nothing has ever been used is the
    least surprising default, and avoids churn in the index before there is
    signal.
    """
    for rec in usage.values():
        if isinstance(rec, dict) and int(rec.get(KEY_USE_COUNT, 0) or 0) >= 1:
            return True
    return False


def _usage_for(name: str, usage: Dict[str, Dict[str, object]]) -> Optional[Dict[str, object]]:
    """The usage record for ``name``, or None when unused (missing/invalid)."""
    rec = usage.get(name)
    if not isinstance(rec, dict):
        return None
    if int(rec.get(KEY_USE_COUNT, 0) or 0) < 1:
        return None
    return rec


def rank_and_demote(
    entries: List[Dict[str, object]],
    usage: Dict[str, Dict[str, object]],
) -> Tuple[List[RankedEntry], Optional[NamesOnlyLine]]:
    """Split visible skill entries into (used-ranked, never-used-names-only).

    ``entries`` are the visible snapshot entries (dicts with ``frontmatter_name``
    / ``skill_name`` / ``description``). ``usage`` is the raw sidecar map
    (or ``{}`` when unavailable). Returns:

    - ``used`` — entries with a recorded use, sorted by usage recency
      (most-recent first; ties and missing timestamps alphabetical).
    - ``never_used`` — a single names-only line (names joined, human note) or
      None when every entry has a use.

    Deterministic and pure.
    """
    used: List[RankedEntry] = []
    never_used_names: List[str] = []

    for entry in entries:
        name = str(entry.get("frontmatter_name") or entry.get("skill_name") or "").strip()
        desc = str(entry.get("description") or "")
        rec = _usage_for(name, usage)
        if rec is not None:
            used.append({
                "name": name,
                "description": desc,
                "usage": rec,
            })
        else:
            never_used_names.append(name)

    # Rank: most-recently-used first. To keep ties trivially deterministic,
    # sort by NEGATED numeric recency (ascending => most recent first) with an
    # ascending-alphabetical tiebreak. A missing/invalid timestamp maps to
    # epoch 0, so it sorts LAST (most negative), never crashes.
    def _sort_key(item: RankedEntry) -> Tuple[float, str]:
        rec = item.get("usage") or {}
        last = str(rec.get(KEY_LAST_USED) or "")

        def _epoch(iso: str) -> float:
            try:
                from datetime import datetime, timezone
                # iso "2026-08-20T10:00:00Z" == ".0+00:00"-style; strip Z for
                # fromisoformat. A full date without time still parses, and a
                # garbage string raises -> 0.0 (sorts last, deterministic).
                return datetime.fromisoformat(
                    iso.replace("Z", "+00:00")
                ).replace(tzinfo=timezone.utc).timestamp()
            except Exception:
                return 0.0

        return (-_epoch(last), str(item.get("name", "")))

    used.sort(key=_sort_key)

    names_only: Optional[NamesOnlyLine]
    if never_used_names:
        note = "not used recently"
        names_only = (", ".join(sorted(never_used_names)), note)
    else:
        names_only = None

    return used, names_only