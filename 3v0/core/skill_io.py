"""Shared skill-file I/O for the 3v0 skill axis.

Locating, writing, and removing SKILL.md files in the Hermes profile's skills
directory. The profile directory is the *operational* system (Hermes loads
skills from it); the native skill store is the canonical record. These helpers
are the single place that knows how to map a skill name -> SKILL.md path and
content, shared by ``seed_skills.py`` (baseline), ``ingest_skills.py``
(patch-content capture) and ``sync_skills.py`` (reconciliation).

Skills are located by *directory name*, not by a stored category — a skill that
was moved between categories is still found (mirrors the seed's posture and the
resolver's: the category subdirectory is organizational, the name is identity).
"""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path

# Fallback when neither THREEV0_SKILLS_DIR nor HERMES_HOME resolves (the 3v0
# profile's skills dir). The runtime subprocess inherits HERMES_HOME, so this is
# only a last resort for direct CLI use outside a profile.
DEFAULT_PROFILE = Path.home() / ".hermes" / "profiles" / "3v0" / "skills"


def profile_skills_dir() -> Path:
    """The active profile's skills directory.

    Honors ``THREEV0_SKILLS_DIR`` (tests / explicit override) first, then
    ``HERMES_HOME/skills`` (the runtime's profile), then the 3v0 profile
    default.
    """
    env = os.environ.get("THREEV0_SKILLS_DIR")
    if env:
        return Path(env).expanduser()
    hermes_home = os.environ.get("HERMES_HOME")
    if hermes_home:
        return Path(hermes_home).expanduser() / "skills"
    return DEFAULT_PROFILE


@dataclass
class SkillFile:
    name: str
    content: str
    category: str   # "" when the skill lives at the skills root
    path: Path


def skill_index(skills_dir: Path) -> dict[str, SkillFile]:
    """Map every *live* skill name under ``skills_dir`` to its SKILL.md.

    One walk of the tree; on a name collision the first match wins (the
    resolver treats ambiguous names as an error, so this is a rare guard, not a
    resolution strategy). Skills under ``.archive/`` are excluded — archived
    skills are not live in the profile and their content is already frozen in
    the store.
    """
    index: dict[str, SkillFile] = {}
    for md in skills_dir.rglob("SKILL.md"):
        dir_rel = md.parent.relative_to(skills_dir)
        if any(part == ".archive" for part in dir_rel.parts):
            continue
        name = md.parent.name
        if name in index:
            continue
        category = "" if dir_rel.parent == Path(".") else str(dir_rel.parent)
        try:
            index[name] = SkillFile(name, md.read_text(encoding="utf-8"), category, md)
        except OSError:
            continue
    return index


def find_skill_md(skills_dir: Path, name: str) -> SkillFile | None:
    """Locate ``name``'s SKILL.md anywhere under ``skills_dir``, or None."""
    return skill_index(skills_dir).get(name)


def write_skill_md(skills_dir: Path, name: str, content: str, category: str = "") -> Path:
    """Write ``name``'s SKILL.md into ``skills_dir`` (under ``category`` when
    given). Creates parent directories. Returns the written path."""
    target = skills_dir / category / name if category else skills_dir / name
    target.mkdir(parents=True, exist_ok=True)
    path = target / "SKILL.md"
    path.write_text(content, encoding="utf-8")
    return path


def remove_skill(skills_dir: Path, name: str) -> bool:
    """Remove ``name``'s skill directory (SKILL.md + supporting files).

    Removes only the leaf directory (``<category>/<name>``), never the category
    parent, and only when the skill is actually present. Returns True when a
    directory was removed.
    """
    found = find_skill_md(skills_dir, name)
    if found is None:
        return False
    leaf = found.path.parent
    shutil.rmtree(leaf)
    return True
