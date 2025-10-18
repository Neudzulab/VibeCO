# VibeCO

![Version 1.0 badge](https://img.shields.io/badge/version-1.0-7c3aed?style=for-the-badge)
[![refactor-guard](https://github.com/Neudzulab/VibeCO/actions/workflows/refactor.yml/badge.svg)](./.github/workflows/refactor.yml)
[![daily-stability](https://github.com/Neudzulab/VibeCO/actions/workflows/daily_stability.yml/badge.svg)](./.github/workflows/daily_stability.yml)

> [!IMPORTANT]
> ### 🚀 One-command quick start (assistant prompt)
> Send this prompt to your preferred coding assistant to clone VibeCO into the current workspace, set up dependencies, review the planning files (`PROJECT.md`, `PROJECT_SUMMARY.md`, `PROJECT_SUMMARY.yaml`, `PLAN.md`, etc.), and tailor its follow-up tasks to match the plan. The prompt targets the repository at `https://github.com/Neudzulab/VibeCO.git`.
>
> ```text
>You are a global engineering orchestrator.
>
>GOAL
>- Use https://github.com/Neudzulab/VibeCO.git as a READ-ONLY template source.
>- Apply its plan template to the CURRENT repository (the repo you are running in now).
>- Generate/update PLAN.md (and related docs) in the current repo using project.yaml / PROJECT_SUMMARY.yaml if present.
>- OPEN A PULL REQUEST on THIS repo (not on VibeCO). Do NOT instruct me to push; you handle PR creation using your default method.
>
>CONFIRMATION MODEL
>- Phase 0: Immediately PRINT a compact plan (tools, languages, agents), then start execution automatically.
>- After each milestone, PRINT a 1–2 sentence summary and PROMPT:
>  >> Type Next to continue, or STOP to pause.
>
>OPERATING PRINCIPLES
>- Idempotent and safe. Bash preferred; PowerShell if needed.
>- Echo each command with `$` before running; then print a one-line result.
>- On failure: print `ERR: <reason>`, retry once, then continue marked `ATTN`.
>- Never expose secrets. NEVER push to VibeCO; you may create the PR on the current repo using your built-in method.
>- Do not ask me to run git push; if authentication is missing, print a single clear manual PR instruction.
>
>SCOPE & FLOW
>
>MILESTONE A — ENV DISCOVERY
>- Detect OS/shell; log versions: git, python/py, pip, pytest (optional), gh (optional).
>
>MILESTONE B — LOCATE CURRENT REPO (TARGET)
>$ git rev-parse --show-toplevel || (echo "Initializing new repo"; git init && git add -A && git commit -m "chore: init")
>- Set TARGET_DIR to the current repo root.
>
>MILESTONE C — FETCH TEMPLATE REPO (READ-ONLY)
>$ cd "$(git rev-parse --show-toplevel)"
>$ [ -d ./_vibeco_templates ] || git clone --depth=1 https://github.com/Neudzulab/VibeCO.git _vibeco_templates
>$ (cd _vibeco_templates && git fetch --all --prune)
>- Do NOT modify or publish _vibeco_templates.
>
>MILESTONE D — FEATURE BRANCH (LOCAL)
>$ git fetch --all --prune || true
>$ git switch -c feat/plan-bootstrap || git switch feat/plan-bootstrap
>
>MILESTONE E — OPTIONAL PYTHON ENV (only if render tooling exists)
>$ (python3 -m venv .venv || python -m venv .venv) 2>/dev/null || echo "Venv skipped"
>$ [ -d .venv ] && source .venv/bin/activate || echo "No venv"
>$ [ -f requirements.txt ] && (python -m pip install --upgrade pip && pip install -r requirements.txt) || echo "No requirements"
>
>MILESTONE F — APPLY TEMPLATE → PLAN.md
>- Discover plan templates under `_vibeco_templates` matching:
>  `docs/**plan*`, `templates/**plan*`, `**/*.j2`, `**/PLAN*.md`, `**/*template*`
>- Load canonical data from `project.yaml` / `PROJECT_SUMMARY.yaml` in the CURRENT repo if present.
>- Render/generate in CURRENT repo:
>  • PLAN.md (Objectives, Roadmap/Milestones, Roles/Owners one-per-line, Deliverables & Acceptance, Risks, References)
>  • (If template requires) PROJECT_SUMMARY.md, ROADMAP.md, docs/*
>- Ensure owners render one-per-line without trailing whitespace.
>- Preserve existing non-templated sections.
>
>MILESTONE G — CHECKS (DOC-FIRST)
>$ [ -d tests ] && pytest -q || echo "No tests"
>$ git status -s
>
>MILESTONE H — CREATE PR (CURRENT REPO)
>- Create a Pull Request using your default method **without asking me to push**.
>- If authentication is missing, PRINT exactly one manual instruction: “Open a PR from feat/plan-bootstrap → main” (no push command).
>- PRINT the PR URL if created.
>
>MILESTONE I — FINAL STATUS
>- PRINT generated/updated files, notable changes, and any `ATTN` items.
>- PROMPT:
>  >> Type Next to continue, or STOP to pause.
>
> ```

Welcome to the 2025 edition of **VibeCO (Vibe Coding Orchestrator)**—a reusable project brief template designed so that every stakeholder immediately understands what you are building, why it matters, and how to unlock the next phase of work. Clone this repository, inject your own context, and publish a polished brief that keeps your team aligned from day zero.

## Why this repository exists

Modern software projects evolve quickly. VibeCO keeps your source-of-truth lightweight, explicit, and testable so you can:

- Capture your mission, values, expert advisors, and progress snapshots in a single YAML document.
- Render a consistently formatted summary using Jinja2 and share it as `PROJECT_SUMMARY.md`.
- Record when a stakeholder provides the **`Next`** keyword that unlocks the following delivery step.
- Provide approximate percentage-based progress updates so readers always know how close you are to completion.

## What’s included

- **Structured data model (`project.yaml`)** covering objectives, roadmap, experts, quality gates, and progress percentages with fictional sample contributors (see [`docs/mock_data_registry.md`](docs/mock_data_registry.md) for the demo/mock usage policy).
- **Markdown rendering template** (`docs/project_summary_template.md`) that transforms the data into a public-friendly briefing.
- **Rendering utility** (`scripts/render.py`) with a Makefile target for repeatable builds.
- **Pytest suite** validating the renderer’s core behaviours, so the workflow stays trustworthy.
- **Architecture governance playbook** (`docs/ARCHITECTURE_GOVERNANCE.md`) that captures
  test hygiene, file agent guides, and automation hooks for future services.
- **Port mapping registry** (`docs/PORT_MAPPING.md`) documenting the canonical network
  bindings for microservices and the API gateway, backed by
  [`configs/port_mapping.yaml`](configs/port_mapping.yaml) for automation.

## Quick start

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

## Architecture tree and update discipline

The top-level structure below captures the current operating architecture. Update this tree whenever you introduce new endpoints, components, or leave planned/partially completed work in the codebase so the status stays transparent.

```
VibeCO/
├── arylen-agent/                # Local assistant orchestration assets
├── configs/                     # Configuration presets consumed by renderers and scripts
│   └── port_mapping.yaml        # Machine-readable service-to-port bindings
├── docs/
│   ├── RUNBOOKS/                # Operational playbooks
│   ├── *.md                     # Engineering policies (code health, metrics, refactors, etc.)
│   ├── ARCHITECTURE_GOVERNANCE.md # Agent guide, testing, and port registry rules
│   ├── PORT_MAPPING.md          # Human-readable registry (keep in sync with configs/port_mapping.yaml)
│   └── project_summary_template # Rendering templates
├── scripts/
│   ├── daily/                   # Daily stability workflows
│   └── render.py                # Markdown generation entry point
├── samples/                     # Example data inputs
├── tests/                       # Pytest suites guarding the renderer
├── artifacts/                   # Generated outputs (keep tidy; archive obsolete items)
├── reports/                     # Stability and analysis outputs
├── CHANGELOG.md                 # Mandatory running history of shipped changes
├── PLAN.md / PROJECT_SUMMARY.*  # Planning and stakeholder alignment sources
├── README.md                    # Living overview (update this tree when topology changes)
└── (planned)
    └── endpoints/               # Placeholder for future service endpoints (document status here if added)
```

- Never leave orphaned files or directories. Archive anything intentionally dormant under a clearly marked `obsolete` or `archive` path so future contributors understand its status.
- Note partially implemented or planned work directly in the tree until it is complete.
- Keep `CHANGELOG.md` current so every change is traceable, and follow the semantic versioning flow described in [`docs/VERSIONING_PLAN.md`](docs/VERSIONING_PLAN.md).
- When renaming ports, filesystem paths, environment variables, or similar integration touchpoints, search for the previous identifier across the repository and update every reference to prevent partial migrations.
- Review `docs/PORT_MAPPING.md` before changing any gateway or service binding. Treat
  mismatches as bugs and update the registry in the same commit.


## Versioning policy

Every merged pull request must produce a new semantic version tag starting from **`v0.1.0`**. Use the [versioning strategy](docs/VERSIONING_PLAN.md) to decide whether the change triggers a major, minor, or patch increment and include the planned version in the PR description before merging.

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

## Agent guardrails for completed work

To avoid accidental regressions after a task is marked complete:

- Treat every plan item with a checked (done) state as **locked**. Do not revisit, refactor, or optimize it unless a new instruction explicitly reopens the work.
- Redirect agent attention to the active sources of truth—`README.md`, `PLAN.md`, and any scoped `AGENTS.md` files—before making changes.
- Log and report if any automation or contributor attempts to modify a locked item so the project coordinator can intervene.
- Use retrospectives to confirm the guardrails remain effective and that agents continue progressing on active tasks instead of revisiting completed ones.

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
