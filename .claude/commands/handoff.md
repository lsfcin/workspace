---
name: handoff
description: >
  Emit a copy-pasteable resume prompt for the next session — the narrow last step only. For the full session-close ritual (archive done work + route knowledge + drain INBOX + verify, then hand off), use /roundup, which calls this. Invoke with /handoff [focus].
---

# Handoff skill

Produce the resume prompt for the next session. Capture only what is **not already in project files** — reference the file instead of repeating it.

Arguments: $ARGUMENTS  (focus for next session)

> **Narrow by design.** This emits only the resume prompt. To also archive completed work, route session knowledge to durable files, drain the INBOX, and run the verification gate first, use `/roundup` — it runs those phases, then calls `/handoff`.

## Gather state

```bash
git branch --show-current 2>/dev/null
git rev-parse --short HEAD 2>/dev/null
git status --short 2>/dev/null | wc -l
git for-each-ref --format='%(refname:short) %(upstream:track)' refs/heads 2>/dev/null
git log --oneline main..develop 2>/dev/null | wc -l
```

If a fresh verification result exists from this session, cite it. If not run this session, say "not run".

**Report sync divergence, never fix it.** `/handoff` can be invoked mid-session, so merging here risks
promoting unverified work. Just state what is unpushed or unpromoted (`[ahead N]` on any branch, or
`develop` ahead of `main`) so a session resumed on another machine knows what it is missing.
Promotion is `/roundup` Phase 5 — point there if anything is behind.

## Output

Print the block between the `---` markers:

---

```
## Resume — [PROJECT] — [DATE]

### Next action
[If $ARGUMENTS: use as directive. Else: single most strategic next step from ROADMAP + current state.]

### Worked on
[Specific tasks, terse; last 30 min first. Not a project overview.]

### Open threads
[Discussed but unresolved — include dead ends and what was tried. If none: "none."]

### State
branch@sha · N uncommitted · verify: green / red / not-run
sync: all pushed / [branch ahead N unpushed] / develop N ahead of main
[Files worth reading first — one line each, only if not obvious from ROADMAP.]
```

---

After printing:

> Resume prompt ready. Copy the block, paste as the first message in a new session (`/clear` or a fresh Claude Code window).
