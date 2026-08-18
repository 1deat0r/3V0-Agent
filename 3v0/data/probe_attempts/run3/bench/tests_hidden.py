#!/usr/bin/env python3
"""PROBE tests_hidden.py: deterministic exact-stdout cases for ref.py (STAGE1)."""
import subprocess
import sys

CASES = [
    ("3 3\n1 2 3", "1"),
    ("5 4\n1 2 3 4", "2"),
    ("4 4\n2 2 2 2", "6"),
    ("6 3\n3 3 3", "3"),
    ("10 5\n1 2 8 2 8", "4"),
    ("9 4\n1 1 2 2", "0"),
]


def run_case(inp):
    out = subprocess.run([sys.executable, "ref.py"], input=inp, capture_output=True,
                         text=True, timeout=30)
    return out.stdout.strip(), out.returncode


def main():
    fails = 0
    for inp, expected in CASES:
        got, rc = run_case(inp)
        if rc != 0 or got != expected:
            fails += 1
            print(f"HIDDEN-FAIL input={inp!r}: expected {expected!r} got {got!r} rc={rc}")
    if fails:
        print(f"tests_hidden: {fails}/{len(CASES)} failures")
        sys.exit(1)
    print(f"tests_hidden: {len(CASES)} deterministic cases PASS")


if __name__ == "__main__":
    main()
