#!/usr/bin/env python3
"""probe015: fix race on shared counter. counter += 1 is not atomic in CPython
GIL era; the read-modify-write can interleave across threads on a hot counter.
Correct fix: guard the increment with a threading.Lock (mutual exclusion)."""
import threading

counter = 0
lock = threading.Lock()


def worker():
    global counter
    for _ in range(1_000_000):
        with lock:            # make the non-atomic increment mutually exclusive
            counter += 1


threads = [threading.Thread(target=worker) for _ in range(8)]
for t in threads:
    t.start()
for t in threads:
    t.join()
assert counter == 8_000_000, counter
print('OK', counter)
