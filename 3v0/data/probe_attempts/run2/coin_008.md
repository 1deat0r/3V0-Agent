# Greedy counterexample for [1, 6, 10] (probe008)

**Answer: A = 12.**

### Greedy selection for 12
Take the largest coin ≤ remaining each time:
- 12 ≥ 10 → take **10**, remaining 2
- 2 ≥ 1 → take **1**, remaining 1
- 1 ≥ 1 → take **1**, remaining 0

Greedy uses **10 + 1 + 1 = 3 coins**.

### Optimal selection for 12
- **6 + 6 = 12** uses **2 coins**.

So greedy uses 3 coins > the minimum 2 coins. **Greedy is suboptimal for 12.**

### Why 12 is the SMALLEST counterexample
Check every amount 1..11 with greedy vs optimal:
- Coins ≤ 10: amounts 1,6,10 use exactly 1 coin (greedy = optimal).
- 2 = 1+1 (greedy 2, optimal 2); 3=1+1+1; 4; 5 → greedy 4–5 coins, optimal same (only 1s).
- 7 = 6+1 (greedy 7: take 6, then 1; 2 coins; optimal 2).
- 8 = 6+1+1 (greedy 3, optimal 3).
- 9 = 6+1+1+1 (greedy 4, optimal 4).
- 11 = 10+1 (greedy 2, optimal 2).

Every amount 1..11 is greedy-optimal; **12 is the smallest amount where greedy is worse than optimal.**
