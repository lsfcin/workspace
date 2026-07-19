#!/usr/bin/env bash
# Git Flow branch gate — block direct commits to main/master/develop; require feature/|release/|hotfix/
# branch names. Scoped to code/ project repos (the workspace structural repo is exempt).
# Called from .hooks/pre-commit. Convention: code/SPECS.md § Git Flow.

TOPLEVEL=$(git rev-parse --show-toplevel 2>/dev/null || true)
case "$TOPLEVEL" in
  /mnt/workspace/code/*) : ;;
  *) exit 0 ;;   # only code/ project repos follow the enforced flow
esac

BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)
case "$BRANCH" in
  main|master|develop)
    printf "⛔ Git Flow: direct commits to '%s' are not allowed.\n" "$BRANCH"
    printf "   Branch first:  git checkout -b feature/<name>   (or release/*, hotfix/*).\n"
    printf "   See code/SPECS.md § Git Flow. (Emergency bypass: git commit --no-verify.)\n"
    exit 1 ;;
  feature/*|release/*|hotfix/*|HEAD)
    exit 0 ;;   # HEAD = detached (rebase/bisect) — don't block
  *)
    printf "⛔ Git Flow: branch '%s' doesn't match feature/*, release/*, or hotfix/*.\n" "$BRANCH"
    printf "   Rename:  git branch -m feature/<name>. See code/SPECS.md § Git Flow.\n"
    exit 1 ;;
esac
