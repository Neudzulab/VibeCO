<!--
  Scope: Repository-wide agent operating rules for VibeCO.
  Last updated: Condensed the handbook to stay under 100 lines and clarified that changes belong in CHANGELOG.md.
-->

# VibeCO Agent Handbook (Condensed)

Welcome! Follow these rules when working in this repo.

## Core principles
- Use stable, non-deprecated dependencies; keep tests, linting, and type checks strict and warning-free.
- Keep architecture clean: modular, DI-friendly, and maintainable.
- Keep files under 1000 lines; split into logical modules unless critically impossible.
- Do not add a changelog section here; record changes in `CHANGELOG.md`.
- Keep this file under 100 lines.

## Microservice routing audit (only when the plan is microservices)
- Parse the README endpoint tree.
- Verify each endpoint exists in its service routes and the API gateway configuration.
- Append inline badges to each endpoint line: ✅ [Service], ✅ [Gateway], ⚠️ [Service?], ⚠️ [Gateway?], or 📝 [Planned].
- Output a JSON array with missing/planned endpoints (service, method, path, status, missing, notes).
- Optional: short coverage table. Do not delete existing README text.

## Start here
- Read `README.md` first, then `PROJECT_SUMMARY.md` and `PLAN.md`.
- Review `docs/` and `scripts/` for automation and governance.

## Bootstrap & checks
- Bootstrap: `./scripts/bootstrap.sh` or `make bootstrap`.
- Render: `make render` or `python scripts/render.py`.
- Run tests: `pytest` before publishing updates.

## Contribution hygiene
1. **File headers**: add/update purpose headers; note what changed and why.
2. **README tree**: sync when directories/services change.
3. **Changelog**: log meaningful updates in `CHANGELOG.md`.
4. **Roadmap**: update `PLAN.md` and `PROJECT_SUMMARY.md` when scope/owners change.
5. **Agent guidance**: add scoped AGENTS files for new directories.
6. **TODOs**: record large efforts in `TODO.md` near related tasks.

## Guidance for downstream projects
- Use `AGENTS_SAMPLE.md` as a starting template; adapt to the host project.
- Merge local rules explicitly; call out precedence when VibeCO rules win.

## Clarification workflow
- Request `clarification.yaml` only for concrete decision points; keep working on other tasks.
- If options are provided, pick the selected option and document it.
