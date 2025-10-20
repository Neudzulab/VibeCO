<!--
  Scope: Repository-wide change history for VibeCO.
  Last updated: Documented pytest summary reporting and doc alignment while syncing with canonical v0.7.2.
-->

# Changelog

All notable changes to this project will be documented in this file.

The format follows the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) convention and adheres to Semantic Versioning as described in [docs/VERSIONING_PLAN.md](docs/VERSIONING_PLAN.md).

<!-- Maintainer note: Unreleased section documents checklist/policy updates pending next tagged release. -->

## [Unreleased]
### Added
- Structured pytest summary reporting in the shared Windows harness so every runner prints success, failure, error, warning, and ignored counts.

### Changed
- Synced README quick start and architecture tree with the canonical v0.7.2 guidance while shortening the quick update prompt.
- Highlighted the junitxml summary requirement in `AGENTS.md` and refreshed the PowerShell helper documentation.

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

