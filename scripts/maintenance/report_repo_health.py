#!/usr/bin/env python3
"""Report repository hygiene items for periodic maintenance."""
from __future__ import annotations

import pathlib
import re
import subprocess
from typing import Iterable, List, Sequence, Set

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
AGENT_FILENAME = "AGENTS.md"
LARGE_FILE_THRESHOLD = 512 * 1024  # 512 KiB
TEST_FILE_RE = re.compile(r"(test_.*|.*_test)\.py$", re.IGNORECASE)


class RepoReport:
    def __init__(self) -> None:
        self.large_files_without_guides: List[pathlib.Path] = []
        self.stray_tests: List[pathlib.Path] = []

    def has_findings(self) -> bool:
        return bool(self.large_files_without_guides or self.stray_tests)


def git_tracked_files() -> Sequence[pathlib.Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return [pathlib.Path(line) for line in result.stdout.splitlines() if line]


def directories_with_agents(files: Iterable[pathlib.Path]) -> Set[pathlib.Path]:
    dirs: Set[pathlib.Path] = set()
    for path in files:
        if path.name == AGENT_FILENAME:
            dirs.add(path.parent)
    return dirs


def path_has_agent(path: pathlib.Path, agent_dirs: Set[pathlib.Path]) -> bool:
    current = path.parent
    while True:
        if current in agent_dirs:
            return True
        if current == pathlib.Path('.'):
            break
        current = current.parent
    return pathlib.Path('.') in agent_dirs


def find_large_files_without_guides(files: Iterable[pathlib.Path], agent_dirs: Set[pathlib.Path]) -> List[pathlib.Path]:
    offenders: List[pathlib.Path] = []
    for rel_path in files:
        abs_path = REPO_ROOT / rel_path
        if not abs_path.is_file():
            continue
        try:
            size = abs_path.stat().st_size
        except OSError:
            continue
        if size < LARGE_FILE_THRESHOLD:
            continue
        if path_has_agent(rel_path, agent_dirs):
            continue
        offenders.append(rel_path)
    return offenders


def find_stray_tests(files: Iterable[pathlib.Path]) -> List[pathlib.Path]:
    offenders: List[pathlib.Path] = []
    for rel_path in files:
        if "tests" in rel_path.parts:
            continue
        if TEST_FILE_RE.search(rel_path.name):
            offenders.append(rel_path)
    return offenders


def print_report(report: RepoReport) -> None:
    if not report.has_findings():
        print("No maintenance issues detected.")
        return
    if report.large_files_without_guides:
        print("Large files without AGENTS.md guidance (>512 KiB):")
        for path in report.large_files_without_guides:
            print(f" - {path}")
    if report.stray_tests:
        print("Test-like files detected outside the tests/ directory:")
        for path in report.stray_tests:
            print(f" - {path}")


def main() -> int:
    tracked_files = git_tracked_files()
    agent_dirs = directories_with_agents(tracked_files)
    report = RepoReport()
    report.large_files_without_guides = find_large_files_without_guides(tracked_files, agent_dirs)
    report.stray_tests = find_stray_tests(tracked_files)
    print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
