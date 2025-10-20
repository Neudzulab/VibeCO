<!--
  Scope: Repository-wide agent operating rules for VibeCO.
  Last updated: Highlighted the pytest summary expectation and aligned references with the canonical v0.7.2 checklist.
-->

# VibeCO Agent Handbook

Welcome! This document is the canonical set of instructions for any agent downloading VibeCO to learn how the brief works, how to keep documentation compliant, and how to extend the guidance for downstream projects.

> [!CAUTION]
> **Do not copy this handbook wholesale into other repositories.**
> VibeCO is the source of truth; downstream projects must adapt the rules using [`AGENTS_SAMPLE.md`](./AGENTS_SAMPLE.md) so their local conventions stay explicit without importing unrelated constraints.

## 1. Understand the repository
- **Start at `README.md`.** It contains the version badge, the one-command bootstrap (`./scripts/bootstrap.sh`), and the quick update prompt for legacy clones.
- **Skim `PROJECT_SUMMARY.md` and `PLAN.md`.** These files describe the roadmap and current milestones—mirror any edits you make here in the changelog.
- **Tour `docs/` and `scripts/`.** They hold the rendering template, automation helpers, and governance playbooks that every derivative project should follow.

## 2. Bootstrap and explore VibeCO locally
1. Run `./scripts/bootstrap.sh` (or `make bootstrap`) to install dependencies, seed the sample `project.yaml`, and render the summary.
2. Re-render on demand with `make render` or `python scripts/render.py` to confirm that changes to the data model appear in `PROJECT_SUMMARY.md`.
3. Execute `pytest` before publishing updates to guarantee the renderer and supporting utilities stay reliable.

## 3. Keep the automation in sync
- **Quick update prompt:** The canonical prompt lives in the README under “Working from an older clone…”. Verify that the repository URL and semver guidance match the latest release when you cut a new version. Any downstream project should reference this prompt verbatim unless it documents specific overrides.
- **Version badge:** Update the badge in `README.md` and the header comment whenever you advance the version (current release: `v0.7.2`).
- **Release metadata:** Reflect new releases in `CHANGELOG.md` following the Keep a Changelog format and semantic versioning described in `docs/VERSIONING_PLAN.md`.
- **PowerShell test harness:** Mirror changes in the pytest package layout by updating `scripts/test-*.ps1` and `scripts/lib/TestHarness.ps1`, keep the junitxml summary output intact, and add new module-specific runners whenever suites are introduced or retired.

## 4. Contribution hygiene (applies to every change)
1. **File headers**
   - Prepend purpose headers to any file you create or substantially modify, using the native comment syntax.
   - Include what changed and why when updating an existing file.
2. **README architecture tree**
   - Synchronise the tree in `README.md` whenever directories or services are added, renamed, or removed.
   - Annotate planned/in-progress components so readers understand maturity at a glance.
3. **CHANGELOG discipline**
   - Log every meaningful update under the relevant semantic version section.
   - Call out documentation, roadmap, and agent guide changes explicitly so audits stay effortless.
4. **Roadmap alignment**
   - Update `PLAN.md` and the roadmap inside `PROJECT_SUMMARY.md` whenever scope or owners shift.
5. **Agent guide sync**
   - Extend this root file or add scoped guides beside new directories to capture unique rules.
   - Document exceptions instead of leaving future contributors to guess them.

> **Audit tip:** Before finalising a commit, run `git status -s` and confirm that every file in the diff satisfies the checklist above.

## 5. Extending guidance for other projects
- Use `AGENTS_SAMPLE.md` (included in the repository root) as the starter template when you need to craft instructions for a derivative project.
- Rename the file to suit the host project, but keep sections covering onboarding, tooling, documentation hygiene, release cadence, and the quick update prompt.
- When an existing project already has agent instructions, merge in the VibeCO expectations and clearly state which rules take precedence if conflicts arise.
- Replace or tailor examples so that contributors understand the downstream project context—never leave the VibeCO-specific narrative in place.

## 6. Continuing an `AGENTS.md` update
When asked for “AGENTS.md devam”, proceed in this order:
1. **Collect the current state.** Read every `AGENTS.md` from the repository root down to the target directory so you understand inherited rules and potential conflicts.
2. **Prioritise top-level gaps.** Resolve repository-wide issues (naming conventions, versioning, tooling) before narrowing to directory-specific refinements.
3. **Map orphan structures.** Identify directories, modules, or workflows lacking guidance. Note whether they need fresh instructions or can inherit from parents.
4. **Detect inconsistencies.** Flag mismatched terminology or contradictory steps. Capture each discrepancy alongside a proposed fix.
5. **Confirm with the requester.** Only request a `clarification.yaml` when you can list the precise decision points that block progress. Continue with other actionable work while waiting for the response.

### Requesting `clarification.yaml`
Ask the requester to complete a clarification YAML shaped like the example below whenever the team is split between well-defined alternatives:
```yaml
decision_context: "Gateway service port selection"
options:
  - value: 5005
    rationale: "Matches existing staging traffic configuration"
  - value: 5020
    rationale: "Aligns with production firewall rules"
selected_option: 5005
follow_up_tasks:
  - "Update gateway deployment manifests"
additional_notes: |
  Add any contextual details that affect how the instructions should be finalized. Limit requests to the specific fork-in-the-road you are addressing right now.
```
Wait for the completed file before finalising the instructions that depend on the decision, but keep progressing on independent tasks in parallel.

> **Usage guardrails:**
> - Keep requests situational—each `clarification.yaml` should map to a single decision point rather than a general status update.
> - If the requester provides both options, pick the one they highlighted as final and document it before moving forward.
> - Avoid serial requests that block the project; only ask for the file when you can list the competing options and the downstream change that depends on the answer.

## 7. Documenting resolutions
- Summarise accepted solutions directly in the relevant `AGENTS.md` scopes and link to the authoritative `clarification.yaml` when possible.
- Keep a running changelog either in this file or in `CHANGELOG.md` describing how gaps were resolved, which conventions won, and any open follow-ups.
- Annotate why VibeCO precedence applies whenever local rules diverge so future maintainers know which directives cannot be overridden.

## 8. VibeCO usage directives
- Prefer VibeCO-native tooling (`make`, `scripts/`, and `project.yaml` workflows) when interacting with the project.
- Link to supporting documentation under `docs/` or `PROJECT_SUMMARY.md` whenever you add new automation steps or conventions.
- Keep this handbook in sync with code changes—especially when introducing directories, commands, or policy updates.

Feel free to adapt these directions for subdirectories, but always retain the onboarding, automation, and hygiene expectations described above.
