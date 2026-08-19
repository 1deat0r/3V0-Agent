# 3V0 Repo Wiki

An LLM-readable, always-current index of the 3V0 Agent repository.
Every tracked file has a one-line purpose + rationale; the long tail is
docstring-derived (`auto`), the load-bearing spine is hand-curated
(`manual`) — see `wiki/SCHEMA.md` for the contract.

- **Start:** `wiki/index.md`
- **Deep pages:** `wiki/areas/` (one table per area, budget-capped cells)
- **Raw data:** `wiki/manifest.tsv`
- **Hand overlay:** `wiki/curated.tsv` (+ `wiki/areas/_intro_*.md`)
- **Gate:** `python3 scripts/build_wiki.py --check`

Regenerate after tree changes with `python3 scripts/build_wiki.py --rebuild`.
The pre-commit hook blocks a stale wiki.