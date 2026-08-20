# Store-first: the store is canonical, the profile is a derived view

3V0's memory and skill state live in the native store (`3v0/data/`), which is
the append-only, provenance-bearing source of truth; the 3V0 profile
(MEMORY.md / USER.md / SKILL.md) is re-exported from it as a projection.
This inverts 3V0's default (profile-as-origin) so nothing is ever silently
overwritten — corrections are supersessions with a recoverable audit trail,
and the profile can always be rebuilt from the store.

**Status:** accepted

**Considered options:**

- *Profile-as-origin (3V0 default):* simpler, but edits are destructive — a
  correction erases what it replaced, and history lives only in the session DB.
- *Store-as-origin (chosen):* the store is canonical and append-only; the
  profile becomes a derived view. Cost: two copies to reconcile, so drift is
  possible and must be checked.

**Consequences:**

- Every memory/skill write is mirrored into the store by a plugin bridge; the
  profile is a projection the reconciler keeps consistent.
- Drift between store and profile is a first-class, *checked* property (a
  healable continuity invariant), not an unmanaged failure mode.
