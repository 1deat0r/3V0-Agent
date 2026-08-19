#!/usr/bin/env python3
"""Wake-time standing-system runner: coherence then coalesce. Best-effort.

* coherence.run(apply=True) — detect + auto-resolve mechanical contradictions
  (one example this system was built for: README drifting from core modules),
  fail-closed on policy/substrate divergence / stale-doctrine reintroduction.
* coalesce.run(...) — watermark-BOUNDED consolidation (conflict reconcile +
  conservative near-duplicate merge), so it fires on cadence across wakes,
  never every wake, and never fails the wake: any error degrades to a message
  and exit 0.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # -> 3v0/

from core import coherence, coalesce, memdb  # noqa: E402


def main() -> int:
    try:
        rep = coherence.run(apply=True)
        for c in rep.conflicts:
            tag = "resolved" if c.resolved else "OPEN (fail-closed)"
            print(f"  coherence[{tag}] {c.name}: {c.detail}")
    except Exception as e:  # noqa: BLE001 - never fail the wake
        print(f"  coherence: skipped ({e})")
    try:
        conn = memdb.connect(memdb.DEFAULT_PATH)
        r = coalesce.run(conn)
        if r.fired:
            print(f"  coalesce: fired  reconciled={r.reconciled} "
                  f"merged={r.merged} superseded={len(r.superseded_ids)}")
        else:
            print(f"  coalesce: not-due ({r.reason})")
    except Exception as e:  # noqa: BLE001
        print(f"  coalesce: skipped ({e})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())