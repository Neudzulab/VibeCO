# Agent Guide
# Purpose: Verify health score CLI computes measurable output from a real JSON file.
# Changed: Added one end-to-end unit test for the new health score command.

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys


def test_health_score_cli_outputs_expected_values(tmp_path) -> None:
    payload = {
        "results": [{"path": "/a"}, {"path": "/b"}, {"path": "/c"}],
        "failures": [{"path": "/b"}],
    }
    report_file = tmp_path / "report.json"
    report_file.write_text(json.dumps(payload), encoding="utf-8")

    repo_root = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")

    process = subprocess.run(
        [sys.executable, "-m", "vibeco.health_score", str(report_file)],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )

    assert process.stdout.strip() == "total=3 failures=1 health_score=67"
