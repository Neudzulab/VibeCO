<!--
  Scope: Repository-wide change history for VibeCO.
  Last updated: Recorded the v0.7.4 release with the endpoint validator refinements, documentation refresh, the TODO capture principle update in the root agent guide, and the persistent TODO tracker rollout.
-->

# Changelog

All notable changes to this project will be documented in this file.

The format follows the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) convention and adheres to Semantic Versioning as described in [docs/VERSIONING_PLAN.md](docs/VERSIONING_PLAN.md).

<!-- Maintainer note: Unreleased section documents checklist/policy updates pending next tagged release. -->

## [Unreleased]
### Added
- Endpoint validation engine (`src/vibeco/endpoint_validator.py`) with CLI support for discovery,
  streaming-aware probing, and Markdown/JSON reporting.
- Default configuration, allowlist scaffolding, and documentation updates for the validator
  workflow.
- Continuous integration workflow exercising the endpoint validator against httpbin on pull
  requests and a scheduled cadence.
- Batch validation capabilities enabling a single configuration to orchestrate multiple
  microservice or gateway checks with shared summary reporting.
- Repository TODO tracker (`TODO.md`) capturing the checkbox-first backlog agents must maintain.

### Changed
- CLI now supports per-run labels and multi-target YAML files, emitting consolidated Markdown
  and JSON outputs for heterogeneous environments.
- Documented the requirement to capture large or time-intensive work as TODO entries in the canonical task list within the root agent guide.
- Expanded agent guidance to point at the persistent TODO tracker and outline placement rules for new entries.

### Removed
- _None_

## [v0.7.4] - 2025-10-27
### Added
- Endpoint validation engine (`src/vibeco/endpoint_validator.py`) with CLI support for discovery,
  streaming-aware probing, and Markdown/JSON reporting.
- Default configuration, allowlist scaffolding, and documentation updates for the validator
  workflow.
- Continuous integration workflow exercising the endpoint validator against httpbin on pull
  requests and a scheduled cadence.

### Changed
- Hardened payload synthesis and streaming cleanup in the endpoint validator engine to avoid
  resource leaks and ensure JSON bodies are transmitted correctly.

### Removed
- _None_

## [v0.7.3] - 2025-10-23
### Added
- `arylen-agent/AGENTS-REQUESTS.md` as the ready-to-use ledger so requesting agents can log synchronization-bound work items without maintainer intervention.
- Structured pytest summary reporting in the shared Windows harness so every runner prints success, failure, error, warning, and ignored counts.

### Changed
- Synced README quick start and architecture tree with the canonical v0.7.3 guidance while shortening the quick update prompt.
- Highlighted the junitxml summary requirement in `AGENTS.md`, refreshed the PowerShell helper documentation, and linked the ledger workflow updates across the docs.

### Removed
- _None_

## [v0.7.2] - 2025-10-22
### Added
- `AGENTS_SAMPLE.md` as the official, ready-to-adapt template for downstream teams to craft their own agent guides while mirroring VibeCO expectations.

### Changed
- Re-centered the root `AGENTS.md` on onboarding agents who clone VibeCO, refreshed automation guidance, and pointed readers at the renamed sample file.
- Bumped the README header note and version badge to advertise the v0.7.2 release and highlight the quick update workflow alignment.

## [v0.7.1] - 2025-10-21
### Added
- `clarification.yaml.example` illustrating how to request and return focused decision checkpoints without stalling other workstreams.

### Changed
- Refined the repository-wide `AGENTS.md` to limit clarification requests to concrete option selections and renamed the workflow to `clarification.yaml`.

## [v0.7.0] - 2025-10-20
### Added
- Repository-wide contribution checklist in `AGENTS.md` enforcing file headers, architecture tree maintenance, roadmap alignment, and changelog hygiene.
- Quick VibeCO update assistant prompt in `README.md` so legacy clones can automatically adopt checklist requirements.

### Changed
- Bumped the README version badge to `v0.7.0` and annotated the file header to reflect the new documentation release.

## [v0.6.5] - 2025-10-19
### Added
- Continuation workflow guidance for extending `AGENTS.md`, including orphan detection, inconsistency tracking, and `netlestirme.yaml` coordination steps.

### Changed
- Updated documentation references to advertise the v0.6.5 milestone badge.

## [v0.6.0] - 2025-10-18
### Added
- Documented engineering principles covering orphaned code handling, architecture tree maintenance, change logging, versioning discipline, bug-first prioritisation, and comprehensive identifier updates during port/path/env renames.
- Renderer guardrails that restrict bundled mock project data to demo mode and new registry documenting all mock/demo resources.
- One-command bootstrap script (`scripts/bootstrap.sh`) that provisions the virtual environment, installs dependencies, seeds `project.yaml`, and renders the sample summary.

### Changed
- README now leads with the local quick start, clarifies the assistant prompt as an optional path, and refreshes the architecture tree to match the current repository layout.
- Version references updated to advertise the v0.6.0 milestone badge.

