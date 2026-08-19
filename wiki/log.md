# wiki/log.md — Append-only change log

## 2026-08-22 — initial build: 100% coverage achieved and gated

- `scripts/build_wiki.py` (v1): tracked-file manifest generator + area renderer
  + `--check` hard gate (exit 1 on missing/empty/overlength) + `--report`.
- `wiki/manifest.tsv`: 9,722 rows = 100.0% coverage of tracked paths
  (auto entries from module docstrings + path rules).
- `wiki/curated.tsv`: 414 hand-curated rows covering the load-bearing spine —
  repo root, 3v0/ core, agent/, tools/, gateway/, ev0_cli/, cron/, plugins/,
  skills categories, providers, apps/, ui-tui/, web/, website/, docs/,
  scripts/, tests/, infra, misc.
- 20 area pages + 20 hand-written area intros (`wiki/areas/`).
- Wiring: `.githooks/pre-commit` step 4 runs `build_wiki.py --check`;
  `verify.sh` checks wiki cleanliness; `AGENTS.md` points agents at
  `wiki/SCHEMA.md`.
- Consumer target: the `deepseek-v4-flash-0731` aux agent (budget-capped cells).
- Schema v1: 6-col TSV (`path kind curated purpose why related`), caps
  purpose/why ≤ 160, related ≤ 220.