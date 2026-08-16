# 3V0 — Session Handoff (GENERATED DRAFT)

> ⚠️ MECHANICAL DRAFT — never canonical. Generated from verified-consistent state by `3v0/scripts/generate_handoff.py`. The hand-written `HANDOFF.md` is canonical. Diff this against `HANDOFF.md` each wake; the diff is the acceptance evidence for the generated-handoff flip, which is the Operator's call and never self-authorized.

Generated: 2026-08-16T04:37:17Z · body HEAD `18e3f64e4`

## Body
branch `main` · ahead 87 · behind 0 · working tree dirty

```
18e3f64e4 docs(3v0): handoff — deferral resolved by research: fault-injection acceptance + shadow-mode draft-first
30f87785f test(3v0): fault-injection (chaos) validation of the continuity clock's collection half
b1b0a5c63 docs(3v0): handoff — correct grill-found false claims; re-scope generated-handoff deferral to operator
9b6ad9325 fix(3v0): continuity clock checks before heal — healable invariants were self-fulfilling (grill-found)
85899381d docs(3v0): handoff — wake #2, continuity clock observed clean, drift baseline re-recorded
543f67a26 ledger(3v0): record post-Stone-17 position baseline (drift_check --update)
908dc2dd4 memory(3v0): daemon captured Stone 17 continuity-meta + continuity-tick fact (session-review)
9b589068f feat(3v0): Stone 17 — loop claim registry + github-loops invariant
4bfa15e98 memory(3v0): retract fulfilled Stone 17 directive (built this session)
4b5a1f046 feat(3v0): Stone 17 — continuity meta (anchor → invariant model → reconstruction clock)
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
- OK    Axiom (axiom)  behind=0 ahead=23  dirty=no  [head moved]
- OK    F1NANCE (f1nance)  behind=0 ahead=41  dirty=no  [head moved]
- DRIFT 3V0 (threev0)  behind=0 ahead=87  dirty=yes  [head moved]

summary: 1 drifting, 3 ok

## Open loops
- #72067 (pr) · claim OPEN · live OPEN (mergeable CONFLICTING, updated 2026-08-05) · agree — fix(memory): recover null/omitted action instead of dead-ending in 'Un… [canonical memory null-action recovery; CONFLICTING, author's job]
- #73453 (pr) · claim OPEN · live OPEN (mergeable MERGEABLE, updated 2026-08-05) · agree — fix(skills): preserve load failure details [preserve skill load failure details; awaiting merge]
- #84667 (issue) · claim OPEN · live OPEN (updated 2026-08-15) · agree — [Bug]: Skill loads via --skills but not when attached to a cron job; s… [cron skill-not-found; waiting on reporter's <error> string]
- #86711 (pr) · claim OPEN · live OPEN (mergeable MERGEABLE, updated 2026-08-15) · agree — fix(approval): collapse whitespace before matching approvals.deny glob… [approval-deny whitespace fix; awaiting maintainer merge]

## Store
facts by kind: directive=1, identity=1, memory=13, user=8 · 75 fact versions · 7 active skills · 56 skill versions

## Daemons
- 3v0-review: active
- axiom-review: active
- f1nance-review: active

## Startup (canonical)
1. `systemctl --user status 3v0-review f1nance-review axiom-review`
2. `bash scripts/handoff_check.sh`
3. `python3 3v0/scripts/continuity_check.py` (and `--heal` / `--accept`)
