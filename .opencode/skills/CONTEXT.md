# skills
> OpenCode skills for this workspace.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`prepare/`](prepare/CONTEXT.md) | Prepare a raw prompt for Claude Code. |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`calendar/SKILL.md`](calendar/SKILL.md) | — | — | List upcoming events and query date ranges from Google Calendar across all configured accounts (personal, cin, ufrpe). Invoke with /calendar [intent]. |
| [`compass/SKILL.md`](compass/SKILL.md) | — | — | Gentle strategic review of Brain: surface what has good wind, reorder energy by motivation, negotiate timing, offer guilt-free ditching, close wins, and hand you the next easy start. Invoke with /compass [optional goal or focus]. |
| [`dedup/SKILL.md`](dedup/SKILL.md) | — | — | Semantic duplication audit for a code project: finds regenerated near-duplicate logic that the jscpd pre-commit gate (verbatim clones) misses, using codegraph + targeted reading. Invoke with /dedup [project path, defaults to cwd project]. |
| [`drive/SKILL.md`](drive/SKILL.md) | — | — | List, search, and download files from Google Drive across all configured accounts (personal, cin, ufrpe). Invoke with /drive [intent]. |
| [`foundry/SKILL.md`](foundry/SKILL.md) | — | — | Foundry VTT v14 module dev reference — router. Load relevant subfiles before working. Invoke with /foundry [topic] |
| [`gmail/SKILL.md`](gmail/SKILL.md) | — | — | Triage Gmail across all configured accounts — classify, confirm routes, write to brain/INBOX.md. |
| [`handoff/SKILL.md`](handoff/SKILL.md) | — | — | Emit a copy-pasteable resume prompt for the next session — the narrow last step only. For the full session-close ritual (archive done work + route knowledge + drain INBOX + verify, then hand off), use /roundup, which calls this. Invoke with /handoff [focus]. |
| [`inbox/SKILL.md`](inbox/SKILL.md) | — | — | Triage brain/INBOX.md — route each entry to a goal, task, reference, project doc, writing draft, or delete. Cross-domain front door: reaches into code ROADMAP/KNOWN-BUGS and domain refs/, not just brain/. |
| [`iso-visual/SKILL.md`](iso-visual/SKILL.md) | — | — | Isoroll visual-semantics reference: conventions that map isometric imagery to text, known model failure modes, and the hard rule for verifying visual/geometric output. Load before any session/loop that touches isoroll guides, kits, sprites, or scene assembly. Invoke with /iso-visual |
| [`loops/SKILL.md`](loops/SKILL.md) | — | — | Run the craft flow: develop a feature in file-relayed loops with model autorouting (clarify → plan → ground → architecture → TDD → code → user test → ship). Invoke with /loops [task or feature request]. |
| [`research/SKILL.md`](research/SKILL.md) | — | — | Execute a research workflow from the workspace Core research system. |
| [`roundup/SKILL.md`](roundup/SKILL.md) | — | — | Full session-close ritual: archive completed work to HISTORY, route session knowledge to durable files, drain the INBOX, run the verification gate, then emit the resume prompt via /handoff. Use at session end. Invoke with /roundup [focus for next session]. |
<!-- routing:end -->
