# Code Health Guide
- Ship small increments with frequent PRs.
- Guard clear boundaries; design interfaces first.
- Lean on guard classes and adapter patterns when stabilising seams.

## Engineering principles

- Remove or relocate orphaned files/directories immediately; if future resurrection is likely, park them in a clearly labelled `archive/` or `obsolete/` module with rationale.
- Avoid competing or duplicated implementations that could create divergent behaviour—prefer shared utilities and well-defined single sources of truth.
- Maintain the architecture tree in [`README.md`](../README.md); add new endpoints/services there as they appear and annotate any planned or partially implemented work until it ships.
- Keep `CHANGELOG.md` synchronized with every merged change so the delivery narrative is auditable.
- Follow the semantic versioning rules in [`docs/VERSIONING_PLAN.md`](VERSIONING_PLAN.md) and ensure each release increments correctly.
- When adjusting ports, filesystem paths, environment variables, or other cross-cutting identifiers, run a repository-wide search for the previous name and update every callsite to avoid split-brain behaviour.
- Never bypass critical/priority services in workflows or scripts; design changes should respect existing stabilisation guards.
- Treat bug resolution as the highest priority—stabilise failing paths before pursuing net-new features.
- Uphold clean-code fundamentals: expressive naming, focused functions, comprehensive tests around critical seams, and consistent formatting.
