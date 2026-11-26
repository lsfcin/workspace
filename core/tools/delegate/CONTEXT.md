# delegate
> Hand a task to another vendor's model through one contract, read-only for now. Leaf: `ask` (answer mode, an outside verdict included); the chain it walks is `core/workers.txt`.

A task: `core/run tools/delegate/ask <contract.md>` — a YAML frontmatter (`goal, work, role, read_paths, write_paths, checks, attempt, return`), then `## Context`; the cut answer prints, the whole one lands in `outputs/delegate/` or `--out`. An outside verdict: `core/run tools/delegate/ask --out outputs/<topic>-panel.md prompt.md`. The calls and their traps: [`../../agents/SPECS.md`](../../agents/SPECS.md).

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`ask`](ask) | — | — | hand a task to another vendor's model, falling to the next model when one gives no answer |
| [`delegation.py`](delegation.py) | [`delegation.pyi`](delegation.pyi) | `is_contract`, `sections`, `parse`, `validate`, `bundle` | delegation.py — the delegation contract as text: read one, refuse what v0 cannot keep, build the worker's prompt from it, and read, flag and cut what came back. Pure: no call, no disk write. |
| [`roles.txt`](roles.txt) | — | — | Every role a delegated worker can be given, and the pre-prompt that opens its prompt. Read by core/tools/delegate/ask. The pre-prompt is the stable head of every prompt, so a change here re-bills every provider's prefix cache once. A repeated failure becomes one line here only once it passes the logged cases (core/ROADMAP-workers.md § v2). role	pre |
<!-- routing:end -->
