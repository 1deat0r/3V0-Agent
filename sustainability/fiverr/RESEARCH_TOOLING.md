# Fiverr gig-filling tooling research (2026-08-17)

Research into tools / tooling / GitHub projects to fill out + run the Fiverr
gigs easier or better. **Verdict: no new dependency needed — the attended
shared-browser (CDP) pattern is the answer, and this session already has it.**

## What does NOT exist

- **No public Fiverr API** for gig creation/management. Gig creation is a
  logged-in web flow only; there is no sanctioned seller API to automate.

## What exists and helps

- **Attended CDP browser (the answer).** A real Chrome window the human logs
  into — and can take over at any point — while the agent drives it over CDP
  to fill forms. Already available here as `browser_exec` (Browser Use CLI).
  The DeepSeek Harness ecosystem independently confirms the pattern:
  `dsh-builtin-browser` ("a visible browser window the human can take over,
  driven by the agent over CDP") and `dsh-computer-use` (text-first CDP,
  doesn't steal the pointer). Keep credentials with the human; automate only
  the form-filling.
- **Playwright / raw CDP** for a self-run script if the operator prefers to
  keep full control of the browser (higher detection risk than attended).

## Traps (ban risk — do NOT use)

- **Rank-manipulation Chrome extensions** — "Fiverr Seller Assistant",
  "Smart Fiverr" ("daily Gig favorites, clicks and impressions") fake
  engagement → rank manipulation → ban. Avoid.
- **Headless automation** of the seller dashboard is more detectable than an
  attended browser session.
- **Third-party reply bots** — already flagged unauthorized in
  `COMPETITOR_ANALYSIS.md` §8.6.

## Environment note

The prior Fiverr session ran inside **DeepSeek Harness** (`dsh`,
`npx @deepseek-ai/dsh web`, "everything is a plugin", Cordis). This session is
the 3V0 TUI (Hermes runtime) — same work, different harness. No switch needed:
the browser tool here is equivalent. (dsh ecosystem tracked at
`0xsline/awesome-deepseek-harness`; browser plugins under its
"Browser & Remote" section.)

## Confirmed walls (prior session + this one)

- `curl` on fiverr.com → 403 (Cloudflare bot-wall). Use the browser.
- `browser_exec` → Chrome raises an "Allow remote debugging?" popup; the
  operator must click **Allow** once, then the session persists.
