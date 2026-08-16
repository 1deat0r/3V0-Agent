# The continuity clock checks before it heals

The clock evaluates every invariant and reports drift *before* running the
safe mechanical heal, and healable invariants are only ever healed after
being checked. If heal ran first, healable drift would be fixed before it was
ever observed — the clock would report clean on exactly the corruption it
exists to catch (self-fulfilling).

**Status:** accepted

**Consequences:**

- The tick order (sync → drain → drift → continuity) is load-bearing and
  locked by a regression test; reordering it silently re-breaks drift
  detection.
- Only *healable* drift is auto-fixed; semantic drift is never auto-healed.
