from __future__ import annotations

from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import render


def _write_sample_project(path: Path) -> None:
    path.write_text(
        """
name: Sample Project
slug: sample-project
tagline: Write a short, inspiring one-liner.
progress_updates:
  - date: 2025-01-01
    percent_complete: 10
    summary: Kickoff
""".strip(),
        encoding="utf-8",
    )


def _write_template(path: Path) -> None:
    path.write_text(
        "Project: {{ project['name'] }} ({{ project['tagline'] }})",
        encoding="utf-8",
    )


def test_main_blocks_mock_data_without_demo_mode(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    data_file = tmp_path / "project.yaml"
    _write_sample_project(data_file)
    template = tmp_path / "template.md"
    _write_template(template)
    output = tmp_path / "PROJECT_SUMMARY.md"

    argv = [
        "render",
        "--data",
        str(data_file),
        "--template",
        str(template),
        "--output",
        str(output),
        "--mode",
        "production",
    ]
    monkeypatch.setattr(sys, "argv", argv)

    with pytest.raises(SystemExit) as excinfo:
        render.main()

    assert "demo mode" in str(excinfo.value)
    assert not output.exists()


def test_main_renders_summary_in_demo_mode(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    data_file = tmp_path / "project.yaml"
    _write_sample_project(data_file)
    template = tmp_path / "template.md"
    _write_template(template)
    output = tmp_path / "PROJECT_SUMMARY.md"

    argv = [
        "render",
        "--data",
        str(data_file),
        "--template",
        str(template),
        "--output",
        str(output),
        "--mode",
        "demo",
    ]
    monkeypatch.setattr(sys, "argv", argv)

    render.main()

    captured = capsys.readouterr()
    assert "Rendered" in captured.out
    assert output.exists()
    assert "Sample Project" in output.read_text(encoding="utf-8")
