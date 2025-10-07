#!/usr/bin/env python
"""Advance the delivery plan or manage plan locks."""
from __future__ import annotations

import argparse
import sys

from planlib import (
    LockArgumentParser,
    acquire_lock,
    describe_lock,
    is_locked,
    mark_next_step,
    release_lock,
    PlanLockedError,
)


def build_parser() -> argparse.ArgumentParser:
    parser = LockArgumentParser(description="Progress the next plan step")
    parser.add_argument("--lock", nargs="?", const="", help="Lock the plan with an optional reason")
    parser.add_argument("--unlock", action="store_true", help="Release the current plan lock")
    parser.add_argument("--status", action="store_true", help="Show lock status without modifying the plan")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.lock is not None and args.unlock:
        parser.error("--lock and --unlock cannot be used together")

    if args.lock is not None:
        try:
            acquire_lock(args.lock)
        except PlanLockedError as exc:  # pragma: no cover - sanity feedback
            print(f"Plan already locked: {exc}")
            return 1
        print("Plan locked")
        return 0

    if args.unlock:
        release_lock()
        print("Plan unlocked")
        return 0

    if args.status:
        if is_locked():
            print(f"Plan locked:\n{describe_lock()}")
        else:
            print("Plan unlocked")
        return 0

    try:
        step = mark_next_step()
    except PlanLockedError as exc:
        print(f"Cannot progress plan: {exc}")
        return 1
    except RuntimeError as exc:
        print(str(exc))
        return 1

    print(f"Completed {step.label}{step.rest}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
