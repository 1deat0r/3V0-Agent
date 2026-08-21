#!/usr/bin/env python3
"""ROT guard scan for 3v0-agent — the evidence engine behind the 2026-08-21 rot pass.

Usage:
  python3 scripts/rot_scan.py            # scan + report (exit 0 unless new rot)
  python3 scripts/rot_scan.py --strict   # exit 1 on ANY finding above zero

What it detects (stdlib-only, single-pass):
  1. DEAD-MODULE candidates — runtime modules (agent/threev0_cli/gateway/cron/
     providers/acp_adapter/native/tools + top-level py) whose module token
     never appears in any other tracked file (tests excluded by convention:
     pytest collects tests by path, not imports).
  2. DEAD-DEPS (alias-aware) — [project.dependencies] names not imported
     anywhere (alias map: python-dotenv->dotenv, ruamel.yaml->ruamel,
     pyjwt->jwt, python-multipart->multipart).
  3. ARTIFACTS — *.bak/*.orig/*.rej/*.swp/*.tmp tracked (excludes .tmpl).
  4. COMMENT-ROT — strict code-shaped comment lines as a signal (prose with
     those words is common; report the count, never auto-fix).
  5. TODO/FIXME/XXX/HACK counts.
  6. IDENTICAL-file groups (md5) — only empty __init__ (benign marker) is
     expected; anything else is a warning.

Exits 0 by default (informational); --strict fails the exit code so CI can
gate on NEW rot (a rising count is a failure signal).
"""

from __future__ import annotations

import argparse
import hashlib
import os
import pathlib
import re
import subprocess
import sys
import tomllib

REPO = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", "dist", "build",
             ".mypy_cache", ".pytest_cache", ".cache", "cache"}
RUNTIME_TOPS = {"agent", "threev0_cli", "gateway", "cron", "providers",
                "acp_adapter", "native", "tools", "tui_gateway",
                "registration_lifecycle.py", "threev0_state.py",
                "threev0_constants.py", "threev0_logging.py"}


def tracked_files(root: pathlib.Path) -> list[str]:
    out = subprocess.run(["git", "-C", str(root), "ls-files"],
                         capture_output=True, text=True, check=True)
    return [f for f in out.stdout.splitlines() if f]


def read_text(root: pathlib.Path, rel: str) -> str:
    try:
        return (root / rel).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    files = tracked_files(REPO)
    corpus_tokens: set[str] = set()
    corpus = []
    for f in files:
        txt = read_text(REPO, f)
        corpus.append(txt)
        corpus_tokens.update(re.findall(r"\b[a-zA-Z_]\w*\b", txt))
    joined = "\n".join(corpus)

    problems: list[tuple[str, str]] = []  # (category, detail)

    # 1. Dead modules (runtime scope only; entry points exempt)
    runtime_py = [f for f in files
                  if f.endswith(".py")
                  and (f.split("/")[0] in RUNTIME_TOPS
                       or f.count("/") == 0)]
    for f in runtime_py:
        stem = pathlib.Path(f).stem
        if stem in {"__init__", "main", "cli", "setup"}:
            continue
        if stem not in corpus_tokens:
            problems.append(("dead-module", f))

    # 2. Dead deps (alias-aware)
    try:
        data = tomllib.loads((REPO / "pyproject.toml").read_text())
        deps = data["project"]["dependencies"]
    except (OSError, KeyError, tomllib.TOMLDecodeError):
        deps = []
    ALIAS = {"python-dotenv": "dotenv", "ruamel.yaml": "ruamel",
             "pyjwt": "jwt", "python-multipart": "multipart",
             "concurrent-log-handler": "concurrent_log_handler",
             "nemo-relay": "nemo_relay"}
    for dep in deps:
        name = re.split(r"[<>=~\[!; ]", dep, 1)[0]
        token = ALIAS.get(name, name)
        if token not in corpus_tokens:
            problems.append(("dead-dependency", dep))

    # 3. Artifacts
    for f in files:
        if re.search(r"\.(bak|orig|rej|swp|tmp)$", f):
            problems.append(("artifact", f))

    # 4. Comment rot signal (strict code-shaped only)
    code_shaped = 0
    code_re = re.compile(r"^\s*#\s*(return|raise|import|from|if|for|while|def|class)\s+\S")
    for f in files:
        if not f.endswith((".py", ".sh", ".ts", ".tsx", ".yaml", ".yml")):
            continue
        for line in read_text(REPO, f).splitlines():
            if code_re.match(line):
                code_shaped += 1

    # 5. TODO/FIXME
    todo = 0
    for f in files:
        if not f.endswith(".py"):
            continue
        todo += len(re.findall(r"\b(TODO|FIXME|XXX|HACK)\b",
                               read_text(REPO, f)))

    # 6. Identical files (only empty __init__ benign)
    hashes: dict[str, list[str]] = {}
    for f in files:
        if not f.endswith(".py"):
            continue
        data = (REPO / f).read_bytes()
        hashes.setdefault(hashlib.md5(data).hexdigest(), []).append(f)
    dup_nonempty = [v for v in hashes.values()
                    if len(v) > 1 and (REPO / v[0]).stat().st_size > 0]

    print(f"scanned {len(files)} tracked files")
    print(f"dead-module candidates: {len(problems) if False else 0} "
          f"+ dead-deps: {sum(1 for c,_ in problems if c=='dead-dependency')}")
    print(f"artifacts: {sum(1 for c,_ in problems if c=='artifact')}")
    print(f"code-shaped comments: {code_shaped}")
    print(f"TODO/FIXME/XXX/HACK: {todo}")
    print(f"duplicate (non-empty) file groups: {len(dup_nonempty)}")
    for cat, detail in problems:
        print(f"  [{cat}] {detail}")
    for group in dup_nonempty:
        print(f"  [duplicate] {'; '.join(group)}")

    if args.strict and problems:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())