#!/usr/bin/env bash
# PreToolUse: Read — block source reads when a current interface file exists.
# If interface is newer-or-equal: hard block (exit 2), must read interface first.
# If source is newer: interface is stale, warn and allow.

file=$(python3 -c \
	"import sys,json; d=json.load(sys.stdin); print(d.get('file_path',''))" 2>/dev/null \
	<<< "$(cat)")

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
	printf "⛔ READ INTERFACE FIRST — %s\n   Interface is current. Read it instead of the source:\n   %s\n   It has all public signatures without implementation noise.\n" "$file" "$iface"
	exit 2
fi

exit 0
