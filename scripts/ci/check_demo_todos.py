#!/usr/bin/env python3
"""Fail if tracked production files contain placeholder TODO demo markers."""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys
from typing import Iterable, List

PATTERN = re.compile(r"todo\s*[:\-]*\s*demo", re.IGNORECASE)
# Top-level directories that are not considered production code.
NON_PRODUCTION_ROOTS = {
    "tests",
    "docs",
    "artifacts",
    "reports",
    "samples",
}


def git_tracked_files() -> List[pathlib.Path]:
    """Return all tracked files in the repository as Path objects."""
    result = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [pathlib.Path(line) for line in result.stdout.splitlines() if line]


def is_production(path: pathlib.Path) -> bool:
    """Return True if the file is considered production."""
    parts = path.parts
    if not parts:
        return False
    # Ignore files under excluded top-level directories.
    if parts[0] in NON_PRODUCTION_ROOTS:
        return False
    return True


def is_binary(path: pathlib.Path) -> bool:
    """Heuristic binary detection."""
    try:
        with path.open("rb") as handle:
            chunk = handle.read(1024)
    except OSError:
        return False
    return b"\0" in chunk


def find_markers(paths: Iterable[pathlib.Path]) -> List[pathlib.Path]:
    """Return the files containing the TODO demo marker."""
    offenders: List[pathlib.Path] = []
    for path in paths:
        if not path.is_file() or not is_production(path) or is_binary(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Skip files we cannot decode as UTF-8.
            continue
        if PATTERN.search(text):
            offenders.append(path)
    return offenders


def main() -> int:
    files = git_tracked_files()
    offenders = find_markers(files)
    if offenders:
        print("Found placeholder TODO demo markers in production files:")
        for path in offenders:
            print(f" - {path}")
        print("Please remove or replace these demo TODO blocks before committing.")
        return 1
    print("No demo TODO markers detected in production files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
