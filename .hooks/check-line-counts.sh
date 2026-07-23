#!/usr/bin/env bash
# Check workspace code file line counts and print warnings/errors.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/line-limits.env"

: "${WARN_LINES:=150}"
: "${BLOCK_LINES:=200}"

# Third-party code tracked verbatim is exempt: splitting it would fork it from
# upstream and make the next update impossible to diff. Declared per directory by
# a `.vendor` marker file, which applies to that directory and everything under it.
is_vendored() {
  local dir
  dir="$(cd "$(dirname "$1")" 2>/dev/null && pwd)" || return 1
  while [ -n "$dir" ] && [ "$dir" != "/" ]; do
    [ -f "$dir/.vendor" ] && return 0
    [ -d "$dir/.git" ] && return 1     # stop at a repo root
    dir="$(dirname "$dir")"
  done
  return 1
}

check_file() {
  local f="$1"
  [ -f "$f" ] || return 0

  case "$f" in
    *.d.ts) return 0 ;;
  esac

  is_vendored "$f" && return 0

  if ! printf '%s\n' "$f" | grep -Eq '\.(js|ts|tsx|py|dart|html|css|scss|tex)$'; then
    return 0
  fi

  local lines
  lines=$(wc -l < "$f")
  if [ "$lines" -ge "$BLOCK_LINES" ]; then
    printf "🚨 BLOCK: %s (%s lines)\n" "$f" "$lines"
    return 1
  fi

  if [ "$lines" -ge "$WARN_LINES" ]; then
    printf "⚠ WARN: %s (%s lines)\n" "$f" "$lines"
  fi

  return 0
}

found_warn=0
found_block=0
files=()

if [ "${1:-}" = "--from-stdin" ]; then
  while IFS= read -r f; do
    [ -n "$f" ] && files+=("$f")
  done
elif [ "$#" -gt 0 ]; then
  files=("$@")
else
  shopt -s nullglob globstar
  files=(**/*.{js,ts,tsx,py,dart,html,css,scss,tex})
fi

for f in "${files[@]}"; do
  if check_file "$f"; then
    if [ -f "$f" ]; then
      lines=$(wc -l < "$f")
      if [ "$lines" -ge "$WARN_LINES" ] && [ "$lines" -lt "$BLOCK_LINES" ]; then
        found_warn=1
      fi
    fi
  else
    found_block=1
  fi
done

if [ "$found_block" -eq 1 ]; then
  printf "\nOne or more code files exceed the block threshold (%s lines).\n" "$BLOCK_LINES"
  exit 1
fi

if [ "$found_warn" -eq 1 ]; then
  printf "\nOne or more code files exceed the warn threshold (%s lines).\n" "$WARN_LINES"
  exit 0
fi

printf "No code files exceed thresholds.\n"
exit 0
