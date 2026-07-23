---
name: roundup
description: >
  Full session-close ritual: archive completed work to HISTORY, route session knowledge to durable files, drain the INBOX, run the verification gate, then emit the resume prompt via /handoff. Use at session end. Invoke with /roundup [focus for next session].
---

# Roundup skill

End the session cleanly. Gather everything the session produced into its durable home, then hand off.

Execute all phases in order. Write directly to files. Ask only on conflict or destructive ambiguity.

Arguments: $ARGUMENTS  (focus for next session — passed through to `/handoff`)

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

If the project's `package.json` declares `verify:full`, run it now (`npm run verify:full`) and record the result (green / red + failing specs) — it flows into the resume prompt. A session must not hand off claiming working state without this proof. `verify:fast`-only projects: run that instead. No contract: note "no verification contract".

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
Create only if there is content to add:
```markdown
# History

Archive of completed work and resolved issues.
```

---

## Phase 3 — Route session knowledge to durable files

Identify all knowledge from the session. Route each piece using the table below. Write directly. Conflict with existing content → ask before writing.

### Routing table

| Knowledge type | Target |
|---|---|
| Non-obvious design decision + rationale | `SPECS.md` → Architecture Decisions |
| Discovered convention / coding rule | `SPECS.md` → Conventions |
| Bug found, not fixed | `KNOWN-BUGS.md` |
| New technical work item (project has `ROADMAP.md`) | `ROADMAP.md` |
| Reference / link / paper / tool worth keeping | domain `refs/REFS.md` (route-by-domain — see `/inbox`) |
| Personal / admin / life / teaching task — or project task with hard deadline | `brain/TODO.md` (right horizon: today / week / month / backlog) |
| Insight about a specific life or career goal | `brain/goals/[goal].md` (achievement, backlog item, or obstacle) |
| Skill workflow improvement | the skill file directly |
| Workspace-wide rule across all projects | `AGENTS.md` |
| Critical quick-reference fact or constant needed at session start | `CONTEXT.md` — see exclusions |
| Doesn't fit cleanly | `brain/INBOX.md` — triaged in Phase 4 |

### TODO vs ROADMAP
**ROADMAP**: project has `ROADMAP.md` AND item is a technical milestone with agent-ready context.
**TODO**: personal / admin / life / teaching task; OR project has no `ROADMAP.md`; OR project task with a hard external deadline needing horizon tracking.
Unclear → INBOX.

### CONTEXT.md — explicit exclusions
- Routing block changes → ignore. Hooks auto-sync on edit/commit.
- Behavioral cues ("be careful with X", "prefer Y") → `SPECS.md` Conventions or `AGENTS.md`, not `CONTEXT.md`.
- Decisions + rationale → `SPECS.md` Architecture Decisions, not `CONTEXT.md`.

Write to `CONTEXT.md` only if: critical constant, invariant, or quick-start command needed at next session start — and it doesn't fit `SPECS.md`.

### Memory
Do not write to memory unless the knowledge is homeless across all files above. Filesystem is source of truth.

---

## Phase 4 — Drain the INBOX

If `brain/INBOX.md` has entries, triage them now via the `/inbox` routes (goal / task / ref / project / draft / delete): propose routes, get confirmation, act; leave unconfirmed entries. This is the session-end sweep that keeps INBOX from silently growing (paired with the `inbox-nudge` SessionStart warning).

---

## Phase 5 — Sync branches (gitflow promotion)

The session end is the **only** reliable moment to promote work. `feature/*` is already safe — the
`post-commit` hook auto-pushes it. This phase moves work up so the other machine sees it on `main`.

Applies to the workspace repo and `code/*` repos (same scope as `.hooks/gitflow-gate.sh`).
Other repos (`academy/papers/*`, `branches/*`): push the current branch, skip the merges.

```bash
git branch --show-current
git status --short
git log --oneline origin/develop..develop 2>/dev/null | wc -l   # develop unpushed
git log --oneline main..develop 2>/dev/null | wc -l             # main behind develop
```

1. **Uncommitted work** → commit it on the feature branch first (auto-push carries it out).
2. **Verification gate red or not-run** (Phase 1) → **stop here**. Do not merge. Report that the
   feature branch is pushed but unpromoted, and why. A red merge into `main` breaks the other machine.
3. **Feature complete** (its milestone shipped this session) → merge `feature/*` → `develop`, push
   `develop`. Feature still in progress → leave it; auto-push already preserved it.
4. **`develop` ahead of `main`** → merge `develop` → `main`, push `main`.
5. **Merge conflict** → abort (`git merge --abort`), leave branches untouched, report it as an open
   thread for the handoff. Never resolve conflicts unattended at session close.

Report each branch's final state (pushed / unpromoted + reason) — it flows into the resume prompt.

---

## Phase 6 — Hand off

Run `/handoff $ARGUMENTS` to emit the resume prompt. Then report:

> Roundup complete.
> [If HISTORY.md updated]: HISTORY.md updated with [N] items.
> [If files trimmed]: ROADMAP.md / KNOWN-BUGS.md trimmed.
> [List every file written this session, one line each.]
> Start the next session with `/clear` or a fresh window, pasting the resume block above.
