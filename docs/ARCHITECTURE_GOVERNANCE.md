# Architecture Governance Playbook

This playbook captures the standards we apply when multiple agents collaborate on
the same VibeCO deployment. The goal is to keep architectural intent obvious,
prevent “temporary” experiments from leaking into production code, and offer a
repeatable blueprint that future project teams can copy.

## 1. Test hygiene and relocation flow

1. **Audit non-standard tests** – Search production folders with
   `rg "(demo|manual|tmp|todo)"` to find exploratory code or temporary fixtures.
2. **Pick the proper suite** – Decide whether the snippet belongs in
   `tests/unit`, `tests/integration`, or `tests/e2e` based on its dependencies.
3. **Move and adapt** – Relocate the block, update imports/fixtures, and remove
   orphaned helpers left behind in production modules.
4. **Lock behaviour** – Run `pytest -q` to re-establish the baseline assertions
   before continuing with refactors.
5. **Document the move** – Update the affected file agent guides so the
   rationale stays discoverable for the next person.

> **Automation hint:** Add a pre-commit hook that fails when files under `src/`
> or `scripts/` contain `pytest`-style asserts or references to demo fixtures.

## 2. File agent guides and modularisation

Large or high-churn modules start with an “agent guide” comment describing:

- **Purpose** – What the file owns and the boundaries it enforces.
- **Key flows** – Entry points, orchestrated helpers, and downstream
  dependencies.
- **Relevant tests** – Suites or fixtures that guard the behaviour.

Template:

```text
# Agent Guide
# Purpose: <one sentence>
# Key Flows:
#   - <callable or scenario>
# Relevant Tests:
#   - <path::test_name>
```

Whenever you touch a file, refresh the guide before changing the implementation.
Prefer small modules over sprawling ones; if a guide spans more than a handful of
bullets, split the implementation and have each file host its own guide.
Supporting data or shared routines should live in helper modules that callers
`import`, never copied inline.

## 3. Port mapping source of truth

The canonical port inventory lives in **two** places and must stay in sync:

- `configs/port_mapping.yaml` – Machine-readable snapshot for automated checks,
  dashboards, and incident tooling.
- `docs/PORT_MAPPING.md` – Human-facing explanation with verification steps and
  operational context.

Treat the port map as the first file to consult before adjusting the gateway or
any microservice listener. When a change is required:

1. Propose the new values by editing the YAML.
2. Mirror the update in the markdown table and include any operational notes.
3. Update manifests (Docker Compose, Helm charts, Terraform, etc.) in the same
   change list.
4. Have reviewers confirm the YAML and markdown agree before merging.
5. Publish the update via release notes and stand-up callouts.

## 4. Automation & process hooks

- **CI checks** – Validate that files over the line-count threshold contain an
  agent guide, and that the YAML port mapping matches declared ports in
  manifests.
- **PR template** – Require authors to tick boxes for:
  - “Agent guide updated?”
  - “Port mapping reviewed/updated?”
  - “Tests relocated if needed?”
- **Monthly maintenance** – Run `scripts/refactor_guard.py --report` to list
  files missing guides or containing demo artefacts, and compare the YAML port
  map against live environments.

By following this playbook we minimise architectural drift, keep demos isolated,
and make onboarding smoother for every contributor.
