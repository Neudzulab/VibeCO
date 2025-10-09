# Versioning strategy

This document defines how every pull request maps to a semantic version so the repository history stays predictable across all projects.

## Version format and starting point
- Versions use `vMAJOR.MINOR.PATCH` (Semantic Versioning 2.0.0).
- All projects begin at **`v0.1.0`**.
- Version tags are applied to the main branch after the pull request merges.

## Pull request flow
1. When a pull request is opened, evaluate the change scope using the criteria below.
2. Update the project changelog or release notes draft with the planned version bump.
3. After merge, create a git tag (e.g., `git tag v0.1.0 && git push origin v0.1.0`).
4. Communicate the version in the PR description and any deployment announcements.

## Selecting the version bump
| Change type | Examples | Version increment |
|-------------|----------|-------------------|
| **Major**   | Backward-incompatible API change, database migration requiring manual intervention, removal of a supported integration | `MAJOR + 1`, `MINOR = 0`, `PATCH = 0` |
| **Minor**   | Backward-compatible feature, new endpoint, new configuration capability | `MINOR + 1`, `PATCH = 0` |
| **Patch**   | Bug fix, documentation-only update, refactor without behaviour change | `PATCH + 1` |

> **Note:** While the starting version is `v0.1.0`, continue to follow the same rules; breaking changes before `1.0.0` still trigger a major bump (e.g., `v0.2.0 → v1.0.0`).

## Cross-project planning
To keep versioning consistent across multiple repositories:
- Store this document (or a link to it) in each project.
- Add a CI check or manual checklist item to confirm the version bump before approving a PR.
- Include the targeted version in the PR template to remind contributors.
- Align release notes sections (e.g., Features, Fixes, Breaking) so they match the bump table above.

## Example timeline
| PR | Description | Version |
|----|-------------|---------|
| #1 | Initial scaffold and documentation | `v0.1.0` |
| #2 | Adds a new feature without breaking changes | `v0.2.0` |
| #3 | Fixes a regression | `v0.2.1` |
| #4 | Introduces a breaking API change | `v1.0.0` |

Consistently applying this workflow ensures every pull request results in a clearly communicated release version.
