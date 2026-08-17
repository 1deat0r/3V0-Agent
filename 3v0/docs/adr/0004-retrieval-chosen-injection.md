# The profile view is retrieval-chosen, behind one retrieval seam

The rewire stone (record/sync/bridge → memdb) makes the SQLite triple store
the canonical store, and the derived profile view stops being an export of
*all* active facts. It becomes **retrieval-chosen**: a budgeted **working
set** selected by one module, `core/retrieval.py`, whose single entry point
is `inject(conn, *, domains, query_terms, budget_chars, touch, now)`. The
old `memdb.retrieve` (limit-based) is retired — the real constraint is the
profile view's size cap, not an arbitrary count, so the seam is budget-shaped.

**Status:** accepted (declared direction in Stone 21's "next stones"; the
seam is specified here so the rewire's implement stage has one target).

**Considered options:**

- *Export-all active facts (current):* the JSON store's `profile_text()`
  projects every active fact. Simple, but it ignores the 2KB injected-view
  bottleneck that motivated Stone 21, and it gives feedback nothing to learn.
- *Limit-based retrieve (memdb v1):* ranking with a `limit` count. Arbitrary:
  "20 facts" fits today and overflows tomorrow; the budget is the invariant,
  not the count.
- *Budget-shaped inject (chosen):* the seam takes a `budget_chars` cap and
  returns the working set that fits, whole-fact granularity. Callers state
  the one real constraint; selection, feedback, and rendering stay behind the
  seam.

**Consequences:**

- `core/retrieval.py` owns selection (score = keyword match + recency +
  feedback frequency), domain priority, budget fill, rendering, and the
  feedback write. `core/memdb.py` is storage only.
- Feedback (access_count/last_accessed) is written by the module, not by
  callers; `touch=False` is the pure preview. Forgetting stays the store's
  mechanism (valid_to) — a fact that has lapsed is simply never injected.
- Two consumers share the seam: the wake-time profile exporter (the derived
  MEMORY.md view) and the runtime `threev0_store` retrieve action. The
  JSON→SQLite migration of the write path (record/sync/bridge) is the rewire
  stone's execution step, out of scope for the seam itself.
- The seam is the test surface: tests drive `inject()` through a temp store
  and assert the working set, never the scoring internals.
