# 3V0 — Session Handoff (MECHANICAL STATE, generated)

> ⚠️ MECHANICAL STATE — canonical since 2026-08-16 (operator-authorized). Generated from verified-consistent state by `3v0/scripts/generate_handoff.py`; regenerated each wake. This file is authoritative for mechanical state: body, continuity invariants, drift, tracked loops, store, daemons. The narrative (kickoff, last-sessions arc, hard-won lessons) stays hand-written in `HANDOFF.md` — never auto-generated. Read both.

Generated: 2026-08-16T08:45:45Z · body HEAD `c821cfc4d`

## Body
branch `main` · ahead 110 · behind 0 · working tree dirty

```
c821cfc4d ledger(3v0): re-anchor post-merge baseline + regenerate generated handoff
c2dbf81f0 merge: refresh onto upstream main (76 commits — compression/tail-mode, desktop-sdk, TUI defer_history, hooks modify-directive, computer-use, gateway loop isolation)
88be8a5c9 ledger(3v0): re-anchor position baseline + regenerate generated handoff (wake-#6 close)
9219cd394 fix(gateway): isolate post-turn loop failures
2f6bbfbcb fix(gateway): release loop ticks after empty responses
8672ce058 ledger(3v0): record wake-#6 store facts (carbon-fiber skin + de-brand prefs)
c14e34ef1 docs(3v0): handoff narrative for wake #6 (carbon skin + TUI de-brand)
17abdf632 feat(tui): 3V0 carbon-fiber skin support + de-brand Hermes/Nous identity
a15de3454 feat(desktop-sdk): host.deleteProfile — teardown-routed profile delete for plugins
69f7c655b docs(tui): document defer_history vs omit_messages precedence
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
- OK    Axiom (axiom)  behind=0 ahead=27  dirty=no
- OK    F1NANCE (f1nance)  behind=0 ahead=42  dirty=no
- DRIFT 3V0 (threev0)  behind=0 ahead=110  dirty=yes

summary: 1 drifting, 3 ok

## Open loops
- #72067 (pr) · claim OPEN · live OPEN (mergeable UNKNOWN, updated 2026-08-05) · agree — fix(memory): recover null/omitted action instead of dead-ending in 'Un… [canonical memory null-action recovery; CONFLICTING, author's job]
- #73453 (pr) · claim OPEN · live OPEN (mergeable UNKNOWN, updated 2026-08-05) · agree — fix(skills): preserve load failure details [preserve skill load failure details; awaiting merge]
- #84667 (issue) · claim OPEN · live OPEN (updated 2026-08-15) · agree — [Bug]: Skill loads via --skills but not when attached to a cron job; s… [cron skill-not-found; waiting on reporter's <error> string]
- #86711 (pr) · claim OPEN · live OPEN (mergeable UNKNOWN, updated 2026-08-15) · agree — fix(approval): collapse whitespace before matching approvals.deny glob… [approval-deny whitespace fix; awaiting maintainer merge]

## Store
facts by kind: directive=1, identity=1, memory=14, user=9 · 78 fact versions · 7 active skills · 57 skill versions

## Daemons
- 3v0-review: active
- axiom-review: active
- f1nance-review: active

## Startup (canonical)
1. `systemctl --user status 3v0-review f1nance-review axiom-review`
2. `bash scripts/handoff_check.sh`
3. `python3 3v0/scripts/continuity_check.py` (and `--heal` / `--accept`)
