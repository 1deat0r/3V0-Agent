"""Author a SKILL.md body from a SkillForge proposal (the model-facing half).

``core/skill_forge.synthesize_proposal`` emits a *proposal* (metadata +
public callables). This module turns that proposal into a well-formed SKILL.md
body — the durable, agentskills-style skill content a model (or a human) can
review, and which ``record_skills.py --action skill_update`` can write
store-first.

It is pure and deterministic: given a proposal, it emits a canonical body
structured as:

  ---
  name: <name>
  description: <description>
  ---
  # <name>
  <overview>
  ## When to use
  ...
  ## Method
  - <callable> — <docstring>
  ...
  ## References
  (source module path)

The body is a *scaffold the model completes* — it encodes the distilled method
from the module's public API, which is the SkillForge "create" payload. No
store write here; the driver writes it via ``record_skills.py`` (gated by
``safe_evolve``). Deterministic, no LLM, no I/O.
"""

from __future__ import annotations

from typing import Any, Dict, Optional


def _callable_line(name: str, doc: Optional[str]) -> str:
    d = (doc or "").strip().split("\n", 1)[0].strip()
    if d:
        return f"- {name} — {d}"
    return f"- {name}"


def build_skill_md(proposal: Dict[str, Any]) -> str:
    """A complete SKILL.md from a proposal dict (as ``synthesize_proposal``
    emits). Deterministic: the same proposal always yields the same body.

    Callable docstrings come from the proposal's ``callable_docs`` map (the
    AST-parse result); absent docs fall back to the bare name.
    """
    name = str(proposal.get("name") or "skill")
    description = str(proposal.get("description") or "")
    overview = str(proposal.get("overview") or "")
    callables = list(proposal.get("public_callables") or [])
    callable_docs = proposal.get("callable_docs") or {}
    source = str(proposal.get("source") or "3v0 core")

    # Strip the category from the name when it's a nested path (the store keys
    # by bare name; category is metadata).
    bare_name = name.split("/")[-1]

    lines: list[str] = []
    lines.append("---")
    lines.append(f"name: {bare_name}")
    # Escape embedded double quotes so the YAML description line stays valid.
    safe_desc = description.replace('"', '\\"')
    desc_line = f'description: "{safe_desc}"' if description else "description: ''"
    lines.append(desc_line)
    lines.append("---")
    lines.append("")
    lines.append(f"# {bare_name}")
    if overview:
        lines.append(overview)
    lines.append("")
    lines.append("## When to use")
    lines.append(
        "Use this skill when the task involves the method this module encodes "
        "— matching on the public callables below."
    )
    lines.append("")
    lines.append("## Method")
    if callables:
        docs = callable_docs if isinstance(callable_docs, dict) else {}
        for c in callables:
            lines.append(_callable_line(str(c), docs.get(c)))
    else:
        lines.append("(No public callables distilled — complete the method by hand.)")
    lines.append("")
    lines.append("## References")
    lines.append(f"Source: `{source}`")
    lines.append("")
    return "\n".join(lines)