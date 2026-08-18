# Problem: count pairs that sum to a target

**Input** (stdin):
- Line 1: `T n` — target integer, then the number of elements.
- Line 2: `n` space-separated integers `a_0 a_1 ... a_(n-1)`.

**Output** (stdout): exactly one integer — the number of **distinct index pairs** `i < j` such that `a[i] + a[j] == T`.

Examples (input line2 shown as the array; output is the count):
- `T=3`   `1 2 3`        -> `1`   (only pair 1+2)
- `T=5`   `1 2 3 4`      -> `2`   (1+4, 2+3)
- `T=4`   `2 2 2 2`      -> `6`   (all 4 choose 2 = 6 index pairs sum to 4)
- `T=6`   `3 3 3`        -> `3`   (three distinct-index pairs of 3+3)
- `T=10`  `1 2 8 2 8`    -> `4`   (each 2 pairs with each 8: 2×2 = 4 index pairs)
- `T=9`   `1 1 2 2`      -> `0`   (no pair sums to 9)
