# Brain
> Personal OS: goals, attention, ideas, life. Agent collaborates here.

## What This Is

Brain = Lucas's personal OS. Not productivity tool — thinking partner space.
Agent is first-class collaborator, not just reader.

Core files:

| File / Folder | Role |
|---------------|------|
| [GOALS.md](GOALS.md) | Dashboard, attention monitor, Pareto lens, router to goal files |
| [goals/](goals/) | One file per goal — organic growth from seed to full |
| [USER.md](USER.md) | User profile — identity, language, patterns, what helps |
| [INBOX.md](INBOX.md) | Zero-friction capture, no taxonomy |
| [ARCHIVE.md](ARCHIVE.md) | Closed goals — never auto-loaded, ask explicitly |
| [.log/done.md](.log/done.md) | Achieved items archived from goal files |

---

## User Profile

→ [USER.md](USER.md)

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

Goal files grow from seed to full. No section required at creation.

**Minimum viable seed:**
```
# [ area | horizon ] goal title
- [ ] [short-id] first backlog item
```

Area: `health` / `career` / `finances` / `fun` / `spiritual`
Horizon: `now` / `near` / `year` / `dream`

**Growth triggers** — add section when useful, not before:

| Section | Add when... |
|---------|-------------|
| description | scope worth writing down |
| `>**signals**` | want to reason about priority |
| `>**dynamics**` | diagnosing stall, or after meaningful work session |
| `>**fears**` | stalling on goal, or stakes feel high |
| `>**analysis**` | need strategic synthesis on fears or block |
| `## selected next achievement` | always on once backlog exists — ease-start always filled |
| `>**timing**` | external anchor or window worth naming |
| `## stats` | refreshed by agent during compass review |

**Signals** — display order always: impact · requirement · engagement
- impact: `forgettable` / `useful` / `meaningful` / `transformative`
- requirement: `optional` / `expected` / `essential`
- engagement: `reluctant` / `indifferent` / `motivated` / `thrilled`

Rule: 80% energy → transformative/meaningful × motivated/thrilled. Essential-only goals get minimum viable effort.

**Dynamics** (agent-filled — update during compass review or diagnosing):
- mode: `overprocessing` / `pressured` / `avoidant` / `pragmatic` / `relaxed` / `immersed`
- motion: `blocked` / `stalled` / `looping` / `advancing` / `steady` / `intense`
- source: `intrinsic` / `structured` / `external`

**Fears block** (what/when/why/how — raw data, no interpretation):
- what: specific negative outcome or emotional experience avoided
- when: situations that trigger it
- why: origins — perceived beliefs, past experiences, internal expectations
- how: current behavioral response — barriers, patterns in the way

**Analysis block** (agent-filled — synthesis on top of fears):
- How goal is being handled
- Science-backed strategies for specific block or fear
- Practical, precise, grounded in behavioral science and self-regulation research

**Backlog ordering policy** (enforced by agent):
- Selected achievement = always first unchecked `[ ]` item in backlog
- Remaining unchecked = ordered by Lucas's judgment
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
- `fallback` — if window closes, how does this evolve instead of collapse?

**Selected Next Achievement** (always on once backlog exists):
```
## selected next achievement
    [short-id] full description

**ease-start**
smallest action that bypasses the emotional or cognitive barrier — specific, doable now
steps to proceed afterwards
```
Ease-start always filled, never blank.

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

Mark `[id]` done in backlog, move to done section, advance selected next achievement, write new ease-start, update dynamics to `advancing`. Acknowledge win before moving on.

### /brain-inbox — Triage INBOX
Triggered by: `/brain-inbox`, "triage inbox", or similar.

Read INBOX.md, propose route per entry (new goal / add to backlog / delete). Wait for confirmation before moving anything.

### Writing Ease-Start
Triggered when: reviewing selected next achievement, or goal stalling.

- Read goal context, selected achievement, `fears` + `analysis` blocks
- Propose smallest action bypassing emotional or cognitive barrier
- Phrase as "easiest way in is..." — specific, action-oriented, minimal
- Barrier usually emotional (fear of judgment, perfectionism) or cognitive (unclear first step) — sidestep it, don't fight it

### Auto-Diagnosis
Read: git touches for goal file + checked achievements + timing. Diagnose:
- `on-track` — touches consistent, achievements moving
- `stalled` — was active, no touches 2+ weeks
- `stuck` — touches but no achievement progress
- `always-postponed` — low touches consistently, timing pressure building
- `achieveless-hardwork` — many touches, no `[x]` items recently

### Pareto Lens (during compass review)
- Score: impact × engagement → transformative/meaningful × motivated/thrilled = top bucket
- Cross-reference timing urgency (approaching anchor = bump priority)
- Name 2–3 goals deserving 80% of energy
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
| [.log/done.md](.log/done.md) | Achieved items archived from goal files |
| [FOUNDATIONS.md](FOUNDATIONS.md) | Design rationale and research basis |