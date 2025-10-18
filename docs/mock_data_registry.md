# Mock Data and Demo Mode Registry

This document catalogs where mock data lives, which workflows rely on it, and how to run those flows safely in demo mode. Keep this file updated whenever new mock fixtures or demo-only scripts are introduced.

## Execution Modes

The renderer and supporting scripts understand two execution modes:

- **`production`** – default mode for real project data. Mock payloads are blocked here.
- **`demo`** – explicitly opt-in mode that allows the bundled sample content for walkthroughs and training.

Configure the mode via either option:

- Command line: `python scripts/render.py --mode demo`
- Environment variable: `VIBECO_MODE=demo make render`

## Mock Data Inventory

| Component | Location | Notes |
| --- | --- | --- |
| Project brief sample | `project.yaml` (default template) | Marked by `slug: sample-project`; only allowed in demo mode. Replace with real project data for production runs. |
| Alternative project template | `project.yaml.example` | Copy to create a new project brief; contains the same mock markers as the default file. |
| Rendered summary example | `samples/PROJECT_SUMMARY.sample.md` | Static markdown generated from the mock project data. Useful for onboarding demos only. |

## Demo-Only Workflows

| Workflow | Command | Purpose |
| --- | --- | --- |
| Render project summary with mock data | `VIBECO_MODE=demo make render` | Generates `PROJECT_SUMMARY.md` using the bundled sample data. |
| Direct renderer invocation | `python scripts/render.py --mode demo --data project.yaml` | Same as above without the Makefile wrapper. |

Running these commands without `--mode demo` or `VIBECO_MODE=demo` triggers a guard that stops the execution when mock markers are detected.

## Updating This Registry

When introducing new mock fixtures or demo scripts:

1. Place mock assets under a clearly labelled directory (e.g., `samples/` or `*-example.*`).
2. Add a new row in the tables above describing the location and usage.
3. Reference this file from any onboarding or README updates so newcomers know where to look.
