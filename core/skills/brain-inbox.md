---
name: brain-inbox
description: >
  Triage brain/INBOX.md — route each entry to a goal file, TODO list, writing draft, or delete.
---

Triage brain/INBOX.md — route each entry to a goal file, TODO list, writing draft, or delete.

Arguments: $ARGUMENTS

## Routes

Every INBOX entry lands in exactly one place:

| route | destination |
|-------|-------------|
| **goal** | new goal file in `brain/goals/` or backlog item in existing goal |
| **task** | `brain/TODO.md` at the right timeframe (today / week / month / backlog) |
| **draft** | new file in `branches/writing/drafts/[slug].md` |
| **delete** | gone |

Lucas may preemptively signal the route in the INBOX entry:
- `goal` — new or existing goal
- `task: today` / `task: week` / `task: month` / `task: backlog` — TODO.md
- `draft` — writing draft
- no signal → you decide based on content

## Protocol

Read `brain/INBOX.md`. If empty, say so and stop.

For each entry:
1. Detect signal if present; otherwise infer intent from content
2. Propose route:
   - **goal (new)** → suggest `# [ area | subarea | horizon ] title` + first backlog item + ease-start
   - **goal (existing)** → name the goal file and the exact backlog line to append
   - **task** → state timeframe and the exact line to add to TODO.md
   - **draft** → propose filename slug and one-line description of the draft
   - **delete** → one-line reason
3. Present all proposed routes first. Wait for confirmation. Act only after Lucas confirms.

## Timeframe judgment (when Lucas doesn't specify)

- **today** — urgent, hard deadline within days, or explicitly now
- **week** — near-term action with no hard deadline
- **month** — important but not pressing
- **backlog** — valid someday, no urgency

## After confirmation

- Write new goal files or append to confirmed backlogs
- Add task lines to the correct timeframe section in `brain/TODO.md`
- Create draft files in `branches/writing/drafts/[slug].md` with a title and blank body
- Clear confirmed entries from `brain/INBOX.md` — leave unconfirmed entries untouched
