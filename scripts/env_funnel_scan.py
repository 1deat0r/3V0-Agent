#!/usr/bin/env python3
"""ENV-FUNNEL inventory + contract gate (tickets #19 / #20 / #21).

AST-based classifier for every ``os.environ`` / ``os.getenv`` touchpoint in
the prod tree. Replaces the per-batch manual grep-and-eyeball audit with one
command:

    python3 scripts/env_funnel_scan.py                 # default prod scope
    python3 scripts/env_funnel_scan.py tools/ agent/   # specific paths
    python3 scripts/env_funnel_scan.py --check tools/  # gate: 0 branded reads

Classification kinds:
- branded_read          os.environ.get("EV0_X"/"3V0_X"...) / os.getenv(...)   -> migrate to branded_env (#20)
- branded_bracket_read  x = os.environ["EV0_X"]      (KeyError-deliberate; case-by-case)
- branded_write         os.environ["EV0_X"] = ... / setdefault                              (write-half, later)
- branded_pop/del       os.environ.pop("EV0_X"...), del os.environ["EV0_X"]
- unprefixed_*          bare wire/config vars (IRC_SERVER, TERMINAL_CWD, ...) — documented exceptions
- dynamic               non-constant key (f-string/variable) — manual review required

Exit codes: 0 ok; 1 --check found branded reads in scope; 2 usage/IO error.
Stdlib-only, no project imports (safe to run from anywhere).
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

BRANDED_PREFIXES = ("3V0_", "EV0_")

READ_KINDS = ("branded_read", "branded_bracket_read")

# Default scan scope = the prod tree (tests/plugins are opt-in).
DEFAULT_SCOPE = (
    "agent/",
    "tools/",
    "gateway/",
    "threev0_cli/",
    "tui_gateway/",
    "acp_adapter/",
    "cron/",
    "cli.py",
    "run_agent.py",
    "batch_runner.py",
    "model_tools.py",
    "toolsets.py",
    "utils.py",
    "threev0_constants.py",
    "threev0_state.py",
)


@dataclass(frozen=True)
class Finding:
    file: str
    line: int
    kind: str
    var: str  # env-var name, or "<dynamic>" when the key isn't a constant


def _key_of(node: ast.AST) -> str | None:
    """Constant subscript/call key -> string; non-constant -> None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _is_os_environ(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Attribute)
        and node.attr == "environ"
        and isinstance(node.value, ast.Name)
        and node.value.id == "os"
    )


def _is_os_getenv_call(func: ast.AST) -> bool:
    return (
        isinstance(func, ast.Attribute)
        and func.attr == "getenv"
        and isinstance(func.value, ast.Name)
        and func.value.id == "os"
    )


def _classify_key(var: str | None, base_kind: str) -> tuple[str, str]:
    """(var, kind) pair given a resolved-or-None key and the unbranded kind."""
    if var is None:
        return "<dynamic>", "dynamic"
    if var.startswith(BRANDED_PREFIXES):
        return var, base_kind.replace("unprefixed", "branded")
    return var, base_kind


def classify_source(text: str) -> list[tuple[int, str, str]]:
    """Pure classifier: [(line, kind, var)] for one Python source text."""
    findings: list[tuple[int, str, str]] = []

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call) -> None:
            func = node.func
            line = node.lineno
            if isinstance(func, ast.Name) and func.id == "wire_env" and node.args:
                # The sanctioned bare-fallback accessor (unprefixed wire-var
                # decision, #20/#21 follow-up): counted as funnel-consumed.
                var = _key_of(node.args[0])
                findings.append((line, "wire_read", var))
                self.generic_visit(node)
                return
            if isinstance(func, ast.Attribute):
                # os.environ.get(...), os.environ.setdefault(...), os.environ.pop(...)
                if _is_os_environ(func.value) and func.attr in {"get", "setdefault", "pop"}:
                    if node.args:
                        var = _key_of(node.args[0])
                        if func.attr == "get":
                            kind = "unprefixed_read"
                        elif func.attr == "setdefault":
                            kind = "unprefixed_write"
                        else:
                            kind = "unprefixed_pop"
                        v, k = _classify_key(var, kind)
                        findings.append((line, k, v))
                elif _is_os_getenv_call(func) and node.args:
                    v, k = _classify_key(_key_of(node.args[0]), "unprefixed_read")
                    findings.append((line, k, v))
            self.generic_visit(node)

        def visit_Subscript(self, node: ast.Subscript) -> None:
            if _is_os_environ(node.value):
                var = _key_of(node.slice)
                if isinstance(node.ctx, ast.Load):
                    v, k = _classify_key(var, "unprefixed_bracket_read")
                elif isinstance(node.ctx, ast.Store):
                    v, k = _classify_key(var, "unprefixed_write")
                else:  # ast.Del
                    v, k = _classify_key(var, "unprefixed_del")
                findings.append((node.lineno, k, v))
            self.generic_visit(node)

    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    Visitor().visit(tree)
    return findings


def scan_file(path: Path) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    out = []
    for line, kind, var in classify_source(text):
        out.append(Finding(file=str(path), line=line, kind=kind, var=var))
    return out


def scan_paths(paths: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    seen = 0
    for raw in paths:
        p = Path(raw)
        if p.is_file() and p.suffix == ".py":
            findings.extend(scan_file(p))
            seen += 1
        elif p.is_dir():
            for py in sorted(p.rglob("*.py")):
                if any(part in {"__pycache__", "node_modules"} for part in py.parts):
                    continue
                findings.extend(scan_file(py))
                seen += 1
        else:
            print(f"env_funnel_scan: skipping missing path {raw}", file=sys.stderr)
    return findings


def summarize(findings: list[Finding]) -> dict[str, Counter]:
    per_file: dict[str, Counter] = defaultdict(Counter)
    for f in findings:
        per_file[f.file][f.kind] += 1
    return dict(per_file)


def branded_reads(findings: list[Finding]) -> list[Finding]:
    return [f for f in findings if f.kind in READ_KINDS]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "paths",
        nargs="*",
        default=None,
        help="files/directories to scan (default: the prod tree)",
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--verbose", action="store_true", help="list every finding line, not summaries"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if any branded READS remain in scope (the #21 gate)",
    )
    args = parser.parse_args(argv)

    scope = args.paths if args.paths else [
        s for s in DEFAULT_SCOPE if (Path(".") / s).exists()
    ]
    findings = scan_paths(scope)

    if args.check:
        bad = branded_reads(findings)
        if args.json:
            print(json.dumps({
                "ok": not bad,
                "branded_reads": [f.__dict__ for f in bad],
            }, indent=2))
        else:
            if bad:
                print(f"FAIL: {len(bad)} branded read(s) remain in scope:")
                for f in bad:
                    print(f"  {f.file}:{f.line}  {f.kind}  {f.var}")
            else:
                print("OK: no branded env reads remain in scope.")
        return 1 if bad else 0

    if args.json:
        print(json.dumps({
            "scope": scope,
            "findings": [f.__dict__ for f in findings],
            "totals": dict(Counter(f.kind for f in findings)),
        }, indent=2))
        return 0

    per_file = summarize(findings)
    totals = Counter(f.kind for f in findings)
    width = max((len(k) for k in per_file), default=0)
    for fname in sorted(per_file):
        c = per_file[fname]
        cells = "  ".join(f"{k}={c[k]}" for k in sorted(c) if c[k])
        print(f"{fname.ljust(width)}  {cells}")
    print()
    print("TOTALS:", "  ".join(f"{k}={totals[k]}" for k in sorted(totals)))
    if args.verbose:
        print()
        for f in sorted(branded_reads(findings), key=lambda f: (f.file, f.line)):
            print(f"  MIGRATE {f.file}:{f.line}  {f.var}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
