from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.render import load_project_data, render_template


def test_load_project_data_requires_mapping(tmp_path: Path) -> None:
    data_file = tmp_path / "project.yaml"
    data_file.write_text("- not-a-mapping", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        load_project_data(data_file)

    assert "mapping" in str(excinfo.value)


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
