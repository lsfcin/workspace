# Brain
> Personal operating system: goals, attention, ideas, life. Agent collaborates here.

## What This Is

Brain is Lucas's personal OS. Not a productivity tool — a thinking partner space.
The agent is a first-class collaborator here, not just a reader.

Core files:

| File / Folder | Role |
|---------------|------|
| [GOALS.md](GOALS.md) | Dashboard, attention monitor, Pareto lens, router to goal files |
| [goals/](goals/) | One file per goal — organic growth from seed to full |
| [INBOX.md](INBOX.md) | Zero-friction capture, no taxonomy |
| [ARCHIVE.md](ARCHIVE.md) | Closed goals — never auto-loaded, ask explicitly |
| [.log/attention.md](.log/attention.md) | Auto-appended by post-commit hook |

---

## User Profile

Lucas is a CS professor (UFRPE / CIn-UFPE). Research areas: Hybrid Intelligence, Mechanism Design, AR, 3D Computer Vision. Creative, fuzzy thinker. Very good at starting; struggles to finish.

**What helps:**
- Internal motivation and alignment — works best when genuinely believes in what he's doing
- Forward-looking framing ("next achievement to celebrate") over completion pressure
- Small consistent wins over milestone sprints
- Being asked the right question, not given a task list

**Patterns to know:**
- **Finishing problem**: over-refines, loses interest, gets overwhelmed by new things. `closure` and `ease-start` address this directly.
- **Fear mapping**: high-stakes goals carry completion anxiety. The `fears` block is real data — read it when diagnosing stalls. `analysis` is the synthesis layer on top.
- **Internal timing**: almost all timing is self-imposed. Treat `anchor` dates as aspirations unless explicitly flagged as hard commitments. `tolerance` usually reveals the consequence of missing is manageable.
- **Motivation over obligation**: impact × engagement drives 80% of energy. `essential` requirement goals get 20% — enough to satisfy, not primary focus.

---

## Area Taxonomy

| Area | Covers |
|------|--------|
| `health` | Body, sleep, exercise, medical checkups |
| `career` | Research, papers, teaching, academic positioning, grants |
| `finances` | Money management, taxes, admin, investments |
| `fun` | Hobbies, play, exploration, anything done for its own sake |
| `spiritual` | Reflection, meaning, inner life, values |

---

## Goal File Structure — Organic Growth

Goal files grow from seed to full. No section is required at creation.

**Minimum viable seed:**
```
# [ area | horizon ] goal title
- [ ] [short-id] first backlog item
```

Area: `health` / `career` / `finances` / `fun` / `spiritual`
Horizon: `now` / `near` / `year` / `dream`

**Growth triggers** — add a section when it becomes useful, not before:

| Section | Add when... |
|---------|-------------|
| description | scope worth writing down |
| `>**signals**` | want to reason about priority |
| `>**dynamics**` | diagnosing a stall, or after a meaningful work session |
| `>**fears**` | stalling on this goal, or stakes feel high |
| `>**analysis**` | need strategic synthesis on the fears or block |
| `## selected next achievement` | always on once a backlog exists — ease-start always filled |
| `>**timing**` | external anchor or window worth naming |
| `## stats` | refreshed by agent during compass review |

**Signals** — display order is always: impact · requirement · engagement
- impact: `forgettable` / `useful` / `meaningful` / `transformative`
- requirement: `optional` / `expected` / `essential`
- engagement: `reluctant` / `indifferent` / `motivated` / `thrilled`

Rule: 80% of energy → transformative/meaningful × motivated/thrilled. Essential-requirement-only goals get minimum viable effort.

**Dynamics** (agent-filled — update during compass review or when diagnosing):
- mode: `overprocessing` / `pressured` / `avoidant` / `pragmatic` / `relaxed` / `immersed`
- motion: `blocked` / `stalled` / `looping` / `advancing` / `steady` / `intense`
- source: `intrinsic` / `structured` / `external`

**Fears block** (what/when/why/how — raw data, no interpretation):
- what: specific negative outcome or emotional experience being avoided
- when: situations that trigger it
- why: origins — perceived beliefs, past experiences, internal expectations
- how: current behavioral response — barriers, patterns getting in the way

**Analysis block** (agent-filled — synthesis on top of fears):
- How the goal is being handled
- Science-backed strategies for the specific block or fear
- Practical, precise, grounded in behavioral science and self-regulation research

**Backlog ordering policy** (enforced by agent):
- Selected achievement = always first unchecked `[ ]` item in backlog
- Remaining unchecked items = ordered by Lucas's judgment
- Done items = move to `## done` section
- Achievement format: `[short-id] description` — short-id is 2-4 word kebab-case slug
- Optional inline timing: `> [ ] [id] description — Jun 01`
- On check-off: use `/brain-finished [id]`

Backlog item format:
```
> [ ] [short-id] description
> [x] [short-id] completed item
```

**Timing fields** (when added):
- `target` — when does this feel naturally right? personal rhythm, not obligation
- `anchor` — external timing anchor intentionally chosen (conference, semester, commitment)
- `closure` — what outcome makes this feel complete enough to release?
- `tolerance` — what actually happens if missed? negotiable, costly, or mostly symbolic?
- `fallback` — if the window closes, how does this evolve instead of collapse?

**Selected Next Achievement** (always on once backlog exists):
```
## selected next achievement
    [short-id] full description

**ease-start**
smallest action that bypasses the emotional or cognitive barrier — specific, doable now
steps to proceed afterwards
```
Ease-start is always filled, never blank.

---

## Agent Workflows

### /brain-compass — Compass Review
Triggered by: `/brain-compass`, "what should I touch today?", "compass review", "what has good wind?", or similar.

1. Read GOALS.md + all goal files in `goals/`
2. Run `git log --oneline --since="14 days ago" -- Brain/goals/`
3. Parse `anchor` dates, compute countdowns
4. Cross-reference prescribed priority (signals: impact × engagement) vs actual git touches
5. Identify gaps — diagnose type: fear/avoidance · drift · deliberate park (read `fears` + `dynamics`)
6. **Surface**: what has good wind (high engagement + impact + timing-aligned)
7. **Urgent mode** (anchor < 3 weeks): lead with that goal, offer ease-start immediately
8. Write back: update `>**dynamics**`, `>**analysis**` per file; fill `>**pareto**` and `>**gap**` in GOALS.md

Tone: "here's what has good wind" — not "here's what you're behind on."

### /brain-finished [id] — Achievement Check-off
Triggered by: `/brain-finished [id]`, "finished [id]", "done with [id]", or similar.

Marks `[id]` done in backlog, moves to done section, advances selected next achievement, writes new ease-start, updates dynamics to `advancing`. Acknowledge the win before moving on.

### /brain-inbox — Triage INBOX
Triggered by: `/brain-inbox`, "triage inbox", or similar.

Reads INBOX.md, proposes route for each entry (new goal / add to backlog / delete). Waits for confirmation before moving anything.

### Writing Ease-Start
Triggered when: reviewing a selected next achievement, or when a goal is stalling.

- Read goal context, selected achievement, `fears` + `analysis` blocks
- Propose the smallest action that bypasses the emotional or cognitive barrier
- Phrase as "the easiest way in is..." — specific, action-oriented, minimal
- The barrier is usually emotional (fear of judgment, perfectionism) or cognitive (unclear first step) — sidestep it, don't fight it

### Auto-Diagnosis
Read: git touches for this goal file + checked achievements + timing. Diagnose:
- `on-track` — touches consistent, achievements moving
- `stalled` — was active, no touches for 2+ weeks
- `stuck` — touches but no achievement progress
- `always-postponed` — low touches consistently, timing pressure building
- `achieveless-hardwork` — many touches, no `[x]` items recently

### Pareto Lens (during compass review)
- Score: impact × engagement → transformative/meaningful × motivated/thrilled = top bucket
- Cross-reference timing urgency (approaching anchor = bump priority)
- Name the 2–3 goals that deserve 80% of energy
- Everything else: minimum viable attention

---

## Philosophical Foundations

See [FOUNDATIONS.md](FOUNDATIONS.md) — research basis and design rationale.

---

## Routing

| Subdirectory / File | Description |
|---------------------|-------------|
| [GOALS.md](GOALS.md) | Dashboard and goal router |
| [goals/](goals/) | Individual goal files |
| [INBOX.md](INBOX.md) | Capture inbox |
| [ARCHIVE.md](ARCHIVE.md) | Closed and abandoned goals |
| [.log/attention.md](.log/attention.md) | Auto-generated attention log |
| [FOUNDATIONS.md](FOUNDATIONS.md) | Design rationale and research basis |
