# Forgetting archives never-used facts; projection is a usage signal

The rewire's retrieval seam caps the *view* at 2KB, but the *store* still
grows unboundedly: every recorded fact persists forever, including facts that
were added but never actually pulled into context. Forgetting is the store's
counterpart to retrieval's reinforcement — it archives facts that never earned
their keep, so the store tracks the agent's *actual* working knowledge rather
than everything it ever wrote down.

**Status:** accepted (design for Stone 24; the mechanism is specified here so
the implement stage has one target).

**The core subtlety — "used" is not "retrieved".** The wake-time profile
export deliberately projects with `touch=False` (a mechanical sync is not
evidence of use; touching would rich-get-richer the view into permanence —
locked by `test_export_does_not_inflate_feedback`). So a fact injected into
MEMORY.md every wake has `access_count == 0` forever. A forgetting policy
keyed on `access_count` alone would archive the facts that are, in fact, live
in context every turn. The policy must measure *use* as the union of explicit
retrieval and profile projection.

**Considered options:**

- *`access_count == 0` (naive):* archives every profile-projected fact.
  Wrong — conflates "never touched" with "touched, but projected
  touch=False".
- *Exclude the current working set (no schema):* forgetting recomputes the
  view and only archives facts outside it. No migration, but "current view"
  is a snapshot — a fact that fell out of the view on the run day (budget
  boundary) could be archived despite being near-live, and the forget path
  would re-derive the working set instead of reading a record of it.
- *`last_projected` column (chosen):* the profile export records, on each
  projected fact, an export timestamp — a *distinct, non-ranking* signal
  (`last_projected`), separate from the feedback counter. "In use" is then
  `access_count > 0 OR last_projected IS NOT NULL`. Robust (ever-projected is
  protected), provenance-aligned (the export is recorded, not recomputed), and
  it never touches ranking, so the rich-get-richer guard holds.

**Consequences:**

- `core/memdb.py` gains a nullable `last_projected` column (migration:
  `ALTER TABLE ... ADD COLUMN`, existing rows NULL — correct: nothing was
  projected under the pre-signal export). It is *not* a ranking input.
- The profile exporter (`project_memory` / `export_to_profile`) stamps
  `last_projected = now` on the projected working set — a write distinct from
  the `touch` feedback, so selection is unaffected.
- A new `core/forget.py`: a pure `stale_ids(conn, threshold_days, now)`
  selecting *active* facts of a forgettable kind with
  `access_count == 0 AND last_projected IS NULL AND age > threshold`, and a
  `forget(...)` that archives them (`valid_to = now`, source="forgetting").
- Forgettable kinds: `memory`, `user`. `identity` and `directive` are
  permanent — the agent's core identity and Prime Directive are never
  auto-archived.
- Threshold: 30 days (conservative; the store is young so nothing archives
  yet — the mechanism is exercised under short thresholds in tests, exactly
  as the rewire's `test_amnesia` drives the forget path).
- Archive, never delete: forgetting sets `valid_to` (recoverable via
  `fact_history`), matching the retract/supersede discipline. A forgotten
  fact can be re-recorded; its supersession chain stays intact.
