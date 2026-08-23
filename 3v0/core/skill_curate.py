"""Skill curation — act on the outcome axis.

The review driver records per-skill outcome history (success/failure/unknown)
in the store's usage ``meta``. This module turns that signal into a
*curation decision*: which skills are failing enough to warrant rewrite /
decommission. It is pure and deterministic (no LLM) — the grade comes from
the review model, the judgment of "is this failing" comes from this module,
and the *fix* (authored content) is gated by ``safe_evolve`` before it ever
becomes a store write.

Decisions:

- ``failing_skills(meta_records, ...)`` — the skills whose outcome history
  crosses a failure threshold. Returns a list of dicts ``{name, failures,
  total, outcomes}`` (the outcomes the caller can feed a curator).
  A skill is "failing" when, among its *resolved* outcomes (failures +
  successes) within the bounded history, failures are >= ``min_failures``
  and failure-rate >= ``threshold``. Skills with only ``unknown`` outcomes
  are never failing (untested, not failed).

- ``curation_decision(meta_records, ...)`` — for a failing skill, decide
  ``rewrite`` vs ``retire`` from the same history. A skill that has NEVER
  succeeded (no ``success`` in the window) is ``retire`` (beyond repair);
  one that has some successes but a dominant failure trend is ``rewrite``.
  Advisory — the review model authors the actual content and can override.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_MIN_FAILURES = 2
DEFAULT_THRESHOLD = 0.5
# How far back into the history we look (the store bounds it at 12).
_MAX_HISTORY = 12


@dataclass
class FailingSkill:
    name: str
    failures: int
    successes: int
    resolved: int
    rate: float  # failures / resolved
    outcomes: List[str]  # most-recent-first, capped

    @property
    def ever_succeeded(self) -> bool:
        return self.successes > 0

    def decision(self) -> str:
        """rewrite (has been useful, now failing) vs retire (never worked)."""
        return "rewrite" if self.ever_succeeded else "retire"


def _meta_outcomes(rec: Any) -> List[str]:
    """The bounded outcome list from one skill's meta record."""
    if not isinstance(rec, dict):
        return []
    history = rec.get("outcome_history")
    if not isinstance(history, list):
        return []
    out: List[str] = []
    for entry in history[: _MAX_HISTORY]:
        if isinstance(entry, dict) and isinstance(entry.get("outcome"), str):
            out.append(entry["outcome"])
    return out


def failing_skills(
    meta_records: Dict[str, Any],
    *,
    min_failures: int = DEFAULT_MIN_FAILURES,
    threshold: float = DEFAULT_THRESHOLD,
) -> List[FailingSkill]:
    """Skills whose outcome history crosses a failure threshold.

    ``meta_records`` maps skill name -> store meta (with ``outcome_history``).
    Resolution counts only success/failure (unknowns are untested, not
    failed). Sorted by failure rate descending (worst first).
    """
    result: List[FailingSkill] = []
    for name, rec in meta_records.items():
        outcomes = _meta_outcomes(rec)
        if not outcomes:
            continue
        failures = outcomes.count("failure")
        successes = outcomes.count("success")
        resolved = failures + successes
        # min_failures is a COUNT of failures, not of resolved outcomes: a
        # single failure amid many successes is a fluke, not a trend.
        if failures < min_failures:
            continue
        rate = failures / resolved
        # Strict: a 50/50 split is not a failure trend (rate > threshold).
        if rate > threshold:
            result.append(
                FailingSkill(
                    name=name,
                    failures=failures,
                    successes=successes,
                    resolved=resolved,
                    rate=rate,
                    outcomes=outcomes,
                )
            )
    result.sort(key=lambda f: f.rate, reverse=True)
    return result


def curation_decision(
    meta_records: Dict[str, Any],
    *,
    min_failures: int = DEFAULT_MIN_FAILURES,
    threshold: float = DEFAULT_THRESHOLD,
) -> Dict[str, str]:
    """Map failing skills to their curation decision (rewrite|retire)."""
    return {f.name: f.decision() for f in failing_skills(
        meta_records, min_failures=min_failures, threshold=threshold
    )}