#!/usr/bin/env python3
"""Onboard and inspect projects in the drift ledger.

The onboarding surface of the multi-project meta (Stone 16): a project is a
*ledger entry*, never a code edit. Any git repo with an upstream is
onboardable; the three known projects are seed entries, not the schema.

Commands:
  project.py add <name> --repo <path> [--upstream origin] [--ref main]
              [--profile <name>] [--delta <desc>] [--store <path>]
              [--skill-store <path>] [--primary] [--no-track] [--title <str>]
  project.py list
  project.py status [<name> ...] [--update]
  project.py remove <name>

Env (tests / explicit): THREEV0_BODY (body root), THREEV0_LEDGER (ledger path).

``--profile <name>`` marks a project as a Hermes hardfork 3V0 reviews, and
defaults its store to ``3v0/data/<name>/memory.json``. ``--primary`` is 3V0's
own slot (store + skill axis + profile projection). Without either, a project
is drift-tracking only (no store, no review).
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.drift import compute_drift  # noqa: E402
from core.gitstate import collect_git_state, store_hash  # noqa: E402
from core.projects import LedgerEntry, ProjectLedger  # noqa: E402

BODY = Path(os.environ.get("THREEV0_BODY") or REPO_ROOT)
LEDGER_PATH = Path(
    os.environ.get("THREEV0_LEDGER") or (BODY / "3v0" / "data" / "projects" / "ledger.json")
)
HOME = Path.home()


def _user_path(raw: str) -> Path:
    """Normalize a user-supplied path (expand ~; resolve relative to cwd)."""
    p = Path(raw).expanduser()
    if not p.is_absolute():
        p = (Path.cwd() / p).resolve()
    return p


def _load() -> ProjectLedger:
    try:
        return ProjectLedger.load(body_root=BODY, home=HOME, path=LEDGER_PATH)
    except FileNotFoundError:
        return ProjectLedger({})
    except (OSError, ValueError) as e:
        print(f"ledger unreadable: {e}", file=sys.stderr)
        raise SystemExit(1)


def _short(sha: Optional[str]) -> str:
    return sha[:12] if sha else "(unknown)"


def cmd_add(args) -> int:
    ledger = _load()
    name = args.name.strip()
    if name in ledger:
        print(f"project {name!r} already exists — remove it first", file=sys.stderr)
        return 1

    repo = _user_path(args.repo)
    if not repo.exists():
        print(f"warning: repo does not exist yet: {repo}", file=sys.stderr)

    store: Optional[Path] = None
    skill_store: Optional[Path] = None
    if args.store:
        store = _user_path(args.store)
    elif args.primary:
        store = BODY / "3v0" / "data" / "memory.db"
    elif args.profile:
        store = BODY / "3v0" / "data" / name / "memory.json"
    if args.skill_store:
        skill_store = _user_path(args.skill_store)
    elif args.primary:
        skill_store = BODY / "3v0" / "data" / "skills.json"

    entry = LedgerEntry(
        name=name,
        title=args.title or name,
        repo=repo,
        upstream=args.upstream,
        upstream_ref=args.ref,
        delta=args.delta or "",
        track_upstream=not args.no_track,
        profile=args.profile,
        store=store,
        skill_store=skill_store,
        primary=args.primary,
    )
    ledger.add(entry)
    ledger.save(body_root=BODY, home=HOME, path=LEDGER_PATH)
    kind = "primary" if entry.primary else ("reviewed hardfork" if entry.store else "drift-tracked")
    print(f"added {name!r} ({kind}) -> {LEDGER_PATH}")
    print(f"  repo:    {entry.repo}")
    print(f"  upstream: {entry.upstream}/{entry.upstream_ref} (track={entry.track_upstream})")
    if entry.store:
        print(f"  store:   {entry.store}")
    if entry.skill_store:
        print(f"  skills:  {entry.skill_store}")
    if entry.delta:
        print(f"  delta:   {entry.delta}")
    return 0


def cmd_list(args) -> int:
    ledger = _load()
    if not ledger:
        print("(no projects — onboard one with `project.py add ...`)")
        return 0
    for entry in ledger.entries():
        store = "store" if entry.store else "drift-only"
        profile = entry.profile or "-"
        track = "track" if entry.track_upstream else "pinned"
        print(
            f"{entry.name:14} {entry.title:10} profile={profile:8} "
            f"upstream={entry.upstream}/{entry.upstream_ref:5} {track:5} {store:10} "
            f"repo={entry.repo}"
        )
    return 0


def _print_status(report: dict) -> None:
    print(f"=== {report['title']} ({report['name']}) ===")
    print(f"  repo:      {report['repo']}")
    print(
        f"  profile={report['profile'] or '-'}  primary={'yes' if report['primary'] else 'no'}  "
        f"upstream={report['upstream']}/{report['upstream_ref']}  "
        f"track={'yes' if report['track_upstream'] else 'no'}"
    )
    if report["delta"]:
        print(f"  delta:     {report['delta']}")
    print(f"  HEAD:      {_short(report['head'])}" + ("  (moved since snapshot)" if report["head_moved"] else ""))
    if report["upstream_head"]:
        print(
            f"  upstream:  {_short(report['upstream_head'])}  "
            f"(behind {report['behind']}, ahead {report['ahead']})"
        )
    else:
        print("  upstream:  (ref not found — fetch?)")
    if report["store_present"] is not None:
        state = "present" if report["store_present"] else "MISSING"
        if report["store_changed"]:
            state += " (changed since snapshot)"
        print(f"  store:     {state}")
    if report["open_loops"]:
        print("  open loops:")
        for loop in report["open_loops"]:
            print(f"    - {loop}")
    verdict = "DRIFT" if report["drifting"] else "OK"
    if report["reasons"]:
        verdict += " — " + "; ".join(report["reasons"])
    print(f"  VERDICT:   {verdict}")
    print()


def cmd_status(args) -> int:
    ledger = _load()
    names: List[str] = args.names or ledger.names()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for name in names:
        entry = ledger.get(name)
        if entry is None:
            print(f"unknown project: {name!r}", file=sys.stderr)
            return 1
        git = collect_git_state(entry)
        sh = store_hash(entry.store)
        report = compute_drift(entry, git, sh)
        _print_status(report)
        if args.update:
            ledger.add(
                replace(
                    entry,
                    head=git.head,
                    upstream_head=git.upstream_head,
                    store_head=sh,
                    last_seen_at=now,
                )
            )
    if args.update:
        ledger.save(body_root=BODY, home=HOME, path=LEDGER_PATH)
        print("(position recorded in the ledger)")
    return 0


def cmd_remove(args) -> int:
    ledger = _load()
    name = args.name.strip()
    if name not in ledger:
        print(f"unknown project: {name!r}", file=sys.stderr)
        return 1
    ledger.remove(name)
    ledger.save(body_root=BODY, home=HOME, path=LEDGER_PATH)
    print(f"removed {name!r} from the ledger")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="onboard/inspect projects in the drift ledger")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="onboard a project as a ledger entry")
    p_add.add_argument("name")
    p_add.add_argument("--repo", required=True, help="path to the git repo (~/... ok)")
    p_add.add_argument("--upstream", default="origin", help="git remote name to merge from")
    p_add.add_argument("--ref", default="main", help="branch on that remote")
    p_add.add_argument("--profile", default=None, help="Hermes profile name (marks a reviewed hardfork)")
    p_add.add_argument("--delta", default="", help="description of the deliberate divergence")
    p_add.add_argument("--store", default=None, help="canonical memory store path")
    p_add.add_argument("--skill-store", default=None, help="canonical skill store path")
    p_add.add_argument("--primary", action="store_true", help="3V0's own slot (store + skills + projection)")
    p_add.add_argument("--no-track", action="store_true", help="deliberate hardfork; behind/ahead is informational")
    p_add.add_argument("--title", default=None, help="display name (default: the project name)")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="list every project in the ledger")
    p_list.set_defaults(func=cmd_list)

    p_status = sub.add_parser("status", help="live drift status (default: all projects)")
    p_status.add_argument("names", nargs="*", help="project names (default: all)")
    p_status.add_argument("--update", action="store_true", help="record position into the ledger")
    p_status.set_defaults(func=cmd_status)

    p_remove = sub.add_parser("remove", help="drop a project from the ledger")
    p_remove.add_argument("name")
    p_remove.set_defaults(func=cmd_remove)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
