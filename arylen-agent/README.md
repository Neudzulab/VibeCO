# Arylen Agent

[![CI](https://github.com/VibeCO/arylen-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/VibeCO/arylen-agent/actions/workflows/ci.yml)

Arylen Agent is a reference automation project that coordinates a specialist crew and Kanban workflow. The repository provides team configuration utilities, process automation helpers, and a CI-ready baseline.

## Quick start
1. Clone the repository and install the dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the automated formatting and test steps:
   ```bash
   make ci
   ```

## Build the roster
Generate the recommended specialist roster and CODEOWNERS file for your project needs:
```bash
python scripts/staff.py
python scripts/gen_codeowners.py
```

## Use the Kanban workflow
The board columns, WIP limits, and card template live in `docs/KANBAN.md`.

## Plan progression
`PLAN.md` lists the steps mapped to each role. Use `python scripts/next.py` to mark the next step as complete or blocked.

## Coordinate multi-agent workspaces
Follow `docs/MULTI_AGENT_COLLAB_PROTOCOL.md` to implement the request-ledger collaboration
pattern across every project workspace. It explains how to structure owned folders,
operate the `AGENTS-REQUESTS.md` hub, and run sync scripts so that agents never overwrite
each other.

## Contributing
- Review `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` before sending a pull request.
- For tasks, bugs, and feature ideas, follow the templates under `.github/ISSUE_TEMPLATE`.
