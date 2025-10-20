<!--
  File: AGENTS_SAMPLE.md
  Purpose: Ready-to-adapt agent instruction template that demonstrates how downstream teams can tailor VibeCO guidance.
  Last updated: Provide a structured example covering setup, documentation hygiene, and release coordination for local projects.
-->

# Agent Guide Template (rename as needed)

Welcome! Copy this file into your own project (renaming it to match your conventions) and replace the placeholder text with guidance that reflects your team’s workflow. The sections below mirror the expectations defined in the canonical VibeCO repository so you can stay aligned while customising details for your context.

## 1. Project snapshot
- **Mission:** Summarise the product or service your repository delivers.
- **Key docs:** Link to your README, architecture diagrams, roadmap, and any onboarding briefings.
- **Primary owners:** List the contact points responsible for approvals or clarifications.

> ✅ Replace every bullet with project-specific information before sharing this file with collaborators.

## 2. Environment bootstrap
1. **Clone & dependencies**
   - Include the exact command to initialise the repo (e.g., `git clone` or `gh repo clone`).
   - Document prerequisite system packages, environment variables, and secrets.
2. **Bootstrap command**
   - Reference your local equivalent of `./scripts/bootstrap.sh` or document the sequence of steps to install dependencies and seed sample data.
3. **Verification**
   - Specify how to render or build the primary artifact (for VibeCO, `make render` or `python scripts/render.py`).
   - List the smoke tests that confirm the installation succeeded.

## 3. Required hygiene
- **File headers:** Ensure contributors add purpose headers to every Markdown, Python, YAML, or config file they create or substantially update.
- **README tree:** Keep the architecture tree up to date whenever components move, appear, or vanish.
- **Changelog discipline:** Record every meaningful change in `CHANGELOG.md` under the correct semantic version heading.
- **Roadmap sync:** Update `PLAN.md` and `PROJECT_SUMMARY.md` whenever scope, timelines, or owners shift.

Encourage reviewers to block merges if any of these elements are missing from a pull request.

## 4. Release cadence
- Document your versioning scheme (semantic versioning is recommended).
- Provide the checklist for cutting a release, including tagging, documentation updates, and announcement channels.
- Call out who approves version increments and how hotfixes are handled.

## 5. Quick update prompt (keep aligned with VibeCO)
If your downstream project inherits the VibeCO quick update workflow, link to the canonical prompt in the README and verify it points at the correct repository/tag. Note any additional files your fork requires when the automation runs.

## 6. Support channel
Describe how agents and contributors should request help—Slack channel, issue tracker labels, weekly triage meeting, etc. Include expected response times for urgent vs. routine questions.

---

Feel free to delete sections that do not apply, but ensure the final document covers onboarding, tooling, documentation hygiene, release management, and update automation.
