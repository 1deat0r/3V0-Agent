#!/usr/bin/env python3
"""3V0 self-analytics — aggregate the session DB into an owned report.

Reads Hermes's state.db (sessions, messages, session_model_usage) and turns
it into a self-owned analytics report: per-tool frequency / latency / success,
per-model tokens / cost, per-day burn, and body-health signals.

Local and self-owned: reads only the local profile DB, writes only to
3v0/data/analytics/. No outbound telemetry, nothing phones home.

Usage:
    python3 3v0/scripts/analytics.py                 # print human report
    python3 3v0/scripts/analytics.py --top 15        # more tools
    python3 3v0/scripts/analytics.py --out ''        # don't persist report
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

from core.analytics import summarize  # noqa: E402
from core.analytics_collect import build_events, load_sessions, load_usage  # noqa: E402

DEFAULT_DB = Path(os.environ.get(
    "THREEV0_STATE_DB",
    os.path.expanduser("~/.hermes/profiles/3v0/state.db"),
))
DEFAULT_REPORT = REPO_ROOT / "3v0" / "data" / "analytics" / "report.json"


def render(report, top=10):
    t = report["totals"]
    ch = f"{t['cache_hit_ratio']*100:.1f}%" if t.get("cache_hit_ratio") is not None else "n/a"
    os_ = f"{t['output_token_share']*100:.1f}%" if t.get("output_token_share") is not None else "n/a"
    lines = [
        f"3V0 self-analytics — {t['sessions']} sessions, {t['active_days']} active days",
        f"tokens: in={t['input_tokens']:,} out={t['output_tokens']:,} "
        f"cache_read={t['cache_read_tokens']:,} reasoning={t['reasoning_tokens']:,}",
        f"cache-hit {ch} | output share {os_} (levers per TOKEN_EFFICIENCY.md)",
        f"cost (est): ${t['estimated_cost_usd']:.2f} | api calls {t['api_calls']:,} | tool calls {t['tool_calls']:,}",
        "",
        "models:",
    ]
    for m in report["models"]:
        mch = f" ch={m['cache_hit_ratio']*100:.1f}%" if m.get("cache_hit_ratio") is not None else ""
        lines.append(f"  {m['model']:<22} ${m['estimated_cost_usd']:>9.2f}  "
                     f"in={m['input_tokens']:,} out={m['output_tokens']:,}{mch}")
    lines += ["", "tasks (task × model — aux should be flash):"]
    for tsk in report["tasks"]:
        lines.append(f"  {tsk['task']:<12} {tsk['model']:<22} ${tsk['estimated_cost_usd']:>9.2f}  "
                     f"in={tsk['input_tokens']:,}")
    lines += ["", f"tools (top {top} by count):",
              f"  {'tool':<20} {'n':>5} {'succ%':>6} {'p50ms':>8} {'p95ms':>8}"]
    for tool in report["tools"][:top]:
        rate = f"{tool['success_rate']*100:.0f}%" if tool["success_rate"] is not None else "   ?"
        p50 = f"{tool['latency_median_ms']:.0f}" if tool["latency_median_ms"] is not None else "-"
        p95 = f"{tool['latency_p95_ms']:.0f}" if tool["latency_p95_ms"] is not None else "-"
        lines.append(f"  {tool['name']:<20} {tool['count']:>5} {rate:>6} {p50:>8} {p95:>8}")
    lines += ["", "daily (last 7):",
              f"  {'date':<12} {'sess':>4} {'tools':>6} {'in_tok':>9} {'ch%':>5} {'cost$':>7}"]
    for d in report["daily"][-7:]:
        dch = f"{d['cache_hit_ratio']*100:.0f}%" if d.get("cache_hit_ratio") is not None else "   ?"
        lines.append(f"  {d['date']:<12} {d['sessions']:>4} {d['tool_calls']:>6} "
                     f"{d['input_tokens']:>9,} {dch:>5} {d['estimated_cost_usd']:>7.2f}")
    h = report["health"]
    lines += ["",
              f"health: compression_failures={h['compression_failure_errors']} "
              f"rewinds={h['rewinds']} end_reasons={h['end_reasons']}"]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="3V0 self-analytics")
    ap.add_argument("--db", default=str(DEFAULT_DB), help="path to state.db")
    ap.add_argument("--out", default=str(DEFAULT_REPORT),
                    help="report.json path (default: 3v0/data/analytics/report.json; '' to skip)")
    ap.add_argument("--top", type=int, default=10, help="tools shown in human report")
    ap.add_argument("--days", type=int, default=30, help="daily buckets to include")
    args = ap.parse_args()

    if not os.path.exists(args.db):
        print(f"no state DB at {args.db}", file=sys.stderr)
        return 1

    report = summarize(load_sessions(args.db), load_usage(args.db),
                       build_events(args.db), last_n=args.days)
    report["generated_at"] = datetime.now(timezone.utc).isoformat()
    print(render(report, top=args.top))

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
