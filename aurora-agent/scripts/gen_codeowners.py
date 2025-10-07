#!/usr/bin/env python
"""Generate CODEOWNERS entries from the staffing roster."""
from __future__ import annotations

import pathlib
from typing import Dict, List

import yaml

ROSTER_PATH = pathlib.Path("agents/roster.yaml")
CODEOWNERS_PATH = pathlib.Path("CODEOWNERS")
PRIMARY_OWNER = "@Neudzulab"
ORG_HANDLE_PREFIX = "@VibeCO-"

PATTERNS = {
    "src/frontend/**": ["FrontendEngineer", "TechLead"],
    "src/backend/php/**": ["BackendEngineerPHP", "TechLead"],
    "src/backend/python/**": ["BackendEngineerPython", "TechLead"],
    "tests/**": ["QAEngineer"],
    "infra/**": ["DevOpsEngineer", "SREEngineer", "SecurityEngineer"],
}


def load_roster() -> Dict[str, dict]:
    if not ROSTER_PATH.exists():
        raise FileNotFoundError("agents/roster.yaml not found. Run scripts/staff.py first.")
    data = yaml.safe_load(ROSTER_PATH.read_text(encoding="utf-8"))
    roster = {}
    for member in data.get("team", []):
        roster[member["role"]] = member
    return roster


def handle_for(role: str) -> str:
    return f"{ORG_HANDLE_PREFIX}{role}"


def format_line(pattern: str, roles: List[str], roster: Dict[str, dict]) -> str:
    owners = []
    for role in roles:
        if role in roster:
            owners.append(handle_for(role))
    if not owners:
        owners.append(PRIMARY_OWNER)
    return f"{pattern} {' '.join(owners)}"


def generate_codeowners(roster: Dict[str, dict]) -> List[str]:
    lines = [f"* {PRIMARY_OWNER}"]
    for pattern, roles in PATTERNS.items():
        lines.append(format_line(pattern, roles, roster))
    return lines


def main() -> int:
    roster = load_roster()
    lines = generate_codeowners(roster)
    CODEOWNERS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {CODEOWNERS_PATH}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
