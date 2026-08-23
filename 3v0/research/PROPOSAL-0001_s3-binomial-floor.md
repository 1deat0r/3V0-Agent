# PROPOSAL-0001 — §3 binomial sampling floor for live-run detection
**STATUS: DRAFT PROPOSAL — NOT APPLIED.**
Author: assistant (for operator review). Date: 2026-08-22.
Governance call: amends EVOLUTION_PROBE.md §3 (frozen, peer-reviewed). Takes effect only if the
operator approves; until then the spec and `native/probe.py` are unchanged.

This file is intentionally a candidate text, not a change set. Criticize it freely.

---

## 1. Problem (in one paragraph)
The §3 detection thresholds are `calibration mean ± 2*sigma_cal`. Under a no-change body the three
recorded runs all passed 23/23, and the K=5 calibration re-graded that same evidence — so
`sigma_cal = 0` and every band's detection band is `[1.0, 1.0]`. Because the grader is deterministic on fixed
evidence, the monitor currently treats ANY live pass rate below 1.0 as "out of band," even though
with only n=4–8 tasks per band the *sampling* of a still-unchanged agent can legitimately land
below 1.0 by pure luck. We are confusing "the grader is perfectly consistent" (true, sigma_cal=0)
with "we can detect a 5% decline" (false at these sample sizes — the §3 power-honesty clause already
admits only ≥30pp shifts are resolvable, but the concrete detection threshold contradicts that by
sitting at 1.0).

## 2. Proposed amendment (§3 text replacing the "Thresholds" bullet)
> **Thresholds (pre-registered, amended PROPOSAL-0001):** the *detection* lower bound per band is
> the **one-sided 95% binomial (Clopper–Pearson) lower bound on the frozen null's observed pass
> rate**, computed from that band's task count `n` (from the frozen bank). With the current all-pass
> null this is: easy `n=5 → 0.549`, medium `n=8 → 0.688`, hard `n=6 → 0.607`, escalated `n=4 → 0.473`.
> A live band rate is `regression-suspect` only if it falls **below that floor** and is reproducible
> across ≥2 consecutive runs (the §3 gate is unchanged). Rates above the floor are reported as
> "no measurable change," never as "no change occurred" (power-honesty retained). The calibration
> `mean ± 2*sigma_cal` band is retained **only as an upper/growth-side and grader-reproducibility
> diagnostic** and does not narrow the regression floor, because `sigma_cal` measures grading
> determinism, not sampling.

*(The `hi` side stays 1.0: an all-pass band cannot exceed itself. The grader `sigma_cal` would only
widen the floor upward if grading were noisy, i.e. the binomial floor is the floor; grader noise can
only raise it, never lower it.)*

## 3. The intended code delta (sketch, not a patch)
- Add a small, stdlib-only helper in `native/probe.py`:
  `regression_floor(n: int, observed_p: float, alpha: float = 0.05) -> float`
  returning the one-sided Clopper–Pearson lower bound (inverse incomplete-beta via stable bisection,
  like the one already used to sanity-check in review).
- `thresholds()` gains an optional `use_binomial_floor: bool = False`; when **False** (default) the
  current behaviour and existing determinism tests are unchanged; when **True**, each band's detection
  `lo` is **replaced** by the binomial floor for the regression bound (`regression_floor(n, 1.0)`),
  and grader `sigma_cal` is used only to **widen upward** (raise `lo`) when grading is noisy —
  NOT via `max(grader_lo, floor)`, because for an all-pass band `grader_lo=1.0` would always win and
  make the amendment a no-op. See §4.2 for the explicit ruling on this.
- **Pre-registered helper contract** (pinned now; not left to implementation):
  `regression_floor(n: int, observed_p: float, alpha: float = 0.05) -> float`, one-sided
  Clopper–Pearson lower bound via stable bisection of the exact binomial tail. Rules:
  `n <= 0 -> skip band` (no floor, band omitted from detection); `observed_p <= 0.0 -> 0.0`
  (nothing is below the floor); `alpha` fixed at `0.05` (no other alpha sinks in). Every band's floor
  is recomputed deterministically from the frozen bank's `n`; no randomness and no new data.
- **Tests required in any applied patch** (not optional): new cases for `regression_floor` edge
  table above + a `use_binomial_floor=True` `thresholds()` case and a `NullControlTest` case
  asserting a persistent 1-task band drop becomes `"no measurable change"`. Existing tests must pass
  unchanged because `use_binomial_floor` defaults `False`.
- `data/probe_results.json` records the amendment as applied (new `_notes` entry + a
  `binomial_floor_v1` dict per band) so the threshold change is auditable and reversible.

## 4. Deliberate choices the operator should confirm
1. **One-sided 95%**, not 90% or 99%. 95% matches the existing §3 sigma=2 (≈95%) spirit while
   staying a regression-only (one-sided) claim — we are not claiming growth from the floor.
2. **Binomial floor replaces, not merely widens, the degenerate `lo=1.0`.** This is the crux. If we
   instead did `lo_eff = max(grader_lo, binomial_floor)`, the answer would stay `1.0` (because grader
   lo is 1.0) and the amendment would be a no-op. The proposal's position is that grader `lo=1.0`
   asserts grading determinism, not sampling certainty, and is therefore the *wrong* value to detect
   against. Confirm this reading of the stats before approving.
3. **Applies only to regression detection on the `lo` side.** Growth (`hi`) is unchanged and remains
   "not claimable" (power honesty), consistent with §1.
4. **Advisory-only scope is unchanged.** The floor lowers the false-alarm rate of an advisory signal;
   it never gates a decision (EVOLUTION_PROBE §6).

## 5. What this does and does not do
- **Does**: stops the monitor from flagging a small, sampling-expected partial band drop as suspicious
  for a band of only 4–8 tasks. Makes the monitor's stated power-honesty consistent with its actual
  detection threshold. Concretely: a *persistent* 1-task-per-band drop (e.g. easy 4/5 twice in a row,
  which today is "regression-suspect") becomes "no measurable change," because at n=5 a 4/5 is within
  binomial luck of a still-perfect underlying rate.
- **Does NOT**: increase statistical power (n is fixed by the bank), detect small drift, claim growth,
  or change the ≥2-consecutive-run reproducibility gate, the grader pinning, the frozen-null control,
  or §6 advisory coupling.

## 6. Honest cost the operator must accept (informed approval)
The floor is a **regression-only, lenient** change: a live band rate above the floor is "no measurable
change" — even across ≥2 consecutive runs. So a *modest but real* decline (e.g. underlying truth
drops to ~80%) will now NOT be flagged at all, because ~0.8 exceeds every band's floor (0.47–0.69).
The monitor becomes **less likely to cry wolf AND less likely to notice a genuine small/moderate
decline**. This is consistent with §3 power-honesty ("small drift is undetectable") but is a real
sensitivity loss, not a free lunch. It is acceptable only because the signal is purely advisory (§6)
and never gates a decision. If the operator wants the monitor to also catch modest declines, this
proposal is the wrong lever (that would require more tasks per band, which is out of scope).

**Marginal-value note, kept honest:** the monitor is already a demoted, low-power, advisory second-best
surrogate, and the existing §3 ≥2-consecutive-run gate already dampens single-run noise. The concrete
win here is narrow (removing false-positive `regression-suspect` on persistent sampling-plausible
partial drops). A fully informed operator may reasonably decide this is too much machinery for a
second-best surrogate and decline — that is a valid outcome, not a missed defect.

## 7. Explicitly out of scope (why)
- Re-running the agent for an "agent-attempt variance" floor — rejected (see
  `indep_review_null_calib_2026-08-22.md`): it calibrates out the very signal the monitor observes.
- Any change to the bank size `n` or band composition (`EXPECT_BANDS`).

---

## Independent review verdict (companion: `indep_review_PROPOSAL-0001.md`)
**APPROVE — revised version, review pass 2.** The `max`→replace fix (§4.2), the helper edge-case
contract, and the `use_binomial_floor=False` default + new-path tests are all now in the text (§3);
the miss-rate tradeoff and marginal-value note are surfaced (§6). Full reasoning (including the review
that caught the original `max` no-op flaw) in the companion review. Remaining open point is the
operator's governance decision, not a technical one. Still NOT APPLIED.