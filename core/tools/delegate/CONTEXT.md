# delegate
> Hand a task to another vendor's model through one contract: `return: answer` reads, `return: artifact` writes in an isolated copy held to checks. Leaf: `ask`; routes from `core/workers.txt`.

A task: `core/run tools/delegate/ask <contract.md>` — a YAML frontmatter (`goal, work, role, read_paths, write_paths, checks, attempt, return`), then `## Context`. An answer: the cut answer prints, the whole one lands in `outputs/delegate/` or `--out`. An artifact: the worker edits a copy (`sandbox.py`), the wrapper runs `checks` there, and only `write_paths` come back; the report — paths, hashes, checks, route — is all the orchestrator reads (`produce.py`), and each run's size lands in `core/state/delegations.tsv`. An outside verdict: `core/run tools/delegate/ask --out outputs/<topic>-panel.md prompt.md`. The calls and their traps: [`../../agents/SPECS.md`](../../agents/SPECS.md).

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`ask`](ask) | — | — | hand a task to another vendor's model, falling to the next model when one gives no answer |
| [`delegation.py`](delegation.py) | [`delegation.pyi`](delegation.pyi) | `is_contract`, `sections`, `parse`, `validate`, `bundle` | delegation.py — the delegation contract as text: read one, refuse what this version cannot keep, build the worker's prompt from it, and read, flag and cut what came back. Pure: no call, no disk write. |
| [`produce.py`](produce.py) | [`produce.pyi`](produce.pyi) | `ladder`, `produced`, `report` | produce.py — the artifact mode: pick the route ladder, run each route in its own copy, hold it to the contract's checks, retry with the evidence, and hand the orchestrator a report instead of the files. |
| [`roles.txt`](roles.txt) | — | — | Every role a delegated worker can be given, and the pre-prompt that opens its prompt. Read by core/tools/delegate/ask. The pre-prompt is the stable head of every prompt, so a change here re-bills every provider's prefix cache once. A repeated failure becomes one line here only once it passes the logged cases (core/ROADMAP-workers.md § v2). role	pre |
| [`sandbox.py`](sandbox.py) | [`sandbox.pyi`](sandbox.pyi) | `make`, `changed`, `check`, `bring`, `drop` | sandbox.py — the isolated copy a writing worker runs in: make it, list what the worker changed, run the checks there, and bring back only what passed. |
<!-- routing:end -->
