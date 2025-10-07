"""Utilities for managing the delivery plan."""
from __future__ import annotations

import argparse
import getpass
import pathlib
import re
from dataclasses import dataclass
from typing import Iterable, List, Optional

PLAN_PATH = pathlib.Path("PLAN.md")
LOCK_PATH = pathlib.Path("PLAN.lock")
STEP_PATTERN = re.compile(r"^- \[(?P<state>.|)\] (?P<label>STEP-[0-9]+)(?P<rest>.*)$")


@dataclass
class Step:
    index: int
    state: str
    label: str
    rest: str

    @property
    def completed(self) -> bool:
        return self.state.lower() == "x"


class PlanLockedError(RuntimeError):
    """Raised when attempting to modify the plan while it is locked."""


def read_plan() -> List[str]:
    if not PLAN_PATH.exists():
        raise FileNotFoundError("PLAN.md not found")
    return PLAN_PATH.read_text(encoding="utf-8").splitlines()


def write_plan(lines: Iterable[str]) -> None:
    PLAN_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def iter_steps(lines: Iterable[str]) -> Iterable[Step]:
    for idx, line in enumerate(lines):
        match = STEP_PATTERN.match(line.strip())
        if match:
            yield Step(
                index=idx,
                state=match.group("state"),
                label=match.group("label"),
                rest=match.group("rest"),
            )


def next_open_step(lines: List[str]) -> Optional[Step]:
    for step in iter_steps(lines):
        if not step.completed:
            return step
    return None


def mark_next_step() -> Step:
    if is_locked():
        raise PlanLockedError("Plan is locked. Unlock before updating steps.")

    lines = read_plan()
    step = next_open_step(lines)
    if step is None:
        raise RuntimeError("No remaining open steps in PLAN.md")

    original_line = lines[step.index]
    lines[step.index] = original_line.replace("[ ]", "[x]", 1)
    write_plan(lines)
    return Step(index=step.index, state="x", label=step.label, rest=step.rest)


def is_locked() -> bool:
    return LOCK_PATH.exists()


def acquire_lock(reason: Optional[str] = None) -> pathlib.Path:
    if is_locked():
        raise PlanLockedError("Plan is already locked")

    content = {
        "locked_by": getpass.getuser(),
        "reason": reason or "",
    }
    LOCK_PATH.write_text(
        "\n".join(f"{key}: {value}" for key, value in content.items()) + "\n",
        encoding="utf-8",
    )
    return LOCK_PATH


def release_lock() -> None:
    if not is_locked():
        return
    LOCK_PATH.unlink()


def describe_lock() -> Optional[str]:
    if not is_locked():
        return None
    return LOCK_PATH.read_text(encoding="utf-8").strip() or "(lock file empty)"


class LockArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:  # pragma: no cover - argparse default path
        raise ValueError(message)
