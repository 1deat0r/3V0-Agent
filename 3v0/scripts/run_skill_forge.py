#!/usr/bin/env python3
"""3V0-owned SkillForge driver — synthesize + author a skill from a body module.

The "create half" of the skill axis (SkillForge, arXiv 2608.18933 kernel #6):
instead of waiting for a real-task failure, proactively distill a reusable
skill from a module in the body's own core/ that encodes a proven method. This
driver:

  --module <path>      emit the *proposal* (pretty JSON)
  --author <path>      emit the authored SKILL.md body (deterministic)
  --write <path>       ALSO write the authored SKILL.md store-first via
                       record_skills.py --action skill_update (the exact
                       threev0_record backend), gated by safe_evolve — a
                       blocking (unsafe) body is refused and never written.
  --all                synthesize proposals for every core module (NDJSON)

Pure + deterministic: no LLM, no store write unless --write. Best-effort: a
module without public callables yields nothing.

Usage:
  python3 3v0/scripts/run_skill_forge.py --module core/safe_evolve.py
  python3 3v0/scripts/run_skill_forge.py --author core/safe_evolve.py
  python3 3v0/scripts/run_skill_forge.py --write core/safe_evolve.py
  python3 3v0/scripts/run_skill_forge.py --all 2>/dev/null | head
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.skill_forge import synthesize_proposal  # noqa: E402
from core.forge_skill import build_skill_md  # noqa: E402
from core.safe_evolve import audit as _safe_evolve_audit  # noqa: E402

DEFAULT_CORE = REPO_ROOT / "3v0" / "core"
RECORD_SKILLS = REPO_ROOT / "3v0" / "scripts" / "record_skills.py"


def _emit(prop: dict, *, compact: bool = False) -> None:
    if compact:
        print(json.dumps(prop, ensure_ascii=False))
    else:
        print(json.dumps(prop, ensure_ascii=False, indent=2))


def main() -> int:
    ap = argparse.ArgumentParser(description="3V0 SkillForge driver")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--module", help="core/ module path to synthesize from")
    group.add_argument(
        "--author", metavar="PATH",
        help="emit the authored SKILL.md for a module",
    )
    group.add_argument(
        "--write", metavar="PATH",
        help="author + write the SKILL.md store-first via record_skills.py "
        "(gated by safe_evolve)",
    )
    group.add_argument(
        "--all", action="store_true",
        help="synthesize proposals for every core module that has public "
        "callables",
    )
    ap.add_argument("--json", action="store_true", help="emit proposal(s) as JSON")
    args = ap.parse_args()

    def _one(module_path: Path, *, compact: bool = False) -> None:
        if not module_path.exists():
            print(json.dumps({"error": f"module not found: {module_path}"}))
            return
        prop = synthesize_proposal(module_path)
        if prop is None:
            print(json.dumps({"skipped": str(module_path)}))
            return
        _emit(prop, compact=compact)

    if args.module:
        _one(Path(args.module), compact=args.json)
        return 0

    if args.author or args.write:
        path = Path(args.author or args.write)
        if not path.exists():
            print(json.dumps({"error": f"module not found: {path}"}))
            return 1
        prop = synthesize_proposal(path)
        if prop is None:
            print(json.dumps({"skipped": str(path)}))
            return 1
        body = build_skill_md(prop)
        if args.author:
            print(body)
            return 0
        # --write: gate the DISTILLED PROCEDURE TEXT (the authored body PLUS
        # the source callables' docstrings the skill encodes — a docstring
        # that documents a destructive command is unsafe even if the distilled
        # body's free text doesn't repeat the literal). A blocking result is a
        # refusal; the store is never touched.
        docs_text = "\n".join(
            str(d) for d in (prop.get("callable_docs") or {}).values() if d
        )
        gate = _safe_evolve_audit(body + "\n" + docs_text)
        if gate.blocking:
            print(json.dumps({
                "refused": f"safe_evolve blocked: {gate.reason()}",
                "name": prop["name"],
            }))
            return 1
        name = prop["name"].split("/")[-1]
        env = dict(os.environ)
        env.setdefault("THREEV0_SKILL_STORE", str(REPO_ROOT / "3v0" / "data" / "skills.json"))
        proc = subprocess.run(
            [sys.executable, str(RECORD_SKILLS), "--action", "skill_update",
             "--name", name, "--content", body, "--write", "--json"],
            capture_output=True, text=True, timeout=30, env=env,
        )
        if proc.returncode != 0:
            out = proc.stdout.strip() or proc.stderr.strip() or "unknown error"
            print(json.dumps({"error": f"record_skills failed: {out}"}))
            return 1
        print(proc.stdout.strip() or json.dumps({"applied": True, "name": name}))
        return 0

    # --all: iterate core modules (skip tests/scripts/plugins/init). Emit
    # compact (single-line) so a consumer can stream NDJSON.
    for p in sorted(DEFAULT_CORE.glob("*.py")):
        if p.name == "__init__.py":
            continue
        _one(p, compact=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())