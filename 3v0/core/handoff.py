"""Handoff generation — the pure render half (Stone 18).

Mirrors ``core/continuity.py`` and ``core/drift.py``: **no I/O here.** It takes
a flat, JSON-safe context dict of collected facts and renders the mechanical
``HANDOFF.generated.md`` draft. The collection half
(``scripts/generate_handoff.py``) gathers the facts; this module only
*renders* and *decides*.

The generated draft is **never canonical**. It carries the mechanical state a
fresh session must know and that drifts when hand-maintained: body git state,
continuity invariants, the project-ledger drift report, the open upstream
loops (from the claim registry + live GitHub), store counts, and daemon
health. The hand-written ``HANDOFF.md`` keeps the *narrative* — the kickoff
judgment, the last-sessions arc, the hard-won lessons — which is 3V0's own
account and must never be auto-generated (auto-rewriting one's own narrative
is the self-reinforcing-bias trap named as weakness #2).

The acceptance mechanism is the **shadow diff**: each wake the generated
draft is diffed against the hand-written one. The loop-claim diff
(``diff_loop_claims``) specifically measures how far the hand-written
narrative's loop-state assertions have drifted from live reality — the exact
failure the grill found in 2026-08-16 (three hand-synced loop lists that had
already diverged). The flip from hand-written to generated is the Operator's
call, never self-authorized; this module only produces the evidence.

Pure by construction: ``render_handoff`` and ``diff_loop_claims`` read the
context dict and a string, and return strings / lists — no filesystem, no
git, no network.
"""

from __future__ import annotations

import re
from typing import Dict, Iterable, List

# The gh ``state`` field's closed set (PRs and issues). These are the only
# words whose *presence in the hand-written narrative* can contradict live
# reality. Status words like MERGEABLE / CONFLICTING are NOT states — they are
# the ``mergeable`` field and are consistent with state=OPEN, so they are
# deliberately excluded from the contradiction set.
GH_STATES = ("OPEN", "CLOSED", "MERGED")

_STATE_RE = re.compile(r"\b(OPEN|CLOSED|MERGED)\b")

GENERATED_BANNER = (
    "> \u26a0\ufe0f MECHANICAL DRAFT \u2014 never canonical. Generated from "
    "verified-consistent state by `3v0/scripts/generate_handoff.py`. The "
    "hand-written `HANDOFF.md` is canonical. Diff this against `HANDOFF.md` "
    "each wake; the diff is the acceptance evidence for the generated-handoff "
    "flip, which is the Operator's call and never self-authorized."
)


# ---------------------------------------------------------------------------
# Loop-claim extraction + diff (the "shadow diff" decision half)
# ---------------------------------------------------------------------------

def _loop_occurrences(text: str, num: str) -> List[re.Match]:
    """Occurrences of a loop number not embedded in a longer number."""
    return list(re.finditer(rf"(?<!\d){re.escape(num)}(?!\d)", text))


def extract_loop_state_claims(
    text: str, loop_nums: Iterable[str], window: int = 200
) -> Dict[str, set]:
    """State words the narrative asserts near each loop number.

    For every canonical loop number, scan a ``window``-character span around
    each of its occurrences for ``GH_STATES`` words. Returns ``{num: set[str]}``
    — the set of states the narrative asserts (possibly empty: the number is
    mentioned but no state word is nearby). Conservative by design: it only
    ever *collects*; whether a collected word contradicts reality is
    ``diff_loop_claims``'s call.
    """
    out: Dict[str, set] = {}
    for num in loop_nums:
        words: set = set()
        for m in _loop_occurrences(text, str(num)):
            lo = max(0, m.start() - window)
            hi = min(len(text), m.end() + window)
            words.update(_STATE_RE.findall(text[lo:hi]))
        out[str(num)] = words
    return out


def _truth_of(loop: dict) -> str | None:
    """The state a loop should be compared against: live first, else claimed."""
    if loop.get("live_ok"):
        return loop.get("live_state")
    return loop.get("claimed_state")


def diff_loop_claims(loops: List[dict], handwritten_text: str, window: int = 200) -> List[dict]:
    """Compare each loop's asserted state (in the hand-written narrative)
    against its truth (live GitHub state, else the claim registry's claim).

    Returns one dict per loop: ``{num, truth, asserted, status}`` where status
    is one of:

    - ``drift``        the narrative asserts a state word that contradicts truth;
    - ``agree``        the narrative asserts the truthful state (and nothing else);
    - ``unmentioned``  the loop number appears but no state word is nearby;
    - ``unverifiable`` neither live nor claimed state is known.
    """
    nums = [str(loop.get("num") or "") for loop in loops]
    claims = extract_loop_state_claims(handwritten_text, nums, window=window)
    out: List[dict] = []
    for loop in loops:
        num = str(loop.get("num") or "")
        truth = _truth_of(loop)
        asserted = sorted(claims.get(num) or [])
        if truth is None:
            status = "unverifiable"
        elif not asserted:
            status = "unmentioned"
        elif set(asserted) == {truth}:
            status = "agree"
        else:
            status = "drift"
        out.append(
            {
                "num": num,
                "truth": truth,
                "asserted": asserted,
                "status": status,
            }
        )
    return out


# ---------------------------------------------------------------------------
# Rendering (the "generate the draft" half)
# ---------------------------------------------------------------------------

def _fmt_num(v, default: str = "?") -> str:
    return str(v) if v is not None else default


def _render_body(ctx: dict) -> str:
    git = ctx.get("git") or {}
    branch = git.get("branch") or "?"
    ahead = _fmt_num(git.get("ahead"))
    behind = _fmt_num(git.get("behind"))
    dirty = "dirty" if git.get("dirty") else "clean"
    lines = [f"branch `{branch}` \u00b7 ahead {ahead} \u00b7 behind {behind} \u00b7 working tree {dirty}"]
    recent = git.get("recent") or []
    if recent:
        lines.append("")
        lines.append("```")
        lines.extend(str(c) for c in recent[:10])
        lines.append("```")
    return "\n".join(lines)


def _render_continuity(ctx: dict) -> str:
    cont = ctx.get("continuity") or {}
    invariants = cont.get("invariants") or []
    if not invariants:
        return "(continuity report unavailable)"
    lines = []
    for r in invariants:
        verdict = "DRIFT" if r.get("drift") else "OK"
        lines.append(f"- {verdict:5} {r.get('name', '?'):16} {r.get('detail', '')}")
    drift = _fmt_num(cont.get("drift_count"))
    total = _fmt_num(cont.get("total"))
    lines.append("")
    lines.append(f"summary: {drift} drifting, {total} ok")
    return "\n".join(lines)


def _render_drift(ctx: dict) -> str:
    drift = ctx.get("drift") or {}
    projects = drift.get("projects") or []
    if drift.get("error"):
        return drift["error"]
    if not projects:
        return "(drift report unavailable)"
    lines = []
    for r in projects:
        verdict = "DRIFT" if r.get("drifting") else "OK"
        behind = _fmt_num(r.get("behind"))
        ahead = _fmt_num(r.get("ahead"))
        dirty = "yes" if r.get("dirty") else "no"
        line = (
            f"- {verdict:5} {r.get('title', '?')} ({r.get('name', '?')})  "
            f"behind={behind} ahead={ahead}  dirty={dirty}"
        )
        if r.get("head_moved"):
            line += "  [head moved]"
        lines.append(line)
    lines.append("")
    lines.append(
        f"summary: {_fmt_num(drift.get('drifting'))} drifting, "
        f"{_fmt_num(drift.get('total'))} ok"
    )
    return "\n".join(lines)


def _render_loops(ctx: dict) -> str:
    loops = ctx.get("loops") or []
    if not loops:
        return "(no tracked loops)"
    lines = []
    for loop in loops:
        num = loop.get("num") or "?"
        kind = loop.get("kind") or "?"
        claimed = loop.get("claimed_state") or "?"
        live = loop.get("live_state") or "?"
        if not loop.get("live_ok"):
            live = f"unverifiable ({loop.get('live_error', 'gh failed')})"
        agree = "agree" if loop.get("live_ok") and live == claimed else "claim\u2260live"
        extras = []
        if loop.get("live_ok"):
            if loop.get("mergeable"):
                extras.append(f"mergeable {loop['mergeable']}")
            if loop.get("updated_at"):
                extras.append(f"updated {loop['updated_at'][:10]}")
        title = loop.get("title") or ""
        title = title[:70] + ("\u2026" if len(title) > 70 else "")
        note = loop.get("note") or ""
        line = f"- #{num} ({kind}) \u00b7 claim {claimed} \u00b7 live {live}"
        if extras:
            line += " (" + ", ".join(extras) + ")"
        line += f" \u00b7 {agree}"
        if title:
            line += f" \u2014 {title}"
        if note:
            line += f" [{note}]"
        lines.append(line)
    return "\n".join(lines)


def _render_store(ctx: dict) -> str:
    store = ctx.get("store") or {}
    if store.get("error"):
        return store["error"]
    facts = store.get("facts") or {}
    if facts:
        by_kind = ", ".join(f"{k}={v}" for k, v in sorted(facts.items()))
    else:
        by_kind = "(empty)"
    fact_versions = _fmt_num(store.get("fact_versions"))
    active_skills = _fmt_num(store.get("active_skills"))
    skill_versions = _fmt_num(store.get("skill_versions"))
    return (
        f"facts by kind: {by_kind} \u00b7 {fact_versions} fact versions \u00b7 "
        f"{active_skills} active skills \u00b7 {skill_versions} skill versions"
    )


def _render_daemons(ctx: dict) -> str:
    daemons = ctx.get("daemons") or {}
    if not daemons:
        return "(daemon status unavailable)"
    return "\n".join(f"- {name}: {state}" for name, state in sorted(daemons.items()))


def render_handoff(ctx: dict) -> str:
    """Render the mechanical ``HANDOFF.generated.md`` draft from ``ctx``.

    Best-effort: every section tolerates missing keys (a partial context
    renders a partial draft, never raises). The sections are the mechanical
    mirror of the hand-written handoff's drift-prone parts.
    """
    parts: List[str] = []
    parts.append("# 3V0 \u2014 Session Handoff (GENERATED DRAFT)")
    parts.append("")
    parts.append(GENERATED_BANNER)
    parts.append("")
    generated = ctx.get("generated_at") or "unknown"
    head = ctx.get("git_head") or "?"
    parts.append(f"Generated: {generated} \u00b7 body HEAD `{head}`")
    parts.append("")
    parts.append("## Body")
    parts.append(_render_body(ctx))
    parts.append("")
    parts.append("## Continuity")
    parts.append(_render_continuity(ctx))
    parts.append("")
    parts.append("## Drift (project ledger)")
    parts.append(_render_drift(ctx))
    parts.append("")
    parts.append("## Open loops")
    parts.append(_render_loops(ctx))
    parts.append("")
    parts.append("## Store")
    parts.append(_render_store(ctx))
    parts.append("")
    parts.append("## Daemons")
    parts.append(_render_daemons(ctx))
    parts.append("")
    parts.append("## Startup (canonical)")
    parts.append(
        "\n".join(
            [
                "1. `systemctl --user status 3v0-review f1nance-review axiom-review`",
                "2. `bash scripts/handoff_check.sh`",
                "3. `python3 3v0/scripts/continuity_check.py` (and `--heal` / `--accept`)",
            ]
        )
    )
    parts.append("")
    return "\n".join(parts)
