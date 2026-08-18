# Count of digit '1' from 1 to 999 (probe016)

**Answer: 300.**

### Per-position derivation
Count digit '1' in each decimal place across 000..999 (writing leading zeros, which add nothing):

- **Hundreds place:** '1' appears in 100–199 → **100** occurrences.
- **Tens place:** '1' appears in each ten-block (10–19, 110–119, 210–219, …, 910–919) = 10 blocks × 10 = **100** occurrences.
- **Units place:** '1' appears once in every block of ten (1, 11, 21, …, 991) = 100 blocks × 1 = **100** occurrences.

Total = 100 + 100 + 100 = **300**.

The number 000 contributes no '1', so the total is unchanged when counting 1..999 instead of 000..999.

### Brute-force verification (code-verified, not assumed)
```python
>>> sum(str(n).count("1") for n in range(1, 1000))
300
```
The per-position count matches the exhaustive count. Final answer: **300**.
