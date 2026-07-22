#!/usr/bin/env bash
# Nested-gitlink gate — block committing undeclared gitlinks (mode 160000) into the
# workspace structural repo. Internal projects use their own git repos (AGENTS.md);
# they must NOT be embedded as gitlinks (a fresh clone can't fetch them → broken pins
# + recurring "M" noise every time you commit inside them). Real submodules declared
# in .gitmodules are allowed. Called from .hooks/pre-commit.

# Only the workspace structural repo.
TOPLEVEL=$(git rev-parse --show-toplevel 2>/dev/null || true)
[ "$TOPLEVEL" = /mnt/workspace ] || exit 0

# Newly-staged/modified gitlinks: --raw field 2 is the new mode.
staged_gitlinks=$(git diff --cached --raw | awk '$2 == "160000" {print $NF}')
[ -z "$staged_gitlinks" ] && exit 0

offenders=""
while IFS= read -r path; do
  [ -z "$path" ] && continue
  # Declared submodule? (path present in .gitmodules)
  if [ -f .gitmodules ] && git config --file .gitmodules --get-regexp '^submodule\..*\.path$' 2>/dev/null \
       | awk '{print $2}' | grep -qxF "$path"; then
    continue
  fi
  offenders="$offenders $path"
done <<< "$staged_gitlinks"

if [ -n "$offenders" ]; then
  printf "⛔ Undeclared gitlink(s) staged:%s\n" "$offenders"
  printf "   Internal projects use their own repos — don't embed them in the workspace.\n"
  printf "   Untrack:  git rm --cached <path>   then add the dir to .gitignore.\n"
  printf "   (A genuine submodule must be declared in .gitmodules.)\n"
  exit 1
fi
exit 0
