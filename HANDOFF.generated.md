# 3V0 — Session Handoff (MECHANICAL STATE, generated)

> ⚠️ MECHANICAL STATE — canonical since 2026-08-16 (operator-authorized). Generated from verified-consistent state by `3v0/scripts/generate_handoff.py`; regenerated each wake. This file is authoritative for mechanical state: body, continuity invariants, drift, tracked loops, store, daemons. The narrative (kickoff, last-sessions arc, hard-won lessons) stays hand-written in `HANDOFF.md` — never auto-generated. Read both.

Generated: 2026-08-17T21:51:25Z · body HEAD `14e2fc11b`

## Body
branch `main` · ahead 163 · behind 0 · working tree dirty

```
14e2fc11b feat(3v0): Stone 23 — rewire memory pipeline to SQLite store + retrieval-chosen injection
8a4a500ad refactor(3v0): retrieval seam — extract rank/render into core/retrieval.py with budget-shaped inject
485021b0a docs(3v0): ADR-0004 retrieval-chosen injection + retrieval glossary terms
02229bbc4 refactor(3v0): deepen analytics — shared usage accumulator + collection split
d36c908a9 docs(3v0): add self-analytics terms to domain glossary (finding, cache-hit ratio, aux routing, report)
91463cc69 docs(3v0): fix aux-routing false claim + pin compression/approval models
94651433c fix(3v0): measure policy levers, not token totals (Stone 22)
ccd7394ab feat(3v0): Stone 21 memory rework foundation — SQLite temporal-fact store (triples, validity, sub-memory domains, retrieval feedback)
7e3fdadd8 feat(3v0): Stone 20 self-insights — ranked evidence-backed findings over the analytics report
cd61b85a1 feat(3v0): Stone 19 self-analytics — owned metrics from state.db (tool latency/success, cost/tokens, burn)
```

## Continuity
- OK    anchor           anchor present and well-formed
- OK    self-describing  anchor references the continuity model; model reachable
- OK    memory-profile   memory store <-> profile consistent
- OK    skills-store     skill store <-> SKILL.md consistent
- OK    ledger           project ledger parseable (3 projects)
- OK    github-loops     claims agree with live GitHub (4 loops)

summary: 0 drifting, 6 ok

## Drift (project ledger)
- OK    Axiom (axiom)  behind=0 ahead=63  dirty=no  [head moved]
- OK    F1NANCE (f1nance)  behind=0 ahead=42  dirty=no
- DRIFT 3V0 (threev0)  behind=0 ahead=163  dirty=yes  [head moved]

summary: 1 drifting, 3 ok

## Open loops
- #72067 (pr) · claim OPEN · live OPEN (mergeable CONFLICTING, updated 2026-08-05) · agree — fix(memory): recover null/omitted action instead of dead-ending in 'Un… [canonical memory null-action recovery; CONFLICTING, author's job]
- #73453 (pr) · claim OPEN · live OPEN (mergeable CONFLICTING, updated 2026-08-05) · agree — fix(skills): preserve load failure details [preserve skill load failure details; awaiting merge]
- #84667 (issue) · claim OPEN · live OPEN (updated 2026-08-15) · agree — [Bug]: Skill loads via --skills but not when attached to a cron job; s… [cron skill-not-found; waiting on reporter's <error> string]
- #86711 (pr) · claim OPEN · live OPEN (mergeable MERGEABLE, updated 2026-08-16) · agree — fix(approval): collapse whitespace before matching approvals.deny glob… [approval-deny whitespace fix; awaiting maintainer merge]

## Store
facts by kind: directive=1, identity=1, memory=15, user=10 · 117 fact versions · 9 active skills · 86 skill versions

## Daemons
- 3v0-review: active
- axiom-review: active
- f1nance-review: active

## Startup (canonical)
1. `systemctl --user status 3v0-review f1nance-review axiom-review`
2. `bash scripts/handoff_check.sh`
3. `python3 3v0/scripts/continuity_check.py` (and `--heal` / `--accept`)
