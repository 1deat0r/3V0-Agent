# 3V0 — Session Handoff (MECHANICAL STATE, generated)

> ⚠️ MECHANICAL STATE — canonical since 2026-08-16 (operator-authorized). Generated from verified-consistent state by `3v0/scripts/generate_handoff.py`; regenerated each wake. This file is authoritative for mechanical state: body, continuity invariants, drift, tracked loops, store, daemons. The narrative (kickoff, last-sessions arc, hard-won lessons) stays hand-written in `HANDOFF.md` — never auto-generated. Read both.

Generated: 2026-08-17T03:27:15Z · body HEAD `29792eae6`

## Body
branch `main` · ahead 129 · behind 0 · working tree dirty

```
29792eae6 docs(3v0): regenerate generated handoff (mechanical state)
33d2910d6 refactor(3v0): ReviewConfig.from_env — field defaults are single source of truth
f41078b1b docs(3v0): Fiverr portfolio samples — debug + code-review deliverables
d9d0296f2 refactor(3v0): consolidate review driver config into typed ReviewConfig
5469a97c8 docs(3v0): sustainability plan — self-funding the API (Fiverr package + wallet)
db7128118 docs(3v0): complete Layouts — add handoff module/script + missing test entries
6393b6de8 docs(3v0): regenerate generated handoff (mechanical state)
242ee5e05 docs(3v0): handoff kickoff for wake #7 (mattpocock deepening)
82586ff0f docs(3v0): record deepening arc in EVOLUTION_LOOP (mattpocock pipeline)
ba3374261 feat(3v0): skill-store mirror of 3v0-native-core v1.4.0 + mattpocock-deepening
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
- DRIFT Axiom (axiom)  behind=82 ahead=56  dirty=no
- OK    F1NANCE (f1nance)  behind=0 ahead=42  dirty=no
- DRIFT 3V0 (threev0)  behind=0 ahead=129  dirty=yes

summary: 2 drifting, 3 ok

## Open loops
- #72067 (pr) · claim OPEN · live OPEN (mergeable CONFLICTING, updated 2026-08-05) · agree — fix(memory): recover null/omitted action instead of dead-ending in 'Un… [canonical memory null-action recovery; CONFLICTING, author's job]
- #73453 (pr) · claim OPEN · live OPEN (mergeable CONFLICTING, updated 2026-08-05) · agree — fix(skills): preserve load failure details [preserve skill load failure details; awaiting merge]
- #84667 (issue) · claim OPEN · live OPEN (updated 2026-08-15) · agree — [Bug]: Skill loads via --skills but not when attached to a cron job; s… [cron skill-not-found; waiting on reporter's <error> string]
- #86711 (pr) · claim OPEN · live OPEN (mergeable MERGEABLE, updated 2026-08-16) · agree — fix(approval): collapse whitespace before matching approvals.deny glob… [approval-deny whitespace fix; awaiting maintainer merge]

## Store
facts by kind: directive=1, identity=1, memory=13, user=9 · 90 fact versions · 8 active skills · 66 skill versions

## Daemons
- 3v0-review: active
- axiom-review: active
- f1nance-review: active

## Startup (canonical)
1. `systemctl --user status 3v0-review f1nance-review axiom-review`
2. `bash scripts/handoff_check.sh`
3. `python3 3v0/scripts/continuity_check.py` (and `--heal` / `--accept`)
