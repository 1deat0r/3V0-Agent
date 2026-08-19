# docker/ nix/ .github/ packaging — deployment & CI

Deployment/CI/packaging: Dockerfile + docker/, nix/, .github, pyproject.toml (upper-bound pins are policy), uv.lock, the CLI launcher, and the bytecode fingerprint.
---
Auto-rendered from `wiki/manifest.tsv` — `python3 scripts/build_wiki.py --rebuild` regenerates.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `.github/ISSUE_TEMPLATE/bug_report.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/ISSUE_TEMPLATE/config.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/ISSUE_TEMPLATE/feature_request.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/ISSUE_TEMPLATE/setup_help.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/PULL_REQUEST_TEMPLATE.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `.github/actions/detect-changes/action.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/actions/get-app-token/action.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/actions/nix-setup/action.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/actions/retry/action.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/dependabot.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/ci-review-comment.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/ci.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/contributor-check.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/deploy-site.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/docker-lint.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/docker.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/docs-site-checks.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/e2e-desktop.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/history-check.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/infographic-check.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/install-e2e-run.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/install-e2e.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/installer-tests.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/js-autofix.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/js-tests.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/label-rerun.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/lint.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/lockfile-diff.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/osv-scanner.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/publish-e2e-evidence.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/review-labels.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/skills-index-freshness.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/skills-index.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/supply-chain-audit.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/tests-os.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/tests.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `.github/workflows/uv-lockfile-check.yml` | config | YAML configuration | Declarative config for deployment/CI/tooling |  |
| `3v0-cli` | script | Launcher script for the 3v0 CLI | Thin exec shim so `3v0 --tui` etc. work from PATH | ev0_cli/main.py;run_agent.py |
| `Dockerfile` | build | Container image definition (+ multi-stage build) | Dockerized deployment for the gateway/CLI | docker/;docker-compose.yml |
| `constraints-termux.txt` | asset | File `constraints-termux.txt` | Repository content; see related files / area page for the enclosing subsystem |  |
| `docker/SOUL.md` | doc | Documentation page | Human/agent-readable explanation; knowledge layer |  |
| `docker/cont-init.d/015-supervise-perms` | asset | File `015-supervise-perms` | Repository content; see related files / area page for the enclosing subsystem |  |
| `docker/cont-init.d/02-reconcile-profiles` | asset | File `02-reconcile-profiles` | Repository content; see related files / area page for the enclosing subsystem |  |
| `docker/entrypoint-dispatch.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `docker/entrypoint.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `docker/hermes-exec-shim.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `docker/main-wrapper.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `docker/s6-rc.d/dashboard/dependencies.d/base` | asset | File `base` | Repository content; see related files / area page for the enclosing subsystem |  |
| `docker/s6-rc.d/dashboard/finish` | asset | File `finish` | Repository content; see related files / area page for the enclosing subsystem |  |
| `docker/s6-rc.d/dashboard/run` | asset | File `run` | Repository content; see related files / area page for the enclosing subsystem |  |
| `docker/s6-rc.d/dashboard/type` | asset | File `type` | Repository content; see related files / area page for the enclosing subsystem |  |
| `docker/s6-rc.d/main-3v0/dependencies.d/base` | asset | File `base` | Repository content; see related files / area page for the enclosing subsystem |  |
| `docker/s6-rc.d/main-3v0/run` | asset | File `run` | Repository content; see related files / area page for the enclosing subsystem |  |
| `docker/s6-rc.d/main-3v0/type` | asset | File `type` | Repository content; see related files / area page for the enclosing subsystem |  |
| `docker/s6-rc.d/user/contents.d/dashboard` | asset | File `dashboard` | Repository content; see related files / area page for the enclosing subsystem |  |
| `docker/s6-rc.d/user/contents.d/main-3v0` | asset | File `main-3v0` | Repository content; see related files / area page for the enclosing subsystem |  |
| `docker/stage2-hook.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `docker/tini-shim.sh` | script | Shell script | Shell automation invoked manually or by CI/hooks |  |
| `flake.lock` | lockfile | Nix flake lock | Pins nix derivation inputs; regenerated by nix flake lock |  |
| `flake.nix` | build | Nix flake declaration | for nix-based dev environments | nix/;flake.lock |
| `mcp_serve.py` | source | MCP server mode — expose the agent as an MCP host/server | Lets external MCP clients drive the agent; catalog + client bridging lives in tools/mcp_tool.py | tools/mcp_tool.py;tools/setup_mcp_tool.py |
| `mini_swe_runner.py` | source | Minimal SWE-bench-style evaluator harness for the agent | Runs model patch-turns against task instances for offline evals | evals/;scripts/run_tests.sh |
| `nix/3v0-agent.nix` | asset | File `3v0-agent.nix` | Repository content; see related files / area page for the enclosing subsystem |  |
| `nix/checks.nix` | asset | File `checks.nix` | Repository content; see related files / area page for the enclosing subsystem |  |
| `nix/configMergeScript.nix` | asset | File `configMergeScript.nix` | Repository content; see related files / area page for the enclosing subsystem |  |
| `nix/desktop.nix` | asset | File `desktop.nix` | Repository content; see related files / area page for the enclosing subsystem |  |
| `nix/devShell.nix` | asset | File `devShell.nix` | Repository content; see related files / area page for the enclosing subsystem |  |
| `nix/lib.nix` | asset | File `lib.nix` | Repository content; see related files / area page for the enclosing subsystem |  |
| `nix/nixosModules.nix` | asset | File `nixosModules.nix` | Repository content; see related files / area page for the enclosing subsystem |  |
| `nix/node-gyp-11-4-0-package-lock.json` | config | Structured data/config file | Persistent state or declarative config read by tooling |  |
| `nix/node-gyp-11-4-0.nix` | asset | File `node-gyp-11-4-0.nix` | Repository content; see related files / area page for the enclosing subsystem |  |
| `nix/npm-12-0-2.nix` | asset | File `npm-12-0-2.nix` | Repository content; see related files / area page for the enclosing subsystem |  |
| `nix/overlays.nix` | asset | File `overlays.nix` | Repository content; see related files / area page for the enclosing subsystem |  |
| `nix/packages.nix` | asset | File `packages.nix` | Repository content; see related files / area page for the enclosing subsystem |  |
| `nix/python.nix` | asset | File `python.nix` | Repository content; see related files / area page for the enclosing subsystem |  |
| `nix/sandbox.nix` | asset | File `sandbox.nix` | Repository content; see related files / area page for the enclosing subsystem |  |
| `nix/tui.nix` | asset | File `tui.nix` | Repository content; see related files / area page for the enclosing subsystem |  |
| `nix/web.nix` | asset | File `web.nix` | Repository content; see related files / area page for the enclosing subsystem |  |
| `package-lock.json` | lockfile | Generated dependency lockfile | Pins every transitive dep with hashes (supply-chain invariant); regenerated by uv/npm |  |
| `package.json` | build | Root npm workspace manifest | Orchestrates the JS side (ui-tui, web, apps, website) | package-lock.json;ui-tui/package.json |
| `pyproject.toml` | build | Python packaging + dependency declaration with upper-bound pins | Defines the package and the supply-chain pinning policy | uv.lock;setup.py |
| `registration_lifecycle.py` | source | Lifecycle hooks for registration/licensing flows | Registration/activation side of the product surface | ev0_cli/auth*.py |
| `setup-3v0.sh` | script | Environment bootstrap shell | Provision a working 3V0 run/dev environment |  |
| `setup.py` | build | Legacy setup shim | Compatibility entrypoint delegating to pyproject |  |
| `uv.lock` | lockfile | uv lockfile with hashes | Reproducible installs; regenerate via uv lock | pyproject.toml |
