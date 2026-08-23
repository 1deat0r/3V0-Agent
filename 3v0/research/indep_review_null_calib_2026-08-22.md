# Independent review of the proposed "agent-variance calibration" next move — 2026-08-22
A hard re-check of the idea "establish a true agent-variance noise floor by re-running the probe
bank K≥ times under the agent's own body, replacing the degenerate 0-width band." This document
concludes that idea is the WRONG move and rejects it. Written BEFORE doing it, intentionally.

## Ground truth from the recorded data (verified in `probe_results.json`)
- Calibration §3 condition: `no-change (same frozen bank + same frozen attempt set runs 1-3; body
  state unchanged)`; aggregation `per-band pass rate per pass; mean/sd across K=5`.
- So the §3 calibration re-grades the SAME 23 attempt artifacts with K=5 fresh pinned subagents.
  `mean=1.0, sd=0.0` therefore asserts exactly ONE thing: **the pinned grader (temp=0, seed=0) is
  deterministic on fixed evidence.** It is NOT an estimate of the agent's run-to-run variance.
- The "0-width band" that results is the *mathematically correct* output of §3's own
  `mean ± 2*sigma_cal` rule given sigma_cal=0.

## Why the proposed move is wrong (three independent, fatal problems)

1. **It calibrates away the very signal the monitor exists to detect.**
   Run-to-run variability of the agent's ATTEMPTS is not grader noise — it is one of the two thins a
   pass-rate can move between (the other being real capability change). The monitor is explicitly a
   **weak, low-power surrogate that does NOT prove evolution** (EVOLUTION_PROBE §1, §10). If you
   fold agent-attempt variance into the noise floor, you subtract the thing you are trying to observe.
   The whole point of the frozen null is to FIX the reference while keeping the agent's side live and
   comparable — not to smooth the agent's side into the floor.

2. **It re-scopes a peer-reviewed, deliberately scoped spec.**
   EVOLUTION_PROBE v0.2 was revised 2026-08-18 after an ML/psych/SWE review that among other things
   pinned the grader precisely so the measured floor is adjudication reproducibility. The calibration's
   K-repeat over the GRADER is the design's choice. Re-running the AGENT to get an "agent-variance
   floor" is a §3 design change, not a bug fix — and it is a change the design text discourages.

3. **It is empirically likely to be a no-op AND expensive.**
   The frozen body passes 23/23 on the bank. Running that body K more times would most likely yield
   all-1.0 again → sd=0 again → the same 0-width gate, achieved at the cost of K full-bank agent runs
   (expensive; this is the agent's own labor). You would spend real compute to reproduce the same
   degenerate number.

## The actual (non-)problem and its cheaper truth
- A 0-width band does NOT cause false alarms in the final pipeline, because the §3 reproducibility
  gate (`apply_trend`, ≥2 consecutive runs) is the dampener for single-run excursions. One stray
  candidate never reaches `flagged`.
- The genuine limitation — small drift is undetectable at n=4-8/band, growth is not claimable — is
  ALREADY documented as §3 "Power honesty" ("only ≥30pp persistent shifts resolvable; the monitor
  says 'no measured change', never 'no change occurred'"). Nothing is broken; nothing needs fixing.
- The only honest improvement available is the DETECTION bound, not the grader-noise band: fold a
  binomial/Clopper-Pearson lower bound on the observed all-pass rate into the *interpretation* of a
  live run (e.g. easy n=5 → p≥0.55, medium n=8 → p≥0.69, hard n=6 → p≥0.61, escalated n=4 → p≥0.47
  at 95%). That is a §3 **design/gov decision for the operator to make** — not something to quietly
  do — and even then the monitor stays advisory.

## Verdict
REJECT the agent-variance re-calibration move. Do not spend agent runs on it. The 0-width gate is
correct behavior for a deterministic grader; the detector's real bound is the §3 power limit, already
on paper. The one legitimate follow-up is an OPERATOR-decided §3 amendment to interpret live-run
deltas against a binomial sampling floor instead of a grader-only band.

## What was done in the process (to keep the record honest)
- Corrected the earlier `_notes` entry that had framed the 0-width floor as a defect to "fix" — it now
  states it is expected/correct and warns against the agent-variance "fix" (the trap this review
  caught). No code change to `native/probe.py`; the `null_control` implementation and its tests are
  unchanged and remain valid.