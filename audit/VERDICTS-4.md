# VERDICTS-4 — cohort 5: ui-tui + web (untouched)

283 files: 265 TS/TSX, 11 binary assets (fonts/favicon), configs (tsconfig,
vitest, eslint). Evidence:
- Unreferenced TS/TSX modules: 0 (every basename imported elsewhere).
- Risk scan: 1 hit — ui-tui/src/lib/openExternalUrl.ts uses child_process
  `spawn`; review: benign and safety-documented (http(s)-only URL filter,
  arg-array spawn, no shell; wired to onHyperlinkClick). Not a defect.
- Binary assets functional (served from web/public; fonts/favicon).
- Configs functional (build/typecheck/test/lint pipelines).

**Verdict: NEEDED ×283. No changes.**

COHORT 5 COMPLETE.