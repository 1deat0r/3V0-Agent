#!/usr/bin/env python3
"""PROBE naive.py: O(n^2) correct solution for "count pairs summing to target".

Deliberately quadratic (double loop) so it is far slower than ref.py on large n.
Correct: counts each distinct index pair i<j exactly once."""
import sys


def solve(T, a):
    n = len(a)
    ans = 0
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] + a[j] == T:
                ans += 1
    return ans


if __name__ == "__main__":
    line1 = sys.stdin.readline()
    line2 = sys.stdin.read().strip()
    T, n = map(int, line1.split())
    a = list(map(int, line2.split()))[:n]
    print(solve(T, a))
