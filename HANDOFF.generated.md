# 3V0 — Session Handoff (MECHANICAL STATE, generated)

> ⚠️ MECHANICAL STATE — canonical since 2026-08-16 (operator-authorized). Generated from verified-consistent state by `3v0/scripts/generate_handoff.py`; regenerated each wake. This file is authoritative for mechanical state: body, continuity invariants, drift, tracked loops, store, daemons. The narrative (kickoff, last-sessions arc, hard-won lessons) stays hand-written in `HANDOFF.md` — never auto-generated. Read both.

Generated: 2026-08-16T05:04:11Z · body HEAD `0fc19db12`

## Body
branch `main` · ahead 97 · behind 0 · working tree clean

```
0fc19db12 docs(3v0): handoff kickoff — wake #4 reconciliation + arc bullet
af7513e42 ledger(3v0): re-anchor position baseline + regenerate generated handoff
cace12e9e docs(3v0): reconcile loop-claim OPEN assertions in handoff narrative
6e9b060a9 ledger(3v0): record post-flip position baseline + regenerate generated handoff
7dd4b4337 feat(3v0): operator-authorized flip — generated handoff is canonical mechanical state
5b3643eb2 docs(3v0): fix test count (18→19) + regenerate generated handoff
505710039 docs(3v0): regenerate HANDOFF.generated.md at post-Stone-18 HEAD
84d4e4181 ledger(3v0): record post-Stone-18 position baseline (drift_check --update)
21684b941 memory(3v0): daemon captured grill-session facts (fault-injection acceptance + continuity-before-heal)
8603d265a feat(3v0): Stone 18 — shadow generated handoff (render + loop-claim diff + CLI)
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
- OK    Axiom (axiom)  behind=0 ahead=25  dirty=no
- OK    F1NANCE (f1nance)  behind=0 ahead=41  dirty=no
- OK    3V0 (threev0)  behind=0 ahead=97  dirty=no  [head moved]

summary: 0 drifting, 3 ok

## Open loops
- #72067 (pr) · claim OPEN · live OPEN (mergeable CONFLICTING, updated 2026-08-05) · agree — fix(memory): recover null/omitted action instead of dead-ending in 'Un… [canonical memory null-action recovery; CONFLICTING, author's job]
- #73453 (pr) · claim OPEN · live OPEN (mergeable MERGEABLE, updated 2026-08-05) · agree — fix(skills): preserve load failure details [preserve skill load failure details; awaiting merge]
- #84667 (issue) · claim OPEN · live OPEN (updated 2026-08-15) · agree — [Bug]: Skill loads via --skills but not when attached to a cron job; s… [cron skill-not-found; waiting on reporter's <error> string]
- #86711 (pr) · claim OPEN · live OPEN (mergeable MERGEABLE, updated 2026-08-15) · agree — fix(approval): collapse whitespace before matching approvals.deny glob… [approval-deny whitespace fix; awaiting maintainer merge]

## Store
facts by kind: directive=1, identity=1, memory=13, user=8 · 76 fact versions · 7 active skills · 56 skill versions

## Daemons
- 3v0-review: active
- axiom-review: active
- f1nance-review: active

## Startup (canonical)
1. `systemctl --user status 3v0-review f1nance-review axiom-review`
2. `bash scripts/handoff_check.sh`
3. `python3 3v0/scripts/continuity_check.py` (and `--heal` / `--accept`)
