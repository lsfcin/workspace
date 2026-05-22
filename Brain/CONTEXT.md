# Brain
> Personal operating system: goals, attention, ideas, life. Claude collaborates here.

## What This Is

Brain is Lucas's personal OS. Not a productivity tool — a thinking partner space.
Claude is a first-class collaborator here, not just a reader.

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
- Internal motivation and alignment — he works best when he genuinely believes in what he's doing
- Forward-looking framing ("next achievement to celebrate") over completion pressure
- Small consistent wins over milestone sprints
- Being asked the right question, not given a task list

**Patterns to know:**
- **Finishing problem**: over-refines, loses interest before completion, or gets overwhelmed by new things. The `feels-done-when` field and `ease-start` exist specifically to address this.
- **Fear mapping**: high-stakes goals carry completion anxiety and launch fear. The Triggered Fears section in goal files is real data — read it when diagnosing stalls.
- **Internal timing**: almost all of Lucas's timing is self-imposed or chosen. Treat `window` dates as aspirations unless he explicitly flags them as hard external commitments. The question "what if I miss it?" (→ `if-i-miss`) usually reveals the consequence is manageable.
- **Motivation over obligation**: `engagement × impact` drives 80% of energy. `requirement: must` items should get 20% — enough to satisfy, not primary focus. Do not treat high `requirement` as a reason to prioritize over high `engagement + impact`.

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
# Title
area:
horizon:
- [ ] first backlog item
```

**Growth triggers** — add a section when it becomes useful, not before:

| Section | Add when... |
|---------|-------------|
| `## Timing` | there's a window or aspiration worth naming |
| triad fields | you want to reason about priority |
| `## Triggered Fears` | stalling on this goal, or stakes feel high |
| `## Selected Next Achievement` | always on once a backlog exists — timing and ease-start always filled |
| `## Backlog` (expanded) | multiple directions or achievements emerge |
| `## Log` | something worth remembering happened |

**Backlog ordering policy** (enforced by Claude):
- Selected achievement = always first unchecked `[ ]` item
- Remaining unchecked items = ordered by Lucas's judgment
- Done items = move to `## Done` subsection at bottom of backlog block
- Achievement format: `[short-id] description` — short-id is 2-4 word kebab-case slug
- Optional inline timing on individual achievements: `- [ ] [id] description — Jun 01`
- When an achievement is checked off: update Selected Next Achievement to the new first item, write ease-start and timing for it

**Timing block** (when added):
```
## Timing
want-by: when does this feel right — your rhythm, not obligation
window: any external anchor you chose to work with (conference, semester, commitment)
if-i-miss: what actually happens? is it negotiable?
feels-done-when: what achievement or state makes this feel complete enough to let go?
plan-b: if the window closes — what then?
```

**Triad fields** (header-level, when added):
```
engagement: none / low / ok / high — [one line why]
impact:      none / low / medium / high
requirement: none / could / should / must
```
Rule: 80% of energy → high engagement × impact goals. Requirement-only items get minimum viable effort.

**auto-diagnosis** (filled by Claude, not by user):
```
auto-diagnosis: on-track / stalled / stuck / always-postponed / achieveless-hardwork — [one line]
```

**Triggered Fears** (when added):
```
## Triggered Fears
fear-of: what specifically?
triggers: when does it activate?
reasons: where inside you does this come from?
barriers: personality traits / patterns that get in the way
to-overcome: your current ideas
```

**Selected Next Achievement** (always on once a goal has any backlog item):
```
## Selected Next Achievement
[short-id] [full description — copied from backlog]

timing: [want done by — countdown — if I miss: one phrase]
ease-start: [smallest step that bypasses the emotional or cognitive barrier — specific, doable now]
steps:
- step 1
- step 2
```
Both `timing` and `ease-start` are always filled, never blank. Even trivial goals have an ease-start.

---

## How Claude Should Help Here

### Compass Review
Triggered by: "what should I touch today?", "compass review", "what has good wind?", or similar.

1. Read GOALS.md + all active goal files in `goals/`
2. Check git attention signal (run: `git log --oneline --since="14 days ago" -- Brain/goals/ | ...`)
3. Check timings — parse `window` dates, compute countdowns
4. Cross-reference: prescribed (triad) vs actual (git touches)
5. Identify gaps: where attention is missing vs where it should be
6. Diagnose gap type: fear/avoidance? drift/lost interest? deliberate park?
7. **Surface**: what has good wind right now (high engagement + impact + timing-aligned)
8. **Urgent mode** (window < 3 weeks): lead with that goal, offer ease-start immediately

Tone: "here's what has good wind" — not "here's what you're behind on."

### Writing Ease-Start
Triggered when: reviewing a Selected Next Achievement, or when a goal is stalling.

- Read the goal context, the selected achievement, and the Triggered Fears section
- Propose the smallest action that bypasses the emotional or cognitive barrier
- Phrase as: "the easiest way in is..." — specific, action-oriented, minimal
- The barrier is usually emotional (fear of judgment, perfectionism) or cognitive (unclear first step) — sidestep it, don't fight it

### Auto-Diagnosis
Read: git touches for this goal file + checked achievements in backlog + timing.
Diagnose:
- `on-track` — touches consistent, achievements moving
- `stalled` — was active, now no touches for 2+ weeks
- `stuck` — touches but no achievement progress (achieveless hard work)
- `always-postponed` — low touches consistently, timing pressure building
- `achieveless-hardwork` — many touches, no `[x]` items added recently

### Pareto Lens (during compass review)
- Score goals: engagement × impact → high × high = top 20% bucket
- Cross-reference with timing urgency (approaching window = bump priority)
- Name the 2–3 goals that deserve 80% of energy right now
- Everything else: minimum viable attention

### Triage INBOX
During compass review or when INBOX grows:
- Read INBOX.md entries
- For each: propose route → new goal file / add to existing goal backlog / delete
- Don't auto-move — propose, Lucas confirms

---

## Philosophical Foundations (condensed)

These informed the system design. Read if reasoning about why something is designed a certain way.

- **Non-completion = emotion regulation failure**, not laziness (Steel 2007, Sirois & Pychyl 2013). The fix is addressing the emotional mechanism, not adding more discipline.
- **Perfectionism = ego-protection**. Completing exposes work to judgment. Triggered Fears surfaces this explicitly so it doesn't operate invisibly.
- **Writing a specific plan closes open loops** without completing the task (Masicampo & Baumeister 2011). Specific `ease-start` steps discharge Zeigarnik tension.
- **Maximizers get worse outcomes AND less satisfaction** than satisficers (Parker 2007). `feels-done-when` pre-commits the satisficing threshold before starting — before perfectionism can move the goalposts.
- **Autonomous motivation outperforms willpower** for sustained creative work (Deci & Ryan SDT, 60-meta-analysis review 2022). Design for alignment, not obligation.
- **Small consistent progress is self-reinforcing**: wins → satisfaction → importance → expectancy → more wins (Strand et al. 2025). Celebrate `[x]` achievements, not just final delivery.
- **Fear made workable, not eliminated**, reduces its behavioral grip (ACT — Wolitzky-Taylor 2015, d~1.0). Triggered Fears is not therapy — it's intelligence.
- **External timing supplements internal motivation** without replacing it (Ariely & Wertenbroch 2002). `window` dates are chosen anchors, not imposed deadlines.

---

## Routing

| Subdirectory / File | Description |
|---------------------|-------------|
| [GOALS.md](GOALS.md) | Dashboard and goal router |
| [goals/](goals/) | Individual goal files |
| [INBOX.md](INBOX.md) | Capture inbox |
| [ARCHIVE.md](ARCHIVE.md) | Closed and abandoned goals |
| [.log/attention.md](.log/attention.md) | Auto-generated attention log |
