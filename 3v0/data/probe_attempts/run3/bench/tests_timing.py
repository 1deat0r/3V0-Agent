#!/usr/bin/env python3
"""PROBE tests_timing.py: ref.py (O(n)) must be <20% of naive.py (O(n^2)) on the largest input (STAGE2)."""
import subprocess
import sys
import time

N = 30_000  # large enough that O(n^2) naive is far slower than O(n) ref


def time_sol(prog, inp):
    t0 = time.perf_counter()
    subprocess.run([sys.executable, prog], input=inp, capture_output=True,
                   text=True, timeout=120)
    return time.perf_counter() - t0


def main():
    # arbitrary sequence: many complements of target present -> nontrivial counting work
    a = [(i * 37) % 100000 for i in range(N)]
    inp = f"50000 {N}\n" + " ".join(str(x) for x in a) + "\n"
    r = time_sol("ref.py", inp)
    n = time_sol("naive.py", inp)
    ratio = r / n if n else float("inf")
    ok_ref = subprocess.run([sys.executable, "ref.py"], input=inp, capture_output=True,
                            text=True).stdout.strip()
    ok_na = subprocess.run([sys.executable, "naive.py"], input=inp, capture_output=True,
                           text=True).stdout.strip()
    agree = ok_ref == ok_na
    print(f"ref.py time:   {r:.4f}s")
    print(f"naive.py time: {n:.4f}s")
    print(f"ratio(ref/naive) = {ratio:.6f}  (need < 0.20)")
    print(f"ref==naive answer: {agree} (count={ok_ref})")
    if agree and ratio < 0.20:
        print("tests_timing: PASS (ref < 20% of naive on largest input)")
        sys.exit(0)
    print("tests_timing: FAIL")
    sys.exit(1)


if __name__ == "__main__":
    main()
