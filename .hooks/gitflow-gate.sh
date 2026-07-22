#!/usr/bin/env bash
# Git Flow branch gate — block direct commits to main/master/develop; require feature/|release/|hotfix/
# branch names. Scoped to code/ project repos AND the workspace structural repo.
# Paper repos (academy/papers/*) and any other nested repo are exempt.
# Called from .hooks/pre-commit. Convention: AGENTS.md (workspace) / code/SPECS.md § Git Flow (projects).

TOPLEVEL=$(git rev-parse --show-toplevel 2>/dev/null || true)
case "$TOPLEVEL" in
  /mnt/workspace/code/*) : ;;   # code project repos: enforce
  /mnt/workspace)        : ;;   # workspace structural repo: enforce
  *) exit 0 ;;                  # academy/papers/*, branches/*, and any other repo: exempt
esac

# Allow sanctioned merges (the gitflow integration steps: feature → develop → main).
# A merge in progress leaves MERGE_HEAD; that is a merge, not a hand-typed commit,
# so it must pass even on main/develop. Direct commits still get blocked below.
if [ -f "$(git rev-parse --git-dir)/MERGE_HEAD" ]; then
  exit 0
fi

BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)
case "$BRANCH" in
  main|master|develop)
    printf "⛔ Git Flow: direct commits to '%s' are not allowed.\n" "$BRANCH"
    printf "   Branch first:  git checkout -b feature/<name>   (or release/*, hotfix/*).\n"
    printf "   See AGENTS.md / code/SPECS.md § Git Flow. (Emergency bypass: git commit --no-verify.)\n"
    exit 1 ;;
  feature/*|release/*|hotfix/*|HEAD)
    exit 0 ;;   # HEAD = detached (rebase/bisect) — don't block
  *)
    printf "⛔ Git Flow: branch '%s' doesn't match feature/*, release/*, or hotfix/*.\n" "$BRANCH"
    printf "   Rename:  git branch -m feature/<name>. See code/SPECS.md § Git Flow.\n"
    exit 1 ;;
esac
