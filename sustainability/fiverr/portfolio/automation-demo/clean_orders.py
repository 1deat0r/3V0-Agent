#!/usr/bin/env python3
"""Clean a weekly orders CSV: dedupe rows, fill blank prices, print a summary.

Stdlib only — no pip install. Fails loudly (clear message + exit code 1) on a
missing file or empty CSV; never silently writes wrong data.
"""
import argparse
import csv
import sys
from pathlib import Path


def clean(rows):
    """Dedupe (by id, keep last) and forward-fill blank prices. Pure function."""
    out, order, last_price = {}, [], None
    for r in rows:
        if r.get("price", "").strip() == "":
            r["price"] = last_price if last_price is not None else "0"
        last_price = r["price"]
        if r["id"] not in out:
            order.append(r["id"])
        out[r["id"]] = r  # last wins (overwrite)
    return [out[i] for i in order]


def main():
    ap = argparse.ArgumentParser(description="Clean a weekly orders CSV.")
    ap.add_argument("csv", help="input CSV path")
    ap.add_argument("-o", "--out", default="orders.clean.csv",
                    help="output path (default: orders.clean.csv)")
    args = ap.parse_args()

    path = Path(args.csv)
    if not path.exists():
        sys.exit(f"error: {args.csv} does not exist")

    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("error: input CSV has no rows")

    cleaned = clean(rows)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(cleaned)

    dupes = len(rows) - len(cleaned)
    print(f"cleaned {len(rows)} rows -> {len(cleaned)} "
          f"({dupes} duplicates removed); wrote {args.out}")


if __name__ == "__main__":
    main()
