"""Forgetting — archive facts that never earned their keep (Stone 24).

The counterpart to retrieval's reinforcement (ADR-0005): a fact that stays
valid but is never pulled into context — never explicitly retrieved
(``access_count == 0``) and never projected to the profile (``last_projected``
is NULL) — is archived after a grace period, so the store tracks what the
agent actually uses, not everything it ever wrote down.

Decision-pure / collection-at-edges: ``is_stale`` is the pure rule; ``stale_ids``
collects valid facts and applies it; ``forget`` is the write (archive, never
delete — ``valid_to`` is set, recoverable via ``fact_history``).
"""

from __future__ import annotations

import time

from .memdb import valid_facts

FORGETTABLE_KINDS = ("memory", "user")
FORGET_TAG = "forgotten (never used)"


def is_stale(fact: dict, threshold_days: float, now: float) -> bool:
    """Pure: is this *valid* fact eligible for forgetting?

    Forgettable only if a forgettable kind, never retrieved, never projected,
    and older than the threshold. ``identity``/``directive`` are permanent —
    they are the agent's core identity and Prime Directive.
    """
    if fact["kind"] not in FORGETTABLE_KINDS:
        return False
    if fact.get("access_count", 0) != 0:
        return False
    if fact.get("last_projected") is not None:
        return False
    created = fact.get("created_at")
    if created is None or (now - created) <= threshold_days * 86400.0:
        return False
    return True


def stale_ids(conn, threshold_days, now=None):
    """Ids of valid facts eligible for forgetting (collection + pure rule)."""
    now = now if now is not None else time.time()
    return [f["id"] for f in valid_facts(conn, now=now)
            if is_stale(f, threshold_days, now)]


def forget(conn, threshold_days, now=None):
    """Archive the stale facts (valid_to = now, note-tagged); return count."""
    now = now if now is not None else time.time()
    ids = stale_ids(conn, threshold_days, now)
    if not ids:
        return 0
    for fid in ids:
        row = conn.execute("SELECT note FROM facts WHERE id = ?", (fid,)).fetchone()
        note = (row["note"] or "").strip()
        new_note = f"{note} {FORGET_TAG}".strip() if note else FORGET_TAG
        conn.execute("UPDATE facts SET valid_to = ?, note = ? WHERE id = ?",
                     (now, new_note, fid))
    conn.commit()
    return len(ids)
