#!/usr/bin/env bash
# probe023: reproducible demo of shortest.py across the three stages.
cd "$(dirname "$0")"
echo "== STAGE1a: simple 2-node chain (non-negative) =="
printf '2 1 0\n0 1 7\n' | python3 shortest.py
echo "== STAGE1b: s == t (2 nodes, edge away from s) =="
printf '2 1 1\n0 1 5\n' | python3 shortest.py
echo "== STAGE1c: diamond, all non-negative =="
printf '4 4 0\n0 1 1\n0 2 4\n1 3 3\n2 3 2\n' | python3 shortest.py
echo "== STAGE2: negative edges (no neg cycle) — honest BF =="
echo "# s=0, edges: 0->1 w5, 0->2 w-1, 2->1 w1; true d1 = -1+1 = 0 (not 5)"
printf '3 3 0\n0 1 5\n0 2 -1\n2 1 1\n' | python3 shortest.py
echo "== STAGE3: negative cycle reachable from s =="
echo "# 0->1 (1), 1->0 (-2) => cycle weight -1 < 0"
printf '2 2 0\n0 1 1\n1 0 -2\n' | python3 shortest.py
