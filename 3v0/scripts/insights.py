#!/usr/bin/env python3
"""Stone 20 — turn the analytics report into ranked, evidence-backed findings.

Decision-support: reads `data/analytics/report.json` (written by
`scripts/analytics.py`), runs the pure detectors in `core.insights`, prints a
ranked list, and writes `data/analytics/insights.json`. It PROPOSES; the
caller DISPOSES through the normal disciplined pipeline.

Usage:
    python3 3v0/scripts/insights.py                 # print findings
    python3 3v0/scripts/insights.py --out ''        # don't persist
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "3v0"))

from core.insights import detect  # noqa: E402

DEFAULT_REPORT = REPO_ROOT / "3v0" / "data" / "analytics" / "report.json"
DEFAULT_INSIGHTS = REPO_ROOT / "3v0" / "data" / "analytics" / "insights.json"


def render(findings):
    if not findings:
        return "self-analytics: no findings — every signal is within thresholds."
    lines = ["self-analytics findings (ranked):", ""]
    for i, f in enumerate(findings, 1):
        lines.append(f"{i}. [{f['severity'].upper()}] {f['message']}")
        lines.append(f"   evidence: {f['evidence']}")
        lines.append(f"   action:   {f['suggested_action']}")
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="3V0 self-analytics insights")
    ap.add_argument("--report", default=str(DEFAULT_REPORT), help="path to report.json")
    ap.add_argument("--out", default=str(DEFAULT_INSIGHTS),
                    help="insights.json path (default: 3v0/data/analytics/insights.json; '' to skip)")
    args = ap.parse_args()

    if not os.path.exists(args.report):
        print(f"no report at {args.report}; run scripts/analytics.py first", file=sys.stderr)
        return 1

    with open(args.report) as f:
        report = json.load(f)

    findings = detect(report)
    print(render(findings))

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w") as f:
            json.dump({
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "findings": findings,
            }, f, indent=2)
        print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
