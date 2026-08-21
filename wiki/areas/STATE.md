# threev0_state* + threev0_constants/logging — session store & profile paths

The session store family. `threev0_state.py` (SessionDB, FTS5) + schema/search/common/portability siblings; `threev0_constants.py` (home resolution — profile-aware), `threev0_logging.py`, `threev0_time.py`. Hardcoding ~/.3V0 elsewhere is the known-bug class.
---
Auto-rendered from `wiki/manifest.tsv` — `python3 scripts/build_wiki.py --rebuild` regenerates.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `threev0_bootstrap.py` | source | Early-boot module that applies profile override and seeds environment before other imports | Runs before everything so EV0_HOME / profile routing is correct at import time | threev0_constants.py; threev0_cli/main.py |
| `threev0_constants.py` | source | get_ev0_home() / display_ev0_home() — profile-aware path resolution | Every state path in the body resolves through here; hardcoding ~/.3V0 elsewhere is a known-bug class | threev0_logging.py; threev0_bootstrap.py; tests/threev0_cli/test_profiles.py |
| `threev0_logging.py` | source | setup_logging() — agent.log / errors.log / gateway.log (profile-aware) | All logs land per-profile via EV0_HOME; browse with 3v0 logs | threev0_constants.py; gateway/run.py |
| `threev0_state.py` | source | SessionDB — the SQLite session store (FTS5 search, project/session records) | Canonical session persistence backing resume/search/desktop; god-file, split across threev0_state_* siblings | threev0_state_schema.py; threev0_state_search.py; threev0_state_common.py; threev0_state_portability.py |
| `threev0_state_common.py` | source | Shared helpers for the session store family (types, paths, common queries) | Avoids circular imports between threev0_state and its satellites | threev0_state.py; threev0_state_portability.py |
| `threev0_state_portability.py` | source | Portability/backup layer for session stores (export, import, relocation) | Lets sessions survive profile moves and installs | moves: threev0_state.py; threev0_constants.py |
| `threev0_state_schema.py` | source | SQLite schema definitions + migrations for the session store | Keeps the DB schema versioned and migratable | threev0_state.py |
| `threev0_state_search.py` | source | FTS5 search layer over the session store | Powers /search and session picker; SQLite-side, no external indexer | threev0_state.py |
| `threev0_time.py` | source | Time helpers (UTC stamps, duration parsing) | Consistent time handling across scheduler/cron/session code | cron/scheduler.py; threev0_constants.py |
