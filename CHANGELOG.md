<!--
  Scope: Repository-wide change history for VibeCO.
  Last updated: Recorded the v0.7.0 release with checklist enforcement guidance and the quick update assistant prompt.
-->

# Changelog

All notable changes to this project will be documented in this file.

The format follows the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) convention and adheres to Semantic Versioning as described in [docs/VERSIONING_PLAN.md](docs/VERSIONING_PLAN.md).

<!-- Maintainer note: Unreleased section documents checklist/policy updates pending next tagged release. -->

## [Unreleased]
### Added
- Nothing yet.

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

