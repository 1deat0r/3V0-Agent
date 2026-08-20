# Audit — files not edited 2026-08-21 (untouched cohort)

Goal (operator, 2026-08-21): every file/folder NOT edited today → every
line → verdict: NEEDED / IMPROVE / UPDATE / REMOVE / REPLACE (+ evidence).
Isolated worktree: this branch. Main tree untouched. Math: 2,920 files.

## Rubric
- NEEDED   — correct, current, keep as-is.
- IMPROVE  — keep, but fix/strengthen (toml/config hygiene, gaps).
- UPDATE   — keep, but refresh content (stale versions, dates, exclusions).
- REMOVE   — dead/obsolete/duplicated; safe deletion with rationale.
- REPLACE  — better option exists; propose the replacement, don't half-do it.

Evidence required per verdict: file:line or tool output. No verdict without
a look. TDD gate for any code change: run the file's tests in this worktree.

## Cohorts (priority order)
1. top-level + config (13 files)              -> VERDICTS-1
2. ev0_cli / gateway / agent / tools / cron / providers / acp_adapter / native
   untouched .py (runtime code)
3. plugins (145) — leaked-core/gate checks
4. skills + optional-skills (655) — stale refs, broken install scripts
5. ui-tui / web (283) — ts/js untouched files
6. wiki / docs / locales / assets (83+)
7. tests (1,406 untouched) — dead tests, stale fixtures (ties into P2)
8. .github / nix / misc infra (16+)

## State log
- 2026-08-21: worktree created (branch audit/untouched-2026-08-21),
  inventory → audit/untouched-inventory.txt. VERDICTS-1 drafted.