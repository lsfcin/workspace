# ZCode hook protocol
> Will ZCode execute this workspace's hook registration in `.zcode/config.json`, and what does a fired hook actually
> receive?

## Method

Register probe hooks in `.zcode/config.json` (`hooks.enabled: true`, all four usable events,
no matcher): `core/hooks/zcode/probe.sh` dumps stdin + filtered env + cwd + ppid to
`/tmp/zcode_probe/`; `probe-deny.sh` (plain-text stdout + exit 2) rides a sacrificial
`WebFetch` matcher. Run the battery in a fresh ZCode session: Read, Bash, Write, Edit, Agent
(Explore subagent), WebFetch, prompt submit. Measurement = dump files present per event +
verbatim block text for WebFetch. Re-run after any trust/config change — the instruments were
deleted after Sonda 2 (done work; restore from git history to re-run).

## Results

| Date | Run | Hooks fired | WebFetch blocked | Verdict |
|---|---|---|---|---|
| 2026-08-21 | Sonda 1 — fresh scheduled session, config created mid-session of another | **0** (`/tmp/zcode_probe/` never created) | no (deny never ran) | config read + parsed, execution blocked by workspace-trust gate |
| 2026-09-04 | Sonda 2 — trusted session (trust accepted after Sonda 1) | **yes** (probe dump written at session start; canonical gates visibly blocked) | **yes**, plain text verbatim | hooks fire post-trust; direct registration (2A) confirmed |

Run detail (2026-08-21, ZCode 3.8.1):

- Config accepted: diagnostics name `/mnt/workspace/.zcode/config.json`, scope `project`,
  path `hooks` — schema valid, `enabled: true` honored as a flag.
- Blocker, logged at every session event:
  `config.project_hooks.pending_trust` (adapters.config) — *"Project hooks are pending
  workspace trust and remain blocked"*. Not a matcher miss: nothing executed at all.
- Trust state is not agent-writable: absent from `~/.zcode/v2/setting.json`,
  `~/.zcode/v2/config.json`, and `~/.zcode/cli/db/db.sqlite` (`local_setting` holds only
  `permission.mode=yolo`, `model.reasoningLevel`; `permission` table empty). Client-UI
  acceptance, once per machine.
- Config is evaluated per fresh session, not per tool call, not mid-session (main session
  that authored the config never saw it; the scheduled session did; a user-scope config
  created mid-session was likewise ignored).
- `zcode` binary is the Electron desktop launcher — no headless session spawn from Bash.
- Doc discrepancy: zcode-plugin skill `diagnosing-hooks` claims non-plugin config hooks have
  "no trust gate … run unconditionally" — contradicted for project scope by this run. User
  scope untested (a user-scope probe config was created for a Sonda 2, then removed without
  running: its WebFetch-deny would block every workspace).

Run detail (2026-09-04, ZCode 3.8.1, trusted):

- SessionStart probe fired at startup: `probe.sh` executed through the expanded
  `${ZCODE_PROJECT_DIR}` and wrote `/tmp/zcode_probe/000_SessionStart.txt` — variable
  expansion works, and the env carries **both** spellings (`ZCODE_PROJECT_DIR` and
  `CLAUDE_PROJECT_DIR`, plus `ZCODE_SESSION_ID`/`CLAUDE_SESSION_ID`).
- stdin payload measured: flat JSON (not nested), with duplicated camelCase/snake_case keys —
  `session_id`/`sessionId`, `hook_event_name`/`hookEventName`,
  `transcript_path`/`transcriptPath` — plus `cwd`, `permission_mode`, `source`, `model`,
  `traceId`, `turnId`. `session_id` is present, so no PPID fallback is needed;
  `hook_input.py` tolerates the shape as-is.
- Exit-2 fidelity: the WebFetch deny probe's plain-text stdout reason
  (`PROBE-DENY-PLAIN: …`) reached the agent **verbatim** as the tool error. 2A stands —
  no adapter `zcode-hook.py` is needed.
- Canonical gates fired under ZCode in the same session: the Read context-gate and the Bash
  context-gate both blocked exactly as they do under Claude Code; the pre-edit chain fired on
  the B5 edits themselves, and the SessionStart list (prune, branch marker, mirror-heal,
  nudges) ran with the probe.

## What changed

- Direct registration (2A) **confirmed** by Sonda 2: the canonical `core/hooks/*` scripts spawn
  through `core/run` with `${ZCODE_PROJECT_DIR}`, no adapter was ever needed, and
  `core/hooks/zcode/` was deleted — done work, git holds the probes.
- Both probe registrations removed from `.zcode/config.json` (2026-09-04): WebFetch is
  unblocked and `/tmp/zcode_probe/` stays empty. `.zcode/SPECS.md` § Measured answers
  holds the three of them; the B5 section left ISSUES.md behind its regression spec.
- `test_shim_paths.py` reads `.zcode/config.json` in SHIMS (2026-08-28-style path check) and
  `test_port_ratchet.py` dropped the two probe shells when the directory died.

## Limitations

- Only SessionStart got a probe **dump** — the other events were verified indirectly, by the
  gates' visible behavior (blocks, nudges), not by payload capture. Per-event stdin for
  PreToolUse/PostToolUse is assumed Claude-compatible from the SessionStart schema, not dumped.
- One machine, one ZCode version (3.8.1, Linux); the trust gate's UI wording/flow was not
  observed, only its log signature.
- Sonda 1 could not separate "config re-read at session start" from "diagnostics emitted per
  event" — both are consistent with the log.
