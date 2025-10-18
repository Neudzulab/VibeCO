# Architecture Governance Playbook

This playbook captures the principles we apply across VibeCO projects when multiple
agents collaborate on the same codebase. It provides a reference implementation that
future teams can adopt and tailor when they spin up new services.

## 1. Test Hygiene and Relocation Flow

1. **Audit non-standard tests** – Use `rg "(demo|manual|tmp|todo)"` within
   production directories to locate exploratory code or temporary fixtures.
2. **Decide the target suite** – For every discovered block, determine whether it
   belongs to `tests/unit`, `tests/integration`, or `tests/e2e` based on its external
   dependencies.
3. **Move, then adapt** – Physically relocate the code into the proper suite and
   adjust imports/fixtures. Remove orphaned helpers from production modules.
4. **Lock behaviour** – Run `pytest -q` to confirm coverage and preserve baseline
   assertions before continuing with refactors.
5. **Document the move** – Update the associated file agent guides (see below) so the
   rationale for the relocation stays discoverable.

> **Tip:** Add a pre-commit hook that fails when files under `src/` or `scripts/`
> contain `pytest`-style asserts or references to demo fixtures.

## 2. File Agent Guides

Large or high-churn modules must begin with a short “agent guide” comment describing:

- **Purpose** – What the file owns and the boundaries it enforces.
- **Key flows** – Entry points, orchestrated helpers, and downstream dependencies.
- **Relevant tests** – Suites or fixtures that guard the behaviour.

### Template

```text
# Agent Guide
# Purpose: <one sentence>
# Key Flows:
#   - <callable or scenario>
# Relevant Tests:
#   - <path::test_name>
```

When modifying the file, update the guide first, then the implementation. Reviewers
check that the guide still matches reality.

## 3. Port Mapping Registry

Maintain `docs/PORT_MAPPING.md` as the single source of truth for service ports.
Every change to network bindings must update this file before merging.

Checklist for releases:

- [ ] API gateway routes reflect the current microservice set.
- [ ] Downstream services expose only the documented ports.
- [ ] Deprecated ports are marked with the removal date and mitigation steps.

## 4. Encouraging Smaller, Composable Files

- Cap files at **~200 logical lines** where possible.
- Extract reusable flows into helper modules under `src/<domain>/` and import them.
- Prefer declarative configuration (YAML/TOML) instead of procedural constants in
  Python scripts.
- Highlight exceptions in the agent guide when a file must stay large.

## 5. Automation & Process Hooks

- **CI** – Add a job that validates agent guides exist for files over the line cap
  and that the port mapping registry lists any exposed ports in Docker compose or
  Kubernetes manifests.
- **PR Template** – Require authors to tick boxes for:
  - “Agent guide updated?”
  - “Port mapping reviewed?”
  - “Tests relocated if needed?”
- **Monthly maintenance** – Run `scripts/refactor_guard.py` in report mode to list
  files missing guides or containing demo artefacts.

By following this playbook we minimise architectural drift, keep demos isolated, and
make onboarding smoother for new contributors.
