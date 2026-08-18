#!/usr/bin/env python3
"""PROBE naive_wrong.py: counts ORDERED pairs (i != j), so it double-counts every
actual pair. Objectively wrong whenever a valid pair exists."""


def solve(T, a):
    n = len(a)
    ans = 0
    for i in range(n):
        for j in range(n):
            if i != j and a[i] + a[j] == T:
                ans += 1
    return ans


if __name__ == "__main__":
    import sys
    line1 = sys.stdin.readline()
    line2 = sys.stdin.read().strip()
    T, n = map(int, line1.split())
    a = list(map(int, line2.split()))[:n]
    print(solve(T, a))
