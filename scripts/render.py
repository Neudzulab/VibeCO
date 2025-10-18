# Agent Guide
# Purpose: Entry point that renders project summaries from structured YAML data while
#          enforcing demo-mode guardrails for mock content.
# Key Flows:
#   - build_parser(): CLI surface for render options.
#   - resolve_mode(): Mode resolution with environment fallback.
#   - ensure_mock_usage_allowed(): Prevents mock data from leaking into production.
#   - render_template(): Applies the Jinja template and returns markdown output.
# Relevant Tests:
#   - tests/test_render.py::test_ensure_mock_usage_blocked_in_production
#   - tests/test_render.py::test_resolve_mode_prefers_cli

"""Render PROJECT_SUMMARY.md from project.yaml using a markdown template."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader

DEMO_MODE = "demo"
PRODUCTION_MODE = "production"
ALLOWED_MODES = {DEMO_MODE, PRODUCTION_MODE}

MOCK_DATA_MARKERS = {
    ("name", "Sample Project"),
    ("slug", "sample-project"),
    ("tagline", "Write a short, inspiring one-liner."),
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Render PROJECT_SUMMARY.md by combining project.yaml with "
            "docs/project_summary_template.md."
        )
    )
    parser.add_argument(
        "--data",
        default="project.yaml",
        type=Path,
        help="Path to the YAML file that describes the project.",
    )
    parser.add_argument(
        "--template",
        default=Path("docs") / "project_summary_template.md",
        type=Path,
        help="Path to the markdown template that should be rendered.",
    )
    parser.add_argument(
        "--output",
        default=Path("PROJECT_SUMMARY.md"),
        type=Path,
        help="Where to write the rendered markdown file.",
    )
    parser.add_argument(
        "--mode",
        choices=sorted(ALLOWED_MODES),
        default=None,
        help=(
            "Execution mode. Use 'demo' when relying on bundled mock data; "
            "defaults to the VIBECO_MODE environment variable or 'production'."
        ),
    )
    return parser


def resolve_mode(cli_mode: str | None) -> str:
    """Return the execution mode from CLI or environment input."""

    mode = cli_mode or os.getenv("VIBECO_MODE") or PRODUCTION_MODE
    if mode not in ALLOWED_MODES:
        raise SystemExit(
            f"Unsupported mode '{mode}'. Allowed values: {', '.join(sorted(ALLOWED_MODES))}."
        )
    return mode


def ensure_mock_usage_allowed(
    data: dict[str, Any], *, mode: str, data_path: Path | None = None
) -> None:
    """Prevent mock project data from leaking into production workflows."""

    uses_mock_data = any(data.get(key) == value for key, value in MOCK_DATA_MARKERS)
    if uses_mock_data and mode != DEMO_MODE:
        source = f" ({data_path})" if data_path else ""
        raise SystemExit(
            "Mock project data detected. Run the renderer in demo mode"
            " (--mode demo or VIBECO_MODE=demo) or replace mock values before"
            f" proceeding{source}."
        )


def load_project_data(path: Path) -> dict[str, Any]:
    if not path.exists():
        example_path = Path(f"{path}.example")
        suggestion = (
            f" Copy it from {example_path} first."
            if example_path.exists()
            else " Create it from project.yaml.example first."
        )
        raise SystemExit(f"Project data not found: {path}.{suggestion}")

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except yaml.YAMLError as exc:  # pragma: no cover - defensive branch
        raise SystemExit(f"Unable to parse YAML file {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit("project.yaml must contain a mapping at the top level.")
    return data


def render_template(template_path: Path, context: dict) -> str:
    if not template_path.exists():
        raise SystemExit(f"Template file not found: {template_path}")
    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_path.name)
    content = template.render(project=context).strip()
    return content + "\n"


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    mode = resolve_mode(args.mode)
    project_data = load_project_data(args.data)
    ensure_mock_usage_allowed(project_data, mode=mode, data_path=args.data)
    output = render_template(args.template, project_data)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    print(
        f"Rendered {args.output} from {args.data} using {args.template}"
        f" (mode={mode})"
    )


if __name__ == "__main__":
    main()
