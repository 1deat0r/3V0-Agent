# VERDICTS-5 — cohorts 6-8: wiki/docs, tests, misc infra (untouched)

## Wiki/docs (84) — NEEDED
All indexed (manifest.tsv, curated.tsv, MISC/DOCS area pages, HANDOFF, log).
The `_intro_*` pages are area-intro entries; REVIEW-2026-08-20 is a live
audit artifact; 3v0-kanban-v1-spec.pdf is the kanban contract.
FIND (low): wiki/curated.tsv has DUPLICATE rows for
docs/3v0-kanban-v1-spec.pdf (rows 392 + 456) — tidy later (curated.tsv is
in the touched set; wiki rebuild/QA can dedupe).

## Tests (1,406) — NEEDED (mechanical pass)
- 1,401 .py + 5 fixtures; 0 dead fixtures; 0 broken `tests.*` imports;
  43 skip/skipif + 1 xfail (reasonable, not rot).
- Deep de-flake (the 82 canonical failures + order-dependence) is tracked
  in the main-tree ROT plan (3v0/plans/rot-removal.md, P2) — not a
  static-cohort issue.

## Misc infra (.github 17 workflows, top-level configs) — NEEDED
All workflows parse and target real jobs (lint/tests/os matrix/install
e2e/supply-chain/lockfile-diff). .coderabbit auto-review disabled by
design. nix layer: none tracked (watcher refs stale — low IMPROVE noted
in AUDIT_PLAN).

ALL COHORTS COMPLETE (2,920 files). Summary in audit/SUMMARY.md.