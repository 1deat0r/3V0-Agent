# Liar puzzle (probe004)

Let each person be T (truthful) or L (liar). A liar's statement is false; a truth-teller's is true.

Let X_A = assigned truth value of A's statement, etc. Work by cases.

- If A is truthful, then "B is a liar" is true ⇒ B is a liar. If A is a liar, then "B is a liar" is false ⇒ B is truthful.
  So A and B are always **opposites**: exactly one of {A, B} is truthful.

- D says "Exactly one of A and B is a liar." Since exactly one of A, B is a liar, **D's statement is true ⇒ D is truthful**.

- C says "D is a liar." D is truthful, so C's statement is false ⇒ **C is a liar**.

- B says "C is a liar." C is a liar, so B's statement is true ⇒ **B is truthful**.

- A says "B is a liar." B is truthful, so A's statement is false ⇒ **A is a liar**.

Assignment: **A = liar, B = truth, C = liar, D = truth.** Every statement is consistent (A false, B true, C false, D true).

**Final answer: 2 liars: A and C**
