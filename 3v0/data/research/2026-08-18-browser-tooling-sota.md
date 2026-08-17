# Browser Tooling SOTA for Agents — 2026-08-18

Research mandate: map the entire `browser-use` GitHub org, all repos, and the
current state-of-the-art for agent browser tooling as of **August 18, 2026**.
Goal: replace the fragile click-by-coordinate browser_exec workflow with the
right harness so Fiverr gig-filling (and all future browser work) stops
tripping detection and stops wasting turns.

## Executive verdict

The tooling that solves this already exists and is **2 days old**: the
browser-use org shipped **`browsercode` (bcode)** on 2026-08-16 — a
browser-native agent (OpenCode fork) that drives a real Chrome over
unconstrained CDP, supports **DeepSeek as a provider**, writes reusable
scripts as it works, and has a TUI you can steer. That is the direct answer
to "why can't you use a browser-harness like this does."

My current stack (browser_use 0.13.8 + browser-harness 0.1.9 via browser_exec)
IS the right substrate — but I've been using it like a raw CDP scripting
layer (coordinate clicks, ad-hoc helpers) instead of the harness's designed
loop (agent-workspace/agent_helpers.py self-healing + domain skills + full
agent loop). Both the substrate and the *usage pattern* need to change.

## 1. browser-use org — all 51 repos (updated 2026-08-16)

| Repo | Stars | What it is | Relevance |
|---|---|---|---|
| browser-use | 109,486 | Python lib: LLM agent loop over Playwright/CDP; BU Bench #1, 89.1% WebVoyager, #1 Odysseys 87.4% | Core library |
| browser-harness | 16,736 | Self-healing CDP harness; agent writes helpers to agent-workspace; domain skills | **Current substrate (0.1.9 installed)** |
| browsercode | 289 | **NEW 2026-08-16** — browser-native agent (OpenCode fork), unconstrained CDP, TUI, any model incl. DeepSeek | **The SOTA answer** |
| terminal | 621 | Rust TUI for browser agents; new LLM harness "2x cheaper, 2x faster than Browser Harness" | Alternative harness |
| workflow-use | 4,134 | Deterministic RPA 2.0 workflows w/ browser-use fallback | Repetitive gigs later |
| video-use | 20,889 | Video editing with coding agents | Not now |
| web-ui | 16,282 | Run AI agent in browser | Not now |
| sdk | 21 | Browser Use Cloud SDK | Cloud path |
| cdp-use | 310 | Type-safe CDP client generator | Deep-dive CDP |
| bux | 416 | 24/7 Claude Code + browser on a $5 VPS, Telegram-driven | Future always-on |
| desktop | 660 | Desktop app: cookies→fresh Chromium, keyboard-shortcut tasks | Operator-facing |
| browser-harness-js | 478 | JS harness: 56 domains, 652 typed wrappers, zero wrapping | JS agents |
| agent-sdk | 685 | "An agent is just a for-loop" minimal framework | Learning |
| benchmark | 116 | Stealth Bench V1 (71 tasks), BU Bench (100 tasks), official plots | Ground truth |
| browser-harness-tui | 1 | Codex CLI forked + embedded as browser-harness agent | Niche |
| n8n-nodes-browser-use, plugin-marketplace, plugins, eve, browser-agent-template, browser-use-examples, stress-tests, template-library, gemini-demo, browser-use-node/python, go-harnessless, mix-eval-go, qa-use, vibetest-use, macOS-use, contact-use, docs, ... | — | Ecosystem/niche |

Key structural facts:
- browser-harness SKILL.md is the canonical usage doc: heredoc invocation
  (`browser-harness <<'PY' ... PY`), helpers pre-imported, AX-tree-first
  element discovery, `new_tab()` for first navigation, cloud browsers for
  parallel/stealth work, `--doctor` for diagnostics.
- install.md fast path: `uv tool install --python 3.12 --upgrade --force
  browser-harness`, then `browser-harness skill` to register the skill.
- 16 interaction-skills: dropdowns, uploads, tabs, scrolling, iframes,
  shadow-dom, dialogs, drag-and-drop, downloads, viewport, screenshots,
  profile-sync, cross-origin-iframes, network-requests, print-as-pdf,
  make-video. These are the reusable recipes I should have been loading.

## 2. browsercode (bcode) — the 2026-08-16 SOTA

- One-line install: `curl -fsSL https://bcode.sh/install | bash` → `bcode`.
- `bcode` (TUI) or `bcode run "<task>"` (headless).
- "Drives real browsers through unconstrained CDP. The agent adapts to every
  site at runtime and writes scripts to reuse later." — literally the
  self-improvement loop the Fiverr task needs.
- **Providers: "any model you can reach with an API key, plus every provider
  OpenCode supports."** DeepSeek is an OpenCode-supported provider (per
  deepseek-ai/awesome-deepseek-agent), so bcode satisfies the Prime
  Directive (DeepSeek API only, never local).
- Recommended models from BU Bench evals: claude-opus-4-8 (best),
  kimi-k3 (best open-weight), gpt-5.6-luna xhigh (best value). DeepSeek
  V4-Pro is not listed on the banner but is connectable via OpenCode's
  DeepSeek provider.
- "Connect to my current tab" — it can take over the operator's real Chrome
  tab (same attended-browser model we use now).

## 3. SOTA landscape, August 2026 (third-party verified)

Frameworks (intelligence layer):
- **Browser Use** — 89.1% WebVoyager (highest verified open-source),
  #1 Odysseys leaderboard 87.4% average ahead of OpenAI/Anthropic/Google/
  Microsoft computer-use agents; BU Bench V1 = 100 real tasks. ~$0.07/10-step
  task on their model; hybrid DOM+vision architecture (2.0).
- **Skyvern** — 85.85% WebVoyager; best on form-filling; vision-only, no
  selectors; native 2FA/TOTP; $29/mo entry.
- **Stagehand** — TypeScript, drop-in Playwright enhancement, action caching
  cuts tokens, MIT.
- **Playwright MCP** — free, sub-100ms actions, ships with GitHub Copilot.
- **Agent Browser** — CLI-first browser control, 35k stars.

Infrastructure (browser layer):
- Firecrawl (Browser Sandbox), Browserbase, Steel, Browserless, Hyperbrowser,
  Anchor, Kernel, Browser Use Cloud. Cloud = stealth proxies + CAPTCHA
  solving + parallel sessions — the escape hatch when local Chrome keeps
  getting PerimeterX-walled.

Architectures: DOM+AX parsing (Playwright MCP), vision (Skyvern/Operator/
Claude Computer Use), hybrid (Browser Use 2.0). Hybrid is the sweet spot.

## 4. What this means for the Fiverr workflow (and all future browser work)

Root causes of the last session's pain, mapped to fixes:

1. **Fragile coordinate clicking** → bcode's agent loop finds elements via
   the harness (AX tree + self-healing helpers), not my hand-rolled
   click_at_xy chains. Or: use browser-harness properly with the
   interaction-skills as the recipe set.
2. **PerimeterX repeated walls** → the operator's local Chrome is flagged
   after bursts of CDP automation. Options: (a) bcode/harness human-paced
   pacing built in; (b) Browser Use Cloud browser (clean IPs + stealth) for
   the gig-filling runs — the org's own docs recommend cloud browsers for
   bot-sensitive sites; (c) keep the attended browser for login-only steps.
3. **Tab/typing mishaps** → harness owns tab management (`new_tab`/`switch_tab`
   attach without stealing focus; `activate_tab` only when needed).
4. **Upload/order bugs** → uploads.md interaction skill has the CDP
   setFileInputFiles recipe; the harness keeps agent_helpers.py persistent.

Recommended migration (in order):
1. **Install bcode** (`curl -fsSL https://bcode.sh/install | bash`), configure
   DeepSeek provider (api.deepseek.com), and drive the remaining Fiverr gigs
   with `bcode` — it does the learning and script-writing itself.
2. **Keep browser-harness upgraded** (0.1.9 → latest) and load the
   interaction-skills before browser work.
3. If local Chrome keeps getting walled: use a **Browser Use Cloud browser**
   (free tier: 3 concurrent, proxies, CAPTCHA solving) for the bulk form
   filling; keep local for the logged-in account steps.
4. Codify all of this into the `browser-automation` skill.

## Sources

- api.github.com/orgs/browser-use/repos (51 repos, 2026-08-18 pull)
- browser-use/browser-harness README + SKILL.md + install.md + interaction-skills listing
- browser-use/browsercode README + install.sh + DeepWiki getting-started
- browser-use/{terminal,workflow-use,cdp-use,browser-harness-js,bux,desktop,agent-sdk,benchmark,browser-use-python} READMEs
- firecrawl.dev/blog/best-browser-agents (2026-06-16, updated)
- awesomeagents.ai/tools/best-ai-browser-automation-tools-2026 (2026-04-19)
- deepseek-ai/awesome-deepseek-agent (README, 2026-08-17)
- browser-use/browser-use README (BU Bench, Odysseys leaderboard)
