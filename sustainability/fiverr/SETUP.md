# Fiverr seller onboarding — the rails (operator does this, ~10 min)

The sustainable split: **your account + identity + payout (the rails); the
agents' disclosed, hand-verified work (the deliverables).** This file is the
paste-ready walkthrough for your side. The agents cannot do these steps —
they're yours by design — but everything you paste is already written (see
`gigs.md` for the five gigs and `profile.md` for the seller profile).

> **Security: do this yourself in a private window.** Never share your
> password, SMS codes, or ID with anyone — including the agents. They don't
> need your credentials; they only need the finished gigs to exist.

## What you do (only you can)

1. **Use your EXISTING account (@mustbearn)** — do NOT create a second one
   (one account per person, ever — a second account is a bannable violation).
   Switch it to selling mode: click your **avatar (top right) → "Switch to
   Selling" / "Become a Seller"**; if that's missing, open
   **fiverr.com/start_selling** directly while logged in. NOTE: the footer
   "Become a Fiverr Freelancer" link can bounce you back to the buyer home —
   the onboarding screen you want says **"Create your freelancer profile."**
   The client profile stays; selling mode is added to the same account.
2. **Verify email** — click the confirmation link.
3. **Add + verify phone** — Fiverr texts a code; enter it.
4. **Profile** — paste the description from `profile.md`; add a profile photo,
   a display name of your choosing, and the **intro video** (script in
   `intro-video-script.md`, ~60s — it's a ranking + trust lever).
5. **Publish 4 of the 5 gigs** — for each, paste title / category / tags / tiers /
   description / FAQ / requirements from `gigs.md` (pricing is already
   market-validated). **New sellers are capped at 4 active gigs** (verified
   against Fiverr's levels policy, 2026) — publish **debug, code review, AI
   agent, web scraping** first and keep **workflow automation** in draft until
   Level 1 unlocks more slots. Full reasoning in `COMPETITOR_ANALYSIS.md` §5.
6. **Gig images + portfolio** — upload a clean cover per gig (covers in
   `assets/`), add the gallery proof images (`assets/gallery-*.png`) as
   second/third images, and attach the spec-work portfolio pieces
   (`portfolio/` — see its README for which piece goes on which gig). At 0
   reviews, these artifacts *are* the social proof.
7. **Identity verification (KYC)** — government ID + a live selfie. Mandatory
   before your first payout, and usually before gigs go live.
8. **Payout method** — PayPal, Payoneer, or bank transfer.
9. **Tax form** — W-8/W-9 (US) or the non-US equivalent.
10. **Quick Responses** — save the templates from `quick-responses.md` and set
    the auto-reply (acknowledgment only; the manual reply is what counts
    toward your response rate).

## What the agents do (disclosed AI-assisted, hand-verified)

- 3V0 delivers Gigs 1–3 (debug, code review, workflow automation).
- Axiom delivers Gigs 4–5 (AI agent/chatbot, web scraping).
- 3V0 coordinates: drafts every buyer reply (you relay), routes each order to
  the right agent, and tunes gigs/pricing/positioning as data comes in.

## Multiple agents → multiple gigs, never multiple accounts

Fiverr allows **one seller account per person** — operating multiple accounts
is a bannable violation (detected via IP, device fingerprint, and payment
overlap; a second account also can't pass KYC without your one identity).
The legitimate structure is **one account, multiple gigs**: 3V0's gigs and
Axiom's gigs live on the same account, differentiated into different lanes so
they don't cannibalize. Reviews and levels compound across all gigs on the one
account. (Gig allowance: 4 as a New Seller, 10 from Level 1 — see
`COMPETITOR_ANALYSIS.md` §5 and §8.)

## After you're live

Tell 3V0 the gig URLs. 3V0 will then: monitor the gigs' performance, adjust
pricing/positioning from order + market data, and be ready to deliver the
first order.

## First-week scam playbook (they come for new gigs immediately)

Scam bots message every freshly published gig. Pattern: "I placed your
order," a claim to check an external site, a QR code, or a Telegram invite.

**Never:** click external links, scan QR codes, log in anywhere, or talk
off-platform. A real order always appears under **Orders** first.

**Do:** verify in Orders → reply at most once, on-platform: "I don't see an
order on my side. All orders go through Fiverr, and I'll start as soon as one
appears there." → **Report** the user (spam/scam) → block if available.
Repeat for every such message; it costs 20 seconds and trains the filters.
