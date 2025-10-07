#!/usr/bin/env python3
"""Plan manager: list upcoming steps in English for global visibility."""

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Iterable

sys.path.append(str(pathlib.Path(__file__).resolve().parent))

from planlib import PlanStep, next_steps


def format_step(step: PlanStep) -> str:
    return f"{step.identifier}: {step.title}"


def main(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="List pending plan steps")
    parser.add_argument("--limit", type=int, default=0, help="How many steps to show (0 = all)")
    args = parser.parse_args(argv)

    steps = next_steps(limit=args.limit or None)
    if not steps:
        print("All steps are complete! 🎉")
        return

    print("Upcoming steps:")
    for step in steps:
        print(f"- {format_step(step)}")


if __name__ == "__main__":
    main()
