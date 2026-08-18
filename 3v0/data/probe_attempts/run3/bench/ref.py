#!/usr/bin/env python3
"""PROBE ref.py: O(n) hash-map solution for "count pairs summing to target"."""
import sys
from collections import defaultdict


def solve(T, a):
    seen = defaultdict(int)
    ans = 0
    for x in a:
        ans += seen[T - x]
        seen[x] += 1
    return ans


if __name__ == "__main__":
    line1 = sys.stdin.readline()
    line2 = sys.stdin.read().strip()
    T, n = map(int, line1.split())
    a = list(map(int, line2.split()))[:n]
    print(solve(T, a))
