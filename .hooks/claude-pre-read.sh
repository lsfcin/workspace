#!/usr/bin/env bash
# PreToolUse: Read
# Non-blocking hint: if a companion interface file exists, suggest reading it first.

file=$(python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(d.get('file_path',''))" 2>/dev/null \
  <<< "$(cat)")

case "$file" in
  *.py)
    pyi="${file%.py}.pyi"
    [ -f "$pyi" ] && printf "💡 Interface available: $pyi — read this first.\n"
    ;;
  *.js)
    dts="${file%.js}.d.ts"
    [ -f "$dts" ] && printf "💡 Interface available: $dts — read this first.\n"
    ;;
esac

exit 0
