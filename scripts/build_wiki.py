#!/usr/bin/env python3
"""Build/check the 3V0 codebase wiki — the LLM-readable library index.

The wiki is a persistent, interlinked catalog of the codebase (Karpathy's
"LLM Wiki" pattern applied to a library): code is the raw source, ``wiki/``
is the compiled knowledge layer. An agent (typically the small aux model)
reads ``index.md`` first, then drills into ``areas/*.md`` or raw files.

100% coverage is the invariant: every *tracked* path has exactly one row in
``wiki/manifest.tsv`` with non-empty purpose / why / related. The checker
enforces this, so the index can never silently drift behind the tree.

Rows are ``manual`` (hand-curated, never clobbered) or ``auto``
(regenerated from module docstrings + path rules). Entry text is capped so a
budget-constrained model can read whole area pages in one pass.

Options:
  --rebuild   regenerate manifest.tsv (keeps manual rows) + render areas/*
  --check     enforce 100% coverage; exit 1 on any gap (verify.sh gate)
  --report    print coverage summary + per-area counts
  --json      JSON stdout (with --report)
Env: THREEV0_BODY (repo root, default = parent of this file).
"""
from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("THREEV0_BODY", SCRIPT_DIR.parent))
WIKI = ROOT / "wiki"
MANIFEST = WIKI / "manifest.tsv"
AREAS_DIR = WIKI / "areas"

FIELDS = ["path", "kind", "curated", "purpose", "why", "related"]
MAXLEN = {"purpose": 160, "why": 160, "related": 220}
CURATED = WIKI / "curated.tsv"

AREA_ORDER = [
    "ROOT", "CORE", "AGENT", "STATE", "TOOLS", "CLI", "GATEWAY", "CRON",
    "PLUGINS", "SKILLS", "PROVIDERS", "APPS", "UITUI", "WEB", "WEBSITE",
    "DOCS", "SCRIPTS", "TESTS", "INFRA", "MISC",
]
AREA_TITLE = {
    "ROOT": "Repository root — load-bearing core entrypoints",
    "CORE": "3v0/ — the sovereign agent core (memory, standing systems)",
    "AGENT": "agent/ — AIAgent internals (providers, memory, caching, audio)",
    "STATE": "ev0_state* + ev0_constants/logging — session store & profile paths",
    "TOOLS": "tools/ + toolsets.py + model_tools.py — model tool orchestration",
    "CLI": "ev0_cli/ + cli.py — interactive CLI, config, skins, subcommands",
    "GATEWAY": "gateway/ + tui_gateway/ — platform adapters + TUI backend",
    "CRON": "cron/ — scheduled jobs",
    "PLUGINS": "plugins/ — plugin ecosystem (memory, providers, tools)",
    "SKILLS": "skills/ + optional-skills/ — the skill libraries",
    "PROVIDERS": "providers/ + native/ — inference provider profiles",
    "APPS": "apps/ — desktop app + shared TS packages",
    "UITUI": "ui-tui/ — Ink terminal UI",
    "WEB": "web/ — dashboard frontend",
    "WEBSITE": "website/ — Docusaurus docs site",
    "DOCS": "docs/ + README* + CONTRIBUTING* — documentation",
    "SCRIPTS": "scripts/ — dev/test/ops tooling",
    "TESTS": "tests/ + tests-js/ + evals/ — the test suites",
    "INFRA": "docker/ nix/ .github/ packaging — deployment & CI",
    "MISC": "locales/ assets/ contributors/ — auxiliary content",
}


def tracked_files(root: Path) -> list[str]:
    out = subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"git ls-files failed: {out.stderr}")
    return [p for p in out.stdout.split("\0") if p]


def module_docstring(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    import warnings
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(text)
    except SyntaxError:
        return ""
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) \
                and isinstance(node.value.value, str):
            first = node.value.value.strip().splitlines()
            return first[0].strip() if first else ""
    return ""


def clean(s: str, cap: int) -> str:
    s = re.sub(r"\s+", " ", s).strip().replace("\t", " ")
    return s[:cap]


def sibling_files(path: str, fileset: set[str]) -> list[str]:
    parent = path.rsplit("/", 1)[0] if "/" in path else "."
    prefix = parent + "/" if parent != "." else ""
    return sorted(s for s in fileset
                  if s.startswith(prefix) and s != path)


def walkup_files(path: str, fileset: set[str]) -> list[str]:
    """Nearest files at any ancestor directory (for singleton files)."""
    parts = path.split("/")
    for depth in range(len(parts) - 1, 0, -1):
        anc = "/".join(parts[:depth])
        prefix = anc + "/"
        sibs = sorted(s for s in fileset
                      if s.startswith(prefix) and "/" not in s[len(prefix):])
        if sibs:
            return sibs
    return []


def relations(path: str, fileset: set[str]) -> str:
    """Auto-derive related entries so every row has a non-empty relationship
    column (the operator's 100% relationships invariant), even on auto rows.
    Test files point at the module(s) they exercise; other files point at
    same-directory siblings; singletons walk up to the nearest populated
    directory; last resort is the containing directory itself."""
    budget: list[str] = []

    def add(others: list[str]):
        for x in others:
            if x == path or x in budget:
                continue
            if len("; ".join(budget + [x])) > 200:
                break
            budget.append(x)

    name = path.rsplit("/", 1)[-1]
    is_test = name.startswith("test_") or name.endswith("_test.py") \
        or "/tests/" in path or path.startswith("tests/") \
        or path.startswith("3v0/tests/")
    if is_test:
        cands: list[str] = []
        core = path
        for prefix in ("3v0/tests/", "tests/"):
            if core.startswith(prefix):
                core = core[len(prefix):]
                break
        stem = core[:-3] if core.endswith(".py") else core
        if stem.startswith("test_"):
            stem = stem[5:]
        if stem.endswith("_test"):
            stem = stem[:-5]
        cands.append(stem + ".py")
        if core.count("/") >= 1:
            cands.append(core.replace("test_", "", 1))
        if path.startswith("3v0/tests/"):
            cands.append("3v0/core/" + stem + ".py")
            cands.append("3v0/scripts/" + stem + ".py")
        cands.append(core.split("/", 1)[0] + ".py")
        hits = [c for c in cands if c in fileset and c != path]
        add(hits)
        add(sibling_files(path, fileset))
    else:
        add(sibling_files(path, fileset))
    if not budget:
        add(walkup_files(path, fileset))
    if not budget:
        budget.append(path.rsplit("/", 1)[0] + "/")
    return "; ".join(budget)


def classify(path: str) -> tuple[str, str, str]:
    p = Path(path)
    name = p.name
    low = path.lower()
    parent = str(p.parent)

    if name in ("uv.lock", "package-lock.json"):
        return ("lockfile", "Generated dependency lockfile",
                "Pins every transitive dep with hashes (supply-chain invariant); regenerated by uv/npm")
    if name in ("pyproject.toml",):
        return ("build", "Python packaging + dependency declaration",
                "Defines the installable package, upper-pinned deps, tool config")
    if name == "setup.py":
        return ("build", "Legacy setup shim", "Compatibility entrypoint delegating to pyproject")
    if name == "setup-3v0.sh":
        return ("script", "Environment bootstrap shell", "Provision a working 3V0 run/dev environment")
    if name == "3v0-cli":
        return ("script", "CLI launcher", "Entry shim that execs the CLI with profile wiring")
    if name == ".bytecode-fingerprint":
        return ("artifact", "Bytecode compile fingerprint", "Runtime freshness marker; regenerated")
    if name.endswith((".pyc", ".pyo")):
        return ("artifact", "Bytecode cache", "Transient interpreter cache; reproducible")
    if name.endswith(".md"):
        if name == "SKILL.md":
            return ("skill-doc", f"Skill definition for `{p.parent.name}`",
                    "The instruction contract a model loads when the skill's trigger matches")
        if parent == "skills" and path.count("/") == 1:
            return ("category-doc", f"Category overview for `{name[:-3]}` skills",
                    "Groups related skills under one loadable surface")
        m = re.match(r"README(?:\.([a-z-]+))?\.md$", name)
        if m:
            lang = m.group(1) or "en"
            return ("readme", f"README ({lang})", "Project introduction & quickstart for humans/new agents")
        if name.startswith(("CONTRIBUTING", "SECURITY", "SUSTAINABILITY", "SELF_IMPROVEMENT")):
            return ("policy-doc", f"{name[:-3]} policy", "Defines the contribution/security contract")
        return ("doc", "Documentation page", "Human/agent-readable explanation; knowledge layer")
    if name.endswith(".py"):
        doc = clean(module_docstring(p), MAXLEN["purpose"])
        kind = "test" if parent.startswith("tests") or "test" in name else "source"
        why = ("Test module — asserts the repo contract; run via scripts/run_tests.sh"
               if kind == "test" else
               "Python module executed or imported by the runtime; check git intent before deleting")
        if parent.startswith("scripts/"):
            kind, why = "script", "Dev/ops/release tooling invoked from the command line or CI"
        return (kind, doc or f"Python module `{name}`", why)
    if name.endswith(".ts"):
        return ("frontend-ts", clean(module_docstring(p) or f"TypeScript module `{name}`", MAXLEN["purpose"]),
                "Frontend/shared TS source consumed by the tsc/vite build")
    if name.endswith((".tsx", ".jsx")):
        return ("frontend-tsx", f"React component `{name}`",
                "Renders part of a frontend surface; bundled by the TS build")
    if name == "package.json":
        return ("build", "Node package manifest", "Declares JS workspace deps + scripts")
    if name.endswith((".yaml", ".yml")):
        return ("config", "YAML configuration", "Declarative config for deployment/CI/tooling")
    if name.endswith(".sh"):
        return ("script", "Shell script", "Shell automation invoked manually or by CI/hooks")
    if name.endswith(".css"):
        return ("asset", "Stylesheet", "Styling for a frontend surface")
    if name.endswith((".png", ".jpg", ".svg", ".ico", ".webp", ".gif")):
        return ("asset", "Image asset", "Static media referenced by docs or frontend")
    if name.endswith((".wav", ".mp3")):
        return ("asset", "Audio asset", "Audio sample used by tests or TTS validation")
    if name.endswith((".sqlite", ".db")):
        return ("data", "SQLite database", "Persistent store; canonical state is git-versioned")
    if name == "flake.lock":
        return ("lockfile", "Nix flake lock", "Pins nix derivation inputs; regenerated by nix flake lock")
    if name.endswith(".json"):
        return ("data" if "data" in parent else "config",
                "Structured data/config file", "Persistent state or declarative config read by tooling")
    return ("asset", f"File `{name}`",
            "Repository content; see related files / area page for the enclosing subsystem")


def area_of(path: str) -> str:
    head = path.split("/")[0]
    if head == "3v0":
        return "CORE"
    if head == "agent":
        return "AGENT"
    if head == "tools":
        return "TOOLS"
    if head in ("model_tools.py", "toolsets.py", "toolset_distributions.py"):
        return "TOOLS"
    if head.startswith("ev0_"):
        return "STATE"
    if head == "ev0_cli":
        return "CLI"
    if head in ("gateway", "tui_gateway"):
        return "GATEWAY"
    if head == "cron":
        return "CRON"
    if head == "plugins":
        return "PLUGINS"
    if head in ("skills", "optional-skills"):
        return "SKILLS"
    if head in ("providers", "native"):
        return "PROVIDERS"
    if head == "apps":
        return "APPS"
    if head == "ui-tui":
        return "UITUI"
    if head == "web":
        return "WEB"
    if head == "website":
        return "WEBSITE"
    if head in ("docs", "HANDOFF.md", "SELF_IMPROVEMENT.md", "SUSTAINABILITY.md",
                "README.md", "CONTRIBUTING.md", "SECURITY.md", "LICENSE", "AGENTS.md",
                ".env.example"):
        return "DOCS"
    if head in ("tests", "tests-js", "evals"):
        return "TESTS"
    if head == "scripts":
        return "SCRIPTS"
    if head in ("docker", "nix", ".github", "mcp_serve.py",
                "registration_lifecycle.py", "mini_swe_runner.py", "setup.py",
                "pyproject.toml", "uv.lock", "flake.nix", "flake.lock",
                "package.json", "package-lock.json", "Dockerfile", "setup-3v0.sh",
                "3v0-cli", "constraints-termux.txt", ".bytecode-fingerprint"):
        return "INFRA"
    if head in ("run_agent.py", "cli.py", "batch_runner.py",
                "trajectory_compressor.py", "utils.py", "ev0_bootstrap.py"):
        return "ROOT"
    return "MISC"


def load_tsv(path: Path) -> dict[str, dict]:
    rows = {}
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        cells = line.split("\t")
        if len(cells) == len(FIELDS) and cells != FIELDS:
            rows[cells[0]] = dict(zip(FIELDS, cells))
    return rows


def load_manifest() -> dict[str, dict]:
    return load_tsv(MANIFEST)


def save_manifest(rows: dict[str, dict]):
    WIKI.mkdir(parents=True, exist_ok=True)
    lines = ["\t".join(FIELDS)]
    for path in sorted(rows):
        rec = rows[path]
        lines.append("\t".join(rec[f] for f in FIELDS))
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")


def rebuild():
    files = tracked_files(ROOT)
    old = load_manifest()
    curated = {p: r for p, r in load_tsv(CURATED).items() if p in files}
    rows = {}
    for path in files:
        if path in curated:
            rec = dict(curated[path])
            rec["curated"] = "manual"
        elif path in old and ("curated" in old[path] and old[path]["curated"] == "manual"):
            rec = dict(old[path])  # previously curated (not in overlay anymore? keep)
        elif path in old:
            rec = dict(old[path])
        else:
            kind, purpose, why = classify(path)
            rec = {"path": path, "kind": kind, "curated": "auto",
                   "purpose": purpose, "why": why, "related": relations(path, set(files))}
        for f in FIELDS:
            rec.setdefault(f, "")
        rows[path] = rec
    save_manifest(rows)
    render_areas(rows)
    print(f"wiki: manifest {len(rows)} rows (manual={len(curated)}), areas rendered")


def deficiencies(rows: dict[str, dict]) -> tuple[int, int, int]:
    files = set(tracked_files(ROOT))
    missing = len(files - set(rows))
    empty = overlength = 0
    for path, rec in rows.items():
        if path not in files:
            continue
        if not rec.get("purpose", "").strip() or not rec.get("why", "").strip() \
                or not rec.get("related", "").strip():
            empty += 1
        for f in ("purpose", "why", "related"):
            if len(rec.get(f, "")) > MAXLEN[f]:
                overlength += 1
    return missing, empty, overlength


PAGE_ROW_LIMIT = 300


def render_table(recs: list[dict]) -> list[str]:
    lines = ["| path | kind | purpose | why | related |",
             "|------|------|---------|-----|---------|"]
    for r in recs:
        cells = [f"`{r['path']}`".replace("|", "\\|"), r.get("kind", ""),
                 (r.get("purpose") or "").replace("|", "\\|"),
                 (r.get("why") or "").replace("|", "\\|"),
                 (r.get("related") or "").replace("|", "\\|")]
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def group_key(path: str) -> str:
    parts = path.split("/")
    if len(parts) == 1:
        return "(root)"
    if len(parts) == 2:
        return parts[0] + "/"  # loose files at the area root bucket together
    return parts[0] + "/" + parts[1]


def render_areas(rows: dict[str, dict]):
    AREAS_DIR.mkdir(parents=True, exist_ok=True)
    by_area: dict[str, list] = {}
    for path, rec in rows.items():
        by_area.setdefault(area_of(path), []).append(rec)
    for area in AREA_ORDER:
        recs = sorted(by_area.get(area, []), key=lambda r: r["path"])
        intro = AREAS_DIR / f"_intro_{area}.md"
        head = intro.read_text(encoding="utf-8") if intro.exists() else ""
        lines = [f"# {AREA_TITLE.get(area, area)}", ""]
        if head:
            lines.append(head.rstrip())
            lines.append("---")
        if len(recs) <= PAGE_ROW_LIMIT:
            lines.append("Auto-rendered from `wiki/manifest.tsv` — "
                         "`python3 scripts/build_wiki.py --rebuild` regenerates.")
            lines.append("Columns: path · kind · purpose · why · related")
            lines.append("")
            lines.extend(render_table(recs))
            (AREAS_DIR / f"{area}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
            continue
        # Large area: split into per-directory sub-pages so a budget-constrained
        # model can read any page in one pass. The area page becomes a map.
        groups: dict[str, list[dict]] = {}
        for r in recs:
            groups.setdefault(group_key(r["path"]), []).append(r)
        lines.append("This area is large — split into per-directory pages so a "
                     "budget-constrained model can read each in one pass.")
        lines.append("Auto-rendered overview; sub-pages are regenerated by `--rebuild`.")
        lines.append("")
        lines.append("| group | files | page |")
        lines.append("|-------|-------|------|")
        for g in sorted(groups):
            g_recs = sorted(groups[g], key=lambda r: r["path"])
            safe = g.replace("/", ".").replace(" ", "_") or "root"
            lines.append(f"| `{g}/` | {len(g_recs)} | [`{area}.{safe}.md`]({area}.{safe}.md) |")
            sub = render_table(g_recs)
            sname = AREAS_DIR / f"{area}.{safe}.md"
            shead = f"# {AREA_TITLE.get(area, area)} — `{g}/`\n\n"
            sbody = "\n".join(["Auto-rendered from `wiki/manifest.tsv`.",
                                "Columns: path · kind · purpose · why · related", ""] + sub)
            sname.write_text(shead + sbody + "\n", encoding="utf-8")
        (AREAS_DIR / f"{area}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def report() -> dict:
    rows = load_manifest()
    files = tracked_files(ROOT)
    missing, empty, overlength = deficiencies(rows)
    by_area: dict[str, int] = {}
    kinds: dict[str, int] = {}
    for path, rec in rows.items():
        by_area[area_of(path)] = by_area.get(area_of(path), 0) + 1
        kinds[rec.get("kind", "")] = kinds.get(rec.get("kind", ""), 0) + 1
    manual = sum(1 for r in rows.values() if r.get("curated") == "manual")
    return {"tracked": len(files), "rows": len(rows),
            "missing": missing, "empty": empty, "overlength": overlength,
            "manual_rows": manual, "auto_rows": len(rows) - manual,
            "coverage_pct": round(100 * (len(files) - missing) / max(1, len(files)), 2),
            "areas": by_area, "kinds": kinds}


def main(argv: list[str]) -> int:
    mode = argv[0] if argv else "--report"
    if mode == "--rebuild":
        rebuild()
        return 0
    if mode == "--report":
        r = report()
        if "--json" in argv:
            print(json.dumps(r, indent=2))
        else:
            print(f"wiki coverage: {r['coverage_pct']}% "
                  f"({r['tracked'] - r['missing']}/{r['tracked']} tracked paths)")
            print(f"  rows={r['rows']} manual={r['manual_rows']} auto={r['auto_rows']} "
                  f"missing={r['missing']} empty={r['empty']} overlength={r['overlength']}")
            for area, n in sorted(r["areas"].items(), key=lambda kv: -kv[1]):
                print(f"  {area:9s} {n:5d}")
        return 0
    if mode == "--check":
        rows = load_manifest()
        missing, empty, overlength = deficiencies(rows)
        r = report()
        print(f"wiki check: coverage {r['coverage_pct']}% — "
              f"missing={missing} empty_fields={empty} overlength={overlength}")
        if missing:
            print("  TRACKED PATHS WITH NO INDEX ENTRY (run --rebuild to seed):")
            files = set(tracked_files(ROOT))
            for p in sorted(files - set(rows))[:15]:
                print(f"    {p}")
        if empty:
            print("  ROWS WITH EMPTY PURPOSE/WHY/RELATED:")
            files = set(tracked_files(ROOT))
            for path, rec in sorted(rows.items()):
                if path not in files:
                    continue
                if not rec.get("purpose", "").strip() or not rec.get("why", "").strip() \
                        or not rec.get("related", "").strip():
                    print(f"    {path}")
        if missing or empty or overlength:
            return 1
        print("  PASS — every tracked path has a complete index entry.")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))