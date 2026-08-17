# 2026-08-18 — Browser tooling SOTA: browsercode adopted

Research mandate from operator: map the entire browser-use GitHub org (all 51
repos) + current SOTA for agent browser tooling as of 2026-08-18, because the
Fiverr gig-filling session kept tripping PerimeterX and burning turns on
hand-rolled coordinate clicking.

## Findings

- browser-use org = 51 repos; the important ones: browser-use (109k⭐,
  89.1% WebVoyager, #1 Odysseys 87.4%), browser-harness (16.7k⭐, self-healing
  CDP harness — the substrate browser_exec uses), **browsercode (NEW
  2026-08-16, browser-native agent = OpenCode fork)**, terminal (Rust TUI
  harness "2x cheaper, 2x faster"), workflow-use (RPA 2.0), cdp-use (type-safe
  CDP), browser-harness-js, bux (24/7 VPS agent), desktop, agent-sdk,
  benchmark (Stealth Bench V1 + BU Bench), video-use, web-ui, sdk.
- SOTA landscape (third-party): Browser Use #1 open-source (89.1% WebVoyager),
  Skyvern best forms (85.85%), Stagehand TS, Playwright MCP free in Copilot,
  infrastructure: Firecrawl/Browserbase/Steel/Browser Use Cloud. Architectures:
  DOM+AX vs vision vs hybrid — hybrid wins.
- **The answer to "use a browser-harness like this does":** `browsercode`
  (`bcode`) — drives real Chrome over unconstrained CDP, adapts per-site at
  runtime, writes reusable scripts, supports ANY OpenCode provider including
  DeepSeek (satisfies the Prime Directive: DeepSeek API only).

## Actions

- Wrote `3v0/data/research/2026-08-18-browser-tooling-sota.md` (full repo map
  + SOTA + migration plan).
- Installed bcode 0.1.20 (`~/.bcode/bin/bcode`), configured
  `~/.config/bcode/bcode.jsonc` with `deepseek/deepseek-v4-pro` (+ flash as
  small_model). Env: DEEPSEEK_API_KEY from profile .env, DO_NOT_TRACK=1.
- **Verified live:** `bcode run "get page title of example.com"` → connected
  to the running Chrome itself (found port 9222), self-diagnosed, returned
  "Example Domain". The self-healing loop works.
- Patched `browser-automation` skill v1.1.0: bcode as preferred tool for
  fragile multi-step flows; ReactTags `clear_first=False` lesson; upload-order
  hashing verification; scrollable-dropdown inner-list scrolling; FAQ editor
  Add-vs-Update trap; reload-discards-unsaved-state.

## Next

Use `bcode run` for the remaining Fiverr gigs (AI agent is at Description &
FAQ; scraping gig + profile not started). If local Chrome keeps getting
PerimeterX-walled, switch the bulk filling to a Browser Use Cloud browser
(clean IPs + stealth) and keep local for the logged-in account steps.
