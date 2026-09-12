# Brain
> Personal OS: goals, attention, ideas, life. Agent collaborates here.

Not a productivity tool — a thinking-partner space, where the agent is a first-class collaborator
rather than a reader.

**Capture is free, structure is earned.** A thought lands in `INBOX.md` with no taxonomy and no
formatting, and `/inbox` routes it to a goal, a task, a reference — or deletes it. Nothing else here
has to be tidy at write time. The routing table below says what each file is.

Goal file format, the five areas, section specs, signals/dynamics/timing fields, and the design
rationale: [SPECS.md](SPECS.md).

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`attachments/`](attachments/CONTEXT.md) | Files captured from Gmail and Telegram, filed by month — the raw material, not a ledger. |
| [`drafts/`](drafts/CONTEXT.md) | Work in progress that is not yet anywhere else: proposals being compared, and reports being read. |
| [`goals/`](goals/CONTEXT.md) | One file per goal — organic growth from seed to full. Dashboard + router: [GOALS.md](goals/../GOALS.md). |
| [`memory/`](memory/CONTEXT.md) | What the agent learned across sessions and nothing else records. Harness-written, workspace-owned. |

| File | Description |
|------|-------------|
| [`GOALS.md`](GOALS.md) | Dashboard, attention monitor, Pareto lens, and the router to every goal file. |
| [`INBOX.md`](INBOX.md) | zero friction. thoughts. no taxonomy. no formating. handle duplications. triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted. signal the route preemptively (optional — agent infers if omitted): `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete` |
| [`SPECS.md`](SPECS.md) | Goal file format, section growth triggers, signals, dynamics, timing, and backlog conventions. |
| [`USER.md`](USER.md) | Lucas — read before any Brain task. |
<!-- routing:end -->
