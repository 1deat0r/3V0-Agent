"""Project registry for the review driver — which projects share the 3v0
profile's state.db, where their stores live, and how to scope sessions to them.

The ``3v0`` profile hosts three projects (3V0, F1NANCE, Axiom) in one
``state.db``. Each has its own canonical memory store under ``3v0/data/``.
3V0 is the *primary* project: it reviews memory AND skills, projects facts
into the 3v0 profile (MEMORY.md/USER.md), fails open on an empty/unknown cwd,
and treats ``$HOME`` as its own. Sibling projects (F1NANCE, Axiom) are
reviewed by their own ``--project`` pass and are:

- **store-only** — no Hermes profile projection. Their stores are 3V0's
  *sidecar record* of sibling facts; the sibling's own profile memory (e.g.
  ``~/.hermes/profiles/f1nance/memories/``) is the sibling's namespace and
  must never be clobbered by a projecting ``record.py``/``sync.py``.
- **memory-only** — no skill axis. Siblings manage their own skills (or have
  none under 3V0's store); 3V0 does not decommission sibling skills.
- **strict** — no fail-open. Only sessions whose cwd is the sibling's repo
  (or a subdir) belong to that sibling; an empty/unknown cwd is skipped, not
  folded in.

Resolution is a pure function of (name, body_root, profile_home, home) so it
is unit-testable without touching the live profile; the driver passes its own
resolved ``REPO_ROOT``/``PROFILE_HOME`` and honors ``THREEV0_PROJECT_CWD`` as
a test/migration override for the sibling repo root.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

_PROJECT_NAMES = ("threev0", "f1nance", "axiom")

# Display names for the review charter.
_TITLES = {
    "threev0": "3V0",
    "f1nance": "F1NANCE",
    "axiom": "Axiom",
}

# Sibling repo roots, relative to the operator's home. 3V0's root is the body
# repo itself (passed in) — 3V0 is the primary project.
_SIBLING_CWD = {
    "f1nance": ("Projects", "AI Agents", "F1NANCE Agent"),
    "axiom": ("Projects", "axiom-agent"),
}


@dataclass(frozen=True)
class ProjectSpec:
    name: str
    title: str
    store: Path                       # canonical memory store
    cwd_roots: Tuple[Path, ...]       # repo roots: admit root + subdirs
    primary: bool                     # fail-open empty cwd + admit $HOME exact
    skill_store: Optional[Path]       # None -> memory-only (no skill axis)
    profile_mem: Optional[Path]       # None -> store-only (no projection)
    review_log: Path

    @property
    def memory_only(self) -> bool:
        return self.skill_store is None

    @property
    def store_only(self) -> bool:
        return self.profile_mem is None


def resolve_project(
    name: Optional[str],
    body_root: Path,
    profile_home: Path,
    home: Optional[Path] = None,
    cwd_override: Optional[str] = None,
) -> ProjectSpec:
    """Resolve a project name to its spec. ``cwd_override`` (the driver's
    ``THREEV0_PROJECT_CWD``) redirects the repo root for tests/migration; it
    never changes ``primary``-ness. Unknown names raise ``ValueError``."""
    home = Path(home) if home else Path.home()
    name = (name or "threev0").strip()
    if name not in _PROJECT_NAMES:
        raise ValueError(
            f"unknown project: {name!r} (expected one of {_PROJECT_NAMES})"
        )

    if cwd_override:
        roots: Tuple[Path, ...] = (Path(cwd_override),)
    elif name == "threev0":
        roots = (Path(body_root),)
    else:
        roots = (home.joinpath(*_SIBLING_CWD[name]),)

    data_dir = Path(body_root) / "3v0" / "data"
    if name == "threev0":
        return ProjectSpec(
            name=name,
            title=_TITLES[name],
            store=data_dir / "memory.json",
            cwd_roots=roots,
            primary=True,
            skill_store=data_dir / "skills.json",
            profile_mem=Path(profile_home) / "memories",
            review_log=Path(profile_home) / "3v0_reviews" / "reviews.jsonl",
        )
    return ProjectSpec(
        name=name,
        title=_TITLES[name],
        store=data_dir / name / "memory.json",
        cwd_roots=roots,
        primary=False,
        skill_store=None,
        profile_mem=None,
        review_log=Path(profile_home) / "3v0_reviews" / name / "reviews.jsonl",
    )
