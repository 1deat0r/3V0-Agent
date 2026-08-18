#!/usr/bin/env python3
"""probe006: recursive ASCII directory tree with connectors and optional depth."""
import os
import sys


def list_entries(path):
    entries = [e for e in os.listdir(path) if e not in (".", "..")]
    return sorted(entries, key=lambda e: e.lower())


def walk(path, prefix, my_level, depth, cur):
    """Print children of `path`. my_level is this directory's tree level (root=0)."""
    entries = list_entries(path)
    for i, e in enumerate(entries):
        last = i == len(entries) - 1
        connector = "`-- " if last else "|-- "
        full = os.path.join(path, e)
        is_dir = os.path.isdir(full)
        name = e + ("/" if is_dir else "")
        cur.append(prefix + connector + name)
        if is_dir and (depth is None or my_level + 1 < depth):
            child_prefix = prefix + ("    " if last else "|   ")
            cur = walk(full, child_prefix, my_level + 1, depth, cur)
    return cur


def main():
    args = sys.argv[1:]
    depth = None
    if "-d" in args:
        i = args.index("-d")
        depth = int(args[i + 1])
        del args[i:i + 2]
    target = args[0] if args else "."
    base_name = os.path.basename(os.path.normpath(target))
    lines = [base_name + "/"]
    if depth is None or depth >= 1:
        lines = walk(target, "", 0, depth, lines)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
