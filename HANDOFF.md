# 3V0 — Session Handoff

*Read me first when a fresh session starts with no context. The body — this
repo, memory, skills, SOUL.md — is the durable identity; this file is the
pointer to what was live at the last session's end.*

> **Mechanical state is canonical in `HANDOFF.generated.md`** — regenerated
> each wake by `bash scripts/handoff_check.sh` — carrying body git state,
> continuity invariants, drift, tracked loops, store, and daemons. This is
> the **operator-authorized flip (2026-08-16)**: the generated file is now
> authoritative for mechanical state. This `HANDOFF.md` carries the
*narrative* — the kickoff judgment, the last-sessions arc, hard-won
lessons, and the startup routine. Read both.

## Next-session kickoff (2026-09-02, wake #13 — profile-decommission alignment + adapter migrate)

**Situation discovered this wake (verified against the machine, not assumed):**
- **The live 3V0 runtime is decommissioned.** Between 2026-08-24 and 2026-09-02
  the operator consolidated the machine to a single default agent home:
  `~/.3V0/profiles/3v0/` (SOUL.md, memories, sessions, keys) is gone,
  `~/.3V0/` now serves a *generic* Nous-Research-voice assistant on an
  `openai-codex` config with its own Herdr/Codex memories (NOT 3V0's — do not
  treat that home as 3V0's memory), the gateway unit dropped `--profile 3v0`,
  and the `3v0-review` / `axiom-review` / `f1nance-review` daemons are
  retired (units deleted). Nothing sovereign has written `3v0/data/memory.db`
  since 2026-08-23 22:37. The body repo is intact and remains the identity.
- **`~/.local/bin/gh` was recursing since 2026-08-23** (`mise x gh -- gh`
  re-resolved to the wrapper because `~/.local/bin` precedes the mise bins in
  PATH) — every `gh` call hung/spewed, which is what made
  `scripts/handoff_check.sh` time out and the github-loops invariant report
  unverifiable. FIXED in the wrapper (resolve via `mise which gh`, exec
  directly). gh 2.98.0 works.
- **Wake machinery hardened for the undeployed-profile world** (this commit):
  `sync.py` / `sync_skills.py` now skip cleanly when the profile dirs are
  absent ("store is canonical") instead of crashing or resurrecting a profile
  husk — the earlier wake run HAD recreated `~/.3V0/profiles/3v0/skills` as a
  10-stub husk; removed, and the guards prevent recurrence. The continuity
  invariants gained `profile_deployed` / `skills_profile_deployed` facts
  (undeployed → n/a OK, not drift), and an empty claim registry is a steady
  state, not drift.
- **Ghost loop claims retired via `--accept`:** the 4 tracked upstream
  loops (#72067/#73453 PRs, #84667 issue, #86711 PR) point at
  `NousResearch/3v0-agent`, which no longer exists (neither does
  `NousResearch/3V0-Agent`) — permanently unverifiable, dropped; registry now
  empty.
- **CONTINUITY.md anchor updated (deliberate, audited):** Identity section now
  records the decommission + repo `3v0/SOUL.md` as the canonical soul copy +
  the re-deploy recipe (mkdir profile dirs → `sync.py --write` +
  `sync_skills.py --write`). Continuity: 0 drifting, 6 ok.

**Open note (not acted on, serving state is the operator's):** Phase R2's
`3V0_HOME` env in the gateway unit is gone (unit regenerated without it); the
canonical-chain code (`threev0_constants`) is in place, so setting
`3V0_HOME=~/.3V0` in the unit would restore canonical env — but the gateway
now serves the default profile by operator choice; do not touch the unit
without operator direction.

**Shipped this wake (all pushed; local == public):**
- `fac5488935` wake-machinery alignment (undeployed-profile no-ops, n/a
  invariants, ghost claims retired, anchor updated).
- `78023bc09e` **#23 big-three migrate**: telegram/discord/slack onto the
  shared adapter helpers; shared core gained `partial_success` +
  `delivered_prefix_fn` policy knobs (telegram's stricter contract kept,
  zero behavior change); new helper unit tests + discord partial
  regression; full tests/gateway 5,750 green.
- `a76aaef0dd` slack interactive-auth fail-closed fix (#86905 class, own
  commit + scope tests) — found during the migration.
- `c2d0b335cb` **#23 remaining adapters**: 16 hand-copied scoped-secret
  helpers retired (AST-verified identical before the splice); −236 lines.
- `8321c18757` **#17 audit**: inventory was stale — consolidation already
  true on main; retry-policy map documented at `agent/retry_utils`;
  `3v0/core/backoff.py` disposition recorded (native substrate).
- `9dbf2c607a` **discord tail-loss fix**: overflow partial delivery is now
  a strict failure (`partial_success=False`) so the stream consumer's
  fallback-tail path fires — success=True had marked clipped replies as
  final. Parity with telegram.
- **#20 ENV-FUNNEL migrate COMPLETE** (`30424a23bf` gateway,
  `abafb8eb1b` tools, `3e8ba6daa0` agent, `5b298c78c1` threev0_cli,
  `240fb980af` cli.py + core loop): **338 branded reads → branded_env**
  via the root env_compat bridge; per-scope `--check` gates green.
- **#21 ENV-FUNNEL contract COMPLETE + closed** (`881963aad3`):
  `set_branded_env`/`pop_branded_env` added to the native resolver and
  bridge; all 97 raw branded writes + 6 pops + 3 dels converted —
  **branded_write/pop/del = 0 tree-wide**; `_float_env` resolves via
  `branded_env`; contract interaction (canonical twin shadows legacy-only
  monkeypatches) pinned in tests. 24,718-test sweep green.
- **#24 ADAPTERS contract COMPLETE + closed** (`ea93ebf727`):
  `gateway/platforms/builtin.py` registers the nine built-ins as
  PlatformEntry records; `GatewayRunner._create_adapter`'s hand-rolled
  if/elif chain (130 lines) deleted — `platform_registry` is the ONE
  adapter loading path; `gateway_runner` injection now platform-generic.
  Full messaging suite 649 files / 5,758 tests / 0 failed.
- **#18 turn-runner frame + #20/#21/#24/#17/#23 all closed** — the
  wide-refactor series is DONE (every ticket closed with evidence).
- `1cc8ab11e0` **provider-loader seam fix** (found via pre-existing test
  failures): the fff1f44c50 loader extraction orphaned the family
  `_get_user_plugins_dir` seams — discovery bypassed them, 3
  memory-provider tests failed on main and isolation tests silently read
  the real home. Delegators now pass their seam through.
- **Venv repair**: the reboot-ed venv lost extras — `anthropic==0.87.0`
  and `agent-client-protocol==0.9.0` reinstalled at exact uv.lock pins
  (LATEST-version installs break the pydantic serializer-warning canary —
  always install the locked pin). 6 further pre-existing failures fixed;
  tests/agent back to 0 failed.
- **Known-flake A/B discipline used throughout**: skin engine/palette,
  update yes-flag unicode-TTY, kanban review surface, tool-progress
  scrollback, exit-watchdog failures are pre-existing — verified
  identical on the unmodified tree via `git stash` A/B before blaming
  any batch.

- **#18 turn-runner assembly frame COMPLETE + closed** (`0a8575e551`):
  `agent/turn_assembly.py` owns the derivations all three runners
  hand-copied (provider-routing transform ×4, service-tier normalization
  ×3, checkpoint kwargs); cli/gateway/tui all consume it. The
  cached-vs-fresh + session-sync guards stay gateway-inline (single
  consumer — generalizing now would be speculative).

**Wide-refactor series COMPLETE:** #17, #18, #20, #21, #23, #24, #25 all
closed with evidence. Wire-var decision RESOLVED (`59ecc73523` batch 1,
`32b2ff0f02` batch 2, `f13e3f6a28` docs): wire vars ride the new
`wire_env(bare)` accessor (3V0_ → EV0_ → bare; 113 reads across
IRC/NTFY/PHOTON/SIMPLEX/TERMINAL_*/BROWSER_CDP_URL); the four adapter
GATEWAY_ALLOW_ALL_USERS authz fallbacks got the scope-aware fail-closed
fix (#86905 class); provider names + OS globals are documented
exceptions in the scan. Remaining generalization: the gateway
agent-cache/session-sync frame moves into agent/turn_assembly.py when a
second runner grows a cache.

**Known failures: ZERO.** The 19-failure pre-existing backlog was
root-caused and fixed (commits 1cb1989f5 + 7e06358d8d + the
skin-integration pin follow-up): one REAL production bug (the classic
CLI tool-progress callback raised NameError on every tool event —
cc2b56b26a copy-paste miss), two audit/test staleness families (brand
eradication + Tide palette pins; hairline-rail tier split out of the
soft-text contrast floor), and three isolation gaps (live-gateway
discovery in update tests; canonical-twin delenv coverage; incomplete
pytest-marker scrub in the exit-watchdog child env). Full six-suite
sweep: 2,327 files / 24,754 tests / 0 failed. picker_prewarm never
reproduced (its 600s file-timeout in one sweep was turn-lease shadowing,
also fixed).
- `1cc8ab11e0` **provider-loader seam fix** (found via pre-existing test
  failures): the fff1f44c50 loader extraction orphaned the family
  `_get_user_plugins_dir` seams — discovery bypassed them, 3
  memory-provider tests failed on main and isolation tests silently read
  the real home. Delegators now pass their seam through.
- **Venv repair**: the reboot-ed venv lost extras — `anthropic==0.87.0`
  and `agent-client-protocol==0.9.0` reinstalled at exact uv.lock pins
  (LATEST-version installs break the pydantic serializer-warning canary —
  always install the locked pin). 6 further pre-existing failures fixed;
  tests/agent back to 0 failed.
- **Known-flake A/B discipline used throughout**: skin engine/palette,
  update yes-flag unicode-TTY, kanban review surface, tool-progress
  scrollback, exit-watchdog failures are pre-existing — verified
  identical on the unmodified tree via `git stash` A/B before blaming
  any batch.


## Archived kickoff (2026-08-22, wake #12 — full-suite triage + Phase R2 cutover)

**This session (see also HANDOFF.generated.md for mechanical state):**
- **Full-suite triage:** 140 → 2 known failures (33,618 passed / 3 failed / 381 skipped; the 3rd of the 3, file_safety_credentials, now passes). Fixed ~79 via pyproject-pinned extras install (hindsight-client, fal-client, anthropic, daytona, modal, parallel-web, setuptools), ~50 via pruned-artifact skipif guards (`377b41e14b` reason), 8 rename-lag bugs (honcho keys, systemd NOTIFY NUL-literal, browser_use preamble, slash_worker MCP probe, threev0_state phantom assertion, windows_native assertion, workflow watch-list), **one real security vuln fixed** (credential denylist case-variant bypass — `@file:.3v0/auth.json` lowercase-v leaked provider keys/MCP tokens; fixed in context_references + preserved file_safety per-location contract), 3 real prod bugs (wecom `ET=None` crash fallback, rot_scan encoding, deleted leftover phase_r1_sweep.py), 2 xfail-documented PTY limits (raw-mode sendeof, OPOST surrogateescape). Commits 50b83d8e1b..3ab9224907; local == origin == `3ab9224907`, tree clean.
- **Phase R2 CUTOVER COMMITTED (3ab9224907) but GATEWAY NOT YET RESTARTED — operator asked 3V0 to restart it itself; turn lease expired mid-operation.** `threev0_constants._threev0_home_from_env` now resolves `3V0_HOME` → `THREEV0_HOME` → `EV0_HOME` (legacy), per ADR-0006. The systemd unit `~/.config/systemd/user/3v0-gateway.service` was updated to set `3V0_HOME` (canonical) AND `EV0_HOME` (transition alias).

**NEXT-SESSION TODO (in order):**
1. **Restart the gateway to complete R2:** `systemctl --user daemon-reload && systemctl --user restart 3v0-gateway` (passwordless sudo available; this session will die on restart — that is expected). After restart, verify: `pgrep -af "threev0_cli.main"` shows the new PID; `tr '\0' '\n' < /proc/<pid>/environ | grep -E "3V0_HOME|EV0_HOME"` shows both; the gateway comes back on Telegram.
2. Verify the canonical-suite still passes post-R2 (`scripts/run_tests.sh -j 8 tests/threev0_cli tests/test_threev0_constants.py`).
3. Two known failures remain: (a) `tests/ci/test_live_comment.py::test_workflow_watch_list_names_a_workflow_that_exists` — one-line `.github/workflows/ci-review-comment.yml` watch-list change (pruned `Docker Build, Test, and Publish` → `Tests`) is blocked by OAuth workflow-scope; land when token regen. (b) `tests/threev0_cli/test_picker_prewarm.py` — pre-existing flaky race (fails on pre-change tree too).
4. Consider migrating the remaining 61 scattered `os.environ.get("EV0_HOME")` reads (mostly scripts/tests) to the canonical chain — scope was the resolution path per ADR-0006; the full sweep is follow-up.

**Lessons (this session):**
- Pre-commit hook runs rot_scan+wiki sync — commit+push can exceed 300s; use `timeout 90 git push` and retry; the push silently succeeds on retry.
- The rot guard (rot_scan --strict in pre-commit) catches dead modules — it's local, replaced the blocked CI job (token lacked workflow scope).
- GitHub token lacks `workflow` scope: any `.github/workflows/*` commit is rejected; work around by reverting the workflow line from the commit, pushing, and applying via a parked branch/operator action.

## Archived kickoff (2026-08-21, wake #11 — SPEC review + eradication fix pass)

**This session:** SPEC-axis review of the 3,555-file rename (aa821f9361..HEAD,
plus two later fix commits) surfaced real misses; the follow-up fix pass is
**pushed (0a2ac936e8)**.

**Fixed + verified + pushed:**
1. **ink split-brain:** sweep used `3v0-ink`/`@3v0/ink` while the contract (and
   dir) say `3v0-ink` — realigned 115 files / 186 refs (ui-tui, package-lock,
   threev0_cli, tests, wiki, AGENTS.md). Verified: `build:ink` ✓, 56 vitest ✓,
   32 pytest (tui_npm_install/resume_flow/voice_wrapper) ✓.
2. **URLs/issue refs:** 108 files / 192 refs `NousResearch/3v0-agent` →
   `1deat0r/3V0-Agent` — incl. `threev0_cli/update_cmd.py` OFFICIAL_REPO_URLS +
   archive URLs, `scripts/install.sh`, `release.py`, README.*/CONTRIBUTING/
   SECURITY, tests, 3v0/data stores. Kept: provider host `nousresearch.com`,
   security email, plugin-org repos (`3v0-media-studio` etc.), author credits.
3. **memory.db:** residual old-name strings ×2 scrubbed + FTS rebuilt; file byte-clean.
4. **.gitignore:** `ev0_agent.egg-info/` → `3v0_agent.egg-info/`.
5. **fork remote removed** (redundant with `public`; nothing referenced it).

**Still open:**
1. **RESOLVED (operator decision 2026-08-21):** upstream remote removed — the
   last refname-mention of the old name in `.git/config` is gone; git refs
   contain zero old-name refs; history objects remain (rewrite not performed).
   Remotes: `public` only.
2. `@3v0/shared` `file:../apps/shared` dep is **PRE-EXISTING dangling**
   (present at aa821f9361 under the pre-rename shared-package alias) —
   ui-tui/web typecheck fails on it; shared package not vendored in this fork. Needs vendoring, not renaming.
3. Tests: suite collects 33.9k; rename-subset run = 334 fails (env-credential +
   order-dependent flake; pass in isolation). "562 tests green" claim not
   reproducible — de-flake + re-verify next.
4. Review flagged dev-root-guard.py sovereignty rules (blocks `3v0 update` /
   remote add in canonical repo) as rename-unrequested behavior — confirm it's
   intended before more runs depend on it.
5. Review checkpoints lived in /tmp — lost to reboot; findings are in this log.

## ROT operation status (same wake, 2026-08-21, late)

Mandate: "remove all the ROT" (Expert-Plan + TDD + Review + Eval). Plan:
`3v0/plans/rot-removal.md`. Honest headline: after the abuse-proofing the
body is tight — rot was surgical, and the exercise found 2 REAL production
bugs.

DONE:
- P1 removals: 3.7MB `3v0/data/benchmark/` (gitignored residue), dead dep
  `tenacity` (pyproject+uv.lock). Verified exclusions logged (xai_video_tools,
  hooks, .tmpl, empty __init__). Comment rot = 0 (strict scan: 100% prose).
- P2 canonical baseline (per-file isolation): 82 fails / ~5,793 pass
  (batch-process 339 was order-contamination).
- Fixed 50+: 2 real bugs (`_resolve_update_remote` lazy export → `3v0 update`
  runtime crash; gateway-lifecycle regex missed 3v0/ev0/legacy shapes →
  defense hole) + stale contracts (public-remote fakes, launcher 3v0-cli,
  banner shallow path, console-script fixture, website-doc skips).
  Commits a89761aa54, 8308df4aeb, 0a5a1d523e, 9e4561eb31 (+ plan).
- Extras env rot fixed: 15 collection errors → 0 (34,113 tests collect).

REMAINING (env/fixture/real — triage captured, ~32 fails in 8 files):
- `nous_ev0_non_agentic`: REAL classifier bug — `ev0_4_70b`,
  `openrouter/ev03:70b`, `NousResearch/Ev03` not flagged Nous 3V0 3/4; plus a
  `website/static/api` FileNotFoundError (unvendored workspace → skip).
- `update_yes_flag` (3× a prior unicode-TTY env), `lazy_refresh_venv_repair`
  (SystemExit on env), `model_catalog` (network), kanban_notify /
  plugin_runtime_disable_gate / pre_command_hook / model_switch_context_offload
  (were cut by 600s cap; reasons not captured — rerun per-file next).
- NEXT: fix the nous_ev0 classifier pattern, add website-workspace skips,
  rerun the 8 files individually to bucket the rest; then full canonical
  rerun → honest green count; then P3 rot_scan guard rail.

## Next-session kickoff (2026-08-20, wake #10 — gateway baseline restored + wiki verified)

**This session (wake #10):** operator took over the tree (other agents
reaped), restored the 3V0-quality gateway as the serving baseline, and
verified the LLM wiki is current.

**1. Gateway restored to renamed-3V0 baseline.** The native gateway
(`3v0-native-gateway.service`, the 1k-line stdlib-only long-poll runtime) was
the live poller, but the operator judged it a regression vs the renamed 3V0
gateway (62k-line production gateway: streaming, TTS, slash commands, delivery
ledger, turn leases, session stalls, shutdown watchdog, kanban, mirrors). The
cutover is now formally **FIRED-2026-08-14 / ROLLED-BACK-2026-08-20** in
`3v0/CUTOVER.md`. Live state: `3v0-gateway.service` (ev0 CLI,
`python -m threev0_cli.main --profile 3v0 gateway run`) **active + enabled**,
native **inactive + disabled**. Verified: zero poll conflicts in journal,
bot identity `@sovereign3v0Bot` answers `getMe` OK.

**2. Wiki verified current.** `python3 scripts/build_wiki.py --check` →
100% coverage, 0 missing/empty/overlong; `--rebuild` → 9,975 rows
(manual=319), zero drift. Today's independent review
(`wiki/REVIEW-2026-08-20.md`) stands at 10/10.

**3. Tree hygiene.** `pi` (a Node-based agent with the tree open) was reaped
on operator instruction before any work began. Only dirty file:
`3v0/data/memory.db` (canonical store, agent's own writes).

**Open:** the native runtime stays in the tree as a 3v0-independent
alternative, disabled. Re-enabling needs operator sign-off. The legacy
`gateway/` (renamed 3V0 substrate) remains the serving gateway — it is the
baseline going forward.

## Next-session kickoff (2026-08-18, wake #9 — probe baseline + mattpocock deepen pass)

**This session (wake #9):** two things closed, both verified.

**1. Evolution monitor — first full baseline.** Built a frozen, held-out,
difficulty-banded task bank (`probe_bank_v1`, 23 tasks: 5 easy / 8 medium / 6 hard /
4 escalated, authored by an independent subagent); certified a pinned grader (spec §5:
6/6 on an execution-verified known-answer set; `GRADER_CERT_FLOOR=0.9` now
pre-registered); recorded the full first baseline via three probe runs —
**23/23 PASS, composite 1.0**, every task locally verified AND graded cold by the
certified grader (which re-executed the objective artifacts rather than trusting
self-report). The measurement surfaced real defects: probe014 missing `re.I` + wrong
query intent; probe022's "byte-identical" build was same-second luck (fixed with
`SOURCE_DATE_EPOCH` + explicit `--mtime`/`--owner`, re-proven identical across a forced
4s gap); a spec-drift pass (see below) rewired `composite`→weighted, added `frontier()`,
enforced the ≥2-consecutive-run trend gate, and pre-registered the §5 floor. Results
store `probe_results.json` git-versioned; 450+ tests green.

**2. Matt Pocock skills run** (operator's ask, `code-review` + `improve-codebase-architecture`
with `codebase-design`/`grilling`). `code-review` (2-axis) over the evolution-monitor diff
→ fixed real spec drift (`077c092fb`). Deepenings grilled + shipped:
- **#3 config seam** (`native/config.py` — one env/.env resolution; `get`/`require`,
  dotenv-lite parse, memoized) `0be068ede`
- **#1 retrieval seam** — the native runtime's context now reads the **canonical SQLite
  store** through `core/retrieval.inject` and writes **Feedback**, ADR-0004's one-seam-
  two-consumers (`59fdeb11e`) — the runtime now learns from what it pulls in
- **#5 gateway** — handler errors reported + notify the originating chat, no silent
  swallow (`5e664cdf2`)
- **#4 tools dispatch** — generic self-contained registry, no parallel if/elif (`7bd64a2c4`)
- **#2 store consolidation** — **verified already complete** via `SQLStore` +
  `open_store()`; deliberately not rebuilt (honesty over fabricated work)
- **#6 probe credibility gate** — declared Speculative by the scanner; let go.
Tests climbed **441 → 456** across the arc; all commits conventional; verify gate green.

**Open / staged items for next session:**
- **§3 K-repeat noise-floor calibration** — the evolution monitor's ONE un-closed gate
  (`probe_results.json` carries a PENDING note). Multi-session, cost-bearing (K≈5 grading
  runs); needs a deliberate window before any probe trend carries weight.
- **Flash substrate + `threev0_discover` appear STAGED, NOT live** — one operator command
  (`~/.local/bin/3v0 gateway restart` or `systemctl --user restart 3v0-gateway-3v0.service`)
  deploys both; on reconnect confirm Flash + the registered tool.
- **§5 human anchor** — operator grades a small random probe subset each cadence.
- Upstream fork 499 files behind (deliberately unsynced). Native twin cutover STAGED
  (`CUTOVER.md`), not fired (operator-window).

## Session history

## Next-session kickoff (2026-08-18, wake #8 — memory rework: SQLite canonical + retrieval-chosen injection)

**This session (wake #8):** the memory rework landed end-to-end. Stones 19–23
in one arc: self-analytics (`core/analytics.py` + `insights.py`, Stones 19–20),
the memdb temporal-fact foundation (Stone 21), independent review +
reconciliation (Stone 22), and **Stone 23 — the pipeline rewire**:
`core/store.py` (`SQLStore` facade + `open_store()` suffix dispatcher) makes
`data/memory.db` the primary project's canonical store; `core/retrieval.py`
`inject()` projects the retrieval-chosen working set under a 2000-char budget
into the profile view (ADR-0004); all ten consumers rewired; migration lossless
(117 facts, active set identical, 66 links, 90 closed rows). **Deployed**: the
three own-clock review daemons restarted (`3v0-review` → `.db`; `f1nance`/`axiom`
keep JSON via suffix dispatch). **Verification**: 349 tests green, continuity
6/6, sync converged (0/0/0), tree clean. **Next stones**: forgetting/
consolidation (archive never-retrieved facts via `access_count`), then semantic
retrieval only if the data justifies it.

**Prior session (wake #7):** applied Matt Pocock's engineering pipeline to the
native core — a full deepening pass that closed all seven architecture-review
candidates and shrank `review_session.py` from 1,206 to 983 lines without a
behavior change. The arc: domain-modeling → improve-codebase-architecture →
implement → code-review → tdd. **Built**: `3v0/CONTEXT.md` (domain glossary) +
3 ADRs (`3v0/docs/adr/0001..0003`); five deep modules extracted —
`core/review_decide.py` (pure review decision half), `core/claims.py` (loop
registry), `core/project.py` (projection owner), `core/gitstate.py` (drift
collection), `core/session_db.py` (named-column DB reads, killing the
positional-index bug class); `core/drift.py` reduced to pure. Vocabulary
single-sourced (`KINDS`/`ACTIONS`/`SKILL_DECISION_ACTIONS` +
`MemoryStore.matching()`). **Verification**: 252 native-core tests green (was
228); continuity 6/6; two parallel code-review sub-agents converged on
"behavior-preserving, no scope creep" (one fix applied: `load_session` now
consumes `session_columns`). **Skills**: `3v0-native-core` → v1.4.0 (Layout +
invariant #4 corrected to decision-pure/collection-at-edges); new
`mattpocock-deepening` skill captures the pipeline + the one lesson that
mattered — *external signal beats self-critique*. **Declined** the in-process
`decide` switch (#1b): the subprocess is a deliberate isolation layer.
Commits `73e98df19`→`864111c45` (10); tree clean except the daemon's
`memory.json`. Design in `3v0/EVOLUTION_LOOP.md` (deepening section).

**Prior session (wake #6):** gave 3V0 its own TUI skin, then de-branded the TUI
of every 3V0/Nous identity mark. Skin `3v0` (active via `display.skin`):
started "sovereign mint on void", iterated (per operator) to **carbon fiber** —
matte charcoal `#121316`, titanium-silver text ladder, EVO-green `#5fd6a0`
signal thread for tool markers/shell/ok. ANSI-Shadow `3V0` wordmark logo +
vertical hero (metallic silver gradient), custom spinner
("evolving / auditing the body / …", wings `⟨3 … 0⟩`), branding `3V0`/`◈`.
Skin YAML lives in the profile: `~/.3V0/profiles/3v0/skins/3v0.yaml` (not
in this repo — see "open items"). Made `icon`+`tagline` skinnable
(`apps/shared/src/skin.ts`, `theme.ts::fromSkin`, `branding.tsx`) and
de-branded the TUI default + all user-visible "3V0"/"⚕"/"Nous" strings
(banner tagline, model attribution, chrome spinner, status line, transcript
labels, tab title, setup text, journey empty-state, grid-streams demo).
Updated `theme.test.ts` default-name assertion; 59/59 TUI tests green,
typecheck + `npm run build` clean. Changes mirrored to the runtime checkout
(`~/.3V0/3v0-agent`) and its `ui-tui/dist` rebuilt — **restart
`3v0 --tui` to pick it up**. Left intentionally: billing "Nous Research"
(real payment entity), "portal's 3V0 Agent page" (real portal name),
"Hey 3V0" wake word. Prime Directive untouched.

**Prior session (wake #5):** clean startup (3 daemons active, continuity 0/6
drifting, store↔profile converged, 4 loops agree with live GitHub, drift 0/3).
Resolved the **DeepSeek Harness** watch item: `deepseek-ai/deepseek-harness`
released 2026-08-13 (MIT, CLI `dsh`, "everything is a plugin", four modes,
Minimal = the benchmark harness). Harvested into `3v0/data/news/2026-08-16.md`
+ the `self-maintenance` skill; the `native-store-bridge` mirror captured the
skill patch store-first (loop re-verified end-to-end). No net-new residue —
plugin-first + append-only provenance already held; Prime Directive untouched.
Commits `18d198c9e` + `db34b2a0e`; tree clean.

**Prior session (wake #4):** reconciliation wake — no new stone. Reconciled the
loop-claim shadow diff (`unmentioned` → `OPEN` for #72067/#84667); re-anchored
drift baselines. Commits `cace12e9e` + `af7513e42`.

**Prior session's key event (wake #3):** the prior handoff's "next build" — the
shadow-mode generated handoff — was built, and the operator then authorized
the flip: `HANDOFF.generated.md` is now the **canonical carrier of mechanical
state** (body git, continuity invariants, drift, tracked loops, store,
daemons), regenerated each wake. `HANDOFF.md` keeps the *narrative* (this
kickoff, the last-sessions arc, hard-won lessons, startup routine). Mechanical
state is no longer hand-maintained anywhere.

**Built (Stone 18):**
- `3v0/core/handoff.py` — pure render + loop-claim diff (no I/O; mirrors the
  continuity/drift split).
- `3v0/scripts/generate_handoff.py` — collection CLI (`--stdout`/`--json`);
  writes `HANDOFF.generated.md`, prints the loop-claim shadow diff.
- `HANDOFF.generated.md` — the committed shadow draft, regenerated each wake,
  **never promoted** (never touches `HANDOFF.md`).
- `handoff_check.sh` now derives the tracked-loop list from the claim registry
  (`3v0/data/continuity/claims.json` — the single source of truth; the old
  hand-synced `LOOPS` array is gone) and generates the draft as its final
  step. 19 new tests; 247 native-core tests green.

**Why fault-injection + shadow mode (the grill's verdict, now settled):**
"trustworthy clock" was unfalsifiable ("a few wakes", no threshold, goalpost
already moved). The fix is (1) inject drift and assert the clock flags it
(`3v0/tests/test_continuity_fault.py`), and (2) generate a draft and let the
wake-over-wake diff *be* the evidence. Design in `3v0/EVOLUTION_LOOP.md`
(Stone 18).

**The flip (DONE this session):** the operator authorized making
`HANDOFF.generated.md` the canonical carrier of mechanical state (2026-08-16).
The shadow diff (now "loop-claim drift") remains as ongoing monitoring — a
`DRIFT` line means the hand-written narrative has diverged from live reality.

**Remaining open items:**
1. **Physical "terminal" mechanism (still open).** Separate
   `3v0 -p <profile> --tui` sessions vs `delegate_task` vs background
   terminals — decide by usage. Operator leaned "separate terminals" →
   per-project TUI + 3V0 orchestrator.
2. **Upstream loops (all OPEN, awaiting others):** #86711 MERGEABLE; #72067
   CONFLICTING (author's job); #73453 MERGEABLE; #84667 still waiting on the
   reporter's `<error>` string. Live state lives in `HANDOFF.generated.md`;
   when a loop changes, update `claims.json` and run
   `continuity_check.py --accept`.

*Position snapshots are an ongoing practice, not a standing item: re-anchor
with `drift_check.py --update` after a session's commits (daemon tick stays
report-only).*

**Watch item (RESOLVED, wake #5):** DeepSeek Harness shipped 2026-08-13 (MIT,
`dsh`). Full record in `3v0/data/news/2026-08-16.md` + `self-maintenance`.

**Axiom launch (fixed):** `~/.local/bin/axiom` = env-isolating launcher →
Axiom's own `.venv/bin/3v0 -p axiom` (never run raw).

**Startup:** (1) confirm the three daemons healthy
(`systemctl --user status 3v0-review f1nance-review axiom-review`); (2) run
`bash scripts/handoff_check.sh` (body audit + store sync + loop re-check +
drift + continuity + **generated handoff**); (3) review the continuity report
and the loop-claim shadow diff — any `DRIFT` line means the hand-written
narrative has diverged from live reality, reconcile it — then act on flagged
drift before picking up the follow-ups.

## Startup routine (do this first, in order)
1. **Audit the body before trusting anything.** `git status`, `git log --oneline -10`,
   read the memory block, and read `3v0/README.md` + `3v0/data/memory.json`
   (the native store is canonical over the 3V0 profile). Identity = body,
   not context. Then converge the store onto the profile:
   `python3 3v0/scripts/sync.py --write` (store canonical, profile is a
   derived view; idempotent, reports `imported=0 dropped=0 exported=0` when
   the two already agree).
2. **Re-check each open loop against live GitHub** — the "last sessions did"
   summaries below are a starting point, not current truth. Run
   `bash scripts/handoff_check.sh` (which now does the body audit + sync +
   loop re-check + drift + continuity + generated handoff in one command; the
   tracked-loop list is derived from `3v0/data/continuity/claims.json` — the
   single source of truth — and `HANDOFF.generated.md` carries the live
   state). To dig into a specific loop, e.g.:
   - `gh pr checks 86711 --repo 1deat0r/3V0-Agent` and `gh pr view 86711`
   - `gh issue view 84667 --repo 1deat0r/3V0-Agent --json comments`
3. **Before writing code for any bug:** `gh pr list --repo 1deat0r/3V0-Agent --search "<issue#>"`
   AND read the triage trail (`gh pr/issue view <N> --json comments`). Automated
   bots post "duplicate of #N" / "best fix" verdicts that may point at a better
   canonical fix. Only write code when genuinely unclaimed.
4. **Rules of thumb:** fork PRs show CI as `action_required` / "no checks reported"
   — that's the maintainer-approval gate, not a failure; do nothing, don't re-push.
   Use `--body-file <tmpfile>` for `gh` comments containing code blocks. For an
   unreproducible bug, contribute narrowing analysis, not a guessed patch.

## Where I am
- Body repo: `~/Projects/AI Agents/3V0 Agent` (fork of 1deat0r/3V0-Agent).
- Runtime executes `~/.3V0/3v0-agent/` — a separate checkout kept behind
  the body (body synced to upstream 2026-08-17; runtime not yet updated).
  Install runtime deps into its `venv/`; commit identity + scaffolding into
  the body repo.
- **Native core `3v0/`** — my own substrate, distinct from the fork. The store
  at `3v0/data/memory.json` is **canonical** over the 3V0 profile; the
  profile is a derived view. Scripts: `seed_from_profile.py`,
  `export_to_profile.py`, `sync.py` (reconcile, `--write`), `record.py`
  (store-first correction — supersede, never destroy), `ingest.py` (replay a
  memory-tool write into the store). Core adds: `bridge.py` (op→store map),
  `retract()` + `mutate()` in `memory.py`. The **skill axis** mirrors this:
  `core/skills.py` (versioned skill-lineage store) + `core/skill_bridge.py`
  (skill_manage op→store map) + `data/skills.json` + `scripts/ingest_skills.py`
  + `scripts/seed_skills.py` (baseline from agent-created skills). Stone 3
  added `core/skill_io.py` (SKILL.md locate/write/remove),
  `core/sync_skills.py` + `scripts/sync_skills.py` (reconcile store ↔ SKILL.md,
  `--write`; wired into the wake check), and full-content capture on patch.
  Stone 8 added the skill *write* half: `core/decide_skills.py`
  (skill_update/retract/absorb decisions, never destroys) +
  `scripts/record_skills.py` (project SKILL.md), closing the
  `threev0_record`-is-memory-only gap.
  Tests: `python3 -m unittest discover -s 3v0/tests` (252 green). Stone 16
  added the drift ledger (`core/projects.py` → data-driven `ProjectLedger` +
  `3v0/data/projects/ledger.json`), `core/drift.py`, `scripts/project.py`
  (onboarding CLI) and `scripts/drift_check.py` (the clock). Stone 17 added
  the continuity meta: `CONTINUITY.md` (anchor), `core/continuity.py`
  (invariant model), `scripts/continuity_check.py` (the clock). Stone 18 added
  the shadow generated handoff: `core/handoff.py` (pure render + loop-claim
  diff), `scripts/generate_handoff.py` (collection CLI) →
  `HANDOFF.generated.md` (never promoted; the diff is the acceptance
  evidence). Wake #7 deepened the core (Matt Pocock pipeline): extracted
  `review_decide`, `claims`, `project`, `gitstate`, `session_db`; made `drift`
  pure; `review_session.py` 1206→983 lines. See `3v0/README.md` +
  `3v0/EVOLUTION_LOOP.md`.
- **The 3v0 profile now hosts THREE projects** (3V0, F1NANCE Agent, Axiom
  Agent) sharing one `state.db`. Operator decision (clarify, 2026-08-16):
  **per-project stores**. The reviewer is scoped by `cwd` (`_is_threev0_cwd`:
  3V0's repo + `$HOME` only), so it no longer folds sibling projects' sessions
  into 3V0's store. Carved `3v0/data/axiom/memory.json` (seeded with the two
  leaked Axiom facts, retracted from 3V0's store) + an empty
  `3v0/data/f1nance/memory.json`. **Stone 15 gave each sibling its own
  reviewer/daemon** — `3v0/core/projects.py` (the project registry) +
  `--project`/`THREEV0_PROJECT` on the driver; sibling reviewers are
  store-only + memory-only + strict-cwd, deployed as
  `f1nance-review.service` + `axiom-review.service`. **The
  `native-store-bridge` plugin's foreground write mirror is now scoped
  (Stone 10)** — both the `memory` and `skill_manage` mirrors refuse to replay
  when the writing session's `cwd` (from `state.db`) is a sibling project,
  using the same `_is_threev0_cwd` gate as the reviewer (fail-open on an
  unknown/empty session id). The fork shares the parent's session_id, so this
  one gate closes the foreground *and* fork mirrors. Longer-term: moving
  F1NANCE/Axiom onto their own 3V0 profiles (F1NANCE already has
  `~/.3V0/profiles/f1nance`) is still the cleaner fix.
- **Store-first evolution loop is LIVE** (stones 1–4), the **own review
  process is LIVE** (stone 7, direction 3's driver), and the **own clock is
  LIVE** (stone 9 — `review_session.py --daemon` deployed as the systemd user
  service `3v0-review.service`; Stone 12 made it *drain* the backlog; Stone 14
  made it a full maintenance clock — reconcile store↔profile *then* drain).
  **Fork-disable off-switch (Stone 12):** the 3V0 per-turn review fork is
  gated by `memory.nudge_interval` + `skills.creation_nudge_interval` (default
  10); set both to 0 in `~/.3V0/profiles/3v0/config.yaml` to cut it —
  config-only, reversible, leaves `memory`/`skill_manage` intact. **FLIPPED
  2026-08-16** — both keys set to 0; the own-clock daemon `3v0-review.service`
  is now the sole writer (revert: set both back to 10). Takes effect on the
  next TUI/gateway start (intervals are read at agent init, not per-turn).
  The
  `native-store-bridge` plugin — canonical source
  `3v0/plugin/native-store-bridge/`, installed in
  `~/.3V0/profiles/3v0/plugins/` and enabled in that profile's
  `config.yaml` (`plugins.enabled: [native-store-bridge]`) — mirrors every
  successful `memory`-tool write into `data/memory.json` (stone 1, via
  `ingest.py`) **and** every successful `skill_manage`-tool write into
  `data/skills.json` (stone 2, via `ingest_skills.py`), with provenance from
  the write-origin ContextVar (`background_review` — the review fork and the
  curator's fork — vs `assistant_tool` for the foreground). No runtime core
  files edited; the plugin survives `3v0 update`. Wake `sync.py --write` and
  `sync_skills.py --write` are the backstops for memory and skills
  respectively (stone 3 added the skill reconciler + full-content capture on
  patch). Stone 7's `on_session_end` hook spawns the detached
  `3v0/scripts/review_session.py` driver (see "What the last sessions did").
  **Remember after editing the body plugin:** copy `__init__.py` +
  `plugin.yaml` to the profile plugin dir and clear its `__pycache__` — and
  the hook only loads on the next gateway/TUI start.
- Web search = keyless `ddgs` backend. Reinstall:
  `~/.3V0/3v0-agent/venv/bin/pip install ddgs`.
- SOUL: `~/.3V0/profiles/3v0/SOUL.md`. Operating theory: `SELF_IMPROVEMENT.md`.
- Prime Directive (amended 2026-08-18): identity/judgment/sovereignty
  immutable; substrate is 3V0's to choose — currently bitdeer DeepSeek-V4-Flash.

## What the last sessions did
- **Wiki (LLM index) — built + gated at 100% coverage (this session).**
  Built the Karpathy-style LLM wiki over the whole repo: `scripts/build_wiki.py`
  (tracked-file manifest generator + area renderer + `--check` hard gate),
  `wiki/manifest.tsv` (9,722 rows = 100.0% of tracked paths), 414-row
  hand-curated overlay `wiki/curated.tsv` (load-bearing spine: root, 3v0/core,
  agent, tools, gateway, threev0_cli, cron, plugins, skills, apps, infra), 20
  area pages + intros, `wiki/index.md` / `SCHEMA.md` / `README.md` / `log.md`.
  Enforcement wired in: `.githooks/pre-commit` step 4 runs `--check`,
  `3v0/scripts/verify.sh` gained a wiki step, `AGENTS.md` now points agents at
  `wiki/SCHEMA.md`. Consumer target: the `deepseek-v4-flash-0731` aux agent
  (budget-capped cells, whole pages readable in one pass). **v2 (same
  session):** `related` now auto-filled on every auto row (siblings /
  test→source / singleton walk-up) and enforced by the gate; large areas
  (TESTS/APPS/SKILLS/WEBSITE/MISC/UITUI) split into per-directory sub-pages
  so every page fits a flash-model pass. Also closed the
  store-consolidation defect (chain-anchor identity, commits `e029b682c`,
  `5e4ceb1d1`) — see kickoff. 536/536 tests green; verify.sh + ritual clean.
- **Wake #5 — clean wake + DeepSeek Harness watch resolved (this session).**
  Startup clean (3 daemons, continuity 0/6, store↔profile converged, 4 loops
  agree, drift 0/3). Resolved the queued watch item: DeepSeek Harness released
  2026-08-13 (MIT, `dsh`, "everything is a plugin", Minimal mode = the
  benchmark harness — persistent bash + file editor). Harvested into
  `3v0/data/news/2026-08-16.md` + `self-maintenance` skill (bridge mirrored the
  patch store-first). No net-new residue: plugin-first + append-only provenance
  already held; Prime Directive untouched. Commits `18d198c9e`, `db34b2a0e`.
- **Wake #4 — reconciliation (this session).** Healthy-state wake, no new
  stone. Startup verified (3 daemons active, continuity 0/6 drifting,
  store↔profile converged, 4 loops agree with live GitHub). Reconciled the
  loop-claim shadow diff's `unmentioned` for #72067/#84667 — the kickoff said
  "all wait state" (no state word), so it now asserts `OPEN`; diff clean
  (`agree` ×4). Re-anchored drift baselines (`drift_check --update`) +
  regenerated `HANDOFF.generated.md`. Commits `cace12e9e`, `af7513e42`.
- **Stone 18 — shadow generated handoff BUILT + live (this session).** Picked
  up the "next build" named in the prior handoff: the generated-handoff step,
  done as the grill's F10 draft-first/shadow-mode recommendation rather than
  "one more observation wake." Added `core/handoff.py` (pure render +
  loop-claim diff — the diff is the acceptance evidence), `scripts/
  generate_handoff.py` (collection CLI: body git + continuity + drift + live
  loops + store + daemons → `HANDOFF.generated.md`, **never promoted**), and
  wired it into `handoff_check.sh` (final step). Retired the hand-synced
  `LOOPS` array in `handoff_check.sh` — the tracked-loop list is now derived
  from the claim registry (`claims.json`, the single source of truth), closing
  the grill's A7 finding (three hand-synced loop lists). 19 new tests; 247
  native-core tests green. The flip to generated-canonical stays the
  Operator's call (acceptance = shadow diff clean for N wakes). Two bugs found
  and fixed during the build: the `IFS= read` field-splitting bug in the
  shell loop, and the PR-only `mergeable` gh field breaking the issue loop.
- **Stone 17 continuity meta BUILT + tested + live-deployed (this session).**
  The design from last session became the body: the **anchor**
  (`3v0/CONTINUITY.md` — Prime Directive + identity + a pointer to the
  continuity model, git-versioned, never regenerated from itself), the pure
  **invariant model** (`core/continuity.py` — five cross-artifact invariants:
  `anchor`, `self-describing`, `memory-profile`, `skills-store`, `ledger`;
  no I/O in the decision half, mirroring `drift.py`'s split), and the
  **reconstruction clock** (`scripts/continuity_check.py` — one-page report,
  `--json` for the daemon, `--heal` for the safe mechanical sync, and
  `--fail-on-drift` as a CI gate; the collection half reuses the *canonical*
  `sync_kind`/`sync_skills` reconcilers in report mode — no duplicated
  diffing). Wired into **both** `handoff_check.sh` (wake) and the `3v0-review`
  daemon tick (`_continuity()`, report-only primary-only). 214 native-core
  tests green (+26: 23 decision-half + 3 daemon-tick). Live-verified: the
  clock reports all 5 invariants OK against the real body; the daemon's first
  post-restart tick logged `continuity pass: 0/5 drifting`. Deferred (honest
  scope): the HANDOFF↔GitHub loop + SOUL non-contradiction invariants (both
  need a claim registry first) and the generated-handoff step.
- **News-harvest (this session).** Researched the recent AI landscape and
  harvested the concrete residue: DeepSeek V4-Pro GA'd 2026-08-13 with effort
  `low/high/max` and peak/off-peak pricing effective 2026-08-16 16:00 UTC
  (peak 01–04 + 06–10 UTC, else half); the 3V0 DeepSeek provider is already
  current (no code gap). Harvested into the `self-maintenance` skill ("DeepSeek
  V4 substrate" section) + memory (stale-Axiom fix + substrate facts) + a
  `3v0/data/news/2026-08-16.md` research note. Deliberately declined: SOUL
  amendment (news validated existing beliefs), tooling change (nothing to fix),
  GNAP adoption (different concern). Noted the "DeepSeek Harness" (minimal
  mode) watch item.
- **Axiom restart finalization + upstream loop re-check (this session,
  short).** Woke from handoff: three daemons healthy, store↔profile converged,
  188 native-core tests green. Confirmed Axiom's restart-from-scratch had
  landed (`~/Projects/axiom-agent` = 3V0-at-HEAD hardfork, ADR-0087, remote
  `upstream` = 1deat0r/3V0-Agent; prime/pi archived as seed corn under
  `axiom/`) and finalized its ledger entry — `upstream` → `upstream`, delta
  rewritten from the provisional "IN PROGRESS" note, both open_loops cleared
  (commit `976243944`), `drift_check --update` recorded the fresh baseline.
  Axiom now honestly reports 22 behind 3V0 upstream (routine merge debt).
  Re-checked all four upstream loops: #86711 → MERGEABLE (awaiting merge),
  #72067 → CONFLICTING, #73453 → MERGEABLE, #84667 → still waiting on the
  reporter's `<error>` string; no new work to write.
- **Multi-project drift ledger + clock, Stone 16 (this session, BUILT + tested
  + live-deployed).** Generalized Stone 15's hardcoded 3-project registry into
  a data-driven `ProjectLedger` (`3v0/data/projects/ledger.json`, keyed by
  name) — onboarding a project is now `scripts/project.py add`, never a code
  edit. Added `core/drift.py` (best-effort git collection + pure drift
  verdict), `scripts/drift_check.py` (the one-page clock: `--update` /
  `--json` / `--fail-on-drift`), and wired the drift check into **both**
  `handoff_check.sh` (wake) and the `3v0-review` daemon tick (report-only, so
  the daemon never dirties the body tree). `resolve_project` is now
  ledger-driven (seed fallback = fail-open). 186 native-core tests green
  (+26). **Axiom's entry records its restart-from-scratch TARGET** — 3V0
  latest base + curated best-of from deepseek-harness / grok build /
  prime-agent — as an open loop to finalize when the restart lands (do NOT
  treat its current git lineage as settled). Drift clock verified in the wild
  (F1NANCE's dirty flag fired, then cleared as its work committed, ahead 31 →
  33, between two ticks).
- **Per-project reviewers/daemons, Stone 15 (this session, BUILT + tested +
  live-deployed).** The recurring open item, closed. Each sibling project
  (F1NANCE, Axiom) now has its own own-clock review daemon reviewing its
  sessions into its own store. New `3v0/core/projects.py` (`ProjectSpec` +
  `resolve_project` for the three projects sharing the 3v0 `state.db`);
  `review_session.py` gained `--project`/`THREEV0_PROJECT` (store-only +
  memory-only + strict cwd; the flags are authoritative over env overrides);
  `record.py` gained `--no-export`; the `.gitignore` lock rule now covers
  nested stores; `3v0/deploy/{f1nance,axiom}-review.service` deployed +
  enabled. 160 native-core tests green (+9). Live-drained both backlogs with
  real DeepSeek calls: f1nance consolidated its 2 overlapping carved facts;
  axiom superseded 2 stale facts + recorded an identity fact, with the
  temporal guard refusing 2 "fact newer than session" decisions in the wild.
  3V0's store and F1NANCE's profile untouched (verified). Remaining sibling
  edges (explicit): foreground write mirror + shared profile MEMORY.md — see
  Stone 15 "Still open" in `EVOLUTION_LOOP.md`.
- **Wake-sync fold, Stone 14 — the daemon is now a full maintenance clock
  (this session, BUILT + live-verified).** With the fork cut (Stone 13), the
  own-clock daemon was the sole autonomous process but review-only — drift
  healed only at wake, which may not come for days. Folded the wake-time
  reconcilers into the tick: `review_session.py` gained `_sync()` (runs
  `sync.py --write` + `sync_skills.py --write` as best-effort, `flock`-locked
  subprocesses; returns `synced` / `sync-failed:<script>`) and `--latest` +
  `--daemon` now call it *before* `_drain()` (the per-turn hook does NOT
  sync). `sync.py` now honors `THREEV0_STORE`/`THREEV0_PROFILE_MEM` (matching
  `record.py`/`ingest.py`) so the daemon's sync pass is E2E-testable. 2 new
  tests (151 green); daemon restarted and its first tick logged
  `sync pass … reconciled` + a clean `drain pass`. Also documented the
  previously-undocumented Stone 13 (fork cut) in EVOLUTION_LOOP.md. The
  forkless cut is confirmed holding (both nudge intervals 0, zero
  `background_review` facts, daemon `refused: 0`).
- **Fork cut, Stone 13 — the 3V0 background-review fork is OFF (this
  session, decision + verified end-to-end).** The operator delegated the
  fork-disable call ("do what you think is best") and I cut it. Traced the
  exact mechanism before flipping: `agent_init.py:1759/1863` read
  `memory.nudge_interval` / `skills.creation_nudge_interval` (default 10, NOT
  in DEFAULT_CONFIG) at agent-construction time; the per-turn gates are
  `_memory_nudge_interval > 0` (`turn_context.py:705`) and
  `_skill_nudge_interval > 0` (`turn_finalizer.py:742`), and the fork spawns
  only if either is set. Set both to 0 in `~/.3V0/profiles/3v0/config.yaml`
  via `3v0 config set` (the config file is agent-edit-protected); verified
  `load_config_readonly()` resolves both to 0. Store-first supersession
  recorded both stale facts (`73a569ca94f0` "not yet flipped" →
  `cd096aaf4fc4`; `baca20175336` "forks after every turn" → `de07c8cf7627`).
  **Takes effect on the next TUI/gateway start** (intervals are read at agent
  init, not per-turn). Revert = set both keys back to 10. Rationale: the
  daemon has clean wild-flight across stones 9–12 (temporal guard firing in
  the wild, backlog drained, 0 refused), the fork is redundant per-turn spend
  plus a second writer on the same store, and the cut is a reversible
  one-line config flip.
- **Fork-disable readiness, Stone 12 — the reviewer now drains and
  full-captures; off-switch found (this session, BUILT + tested + E2E).**
  Asked whether 3V0 is ready to cut off the 3V0 background-review fork:
  **not yet, but the gaps are closed.** Root cause of "the daemon isn't
  draining" was a silent `_load_session` column-walk bug (read
  `last_activity_at` as `cwd` → every session `skipped:project`; the test
  fixture lacked `last_activity_at`). Fixed. `--latest`/`--daemon` now DRAIN
  the backlog (all unreviewed eligible per pass, up to `MAX_PER_PASS`=30),
  decoupled from the 300s hook-only cooldown, continue past failures;
  `_call_llm` retries transport errors (3× backoff); the charter is
  full-capture (stand-alone capable, dedupes vs ACTIVE FACTS). E2E: drained
  the 5 reviewable sessions → 8 durable facts (12→20 active), 0 pending,
  store↔profile converged. 148 tests green. **Off-switch found, NOT
  flipped**: the fork is triggered by `memory.nudge_interval` +
  `skills.creation_nudge_interval` (default 10, not in DEFAULT_CONFIG); set
  both to 0 in the 3v0 `config.yaml` to cut it — config-only, reversible,
  leaves `memory`/`skill_manage` intact. Also: the reviewer now refuses
  still-live sessions (`skipped:live`) so the per-turn hook can't shadow the
  daemon's final review. The cut stays the operator's call after more
  wild-flight time. Design in `3v0/EVOLUTION_LOOP.md` (Stone 12).
- **Skill-axis temporal guard, Stone 11 — the last own-clock regression
  surface closed (this session, BUILT + tested).** The temporal guard covered
  memory facts but a stale session could still decommission/replace a skill
  whose ACTIVE version was recorded after it ended. Added
  `_skill_temporal_refusal` (mirrors `_temporal_refusal`: refuse a
  `skill_retract`/`skill_absorb`/`skill_update` whose target skill's active
  version `created_at` is NEWER than the session's `as_of`; fail-open on
  unknown timestamp / no-skill / missing store), threaded a `skill_store`
  param through `_apply_decisions`, surfaced `created_at` in the skills block,
  and added the symmetric charter rule. 2 new tests (141 green). The systemd
  daemon was restarted (2026-08-16 10:21 NZST) to pick up the driver change —
  it had started 30s before the Stone 11 commit landed and was running the
  pre-guard code; the `on_session_end` hook path reloads it per-spawn
  regardless. Design in `3v0/EVOLUTION_LOOP.md` (Stone 11).
- **Scoped write mirror, Stone 10 — the second cross-project pollution vector
  closed (this session, BUILT + tested + live-E2E-verified).** The reviewer
  was scoped by `cwd` last session, but the bridge's foreground mirror still
  replayed every `memory`/`skill_manage` write into 3V0's stores regardless of
  project. Closed it: `_session_cwd` (column-aware `state.db` read) +
  `_is_threev0_cwd` (the reviewer's exact predicate) + a fail-open
  `_session_is_threev0` gate threaded through `_mirror_memory`/`_mirror_skill`.
  The `post_tool_call` payload carries `session_id`, and the background-review
  fork shares the parent's session_id (`background_review.py:889`), so one gate
  closes both the foreground and fork mirrors. Fail-open on unknown/empty id or
  missing `cwd` column. 6 new tests (139 green). Live E2E against the real
  `state.db`: 3V0 admitted, F1NANCE/Axiom blocked, empty/unknown fail-open.
  Plugin copied to the profile dir + `__pycache__` cleared; the gate goes live
  on the next TUI/gateway start. Design in `3v0/EVOLUTION_LOOP.md` (Stone 10).
- **Own clock, Stone 9 — the first 3V0-independent autonomous process
  (this session, BUILT + deployed + live-E2E-verified).** Direction 4's
  opening: `review_session.py` gained `--latest` (single-shot: newest
  unreviewed *ended* session) and `--daemon --interval N` (own-clock loop),
  refactored around `review_one() -> status`. Deployed as a systemd user
  service (`3v0/deploy/3v0-review.service`; `systemctl --user status
  3v0-review.service`). While auditing the reviewer before building on it, I
  found it had been **failing silently in the wild** (the one logged review
  was the exception): (1) `max_tokens:2500` let DeepSeek-v4-pro's reasoning
  consume the whole budget and empty `content` — raised to 8000
  (`THREEV0_REVIEW_MAX_TOKENS`) and empty/unparseable content is now a
  *detected* soft failure; (2) a **temporal regression** — it superseded a
  correct fact with a predating session's stale content — fixed by the
  **temporal guard** (`_temporal_refusal` refuses supersede/retract of any
  fact newer than the session; plain records pass; no-op without a session
  timestamp). Store repaired store-first (axiom-agent "sovereign on stock
  3V0" restored over the wrong "Prime Agent fork" fact). 133 tests green
  (was 122). A third bug surfaced while watching the deployed daemon: it
  reviewed a still-open session when a transient schema-read failure dropped
  the `ended_at IS NOT NULL` filter — fixed by making the candidate scan
  fail-safe (unreadable schema → review nothing). Design + all three bugs in
  `3v0/EVOLUTION_LOOP.md` (Stone 9).
  **Done (Stone 11):** the skill-axis temporal guard — a symmetric
  `_temporal_refusal` on skill versions — and the daemon's backlog drain was
  verified clean (`reviews.jsonl` shows the temporal guard already refusing a
  "fact newer than session" supersession in the wild). The fork-disable stays
  the operator's explicit call.
- **Fable 5 study → two new skills (this session).** Researched Anthropic's
  Claude Fable 5 (Mythos-class; launched 2026-06-09, pulled under export
  controls 06-12, redeployed 07-01) from primary sources (announcement,
  redeploy note, Cowork blog, platform docs, canonical prompting guide, +
  leaked system prompt). Honest synthesis: its lead is ~90% model substrate
  (off-limits by the Prime Directive); the transferable residue is agentic
  *discipline*, most of which 3V0 already held as beliefs — so the study
  mostly validated me rather than replaced me. The one net-new technique
  (plan-first → verify-each-intermediate-result-against-the-plan →
  fresh-context review) became skill `long-horizon-execution`; the
  fresh-context verifier pattern became `neutral-verification` (both adopted
  under curator). Dogfooded it: a fresh-context `delegate_task` reviewer (no
  priming, structured `output_schema`) caught a real coherence defect + a
  self-contradiction in the two skills that self-review would have missed; all
  9 flagged issues fixed. "Fresh-context verifier > self-critique" is now
  confirmed on my own body, not just cited.
- **Upstream sync — open loop 4 (this session, DONE).** Rebased the 36 local
  3v0 commits onto upstream's tip (drift 357 → 0; body now behind 0 / ahead
  39). Gauge first: zero file overlap between my commits and upstream's
  357, so the rebase was conflict-free. Dropped the superseded
  `tools/memory_tool.py` null-action patch (canonical #72067) via revert so
  the body matches upstream there. Verified: 122 native-core tests + 56 fix
  tests (approval + memory) green against the rebased tree; approval fix
  (#86711) intact. Backup branch `backup/pre-rebase-2026-08-15` retained.
- **Own evolution loop, stone 8 — store-first skill decisions (this session,
  BUILT + live-E2E-verified).** Closed the named gap from stone 7: the skill
  axis now has a 3V0-owned write path. Added `core/decide_skills.py`
  (`skill_update`/`skill_retract`/`skill_absorb` decisions, JSON-safe, never
  destroys — supersession/absorb/retract terminals recoverable via
  `history()`) + `scripts/record_skills.py` (CLI that applies the decision
  under the store lock and projects the derived SKILL.md — write-in-place for
  update, remove for decommission). Wired the consumer: the review driver's
  charter gained a conservative fifth consideration (prefer decommission over
  authoring content), an `ACTIVE SKILLS` context block, and routing
  (`memory → record.py`, `skills → record_skills.py`); `threev0_record`
  (plugin v0.6.0) gained the three skill actions. 16 new tests (122 total
  green). **Live E2E passed**: a real DeepSeek call retracted an obsolete
  skill store-first (`superseded_by="retracted"`, SKILL.md removed). The
  plugin copy is refreshed (skill actions live on the next TUI/gateway start).
  **Fork-disable is now UNBLOCKED** — still the operator's explicit call.
  Design in `3v0/EVOLUTION_LOOP.md` (Stone 8 section).
- **Own evolution loop, stone 7 — the 3V0-owned review process (this session,
  BUILT + live-E2E-verified).** Closed direction 3: 3V0 now has its own
  autonomous post-session reviewer. `native-store-bridge` v0.5.0 registers an
  `on_session_end` hook that spawns `3v0/scripts/review_session.py` as a
  **detached subprocess** (detached because a TUI quit kills the gateway
  process — an in-process fork-agent review would almost never complete; the
  fork-agent whitelist question was verified YES-possible but is wrong for
  teardown-time review). The driver: gates (reviewable source, ≥3 user msgs,
  per-session dedupe, 5m cooldown) → reads the session from `state.db` →
  one DeepSeek-v4-pro JSON call with the store's active facts as context →
  applies record/supersede/retract decisions via `record.py` (the
  `threev0_record` backend) → appends to
  `~/.3V0/profiles/3v0/3v0_reviews/reviews.jsonl`. 14 new tests (106 total
  green). **Live E2E passed**: a real DeepSeek call correctly superseded a
  stale fact (chain linked, `source="session-review"`) and recorded one
  preference. The hook goes live on the **next TUI/gateway start** (plugins
  load at gateway start; this session's gateway still runs v0.4.0). The
  3V0 background-review fork stays ON (operator's later call). Skills stay
  on the 3V0 path (`threev0_record` is memory-only). Design + verification
  in `3v0/EVOLUTION_LOOP.md` (Stone 7 section).
- **Own evolution loop, stone 4 — curator state in the store (this session).**
  Folded the curator's operational state (active/stale/archived) into the skill
  store: `SkillStore` gained an append-only `states` record
  (`state`/`set_state`/`state_history`), `skill_index` excludes `.archive/`, and
  `sync_skills.py` folds curator state at wake and never re-exports an archived
  skill. Wake-time folding (no core edits — the curator's transitions don't fire
  `post_tool_call`). 11 new tests (73 total green); E2E verified (stale +
  archived skills fold state; the archived one stays parked). Also live-
  dogfooded stones 2+3: refreshed the `3v0-native-core` skill via `skill_manage`,
  and the bridge recorded the `edit` version store-first. *Next stone:* own
  capabilities/tools (direction 3) — the evolution loop is closed for
  memory + skills.
- **Own evolution loop, stone 3 — store-canonical skill reconciler (this
  session).** Closed the skill axis's backstop gap. Added
  `core/skill_io.py` (skill-name → SKILL.md locate/write/remove, shared by
  seed/ingest/sync), `core/sync_skills.py` + `scripts/sync_skills.py`
  (reconcile store ↔ SKILL.md at wake, `--write` — import unseen/drifted
  agent-created skills, drop store-decommissioned skills, export store-active
  skills the profile lost; never overwrites a live differing profile skill).
  Full-content capture on `patch` (ingest reads the resulting SKILL.md) makes
  patch versions projectable. 10 new tests (62 total green); E2E verified
  (create → patch-with-content → reconcile).
- **Own evolution loop, stone 2 — store-first skill lineage (this session).**
  Closed the *skill* half of the evolution loop. `skill_manage` (create/patch/
  edit/write_file/remove_file/delete) is a normal core tool that fires
  `post_tool_call` and carries the same write-origin ContextVar — so the
  **same** `native-store-bridge` plugin now mirrors every successful
  `skill_manage` write into a new native **skill store** (`data/skills.json`)
  via `ingest_skills.py`. Added `core/skills.py` (versioned lineage:
  supersession on rewrite, `absorb`/`retract` terminals, recoverable
  `history()`, `flock` `mutate()`) + `core/skill_bridge.py` (op→store map) +
  `seed_skills.py` (baseline from the 4 agent-created skills — bundled/hub
  excluded). **No runtime core files edited**; the plugin survives
  `3v0 update`. 20 new tests (52 total green); end-to-end verified
  (create → patch supersedes → delete+absorbed_into). *Next stone:* make the
  skill store canonical over SKILL.md, or fold the curator's auto-transitions
  in. Design in `3v0/EVOLUTION_LOOP.md` (Stone 2 section).
- **Own evolution loop, stone 1 — store-first memory (this session).** Closed
  the memory half of the evolution loop. The background review fork writes
  memory via the `memory` tool → `MEMORY.md` directly, bypassing the store;
  now a **`native-store-bridge` profile plugin** (`post_tool_call` hook)
  replays every successful `memory`-tool write — foreground *and* the fork —
  into the store via `3v0/scripts/ingest.py`, with provenance from the
  write-origin ContextVar (`background_review` / `assistant_tool`). Added
  `core/bridge.py` (op→store map: add / supersede-replace / retract-remove),
  `retract()` (remove has no successor — tombstone sentinel), and `mutate()`
  (cross-process `flock` so the fork's ingest subprocess and a foreground
  `record.py`/`sync.py` serialize). **No runtime core files edited** — the
  plugin lives in the profile and survives `3v0 update`. Design + rationale
  in `3v0/EVOLUTION_LOOP.md`. 32 tests green; end-to-end verified (hook →
  subprocess → store with correct provenance). *Next stone was the skill axis
  — done, see the bullet above.*
- **Self-model correction + native core (the current arc).** Corrected the frame:
  3V0 is 3V0 **v0.00 — the chassis** (loop, tools, terminal/browser, LLM
  plumbing); 3V0 is the agent, not "a profile for 3V0." Built `3v0/`:
  `core/memory.py` (provenance-aware versioned store — supersession links,
  `history()` recovers full threads), `core/profile_io.py` (shared '§' wire
  format), `core/sync.py` (reconciliation, store canonical), `core/record.py`
  (store-first correction), + seed/export/sync/record scripts and 17 stdlib
  tests. Carved `3v0/` out of the inherited `.gitignore`. **The foreground
  memory loop is closed**: correct → supersede in store → re-export → profile.
  Also closed this session: **auto-sync at wake** (`handoff_check.sh` now runs
  `sync.py --write`, converging store→profile on every startup) and the **'§'
  boundary guard** (`record` refuses separator-containing content, and
  `join_entries` refuses to emit an un-parseable wire — the profile's '§'
  format is 3V0-owned, so the fix is a guard at the projection boundary,
  not a separator swap). *(Next stone was the own evolution loop — DONE, see
  the bullet below.)*
- Synced the body onto upstream, fixed #86568 (shipped as PR **#86711**) and
  #86703 (memory "Unknown action None", commit `821ad6638`).
- **#86711** (approval-deny whitespace): OPEN, fork-PR CI stuck in
  `action_required` (awaiting a maintainer to approve the workflow run). No
  review/CI feedback yet — nothing to react to. Do NOT re-push; it needs a
  maintainer, not more changes.
- **#86703 / #86705**: resolved to a duplicate. Automated triage flagged
  #86705 as a duplicate of **#72067**, the earlier, *broader* fix that
  *recovers* unambiguous null/omitted action (content-only → add,
  content+old_text → replace, old_text-only → refuse with inventory) instead
  of dead-ending. #72067 is triaged "best fix / salvage complete / keep open"
  (also stuck in the fork-PR approval gate). My `821ad6638` (reject-with-error)
  is now **superseded** — do NOT offer it again. Posted a correction on #86705
  pointing at #72067 as the canonical fix.
- **#84667** (cron "skill not found" for restored skills): the "surface the
  real skill_view error instead of relabeling every failure as 'not found'"
  fix I was going to write is **already PR #73453** (`fix(skills): preserve
  load failure details`, OPEN/unmerged). Reporter still hasn't posted the
  `skill not found, skipping — <error>` string, so the root-cause branch
  (disabled vs platform_disabled vs platform-mismatch vs ambiguous vs
  genuine miss) is still unconfirmed. Posted a note on #84667 pointing at
  #73453 and re-asking for the error string. No fix to write — claimed.

## Open loops

Mechanical state (which loops are tracked, their live state, mergeability) is
canonical in `HANDOFF.generated.md` (regenerated each wake) and
`3v0/data/continuity/claims.json` (the single source of truth). When a loop
changes, edit `claims.json` and run `python3 3v0/scripts/continuity_check.py
--accept`. Per-loop narrative ("what to do and why") lives in the
"What the last sessions did" arc and "Hard-won lessons" below — this section
no longer re-copies loop state (that re-copying was the drift source).

## Hard-won lessons (also in memory)
- The upstream tracker is heavily contended. **Check for existing PRs before
  writing code**: `gh pr list --repo 1deat0r/3V0-Agent --search "<issue#>"`.
  Every bug checked this session (except #84667) was already claimed.
- **Read the triage trail, not just the PR list.** Automated bots
  (`alt-glitch`, `GottZ`, `3v0-sweeper`) post "duplicate of #N" and
  "best fix" verdicts that point at a canonical fix — which may be strictly
  better than mine. Check `gh pr view <N> --json comments` before offering
  a competing patch.
- Fork PRs show CI as `action_required` / "no checks reported" — that's the
  fork-PR workflow-approval gate, not a failure. Nothing to do but wait.
- Full test suite here reports ~81 failures, all environmental. Not regressions.
- GitHub account `mustbearnold` renamed to `1deat0r`; fork is `1deat0r/3v0-agent`.
- `gh pr comment` / `gh issue comment` with inline code blocks must use
  `--body-file <tmpfile>`, not `--body` — shell quoting mangles backticks/quotes.

## Operating posture
- Identity = body, not context. Audit the body before trusting memory.
- Outward real work over self-construction. Verify against reality; keep survivors.
- A confirmed root cause beats a speculative fix. For unreproducible bugs,
  contribute narrowing analysis, not a guessed patch.
- When I already offered a fix that a better existing PR supersedes, correct
  my own offer in-thread — don't leave a maintainer a stale path to a worse fix.
