# skills
> OpenCode's discovery point for the skill library: generated copies of core/skills, not tracked.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`prepare/`](prepare/CONTEXT.md) | Prepare a raw prompt for an agent: optimize, contextualize, and recommend tier/effort settings. |

| File | Description |
|------|-------------|
| [`calendar/SKILL.md`](calendar/SKILL.md) | List upcoming events and query date ranges from Google Calendar across all configured accounts (personal, cin, ufrpe). Invoke with /calendar [intent]. |
| [`compass/SKILL.md`](compass/SKILL.md) | Gentle strategic review of Brain: what has good wind, reorder by motivation, ditch guilt-free, close wins, next easy start. Invoke with /compass [optional goal or focus]. |
| [`craft/SKILL.md`](craft/SKILL.md) | Run the craft flow: develop a feature in file-relayed loops with model autorouting (clarify → plan → ground → architecture → TDD → code → user test → ship). Invoke with /craft [task or feature request]. |
| [`dedup/SKILL.md`](dedup/SKILL.md) | Semantic duplication audit for a code project: near-duplicate logic that the verbatim-clone gate misses. Invoke with /dedup [project path, defaults to cwd project]. |
| [`drive/SKILL.md`](drive/SKILL.md) | List, search, and download files from Google Drive across all configured accounts (personal, cin, ufrpe). Invoke with /drive [intent]. |
| [`foundry/SKILL.md`](foundry/SKILL.md) | Foundry VTT v14 module dev reference — router. Load relevant subfiles before working. Invoke with /foundry [topic] |
| [`gmail/SKILL.md`](gmail/SKILL.md) | Triage Gmail across all configured accounts — classify, confirm routes, write to brain/INBOX.md. |
| [`handoff/SKILL.md`](handoff/SKILL.md) | Emit a copy-pasteable resume prompt for the next session. For the full session-close ritual use /roundup, which calls this. Invoke with /handoff [focus]. |
| [`inbox/SKILL.md`](inbox/SKILL.md) | Triage brain/INBOX.md — route each entry to a goal, task, reference, project doc, writing draft, or delete. Cross-domain front door: reaches into code ROADMAP/ISSUES and domain refs/, not just brain/. |
| [`install/SKILL.md`](install/SKILL.md) | Install this workspace on the machine you are running on: probe every step in SETUP.md, report what is missing, and execute it. Invoke with /install [feature slug, or blank for everything]. |
| [`iso-visual/SKILL.md`](iso-visual/SKILL.md) | Isoroll visual-semantics reference: image-to-text conventions, known model failure modes, and how to verify visual output. Load before touching isoroll guides, kits, sprites or scenes. Invoke with /iso-visual |
| [`research/SKILL.md`](research/SKILL.md) | Execute a research workflow from the workspace Core research system. |
| [`roundup/SKILL.md`](roundup/SKILL.md) | Full session-close ritual: drain the ledgers, route session knowledge to durable files, then verify and hand off. Use at session end. Invoke with /roundup [focus for next session]. |
<!-- routing:end -->
