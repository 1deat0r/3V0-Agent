# scripts/ — dev/test/ops tooling

Dev/test/ops tooling: `run_tests.sh` (the only sanctioned test runner), `run_tests_parallel.py`, `handoff_check.sh` (the whole-body wake ritual), `build_wiki.py` (this wiki's generator+gate), CI jobs, release, sandbox, observability helpers.
---
Auto-rendered from `wiki/manifest.tsv` — `python3 scripts/build_wiki.py --rebuild` regenerates.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `scripts/3v0-gateway` | source | Gateway launcher scripts for 3V0 | Body gateway deployment | 3v0/scripts/reload_gateway.sh |
| `scripts/LIVETEST_README.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `scripts/add_contributor.py` | source | Add a contributor email → GitHub login mapping. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/analyze_livetest.py` | test | Compare enabled vs disabled runs and produce a readable report. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `scripts/audit_pr_attribution.py` | source | Audit (and auto-fix) contributor email mappings for a PR branch. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/benchmark_browser_eval.py` | source | Quick benchmark: subprocess eval vs supervisor-WS eval. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/build_model_catalog.py` | source | Model catalog builder | Catalog maintenance | agent/model_metadata.py |
| `scripts/build_skills_index.py` | source | Build the Hermes Skills Index — a centralized JSON catalog of all skills. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/build_wiki.py` | script | The wiki generator — tracked-file manifest, area pages, --check gate | Keeps the wiki at 100% coverage; run --rebuild on change, --check in CI | wiki/;.githooks/pre-commit |
| `scripts/capture-cage-terminal.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `scripts/check-windows-footguns.py` | source | Grep-based checker for Windows cross-platform footguns. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/check_subprocess_stdin.py` | source | Check that subprocess calls in TUI-context code specify stdin=. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/ci/assemble_review_comment.py` | script | Assemble the unified CI review comment for a pull request. | Dev/ops/release tooling invoked from the command line or CI |  |
| `scripts/ci/classify_changes.py` | script | Classify a PR's changed files into CI work lanes. | Dev/ops/release tooling invoked from the command line or CI |  |
| `scripts/ci/e2e_screenshot_status.py` | script | Select Desktop E2E visual evidence and build its CI review status. | Dev/ops/release tooling invoked from the command line or CI |  |
| `scripts/ci/emit_review_status.py` | script | Emit review_status JSON for the review-labels workflow. | Dev/ops/release tooling invoked from the command line or CI |  |
| `scripts/ci/list_os_marked_tests.py` | script | List the test files that carry a given OS marker. | Dev/ops/release tooling invoked from the command line or CI |  |
| `scripts/ci/live_comment.py` | script | Live-updating CI review comment. | Dev/ops/release tooling invoked from the command line or CI |  |
| `scripts/ci/lockfile_diff.py` | script | Semantic diff of npm ``package-lock.json`` files for PR comments. | Dev/ops/release tooling invoked from the command line or CI |  |
| `scripts/ci/publish_e2e_evidence.py` | script | Publish validated E2E evidence as GitHub attachments and update its PR comment. | Dev/ops/release tooling invoked from the command line or CI |  |
| `scripts/ci/test_install_ps1_path_migration.ps1` | asset | File `test_install_ps1_path_migration.ps1` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/ci/timings_report.py` | script | Collect CI job/step timings from the GitHub API and generate an HTML diff report. | Dev/ops/release tooling invoked from the command line or CI |  |
| `scripts/contributor_audit.py` | source | Contributor Audit Script | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/desktop-update.ps1` | asset | File `desktop-update.ps1` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/desktop-update/posix.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `scripts/desktop-update/repro.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `scripts/desktop-update/serve-ui.py` | script | Loopback shim server for the desktop update hand-off. | Dev/ops/release tooling invoked from the command line or CI |  |
| `scripts/desktop-update/ui.html` | asset | File `ui.html` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/desktop-update/windows.ps1` | asset | File `windows.ps1` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/dev-sandbox.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `scripts/discord-voice-doctor.py` | source | Discord Voice Doctor — diagnostic tool for voice channel support. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/docker_config_migrate.py` | source | Run Docker boot-time config migrations safely. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/docker_rebootstrap_nous_session.py` | source | Boot-time re-seed of a terminally-dead Nous bootstrap session. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/generate_conformance_vectors.py` | source | Conformance-vector generator — the native adapters as executable spec. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/handoff_check.sh` | script | The whole-body wake ritual — continuity, sync, drift, analytics, insights, coherence+coalesce, handoff | The standing loop the 3V0 wake gate runs | 3v0/scripts/continuity_check.py;3v0/scripts/coherence_coalesce.py |
| `scripts/install.cmd` | asset | File `install.cmd` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/install.ps1` | asset | File `install.ps1` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/install.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `scripts/install_psutil_android.py` | source | Install psutil on Termux/Android by patching upstream platform detection. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/iso-certify.py` | source | iso-certify — AC-4 dashboard turn-isolation certify harness. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/keystroke_diagnostic.py` | source | Diagnose how prompt_toolkit identifies keystrokes in the current terminal. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/kill_modal.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `scripts/lib/node-bootstrap.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `scripts/lint_diff.py` | source | Diff ruff + ty diagnostic reports between two git refs. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/micro_compaction_report.py` | source | Summarize micro-compaction telemetry from Hermes logs. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/observability/gateway_health_export_probe.py` | script | Exercise Gateway Health & Diagnostics Export against a local OTLP capture collector. | Dev/ops/release tooling invoked from the command line or CI |  |
| `scripts/observability/otel_capture_collector.py` | script | Tiny local OTLP/HTTP capture collector for Hermes gateway health smoke tests. | Dev/ops/release tooling invoked from the command line or CI |  |
| `scripts/profile-tui.py` | source | Drive the Hermes TUI under HERMES_DEV_PERF and summarize the pipeline. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/release.py` | source | Release automation | Versioning/tagging | pypi: pyproject.toml |
| `scripts/run_tests.sh` | source | The ONLY sanctioned test runner (CI-parity env, file retries, subprocess isolation) | Direct pytest diverges from CI; use this always | tests/;scripts/run_tests_parallel.py |
| `scripts/run_tests_parallel.py` | source | Per-file subprocess test isolation runner | No cross-file state leakage | scripts/run_tests.sh |
| `scripts/sample_and_compress.py` | source | Sample & compress tooling | for dataset/context experiments | agent/context_compressor.py |
| `scripts/sandbox/openssl.cnf` | asset | File `openssl.cnf` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/sandbox/pick-release-tags.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `scripts/sandbox/proxy.py` | script | MITM proxy backing the dev sandbox's fake Internet. | Dev/ops/release tooling invoked from the command line or CI |  |
| `scripts/sandbox/ssh-shim.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `scripts/sandbox/stage2-run.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `scripts/smoke_nemo_relay_shared_metrics.py` | source | Run a real Hermes CLI turn and validate the Relay shared-metrics output. | Python module executed or imported by the runtime; check git intent before deleting |  |
| `scripts/tests/test-install-ps1-gitbash-compatibility.ps1` | asset | File `test-install-ps1-gitbash-compatibility.ps1` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/tests/test-install-ps1-longpath.ps1` | asset | File `test-install-ps1-longpath.ps1` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/tests/test-install-ps1-stage-protocol.ps1` | asset | File `test-install-ps1-stage-protocol.ps1` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/tool_search_livetest.py` | test | Live test harness for Hermes Agent's Tool Search feature. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `scripts/tool_search_livetest2.py` | test | Tool Search live benchmark v2 — real token accounting + more scenarios + reps. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `scripts/tool_search_livetest_ue.py` | test | Live benchmark v3: Epic Unreal Engine 5.8 MCP surface (830 REAL schemas), replayed. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `scripts/tool_search_livetest_ue_disc.py` | test | Live benchmark v5 — DISCOVERY-BOUND tasks at 830 tools. Opus 4.8, bridge vs listing. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `scripts/tool_search_livetest_ue_hard.py` | test | Live benchmark v4 — ADVERSARIAL Unreal tool selection at 830 tools. | Test module — asserts the repo contract; run via scripts/run_tests.sh |  |
| `scripts/toolperf_abeval/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents |  |
| `scripts/toolperf_abeval/ab_eval.py` | script | Hard A/B evaluation for core-toolset changes: baseline vs fixes. | Dev/ops/release tooling invoked from the command line or CI |  |
| `scripts/toolperf_abeval/run_all.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `scripts/whatsapp-bridge/allowlist.js` | asset | File `allowlist.js` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/whatsapp-bridge/allowlist.test.mjs` | asset | File `allowlist.test.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/whatsapp-bridge/bridge.js` | asset | File `bridge.js` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/whatsapp-bridge/bridge.native.test.mjs` | asset | File `bridge.native.test.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/whatsapp-bridge/bridge.reconnect.test.mjs` | asset | File `bridge.reconnect.test.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/whatsapp-bridge/bridge.sendqueue.test.mjs` | asset | File `bridge.sendqueue.test.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/whatsapp-bridge/bridge_helpers.js` | asset | File `bridge_helpers.js` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/whatsapp-bridge/outbound_ids.js` | asset | File `outbound_ids.js` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/whatsapp-bridge/outbound_ids.test.mjs` | asset | File `outbound_ids.test.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/whatsapp-bridge/owner_message_gate.js` | asset | File `owner_message_gate.js` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/whatsapp-bridge/owner_message_gate.test.mjs` | asset | File `owner_message_gate.test.mjs` | Repository content; see related files / area page for the enclosing subsystem |  |
| `scripts/whatsapp-bridge/package-lock.json` | lockfile | Generated dependency lockfile | Pins every transitive dep with hashes (supply-chain invariant); regenerated by uv/npm |  |
| `scripts/whatsapp-bridge/package.json` | build | Node package manifest | Declares JS workspace deps + scripts |  |
