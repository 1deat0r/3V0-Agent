# docs/ + README* + CONTRIBUTING* — documentation

Docs content: `docs/` (ADRs, RFCs, design, security, kanban, contracts like relay-connector and managed-cron), plus repo-root docs (README*, CONTRIBUTING*, SECURITY*, AGENTS.md, HANDOFF.md).
---
Auto-rendered from `wiki/manifest.tsv` — `python3 scripts/build_wiki.py --rebuild` regenerates.
Columns: path · kind · purpose · why · related

| path | kind | purpose | why | related |
|------|------|---------|-----|---------|
| `.env.example` | config | Example secrets file (.env is for secrets ONLY) | Documentation of every credential the body can use; non-secrets belong in config.yaml | ev0_cli/config.py |
| `AGENTS.md` | doc | The body's governance + contribution contract (3V0 sovereignty, footprint ladder, testing policy) | Constitutional doc; every AI assistant working here is bound by it | wiki/SCHEMA.md;3v0/SOUL.md;3v0/CONTEXT.md |
| `CONTRIBUTING.md` | policy-doc | Contribution guide (full engineering standards) | Merging law for the repo | AGENTS.md;CONTRIBUTING.es.md |
| `HANDOFF.md` | doc | Manual session handoff — the operator's narrative continuity document | Tracked continuity artifact; regenerated draft lives in HANDOFF.generated.md (gitignored) | 3v0/data/continuity/claims.json;3v0/scripts/generate_handoff.py |
| `LICENSE` | doc | License text | Legal basis for distribution | README.md |
| `README.md` | readme | Project README (English) | for humans/new agents | README.es.md;README.zh-CN.md;README.ur-pk.md;CONTRIBUTING.md |
| `SECURITY.md` | policy-doc | Security policy + reporting | Public security contract | SECURITY.es.md;.coderabbit.yaml |
| `SELF_IMPROVEMENT.md` | policy-doc | Self-improvement doctrine (quality loops, verify.sh culture) | Policies the body's own evolution | 3v0/EVOLUTION_LOOP.md;3v0/scripts/verify.sh |
| `SUSTAINABILITY.md` | policy-doc | Cost-efficiency doctrine for LLM spend | Guides token-efficiency; pairs with 3v0/TOKEN_EFFICIENCY.md | 3v0/TOKEN_EFFICIENCY.md;sustainability/ |
| `docs/3v0-kanban-v1-spec.pdf` | doc | 3V0 kanban shared spec (PDF) | Kanban contract artifact | plugins/kanban |
| `docs/ADR.md` | doc | Architecture Decision Records index | Design rationale ledger | docs/rfcs;docs/design |
| `docs/billing-lifecycle.md` | doc | Billing lifecycle doc | Account/billing | agent/billing_view.py |
| `docs/chronos-managed-cron-contract.md` | doc | Managed cron contract | Scheduled tasks spec | cron/scheduler_provider.py |
| `docs/design/kanban-dialogs/index.html` | asset | File `index.html` | Repository content; see related files / area page for the enclosing subsystem | docs/design/kanban-dialogs/ |
| `docs/design/profile-builder.md` | doc | Profile Builder — Dashboard-Native, Full-Featured Profile Creation | Human/agent-readable documentation; the wiki keeps it pointer-capped | docs/design/kanban-dialogs/index.html |
| `docs/kanban/multi-gateway.md` | doc | Multi-gateway deployment | Human/agent-readable documentation; the wiki keeps it pointer-capped | docs/kanban/ |
| `docs/micro-compaction.md` | doc | Micro-compaction design | Context compaction rationale | scripts/micro_compaction_report.py |
| `docs/middleware/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents | docs/middleware/ |
| `docs/observability/README.md` | readme | README (en) | Project introduction & quickstart for humans/new agents | docs/observability/monitoring.md; docs/observability/relay-shared-metrics.md |
| `docs/observability/monitoring.md` | doc | Gateway Monitoring | Human/agent-readable documentation; the wiki keeps it pointer-capped | docs/observability/README.md; docs/observability/relay-shared-metrics.md |
| `docs/observability/relay-shared-metrics.md` | doc | NeMo Relay Shared Metrics | Human/agent-readable documentation; the wiki keeps it pointer-capped | docs/observability/README.md; docs/observability/monitoring.md |
| `docs/profile-routing.md` | doc | Profile routing design | Multi-instance routing | gateway/profile_routing.py;agent/secret_scope.py |
| `docs/rca-ssl-cacert-post-git-pull.md` | doc | RCA: SSL CA certs after git pull | Postmortem lesson | tests/gateway/ |
| `docs/relay-connector-contract.md` | doc | Relay connector contract | Cross-process relay spec | agent/relay_llm.py |
| `docs/rfcs/2026-07-plugin-architecture-lessons-pi-opencode.md` | doc | Research spike: plugin-architecture lessons from Pi and OpenCode | Human/agent-readable documentation; the wiki keeps it pointer-capped | docs/rfcs/plugin-config-state-bridge.md |
| `docs/rfcs/plugin-config-state-bridge.md` | doc | Plugin Config & State Bridge | Human/agent-readable documentation; the wiki keeps it pointer-capped | docs/rfcs/2026-07-plugin-architecture-lessons-pi-opencode.md |
| `docs/security/network-egress-isolation.md` | doc | Network Egress Isolation for Docker Deployments | Human/agent-readable documentation; the wiki keeps it pointer-capped | docs/security/ |
| `docs/session-lifecycle.md` | doc | Session lifecycle doc | Messaging sessions | gateway/session.py |
| `docs/streaming-tts.md` | doc | Streaming TTS doc | Voice streaming | tools/tts_streaming.py |
