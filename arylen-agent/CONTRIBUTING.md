# Contribution guide

Follow these steps to contribute to Arylen Agent.

1. **Clone and prepare the environment**
   - `python -m venv .venv && source .venv/bin/activate`
   - `pip install -r requirements.txt`

2. **Code quality**
   - Lint: `make lint`
   - Tests: `make test`
   - Combined CI target: `make ci`

3. **Plan and Kanban**
   - Track the delivery steps in `PLAN.md`, and mark progress with `python scripts/next.py`.
   - Review the Kanban policies in `docs/KANBAN.md`.

4. **Pull requests**
   - Reference the responsible role and acceptance criteria in every PR description.
   - Run `python scripts/staff.py --codeowners` when you need to refresh the roster or CODEOWNERS file.

5. **Code of conduct**
   - Every contribution must comply with `CODE_OF_CONDUCT.md`.
