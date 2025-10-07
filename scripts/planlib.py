import pathlib
import re
from dataclasses import dataclass
from typing import Iterable, List

STEP_PATTERN = re.compile(r"^- \[( |x)\] (STEP-(?:\d+|RF-\d+)): (.+)$", re.MULTILINE)


@dataclass
class PlanStep:
    identifier: str
    title: str
    done: bool


def parse_plan(text: str) -> List[PlanStep]:
    steps: List[PlanStep] = []
    for match in STEP_PATTERN.finditer(text):
        done = match.group(1) == "x"
        identifier = match.group(2)
        title = match.group(3).strip()
        steps.append(PlanStep(identifier=identifier, title=title, done=done))
    return steps


def load_plan(path: pathlib.Path = pathlib.Path("PLAN.md")) -> Iterable[PlanStep]:
    if not path.exists():
        return []
    return parse_plan(path.read_text())


def next_steps(limit: int | None = None) -> List[PlanStep]:
    steps = [step for step in load_plan() if not step.done]
    if limit is not None:
        return steps[:limit]
    return steps
