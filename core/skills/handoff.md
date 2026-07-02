---
name: handoff
description: >
  End current session cleanly: archive completed work (moves done ROADMAP items and fixed bugs to HISTORY.md), route session knowledge to durable files, then produce a copy-pasteable resume prompt for the next session.
  Invoke with /handoff [focus for next session].
---

# Handoff skill

Arguments: $ARGUMENTS

---

## Execution protocol

Execute all phases in order. Write directly to files. Ask only if conflict or destructive ambiguity arises.

---

## Phase 1 — Discover project files

```bash
find . -maxdepth 3 \( \
  -name "ROADMAP.md" -o -name "KNOWN-BUGS.md" -o -name "HISTORY.md" \
  -o -name "CHANGELOG.md" -o -name "TODO.md" -o -name "AGENTS.md" \
  -o -name "TASKS.md" -o -name "BACKLOG.md" -o -name "INPUT.md" \
\) 2>/dev/null | sort

git log --oneline -10 2>/dev/null || echo "no git"
git status --short 2>/dev/null || echo "no git status"
```

Read every file found above **except HISTORY.md** before proceeding.

### Verification gate

If the project's `package.json` declares `verify:full`, run it now (`npm run verify:full`)
and record the result (green / red + failing specs) in the resume prompt. A session must
not hand off claiming working state without this proof. `verify:fast`-only projects: run
that instead. No contract: note "no verification contract" in the resume prompt.

---

## Phase 2 — Archive completed work

### ROADMAP cleanup

If `ROADMAP.md` exists:

1. Identify completed items (`- [x]`, "done", "shipped", "merged", "✅").
2. Append to `HISTORY.md` under `## Completed — YYYY-MM-DD`.
3. Remove completed items from `ROADMAP.md`.
4. Nothing completed → skip, do not modify.

### KNOWN-BUGS cleanup

If `KNOWN-BUGS.md` exists:

1. Identify resolved items (`- [x]`, "fixed", "resolved", "closed").
2. Append to `HISTORY.md` under `## Resolved Bugs — YYYY-MM-DD`.
3. Remove resolved items from `KNOWN-BUGS.md`.
4. Nothing resolved → skip.

### HISTORY.md

Create only if content to add:
```markdown
# History

Archive of completed work and resolved issues.
```

---

## Phase 3 — Route session knowledge to durable files

Identify all knowledge from session. Route each piece using table below. Write directly. Conflict with existing content → ask before writing.

### Routing table

| Knowledge type | Target |
|---|---|
| Non-obvious design decision + rationale | `SPECS.md` → Architecture Decisions |
| Discovered convention / coding rule | `SPECS.md` → Conventions |
| Bug found, not fixed | `KNOWN-BUGS.md` |
| New technical work item (project has `ROADMAP.md`) | `ROADMAP.md` |
| Personal / admin / life / teaching task — or project task with hard deadline | `brain/TODO.md` (right horizon: today / week / month / backlog) |
| Insight about specific life or career goal | `brain/goals/[goal].md` (achievement, backlog item, or obstacle) |
| Skill workflow improvement | Skill file directly |
| Workspace-wide rule across all projects | `AGENTS.md` |
| Critical quick-reference fact or constant needed at session start | `CONTEXT.md` — see exclusions |
| Doesn't fit cleanly | `brain/INBOX.md` — triage later with `/brain-inbox` |

### TODO vs ROADMAP

**ROADMAP**: project has `ROADMAP.md` AND item is technical milestone with agent-ready context.

**TODO**: personal / admin / life / teaching task; OR project has no `ROADMAP.md`; OR project task with hard external deadline needing time-horizon tracking.

Unclear → INBOX.

### CONTEXT.md — explicit exclusions

- Routing block changes → ignore. Hooks auto-sync on edit/commit.
- Behavioral cues ("be careful with X", "prefer Y") → `SPECS.md` Conventions or `AGENTS.md`, not `CONTEXT.md`.
- Decisions + rationale → `SPECS.md` Architecture Decisions, not `CONTEXT.md`.

Write to `CONTEXT.md` only if: critical constant, invariant, or quick-start command needed at next session start — and doesn't fit `SPECS.md`.

### Memory

Do not write to memory unless knowledge is homeless across all files above. Filesystem is source of truth.

---

## Phase 4 — Output resume prompt

Captures only what is **not already in project files**. Do not repeat content written in Phase 3 — reference the file instead.

Print block between `---` markers:

---

```
## Session Resume — [PROJECT] — [DATE]

### Start
Read `AGENTS.md`, then load relevant `CONTEXT.md` for active subtree.
[Files written/modified in Phase 3 relevant to next session:]
- `path/to/file` — one-line reason it matters

### Git state
[Last 5 log lines + uncommitted changes from `git status`.]

### What was worked on
Specific tasks, not project overview. Last 30 minutes first.

### Open questions / unresolved threads
Discussed but not resolved. Include dead ends and what was tried.
[If none: "none."]

### Next action
[If $ARGUMENTS: use as directive. Otherwise: single most strategic next step from ROADMAP + current state.]
```

---

After printing, say:

> Handoff complete. Copy block above, paste as first message in new session.
> [If HISTORY.md updated]: HISTORY.md updated with [N] items.
> [If files trimmed]: ROADMAP.md / KNOWN-BUGS.md trimmed.
> [List every file written in Phase 3, one line each.]
> Start new session with `/clear` or open fresh Claude Code window.
