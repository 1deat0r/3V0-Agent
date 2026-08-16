"""Continuity meta — the invariant model (Stone 17).

The pure, unit-testable *decision* half of 3V0's continuity meta. A
continuity invariant is a named check over a flat, JSON-safe context dict of
collected facts; it decides ``drift`` (two artifacts disagree about the same
reality) and returns a ``detail`` string. No git / network / file I/O lives
here — the collection half (``scripts/continuity_check.py``) gathers the
facts; this module only *decides*. Mirrors Stone 16's ``core/drift.py`` split
(decision pure, collection shells out).

The invariants check **cross-artifact consistency, not freshness**: a file
being recent cannot catch "the memory store says X while the ledger says Y".
Only a relation between artifacts can — so every invariant here relates two
or more artifacts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List

# The canonical paths of the continuity model itself, relative to the body
# repo root. The "self-describing" invariant verifies the anchor both
# *references* these and that they are *reachable* on disk.
CANONICAL_MODEL_PATHS = (
    "3v0/core/continuity.py",
    "3v0/scripts/continuity_check.py",
)

# Markers the anchor must carry to be considered well-formed: the immutable
# law, plus a pointer to the continuity model.
ANCHOR_MARKERS = ("## Prime Directive", "## Continuity model")


@dataclass(frozen=True)
class InvariantResult:
    drift: bool
    detail: str

    def to_dict(self) -> dict:
        return {"drift": self.drift, "detail": self.detail}


@dataclass(frozen=True)
class Invariant:
    name: str
    description: str
    healable: bool            # True = the safe mechanical heal fixes it
    check: Callable[[dict], InvariantResult]


# ---------------------------------------------------------------------------
# Pure check functions. Context is a flat dict of collected facts (all
# JSON-safe); each check only reads it and decides.
# ---------------------------------------------------------------------------


def check_anchor(ctx: dict) -> InvariantResult:
    """The fixed point exists and is well-formed (never auto-healed)."""
    if not ctx.get("anchor_present"):
        return InvariantResult(True, "anchor file missing")
    text = ctx.get("anchor_text", "")
    missing = [m for m in ANCHOR_MARKERS if m not in text]
    if missing:
        return InvariantResult(True, "anchor malformed: missing " + ", ".join(missing))
    return InvariantResult(False, "anchor present and well-formed")


def check_self_describing(ctx: dict) -> InvariantResult:
    """The anchor's claim about where the model lives matches the model's own
    canonical paths, and those paths are reachable. A corrupted meta fails
    loud, never silent."""
    if not ctx.get("anchor_present"):
        return InvariantResult(True, "anchor missing - cannot verify model reachability")
    text = ctx.get("anchor_text", "")
    reachable = ctx.get("model_reachable", {})
    problems = []
    for p in CANONICAL_MODEL_PATHS:
        if p not in text:
            problems.append(f"{p} not referenced by anchor")
        elif not reachable.get(p):
            problems.append(f"{p} unreachable on disk")
    if problems:
        return InvariantResult(True, "; ".join(problems))
    return InvariantResult(False, "anchor references the continuity model; model reachable")


def _sum_counts(counts: dict, keys: tuple) -> int:
    return sum(int(counts.get(k, 0) or 0) for k in keys)


def check_memory_profile(ctx: dict) -> InvariantResult:
    """Memory store <-> profile (MEMORY.md / USER.md) consistent: the
    reconciler reports no imported / dropped / exported for either kind, and
    the store was readable."""
    errors = []
    diffs = []
    for kind in ("memory", "user"):
        counts = ctx.get(kind) or {}
        if counts.get("error"):
            errors.append(f"{kind}: {counts['error']}")
        n = _sum_counts(counts, ("imported", "dropped", "exported"))
        if n:
            diffs.append(f"{kind}:{n}")
    if errors:
        return InvariantResult(True, "store unreadable: " + "; ".join(errors))
    if diffs:
        return InvariantResult(True, "store != profile: " + ", ".join(diffs))
    return InvariantResult(False, "memory store <-> profile consistent")


def check_skills_store(ctx: dict) -> InvariantResult:
    """Skill store <-> SKILL.md consistent: the reconciler reports no content
    or state deltas, and the store was readable."""
    counts = ctx.get("skills") or {}
    if counts.get("error"):
        return InvariantResult(True, f"skill store unreadable: {counts['error']}")
    keys = ("imported", "edited", "dropped", "exported", "unresolved", "state_changes")
    parts = [f"{k}={int(counts.get(k, 0) or 0)}" for k in keys if int(counts.get(k, 0) or 0)]
    if parts:
        return InvariantResult(True, "skill store != SKILL.md: " + ", ".join(parts))
    return InvariantResult(False, "skill store <-> SKILL.md consistent")


def check_ledger(ctx: dict) -> InvariantResult:
    """The reconstruction clock's data source (the project ledger) parses."""
    if ctx.get("ledger_ok"):
        return InvariantResult(
            False, f"project ledger parseable ({ctx.get('ledger_count', 0)} projects)"
        )
    return InvariantResult(
        True, f"project ledger unreadable: {ctx.get('ledger_detail', 'unknown')}"
    )


# ---------------------------------------------------------------------------
# The invariant registry — the "consistency ledger" (ordered, git-versioned).
# ---------------------------------------------------------------------------

DEFAULT_INVARIANTS: List[Invariant] = [
    Invariant(
        "anchor", "fixed point intact (Prime Directive + model pointer)",
        healable=False, check=check_anchor,
    ),
    Invariant(
        "self-describing", "meta is self-describing and reachable from the anchor",
        healable=False, check=check_self_describing,
    ),
    Invariant(
        "memory-profile", "memory store <-> profile consistent",
        healable=True, check=check_memory_profile,
    ),
    Invariant(
        "skills-store", "skill store <-> SKILL.md consistent",
        healable=True, check=check_skills_store,
    ),
    Invariant(
        "ledger", "project ledger (reconstruction clock data) parseable",
        healable=False, check=check_ledger,
    ),
]


def evaluate(invariants: List[Invariant], ctx: dict) -> dict:
    """Evaluate every invariant over ``ctx`` -> a JSON-safe report dict.

    ``drift_count`` is the total drifting; ``healable_drift`` is the subset
    the safe mechanical heal can fix (drift in a non-healable invariant is a
    deliberate-repair flag, not an auto-heal target)."""
    results: List[dict] = []
    drift_count = 0
    healable_drift = 0
    for inv in invariants:
        r = inv.check(ctx)
        results.append(
            {
                "name": inv.name,
                "description": inv.description,
                "healable": inv.healable,
                "drift": r.drift,
                "detail": r.detail,
            }
        )
        if r.drift:
            drift_count += 1
            if inv.healable:
                healable_drift += 1
    return {
        "total": len(results),
        "drift_count": drift_count,
        "healable_drift": healable_drift,
        "invariants": results,
    }
