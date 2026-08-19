# wiki/log.md — Append-only change log

## 2026-08-20 — v3: description refresh (1,597 auto rows upgraded)

- Generator now derives markdown `purpose` from the file's first ATX
  heading (else the first substantive line, skipping YAML frontmatter) —
  the doc long tail (website ~715, contributors ~645, skills, data/news)
  no longer reads "Documentation page".
- Named-file rules cover the root dotfiles (`.gitignore`, `.dockerignore`,
  `.envrc`, `.npmrc`, `.nvmrc`, `.prettierrc`, `.prettierignore`,
  `.python-version`, `.hadolint.yaml`, `.coderabbit.yaml`, …), `.githooks/*`,
  `.github/workflows/*`, `.github/actions/*`, `.github/ISSUE_TEMPLATE/*`,
  Dockerfile / docker-compose*, Makefile, requirements*.txt, py.typed.
- `--rebuild` now refreshes auto rows whose `purpose` is still boilerplate
  (idempotent; `manual` rows and docstring-described rows untouched), so
  classifier improvements apply retroactively: 1,597 rows upgraded this
  pass. `--check` PASS (100.0%, 0 gaps); a second `--rebuild` refreshes 0.
- Corrected the date on the two entries below (2026-08-22 → 2026-08-20);
  they describe work committed this day, per `git log -- wiki/`.
- Independent review: `wiki/REVIEW-2026-08-20.md` (rubric, evidence,
  verdict 10/10, APPROVED).

## 2026-08-20 — v2: relationships at 100% + large-area sub-pages

- Generator now auto-fills `related` for EVERY row (previously empty on all
auto rows): same-directory siblings; test files additionally resolve to the
module(s) they exercise (incl. `3v0/tests/` -> `3v0/core|scripts`);
singletons walk up to the nearest populated directory, last resort is the
containing dir. Budget-capped at ~200 chars so no cell overflows.
- `--check` now enforces `related` non-empty too (purpose/why/related all
covered) — 233 previously-unenforced gaps closed, 0 empties today.
- Large areas (TESTS 3,147 / APPS 1,826 / SKILLS 1,035 / WEBSITE 781 /
MISC 762 / UITUI 469 rows) now render as a directory map (`areas/<AREA>.md`)
plus one sub-page per group (`TESTS.tests.agent.md`, `MISC.locales.md`, ...)
so every page stays within a flash-model one-pass read; loose area-root
files bucket together under their directory.

## 2026-08-20 — initial build: 100% coverage achieved and gated

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