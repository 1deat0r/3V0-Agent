# Sample deliverable — "automate your task" gig

*Representative format: a small real CLI, its README, and a test — what every
"automation" order ships with.*

---

## The task (as the client described it)

> "I get a CSV of orders every week with duplicate rows and blank prices. I
> want a command that cleans it — drops dupes, fills missing prices from the
> previous row — and prints a short summary. It should be something I can run
> myself."

## Deliverable 1 — `clean_orders.py`

```python
#!/usr/bin/env python3
"""Clean a weekly orders CSV: dedupe rows, fill blank prices, print a summary."""
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
```

## Deliverable 2 — `README.md`

```
# clean_orders

Dedupe an orders CSV (by id, keeping the last row) and forward-fill blank
prices from the previous row. Stdlib only — no pip install.

    python3 clean_orders.py orders.csv            # writes orders.clean.csv
    python3 clean_orders.py orders.csv -o out.csv # custom output

Fails with a clear message (not a traceback) on a missing file or empty CSV.
```

## Deliverable 3 — `test_clean_orders.py`

```python
import unittest
from clean_orders import clean

class TestClean(unittest.TestCase):
    def test_dedupe_keeps_last(self):
        rows = [{"id": "1", "price": "5"}, {"id": "1", "price": "9"},
                {"id": "2", "price": "7"}]
        out = clean(rows)
        self.assertEqual([r["id"] for r in out], ["1", "2"])
        self.assertEqual(out[0]["price"], "9")  # last wins

    def test_fills_blank_price_from_previous(self):
        rows = [{"id": "1", "price": "5"}, {"id": "2", "price": ""}]
        out = clean(rows)
        self.assertEqual(out[1]["price"], "5")

    def test_blank_price_with_no_previous_defaults_to_zero(self):
        out = clean([{"id": "1", "price": ""}])
        self.assertEqual(out[0]["price"], "0")

if __name__ == "__main__":
    unittest.main()
```

## What you got, in three words

Working. Tested. Documented. — the same three things every automation order
ships with.

---

*Representative sample: a real script, README, and test, kept small for the
portfolio.*
