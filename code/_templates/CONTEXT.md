# [Project Name]
> Project scaffolding templates — CONTEXT.md, README.md, SPECS.md, ROADMAP.md skeletons
> goal: none
> spec: none
<!-- goal: [slug](../../brain/goals/<slug>.md) — required on line 3 by pre-commit 1c, or 'none'.
     spec: flip to 'SPEC.md' once this module has a contract (author from _templates/module.SPEC.md);
     'none' opts out. New modules under code/ MUST declare a spec — see code/SPEC-DRIVE.md. -->

<!-- What: workspace routing and agent entry point for this project.
     Not here: feature list (→README.md), architecture decisions (→SPECS.md), setup steps (→SETUP.md).
     Keep it minimal — agents load this first; every extra line costs tokens on every task. -->

## Overview
<!-- Optional. 2–3 sentences: what this project is, its current state, key constraints.
     Skip if README.md already covers it well and this project has no agent-specific context to add. -->

<!-- ↑ Auto-managed by context_synchronizer.py. Do NOT edit the routing block manually.
     Add subdirectories via the filesystem; the sync script updates this table. -->

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`KNOWN-BUGS.md`](KNOWN-BUGS.md) | — | — | [Project Name] — Known Bugs |
| [`README.md`](README.md) | — | — | [Project Name] |
| [`ROADMAP.md`](ROADMAP.md) | — | — | [Project Name] — Roadmap |
| [`SETUP.md`](SETUP.md) | — | — | [Project Name] — Dev Setup |
| [`SPECS.md`](SPECS.md) | — | — | [Project Name] — Specs |
| [`module.SPEC.md`](module.SPEC.md) | — | — | SPEC: [module name] |
<!-- routing:end -->
