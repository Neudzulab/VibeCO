# Changelog

All notable changes to this project will be documented in this file.

The format follows the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) convention and adheres to Semantic Versioning as described in [docs/VERSIONING_PLAN.md](docs/VERSIONING_PLAN.md).

## [Unreleased]

## [v0.6.0] - 2025-10-18
### Added
- Documented engineering principles covering orphaned code handling, architecture tree maintenance, change logging, versioning discipline, bug-first prioritisation, and comprehensive identifier updates during port/path/env renames.
- Renderer guardrails that restrict bundled mock project data to demo mode and new registry documenting all mock/demo resources.
- One-command bootstrap script (`scripts/bootstrap.sh`) that provisions the virtual environment, installs dependencies, seeds `project.yaml`, and renders the sample summary.

### Changed
- README now leads with the local quick start, clarifies the assistant prompt as an optional path, and refreshes the architecture tree to match the current repository layout.
- Version references updated to advertise the v0.6.0 milestone badge.

