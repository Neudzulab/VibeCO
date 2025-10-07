# Refactor Playbook

## Objectives
- Improve internal quality **without changing external behaviour**.
- Raise code health using measurable metrics.

## Rules (TL;DR)
1. **Scope clarity:** Every refactor ticket targets a single module/focus area.
2. **API immunity:** Public API must remain unchanged. If not, produce an RFC and attach `agent_proposal`.
3. **Test safety:** Coverage must stay `>= 85%`. Behavioural tests remain intact.
4. **Metrics:** Track LCOM, cyclomatic complexity, LOC, and duplication in `docs/METRICS.md`.
5. **Rollback plan:** Each PR documents a rollback path.
6. **Branch naming:** `rf/<area>/<short-topic>`.
7. **Commit format:** `refactor: ...` (conventional commits).

## Flow
Backlog → **Refactor Ready** → In Progress → In Review → QA → Done

## Risk Checklist
- [ ] External behaviour unchanged
- [ ] Public API untouched (or RFC provided)
- [ ] Coverage target met
- [ ] No performance regression
- [ ] Rollback instructions included
