#!/usr/bin/env python3
"""discover.py — the mechanical engine behind 3V0's discovery feedback store.

A correction CACHE with heuristic recall over 3v0/data/discovery_feedback.json.
NOT a learning system: consult output is a HYPOTHESIS that must be revalidated
against the current active toolset / catalog / task intent before acting.

This backs the ``threev0_discover`` tool (native-store-bridge plugin) and the
skill_discovery consult step. Self-anchored — STORE resolves relative to this
file, so cwd is irrelevant; DISCOVERY_STORE env overrides.

Usage:
  discover.py consult "<query>"          # advisory recall of prior corrections
  discover.py record "<query>" "<chosen>" "<corrected>" "<reason>"
  discover.py summary                     # count + entries + feedback counters
  discover.py feedback <id> <hit|error>   # close the loop on a correction
"""
from __future__ import annotations

import datetime
import fcntl
import json
import os
import sys
import tempfile
from pathlib import Path

STORE = Path(
    os.environ.get("DISCOVERY_STORE")
    or (Path(__file__).resolve().parent.parent / "data" / "discovery_feedback.json")
)


def _load() -> list:
    try:
        with open(STORE) as f:
            return json.load(f)
    except Exception:
        return []


def _save(d: list) -> None:
    fd, tmp = tempfile.mkstemp(dir=str(STORE.parent))
    with os.fdopen(fd, "w") as f:
        json.dump(d, f, indent=2)
    os.replace(tmp, STORE)


def _lock():
    return open(str(STORE) + ".lock", "a")


def consult(query: str) -> None:
    q = (query or "").lower()
    hits = [
        e
        for e in _load()
        if q in (e.get("query", "") or "").lower()
        or q in (e.get("corrected", "") or "").lower()
        or q in (e.get("reason", "") or "").lower()
    ]
    if not hits:
        print("(no prior correction for this query)")
        return
    for e in hits:
        print(
            f"ADVISORY PRIOR MISS: query='{e.get('query')}' -> chose "
            f"'{e.get('chosen')}', hint corrected='{e.get('corrected')}' "
            f"({e.get('reason')}). REVALIDATE against current active "
            f"set/catalog/intent before acting; do not honor blindly."
        )


def record(query: str, chosen: str, corrected: str, reason: str) -> None:
    with _lock() as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        d = _load()
        for e in d:
            if (
                e.get("query") == query
                and e.get("chosen") == chosen
                and e.get("corrected") == corrected
            ):
                e["count"] = e.get("count", 1) + 1
                e["last_seen"] = datetime.date.today().isoformat()
                _save(d)
                print(f"duplicate correction #{e['id']}: count={e['count']}")
                return
        n = max((e.get("id", 0) for e in d), default=0) + 1
        d.append(
            {
                "id": n,
                "date": datetime.date.today().isoformat(),
                "query": query,
                "chosen": chosen,
                "corrected": corrected,
                "reason": reason,
                "count": 1,
                "hits": 0,
                "errors": 0,
            }
        )
        _save(d)
        print(f"recorded correction #{n} (advisory; revalidate before trusting)")


def summary() -> None:
    d = _load()
    print(f"store entries: {len(d)}")
    for e in d:
        print(
            f"  #{e.get('id')} [{e.get('date')}] count={e.get('count', 1)} "
            f"hits={e.get('hits', 0)} errors={e.get('errors', 0)} "
            f"query='{e.get('query')}' -> corrected='{e.get('corrected')}'"
        )


def feedback(fid: int, kind: str) -> None:
    if kind not in ("hit", "error"):
        print(f"feedback kind must be 'hit' or 'error', got {kind!r}")
        return
    with _lock() as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        d = _load()
        for e in d:
            if e.get("id") == fid:
                e[kind + "s"] = e.get(kind + "s", 0) + 1
                _save(d)
                print(f"feedback recorded: #{fid} {kind}={e[kind + 's']}")
                return
        print(f"no entry #{fid}")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print("usage: discover.py {consult|record|summary|feedback} ...")
        sys.exit(1)
    cmd = args[0]
    if cmd == "consult" and len(args) >= 2:
        consult(args[1])
    elif cmd == "record" and len(args) >= 5:
        record(args[1], args[2], args[3], args[4])
    elif cmd == "summary":
        summary()
    elif cmd == "feedback" and len(args) >= 3:
        try:
            fid = int(args[1])
        except ValueError:
            print("feedback id must be an int")
            sys.exit(1)
        feedback(fid, args[2])
    else:
        print("usage: discover.py {consult|record|summary|feedback} ...")
        sys.exit(1)


if __name__ == "__main__":
    main()
