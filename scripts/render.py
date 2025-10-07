"""Render PROJECT_SUMMARY.md from project.yaml using a markdown template."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader


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
    return parser


def load_project_data(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Project data not found: {path}. Create it from project.yaml.example first.")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
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

    project_data = load_project_data(args.data)
    output = render_template(args.template, project_data)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    print(f"Rendered {args.output} from {args.data} using {args.template}")


if __name__ == "__main__":
    main()
