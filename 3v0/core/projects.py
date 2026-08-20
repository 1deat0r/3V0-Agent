"""Project registry and drift ledger — the data-driven answer to "where does
each project stand", plus the review-driver scoping derived from it.

Stone 16 generalizes Stone 15's hardcoded three-project tuple into a
data-driven ``ProjectLedger`` (``3v0/data/projects/ledger.json``). A project is
an *entry*, not a code edit: ``scripts/project.py add`` onboards any git repo
(repo + upstream + delta + optional profile/store), and
``scripts/drift_check.py`` reports divergence generically. The three known
projects (3V0, F1NANCE, Axiom) are seed entries in that file — the schema is
fixed, the data is not.

Two views over the same ledger:

- ``ProjectLedger`` — the *position* view (drift check): name → repo,
  upstream, delta, HEAD / upstream-merge-point, store head, open loops,
  last-seen. ``project.py`` and ``drift_check.py`` operate on it.
- ``ProjectSpec`` — the *review-scoping* view (Stone 15): ``resolve_project``
  derives it from a ledger entry (store, cwd roots, primary / memory-only /
  store-only, review log) for the session-review driver.

The seed defaults below are the bootstrap used only when the ledger file is
missing (a fresh checkout, or a test that never wrote one); the ledger is
authoritative once it exists.

Path conventions in the ledger file (portable across machines/users):

- ``repo``: ``"."`` = the body repo containing the ledger; ``"~/..."`` =
  relative to the operator's home; otherwise an absolute path.
- ``store`` / ``skill_store``: body-relative (under ``3v0/data/``) or
  absolute; ``null`` = absent (drift-tracking only / memory-only).

Position fields (``head`` / ``upstream_head`` / ``store_head`` /
``last_seen_at``) are snapshots written by ``drift_check.py --update`` (or
``project.py status --update``) and committed; the drift clock itself is
report-only so it never dirties the body repo's working tree.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

LEDGER_VERSION = 1


# ---------------------------------------------------------------------------
# Seed data (Stone 15's hardcoded trio — bootstrap only)
# ---------------------------------------------------------------------------

_SEED_NAMES = ("threev0", "f1nance", "axiom")
_SEED_TITLES = {
    "threev0": "3V0",
    "f1nance": "F1NANCE",
    "axiom": "Axiom",
}
# Sibling repo roots, relative to the operator's home. 3V0's root is the body
# repo itself (resolved at seed time) — 3V0 is the primary project.
_SEED_SIBLING_CWD = {
    "f1nance": ("Projects", "AI Agents", "F1NANCE Agent"),
    "axiom": ("Projects", "axiom-agent"),
}


@dataclass(frozen=True)
class LedgerEntry:
    """One project's position in the ledger.

    ``repo`` / ``store`` / ``skill_store`` are *resolved absolute* paths by
    the time an entry exists (``load``/``seed`` resolve the portable forms in
    the JSON); ``save`` re-serializes them back to portable forms.
    """

    name: str
    title: str
    repo: Path
    upstream: str = "origin"          # git remote name to merge from
    upstream_ref: str = "main"        # branch on that remote
    delta: str = ""                   # the deliberate, named divergence
    track_upstream: bool = True       # False = deliberate hardfork (behind/ahead
                                      #   is informational, not drift)
    profile: Optional[str] = None     # the 3V0 profile the project runs under
    store: Optional[Path] = None      # canonical memory store (None -> not reviewed)
    skill_store: Optional[Path] = None  # None -> memory-only
    primary: bool = False             # fail-open cwd + project to the 3v0 profile
    head: Optional[str] = None        # last recorded HEAD
    upstream_head: Optional[str] = None
    store_head: Optional[str] = None  # sha256 of the store's on-disk bytes
    open_loops: Tuple[str, ...] = ()
    last_seen_at: Optional[str] = None

    @property
    def memory_only(self) -> bool:
        return self.skill_store is None

    @property
    def store_only(self) -> bool:
        return not self.primary


# ---------------------------------------------------------------------------
# Portable path (de)serialization
# ---------------------------------------------------------------------------

def _resolve_repo(raw: Optional[str], body_root: Path, home: Path) -> Path:
    """``"."`` → body root; ``"~/..."`` → home-relative; else as-is."""
    raw = (raw or ".").strip()
    if raw in (".", ""):
        return body_root
    if raw == "~":
        return home
    if raw.startswith("~/"):
        return home / raw[2:]
    return Path(raw).expanduser()


def _resolve_store(raw: Optional[str], body_root: Path) -> Optional[Path]:
    if not raw:
        return None
    p = Path(raw).expanduser()
    if not p.is_absolute():
        p = body_root / p
    return p


def _repo_to_rel(repo: Path, body_root: Path, home: Path) -> str:
    if repo == body_root:
        return "."
    try:
        return "~/" + str(repo.relative_to(home))
    except ValueError:
        return str(repo)


def _store_to_rel(p: Optional[Path], body_root: Path) -> Optional[str]:
    if p is None:
        return None
    try:
        return str(p.relative_to(body_root))
    except ValueError:
        return str(p)


# ---------------------------------------------------------------------------
# The ledger
# ---------------------------------------------------------------------------

class ProjectLedger:
    """Data-driven registry of projects, keyed by name."""

    def __init__(self, entries: Dict[str, LedgerEntry]):
        self._entries: Dict[str, LedgerEntry] = dict(entries)

    # -- read ---------------------------------------------------------------
    def __contains__(self, name: str) -> bool:
        return name in self._entries

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self):
        return iter(self._entries)

    def __getitem__(self, name: str) -> LedgerEntry:
        entry = self._entries.get(name)
        if entry is None:
            raise KeyError(name)
        return entry

    def get(self, name: str) -> Optional[LedgerEntry]:
        return self._entries.get(name)

    def names(self) -> List[str]:
        return sorted(self._entries)

    def entries(self) -> List[LedgerEntry]:
        return [self._entries[n] for n in self.names()]

    # -- write --------------------------------------------------------------
    def add(self, entry: LedgerEntry) -> None:
        self._entries[entry.name] = entry

    def remove(self, name: str) -> None:
        del self._entries[name]

    # -- (de)serialization --------------------------------------------------
    @classmethod
    def seed(cls, body_root: Path, home: Path) -> "ProjectLedger":
        """The Stone 15 trio as ledger entries (bootstrap when the file is
        missing). Only the review-relevant fields are populated; the committed
        ledger carries the richer drift metadata (deltas, upstreams)."""
        body_root = Path(body_root)
        home = Path(home)
        data_dir = body_root / "3v0" / "data"
        entries: Dict[str, LedgerEntry] = {}
        for name in _SEED_NAMES:
            primary = name == "threev0"
            if primary:
                repo = body_root
                store: Optional[Path] = data_dir / "memory.db"
                skill_store: Optional[Path] = data_dir / "skills.json"
                profile = "3v0"
            else:
                repo = home.joinpath(*_SEED_SIBLING_CWD[name])
                store = data_dir / name / "memory.json"
                skill_store = None
                profile = None
            entries[name] = LedgerEntry(
                name=name,
                title=_SEED_TITLES[name],
                repo=repo,
                upstream="origin",
                upstream_ref="main",
                profile=profile,
                store=store,
                skill_store=skill_store,
                primary=primary,
            )
        return cls(entries)

    @classmethod
    def load(
        cls,
        body_root: Path,
        home: Optional[Path] = None,
        path: Optional[Path] = None,
    ) -> "ProjectLedger":
        """Load the ledger from ``path`` (default: body's
        ``3v0/data/projects/ledger.json``), resolving portable paths. Raises
        ``OSError`` / ``ValueError`` on a missing or malformed file."""
        body_root = Path(body_root)
        home = Path(home) if home else Path.home()
        path = Path(path) if path else (body_root / "3v0" / "data" / "projects" / "ledger.json")
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("projects"), dict):
            raise ValueError(f"malformed ledger: {path}")
        entries: Dict[str, LedgerEntry] = {}
        for name, raw in data["projects"].items():
            entries[name] = LedgerEntry(
                name=name,
                title=raw.get("title") or name,
                repo=_resolve_repo(raw.get("repo"), body_root, home),
                upstream=raw.get("upstream") or "origin",
                upstream_ref=raw.get("upstream_ref") or "main",
                delta=raw.get("delta") or "",
                track_upstream=bool(raw.get("track_upstream", True)),
                profile=raw.get("profile"),
                store=_resolve_store(raw.get("store"), body_root),
                skill_store=_resolve_store(raw.get("skill_store"), body_root),
                primary=bool(raw.get("primary", False)),
                head=raw.get("head"),
                upstream_head=raw.get("upstream_head"),
                store_head=raw.get("store_head"),
                open_loops=tuple(raw.get("open_loops") or ()),
                last_seen_at=raw.get("last_seen_at"),
            )
        return cls(entries)

    def save(
        self,
        body_root: Path,
        home: Optional[Path] = None,
        path: Optional[Path] = None,
    ) -> None:
        """Write the ledger back in its portable form (sorted by name)."""
        body_root = Path(body_root)
        home = Path(home) if home else Path.home()
        path = Path(path) if path else (body_root / "3v0" / "data" / "projects" / "ledger.json")
        projects: Dict[str, dict] = {}
        for name in self.names():
            e = self._entries[name]
            projects[name] = {
                "title": e.title,
                "repo": _repo_to_rel(e.repo, body_root, home),
                "upstream": e.upstream,
                "upstream_ref": e.upstream_ref,
                "delta": e.delta,
                "track_upstream": e.track_upstream,
                "profile": e.profile,
                "store": _store_to_rel(e.store, body_root),
                "skill_store": _store_to_rel(e.skill_store, body_root),
                "primary": e.primary,
                "head": e.head,
                "upstream_head": e.upstream_head,
                "store_head": e.store_head,
                "open_loops": list(e.open_loops),
                "last_seen_at": e.last_seen_at,
            }
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"version": LEDGER_VERSION, "projects": projects}
        path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )


# ---------------------------------------------------------------------------
# Review-scoping view (Stone 15, unchanged shape)
# ---------------------------------------------------------------------------

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


def _load_or_seed(body_root: Path, home: Path) -> ProjectLedger:
    """Load the ledger, falling back to the seed trio when the file is missing
    or unreadable (fail-open: the review daemon must keep working)."""
    try:
        return ProjectLedger.load(body_root=body_root, home=home)
    except (OSError, ValueError):
        return ProjectLedger.seed(body_root, home)


def resolve_project(
    name: Optional[str],
    body_root: Path,
    profile_home: Path,
    home: Optional[Path] = None,
    cwd_override: Optional[str] = None,
    ledger: Optional[ProjectLedger] = None,
) -> ProjectSpec:
    """Resolve a project name to its review-scoping spec, now ledger-driven.

    ``cwd_override`` (the driver's ``THREEV0_PROJECT_CWD``) redirects the repo
    root for tests/migration; it never changes ``primary``-ness. Unknown names
    raise ``ValueError``; a ledger entry with no ``store`` is drift-tracking
    only and cannot be reviewed (also ``ValueError``). When ``ledger`` is
    omitted, the default ledger is loaded (seed fallback when missing)."""
    home = Path(home) if home else Path.home()
    body_root = Path(body_root)
    profile_home = Path(profile_home)
    name = (name or "threev0").strip()

    if ledger is None:
        ledger = _load_or_seed(body_root, home)
    entry = ledger.get(name)
    if entry is None:
        raise ValueError(
            f"unknown project: {name!r} (known: {', '.join(ledger.names())})"
        )
    if entry.store is None:
        raise ValueError(
            f"project {name!r} has no store — drift-tracking only, not reviewable"
        )

    if cwd_override:
        roots: Tuple[Path, ...] = (Path(cwd_override),)
    else:
        roots = (entry.repo,)

    review_log = (
        profile_home / "3v0_reviews" / "reviews.jsonl"
        if entry.primary
        else profile_home / "3v0_reviews" / name / "reviews.jsonl"
    )
    return ProjectSpec(
        name=entry.name,
        title=entry.title,
        store=entry.store,
        cwd_roots=roots,
        primary=entry.primary,
        skill_store=entry.skill_store,
        profile_mem=profile_home / "memories" if entry.primary else None,
        review_log=review_log,
    )
