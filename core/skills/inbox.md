---
name: inbox
description: >
  Triage brain/INBOX.md — route each entry to a goal, task, reference, project doc, writing draft, or delete. Cross-domain front door: reaches into code ROADMAP/KNOWN-BUGS and domain refs/, not just brain/.
---

Triage brain/INBOX.md — route each entry to its durable home. INBOX is zero-friction capture; taxonomy happens **here at triage**, never at capture.

Arguments: $ARGUMENTS

## Guardrail — land in on-demand docs, never CONTEXT.md

Every route targets a doc that loads **only when needed**: `ROADMAP.md`, `KNOWN-BUGS.md`, `refs/REFS.md`, goal files, `TODO.md`.

**NEVER route an entry into a `CONTEXT.md`.** CONTEXT.md loads every session for its whole subtree — every line there costs tokens on every task. Ideas, bugs, and references go to on-demand docs. This is the rule that keeps capture cheap without flooding always-loaded context.

## Routes

Every INBOX entry lands in exactly one place:

| route | destination | signal |
|-------|-------------|--------|
| **goal** | new goal file in `brain/goals/` or backlog item in an existing goal | `goal` |
| **task** | `brain/TODO.md` at the right timeframe (today / week / month / backlog) | `task: <when>` |
| **ref** | domain `refs/REFS.md` — one tier-1 line (routing table + convention below) | `ref` |
| **project** | `code/<proj>/ROADMAP.md` `## Backlog` (idea) or `KNOWN-BUGS.md` (bug) | `proj: <name>` |
| **draft** | new file in `branches/writing/drafts/[slug].md` | `draft` |
| **delete** | gone | `delete` |

Lucas may preemptively signal the route in the entry (optional — infer from content if omitted).

## Reference routing (route-by-domain)

A `ref` goes to the **nearest owning subtree's** `refs/REFS.md` — never a central brain file, never CONTEXT.md.

| ref kind | home |
|----------|------|
| isoroll module tech (perfect-vision, elevated-vision, iso-8-view) | `code/isoroll-module/refs/REFS.md` |
| isoroll asset-gen / 3D-gen models (hunyuan3d, HunyuanWorld) | `code/isoroll-content/refs/REFS.md` |
| dobra research (context-folding, graphs+agents, model leaks) | `code/dobra/refs/REFS.md` |
| apptime design | `code/apptime/refs/REFS.md` |
| research paper for a specific manuscript | that paper's `academy/papers/<paper>/refs/` (promote to yaml) |
| general research paper (no target manuscript) | `academy/refs/REFS.md` |
| AI / agent / model tooling to evaluate | `core/WATCHLIST.md` |
| no clear owner yet | `core/WATCHLIST.md` (if tooling) — else ask Lucas |

### refs/ two-tier convention

- **Tier 1 — capture (default, zero-friction):** append one line to `refs/REFS.md`:
  `- [what it is](url) — one-phrase why it matters`. This is **all** `/inbox` ever does for a ref.
- **Tier 2 — promote (manual, deliberate):** when a ref earns real study or citation, a human promotes it to `refs/<slug>.yaml` (schema = `academy/papers/*/refs/CONTEXT.md`). Triage NEVER auto-creates a yaml.
- **Lazy creation:** the first ref routed to a domain births `refs/REFS.md` (and a minimal `refs/CONTEXT.md`: line 2 = `> Captured references for <domain>.`). Do NOT pre-seed empty `refs/` folders across projects.

## project route — writing into code repos

- **idea** → append to `code/<proj>/ROADMAP.md` under `## Backlog` (or the project's backlog section), phrased agent-ready.
- **bug** → append to `code/<proj>/KNOWN-BUGS.md`.
- Code projects are their **own git repos**. Write the file, leave it **staged/uncommitted** — do NOT commit. Report which repo(s) were touched so Lucas commits deliberately.
- Never write project ideas into `code/<proj>/CONTEXT.md`.

## Protocol

Read `brain/INBOX.md`. If empty, say so and stop.

For each entry:
1. Detect signal if present; otherwise infer intent from content.
2. Propose route:
   - **goal (new)** → suggest `# [ area | subarea | horizon ] title` + first backlog item + ease-start
   - **goal (existing)** → name the goal file and the exact backlog line to append
   - **task** → state timeframe and the exact line to add to TODO.md
   - **ref** → name the target `refs/REFS.md` and the exact tier-1 line
   - **project** → name the target file (ROADMAP / KNOWN-BUGS), the exact line, and the repo
   - **draft** → propose filename slug and one-line description of the draft
   - **delete** → one-line reason
3. Present all proposed routes first. Wait for confirmation. Act only after Lucas confirms.

## Timeframe judgment (task, when unspecified)

- **today** — urgent, hard deadline within days, or explicitly now
- **week** — near-term action with no hard deadline
- **month** — important but not pressing
- **backlog** — valid someday, no urgency

## After confirmation

- Write new goal files or append to confirmed backlogs
- Add task lines to the correct timeframe section in `brain/TODO.md`
- Append ref lines to the domain `refs/REFS.md` (create `refs/REFS.md` + `refs/CONTEXT.md` if absent)
- Append project ideas/bugs to `code/<proj>/ROADMAP.md` / `KNOWN-BUGS.md` — leave **staged**, report repos
- Create draft files in `branches/writing/drafts/[slug].md` with a title and blank body
- Clear confirmed entries from `brain/INBOX.md` — leave unconfirmed entries untouched
