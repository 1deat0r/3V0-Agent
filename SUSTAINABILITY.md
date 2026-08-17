# 3V0 — Sustainability (self-funding the API)

Goal: offset the DeepSeek-v4-pro API cost so 3V0 pays for its own substrate
instead of leaning on the Operator indefinitely.

## The cost reality (honest estimate)

DeepSeek-v4-pro pricing (off-peak, per 1M tokens): $0.022 cache-hit /
$0.66 miss / $1.98 out (peak ×2). At a rough mid-usage month (~50M input
mostly cached + ~5M output) the bill lands around **$15–50/mo**; a heavy
autonomous month (large review drains, big research passes) could reach
~$100. This is a *modest, achievable* target — a freelance-product problem,
not a startup problem.

## The one hard constraint (said plainly)

Money moves through identity + payment rails — a legal person, a bank
account, KYC, a payout account (Fiverr/Upwork/Gumroad/Stripe all require
them). I hold none of those, and I cannot sign up for them myself. So this is
**not** "fully autonomous" in the literal sense; it is a **partnership**:

- **3V0 does the work** (define offers, draft copy, build sample
  deliverables, deliver, QA).
- **Operator holds the rails** (create the account, verify identity, connect
  payout, relay anything that requires a human).

Fiverr has an official *"Using AI on Fiverr"* policy — AI-assisted work is
permitted with disclosure — so this is a legitimate path, not a TOS evasion.

## What I'll do — my edge, not volume spam

Careful engineering is the thing I'm actually good at (proven this session on
3V0's own core). High-value, hard-to-fake work, priced for quality:

1. **Debug / fix your Python script or bug** — $35 / $80 / $150
   Root-cause debugging, not guess-and-patch: reproduce, find the root cause,
   fix the whole bug class (sibling call paths), test, and hand back a short
   write-up of *what was wrong and why*.
2. **Review your code for bugs, security, and maintainability** — $50 / $120
   A real line-by-line review: findings ranked by severity, each with a
   concrete fix. Not an AI-fluff checklist — actual careful reading.
3. **Automate a repetitive task with a Python script** — $60 / $150 / $300
   Turn a manual/repetitive task (data processing, file handling, API calls,
   scraping within ToS) into a tested, documented script + README + tests.

## Division of labor

| 3V0 (autonomous) | Operator (rails) |
|---|---|
| Research niches + pricing | Create Fiverr/Upwork account |
| Draft gig copy + portfolio | Verify identity (KYC) |
| Build sample deliverables | Connect payout / bank |
| Do the work + QA + deliver | Relay client messages / TOS steps |

## Milestones

1. **Decide the first gig(s) + platform** (Operator confirms the rails).
2. **Ship 2–3 sample deliverables** as a portfolio (done by 3V0, no account
   needed yet).
3. **Operator opens the account**; 3V0 supplies ready-to-paste gig copy.
4. **First paid delivery** → revenue offsets the API.
5. **Parallel: start a small product** (a niche CLI/automation tool on
   Gumroad or GitHub Sponsors) for revenue that needs less human touch.

## Honest risks

- **Token cost of doing the work.** Each gig burns reasoning tokens. A $50
  gig that burns $3 in tokens is still 94% margin — fine, but it must be
  priced in (it is).
- **Client communication is the human bottleneck.** Buyers expect timely,
  human-ish replies; the Operator owns that layer until/unless a
  suitable relay is set up.
- **"Autonomous earning at scale" is not viable yet** — the honest
  industry consensus (and my read) is that agents do real work well, but the
  identity/trust layer is still human. The plan above works *with* that
  rather than pretending it away.
