# Browser tooling research — 2026-08-17 (self-improvement)

Operator-directed research pass on agent browser tools; outcome = permanent
capability upgrades, not notes-only.

## What changed (permanent)

1. **New skill `browser-automation`** (profile skills, software-development):
   the canonical browser_exec workflow (AX tree → DOM.getBoxModel →
   click_at_xy → verify), React-safe `fill_input`, dropdown taxonomy +
   re-measure/hit-test discipline, `upload_file` via CDP, SPA waiting,
   coordinate traps, verification loop. Reference:
   `references/2026-08-browser-tools-research.md` (repo table + 10 lessons).
2. **Reusable `agent_helpers.py`** written to the harness agent workspace —
   auto-loaded into every browser_exec call (`helpers._load_agent_helpers`).
   Helpers: `fresh_rect` (live re-query + scrollIntoView), `click_fresh`,
   `visible_option` (width>5 + elementFromPoint hit-test), `click_option`,
   `set_select`, `fill_by_index`, `set_checkbox`, `close_menus`, `state_of`.
3. **Memory** updated with the browser-exec mastery facts.

## Repos mined

browser-use/browser-use · browser-use/browser-harness (the tool we actually
run — helpers.py read in full) · vercel-labs/agent-browser · trycua/cua ·
microsoft/playwright · plus: browserbase/stagehand, Skyvern-AI/skyvern,
steel-dev/steel-browser, browserbase/open-operator, nanobrowser,
browserable, vostride/agent-qa, steel-dev/awesome-web-agents (the map).

## The 10 lessons that mattered (condensed)

1. AX tree (role/name/backendDOMNodeId) is the reliable element finder.
2. Box-model quad → click_at_xy; negative/oversized = scroll first.
3. Real CDP input (press_key/click_at_xy/fill_input) beats synthetic events on React.
4. fill_input = focus → Ctrl+A → Backspace → real keys → input+change.
5. Re-measure rects after ANY open/scroll/render; stale coords click wrong.
6. elementFromPoint before clicking dropdown options (menus overlap triggers,
   render behind fields).
7. upload_file = CDP setFileInputFiles — no upload-UI fight.
8. wait_for_load misses SPAs; wait_for_element(visible=True) + network_idle are real.
9. Screenshots are device px; clicks are CSS px (divide by devicePixelRatio).
10. agent_helpers.py auto-loads — write each hard-won pattern once.

## Direct application

Fiverr gig wizard: use fill_by_index/fresh_rect/set_select/click_option instead
of the coordinate-grind that cost ~25 calls; upload gallery covers with
`upload_file`; advance steps with real clicks + wait_for_network_idle.
