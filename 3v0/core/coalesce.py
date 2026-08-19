"""Coalesce — the consistent consolidation process (watermark-driven).

Runs memory consolidation on a cadence, never on demand: a persisted high-water
mark means the process fires only when ``now - last >= interval``, so it is
idempotent across repeated 3V0 wake ticks yet still happens regularly.

Work done on each fire:
  1. conflict reconciliation — collapse conflicting (subject,predicate) facts to
     one current truth (consolidate.py), reversible via valid_to.
  2. near-duplicate merge — within a (subject,predicate) group, supersede sibling
     content that is token-overlap >= threshold (conservative), so the store
     stops growing duplicate truth.

All supersessions are auditable + reversible (valid_to close, never delete).
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path

from . import consolidate, memdb

DEFAULT_INTERVAL_S = 24 * 3600
DEFAULT_WATERMARK = Path(__file__).resolve().parent.parent / "data" / "coalesce.watermark.json"


def _token_set(text: str) -> tuple[str, ...]:
    import re
    return tuple(sorted(re.findall(r"[a-z0-9]+", text.lower())))


def _token_overlap(a: str, b: str) -> float:
    ta, tb = _token_set(a), _token_set(b)
    if not ta or not tb:
        return 0.0
    return len(set(ta) & set(tb)) / max(len(set(ta)), len(set(tb)))


@dataclass
class CoalesceReport:
    fired: bool = False
    reason: str = ""
    reconciled: int = 0
    merged: int = 0
    superseded_ids: list = field(default_factory=list)
    next_due: float = 0.0


def load_watermark(path=DEFAULT_WATERMARK) -> float:
    try:
        return float(json.loads(Path(path).read_text()).get("last_run", 0.0))
    except Exception:
        return 0.0


def save_watermark(now, path=DEFAULT_WATERMARK):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps({"last_run": now}), encoding="utf-8")


def _merge_near_duplicates(conn, threshold: float = 0.95) -> tuple[int, list]:
    """Supersede sibling facts within a (subject,predicate) group whose content
    token-overlap is at/above ``threshold`` — keep the newest id, close the rest.
    Reversible: restore a closed fact's valid_to to bring it back.
    """
    groups: dict[tuple, list] = {}
    for f in memdb.valid_facts(conn):
        key = (str(f.get("subject") or "").lower(),
               str(f.get("predicate") or "").lower())
        groups.setdefault(key, []).append(f)
    merged = 0
    closed: list = []
    for facts in groups.values():
        facts.sort(key=lambda r: r.get("id") or 0, reverse=True)
        keep = facts[0]
        k = str(keep.get("content") or "")
        for other in facts[1:]:
            o = str(other.get("content") or "")
            if _token_set(o) and _token_overlap(o, k) >= threshold:
                now = time.time()
                conn.execute(
                    "UPDATE facts SET valid_to = ? WHERE id = ? AND valid_to IS NULL",
                    (now, other.get("id")))
                closed.append(other.get("id"))
                merged += 1
    if closed:
        conn.commit()
    return merged, closed


def run(conn, *, now=None, interval_s: float = DEFAULT_INTERVAL_S,
        force: bool = False, threshold: float = 0.95,
        watermark=DEFAULT_WATERMARK) -> CoalesceReport:
    """Consolidation on cadence. Superseded ids are reversible (valid_to clear)."""
    now = now if now is not None else time.time()
    last = load_watermark(watermark)
    if not force and (now - last) < interval_s:
        return CoalesceReport(fired=False,
                              reason=f"not due (last {last:.0f}, interval {interval_s:.0f}s)",
                              next_due=last + interval_s)
    rep = CoalesceReport(fired=True)
    for ks in consolidate.pending_consolidations(conn):
        r = consolidate.reconcile(conn, ks.subject, ks.predicate, keep="newest", now=now)
        if r.reconciled:
            rep.reconciled += 1
            rep.superseded_ids += r.closed
    merged, closed = _merge_near_duplicates(conn, threshold=threshold)
    rep.merged = merged
    rep.superseded_ids += closed
    save_watermark(now, watermark)
    rep.next_due = now + interval_s
    return rep