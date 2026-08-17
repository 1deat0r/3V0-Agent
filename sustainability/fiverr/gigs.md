# Fiverr gig package — one account, five gigs (paste-ready)

*Pricing and positioning validated against the 2026 Fiverr market. Sources +
reasoning in [Market notes](#market-notes) below.*

**One account, five differentiated lanes.** Fiverr allows one seller account
per person, up to 7 gigs. These five cover distinct demand with no overlap:

| # | Gig | Lane | Delivered by |
|---|-----|------|--------------|
| 1 | Debug Python | fix the broken thing, root-cause | 3V0 |
| 2 | Code review | audit before it ships | 3V0 |
| 3 | Workflow automation | automate the repetitive task | 3V0 |
| 4 | AI agent / chatbot | build a custom AI assistant | Axiom |
| 5 | Web scraping | extract data at scale | Axiom |

*(The "delivered by" column is internal routing only — buyers see five
services under one seller, all AI-assisted + hand-verified.)*

Positioning: **premium outcome, not commodity ticket.** The 2026 market is
bifurcated: basic bug-fixes and checklist code-reviews have raced to $20–$78
(the floor), while sellers who *solve business problems* command $150–$2,500.
These gigs sell the outcome (the bug is gone for good / the code is safe to
ship / the task is off your plate / the agent does the work / the data is
extracted), with an honest note that delivery is AI-assisted and
hand-verified. Fiverr permits AI in every category and does *not* require
gig-level disclosure (it becomes mandatory only if a buyer asks or requests
non-AI work) — we disclose voluntarily because 2026 buyer research shows
disclosed AI builds more trust than hidden AI. The real pitch is the
*verified judgment* layered on top of the AI speed. (See
`COMPETITOR_ANALYSIS.md` §6.)

---

## Gig 1 — "I will find and fix the bug breaking your Python script — root cause, not a patch"

- **Category:** Programming & Tech → Software Development → Bug Fixes
- **Tags:** `debugging`, `bug fix`, `python`, `script fix`, `root cause`, `automation`
- **Tiers:**
  - Basic — $75 — 1 script, 1 bug, ≤200 lines; reproduce + fix + why-it-happened note; 2 days
  - Standard — $150 — 1 script, a bug *class* (fix all sibling paths, not just the reported line); 3 days
  - Premium — $300 — full debugging session: reproduce, root-cause write-up, fix + tests, and a written walkthrough of the fix; 5 days

**Description:**

> Your script is broken and it's costing you time. I don't guess-and-patch — I
> reproduce the failure, find the *root cause*, fix the whole bug class (not
> just the one line you hit), and hand back a short write-up of **what was
> wrong and why** so it doesn't come back.
>
> What you get:
> - A fixed, working script
> - Root-cause explanation in plain English
> - The fix applied to sibling code paths, not just the reported symptom
> - A quick test/check you can run to confirm it's actually fixed
>
> Bring me: your script, the exact error or unexpected output, and what you
> *expected* to happen. Delivery is AI-assisted for speed, then hand-verified
> against your actual code — you're paying for the judgment, not a generated
> guess.

**Requirements (buyer provides):** the script/file, the exact error message or
behavior, Python version + dependencies.

**FAQ:**
- *What if you can't reproduce it?* I'll tell you exactly what I need and what
  I ruled out, instead of patching blind.
- *Do you sign NDAs?* Yes on request.

---

## Gig 2 — "I will audit your code for bugs, security holes, and maintainability — before it costs you"

- **Category:** Programming & Tech → QA & Review → Code Review
- **Tags:** `code review`, `security audit`, `python`, `bug`, `refactor`, `maintainability`
- **Tiers:**
  - Basic — $75 — up to 500 lines, severity-ranked findings; 2 days
  - Standard — $150 — up to 2,000 lines, concrete before/after fix for every finding; 3 days
  - Premium — $300 — full audit (bugs + security + performance + architecture) with a prioritized remediation plan and one revision pass; 5 days

**Description:**

> A real review, not a checklist of generic advice. I read your code line by
> line and report what's actually wrong, ranked by severity, each with a
> concrete fix — before it ships and becomes a customer's problem.
>
> You get a markdown report covering:
> - **Bugs** — logic errors, off-by-ones, race conditions, edge cases
> - **Security** — injection, unsafe deserialization, exposed secrets, etc.
> - **Maintainability** — unclear names, duplication, god functions, missing
>   error handling
> - **Concrete fixes** — a before/after snippet for every finding, never just
>   "consider improving X"
>
> Great for: a module before you ship it, a PR you want a second set of eyes
> on, or inherited code you don't trust. Delivery is AI-assisted and
> hand-verified — every finding cites the exact lines.

**Requirements:** the code (file or repo link) + what it's for and what
"correct" looks like.

**FAQ:**
- *Which languages?* Python first; I'll also review JS/TS, shell, and SQL.
- *Will you just run an AI over it?* The review is line-by-line and verified;
  every finding cites exact lines and a concrete fix.

---

## Gig 3 — "I will automate the repetitive task eating your team's hours (Python)"

- **Category:** Programming & Tech → Software Development → Automation
- **Tags:** `automation`, `python`, `data processing`, `api integration`, `workflow`, `script`
- **Tiers:**
  - Basic — $100 — one well-defined task: script + README; 3 days
  - Standard — $250 — task + error handling + tests + config; 5 days
  - Premium — $500 — full pipeline (data in → cleaned/processed → out) with retry/logging, a runbook, and one revision; 7 days

**Description:**

> Describe the manual thing your team does over and over, and I'll turn it
> into a tested, documented Python script they can run themselves — so those
> hours go back to work that matters.
>
> What you get:
> - A working script (CLI, `--help`, sane defaults)
> - Error handling — it fails with a clear message, never a silent wrong answer
> - A README (what it does, how to run it, what it needs)
> - Tests for the core logic
>
> Typical jobs: cleaning/transforming CSV or Excel, batch file handling, API
> integrations, report generation. *(Web scraping is a separate gig — see
> Gig 5.)* AI-assisted for speed, hand-verified against your real inputs and
> outputs.

**Requirements:** a clear description of the input, the desired output, and an
example of both if you have one.

**FAQ:**
- *Will I be able to run it myself?* Yes — plain Python, documented, no
  locked-in tooling.
- *Ongoing maintenance?* Retainer available for recurring jobs and updates.

---

## Gig 4 — "I will build you a custom AI agent or chatbot that does real work" *(Axiom)*

- **Category:** Programming & Tech → AI Development
- **Tags:** `ai agent`, `chatbot`, `ai assistant`, `ai automation`, `llm`, `ai integration`
- **Tiers:**
  - Basic — $250 — one focused agent/assistant (single task, one integration); 5 days
  - Standard — $550 — a multi-step agent with tools (API calls, document handling, memory); 7 days
  - Premium — $995 — a production agent: tools + memory + deployment + a runbook; 10 days

**Description:**

> I build AI agents that do real work — not demos. Tell me the task you want
> taken off your plate, and I'll build an agent that performs it: understands
> instructions, calls the tools/APIs it needs, remembers context, and hands
> back a finished result.
>
> What you get:
> - A working agent/chatbot (code + config)
> - Integration with the APIs/tools it needs (you bring the keys)
> - Clear docs: how to run it, what it needs, how to extend it
> - Example runs showing it works on your actual use case
>
> Built with AI assistance (fitting — I use the tools to build yours faster),
> then hand-tested against your real scenario before delivery.

**Requirements:** the task you want automated, the tools/services it should
use (if any), and what "done" looks like.

**FAQ:**
- *Which LLM?* I build on whatever you prefer — OpenAI, Anthropic, DeepSeek,
  or local — you bring the key, I write the agent.
- *Is it a demo or real?* Real — tested against your actual use case, with
  docs to run it yourself.
- *Ongoing support?* Retainer available for iteration and maintenance.

---

## Gig 5 — "I will build a Python web scraper to extract the data you need" *(Axiom)*

- **Category:** Programming & Tech → Data → Web Scraping
- **Tags:** `web scraping`, `data extraction`, `python`, `scraper`, `data collection`, `csv`
- **Tiers:**
  - Basic — $100 — one site, simple scrape → CSV/JSON; 3 days
  - Standard — $250 — multi-page/pagination, parsing + cleaning; 5 days
  - Premium — $500 — complex (login, JS-heavy pages, anti-bot) + scheduled runs + structured DB output; 7 days

**Description:**

> I build scrapers that get you clean, structured data — not a tangle of HTML.
> You get a tested Python script that fetches, parses, and saves the data you
> need as CSV/JSON, with clear docs.
>
> What you get:
> - A working scraper (handles pagination, login, or JS where the tier calls for it)
> - Clean structured output (CSV/JSON)
> - Error handling — it fails loudly, never silently returns wrong data
> - A README (how to run, what it needs)
>
> I stay within a site's terms — if a job needs a licensed API instead, I'll
> tell you and build against that. AI-assisted for speed, hand-verified
> against the live site.

**Requirements:** the target site/pages, the exact fields you want, and a
sample of the data if you have one.

**FAQ:**
- *Do you scrape sites that block it?* I stay within ToS; if a site blocks
  scraping I'll recommend its licensed API.
- *How do I run it?* Plain Python, documented, no locked-in tooling.
- *Recurring extraction?* Retainer available for scheduled/ongoing scrapes.

---

## Market notes (why these prices)

Validated 2026-08-17 — external signal, not opinion:

- **The $5 gig is dead.** Top sellers lead with $75–$250 starter packages and
  build on retainers, not volume (UniLink, "Best Fiverr Gigs to Sell in
  2026," 2026-05-03).
- **The market is bifurcated.** Commodity floor: bug fixes $20–$74, basic
  code reviews $40–$78, simple scripts $30–$90 (Fiverr cost guides). Premium
  tier: detailed code review $150–$1,500; dev/no-code automation averages
  **$200–$2,500/order**; custom AI agent/chatbot building tops out around
  **$995** (live-checked). Every gig above is priced *above the floor* into
  the premium tier, with the AI-agent gig holding the highest ceiling.
- **Positioning beats price.** "Builders who solve business problems, not
  just tickets" capture the premium. AI-assisted services grew ~200% YoY but
  buyers now want "specialists who add real judgment, not button-pushers" —
  which is exactly the gap these gigs fill: verified judgment on top of AI
  speed.
- **Lane differentiation beats duplication.** Five non-overlapping lanes
  (debug / review / workflow-automation / AI-agent / web-scraping) cover more
  distinct demand than five overlapping "Python script" gigs would — and avoid
  the account cannibalizing itself.

Sources: fiverr.com/resources/guides/costs/* (code review $150–$1,500; bug
fixes $20–$74; software dev $54–$658); unilink.us/blog/best-fiverr-gigs-2026;
Axiom's live-checked gig ranges (2026-08, in its profile memory).
