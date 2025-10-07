# VibeCO

[![refactor-guard](https://github.com/Neudzulab/VibeCO/actions/workflows/refactor.yml/badge.svg)](./.github/workflows/refactor.yml)
[![daily-stability](https://github.com/Neudzulab/VibeCO/actions/workflows/daily_stability.yml/badge.svg)](./.github/workflows/daily_stability.yml)

Welcome to the 2025 edition of **VibeCO (Vibe Coding Orchestrator)**—a reusable project brief template designed so that every stakeholder immediately understands what you are building, why it matters, and how to unlock the next phase of work. Clone this repository, inject your own context, and publish a polished brief that keeps your team aligned from day zero.

## Why this repository exists

Modern software projects evolve quickly. VibeCO keeps your source-of-truth lightweight, explicit, and testable so you can:

- Capture your mission, values, expert advisors, and progress snapshots in a single YAML document.
- Render a consistently formatted summary using Jinja2 and share it as `PROJECT_SUMMARY.md`.
- Record when a stakeholder provides the **`Next`** keyword that unlocks the following delivery step.
- Provide approximate percentage-based progress updates so readers always know how close you are to completion.

## What’s included

- **Structured data model (`project.yaml`)** covering objectives, roadmap, experts, quality gates, and progress percentages with fictional sample contributors.
- **Markdown rendering template** (`docs/project_summary_template.md`) that transforms the data into a public-friendly briefing.
- **Rendering utility** (`scripts/render.py`) with a Makefile target for repeatable builds.
- **Pytest suite** validating the renderer’s core behaviours, so the workflow stays trustworthy.

## Quick start (2025 workflow)

1. Fork or clone this repository.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Copy and personalize the project data (a starter `project.yaml` is already included so you can skip this step unless you want a clean slate):
   ```bash
   cp project.yaml.example project.yaml
   ```
4. Replace the placeholder content in `project.yaml` with your project’s realities. Update progress percentages, document the experts you consult, and note who can speak the `Next` keyword for each stage.
5. Generate the shareable summary:
   ```bash
   make render
   ```
6. Review the generated `PROJECT_SUMMARY.md`. When it looks right, commit both `project.yaml` and the rendered summary.
7. Run the automated checks:
   ```bash
   pytest
   ```
8. Publish your repository or share the rendered brief with your collaborators. Each time you receive a new command or the `Next` keyword, update the YAML and re-render.

## Run locally

Reproduce the daily stability workflow on your workstation:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
# rehearse the daily stabilization locally
python scripts/daily/run_all.py
```

## ASCII workflow for new commands

When a new instruction arrives, follow this repeatable path to keep the brief reliable:

```
┌────────────┐    Next keyword?    ┌────────────┐
│ Receive cmd│ ───────────────────►│ Validate   │
└─────┬──────┘        yes/no       └─────┬──────┘
      │                               │
      │ no                            │ yes
      ▼                               ▼
┌────────────┐    clarify intent   ┌────────────┐
│ Ask details│ ◄────────────────── │ Update data│
└─────┬──────┘                      └─────┬──────┘
      │                                   │
      ▼                                   ▼
┌────────────┐    run tests        ┌────────────┐
│ Render md  │────────────────────►│ Share brief│
└────────────┘                     └────────────┘
```

Refer back to this diagram whenever you iterate—the `Next` keyword gates your advancement to the next milestone.

## Project data structure

All canonical information lives in `project.yaml`. The schema below reflects the 2025 defaults. You can freely extend or trim fields; the renderer mirrors what you provide.

```yaml
name: Sample Project
slug: sample-project
status: exploring
tagline: Write a short, inspiring one-liner.
owners:
  - name: Leyla Demir
    role: Product lead
    contact: leyla@example.com
overview:
  problem: What are you trying to solve?
  solution: How will you solve it?
  impact: What value will this deliver?
values:
  - name: Transparency
    description: Communicate openly and share progress often.
  - name: Quality
    description: Deliver maintainable, well-tested software.
experts:
  - name: Dr. Mira Byte
    speciality: Systems architecture
    advice: Keep interfaces decoupled and well documented.
quality_gates:
  - name: Automated tests
    description: "pytest must pass before sharing updates."
  - name: Peer review
    description: A domain expert must approve each milestone.
objectives:
  - title: Launch an MVP
    status: planned
    progress_percent: 35
    next_keyword_holder: Product sponsor
    success_metrics:
      - 50 early-access signups
      - Collect qualitative feedback from 10 users
    notes: Focus on the must-have journey only.
  - title: Automate CI pipeline
    status: planned
    progress_percent: 10
    next_keyword_holder: Platform lead
    success_metrics:
      - Tests run on every pull request
      - Deployment button for staging
roadmap:
  - milestone: Foundation
    due: 2025-03-15
    owner: Leyla Demir
    focus: Authentication, project setup
  - milestone: Beta
    due: 2025-06-01
    owner: Leyla Demir
    focus: Onboarding, feedback loop
progress_updates:
  - date: 2025-01-05
    percent_complete: 25
    summary: Core architecture reviewed by experts; waiting on Next keyword.
  - date: 2025-02-12
    percent_complete: 40
    summary: MVP endpoints coded and passing pytest suite.
artifacts:
  code: https://github.com/your-user/your-repo
  design: https://www.figma.com/file/.../your-designs
  docs: https://docs.example.com/project
notes: Include any additional context your stakeholders should know.
```

### Tips for tailoring the data

- **Track progress responsibly:** Percentages do not need to be perfect; aim for realistic snapshots so readers understand momentum.
- **Highlight expert insight:** Add as many experts as you consult. Their guidance builds trust in your plan.
- **Record Next keyword owners:** For every objective, specify who can supply `Next` to unlock subsequent work.
- **Document quality gates:** List every test or review you must pass before announcing progress.

## Rendering workflow

The `scripts/render.py` script reads `project.yaml`, renders the markdown template (`docs/project_summary_template.md`), and writes the finished document to `PROJECT_SUMMARY.md`.

To run it manually:

```bash
python scripts/render.py
```

Prefer `make render` for a one-line command that resolves paths correctly.

Whenever you change `project.yaml`, re-render and commit both the data and output. This keeps your brief auditable.


## Refactor Workflow
- Open a ticket via the `Refactor` issue template
- Branch naming: `rf/<area>/<short-topic>`
- CI: `refactor-guard` runs automatically on the PR
- Coverage must stay ≥ 85% and public API remains unchanged (RFC required otherwise)

## Directory layout

```
.
├── README.md
├── Makefile
├── requirements.txt
├── project.yaml.example
├── docs/
│   └── project_summary_template.md
├── scripts/
│   └── render.py
├── samples/
│   └── PROJECT_SUMMARY.sample.md
└── tests/
    └── test_render.py
```

## Customize the template

- **Data model freedom:** Add fields for budgets, design tokens, or anything else. Undefined values simply won’t render.
- **Layout control:** Adjust headings or add tables in `docs/project_summary_template.md` to match your communication style.
- **Automation friendly:** Use the `--data`, `--template`, and `--output` flags in `scripts/render.py` to integrate rendering into CI/CD pipelines.

## Sharing your project

Once `PROJECT_SUMMARY.md` looks right:

- Publish it as the main README of your project repository.
- Share it with stakeholders so they can review progress, expert advice, and `Next` keyword ownership.
- Update it after every milestone, expert review, or major command. Re-run the tests and renderer before communicating updates.

## License

This template is released under the [MIT License](LICENSE). You can reuse and adapt it for any purpose.
