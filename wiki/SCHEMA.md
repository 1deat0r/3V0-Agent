# wiki/SCHEMA.md — The Wiki Maintenance Contract

The wiki is the 3V0 Agent repository's compiled knowledge layer: a
persistent, interlinked catalog an aux model (typically
`deepseek-v4-flash-0731`) can read cheaply. Code stays the raw source; the
wiki is a *pointer layer* — it never replaces reading the code, it tells you
where to look and why a file exists.

## 1. The invariant (hard gate)

> **Every tracked git path has exactly one `wiki/manifest.tsv` row with
> non-empty `purpose`, `why`, and `related` (description + rationale +
> relationships — the operator's 100% coverage ask covers all three).**

This is enforced mechanically:

```bash
python3 scripts/build_wiki.py --check   # exit 1 on any gap; wired into .githooks/pre-commit
```

Coverage must stay at 100.0%. The gate makes the index unable to silently
drift behind the tree: add/rename/delete a tracked file and the next pre-commit
fails until the manifest is regenerated.

## 2. Artifacts

| Path | Kind | Maintained by |
|------|------|---------------|
| `wiki/manifest.tsv` | raw catalog, 6 TSV cols: `path kind curated purpose why related` | `--rebuild` (generator) |
| `wiki/areas/<AREA>.md` | per-area tables, regenerated verbatim; large areas render as a directory map with sub-pages per group | `--rebuild` |
| `wiki/areas/_intro_<AREA>.md` | hand-written area narrative, prepended by `--rebuild` | human/agent, never clobbered |
| `wiki/curated.tsv` | hand-curated overlay (manual rows), same 6 columns | human/agent, must keep 6 cols/row |
| `wiki/index.md` | master catalog + reading order | human/agent |
| `wiki/SCHEMA.md` | this contract | human/agent |
| `wiki/log.md` | append-only change log | human/agent |
| `wiki/README.md` | one-paragraph orientation | human/agent |

`manifest.tsv` header is `path\tkind\tcurated\tpurpose\twhy\trelated`.
`curated` is `auto` (regenerated) or `manual` (from `curated.tsv`, preserved).

## 3. Editing workflow

- **Tree changed (any add/rename/delete):** run
  `python3 scripts/build_wiki.py --rebuild`, review the diff, commit.
  `--rebuild` is idempotent and preserves manual rows + intros.
- **Improve one entry:** edit `wiki/curated.tsv` (their format is identical;
  the entry must be a *tracked path* to take effect — bare directory rows are
  reference-only). Keep cells tab-free and within caps:
  purpose ≤ 160 chars, why ≤ 160 chars, related ≤ 220 chars.
- **Rewrite an area's narrative:** edit `wiki/areas/_intro_<AREA>.md`.
- **New area:** add to `AREA_ORDER`/`AREA_TITLE` in `scripts/build_wiki.py`,
  the `area_of()` rule, and an intro file; `--rebuild`.

## 4. Row-writing rules (quality contract)

1. **purpose** = what the file IS (noun phrase). **why** = why it exists /
   what breaks without it. **related** = sibling paths that form the
   subsystem (semicolon-separated).
2. Be **specific and honest** — prefer "the only sanctioned test runner"
   over "test infrastructure". Use the repo's own vocabulary (footprint
   ladder, cache-sacred, fail-closed, chain anchor).
3. Budget-conscious: a flash-class model reads whole pages in one pass;
   keep every cell terse. No filler like "useful for developers".
4. **Never state what you haven't verified** — if unsure, leave the row
   `auto` (docstring-derived) rather than guessing.
5. Tests/docs/config rows may stay `auto` when the docstring is already the
   best description; curation effort goes to the load-bearing spine
   (root, core, agent, tools, gateway, cli, cron, plugins, skills, apps).
6. **Auto rows get `related` for free**: the generator fills same-directory
   siblings (test files additionally point at the module(s) they exercise;
   singletons walk up to the nearest populated dir, last resort the
   containing dir). A curated row's `related` overrides the derivation.

## 5. Wiring

- `.githooks/pre-commit` runs the check (step 4 of the hook chain).
- `scripts/handoff_check.sh` may report wiki health during the wake ritual.
- `verify.sh` treats a failed `--check` as an unclean body.
- `AGENTS.md` points agents here before they navigate the tree.

## 6. Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `--check` fails "missing" | tracked file added/renamed, manifest not rebuilt | `--rebuild`, commit |
| `--check` fails "empty" | a row lost purpose/why/related (bad curated.tsv edit) | fix the row or `--rebuild` |
| `--check` fails "overlength" | a derived related list or hand cell exceeds caps | shrink the cell / rebuild |
| manual count dropped in `--report` | curated.tsv overwritten/no longer parsed (bad TSV) | check 6 columns/row, tabs only |
| area page missing a table | area key added without `--rebuild` | `--rebuild` |
| sub-page missing from a large area | `--rebuild` not run after adding files there | `--rebuild` |

Version note: schema changes to this contract itself are recorded in
`wiki/log.md`, append-only.