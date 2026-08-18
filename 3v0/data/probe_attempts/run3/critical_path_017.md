# Earliest completion time for task H (probe017)

**Answer: the earliest H can complete is 17 hours.**

### Critical paths (both sum to 17)
1. **A1 → C → E → F → H** = 2 + 4 + 2 + 3 + 4 = **17**
2. **A1 → B → D → F → H** = 2 + 3 + 5 + 3 + 4 = **17**

### Why 17 is the earliest
H depends on F (3h), and F's predecessors are E (2h) and D (5h). The two full chains above are the longest paths from A1 to H; the earliest H can finish equals the longest (critical) path through the DAG, because every step on that path must finish before H can begin. Both chains give 17, so 17 hours is the completion time. Any chain involving alternatives (if they exist) is strictly shorter and does not delay H.
