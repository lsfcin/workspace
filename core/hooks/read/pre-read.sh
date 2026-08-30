#!/usr/bin/env bash
# PreToolUse: Read — block source reads when a current interface file exists.
# If interface is newer-or-equal: hard block (exit 2), must read interface first.
# If source is newer: interface is stale, warn and allow.

HOOKS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN="$HOOKS_DIR/../run"

# Asked, not spelled -- see the same note in post-edit.sh. Both `python3` here resolved to the
# Microsoft Store alias on this clone, so `$file` and `$session_id` were empty and every branch
# below fell through to `exit 0`: the interface-first gate could not fire, and read as passing.
PY="$(sh "$RUN" --python)" || exit 0

stdin_json="$(cat)"
file=$("$PY" -c \
	"import sys,json; d=json.load(sys.stdin); ti=d.get('tool_input'); ti=ti if isinstance(ti,dict) else d; print(ti.get('file_path',''))" 2>/dev/null \
	<<< "$stdin_json")
session_id=$("$PY" -c \
	"import sys,json; print(json.load(sys.stdin).get('session_id',''))" 2>/dev/null \
	<<< "$stdin_json")

# Facade files are already minimal interfaces — reading source directly is correct.
case "$(basename "$file")" in
	index.ts|index.tsx|index.js|index.jsx|__init__.py|index.dart) exit 0 ;;
esac

iface=""
case "$file" in
	*.py)   iface="${file%.py}.pyi" ;;
	*.js)   iface="${file%.js}.d.ts" ;;
	*.ts)   iface="${file%.ts}.d.ts" ;;
	*.tsx)  iface="${file%.tsx}.d.ts" ;;
	*.dart) iface="${file%.dart}.dart.api" ;;
	*.tex)  iface="${file%.tex}.texif" ;;
	*.csv|*.tsv) iface="${file}if" ;;  # results.csv → results.csvif
esac

[ -z "$iface" ] || [ ! -f "$iface" ] && exit 0

if [ "$file" -nt "$iface" ]; then
	printf "⚠️  INTERFACE STALE: %s\n   Source was modified after interface was generated.\n   Reading source directly — save the file to regenerate the interface.\n" "$iface"
else
	# Interface already read this session → source read allowed (editing needs implementation).
	#
	# ASKED OF THE MODULE THAT WRITES THE MARKER, never matched as text here. This was three
	# `grep -qxF` against three spellings of one path -- the writer's `C:\...`, the payload's
	# `c:\...` and a `readlink -f` `c:/...` -- so nothing ever matched and the gate below blocked
	# every source read with a message promising that reading the interface would unlock it. It
	# could not. See read/context-tracker.py was_read().
	sid="${session_id:-$(ps -o ppid= -p $PPID 2>/dev/null | tr -d ' ')}"
	if sh "$RUN" hooks/read/context-tracker.py --seen "$sid" "$iface"; then
		exit 0
	fi
	# interface-first-reads, one of the four features the ablation names. The law is consulted
	# on the branch that is about to block, not at the top of the script: this hook fires on
	# every Read, so a check up there would spend a subprocess per read to answer a question
	# that only matters on the rare read a block would stop.
	if ! sh "$RUN" hooks/feature_law.py --enabled interface-first-reads; then
		exit 0
	fi
	printf "⛔ READ INTERFACE FIRST — %s\n   Interface is current. Read it instead of the source:\n   %s\n   It has all public signatures without implementation noise.\n   (Reading the interface unlocks the source for this session.)\n" "$file" "$iface" >&2
	exit 2
fi

# ── codegraph nudge — one-time per project per session ───────────────────────
if [[ "$file" == /mnt/workspace/code/* ]]; then
	case "$file" in
		*.pyi|*.d.ts|*.dart.api|*.texif|*.csvif) : ;;  # generated — skip
		*.py|*.js|*.ts|*.tsx|*.dart|*.jsx)
			cg_root=""; cg_dir=$(dirname "$file")
			while [ "$cg_dir" != "/" ]; do
				[ -d "$cg_dir/.codegraph" ] && cg_root="$cg_dir" && break
				cg_dir=$(dirname "$cg_dir")
			done
			if [ -n "$cg_root" ]; then
				sid="${session_id:-$(ps -o ppid= -p $PPID 2>/dev/null | tr -d ' ')}"
				nudge_file="/tmp/claude_cg_nudged_${sid}.txt"
				if ! grep -qF "$cg_root" "$nudge_file" 2>/dev/null; then
					printf "💡 codegraph indexed — explore before reading source:\n"
					printf "   codegraph explore \"<question>\" %s\n" "$cg_root"
					printf "   codegraph query \"<symbol>\" %s\n" "$cg_root"
					echo "$cg_root" >> "$nudge_file"
				fi
			fi
			;;
	esac
fi

exit 0
