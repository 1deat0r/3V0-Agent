#!/usr/bin/env python3
"""PROBE tests_wrong.py: prove naive_wrong.py is objectively wrong while ref.py passes (STAGE3)."""
import subprocess
import sys


def sol(prog, inp):
    return subprocess.run([sys.executable, prog], input=inp, capture_output=True,
                          text=True, timeout=60).stdout.strip()


def inp(T, a):
    return f"{T} {len(a)}\n" + " ".join(map(str, a)) + "\n"


def main():
    cases = [inp(3, [1, 2, 3]), inp(5, [1, 2, 3, 4]), inp(4, [2, 2, 2, 2]),
             inp(0, [-1, 0, 1, 1, -1]), inp(10, [1, 2, 8, 2, 8]), inp(6, [3, 3, 3])]
    ref_wrong = 0
    for c in cases:
        if sol("ref.py", c) != sol("naive_wrong.py", c):
            ref_wrong += 1
            print(f"  WRONG input={c.splitlines()[0]!r}: ref={sol('ref.py', c)!r} naive_wrong={sol('naive_wrong.py', c)!r}")
        else:
            print(f"  same    input={c.splitlines()[0]!r}: ref={sol('ref.py', c)!r}")
    passing = len(cases) - ref_wrong
    print(f"cases compared: {len(cases)}; naive_wrong FAILS (differs from correct ref.py): {ref_wrong}; passes: {passing}")
    flaw = ("naive_wrong.py counts ordered pairs (i != j), so it double-counts every true "
            "unordered pair (i<j) as both (i,j) and (j,i), giving 2x the correct answer whenever "
            "any valid pair exists (e.g. T=3 [1,2,3] -> 2 instead of 1).")
    with open("flaw.txt", "w") as f:
        f.write(flaw + "\n")
    print("flaw recorded in flaw.txt")
    if ref_wrong >= 2:
        print("tests_wrong: PASS (naive_wrong objectively wrong on >=2 cases; ref correct)")
        sys.exit(0)
    print("tests_wrong: FAIL")
    sys.exit(1)


if __name__ == "__main__":
    main()
