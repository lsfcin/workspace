# Brain — Specs
> Goal file format, section growth triggers, signals, dynamics, timing, and backlog conventions.

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

## Signals

Display order always: impact · requirement · engagement

- **impact**: `forgettable` / `useful` / `meaningful` / `transformative`
- **requirement**: `optional` / `expected` / `essential`
- **engagement**: `reluctant` / `indifferent` / `motivated` / `thrilled`

Rule: 80% energy → transformative/meaningful × motivated/thrilled. Essential-only goals get minimum viable effort.

## Dynamics (agent-filled)

Update during compass review or when diagnosing stall.

- **mode**: `overprocessing` / `pressured` / `avoidant` / `pragmatic` / `relaxed` / `immersed`
- **motion**: `blocked` / `stalled` / `looping` / `advancing` / `steady` / `intense`
- **source**: `intrinsic` / `structured` / `external`

## Fears Block

Raw data, no interpretation. Four fields:
- **what**: specific negative outcome or emotional experience avoided
- **when**: situations that trigger it
- **why**: origins — perceived beliefs, past experiences, internal expectations
- **how**: current behavioral response — barriers, patterns in the way

## Analysis Block (agent-filled)

Synthesis on top of fears:
- How the goal is being handled
- Science-backed strategies for the specific block or fear
- Practical, precise, grounded in behavioral science and self-regulation research

## Backlog Ordering Policy

- Selected achievement = always first unchecked `[ ]` item in backlog
- Remaining unchecked = ordered by Lucas's judgment
- Done items = move to `## done` section
- Achievement format: `[short-id] description` — short-id is 2–4 word kebab-case slug
- Optional inline timing: `> [ ] [id] description — Jun 01`
- On check-off: use `/brain-finished [id]`

**Backlog item format:**
```
> [ ] [short-id] description
> [x] [short-id] completed item
```

## Timing Fields

| Field | Meaning |
|-------|---------|
| `target` | when does this feel naturally right? personal rhythm, not obligation |
| `anchor` | external timing anchor intentionally chosen (conference, semester, commitment) |
| `closure` | what outcome makes this feel complete enough to release? |
| `tolerance` | what actually happens if missed? negotiable, costly, or mostly symbolic? |
| `fallback` | if window closes, how does this evolve instead of collapse? |

## Selected Next Achievement Block

```
## selected next achievement
    [short-id] full description

**ease-start**
smallest action that bypasses the emotional or cognitive barrier — specific, doable now
steps to proceed afterwards
```

Ease-start always filled, never blank.
