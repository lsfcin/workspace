# session
> What a session costs and what fills it, read from the local transcripts. No network, no model.

Split out of [`../CONTEXT.md`](../CONTEXT.md): these three share
[`session_log.py`](session_log.py) and read `~/.claude/projects/<slug>/*.jsonl`, unlike the
parent's other tools, which act on the workspace tree.

Quote neither report from memory — re-run the command. The cost work's lesson was four false claims
from a stale read.

## Two rules that make the attribution honest

1. **Per-turn context is exact; what *entered* is only known in characters.** The chars-per-token
   ratio is measured per turn, not assumed as a global `/4`. `context` prints the measured ratio
   and what it implies: well under ~3.5 means tokens enter that the transcript doesn't log,
   spread across the reported rows in proportion — read the shares as shares of logged material.
2. **A blocking gate is a failed `tool_result`, not an attachment** — scanning only attachments
   undercounts by two orders of magnitude. Guarded by
   `test_a_blocking_gate_is_counted_from_the_failed_tool_result`.

`CLAUDE.md`, `AGENTS.md` and `MEMORY.md` aren't logged in any transcript — the harness folds them
into the system prompt. `context` measures them on disk and subtracts them from the residual, so
the memory store's cost stays separable from everything else's.

`usage` still runs its own transcript loop instead of `session_log.py`'s `walk()`.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`session_cost.py`](session_cost.py) | [`session_cost.pyi`](session_cost.pyi) | `turn_components`, `turn_cost` | session_cost.py — the price of a turn. The one place rates live. |
| [`session_log.py`](session_log.py) | [`session_log.pyi`](session_log.pyi) | `label`, `att_chars`, `blocks`, `output_chars`, `walk` | session_log.py — replay a Claude Code transcript and attribute each turn's context growth. |
| [`session_reads.py`](session_reads.py) | [`session_reads.pyi`](session_reads.pyi) | `kind_of`, `file_reads` | session_reads.py — which files a session read, how often, and what each read served. |
| [`session_turns.py`](session_turns.py) | [`session_turns.pyi`](session_turns.pyi) | `paths_for`, `turns` | session_turns.py — what counts as ONE assistant turn, and how much of it lands in the thread. |
<!-- routing:end -->
