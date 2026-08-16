# 3V0 — Session Handoff (MECHANICAL STATE, generated)

> ⚠️ MECHANICAL STATE — canonical since 2026-08-16 (operator-authorized). Generated from verified-consistent state by `3v0/scripts/generate_handoff.py`; regenerated each wake. This file is authoritative for mechanical state: body, continuity invariants, drift, tracked loops, store, daemons. The narrative (kickoff, last-sessions arc, hard-won lessons) stays hand-written in `HANDOFF.md` — never auto-generated. Read both.

Generated: 2026-08-16T07:04:35Z · body HEAD `b48357d60`

## Body
branch `main` · ahead 101 · behind 0 · working tree dirty

```
b48357d60 docs(3v0): handoff kickoff — wake #5 (DeepSeek Harness watch resolved) + arc bullet
db34b2a0e ledger(3v0): re-anchor position baseline + regenerate generated handoff (post-harvest)
18d198c9e docs(3v0): resolve DeepSeek Harness watch item — released 2026-08-13 (MIT, dsh)
e2af26ee1 docs(3v0): regenerate generated handoff at wake-#4 HEAD
0fc19db12 docs(3v0): handoff kickoff — wake #4 reconciliation + arc bullet
af7513e42 ledger(3v0): re-anchor position baseline + regenerate generated handoff
cace12e9e docs(3v0): reconcile loop-claim OPEN assertions in handoff narrative
6e9b060a9 ledger(3v0): record post-flip position baseline + regenerate generated handoff
7dd4b4337 feat(3v0): operator-authorized flip — generated handoff is canonical mechanical state
5b3643eb2 docs(3v0): fix test count (18→19) + regenerate generated handoff
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
- DRIFT 3V0 (threev0)  behind=0 ahead=101  dirty=yes

summary: 1 drifting, 3 ok

## Open loops
- #72067 (pr) · claim OPEN · live OPEN (mergeable CONFLICTING, updated 2026-08-05) · agree — fix(memory): recover null/omitted action instead of dead-ending in 'Un… [canonical memory null-action recovery; CONFLICTING, author's job]
- #73453 (pr) · claim OPEN · live OPEN (mergeable MERGEABLE, updated 2026-08-05) · agree — fix(skills): preserve load failure details [preserve skill load failure details; awaiting merge]
- #84667 (issue) · claim OPEN · live OPEN (updated 2026-08-15) · agree — [Bug]: Skill loads via --skills but not when attached to a cron job; s… [cron skill-not-found; waiting on reporter's <error> string]
- #86711 (pr) · claim OPEN · live OPEN (mergeable MERGEABLE, updated 2026-08-15) · agree — fix(approval): collapse whitespace before matching approvals.deny glob… [approval-deny whitespace fix; awaiting maintainer merge]

## Store
facts by kind: directive=1, identity=1, memory=13, user=8 · 76 fact versions · 7 active skills · 57 skill versions

## Daemons
- 3v0-review: active
- axiom-review: active
- f1nance-review: active

## Startup (canonical)
1. `systemctl --user status 3v0-review f1nance-review axiom-review`
2. `bash scripts/handoff_check.sh`
3. `python3 3v0/scripts/continuity_check.py` (and `--heal` / `--accept`)
