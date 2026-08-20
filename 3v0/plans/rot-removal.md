# ROT Removal Plan — 3V0 Agent body repo (Expert-Plan, 2026-08-21)

Goal: remove all genuine ROT (Redundant, Obsolete, Trivial; dead code, dead
deps, stale artifacts, comment rot, broken/flaky tests) WITHOUT behavior
change, under Expert TDD / Code Review / Eval gates.

## Definitions (measurable ROT)

| Class | Measure |
|---|---|
| Dead modules | .py non-test file whose module stem never appears as an import token anywhere; not an entry point; not invoked by hook/config/docs |
| Dead deps | pyproject `[project]` dep whose import alias never appears in code |
| Artifacts | *.bak/.orig/.rej/.swp/.tmp tracked files |
| Comment rot | lines matching `^\s*#\s*(if|for|def|return|import|from|class|try:|except|elif|while|print(|self.)` |
| Test rot | failing/flaky/collection-error tests in a clean env |
| Trivial | empty files (non-`__init__`), placeholder stubs |

## Verified baseline (2026-08-21, tool-output grounded)

- 4,414 Python files; corpus tokens 161,020.
- Dead-module candidates: 2,782 raw → **2,704 are `tests/`** (pytest collects by
  path — heuristic false positives, excluded). Runtime true candidates: 43,
  dominated by:
  - `3v0/data/benchmark/*` (bench_core, bench_semantic, bench_tdai2,
    build_corpus, build_corpus2, _prod_enable_proof, _diag_embeddings) —
    orphaned; referenced nowhere.
  - `tools/xai_video_tools.py` (6.3KB) — orphaned (resolve_xai comes from
    elsewhere).
  - `3v0/tests/*`, `3v0/deploy/dev-root-guard.py`,
    `3v0/scripts/coherence_coalesce.py` — FALSE positives (hooks/config refs;
    verify before touching).
- Dead deps: 5 crude → alias-aware: python-dotenv/ruamel.yaml/pyjwt/
  python-multipart all imported. **True candidate: `tenacity`** (no import
  anywhere; verify dynamic/plugin use before removal).
- Commented-out lookalikes: 804 lines; heaviest: gateway/run.py (45),
  agent/conversation_loop.py (24), ev0_cli/config_defaults.py (21),
  tui_gateway/server.py (16), agent/auxiliary_client.py (16), cli.py (15).
- Artifacts: 3; Empty .py: 31 (all package `__init__` markers — benign, keep).
- Duplicate files: 2 groups, both empty-`__init__` clusters — benign.
- TODO 9 / FIXME 0 / XXX 2 — healthy.
- Test rot: 334 fails in rename subset (env-credential + order-dependent);
  15 collection errors from missing optional extras (acp/mcp not installed).
- Disk artifacts: root node_modules 372M, .venv 232M (gitignored).

**Expert-Eval headline:** after the 3,555-file rename the body is TIGHT —
genuine rot is surgical, not systemic: ~12 orphan files, ~800 comment lines,
1 dead dep, 3 artifacts, and a test-suite health problem.

## Phase 1 execution (2026-08-21)

**Verified exclusions (false positives caught by deeper checks):**
- `tools/xai_video_tools.py` — KEEP: wiki/TOOLS.md + manifest.tsv document it as a
  runtime tool module ("check git intent before deleting"); may be dynamically
  imported by the xAI provider. Wiki auto-sync would block removal anyway.
- `3v0/scripts/coherence_coalesce.py` — KEEP: referenced by scripts/handoff_check.sh:78.
- `3v0/deploy/dev-root-guard.py` — KEEP: installed as live profile hook
  (~/.3V0/profiles/3v0/hooks/) per dev-root-guard.README.md.
- "3 artifacts" (.tmpl files) — KEEP: kanban-video-orchestrator TEMPLATES, not junk.
- Empty `__init__.py` ×31 — keep (package markers).

**Removed:**
- `3v0/data/benchmark/` ENTIRE dir (3.7MB: 9 bench/corpus scripts, corpora,
  result JSONs, honest_* DBs, tdai/) — untracked + explicitly gitignored
  (.gitignore:244) + zero tracked references. Removed from disk.
- `tenacity==9.1.4` from pyproject.toml + uv.lock ("Removed tenacity v9.1.4",
  248 pkgs) — no import anywhere (sole mention = skill doc).

**Remaining P1:** comment-rot strip (comment-only diffs) in the 6 heaviest files.
**Gate:** stable-subset pytest rerun vs 339-failure baseline (proc kicked 2026-08-21).

## Phases (each gated)

- **Phase 0 — Eval baseline (DONE):** scans above + stable-subset pytest run
  (proc_10b571ca5614) → `/tmp/rot-eval-baseline.txt`.
- **Phase 1 — Orphan removal (TDD-gated):**
  1. Confirm `tenacity` unused (incl. plugins, dynamic imports, uv.lock).
  2. Confirm `coherence_coalesce.py` + `dev-root-guard.py` refs (hooks/config)
     before excluding.
  3. Delete: `3v0/data/benchmark/*` orphans, `tools/xai_video_tools.py`
     (after one grep for `xai_video` refs), 3 artifacts.
  4. Strip comment rot in the 6 heaviest files (only clearly-stale blocks;
     keep explanatory comments; no behavior delta).
  5. Remove `tenacity` from pyproject + `uv lock`.
  GATE: stable subset must pass at the same rate as baseline (no NEW
  failures); `git grep` + import scan re-run → orphan count = known allowlist.
- **Phase 2 — Test-suite repair (biggest ROI):**
  1. Install dev/mcp extras in a synced env; re-collect → 15 errors vanish.
  2. Triage the 334 failures: env-credential → mark xfail/skip with reason;
     order-dependent → isolate (fixture scope fixes); real bugs → TDD fix.
  3. Freeze an honest green subset; document the true count.
  GATE: stable subset green AND reproducible twice consecutively.
- **Phase 3 — Guard rails (prevention):**
  1. Add `scripts/rot_scan.py` (port of this scanner) + CI step: fail on NEW
     dead modules/deps/artifacts; allowlist current knowns.
  2. Update HANDOFF.generated + claims with the ROT baseline.
  GATE: scanner green on a seeded reintroduction.

## Expert TDD rule

No deletion is "refactor"; every removal is a behavior-preserving change:
run the gate suite BEFORE and AFTER each batch; deletions that flip a test
are not rot — revert. Comment stripping: diff must be comment-only.

## Expert Code Review rule

Each phase diff reviewed for semantic delta beyond the stated class; any
hunk touching executable lines outside the target file list = revert.

## Expert Eval rule

Each phase closes with measured deltas (files/LOC/deps removed, suite
failures delta) written to `3v0/plans/rot-removal.md` + HANDOFF.