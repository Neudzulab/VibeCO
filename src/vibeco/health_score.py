# Agent Guide
# Purpose: Compute a measurable endpoint health score from a validator-style JSON payload.
# Changed: Added a runnable CLI entrypoint that prints totals and score for real report files.

"""CLI to compute endpoint health score from a JSON report."""

from __future__ import annotations

import json
from pathlib import Path
import sys


def compute_health_score(report: dict) -> tuple[int, int, int]:
    """Return (total, failures, score_percent)."""
    results = report.get("results", [])
    failures = report.get("failures", [])
    total = len(results)
    failed = len(failures)
    if total == 0:
        return 0, failed, 0
    score = round(((total - failed) / total) * 100)
    return total, failed, score


def main(argv: list[str] | None = None) -> int:
    args = argv or sys.argv[1:]
    if len(args) != 1:
        print("usage: python -m vibeco.health_score <report.json>")
        return 1

    report_path = Path(args[0])
    report = json.loads(report_path.read_text(encoding="utf-8"))
    total, failed, score = compute_health_score(report)
    print(f"total={total} failures={failed} health_score={score}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
