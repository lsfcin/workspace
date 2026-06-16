---
name: handoff
description: >
  End current session cleanly: archive completed work (moves done ROADMAP items and fixed bugs
  to HISTORY.md), then produce a copy-pasteable resume prompt for the next session.
  Invoke with /handoff [focus for next session].
---

# Handoff skill
End current session cleanly: archive completed work, then produce a copy-pasteable resume prompt for the next session.

Arguments: $ARGUMENTS

---

## Execution protocol

Execute all phases in order. Do not skip phases. Do not ask for confirmation mid-skill unless a destructive ambiguity arises.

---

## Phase 1 — Discover project files

Run these commands:

```bash
# What project files exist?
find . -maxdepth 3 \( \
  -name "ROADMAP.md" -o -name "KNOWN-BUGS.md" -o -name "HISTORY.md" \
  -o -name "CHANGELOG.md" -o -name "TODO.md" -o -name "CLAUDE.md" \
  -o -name "TASKS.md" -o -name "BACKLOG.md" \
\) 2>/dev/null | sort

# Recent git activity (skip if no git)
git log --oneline -15 2>/dev/null || echo "no git"
git status --short 2>/dev/null || echo "no git status"
```

Read every file found above before proceeding. Do not summarize — read the full content. These files define what is ALREADY captured and must not be duplicated in the resume prompt.

---

## Phase 2 — Cleanup pass

### ROADMAP cleanup

If `ROADMAP.md` (or equivalent) exists:

1. Identify completed items — any of:
   - Checkbox syntax: `- [x]`
   - Explicit status: "done", "shipped", "released", "merged", "complete", "✅"
2. For each completed item, append to `HISTORY.md` under `## Completed — YYYY-MM-DD`:
   ```
   - [item text] *(from ROADMAP)*
   ```
3. Remove completed items from `ROADMAP.md`. Leave only active, pending, and in-progress items.
4. If nothing is completed, skip — do not modify `ROADMAP.md`.

### KNOWN-BUGS cleanup

If `KNOWN-BUGS.md` (or equivalent) exists:

1. Identify resolved items — any of:
   - Checkbox: `- [x]`
   - Explicit status: "fixed", "resolved", "closed", "no longer reproducible"
2. Append to `HISTORY.md` under `## Resolved Bugs — YYYY-MM-DD`:
   ```
   - [bug description] *(resolved)*
   ```
3. Remove resolved items from `KNOWN-BUGS.md`. Leave only active known bugs.
4. If nothing is resolved, skip.

### HISTORY.md

If it doesn't exist yet, create it with a minimal header:
```markdown
# History

Archive of completed work and resolved issues.
```

Only create/modify `HISTORY.md` if there is actual content to add. Do not create an empty file.

---

## Phase 3 — Capture session-only knowledge

This phase captures ONLY what exists in this conversation and is NOT already written in any project file. Apply the non-duplication rule strictly: if it is already in ROADMAP.md, CLAUDE.md, KNOWN-BUGS.md, or any other file you read — do not repeat it. Reference the file by path instead.

Identify and record:

**A. Decisions made in this session**
Choices made in this conversation that have not yet been written to any file. Include the reasoning and tradeoffs — not just the conclusion. This is the highest-value content of the handoff.

**B. User constraints established**
Explicit rules given by the user in this conversation ("do not X", "always use Y", "never change Z"). These are the most likely to be lost and the most dangerous if forgotten.

**C. Files modified**
From `git status` output or tool calls made during this session.

**D. What was worked on**
Specific tasks, not the general project description. Focus on the last 30 minutes first — recency matters.

**E. Open questions / unresolved threads**
Things discussed but not resolved. Includes dead ends — what was tried and why it did not work.

**F. Next action**
If `$ARGUMENTS` was provided: use it as the next session's directive.
If no arguments: propose the single most strategic next step based on ROADMAP and current state.

---

## Phase 4 — Output the resume prompt

Print the following block between the two `---` markers. It must be fully self-contained — a fresh Claude instance with no prior context should be able to resume from it alone.

---

```
## Session Resume — [PROJECT] — [DATE]

### 1. Read these files first (do not skip)
[List every project file found in Phase 1, with one-line description of what each contains.
Example:
- `CLAUDE.md` — project context, conventions, constraints
- `ROADMAP.md` — active priorities and upcoming work
- `KNOWN-BUGS.md` — active known issues
Omit files that have no bearing on next session's work.]

### 2. Recent git activity
[Paste last 5-10 git log lines, or "no git".]

### 3. What was just worked on
[Section D from Phase 3. Specific, recent. Not a project overview.]

### 4. Decisions made (not yet in any file)
[Section A from Phase 3. Include reasoning. If empty, say "none — all decisions are reflected in project files."]

### 5. Constraints to preserve
[Section B from Phase 3. If empty, say "none established this session beyond what is in CLAUDE.md."]

### 6. Open questions
[Section E from Phase 3. If none, say "none."]

### 7. Do not
- Do not refactor or rename anything not directly related to the next action.
- Do not re-litigate decisions already made (see section 4).
- Do not recreate files that already exist — read them first.
[Add any session-specific prohibitions here.]

### 8. Next action
[Section F from Phase 3. One clear directive. If no $ARGUMENTS: "Analyze project state from the files above, propose the single most strategic next step with brief reasoning, and wait for confirmation before proceeding."]

### 9. Confidence
- Files read: ✅ verified this session
- Git state: ✅ verified
- Decisions (section 4): ✅ direct from this conversation
- Open questions: ✅ direct from this conversation
[Flag anything that is inferred rather than directly known as ⚠️]
```

---

After printing the resume prompt, say:

> Handoff complete. Copy the block above and paste it as your first message in the new session.
> [If HISTORY.md was updated]: HISTORY.md updated with [N] completed items.
> [If files were cleaned]: ROADMAP.md / KNOWN-BUGS.md trimmed.
> Start a new session with `/clear` or open a fresh Claude Code window.
