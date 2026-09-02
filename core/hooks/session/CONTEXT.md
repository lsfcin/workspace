# session
> Session lifecycle: start, prune, precompact wipe, and the SessionStart nudges.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`compass-nudge.py`](compass-nudge.py) | [`compass-nudge.pyi`](compass-nudge.pyi) | `main` | SessionStart — a soft, ignorable reminder that the compass review hasn't run in a while, so the inspiring work waiting can gently resurface. NOT a nag: one line, in-session only, trivial to skip. Paired with /compass (the gentle strategic review). Tone law lives in brain/FOUNDATIONS.md — "what has good wind", never guilt. Mirrors the inbox-nudge pattern. |
| [`context-meter.py`](context-meter.py) | [`context-meter.pyi`](context-meter.pyi) | `state_file`, `announced`, `mark`, `find_transcript`, `last_context` | UserPromptSubmit — say what the next turn costs, once per threshold crossed. |
| [`inbox-nudge.py`](inbox-nudge.py) | [`inbox-nudge.pyi`](inbox-nudge.pyi) | `read_body`, `count_entries`, `main` | SessionStart — warn Lucas + agent when brain/INBOX.md has piled up past a threshold, so capture doesn't silently grow and scatter. The drain runs HERE, at session start where context is cheap — /roundup only counts, and hands /inbox to the next session (core/skills/roundup.md § Phase 3). |
| [`mirror-heal.py`](mirror-heal.py) | [`mirror-heal.pyi`](mirror-heal.pyi) | `heal_skills`, `report_permissions`, `main` | SessionStart — regenerate the generated content that a `git pull` cannot bring with it, and report the generated content that must NOT regenerate itself. |
| [`precompact-wipe.sh`](precompact-wipe.sh) | — | — | PreCompact — wipe the session CONTEXT.md seen-markers so the chain is re-read after compaction (injected context may be summarized away). See code/ROADMAP-verify.md W1. Switched off: the seen-markers survive compaction, so the chain is not re-read. |
| [`session-prune.sh`](session-prune.sh) | — | — | SessionStart — prune stale session marker files (context seen-markers, facade reads, codegraph nudges) older than 2 days. See code/ROADMAP-verify.md W1. `rm -rf`, not `-delete`: a seen-marker is a DIRECTORY of one file per entry since 2026-09-02 — an append to a shared file lost 22% of its marks under a parallel Read batch (hook_input.py). `-delete` refuses a non-empty one, silently, which would leave every store here forever. |
| [`start-session.sh`](start-session.sh) | — | — | Neutral session-start entrypoint |
<!-- routing:end -->
