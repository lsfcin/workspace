#!/usr/bin/env bash
# PreCompact — wipe the session CONTEXT.md seen-markers so the chain is re-read after
# compaction (injected context may be summarized away). See code/ROADMAP-verify.md W1.
# Switched off: the seen-markers survive compaction, so the chain is not re-read.
RUN="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/run"
sh "$RUN" hooks/feature_law.py --enabled precompact-wipe || exit 0
sid=$("$(sh "$RUN" --python)" -c \
	"import sys,json; print(json.load(sys.stdin).get('session_id',''))" 2>/dev/null)
# Both stores, and `-rf` because each is a directory of one file per entry (hook_input.py). The
# interface marker was never wiped here, so a compaction re-asked for the CONTEXT.md chain while
# leaving the stub gate unlocked — half a wipe, on the one event that exists to reset both.
[ -n "$sid" ] && rm -rf "/tmp/claude_ctx_seen_${sid}" "/tmp/claude_iface_seen_${sid}"
exit 0
