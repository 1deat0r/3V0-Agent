# Root-Cause Report — sample one-pager

*The named deliverable of the debug gig. Real bug, anonymized. Every fix-tier
order ships with a report in exactly this shape; the Basic "Reproduce +
Diagnosis" tier ships everything except the fix + test sections.*

---

## Symptom (client's words)

> "My bot stopped processing anything. It runs without errors, the logs look
> normal, but it silently skips every item as 'wrong project'."

No crash. No traceback. A system that looks alive but does nothing.

## Reproduction

1. Ran the script against a copy of the database — reproduced on the first
   attempt. The failure is deterministic, not intermittent.
2. Minimal repro: one session row + the `is-mine` check returns `False` for
   every session regardless of the real project.

## Root cause

The script read SQLite rows **by positional column index**:

```python
cwd = row[4]   # assumed column #4 was cwd
```

A `last_activity_at` column was later added **in the middle** of the schema.
The `SELECT` list was updated, but the reader still walked the tuple by
position — so index 4 now held a *timestamp*, not the project directory.
Every session looked like it belonged to a different project, and the
"is this mine?" check silently rejected all of them.

The tell: it appeared only after a schema change, and it never threw — it
just mis-read data.

## Why it stayed hidden

- No assertion or test tied the row reader to the schema.
- The failure mode was "wrong answer," not an exception — logs looked clean.

## The fix (Standard tier) + class fix (Premium tier)

Read by **column name**, never by position:

```python
rec = dict(zip(select, row))   # named, order-independent
cwd = rec.get("cwd") or ""
```

- **Order-independence:** keyed by name, a reordered schema can't shift data.
- **Schema-graceful:** a missing column is absent (`None`), never shifted.
- **Class fix:** this removes the entire *positional-read* bug class across
  the codebase — every other positional read got the same treatment.

## Regression test (proves the fix)

```python
# columns deliberately shuffled; reads must still return cwd correctly
assert load_session(db, sid)["cwd"] == "/expected/path"
```

If anyone reorders the schema again, the test fails **loudly** instead of the
bot silently skipping everything.

## Warranty

The fix carries a 14-day warranty: if this bug reappears in that window, the
fix is free.

---

*Representative sample: real bug, real code, edited only to remove
project-specific context. Gallery-sized rendering available in
`../assets/gallery-root-cause-report.png`.*
