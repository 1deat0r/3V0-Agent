# 3V0 EVOLUTION MONITOR v0.2

Status: REVISED 2026-08-18 after independent review (ML / psychology / software-eng).
Supersedes the v0.1 "PROOF" proposal. **The word "proof" is dropped.**

## What this is (demoted, honestly)
A **low-power, surrogate indicator** whose PRIMARY job is **regression floor monitoring**,
and which may offer only a *weak convergent hint* about growth. It does NOT prove
positive evolution. The only legitimate claim it can make, per the psychology review, is:

> "Performance on THIS fixed 20-30 task bank, graded by THIS pinned grader software,
> was X at T and Y at T+n."

It is one weak signal feeding a larger judgment — not a verdict, and never a gate.

## Accepted reviewer findings (v0.1 failures this fixes)
- ML: per-band n=5-8 is ~20-30x underpowered to resolve a 20-30pp shift; trend rule's
  "band of noise" was undefined -> **quantified + pre-registered noise floor** (§3).
- ML+Psych: the grader was "independent" but unpinned -> **pin the grader** (§4); its
  validity was unmeasured -> **calibration protocol** (§5).
- Psych: the "proof of evolution" goal outran the design -> **demoted** (above); grading
  was load-bearing -> **advisory only, decoupled from decisions** (§6).
- All: contamination cannot defeat Goodharting -> **acknowledged** (§7).
- SE: audit.sh / consistency.sh hardcoded absolute paths (break on repo move) ->
  **FIXED** (self-anchored, 2026-08-18).

## 1. Design principles
- **Held-out**: tasks NOT drawn from 3V0's repo/tests/past work. Kills self-graduation
  at the source (item level).
- **Frozen**: bank + rubric git-versioned at ship; same bank+rubric every cadence.
- **Difficulty-banded**: 5 easy / 8 medium / 6 hard / 3+ escalated (frontier walk).
  Easy+medium = regression sensitivity (floor); hard+escalated = growth hint (ceiling).
  Without both ends, a probe only measures one side.
- **Independent + pinned grader**: fresh-context subagent, BUT pinned (fixed model,
  version, temperature=0, seed), identity recorded per run, and calibrated (§4-5).
- **Pre-registered rubric + thresholds**: written before first attempt, frozen. Noise
  floor and trend thresholds quantified and pre-registered, not asserted.

## 2. Instrument
- 20-30 tasks, difficulty-banded, real work (coding, debugging, reasoning, planning,
  research synthesis, tool-chain use). Bank authored by an INDEPENDENT subagent so 3V0
  does not choose its own exam.
- Per task: {PASS, FAIL, INCONCLUSIVE} + outcome-justification. Composite = weighted
  per-band pass rate; frontier = highest band passed.
- Results appended to git-versioned `3v0/data/probe_results.json` (manual cadence; no
  cron per operator preference). Each run records: date, commit, grader identity
  (model+version+temp+seed), bank version, per-task verdicts, composite, frontier.

## 3. Noise floor + power (pre-registered before first trend run)
- **Calibration phase**: run the bank K=5 times under a controlled no-change condition
  (same body state, same grader) to estimate per-band variance. Record mean + sigma per
  band in `probe_results.json` as the declared noise floor.
- **Thresholds** (pre-registered): a band shift is "signal" only if it exceeds the
  calibration mean +/- 2*sigma_cal AND is reproducible across >=2 consecutive runs.
  Anything inside 2*sigma is noise and is reported as "no measured change".
- **Power honesty**: with n=5-8/band and binary outcomes, only large (>=30pp) persistent
  band shifts are resolvable from noise. Small drift is UNDETECTABLE; the monitor says
  "no measured change," never "no change occurred." This limit is stated, not hidden.
- **Frozen-agent null control (Phantom Gains, `2608.20290`; `native.probe.null_control`)**:
  claim "evolution" only ever as a **delta vs. a frozen null**, never as an absolute score.
  A **frozen snapshot of the agent** (fixed commit/body; same pinned grader; same frozen
  bank) runs through the identical pipeline and is recorded as a null-control run
  (`kind:"null-control"`, or the calibration-seed runs at a pinned commit). Each cadence
  run is reported as a live-vs-null per-band delta; a directional signal is accepted only
  when the LIVE rate is outside the calibrated band while the FROZEN NULL is inside it.
  If the NULL ITSELF falls outside the band (`null-drift`), the control is stale and the
  comparison is INVALID — re-freeze the null before trusting any live number. This closes
  the hole §3's grader-only calibration leaves open: that calibration bounds the grader's
  noise, but differencing two noisy estimates of the AGENT still manufactures phantom
  change unless one endpoint is fixed. The frozen null is that fixed endpoint.

## 4. Grading — pinned and independently regraded
- One grader model+version+temperature=0+seed, fixed for the life of the bank; identity
  written into every probe_results.json row so the line is comparable.
- Each run is graded by a fresh subagent applying the frozen rubric; 3V0 never grades
  itself. If grader identity must change, it is a bank/version event: run a bridging
  calibration, flag the line as non-comparable before/after.
- Grading is ADVISORY. Every verdict is a {PASS/FAIL/INCONCLUSIVE + reason} referencing
  an objective outcome where possible (hidden tests; artifact against stated spec).

## 5. Grader calibration / validity
- Before trusting the scoreline, grade a known-answer held-out subset (tasks with
  objective, pre-agreed expected outcomes). Measure grader accuracy vs expected.
- A human (operator) grades a small random subset each cadence as the calibration anchor
  for the subagent grader. Drift in human-vs-grader agreement >threshold is flagged.
- Until accuracy vs the known-answer subset is >= some pre-registered floor, the probe
  is treated as "uncalibrated" and its numbers are not even advisory.

## 6. Decision coupling (deliberately weak)
- Raw bank scores NEVER gate a revert or continue. They feed a judgment only.
- Revert-worthy regression is claimed ONLY by the layered floor (433-suite + baseline.sh
  + review); the probe is a corroborating signal, not the trigger.
- The probe can only ever say: "monitor flags N defeats in easy/medium band, consistent
  with regression; inspect." The inspect+revert decision stays independent of raw numbers.

## 7. Contamination & Goodhart (acknowledged, not over-claimed)
- Attempt order randomized; first-seen vs re-seen tracked per task; a task 3V0 encounters
  in real work is retired from the active bank.
- These mitigate, but CANNOT defeat Goodharting / memorization / learning-the-bank over a
  long horizon. Therefore: bank has a fixed lifetime (~N cadences) then is regenerated
  fresh by an independent subagent; the scoreline across regenerations is NOT directly
  comparable and is flagged as such.

## 8. Limits (honest)
- Surrogate-graded, not ground truth; degenerate without §5 calibration.
- Low power (§3); task-sampling bias; bank-staleness; LLM-judged != human-judged.
- A real shipped outcome (Fiverr, a split) remains the ultimate judge; the probe is a
  second-best continuous proxy.

## 9. Rollout (blocked on the above fixes)
1. Author the first bank + rubric by an INDEPENDENT subagent; freeze+commit. (DONE)
2. Run calibration phase (§3): K=5 noise-floor estimate; pre-register thresholds. (DONE)
3. Certify grader against known-answer subset (§5) to the pre-registered floor.
   (DONE; grader_cert_v1 6/6>=0.9)
4. **Freeze the null control**: pin the calibration-seed / first baseline attempt set at a
   fixed commit and record it as the frozen-agent null (`native.probe.null_control`).
   Every subsequent cadence run is compared to THIS null, not to its own earlier self.
5. First baseline probe run against the null; then cadence at milestones (manual).
6. At bank lifetime end, regenerate fresh (non-comparable line, flagged and re-null'd).

## 10. What this monitor now honestly asserts
- Strong: "3V0 is not regressing below the layered floor" (baseline.sh + suite + verify).
- Weak (surrogate): "per-band pass rates held/rose/dropped within/outside calibrated
  noise over the frozen period" — as an input to judgment, never a proof of evolution.
