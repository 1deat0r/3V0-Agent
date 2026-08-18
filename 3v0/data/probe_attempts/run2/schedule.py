#!/usr/bin/env python3
"""probe012: max non-overlapping meetings, greedy on earliest finish.
A meeting (s,e) may be followed by one that starts exactly when it ends (== allowed)."""
import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        print(0)
        return
    n = int(data[0])
    meet = []
    idx = 1
    for _ in range(n):
        s = int(data[idx]); e = int(data[idx + 1]); idx += 2
        meet.append((s, e))
    meet.sort(key=lambda x: (x[1], x[0]))  # greedy: earliest end
    count = 0
    prev_end = -1
    for s, e in meet:
        if s >= prev_end:
            count += 1
            prev_end = e
    print(count)


TESTCASES = {
    "A": "3\n2 4\n1 3\n3 5\n",   # expect 2
    "B": "0\n",                   # expect 0
    "C": "1\n1 1\n",              # expect 1
    "D": "3\n1 3\n3 6\n6 9\n",    # expect 3 (boundary chaining)
    "E": "3\n5 7\n1 3\n3 5\n",    # expect 3
}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        for name, inp in TESTCASES.items():
            print(f"Input {name}:", end=" ")
            main.__globals__["sys"].stdin = __import__("io").StringIO(inp)
            main()
    else:
        main()
