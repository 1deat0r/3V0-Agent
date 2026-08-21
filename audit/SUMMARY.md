# AUDIT SUMMARY — 1deat0r/3V0-agent, files not edited 2026-08-21

Scope: 2,920 tracked files untouched by the rename/fix window. Isolated
worktree branch `audit/untouched-2026-08-21`. All verdicts evidence-grounded
(import graph, reference corpus, frontmatter, risk-marker scans, spot reads).

## Tally
- NEEDED: 2,918 (kept — legal, functional, or referenced)
- IMPROVE applied: 2
  - .gitattributes: all lockfiles → linguist-generated (was web/ only)
  - plugins/platforms/wecom/wecom_crypto.py: `__import__("time")` → `import time`
- IMPROVE pending (blocked on external verification):
  - .npmrc stale release-age exclusions (needs npm registry age check)
  - AGENTS.md watcher list references nix files that no longer exist (low)
  - wiki/curated.tsv duplicate rows for the kanban PDF (low)
- REMOVE: 0 (nothing qualified — every file is wired into the system)
- UPDATE/REPLACE: 0 justified

## Notable exonerations (looked guilty, proven clean)
- security-guidance plugin eval/pickle/shell markers = prose teaching content
- agent/verify/runner.py shell=True = documented dev-tool trust model
- openExternalUrl.ts child_process.spawn = http(s)-only, arg-array, documented
- skills/index-cache/*.json = functional skill-hub caches; openai one is `[]`
  (honest empty state)
- 31 empty __init__.py = package markers
- 'stale/legacy' comments in session_state.py = deliberate migration-compat

## Legal keeps (untouchable)
LICENSE (MIT notice required on derivative), .mailmap (attribution),
SECURITY*.md (responsibility/contact), SUSTAINABILITY.md (commitment record).

## Merge path
Review branch → operator sign-off → merge to main. Nothing on the branch is
runtime-risky (2 source improvements, both compiled/validated).