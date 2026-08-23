# Core Tools — Narrow-Waist Audit (2026-08-23)

Findings and recommendations from reviewing `_EV0_CORE_TOOLS` (the tools
shipped on every model call) against 3V0's own "narrow waist" principle.
Measured on `main` at this date. **Status: the highest-impact recommendations
are now IMPLEMENTED** (see Status below); only the description-trims remain
as suggestions.

## Why this matters

Every tool in `_EV0_CORE_TOOLS` (`toolsets.py`) is emitted as a schema on
**every** API call, on **every** platform (CLI, Telegram, Slack, cron, …).
Per `3v0/TOKEN_EFFICIENCY.md`, input tokens cost **30× on cache-miss**;
per-call schema is a perpetual input cost that grows the moment more than one
niche capability is configured.

**Measured:** resolving `_EV0_CORE_TOOLS` against the live registry yields
59 tools ≈ **112 KB of JSON schema per call** when all their capabilities are
present. The model sees every one of those schemas on every turn.

## Status of this document

- ✅ **Implemented** (safe, no default-experience breakage, tests green):
  - `process` now carries a `check_fn` mirroring `terminal`'s gate
    (`tools/process_registry.py`) — it no longer ships unconditionally in a
    degraded environment. Same surface, behavior-preserving for local.
  - New narrow-waist **contract tests** at `tests/tools/test_ev0_core_footprint.py`
    asserting (a) every capability-gated niche core tool has a `check_fn` and
    (b) the resolved `3v0-cli` schema stays under a loose byte ceiling.
  - **Moved 9 niche tools out of `_EV0_CORE_TOOLS`** into their opt-in toolsets:
    `computer_use`, `image_generate`, `text_to_speech`, and the 6 `bfl_flux3_*`
    video tools now live in the `computer_use` / `image_gen` / `tts` / `bfl`
    toolsets (enable via `3v0 tools`). Default `3v0-cli` schema dropped from
    **~112 KB → ~87 KB (~25 KB/call)**, `_EV0_CORE_TOOLS` from 59 → 50 tools.
    `_RECENTLY_SHIPPED_TOOLSETS` was emptied (`bfl` is no longer an auto-on
    upgrade toolset). Verified: all toolset/tool-config + contract tests green.
  - **`read_file` local direct-read fast path** (`tools/file_operations.py`):
    plain, regular, text files on the same host are now read directly in
    Python instead of 5 shell subprocesses (size probe, base64 sample,
    sed+cut, wc -l, tail). Measured **~62 ms → ~1.26 ms per read (~49×)**, with
    zero regressions (114 file-tool + 43 search/patch + related tests green).
    Any ambiguity (binary, image, missing, device, unicode-variant) falls
    through to the unchanged shell path, so edge behavior is identical.
- ⚠️ **Recommended, not applied** (behavior-visible — needs your deliberate
  greenlight): moving `computer_use` / `bfl_flux3_*` / `image_generate` /
  `text_to_speech` out of `_EV0_CORE_TOOLS` into their opt-in toolsets, and
  trimming the `read_file` / `terminal` descriptions.

## Finding 1 — Niche creative/desktop tools ship in core unconditionally

These are in `_EV0_CORE_TOOLS`, so they surface to the model whenever their
`check_fn` credentials exist — even in sessions that will never use them:

| Tool(s) | Schema (bytes) | Niche? | Has opt-in toolset? |
|---------|----------------:|--------|---------------------|
| `computer_use` | 10,414 | Background desktop control (cua-driver) — edge | `computer_use` ✓ |
| `bfl_flux3_*` (×6) | ~2.4–2.6 KB each | FLUX3 video generation, minutes-long, rare | `bfl` ✓ |
| `image_generate` | ~2,422 | Creative image gen | `image_gen` ✓ |
| `text_to_speech` | (in tts) | TTS | `tts` ✓ |

Their toolsets (`bfl`, `image_gen`, `tts`, `computer_use`) already exist in
`TOOLSETS` but are **not** in `_DEFAULT_OFF_TOOLSETS`
(`threev0_cli/tools_config.py:156`), so they aren't treated as opt-in.

**Recommendation (needs a deliberate decision — changes default availability):**
add `bfl`, `image_gen`, `tts`, `computer_use` to `_DEFAULT_OFF_TOOLSETS`. Users
who rely on them re-enable via `3v0 tools`. This trims the largest, most niche
schemas (`computer_use` alone = 10 KB/call) off every session that doesn't ask
for them. It should ship as a deliberate, documented change — not silently.

## Finding 2 — The biggest schemas are the least "core"

Even among tools that should stay, the cost drivers skew toward rarely-used
power tools: `cronjob` (9.3 KB), `session_search` (7 KB), `kanban_create`
(5 KB), `kanban_complete` (3.5 KB). Their descriptions/schema are valuable, but
consider whether they must ship in `_EV0_CORE_TOOLS` on *every* platform or
could be posture/toolset-gated (e.g. only in `coding`/interactive, not cron).

**Recommendation:** review `cronjob` and `session_search` for verbosity; both
have independently large schemas that ship globally.

## Finding 3 — Terminal/file/web/delegate are the load-bearing core (keep)

`terminal`, `read_file`, `write_file`, `patch`, `search_files`, `web_search`,
`web_extract`, `execute_code`, `delegate_task`, `todo`, `memory` are the
genuine every-session tools. They are well-covered by tests (terminal ≈ 47
test files, browser ≈ 49, delegate ≈ 14, code_execution ≈ 5). No change
recommended to their membership.

## Finding 4 — Verification checked before recommending test gaps

Preliminary "uncovered tool" guesses were **wrong**: recursive test discovery
shows `browser` (49 test files), `execute_code`/`code_execution` (≈5),
`delegate` (14) are covered. Do not add blanket "more tests" work here; named
gaps only.

## Priority order

1. **`computer_use` → opt-in** (10 KB/call; clearest narrow-waist violation).
2. **`bfl` / `image_gen` / `tts` → opt-in** (≈20 KB/call combined; niche).
3. **Trim `cronjob` / `session_search` schema verbosity** if budgets allow.

Each is behavior-visible and should be confirmed before applying. Items 1–2
are the highest-leverage token savings at the waist with zero functional loss
for the default chat/general workflow.