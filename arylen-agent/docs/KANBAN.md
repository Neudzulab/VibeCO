# Kanban Board

## Columns (WIP limits)
- Backlog (∞)
- Ready (10)
- In Progress (7)
- In Review (5)
- QA (4)
- Done (∞)

## Policies
- Any card in `In Progress` must have an assigned role or owner.
- Cards in `In Review` require the reviewer to differ from the implementer.
- Cards in `QA` must pass automated checks and manual acceptance criteria.
- The `Role:` field on each card must map to entries under `agents/roles`.

## Card template
**Title:** `<STEP-ID> Short summary`
**Role:** `<role-id>`
**Acceptance Criteria:** bullet list of expected outcomes
**Tests:** unit + integration coverage
**Links:** pull request, supporting RFC/Issue
