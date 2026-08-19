"""Coherence engine — detect + auto-resolve contradictions as they appear.

Standing answer to "fix contradictions the moment they appear / make staleness
impossible": a small registry of constitutional invariants (canonical vs
derived), run on every wake/commit. Mechanical drift is auto-resolved against
the canonical side; policy or substrate divergence FAILS CLOSE (reported, never
silently edited). Rules for what the engine may auto-edit and what it must not:
- AUTO-RESOLVE: derived documentation missing a canonical artifact (README
  must list every core module), mechanical store reconciliation.
- FAIL-CLOSE: substrate/config divergence, stale-doctrine reintroduction —
  these are deliberate acts, surfaced not overwritten.
This is the pre-commit guard's and the wake audit's shared check.
"""
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# The single-source list of known-stale doctrine phrases (kept in sync with
# consistency.sh). If any of these appears in a tracked doc, coherence reports
# it as an unresolved (fail-closed) conflict — reintroduction is impossible to
# merge through the guard.
STALE_PHRASES = (
    "DeepSeek-v4-pro via the DeepSeek API only",
    "never another provider",
    "locks the model to DeepSeek-v4-pro",
    "locks the reasoning engine to DeepSeek-v4-pro",
    "approval stays on .pro.",
    "the model to DeepSeek-v4-pro",
    "Prime Directive (immutable): DeepSeek-v4-pro",
)
_DOC_EXT = ("*.md", "*.yaml", "*.yml", "*.sh")


@dataclass
class Conflict:
    name: str
    kind: str        # "auto_resolve" | "fail_close"
    detail: str
    resolved: bool = False
    action: str = ""


@dataclass
class Report:
    checked: int = 0
    conflicts: list[Conflict] = field(default_factory=list)

    @property
    def auto_resolved(self): return [c for c in self.conflicts if c.resolved]
    @property
    def open(self): return [c for c in self.conflicts if not c.resolved]


def _tracked_docs() -> list[Path]:
    """Tracked *.md/*.yaml/*.yml/*.sh under the body (exclude data/vendored)."""
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files", "--"] + list(_DOC_EXT),
        capture_output=True, text=True)
    paths = []
    for p in out.stdout.splitlines():
        if p.startswith(("3v0/data/", "node_modules/", ".venv/", "docs/adr/")):
            continue
        paths.append(REPO_ROOT / p)
    return paths


def check_stale_doctrine() -> list[Conflict]:
    """Any tracked doc carrying a known-stale phrase -> fail-close conflict."""
    out = []
    scanned = 0
    for f in _tracked_docs():
        if f.name == "consistency.sh":
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        scanned += 1
        for ph in STALE_PHRASES:
            m = re.search(re.escape(ph), text)
            if m:
                line = text[:m.start()].count("\n") + 1
                out.append(Conflict(
                    "no_stale_doctrine", "fail_close",
                    f"stale phrase in {f.relative_to(REPO_ROOT)}:{line}: {ph!r}"))
    return out


def check_core_modules_documented() -> list[Conflict]:
    """Every core/*.py module must appear in 3v0/README.md layout."""
    core = REPO_ROOT / "3v0" / "core"
    readme = (REPO_ROOT / "3v0" / "README.md").read_text(encoding="utf-8")
    missing = []
    for m in sorted(core.glob("*.py")):
        if m.name == "__init__.py" or m.name.startswith("_"):
            continue
        if f"`core/{m.name}`".lstrip("`") not in readme and m.name not in readme:
            missing.append(m.name)
    if not missing:
        return []
    return [Conflict("core_modules_documented", "auto_resolve",
                     f"README layout missing core modules: {missing}")]


def check_model_ids_consistent() -> list[Conflict]:
    """insights substrate constants must be self-consistent and match config."""
    try:
        from . import insights
    except ImportError:  # run as a script (python 3v0/core/coherence.py)
        import sys as _s
        _s.path.insert(0, str(REPO_ROOT / "3v0"))
        from core import insights  # noqa: F401
    out = []
    if insights.AUX_MODEL not in insights.INTENDED_MODELS:
        out.append(Conflict("model_ids_consistent", "fail_close",
                            f"AUX_MODEL {insights.AUX_MODEL!r} not in INTENDED_MODELS"))
    if insights.PRIMARY_MODEL not in insights.INTENDED_MODELS:
        out.append(Conflict("model_ids_consistent", "fail_close",
                            f"PRIMARY_MODEL {insights.PRIMARY_MODEL!r} not in INTENDED_MODELS"))
    return out


def _resolve(conf: Conflict) -> Conflict:
    """Apply the resolution policy for auto-resolvable conflicts."""
    if conf.name == "core_modules_documented" and conf.kind == "auto_resolve":
        m = re.findall(r"missing core modules: (\[[^\]]+\])", conf.detail)
        if not m:
            return conf
        import ast as _ast
        try:
            missing = _ast.literal_eval(m[0])
        except Exception:
            return conf
        readme = REPO_ROOT / "3v0" / "README.md"
        text = readme.read_text(encoding="utf-8")
        anchor = "- `core/retrieval.py`"
        if anchor not in text:
            return conf
        insert_at = text.index(anchor)
        block = "\n".join(
            f"- `core/{name}` — (coherence auto-docs)"
            "  [read the module docstring for the canonical description]."
            for name in missing) + "\n"
        text = text[:insert_at] + block + text[insert_at:]
        readme.write_text(text, encoding="utf-8")
        conf.resolved = True
        conf.action = f"appended {', '.join(missing)} to 3v0/README.md layout"
    return conf


def run(apply: bool = True) -> Report:
    """Run all constitutional checks; auto-resolve the mechanical ones."""
    checks = [
        check_core_modules_documented(),
        check_model_ids_consistent(),
        check_stale_doctrine(),
    ]
    rep = Report(checked=sum(bool(c) or 1 for c in checks))
    for c in checks:
        rep.conflicts.extend(c)
    if apply:
        for c in rep.conflicts:
            if c.kind == "auto_resolve" and not c.resolved:
                _resolve(c)
    return rep


if __name__ == "__main__":
    import sys as _sys
    apply = "--check" not in _sys.argv  # --check: detect + report, never mutate
    r = run(apply=apply)
    for c in r.conflicts:
        status = "RESOLVED" if c.resolved else "OPEN  "
        print(f"[{status}] {c.kind:12} {c.name}: {c.detail}"
              + (f" -> {c.action}" if c.action else ""))
    if r.open:
        print(f"coherence: {len(r.conflicts)} conflict(s), "
              f"{len(r.open)} unresolved (fail-closed)")
        raise SystemExit(1)
    print(f"coherence: OK — {r.checked} constraints, "
          f"{len(r.auto_resolved)} auto-resolved")