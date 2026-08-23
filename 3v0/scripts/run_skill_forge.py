#!/usr/bin/env python3
"""3V0-owned SkillForge driver — synthesize a skill proposal from a body module.

The "create half" of the skill axis (SkillForge, arXiv 2608.18933 kernel #6):
instead of waiting for a real-task failure, proactively distill a reusable
skill from a module in the body's own core/ that encodes a proven method. This
driver emits a *proposal* (name/category/description/overview/public_callables/
proposal_id) that a follow-on model pass can flesh into a real SKILL.md, then
write store-first via record_skills.py (gated by safe_evolve, like curation).

Pure + deterministic: no LLM, no store write — only synthesis. Best-effort:
a module without public callables yields nothing.

Usage:
  python3 3v0/scripts/run_skill_forge.py --module core/safe_evolve.py
  python3 3v0/scripts/run_skill_forge.py --module core/memdb.py --json
  python3 3v0/scripts/run_skill_forge.py --all 2>/dev/null | head
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.skill_forge import synthesize_proposal  # noqa: E402

DEFAULT_CORE = REPO_ROOT / "3v0" / "core"


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

    # --all: iterate core modules (skip tests/scripts/plugins/init). Emit
    # compact (single-line) so a consumer can stream NDJSON.
    for p in sorted(DEFAULT_CORE.glob("*.py")):
        if p.name == "__init__.py":
            continue
        _one(p, compact=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())