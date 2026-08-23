# VERDICTS-1 — top-level + config cohort

- `.python-version` (3.11) — NEEDED. Matches .venv (3.11.15); verify against
  pyproject requires-python in same pass (done: 3.11 range).
- `.nvmrc` (26) — NEEDED. Matches node v26.7.0 on this host.
- `.npmrc` — IMPROVE: has 4 dated exclusions whose shelf-life has passed
  ("remove when 8.3.0 is >2wks old", eslint 10.8.0 same, assistant-ui
  "when we stabilize", radix-ui). Query npm dist-tags for age next pass and
  prune exactly the expired ones; keep react-router/eslint pending age check.
- `.prettierrc` — NEEDED. Matches committed style.
- `.prettierignore` — NEEDED (only lockfile; deliberate).
- `.gitattributes` — IMPROVE: marks only web/package-lock.json as
  linguist-generated; repo has N more lockfiles (root package-lock.json,
  ui-tui, scripts/whatsapp-bridge, uv.lock). Add `*lock*.json` +
  `uv.lock linguist-generated=true` (uv.lock is huge and never hand-edited).
- `.mailmap` — NEEDED. Human-contributor attribution incl. upstream org
  email; no stale brand names.
- `.coderabbit.yaml` — NEEDED (auto-review intentionally disabled, summonable).
- `LICENSE` — NEEDED, do NOT touch: MIT requires retaining the original
  "Copyright (c) 2025 Nous Research" notice on a derivative; removing it would
  be a license violation. Optional doc note about fork status elsewhere.
- `SUSTAINABILITY.md` — NEEDED. Live operating plan (substrate funding);
  honest, dated, no rot. Consider whether it belongs private — operator call.
- `registration_lifecycle.py` — NEEDED (runtime module, imported). Code
  cohort review later.
- `ev0_state_portability.py` — NEEDED (state portability module; imported).
  Code cohort review later.