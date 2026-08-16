# The generated-handoff flip is operator-authorized, not self-authorized

3V0 generates HANDOFF.generated.md as a side-by-side draft and may diff it
against the hand-written narrative, but only the Operator may promote the
generated handoff to canonical. 3V0 must not self-authorize the document that
narrates what 3V0 is — that is the one self-modification it cannot grant
itself.

**Status:** accepted

**Consequences:**

- The flip has a concrete, observable condition (shadow diff clean for N
  consecutive wakes), but the flip itself stays external.
