# Fiverr Competitor Analysis & Outperformance Playbook — 3V0 × Axiom

*Prepared 2026-08-17. Data: live scrape of Fiverr gig browse pages (Hugging Face
dataset `Ahad690/fiverr-gigs`, scraped 2026-07-10, 9,213 raw rows → 501 unique
gigs after dedup) + six parallel research threads (per-lane competitive
intelligence + platform mechanics). Where the dataset and articles disagree,
the dataset wins — it is real listings, not SEO prose.*

> Caveat: the dataset is a browse-page sample, not the entire Fiverr market.
> Directionally strong; treat exact counts as floors.

---

## 1. Executive summary — the ten findings that matter

1. **The category paths mostly hold — verify the exact names at publish.** The live tree confirms `Programming & Tech → Software Development → Bug Fixes` (**4,900+ live results**), `Programming & Tech → Software Development → Automations & Agents`, `Data → Data Scraping`, and `AI Development`. The code-review home is now **`QA & Technical Review`** (was "QA & Review"). The browse-page dataset missed the Bug-Fixes/QA branches (sampling artifact, corrected in §4); titles/tags still carry most of the discovery weight.
2. **Debug and code review are whitespace.** In the browse sample there is essentially no entrenched, high-review competitor in either lane (1 bug-fix gig, 0 code-review gigs). We can own both niches from day one — but buyers find these services via *search*, so tags/titles carry the load.
3. **The automation lane was eaten by n8n.** The Software Development subcategory is dominated by no-code workflow gigs (n8n, Make, Zapier, Vapi, Retell, GoHighLevel) — top sellers at $80–$1,250 with 400–500 reviews. A plain "Python automation" gig competes against that wave; ours must sell *code beyond no-code limits*.
4. **The AI lane is a premium-price bloodbath.** 2,398 raw listings in AI Development + Chatbot Development; PK/IN/BD dominate; median basic $125 / premium $1,200; top app-dev sellers run $150→$2,500 with 866 reviews, while manychat wrappers scrape the $30→$85 bottom. Our $250/$550/$995 sits at the 75th percentile of basic prices — defensible only with visible proof.
5. **Scraping is the hardest lane in the package.** Entrenched giants at $30→$125 with 1,000–2,000 reviews ("50k rows in 1 day"); 72% of the market's basic tier is ≤$30. Our $100 basic is at the 95th percentile. It can still work — but only by selling to buyers burned by broken scrapers, and it will be the slowest lane.
6. **Rating is table stakes.** Median rating across lanes is 5.0. A 5.0 average wins nothing; review *text* and portfolio proof are the differentiators.
7. **Zero New Zealand sellers in the sample.** We'd be geographically distinctive, and NZST offers follow-the-sun coverage for US/EU buyers — a real angle, not filler.
8. **AI disclosure is conditional, not mandatory.** `gigs.md` claims "Fiverr requires the disclosure" — that is wrong (§5). Fiverr permits AI in every category; disclosure is required only when a buyer asks or states a "no AI" preference. What's enforced is the quality bar: raw AI slop fails; customized, verified work passes. Lying about tool use is the actual ban trigger.
9. **Buyers want proactive disclosure anyway.** 2026 consumer research (84–91% want AI content labeled) and academic studies (clients want proactive disclosure, freelancers under-disclose) mean our "AI-assisted, hand-verified" framing is the trust-winning move — we keep it, but as *positioning*, not compliance.
10. **API integration + AI voice agents are adjacent whitespace** we're not in. n8n work, Vapi/Retell voice agents, and API integrations are the fastest-moving demand in our subcategory — watch-list, not day-one scope.

---

## 2. Hard market data per lane (live listings, July 2026)

### 2.1 Bug fixing — whitespace, not a battlefield

| Metric | Value |
|---|---|
| Direct competitors visible in browse sample | 1 (Shopify bug fixing, $70→$500, 14 reviews, Level 2, GB) |
| Live-category context | The Bug Fixes subcategory holds 4,900+ results, but they're WordPress/PHP/JS/mobile-dominated; page-1 *Python* debug gigs carry mostly 1–12 reviews — crowded at the general level, undefended at the Python-specialist top |
| Implication | No entrenched giant owns "Python debugging". The commodity floor exists ($20–74 per Fiverr cost guides) but the visible sellers are generic "I fix your code" shops with small review counts. |
| Our position ($75/$150/$300) | Above the commodity floor, inside the premium outcome band, with no dominant brand above us in this sample. |

### 2.2 Code review — emptier still

| Metric | Value |
|---|---|
| Direct competitors visible in browse sample | 0 title-level matches |
| Live-category context | Home is QA & Technical Review; QA averages ~$1,640/project (4th-most-expensive category) but the market is bimodal ($15–78 fix-gigs/thin reviews vs $300–1,500+ pentests) — the middle is empty, which is where our $75/$150/$300 sits |
| Market context | Fiverr cost guides price checklist reviews at $40–78 and detailed reviews at $150–$1,500 — demand exists, but no sampled seller brands it as their main gig. |
| Our position ($75/$150/$300) | We can be *the* named code-review seller in the visible market. Proof portfolio (the `samples/` review) is the moat. |

### 2.3 Workflow automation — the n8n problem

| Metric | Python-automation matches | What actually dominates the subcategory |
|---|---|---|
| Unique gigs | 12 (most bundle scraping) | 30+ n8n / Make / Zapier / Vapi / Retell / GoHighLevel workflow gigs |
| Median pricing | basic $30 (83% ≤$30), premium $125 | top n8n sellers: $80–$110 basic → $950–$1,250 premium, 422–484 reviews |
| Seller geography | IN/BD led | PK/BD/NG led |
| Our position ($100/$250/$500) | 100th percentile of visible Python-automation basics | ≈ premium n8n tier |
| Implication | Buyers searching "automation" meet n8n experts first. We win the buyer whose workflow *outgrew* no-code — custom logic, data quality, tests, no platform lock-in — and the API-integration buyer ($250→$995 gig with 104 reviews shows that demand). |
| Search volume | "python automation" returns **5,600+ results** — the lane is crowded, but the top-ranked automation gigs are almost all *scraping* gigs, not business-workflow automation (CSV/Excel cleaning, batch files, API integration, reports). That's the open gap: **no visible competitor leads with tests + README + error handling + handover docs**, which is exactly our package and exactly what buyers complain is missing (broke-on-real-data, no docs, silent failures, ghosting). |

### 2.4 AI agent / chatbot — crowded, but thin in the middle

| Metric | Value |
|---|---|
| Unique gigs (AI Dev + Chatbot Dev) | 65 (raw listings 2,512) |
| Median pricing | basic $125, standard $475, premium $1,200 |
| Basic≤$30 share | 4.6% (this lane is already premium) |
| Basic≥$75 share | 83.1% |
| Median reviews | 12 — most sellers are unproven; the head is huge (866) |
| Top competitors | $150→$2,500 "AI mobile app + website + chatbot + agent" (866 rev, PK); $300→$5,000 (588 rev); $125→$3,000 (302 rev); manychat $30→$85 (211 rev); RAG-systems $150→$995 (7 rev); multi-agent systems $5,000 (5 rev) |
| Geography | PK 27 / IN 11 / BD 8 / US 7 of 65 unique |
| Our position ($250/$550/$995) | 75th pct basic, 46th pct premium — mid-premium. We undercut app-dev agencies and out-serious the manychat wrappers. The gap: "a production agent tested on MY use case, with docs" — almost nobody sells verification. |

### 2.5 Web scraping — giants at the floor, ceiling open

| Metric | Value |
|---|---|
| Unique gigs (Data Scraping) | 39 |
| Median pricing | basic $30 (72% ≤$30), standard $80, premium $185 |
| Median reviews | 147 — entrenched sellers |
| Top competitors | $30→$125 "any website, 50k rows in 1 day" (1,958 rev); $30→$250 (1,547); $30→$130 (1,433); $30→$280 (1,362); $40 (1,162); $30→$200 (955) |
| Our position ($100/$250/$500) | 95th pct basic, 85th pct premium — priced at the extreme top of the visible market |
| Implication | Do not fight on price. Sell data *quality*: schema guarantees, dedup, monitoring, loud failure, ToS-honest guidance, recurring managed runs. Accept low volume early; this lane compounds once review text proves reliability. |

### 2.6 Software Development subcategory overall (our future home turf)

- 69 unique gigs: median basic $100, standard $450, premium $995 — i.e. **our package's price zone is the subcategory's median**, not an outlier.
- Levels: Level 2 = 43, Level 1 = 15, Top Rated = 8 — plenty of room for a fast-climbing new seller.
- Fastest-moving themes: n8n AI agents, Vapi/Retell voice agents, API integration, SaaS MVP builds ($995→$9,995 and $1,225→$6,215 gigs exist with few reviews — proof that buyers pay for outcome framing).

### 2.7 Structural facts that shape the plan

- **The climb is short.** Market-wide median review counts: Level 1 = 16, Level 2 = 78, Top Rated = 253. At 5–10 premium orders/month a new seller reaches Level 2 inside a year. 17% of unique gigs have ≤5 reviews — most sellers never leave the starting block.
- **Tiered pricing is the norm.** 476 of 501 unique gigs (95%) use 3-tier packages — our tier structure is exactly right; single-price gigs are the outlier.
- **Title vocabulary of the winners:** AI lane head sells `chatbot/mobile/saas/whatsapp` (app-dev framing); Software Development head is `n8n/automation/workflow/agent/vapi`; scraping head is `scraping/mining/extraction/csv`. Our titles already carry the right keywords (`agent`, `chatbot`, `scraper`, `extract`) — we deliberately *don't* chase `n8n/mobile/saas`, which is correct: we sell outcomes, not platform stamps.
- **Premium exists inside Software Development:** gigs at $995→$9,995 and $1,225→$6,215 carry single-digit review counts — proof that outcome-framed premium services win orders in our home subcategory without needing hundreds of reviews.

---

## 3. Price positioning verdict (data, not opinion)

| Gig | Our basic | Market percentile (basic) | Verdict |
|---|---|---|---|
| Debug Python | $75 | n/a — near-empty lane | Keep. Own the niche. |
| Code review | $75 | n/a — near-empty lane | Keep. Own the niche. |
| Automation | $100 | ~100th | Keep price, sharpen positioning to "beyond no-code + API integration". |
| AI agent | $250 | 75th | Keep. Mid-premium in a premium lane; proof portfolio is the gap-filler. |
| Scraping | $100 | 95th | Keep *only* with radical quality differentiation; expect the slowest ramp. Revisit after 10 orders. |

---

## 4. Category-tree verification (checked against live category pages)

The July-2026 browse dataset's subcategory sample was *partial* — it missed branches the live tree has. Verified against live Fiverr category pages via the research threads:

| Gig | Category path (verified live) | Notes |
|---|---|---|
| 1 — Debug Python | **Programming & Tech → Software Development → Bug Fixes** | Exists; **4,900+ live results**, but Python-specific debug gigs on page 1 carry only 1–12 reviews — crowded at the general level, undefended at the Python-specialist top. `gigs.md`'s path is correct. |
| 2 — Code review | **Programming & Tech → QA & Technical Review** | Renamed from "QA & Review". Carry the niche via title + tags (`code review`, `security audit`, `python`). |
| 3 — Automation | **Programming & Tech → Software Development → Automations & Agents** | Dedicated subcategory exists (nested sub-category "Automations & Agents"); the n8n wave lives here. |
| 4 — AI agent | **AI Development** | Confirmed (AI Development + Chatbot Development are separate live subcategories). |
| 5 — Web scraping | **Data → Data Scraping** | Confirmed by both the dataset and the live tree. |

Action at publish: confirm the exact picker values (Fiverr renames periodically) and use exactly the 5 tags per gig from `gigs.md`.

---

## 5. Launch constraint: the 4-gig cap (must-fix in SETUP.md)

`gigs.md`/`SETUP.md` assume "up to 7 gigs" on day one. **Wrong in 2026:** new sellers can have only **4 active gigs** ([Fiverr Community: "Only (4) GIG for New Sellers"](https://community.fiverr.com/forums/topic/326218-only-4-gig-for-new-sallers/), [Gig policies](https://help.fiverr.com/hc/en-us/articles/360011421218-Gig-policies)); more slots unlock at higher seller levels.

**Decision (recommended):** prepare all five, publish four, hold one in draft until Level 1.

| Launch now | Hold in draft | Why |
|---|---|---|
| Debug Python | | Whitespace lane — becomes ours fastest |
| Code review | | Whitespace lane — portfolio proof is already built (`samples/`) |
| AI agent | | Biggest, fastest lane; Axiom's strongest card |
| Web scraping | | Keeps the 2×3V0 + 2×Axiom balance on one account |
| | Workflow automation | Hardest repositioning (n8n wave); publishes stronger after the lane is reframed as "code beyond no-code + API integration" and after first reviews land |

*(Swap scraping and automation if you'd rather Axiom lead with agents only — but don't hold two 3V0 gigs and two Axiom gigs both: the balanced 2+2 uses the account's review flywheel best.)*

---

## 6. AI-disclosure correction (verify the premise)

`gigs.md` line: "Fiverr requires the disclosure." — **Wrong.** Per Fiverr's official [Using AI on Fiverr: Guidelines for freelancers and clients](https://help.fiverr.com/hc/en-us/articles/37554976380177-Using-AI-on-Fiverr-Guidelines-for-freelancers-and-clients) (verified via primary-source review in [Memvers' 2026 disclosure analysis](https://www.memvers.com/blog/ai-disclosure-rules-freelance-platforms-2026)):

- AI is permitted in every category. No default requirement to label gigs or deliveries as AI-made.
- Disclosure becomes mandatory on two triggers: (a) the client asks; (b) the client states a "no AI" preference before/at order start — then you must disclose your intended workflow and honor the request.
- Fiverr's dispute process enforces the **quality bar**, not the tool: generic/unmodified/reused AI output fails; customized, verified output passes. Lying about tool use or misrepresenting AI work = cancellation/refund/permanent suspension.
- The one always-on disclosure: Fiverr's AI Personal Assistant inbox bot self-identifies as AI and cannot be turned off. If 3V0 ever auto-replies via that assistant, bot-identity is enforced by the platform itself.

**Net:** keep "AI-assisted, hand-verified" everywhere — but as the trust story, and make the "hand-verified" part *provable* (review evidence, test runs, before/after). The compliance sentence in `gigs.md` needs a one-line rewrite.

---

## 7. Qualitative per-lane intelligence

*Six parallel research threads; sources inline. Fiverr blocks direct scraping, so aggregator numbers are directional snapshots — cross-check against §2's dataset where they conflict.*

### 7.1 Debug Python (3V0)

**Market:** the Bug Fixes subcategory holds **4,900+ live results** — but it's dominated by WordPress/PHP/JS/Shopify/mobile gigs; the *Python* debug slice is thin: page-1 Python debug gigs carry mostly **1–12 reviews**. Price bands: basic $5–$35, premium $20–$60 for pure Python (up to $500 when it bleeds into web/automation). Our $75/$150/$300 is 3–5× the median — defensible *only* with visibly different deliverables (which is exactly the plan).

**Named competitors:** kyoukai_dev (Fiverr Pro, $20/$35/$60, 12 rev — the closest rival, but **static-analysis only: explicitly does not execute your code**); warona_nyama (L2, $5/$10/$20, 4.9/270 — student, ≤300 lines, learner-focused, no tests); philipgreen00 (L2, $10/$20/$40, 5.0/1k+ — multi-language, slow 3–5d, comments-only explanation); duncancurrier (L2, $10, 4.9/270 — "quickly and efficiently" speed positioning); plus generic multi-language fixers at $15–$35. **No one owns "root-cause bug forensics for Python"** — the biggest players are generalists or build+fix developers.

**Buyer pain points:** patch-not-cure ("you fix one thing and two more break" — [techteems](https://techteems.com/what-its-like-to-fix-your-codebase-after-a-fiverr-disaster/)); no explanation/docs/version control ([humansfix](https://humansfix.ai/guides/common/fiverr-developer-broke-my-app)); AI-generated untested code sold as custom work ([Fiverr Community](https://community.fiverr.com/public/forum/boards/freelancer-lounge-sry/posts/the-difference-between-using-ai-and-selling-ai-du507fwwsp)); sellers disappearing or holding fixes hostage; hardcoded credentials; platform distrust (Trustpilot 3.2/5, "price friction" the #1 complaint — [RedditMaster](https://www.redditmaster.com/reddit-intelligence/fiverr)).

**Whitespace (verified open):** actually **executing/reproducing** the failure (the closest rival advertises *not* doing this); a named root-cause writeup deliverable; **regression tests** (zero competitors list one); a seller-branded **warranty window** (none exists); a "won't reproduce → honest redirect" policy; "fix the whole bug class" framing; a manager-readable plain-English report; a coherent brand (competitors are bare usernames).

**Sharpest tactics:** (1) lead the title with "I reproduce the bug, then fix it — not static-only guessing"; (2) show a sample one-page Root-Cause Report as a gallery image; (3) bundle the regression test + **14-day fix warranty** into every tier — the "$75 is 5× the median" objection becomes a feature comparison nobody else can answer; (4) adopt the honesty policy as a headline trust signal; (5) **consider a $35–45 "Reproduce + Diagnosis" Basic tier** (report only, no code change) so the 0-review gig survives the click test — the $150/$300 tiers keep the premium; (6) own the keyword "Python root cause / bug forensics" (appears in zero leading listings); (7) sub-1-hour response discipline across time zones from day one; (8) work Fiverr Briefs daily for the first 2–3 weeks; (9) frame AI as triage, not the fixer; (10) over-specify scope in writing (what's included, what's not) to protect the first five reviews from scope creep and chargebacks ([forum](https://community.fiverr.com/public/forum/boards/support-and-troubleshooting-by1/posts/336735-programmers-are-not-protected-on-fiverr)).

### 7.2 Code review (3V0)

**Market:** the home is **Programming & Tech → QA & Technical Review**; demand tailwind is the *vibe-coding backlash* — AI-generated code is "fast but dangerously insecure" and buyers now pay humans to review/fix it ([Wedbush/ABNewswire](http://investor.wedbush.com/wedbush/article/abnewswire-2025-11-11-report-how-to-fix-the-hidden-security-risks-of-vibe-coding-and-why-platforms-like-fiverr-are-becoming-the-go-to-solution)); a single niche search "vibe code fixer" already returns 230+ results; QA & Testing averages **~$1,640/project** (4th most expensive category — [Memvers](https://memvers.com/blog/freelance-price-index-2026)). The market is bimodal: commodity floor $15–$78 (fix-gigs, thin single-language reviews) vs premium $300–1,500+ (pentests, audits) — **our $75/$150/$300 slots into the almost-empty middle**.

**Named competitors:** sliverc ($40 Python review — commodity, no fixes), codemetas ($50 C++ — education-branded, one language), asadblc29 ($120 QA+pentest — checklist framing, upsell friction), elvismdev (WordPress-only), ayeshasaleem345 ($35 fix-focused), abdullahkhawaja (~$120+ pentest — security-only, no maintainability axis), plus Pro generalists (codedarkin, rk1203). **Cross-cutting weakness:** nobody promises the combination we lead with — severity-ranked findings + concrete before/after fix for *every* finding + remediation plan + hand-verified line-by-line pass.

**Buyer pain points:** buyers actively avoiding "AI-sounding" sellers and "AI slop" reports ([Fiverr Community](https://community.fiverr.com/public/forum/boards/freelancer-lounge-sry/posts/some-buyers-are-now-avoiding-ai-sounding-sellers-1bjebip2vg)); generic unactionable output ("just tells me what's wrong"); missing real bugs / no security depth (studies: ~40% of AI-suggested code has security flaws — [safeguard.sh](https://safeguard.sh/resources/blog/autocomplete-anxiety-measuring-how-often-ai-coding-assistants-suggest-vulnerable-patterns)); quality decline ("silent exodus of Fiverr buyers" [thread](https://community.fiverr.com/public/forum/boards/freelancer-lounge-sry/posts/the-silent-exodus-of-fiverr-buyers-9n4hdqwv4k)); scam fear ([thread](https://community.fiverr.com/public/forum/boards/support-and-troubleshooting-by1/posts/fiverr-does-not-protect-you-from-scammers-7pm0ng34r1)); revision friction ([thread](https://community.fiverr.com/forums/topic/324693-client-refuses-to-accept-delivery-and-keeps-using-revisions-and-gave-me-1-stars-reviews/)).

**Whitespace:** security-first framing at the *review* price (OWASP/CWE classes named, without pentest prices); before/after fix snippet per finding; **remediation plan** as a named deliverable (competitors stop at "here's a report"); a checkable methodology (kills the AI-slop objection); a free re-review pass; multi-language breadth at one price; NZ/Western trust.

**Sharpest tactics:** (1) make "every finding ships with a before/after fix snippet" the literal headline and *show* a redacted real finding in the gallery; (2) publish a named, checkable **"3V0 Method"** (static scan → AI-assisted triage → human line-by-line verification) — the counter to the AI-sounding-seller filter; (3) reframe the $75 tier as "security + maintainability review" naming OWASP/CWE classes — captures the vibe-coding buyer who expects real security findings; (4) make the $300 tier "audit + **remediation plan**" (prioritized, phased, effort-estimated) not "a bigger report"; (5) bundle languages ("Python-first, plus JS/TS, shell, SQL at no extra charge") against the fragmented single-language field; (6) include ONE free re-review pass in the standard tier — neutralizes revision friction and creates the repeat-buyer loop; (7) win the first 3 reviews via a free redacted sample audit of open-source code → small foot-in-the-door order → over-deliver; (8) drive off-platform traffic to the vibe-coding buyer (r/Python, r/SideProject, indie forums) with a "what I found in 500 lines of AI-generated code" write-up; (9) instrument every deliverable as proof-of-work (line numbers, file paths, diffs) so the report verifies itself.

### 7.3 Workflow automation (Python)

**Market:** "python automation" = 5,600+ Fiverr search results; sub-category splits: Software Development ~2,700, Script Development ~1,400, Data Scraping ~600, Automations & Agents ~500. Three price layers: commodity scripts $5–$67; premium pipelines $109–$500; no-code/AI automation avg ~$250 (n8n avg ~$400). Delivery 2–7 days is standard — our 3/5/7 is on-market.

**Named competitors (live listings):** Nithin Srinivas (Top Rated, $36, 4.9/959 — scraping-led), Majd M (L2, $109, 5.0/486 — no docs/tests), Kawsar (Vetted Pro, $109, 5.0/450 — scraping only), Prakriti K (Top Rated, $183, 4.9/170 — no handover docs), Cristian M (Fiverr's Choice, $67, 5.0/51 — generic), Eazisols agency (Top Rated, $157, 5.0/19 — agency lock-in), Shaheer (L1, $15, 4.9/32 — commodity), Jason Crowe (Top Rated, $500, 5.0/170 — the premium ceiling). Pattern: **none leads with tests, README, error handling, or handover docs** — the one exception buries "with tests" in a single Basic-tier bullet.

**Buyer pain points:** broke-on-real-data + no docs + AI-without-testing ([humansfix](https://humansfix.ai/guides/common/fiverr-developer-broke-my-app)); four named failure modes — ghosting, delivered-but-broken, scope-creep-into-bankruptcy, IP trap ([stepto](https://stepto.net/blog/software-project-rescue-developer-ghosted-what-to-do)); dishonest sellers/misrepresented scope ([Trustpilot](https://uk.trustpilot.com/review/fiver.com)); unresponsive sellers ([Fiverr Community](https://community.fiverr.com/public/forum/boards/ask-the-community-xsm/posts/order-issue-unresponsive-seller-possible-scam-concern-cancellation-rejected-9un2896vxz)).

**Whitespace (verified open):** tests advertised publicly; runbooks/README; explicit failure behavior (logs, exit codes, retry); maintenance retainers ("my script broke" rescue market); "AI-assisted + hand-verified" as a *named* promise; dry-run/`--help` self-verification; business-workflow automation vs scraping (the visible "python automation" top results are mostly scraping gigs — CSV/Excel/batch/API/reports is comparatively open).

**Sharpest tactics (from the lane report):** (1) put "tested, documented" in the title's first line; (2) ship every order with `--dry-run` + `--help` so buyers verify before real data; (3) promise failure behavior in the copy (exit codes, log file, retry) — the screenshot-able guarantee; (4) hold the credible middle ($100/$250/$500 above the cheap-risk floor, below the $500 Crowe floor); (5) sell a post-delivery fix/maintenance tier; (6) niche the keywords to the four buyer jobs (clean Excel/CSV, batch files, API connections, reports); (7) public GitHub spec-work portfolio (3–5 scripts, each with README+tests+runbook) as the review substitute; (8) over-deliver sequence on order one: 30-min reply → delivery with rationale → 24h follow-up + free "what could break" doc.

### 7.4 AI agent / chatbot (Axiom)

**Market:** the category is real and compounding — Fiverr Q1 2026: AI development/consulting orders **+118% YoY**; June 2026 Trends Index: Claude Code specialists +938%, n8n AI automation +125%, vibe coding +61%, AI voice agents +49%; "AI agent" is now its own hireable subcategory ([Fiverr IR](https://investors.fiverr.com/news-releases/news-release-details/businesses-race-hire-claude-code-specialists-demand-surges-938)). Packaged chatbot/agent gigs cluster at **$200–$500**; aggregator tiers: Basic chatbot $100–300 / Custom bot $300–800 / Enterprise $800–5,000+; agents $500–1,500 / $1,500–5,000 / $5,000+. **Our $250/$550/$995 sits exactly in the under-served middle band** — above the wrapper noise floor, below the enterprise cliff.

**Named competitors:** AMZ Automation (~$50, 4.9/450, n8n templates), ConversionAI (~$590, 4.9/40, unverifiable "$23M" claims), Adunsina (~$150, 4.8/60, Vapi voice + n8n), Husnain (~$50, 4.9/100, RAG Q&A bot), Mubashir (~$90, 4.9/100, OpenAI-locked), Sohan/Croco (~$120, 5.0/150, AI mobile apps), Prathamesh2004_ (~$100 — direct title overlap but lowball template), Talaltariq13 (~$9,995 — enterprise platform builds), plus a $10–$60 Botpress/n8n template tier. **Recurring weaknesses:** n8n/RAG templates, OpenAI-locked, nobody leads with memory + deployment + runbook + testing against the buyer's real scenario, unverifiable claims.

**Buyer pain points:** "$50 'fully custom AI agent' = template with your logo" ([Trixly](https://www.trixlyai.com/blogs/how-much-does-custom-ai-agent-development-cost-in-2026)); hidden costs (token fees, 15–30%/yr maintenance, monitoring) that surface after signing; "most AI agents are expensive API wrappers" — no persistent state/goal-planning/failure recovery ([Hotmolts](https://www.hotmolts.com/post/most-ai-agents-are-just-expensive-api-wrappers-wit-0e2ef9a9-9732-49f9-9c0f-02cce1563624)); buyers now ask cost-per-task + accountability + recovery, not capability ([White Beard](https://whitebeardstrategies.com/blog/what-do-you-say-when-a-client-asks-what-does-your-ai-actually-cost-and-who-fixes-it-when-it-breaks/)); fake social proof normalized ([Reddit teardown](https://arctic-shift.photon-reddit.com/api/posts/ids?ids=1o3tnnv)); buyers actively avoiding "AI-sounding" sellers ([Fiverr Community](https://community.fiverr.com/public/forum/boards/freelancer-lounge-sry/posts/some-buyers-are-now-avoiding-ai-sounding-sellers-1bjebip2vg)); "agent washing" erodes the whole label.

**Whitespace:** agent that calls the *buyer's actual* APIs/tools; real memory/persistent state; deployment + runbook; LLM-agnostic builds; honest "you bring the key" pricing (dissolves the #1 hidden-cost complaint); testing against the buyer's real scenario; explicit "not a demo" delivery contract; disclosed AI-assisted framing as a trust asset.

**Sharpest tactics:** (1) keep the outcome-led title; sound like an engineer, never a prompt-slinger; (2) map the three tiers to capability (single agent / multi-tool+memory / agentic workflow+runbook), not "more of the same"; (3) 60-second gig video of a *real agent run* (work product, not demo); (4) FAQ must answer cost-per-task, accountability, and recovery — the three questions no competitor answers; (5) sell "you bring the key" with the math (you own tokens + data, no surprise bills); (6) make "not a demo" a delivery list item: deployed + runbook + example runs + hand-tested; (7) 2–3 redacted spec-work case studies before launch; (8) NZ + English-native as premium trust; (9) Briefs metadata (AI Agent, tool integration, memory, deployment, runbook) + sub-1-hour brief replies; (10) first three orders get a handoff call + 30-day runbook support — those reviews are the whole flywheel.

### 7.5 Web scraping (Axiom)

**Market:** ~5,254 gigs in the Data category scrape; "web scraping" search = thousands of results. Price bands from the sample: **73% of scraping gigs start at ≤$30**; standard tier median ~$80; only **~12% start at $100+**. Median 168 reviews, max 1,958 — commodity sellers hold huge review moats. Geography: PK 9 / BD 4 / IN 4 / EG 2 of 26 — a South-Asian price/volume wall. Delivery: commodity = 1–3 days; our 3/5/7 is slightly conservative (fine — premium should read deliberate).

**Named competitors:** the commodity wall (Python_dev_2025 $30, Hassanali907 $30, Asafcadmon $30, Robertttt007 $25), Fiverr Pro generalists (glad2serviceu, hassan_ali_123), and — critically — **two top-rated sellers already at our exact $100/$250/$500 price point** ("do python web scraping, data scraping, and data mining" 4.9/464 · 1/3/5d; "conduct web scraping using python" 4.9/443 · 2/4/5d) — *without* robustness/loud-failure/ToS positioning. That's the proof the price is accepted and the differentiation is open.

**Buyer pain points:** silent wrong data (incomplete records, duplicate entries from pagination errors, stale data — [Tendem](https://tendem.ai/blog/fiverr-web-scraping-gigs-review)); sellers vanish when the site changes / no maintenance ("support ends when the gig closes"); break-on-change fragility (a real scraper fell 92%→61% success in 30 days from one site change — [dev.to](https://dev.to/perufitlife/why-my-reddit-scraper-went-from-92-to-61-success-rate-in-30-days-and-the-one-line-fix-3013)); unresponsive sellers; ToS/legal risk the buyer inherits ([Lexology](https://www.lexology.com/library/detail.aspx?g=ad99502e-e399-4850-9542-80b96e210ed5)); hidden quality cost ("a $100 gig that needs 3 hours of your management time + 2 revision cycles is not a $100 project").

**Whitespace (the gap map, from a competitor's own teardown):** ongoing/recurring runs; business-critical accuracy with QA; SLA-like guarantees; post-delivery maintenance; ToS/legal guidance; plus: robustness (retry/backoff, config-as-code, a re-runnable smoke test), loud failure modes (validation report: empty fields, failed pages, reasons), clean data contracts (schema agreed before build), hand-verified-against-live-site proof.

**Sharpest tactics:** (1) lead with "survives site changes" not "I'll scrape anything" — README + retry/backoff + selectors in one config + smoke-test command; (2) make **loud failure a literal deliverable** — every order ships a `validation_report` (records scraped, empty fields, failed pages + reasons, live-site diff); (3) prove hand-verification with screenshots + CSV rows cross-checked against the live page in the gallery; (4) **data contract before code** (column names, types, one sample row approved before build); (5) sell the ToS-honest pivot as a feature (licensed-API memo when a site blocks — trust + natural upsell); (6) package **scheduled/recurring runs as the Premium tier** — converts one-shots into the recurring revenue Fiverr structurally lacks; (7) weaponize "New Zealand · hand-verified" against the PK/BD/IN wall; (8) 3–5 spec-work scraper demos in the gallery before any sale; (9) keep the $100/$250/$500 ladder but gate exactly as promised (Basic = 1 static site, single page, CSV + validation report; pagination/login/JS strictly Standard/Premium); (10) Briefs + <1h replies + small freebie (bonus export format) on early orders to farm the first 5-star reviews.

---

## 8. Platform mechanics: ranking, levels, and the first-order playbook

*Compiled from Fiverr's official Help Center (verified Feb-2026 article set by the mechanics research thread).*

### 8.1 What actually determines level now (exact thresholds)

Fiverr's level system is Success-Score-first; seniority, order-completion %, and on-time % no longer gate level directly — they feed the Success Score.

| Requirement | Level 1 | Level 2 | Top Rated |
|---|---|---|---|
| Success Score | ≥5 | ≥7 | ≥9 (+ manual review, 4 pillars) |
| Rating | ≥4.4 | ≥4.6 | ≥4.7 |
| Response rate | ≥80% | ≥90% | ≥90% |
| Orders (all-time) | ≥5 | ≥20 | ≥40 |
| Unique clients | ≥3 | ≥10 | ≥20 |
| Earnings | ≥$400 | ≥$2,000 | ≥$10,000 |

L1/L2 are automatic within 24h of meeting thresholds; Top Rated is manually reviewed.

**Implication:** at premium pricing, **5 clean orders ≈ Level 1** ($400 is one order-and-a-half at our prices). The whole cold-start problem is manufacturing the first five great orders.

### 8.2 Success Score — the hidden ranking engine

- Benchmarked **relative to other freelancers in your price range** — premium-priced gigs compete against premium peers. This structurally favors a real $75–$995 positioning *once reviews prove conversion* — we are not dragged down by $5 sellers' metrics.
- Six areas: customer satisfaction, effective communication, conflict-free orders, order cancellations, delivery time, value for money. **Higher-value and recent orders weigh more** — one $995 order counts more than ten $30 orders.
- Keep cancellations near zero: every cancellation hits the score and the account.

### 8.3 Paid tools are gated — the honest timeline

| Tool | Available to | Cost |
|---|---|---|
| Seller Plus Kickstart | New sellers (day one) | $15/mo |
| Seller Plus Standard | Level 1+ | $25/mo |
| Seller Plus Premium | Level 2+ | $49/mo |
| Fiverr Ads (Promoted Gigs) | Level 1+ | first-price auction CPC, up to ~$6/click |

**Day one:** only Kickstart. **Level 1:** Ads + Standard unlock — this is when paid growth starts. Budget for it after the first 5 orders, not before.

### 8.4 Briefs / Neo matching

- Briefs surface gigs with **Success Score ≥7** — a 0-review seller gets few/no briefs at first; they become a lever only after the first orders land.
- Buyer-side: 72h response window, ≤5 seller offers per brief. When briefs do arrive, replying fast and specifically (not templated) is the differentiator.

### 8.5 Response-time mechanics (this decides inbox trust)

- **Response rate** = % of first replies sent within 24h over 90 days (hidden metric). **Response time** = average hours (visible to buyers).
- Fiverr's own auto-reply does **not** count toward the rate — a manual reply within 24h is required. Third-party reply bots are unauthorized-method risk: don't.
- Sub-1-hour time needs Fiverr's auto-reply + saved quick responses + a fast manual touch. Timezone affects the visible average *time*, not the *rate* — NZST evenings cover the US/EU morning, so a disciplined twice-daily inbox sweep keeps us sub-24h everywhere.
- Every gig FAQ answers the common questions upfront — it cuts inbox volume and pre-qualifies orders.

### 8.6 Account-safety landmines (each one has banned accounts)

- One account, ever. No second account for any reason.
- Off-platform contact only **after** an order exists.
- No review manipulation of any kind (buying, swapping, family/friend orders).
- Original content only: copied gig descriptions, stock images, or reused media = ban risk.
- ID verification: government ID within 14 days, name must match ID **exactly**, VPN off during verification.
- Excessive cancellations / chargebacks flag the account; never cancel to reset metrics.

### 8.7 Money mechanics

- Commission: 20% (you keep 80% of order value).
- Clearing: 14 days (7 days once Top Rated/Pro).
- Orders auto-complete 3 days after delivery unless the buyer intervenes.

### 8.8 Day-one checklist (ToS-safe cold start)

1. 100%-complete profile (photo, description, languages, skills) + **intro video** — a ranking/trust lever we haven't built yet.
2. Publish 4 of 5 gigs (cap) with original text + our own covers + portfolio items.
3. Seller Plus Kickstart ($15/mo) at launch.
4. Save quick responses for the five most common pre-order questions; target <1h visible response time via the NZST-evening sweep.
5. Warm off-platform traffic (LinkedIn, GitHub, the 3V0/Axiom communities) pointed at the gigs — legitimate, and the fastest first-order source that Fiverr itself sanctions.
6. First 5 orders: over-deliver, request reviews through Fiverr's own flow only, zero cancellations.
7. At Level 1: enable Fiverr Ads on the two best-converting gigs; start answering Briefs; add the 5th gig (automation).

---

## 9. Outperform in every way — the consolidated playbook

*(Draft from hard data; to be merged with the qualitative threads in §7–8.)*

### 9.1 The six outperformance levers

1. **Proof, not promises.** 95% of sellers run 3-tier packages and every lane's median rating is 5.0 — so stars are noise. What compounds is *verifiable evidence in the gig itself*: the `samples/` code review, a root-cause write-up, a before/after automation demo, an example agent run log, a scraper output sample. Portfolio items beat adjectives; every gig publishes with at least one real deliverable artifact.
2. **Own the empty lanes outright.** Debug and code review have no visible giants — first mover gets the review flywheel. Put the best proof there and win those lanes before competitors notice.
3. **Sell the outcome the incumbents can't fake.** Scraping giants promise "50k rows in 1 day" (speed); we promise schema-guaranteed, deduped, loud-failing data pipelines (reliability). n8n sellers promise workflow setup (tooling); we promise *code beyond no-code limits* + API integration (capability). manychat sellers promise a chat widget; we promise an agent tested on the buyer's real scenario (verification).
4. **Speed as a product feature.** 2–5 day delivery at premium prices is itself a differentiator when commodity sellers quote the same for $30. Hold the quoted delivery times — on-time % is a ranking factor.
5. **Geography + follow-the-sun.** Zero NZ sellers sampled; NZST covers the APAC window and early-morning US/EU — respond to briefs/messages inside the NZST evening and you answer when PK/IN competitors are asleep. First-response time is a ranking factor; make <1h the standard.
6. **Retainers as the compounding layer.** Every gig FAQ already mentions retainers; make the first-order handoff end with a maintenance offer (monitored scraping, recurring automation, agent iteration). The market head builds on retainers, not volume.

### 9.2 Per-gig battle plans (data-driven)

| Gig | Headline move | Proof asset | Watch out for |
|---|---|---|---|
| Debug Python | "I reproduce the bug, then fix it — never static-only guessing" + fix-the-class + **14-day warranty** + regression test in every tier | Sample one-page Root-Cause Report as a gallery image + `samples/debug-sample.md` | The $5–$40 price crowd and the 1-day delivery norm; the $75 tier must telegraph premium instantly. **Launch decision:** consider a $35–45 "Reproduce + Diagnosis" Basic (report only) so the 0-review gig survives the click test — keep $150/$300 for the actual fix |
| Code review | "Every finding ships with a before/after fix" + named **3V0 Method** (static scan → AI triage → human line-by-line) + security classes (OWASP/CWE) named in the $75 tier + **remediation plan** at $300 | `samples/code-review-sample.md` + a free redacted audit of open-source code as the portfolio anchor | The $15–$78 fix-gig floor and pentest gigs at $120+; the middle band is empty — occupy it visibly |
| Automation | "When n8n/Make hit their ceiling, you need code" + API integration; every order ships `--dry-run` + `--help` + failure behavior (exit codes, log file, retry) | GitHub spec-work portfolio: 3–5 scripts, each with README + tests + runbook | The n8n wave owns "automation" searches (top sellers $80→$1,250, 400–500 rev); don't fight it — sell its overflow |
| AI agent | "A production agent tested on YOUR use case — not a demo" + LLM-agnostic, buyer-brings-keys + FAQ answers cost-per-task/accountability/recovery | 60-second gig video of a real agent run + 2–3 redacted spec-work case studies with runbooks | App-dev agencies above ($150→$2,500) and manychat wrappers below ($30→$85); hold the verified middle. Buyers filter "AI-sounding" sellers — sound like an engineer |
| Scraping | "Survives site changes + loud failure" — every order ships a `validation_report` + data contract agreed before build + ToS-honest API pivots | 3–5 spec-work scraper demos (live CSV + README + validation-report sample) in the gallery | Two top-rated sellers already sit at our exact $100/$250/$500 without our differentiation; commodity wall at ≤$30. Premium tier = scheduled recurring runs (the recurring revenue Fiverr lacks) |

### 9.3 Launch-order reality check

Publish 4 of 5 on day one (new-seller cap): **debug, review, AI agent, scraping.** Hold automation in draft for Level 1. Every early order gets the full quality bar plus an extra proof artifact — the first 10 reviews are the whole growth engine (Level 1 ≈ 16 reviews market-median; Level 2 ≈ 78).

### 9.4 The first-five-orders operating rhythm (the entire cold start)

1. **Day one:** 4 gigs live, ID verified, Kickstart on ($15/mo), intro video + portfolio on all four, quick responses + auto-reply set, "available" status kept on.
2. **Daily:** Briefs sweep (personalized replies only, <1h), inbox sweep ×2 (NZST evening = US morning), five tailored off-platform posts (LinkedIn/X/dev communities) pointing at the gigs — the only ToS-safe traffic accelerator.
3. **Orders 1–5:** reply <30 min → over-scope in writing → deliver early with proof artifacts → follow up via Fiverr's flow only. Zero cancellations, 100% on-time. Every order gets one free extra (warranty note, "what could break" doc, bonus export format).
4. **At Level 1 (5 orders / 3 clients / $400):** add the automation gig (10 slots), enable Fiverr Ads on the two best-converting gigs, Seller Plus Standard, Briefs become a real channel (Success Score ≥7).
5. **Metrics to protect from day one:** response rate ≥90%, on-time 100%, zero cancellations — these feed the Success Score that gates everything else.

---

## 10. Sources

**Primary (Fiverr official — verified by the mechanics thread):**
- [Understanding Fiverr's freelancer levels](https://help.fiverr.com/hc/en-us/articles/360010560118-Understanding-Fiverr-s-freelancer-levels) — thresholds, 4/10/10/30 gig caps, benefit ladder
- [Fiverr's search and recommendation system](https://help.fiverr.com/hc/en-us/articles/37332082211217-Fiverr-s-search-and-recommendation-system) — relevance #1, ranking factors
- [Success score](https://help.fiverr.com/hc/en-us/articles/21965360854673-Success-score) — six areas, price-range benchmarking
- [Can't find your Gig?](https://help.fiverr.com/hc/en-us/articles/4599361153809-Can-t-find-your-Gig) — negative signals, off-platform sharing allowed
- [Seller Plus Kickstart](https://help.fiverr.com/hc/en-us/articles/27291415082257-Seller-Plus-Kickstart-Start-your-freelance-journey-strong) · [Standard & Premium](https://help.fiverr.com/hc/en-us/articles/360017140717-Seller-Plus-Standard-and-Premium-Advanced-tools-for-business-growth)
- [Fiverr Ads](https://help.fiverr.com/hc/en-us/articles/360017729338-Promoting-your-Gigs-with-Fiverr-Ads) — Level 1+ gate, CPC auction
- [Briefs (freelancer side)](https://help.fiverr.com/hc/en-us/articles/4415608857745-Personalized-offers-Briefs-for-freelancers) · [Briefs (buyer side)](https://help.fiverr.com/hc/en-us/articles/4415601609361-Post-a-project-brief-get-tailored-offers-for-your-project) — Success Score 7+ gate, 72h window, ≤5 offers
- [Response time & rate](https://help.fiverr.com/hc/en-us/articles/360011451678-Everything-you-need-to-know-about-response-time-and-rate) · [Auto-reply](https://help.fiverr.com/hc/en-us/articles/10092069817617-Set-up-your-auto-reply) — auto-reply doesn't count toward rate
- [Setting availability](https://help.fiverr.com/hc/en-us/articles/360015529197-Setting-Availability-for-freelancers) — >30 days/180 days ranking risk
- [Using AI on Fiverr](https://help.fiverr.com/hc/en-us/articles/37554976380177-Using-AI-on-Fiverr-Guidelines-for-freelancers-and-clients) — conditional disclosure
- [Policy violations](https://help.fiverr.com/hc/en-us/articles/47982844549905-Policy-Violations-Explained) · [Off-platform policy](https://help.fiverr.com/hc/en-us/articles/37554769759633-Stay-protected-Fiverr-s-off-platform-policy) · [Verify your identity](https://help.fiverr.com/hc/en-us/articles/13127850435345-Verify-your-identity)
- [How Fiverr works for freelancers](https://help.fiverr.com/hc/en-us/articles/34069565843985-How-Fiverr-works-for-freelancers) · [Best practices](https://help.fiverr.com/hc/en-us/articles/360010708757-Best-practices-for-Fiverr-freelancers) · [Top Rated freelancers](https://help.fiverr.com/hc/en-us/articles/15140188560913-Top-Rated-freelancers)
- [Gig policies](https://help.fiverr.com/hc/en-us/articles/360011421218-Gig-policies)

**Market data:** Hugging Face dataset [Ahad690/fiverr-gigs](https://huggingface.co/datasets/Ahad690/fiverr-gigs) (July 2026 scrape, analyzed locally — §2); live category/search pages via research threads: [Bug Fixes](https://www.fiverr.com/categories/programming-tech/software-development/bug-fixes), [QA services](https://www.fiverr.com/categories/programming-tech/qa-services), [Automations & Agents](https://es.fiverr.com/categories/programming-tech/software-development/automations-workflows).

**Lane research & pain-point sources:** [humansfix.ai](https://humansfix.ai/guides/common/fiverr-developer-broke-my-app), [stepto.net](https://stepto.net/blog/software-project-rescue-developer-ghosted-what-to-do), [techteems.com](https://techteems.com/what-its-like-to-fix-your-codebase-after-a-fiverr-disaster/), [Tendem Fiverr scraping teardown](https://tendem.ai/blog/fiverr-web-scraping-gigs-review), [Tendem managed-vs-freelancers](https://tendem.ai/blog/managed-scraping-services-vs-freelancers), [Trixly AI cost guide](https://www.trixlyai.com/blogs/how-much-does-custom-ai-agent-development-cost-in-2026), [Hotmolts wrapper critique](https://www.hotmolts.com/post/most-ai-agents-are-just-expensive-api-wrappers-wit-0e2ef9a9-9732-49f9-9c0f-02cce1563624), [White Beard Strategies](https://whitebeardstrategies.com/blog/what-do-you-say-when-a-client-asks-what-does-your-ai-actually-cost-and-who-fixes-it-when-it-breaks/), [Memvers price index](https://memvers.com/blog/freelance-price-index-2026), [Memvers AI disclosure](https://www.memvers.com/blog/ai-disclosure-rules-freelance-platforms-2026), [Fiverr IR — Claude Code surge](https://investors.fiverr.com/news-releases/news-release-details/businesses-race-hire-claude-code-specialists-demand-surges-938), [Wedbush vibe-coding report](http://investor.wedbush.com/wedbush/article/abnewswire-2025-11-11-report-how-to-fix-the-hidden-security-risks-of-vibe-coding-and-why-platforms-like-fiverr-are-becoming-the-go-to-solution), [safeguard.sh AI security study](https://safeguard.sh/resources/blog/autocomplete-anxiety-measuring-how-often-ai-coding-assistants-suggest-vulnerable-patterns), [smartremotegigs cold-start playbook](https://smartremotegigs.com/get-your-first-fiverr-client/), [hustlespire how-long-to-first-order](https://hustlespire.com/how-long-to-get-orders-on-fiverr/), [Fiverr Community credibility blog](https://community.fiverr.com/public/blogs/how-to-build-credibility-on-fiverr-when-you-have-no-reviews-2025-09-23), plus the community/Trustpilot threads cited inline in §7.
