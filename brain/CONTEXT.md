# Brain
> Personal OS: goals, attention, ideas, life. Agent collaborates here.

## What This Is

Brain = Lucas's personal OS. Not productivity tool — thinking partner space.
Agent is first-class collaborator, not just reader.

**Capture is free, structure is earned.** A thought lands in `INBOX.md` with no taxonomy and no
formatting, and `/inbox` is what routes it to a goal, a task, a reference — or deletes it. Nothing
else here has to be tidy at write time. The routing table below says what each file is.

## Area Taxonomy

| Area | Covers |
|------|--------|
| `health` | Body, sleep, exercise, medical checkups |
| `career` | Research, papers, teaching, academic positioning, grants |
| `finances` | Money management, taxes, admin, investments |
| `fun` | Hobbies, play, exploration, anything done for its own sake |
| `spiritual` | Reflection, meaning, inner life, values |

## Skills

- `/compass` — gentle strategic review: good wind, reorder by motivation, negotiate timing, ditch freely, close wins,
  next easy start
- `/inbox` — triage INBOX.md entries

Goal file format, section specs, signals/dynamics/timing fields → [SPECS.md](SPECS.md).
Design rationale → [SPECS.md](SPECS.md) § Rationale.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`attachments/`](attachments/CONTEXT.md) | Files captured from Gmail and Telegram, filed by month — the raw material, not a ledger. |
| [`goals/`](goals/CONTEXT.md) | One file per goal — organic growth from seed to full. Dashboard + router: [GOALS.md](goals/../GOALS.md). |
| [`memory/`](memory/CONTEXT.md) | What the agent learned across sessions and nothing else records. Harness-written, workspace-owned. |

| File | Description |
|------|-------------|
| [`GOALS.md`](GOALS.md) | Dashboard, attention monitor, Pareto lens, and the router to every goal file. |
| [`INBOX.md`](INBOX.md) | zero friction. thoughts. no taxonomy. no formating. handle duplications. triage with `/inbox`: each entry routed to a goal, task, ref, project doc, draft — or deleted. signal the route preemptively (optional — agent infers if omitted): `goal` · `task: today`/`week`/`month`/`backlog` · `ref` · `proj: <name>` · `draft` · `delete` |
| [`SPECS.md`](SPECS.md) | Goal file format, section growth triggers, signals, dynamics, timing, and backlog conventions. |
| [`USER.md`](USER.md) | Lucas — read before any Brain task. |
<!-- routing:end -->
