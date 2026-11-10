#!/usr/bin/env python3
# Branch promotion at session close: feature → develop → main, and what to say when it did not run.
#
# Imported by core/tools/wos/roundup, which keeps the sequence and the decisions. Same scope as
# core/hooks/git/gitflow_gate.py — the workspace repo and code/* project repos promote; every other
# nested repo just pushes its current branch.
import tempfile

from artifacts import dirt, git, out


def gitflow(workspace, repo) -> bool:
    """Which repos promote develop → main: the workspace itself, and the projects under code/.

    The scope this file's head has always declared, in the one place both callers read it — the
    close's own repo and the project sweep beside it. It was a line inside roundup while the sweep
    promoted nothing, which is how nine projects sat 22 commits behind their own develop.
    """
    return repo == workspace or (repo.parent.name == 'code' and repo.parent.parent == workspace)


def disturbed(repo, branch: str) -> str:
    """Why promotion must not run after all, or ''. Asked AFTER verify: a session writing or
    switching branches meanwhile makes the green describe a tree that is no longer there."""
    if out(repo, 'branch', '--show-current') != branch:
        return f'HEAD moved off {branch} during the close; not promoted'
    if dirt(repo):
        return 'the tree changed during the close — another session is writing; not promoted'
    return ''


def promote(root, branch: str) -> str:
    """'' when every hop landed, else the reason nothing was promoted.

    The whole thing aborts on the first conflict rather than leaving develop ahead of main.
    """
    for target, source in (('develop', branch), ('main', 'develop')):
        # A hop with either end missing has nothing to carry: a repo without develop is not a conflict.
        if target == source or any(git(root, 'rev-parse', '--verify', '-q', ref).returncode != 0
                                   for ref in (target, source)):
            continue
        behind = out(root, 'rev-list', '--count', f'{target}..origin/{target}')
        if behind.isdigit() and int(behind) > 0:
            return f'{target} is behind origin — a parallel session is mid-flight; not promoted'
        # A fast-forward needs no checkout, so it never touches the working tree. Real merges run
        # in a throwaway worktree so HEAD in the caller's working tree never moves.
        if target != branch:
            if git(root, 'merge-base', '--is-ancestor', target, source).returncode == 0:
                if git(root, 'fetch', '-q', '.', f'{source}:{target}').returncode != 0:
                    return f'fast-forward of {target} failed; not promoted'
            else:
                with tempfile.TemporaryDirectory() as wt:
                    if git(root, 'worktree', 'add', '-q', wt, target).returncode != 0:
                        return f'checkout of {target} failed; not promoted'
                    try:
                        if git(wt, 'merge', '--no-edit', '-q', source).returncode != 0:
                            return f'conflict merging {source} → {target} — aborted, branches untouched'
                    finally:
                        git(root, 'worktree', 'remove', '--force', wt)
        else:
            if git(root, 'merge', '--no-edit', '-q', source).returncode != 0:
                git(root, 'merge', '--abort')
                return f'conflict merging {source} → {target} — aborted, branches untouched'
        if git(root, 'push', '-q', 'origin', target).returncode != 0:
            return f'{target} merged but push failed'
    return ''


def park(repo, branch: str) -> str:
    """Put HEAD back on develop once `branch` has landed there; the suffix a status line gains.

    Ruled 2026-11-09 (Lucas): a finished branch left checked out is inherited by the next session,
    which then writes on it. On develop, the branch gate makes its first write choose one instead.
    A tree with anything uncommitted stays where it is: switching would carry that work along.
    """
    if branch in ('develop', 'main', 'master') or \
            git(repo, 'rev-parse', '--verify', '-q', 'develop').returncode != 0 or \
            git(repo, 'merge-base', '--is-ancestor', branch, 'develop').returncode != 0 or dirt(repo):
        return ''
    moved = git(repo, 'switch', '-q', 'develop').returncode == 0
    return ' · HEAD → develop' if moved else ' · could not switch to develop'


def promoted_line(root, branch: str) -> str:
    """What a successful promotion reports: where each branch now points, and what is unpushed."""
    shas = ''
    for name in ('main', 'develop', branch):
        if git(root, 'rev-parse', '--verify', '-q', name).returncode == 0:
            shas += f' {name}@{out(root, "rev-parse", "--short", name)}'
    tracked = out(root, 'for-each-ref', '--format=%(refname:short)%(upstream:track)', 'refs/heads')
    unpushed = sum(1 for line in tracked.splitlines() if 'ahead' in line)
    state = ' all pushed' if unpushed == 0 else f' {unpushed} branch(es) unpushed'
    return f'promoted ·{shas} ·{state}'
