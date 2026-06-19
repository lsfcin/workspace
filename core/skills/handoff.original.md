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

Execute all phases in order. Write directly to files. Ask only if a conflict or destructive ambiguity arises.

---

## Phase 1 — Discover project files

```bash
find . -maxdepth 3 \( \
  -name "ROADMAP.md" -o -name "KNOWN-BUGS.md" -o -name "HISTORY.md" \
  -o -name "CHANGELOG.md" -o -name "TODO.md" -o -name "WORKSPACE.md" \
  -o -name "TASKS.md" -o -name "BACKLOG.md" -o -name "INPUT.md" \
\) 2>/dev/null | sort

git log --oneline -10 2>/dev/null || echo "no git"
git status --short 2>/dev/null || echo "no git status"
```

Read every file found above **except HISTORY.md** before proceeding.

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

Identify all knowledge produced in this session. For each piece, route it to the right file using the table below and write it directly. If a conflict exists (e.g., contradicts existing content), ask before writing.

### Routing table

| Knowledge type | Target |
|---|---|
| Non-obvious design decision + rationale | `SPECS.md` → Architecture Decisions |
| Discovered convention / coding rule | `SPECS.md` → Conventions |
| Bug found, not fixed this session | `KNOWN-BUGS.md` |
| New technical work item for project with `ROADMAP.md` | `ROADMAP.md` |
| Personal / admin / life / teaching task — or time-sensitive project deadline | `brain/TODO.md` (correct horizon: today / week / month / backlog) |
| Insight about a specific life or career goal | `brain/goals/[goal].md` (achievement, backlog item, or obstacle) |
| Skill workflow improvement | Skill file directly |
| Workspace-wide rule applying across all projects | `WORKSPACE.md` |
| Critical quick-reference fact or constant needed at session start | `CONTEXT.md` — see exclusions below |
| Anything that doesn't fit cleanly | `brain/INBOX.md` — zero friction, triage later with `/brain-inbox` |

### TODO vs ROADMAP

Use **ROADMAP** when: project has `ROADMAP.md` AND item is a technical milestone with agent-ready context.

Use **TODO** when: personal / admin / life / teaching task; OR project has no `ROADMAP.md`; OR item is a project task with a hard external deadline that needs time-horizon tracking.

When unclear → INBOX.

### CONTEXT.md — explicit exclusions

- **Routing block changes** → ignore. Hooks auto-sync on edit/commit.
- **Behavioral cues** ("be careful with X", "prefer Y") → `SPECS.md` Conventions or `WORKSPACE.md`, not `CONTEXT.md`.
- **Decisions and rationale** → `SPECS.md` Architecture Decisions, not `CONTEXT.md`.

Only write to `CONTEXT.md` if: a critical constant, invariant, or quick-start command was discovered that would be needed at next session start before any deep dive — and it doesn't fit `SPECS.md`.

### Memory

Do not write to memory unless the knowledge is structurally homeless across all files above. Filesystem is the source of truth.

---

## Phase 4 — Output resume prompt

The resume prompt captures only what is **not already in project files**. Do not repeat content that was just written in Phase 3 — reference the file instead.

Print the block between the `---` markers:

---

```
## Session Resume — [PROJECT] — [DATE]

### Start
Read `WORKSPACE.md`, then load the relevant `CONTEXT.md` for the active subtree.
[List only files written or modified in Phase 3 that are directly relevant to next session:]
- `path/to/file` — one-line reason it matters next session

### Git state
[Last 5 log lines + uncommitted changes from `git status`.]

### What was worked on
Specific tasks, not project overview. Last 30 minutes first.

### Open questions / unresolved threads
Discussed but not resolved. Include dead ends and what was tried.
[If none: "none."]

### Next action
[If $ARGUMENTS provided: use as directive. Otherwise: single most strategic next step from ROADMAP + current state.]
```

---

After printing, say:

> Handoff complete. Copy the block above and paste it as your first message in the new session.
> [If HISTORY.md updated]: HISTORY.md updated with [N] items.
> [If files trimmed]: ROADMAP.md / KNOWN-BUGS.md trimmed.
> [List every file written in Phase 3, one line each.]
> Start new session with `/clear` or open a fresh Claude Code window.
