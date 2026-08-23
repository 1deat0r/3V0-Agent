# Independent review of PROPOSAL-0001 (§3 binomial sampling floor) — 2026-08-22
Adversarial re-check of the draft proposal before it goes to the operator. Verdict at the end.
**Covers review pass 1 (draft) and re-review pass 2 (revised).**

## 1. Math verified (not assumed)
- The four Clopper–Pearson one-sided 95% lower bounds are correct and independently reproduced:
  easy n=5 → **0.549**, medium n=8 → **0.688**, hard n=6 → **0.607**, escalated n=4 → **0.473**
  (computed via scipy beta.ppf semantics reimplemented by exact-binomial bisection; no dependency).
- These are the honest "indistinguishable from the null's all-pass ceiling given n samples" floors.

## 2. Catching a real flaw in the first draft (fixed in the proposal)
The original §3 code sketch used `max(grader_lo, binomial_floor)` with a caveat. That is **incoherent**:
for an all-pass band `grader_lo = 1.0`, so `max` is always `1.0` and the amendment is a silent no-op —
the exact outcome the proposal must avoid. The fix (already edited in): detection `lo` is *replaced* by
the binomial floor; grader `sigma_cal` only ever *widens* it. This is the correct statistical reading:
grader σ measures grading determinism (an error term on top of sampling), never sampling itself, so it
cannot tighten a floor that sampling sets. A proposer version without this fix would be broken.

## 3. Does it double-count noise? — No, with one caveat
Grader reproducibility and sampling error are orthogonal sources of variance in a rate estimate; using
the binomial floor as the `lo` bound and grader σ as an upward widener is statistically sound. Caveat
(the distinction is invisible in the current data): `sigma_cal=0` only because all 23 graded PASS under
a no-change body; the formula must still be correct when grading is noisy (sd>0), which is the *widen,
never tighten* rule. The proposal documents this.

## 4. Real effect (what actually changes)
With the ≥2-consecutive-run gate in `apply_trend`, a single out-of-band run is already not flagged. The
amendment's material effect is for a **persistent** 1-task-per-band drop:
- today: easy 4/5 twice in a row → `0.8 < 1.0` → `regression-suspect`;
- with the floor: `0.8 > 0.549` → "no measurable change," even across two runs.
That is correct: at n=5, a persistent 4/5 is within binomial sampling of a still-perfect underlying
rate, so flagging it is a false alarm on an advisory signal. The monitor trades already-impossible
sensitivity (which §3 power-honesty already disclaims) for honesty. Because the signal is advisory
(§6) and never gates, this is the right trade.

## 5. Residual issues to flag to the operator (not blockers)
1. **Miss-rate increase is real but acceptable.** True small regressions (e.g. genuine 80% underlying)
   now won't be flagged at all until they fall below the floor (≈0.55–0.69/band). That is consistent
   with documented power honesty, but should be stated plainly: the monitor becomes *less* likely to
   cry wolf and *also* less likely to notice a modest real decline.
2. **Helper edge cases need pinning** before any patch: `n=0` (skip band), `observed_p=0` (floor 0),
   non-95% alpha not needed. Should be pre-registered in the applied version, not left to implementation.
3. **Test surface**: `thresholds()` changing when `use_binomial_floor=True` must not silently alter the
   existing `test_calibrate_and_thresholds` / `NullControlTest` (they call `thresholds(cal)` /
   `null_control` with explicitly-passed `th`). The flag should default `False` or be exercised
   explicitly so existing determinism tests are unaffected; the new path needs its own tests.
4. **Worth is marginal.** The monitor is already demoted and advisory. The concrete win is removal of
   false-positive "regression-suspect" on persistent sampling-likely partial drops. Reasonable, but an
   operator could reasonably decline as "too much machinery for a second-best surrogate" — with the
   ≥2-gate already damping noise, the marginal benefit is modest.

## 6. Verdict (review pass 1)
APPROVE the proposal **as amended** (with §2's `max`-vs-replace fix), subject to the operator accepting
the known miss-rate tradeoff (§5.1), with helper edge cases and the test-surface handling (§5.2–5.3)
as REQUIRED additions to the applied patch. Not a blocker, but note the marginal value (§5.4) so the
operator's approval is informed.

## 7. Re-review (review pass 2) — of the REVISED proposal
The revision folded in the four §5 items. Verified in the revised text:
- **§5.1 (miss-rate) → proposal §6**: now states plainly the monitor becomes *less* likely to cry wolf
  AND *less* likely to notice a genuine small/moderate decline, and that a real ~80% decline would no
  longer be flagged. Resolved. Also added an honest "marginal-value" note inviting the operator to
  decline — this is good governance, not self-sabotage.
- **§5.2 (helper contract) → proposal §3**: `regression_floor(n, observed_p, alpha=0.05)` pinned with
  edge rules (`n<=0` skip band; `observed_p<=0` → 0.0; alpha fixed at 0.05) and a note that floors are
  recomputed deterministically from the frozen bank. Resolved.
- **§5.3 (test surface) → proposal §3**: `use_binomial_floor: bool = False` **default**; new-path
  tests enumerated (edge table, a `True` threshold case, a `NullControlTest` persistent-drop case);
  existing tests explicitly required to pass unchanged. Resolved and correctly worded.
- **§5.4 (marginal value) → proposal §6**: surfaced to the operator. Resolved.

New-issue scan from the revision (found none):
- The `observed_p` parameter is only ever called here with `1.0`; the general signature is fine and
  its future generalisation does not leak.
- Cross-references: the proposal's own "§6" now means "Honest cost" and "§7" means "out of scope"; all
  textual `§6` references about advisory coupling correctly point at EVOLUTION_PROBE.md §6, not this
  doc — verified, no dangling refs.
- Grounding check: the recorded `null-control-460698e46` run has band distribution easy 5 / medium 8 /
  hard 6 / escalated 4, identical to `EXPECT_BANDS`, so the four floors (0.549/0.688/0.607/0.473) are
  correctly based on the actual per-band `n`, not an assumption.

## 8. Verdict (re-review pass 2)
APPROVE the **revised** proposal as written. All required add-ons are now in the text, the miss-rate
tradeoff and marginal value are surfaced honestly, and re-review found no new defects. Remaining open
point is purely the operator's governance decision, not a technical one. (No code changed; still
unapplied.) Do NOT re-open bank size or band composition (out of scope).