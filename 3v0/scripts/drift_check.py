#!/usr/bin/env python3
"""One-page drift report over every project in the ledger.

The "clock" of the multi-project meta (Stone 16): iterate the ledger
generically, compare each project's live HEAD / upstream / store against its
recorded position, and print a one-page report. Drift is made *visible*, not
auto-fixed (report-only posture; the operator + orchestrator decide the fix).

Options:
  --update         record the current position (HEAD / upstream head / store
                   hash / last-seen) back into the ledger after checking
  --json           machine-readable JSON on stdout (for the daemon tick)
  --fail-on-drift  exit 1 when any project reports drift (CI-style gate)

Env (tests / explicit): THREEV0_BODY (body root), THREEV0_LEDGER (ledger path).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.drift import collect_git_state, compute_drift, store_hash  # noqa: E402
from core.projects import ProjectLedger  # noqa: E402

BODY = Path(os.environ.get("THREEV0_BODY") or REPO_ROOT)
LEDGER_PATH = Path(
    os.environ.get("THREEV0_LEDGER") or (BODY / "3v0" / "data" / "projects" / "ledger.json")
)
HOME = Path.home()


def _short(sha: str | None) -> str:
    return sha[:12] if sha else "-"


def _store_word(report: dict) -> str:
    if report["store_present"] is None:
        return "-"
    if not report["store_present"]:
        return "MISSING"
    return "changed" if report["store_changed"] else "clean"


def run_check(update: bool = False) -> dict:
    """Iterate the ledger, report drift, optionally record position."""
    try:
        ledger = ProjectLedger.load(body_root=BODY, home=HOME, path=LEDGER_PATH)
    except FileNotFoundError:
        return {"checked_at": None, "drifting": 0, "projects": [], "error": f"no ledger at {LEDGER_PATH}"}
    except (OSError, ValueError) as e:
        return {"checked_at": None, "drifting": 0, "projects": [], "error": f"ledger unreadable: {e}"}

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    reports: List[dict] = []
    for entry in ledger.entries():
        git = collect_git_state(entry)
        sh = store_hash(entry.store)
        report = compute_drift(entry, git, sh)
        reports.append(report)
        if update:
            ledger.add(
                replace(
                    entry,
                    head=git.head,
                    upstream_head=git.upstream_head,
                    store_head=sh,
                    last_seen_at=now,
                )
            )
    if update:
        ledger.save(body_root=BODY, home=HOME, path=LEDGER_PATH)
    return {
        "checked_at": now,
        "drifting": sum(1 for r in reports if r["drifting"]),
        "total": len(reports),
        "projects": reports,
    }


def _print_human(result: dict) -> None:
    if result.get("error"):
        print(result["error"], file=sys.stderr)
        return
    print(f"=== drift check: {result['total']} project(s) — {result['checked_at']} ===")
    for r in result["projects"]:
        verdict = "DRIFT" if r["drifting"] else "OK"
        line = (
            f"  {verdict:5} {r['title']:10} ({r['name']})  "
            f"behind={r['behind'] if r['behind'] is not None else '?'} "
            f"ahead={r['ahead'] if r['ahead'] is not None else '?'}  "
            f"dirty={'yes' if r['dirty'] else 'no'}  "
            f"store={_store_word(r)}"
        )
        if r["head_moved"]:
            line += "  [head moved]"
        if r["open_loops"]:
            line += f"  [open_loops={len(r['open_loops'])}]"
        print(line)
        if r["reasons"]:
            for reason in r["reasons"]:
                print(f"         - {reason}")
    print(
        f"summary: {result['drifting']} drifting, "
        f"{result['total'] - result['drifting']} ok"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="one-page drift report over the ledger")
    ap.add_argument("--update", action="store_true", help="record position into the ledger")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--fail-on-drift", action="store_true", help="exit 1 if any project drifts")
    args = ap.parse_args()

    result = run_check(update=args.update)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        _print_human(result)

    if args.fail_on_drift and result.get("drifting", 0) > 0:
        return 1
    if result.get("error"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
