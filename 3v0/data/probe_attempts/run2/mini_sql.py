#!/usr/bin/env python3
"""probe014: miniature CSV query engine over employee.csv with a fixed DSL."""
import csv
import re
import sys

# --- load the table ---------------------------------------------------------
def load(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    return rows


# --- query executors --------------------------------------------------------
def run(rows, q):
    q = q.strip()
    lo = q.lower()

    if lo.startswith("select count(*)"):
        col, val = _parse_where(q)
        n = sum(1 for r in rows if r[col].lstrip("-").isdigit() and int(r[col]) >= val)
        return [str(n)]

    q2 = re.sub(r"\s*where\b.*$", "", q, flags=re.I).strip()
    q2 = re.sub(r"\s*order by\b.*$", "", q2, flags=re.I).strip()
    q2 = re.sub(r"\s*group by\b.*$", "", q2, flags=re.I).strip()
    q2 = re.sub(r"\s*from\s+\w+\b", "", q2, flags=re.I).strip()

    if re.search(r"\bgroup\s+by\b", lo):
        agg_expr = re.sub(r"^select\s+", "", q2, flags=re.I).strip()  # "dept, MAX(salary)"
        dept_col, agg = [s.strip() for s in agg_expr.split(",")]
        m = re.search(r"MAX\((\w+)\)", agg)
        agg_col = m.group(1)
        best = {}
        for r in rows:
            d = r[dept_col]
            v = int(r[agg_col])
            if d not in best or v > best[d]:
                best[d] = v
        return [f"{d},{best[d]}" for d in sorted(best)]

    # SELECT <cols> [WHERE] [ORDER] (non-agg)
    cols = [c.strip() for c in q2.replace("SELECT", "", 1).split(",")]
    res = rows
    m = re.search(r"\bwhere\b\s+(\w+)\s*(=|[><]=?)\s*'?([^']*?)'?\s*$", q.strip(), re.I)
    if m:
        c, op, v = m.group(1), m.group(2), m.group(3)
        res = [r for r in res if _cmp(r[c], c, op, v)]

    om = re.search(r"\border\s+by\s+(\w+)\s+(asc|desc)", q, re.I)
    if om:
        c, direction = om.group(1), om.group(2).upper()
        res = sorted(res, key=lambda r: _keyf(r[c]), reverse=(direction == "DESC"))

    return [",".join(r[c] for c in cols) for r in res]


def _keyf(v):
    return (int(v), 0) if v.lstrip("-").isdigit() else (v, 1)


def _cmp(v, col, op, needle):
    if v.lstrip("-").isdigit() and needle.lstrip("-").isdigit():
        a, b = int(v), int(needle)
    else:
        a, b = v, needle
    return {"=": lambda x, y: x == y}[op](a, b) if op == "=" else {
        ">": a > b, "<": a < b, ">=": a >= b, "<=": a <= b}.get(op, False)


def _parse_where(q):
    m = re.search(r"\bwhere\b\s+(\w+)\s*(>=|<=|>|<|=)\s*(\d+)", q, re.I)
    if not m:
        return None, None
    return m.group(1), int(m.group(3))


# --- main -------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("usage: mini_sql.py queries.txt", file=sys.stderr)
        return 2
    rows = load("employees.csv")
    with open(sys.argv[1]) as f:
        queries = [l for l in f.read().splitlines() if l.strip()]
    out = []
    for i, q in enumerate(queries):
        if i:
            out.append("")
        out.extend(run(rows, q))
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
