"""Retrieval-chosen injection — the read seam of the memory loop.

The store (``core.memdb``) keeps facts; this module decides which of them
become the **working set** — the retrieval-chosen subset rendered into the
derived profile view. One external seam:

    inject(conn, *, domains=("3v0",), query_terms=None, budget_chars=2000,
           touch=True, now=None) -> Injection

Everything behind it (validity filtering, scoring, ranking, domain priority,
budget fill, feedback, rendering) is the module's implementation, hidden from
callers. Design contract (ADR-0004):

- **Selection is deterministic** given (store state, query, budget, now): the
  score is keyword match + recency + feedback frequency; the budget is the
  profile view's size cap, so ``text`` never exceeds ``budget_chars``.
- **Feedback is the module's own write.** With ``touch=True`` the chosen
  facts' ``access_count``/``last_accessed`` are updated, so future ranking
  reinforces what is actually pulled into context. ``touch=False`` is a pure
  preview — no writes at all.
- **Forgetting is the store's mechanism, not this module's.** A fact whose
  ``valid_to`` has passed is simply not in ``valid_facts``, so it can never be
  injected. When a forgetting policy lands, injection follows automatically.
- **The seam is the test surface.** Tests drive ``inject()`` through a temp
  SQLite store and assert the working set and its text — never the internals.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass

from .memdb import valid_facts

# The profile's injected-view cap (Stone 21): MEMORY.md is a derived view and
# its runtime size is bounded, so the working set must fit a budget.
DEFAULT_BUDGET_CHARS = 2000


@dataclass
class Injection:
    """The result of one retrieval: the working set and its rendered text."""

    facts: list[dict]        # chosen facts, ranked (domain priority, then score)
    ids: list[int]           # their store ids (empty when nothing was chosen)
    text: str                # rendered view; len(text) <= budget_chars
    truncated: bool          # True when valid facts were left out of the view
    budget_chars: int        # the cap that was applied
    budget_used: int         # len(text)


def _score(fact, query_terms, now):
    """Pure relevance score: keyword match + recency + feedback frequency."""
    score = 0.0
    if query_terms:
        hay = " ".join(
            str(fact.get(k) or "") for k in ("subject", "predicate", "object", "content")
        ).lower()
        for term in query_terms:
            if term.lower() in hay:
                score += 1.0
    t = fact.get("last_accessed") or fact.get("created_at") or now
    age_days = max(0.0, (now - t) / 86400.0)
    score += 1.0 / (1.0 + age_days)          # recency: 1.0 now, decaying
    score += math.log1p(fact.get("access_count") or 0)  # feedback frequency
    return score


def rank(facts, query_terms=None, now=None):
    """Pure: sort facts by relevance score (descending)."""
    now = now if now is not None else time.time()
    return sorted(facts, key=lambda f: _score(f, query_terms, now), reverse=True)


def render(facts):
    """Compact one-line-per-fact text (the working set's wire format)."""
    lines = []
    for f in facts:
        line = f"{f['subject']} {f['predicate']} {f['object']}"
        if f.get("content"):
            line += f"  # {f['content']}"
        lines.append(line)
    return "\n".join(lines)


def _ranked_valid(conn, domains, query_terms, now):
    """Valid facts in domain-priority order, each domain ranked by score.

    ``domains`` is a priority-ordered sequence: facts from the first domain
    rank ahead of the second, and so on. ``None`` means all domains, ranked
    by score alone.
    """
    if domains is None:
        return rank(valid_facts(conn, now=now), query_terms=query_terms, now=now)
    out = []
    for domain in dict.fromkeys(domains):
        out.extend(
            rank(valid_facts(conn, domain=domain, now=now),
                 query_terms=query_terms, now=now)
        )
    return out


def _touch(conn, ids, now):
    """Feedback: record that the chosen facts were pulled into context."""
    if not ids:
        return
    conn.executemany(
        "UPDATE facts SET access_count = access_count + 1, last_accessed = ? WHERE id = ?",
        [(now, i) for i in ids],
    )
    conn.commit()


def inject(conn, *, domains=("3v0",), query_terms=None,
           budget_chars=DEFAULT_BUDGET_CHARS, touch=True, now=None):
    """The retrieval seam: choose and render the working set under a budget.

    Facts are taken in ranked order and rendered one line at a time; a fact
    whose line would exceed the budget is skipped (whole-fact granularity —
    later, smaller facts still get their chance), and ``truncated`` reports
    whether any valid fact was left out. With ``touch=True`` the chosen facts'
    feedback counters are updated and committed; ``touch=False`` writes
    nothing (pure preview).
    """
    now = now if now is not None else time.time()
    ranked = _ranked_valid(conn, domains, query_terms, now)

    chosen: list[dict] = []
    lines: list[str] = []
    used = 0
    for fact in ranked:
        line = render([fact])
        candidate = used + (1 if lines else 0) + len(line)
        if candidate > budget_chars:
            continue
        chosen.append(fact)
        lines.append(line)
        used = candidate

    ids = [f["id"] for f in chosen]
    if touch:
        _touch(conn, ids, now)
    return Injection(
        facts=chosen,
        ids=ids,
        text="\n".join(lines),
        truncated=len(chosen) < len(ranked),
        budget_chars=budget_chars,
        budget_used=used,
    )
