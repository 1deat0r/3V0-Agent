#!/usr/bin/env python3
"""Extract product cards from an HTML file into CSV, with a validation report.

Portfolio demo — ToS-safe by design: this parses a LOCAL html file (no network).
The validation report is the "loud failure" deliverable every scraping order
ships with: it says exactly which fields came back empty instead of silently
writing wrong data.
"""
import argparse
import csv
import sys
from html.parser import HTMLParser
from pathlib import Path


class ProductParser(HTMLParser):
    """Extract .product-card blocks: name, price, link, availability."""

    def __init__(self):
        super().__init__()
        self.products = []
        self._in_card = False
        self._in_name = self._in_price = self._in_link = self._in_avail = False
        self._current = None
        self.cards_seen = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if tag == "div" and "product-card" in classes:
            self._in_card = True
            self.cards_seen += 1
            self._current = {"name": "", "price": "", "link": "", "availability": ""}
        elif self._in_card and tag == "h2" and "product-name" in classes:
            self._in_name = True
        elif self._in_card and tag == "span" and "price" in classes:
            self._in_price = True
        elif self._in_card and tag == "a" and "product-link" in classes:
            self._current["link"] = attrs.get("href", "")
        elif self._in_card and tag == "span" and "availability" in classes:
            self._in_avail = True

    def handle_endtag(self, tag):
        if tag == "div" and self._in_card:
            self._in_card = False
            self.products.append(self._current)
            self._current = None
        if tag in ("h2", "span"):
            self._in_name = self._in_price = self._in_avail = False

    def handle_data(self, data):
        if not self._current:
            return
        text = data.strip()
        if self._in_name:
            self._current["name"] += " " + text
        elif self._in_price:
            self._current["price"] += text
        elif self._in_avail:
            self._current["availability"] += text


def validation_report(products, cards_seen, source):
    lines = [
        f"validation report — {source}",
        f"  cards found in html : {cards_seen}",
        f"  products extracted  : {len(products)}",
    ]
    empty = {f: 0 for f in ("name", "price", "link", "availability")}
    for p in products:
        for f in empty:
            if not p[f].strip():
                empty[f] += 1
    lines.append("  empty fields:")
    for f, n in empty.items():
        lines.append(f"    {f:<13}: {n}")
    failed = cards_seen - len(products)
    if failed:
        lines.append(f"  WARNING: {failed} card(s) failed to parse")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("html", help="local HTML file to parse")
    ap.add_argument("-o", "--out", default="products.csv", help="output CSV")
    args = ap.parse_args()

    path = Path(args.html)
    if not path.exists():
        sys.exit(f"error: {args.html} does not exist")

    parser = ProductParser()
    parser.feed(path.read_text(encoding="utf-8"))

    fields = ["name", "price", "link", "availability"]
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(parser.products)

    report = validation_report(parser.products, parser.cards_seen, args.html)
    Path("validation_report.txt").write_text(report + "\n", encoding="utf-8")
    print(report)
    print(f"wrote {args.out} and validation_report.txt")


if __name__ == "__main__":
    main()
