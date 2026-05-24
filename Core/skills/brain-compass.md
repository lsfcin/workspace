Run a compass review of Brain: surface what has good wind, update diagnostics, write ease-starts for stalled goals.

Arguments: $ARGUMENTS

## Protocol

Read: `Brain/GOALS.md` + all files in `Brain/goals/` (skip ARCHETYPE.md).
Run: `git log --oneline --since="14 days ago" -- Brain/goals/`

### Steps

1. Parse `anchor` field in each goal file — compute countdown to today
2. Cross-reference prescribed priority (signals: impact × engagement) vs actual git touches
3. Diagnose each goal — read `>**dynamics**` and `>**fears**` blocks:
   - gap type: fear/avoidance · drift/lost interest · deliberate park
4. Pareto: name the 2–3 goals with highest engagement × impact — these get 80% of energy
5. Urgent mode: anchor < 3 weeks → lead with that goal, offer ease-start immediately
6. Surface result as "what has good wind" — not "what you're behind on"

### Write back

Each goal file:
- `>**dynamics**` — update mode · motion · source
- `>**analysis**` — if stalled, refresh with science-backed strategies

`Brain/GOALS.md`:
- `>**pareto**` — 2–3 top goals with one-line rationale each
- `>**gap**` — gaps found, each with diagnosed type

Write today's date to `Brain/.log/compass-last.txt` (format: YYYY-MM-DD).

### Tone

"Here's what has good wind" — not "here's what you're behind on."
End with one question that opens the conversation.
