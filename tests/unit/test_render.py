# Agent Guide
# Purpose: Validates the renderer CLI, template output, and mock data guardrails.
# Key Flows:
#   - load_project_data*: Ensures YAML validation paths are guarded.
#   - render_template(): Confirms markdown export contains dynamic sections.
#   - resolve_mode(): Exercises CLI vs environment precedence.
# Relevant Implementation:
#   - scripts/render.py

from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.render import (
    DEMO_MODE,
    PRODUCTION_MODE,
    ensure_mock_usage_allowed,
    load_project_data,
    render_template,
    resolve_mode,
)


def test_load_project_data_requires_mapping(tmp_path: Path) -> None:
    data_file = tmp_path / "project.yaml"
    data_file.write_text("- not-a-mapping", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        load_project_data(data_file)

    assert "mapping" in str(excinfo.value)


def test_load_project_data_missing_file_suggests_example(tmp_path: Path) -> None:
    data_file = tmp_path / "project.yaml"
    (tmp_path / "project.yaml.example").write_text("{}", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        load_project_data(data_file)

    assert "Copy it from" in str(excinfo.value)


def test_load_project_data_reports_yaml_error(tmp_path: Path) -> None:
    data_file = tmp_path / "project.yaml"
    data_file.write_text("invalid: [unterminated", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        load_project_data(data_file)

    assert "Unable to parse" in str(excinfo.value)


def test_render_template_includes_progress_sections(tmp_path: Path) -> None:
    template_path = tmp_path / "template.md"
    template_path.write_text(
        "Progress: {% for update in project['progress_updates'] %}{{ update['percent_complete'] }}% {% endfor %}",
        encoding="utf-8",
    )

    context = {
        "progress_updates": [
            {"date": "2025-01-05", "percent_complete": 25, "summary": "Checkpoint"},
            {"date": "2025-02-12", "percent_complete": 40, "summary": "More progress"},
        ]
    }

    rendered = render_template(template_path, context)

    assert "25%" in rendered
    assert "40%" in rendered


def test_ensure_mock_usage_blocked_in_production(tmp_path: Path) -> None:
    data = {"slug": "sample-project"}

    with pytest.raises(SystemExit) as excinfo:
        ensure_mock_usage_allowed(data, mode=PRODUCTION_MODE, data_path=tmp_path / "project.yaml")

    assert "demo mode" in str(excinfo.value)


def test_ensure_mock_usage_allowed_in_demo() -> None:
    data = {"slug": "sample-project"}

    # Should not raise
    ensure_mock_usage_allowed(data, mode=DEMO_MODE, data_path=Path("project.yaml"))


def test_resolve_mode_prefers_cli(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VIBECO_MODE", "demo")

    mode = resolve_mode("production")

    assert mode == PRODUCTION_MODE


def test_resolve_mode_reads_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VIBECO_MODE", "demo")

    mode = resolve_mode(None)

    assert mode == DEMO_MODE


def test_resolve_mode_rejects_invalid(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VIBECO_MODE", "invalid")

    with pytest.raises(SystemExit) as excinfo:
        resolve_mode(None)

    assert "Unsupported mode" in str(excinfo.value)
