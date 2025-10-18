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
- Prioritise the latest stable versions of libraries and their compatible transitive dependencies; treat upgrades as part of routine maintenance rather than exceptional work.
- Investigate and eliminate warnings in dependency installation and runtime/test logs—warnings are signals of impending failures, not noise to ignore.
- Balance forward-looking adoption with compatibility guarantees by validating new versions against existing integration contracts before promotion to production.
- Keep build and runtime infrastructure (CI pipelines, local tooling, deployment manifests) ready for rapid upgrades so we can adopt new releases without disruptive rewrites.
- Pin Docker images to the most recent stable tags and review them regularly to benefit from security patches and performance improvements while avoiding regressions.
- When adjusting ports, filesystem paths, environment variables, or other cross-cutting identifiers, run a repository-wide search for the previous name and update every callsite to avoid split-brain behaviour.
- Never bypass critical/priority services in workflows or scripts; design changes should respect existing stabilisation guards.
- Treat bug resolution as the highest priority—stabilise failing paths before pursuing net-new features.
- Uphold clean-code fundamentals: expressive naming, focused functions, comprehensive tests around critical seams, and consistent formatting.

## Code review kontrolleri

- [ ] Değişen dosyanın en üstündeki agent kılavuzu/Amaç-Ana Akış-İlgili Testler bloğu güncel mi?
- [ ] Yeni dosyalar için `docs/file_agent_template.md` rehberine uygun bir özet eklendi mi?
