#!/usr/bin/env python3
# Branch promotion at session close: feature → develop → main, and what to say when it did not run.
#
# Imported by core/tools/wos/roundup, which keeps the sequence and the decisions. Same scope as
# core/hooks/git/gitflow_gate.py — the workspace repo and code/* project repos promote; every other
# nested repo just pushes its current branch.
from artifacts import git


def _out(repo, *args) -> str:
    done = git(repo, *args)
    return done.stdout.strip() if done.returncode == 0 else ''


def promote(root, branch: str, leave_dirty: bool) -> str:
    """'' when every hop landed, else the reason nothing was promoted.

    The whole thing aborts on the first conflict rather than leaving develop ahead of main.
    """
    for target, source in (('develop', branch), ('main', 'develop')):
        if git(root, 'rev-parse', '--verify', '-q', target).returncode != 0 or target == source:
            continue
        behind = _out(root, 'rev-list', '--count', f'{target}..origin/{target}')
        if behind.isdigit() and int(behind) > 0:
            return f'{target} is behind origin — a parallel session is mid-flight; not promoted'
        # A fast-forward needs no checkout, so it never touches the working tree — which is what
        # makes promoting past another session's dirt safe. Only a real merge needs HEAD to move.
        if target != branch and git(root, 'merge-base', '--is-ancestor',
                                    target, source).returncode == 0:
            if git(root, 'fetch', '-q', '.', f'{source}:{target}').returncode != 0:
                return f'fast-forward of {target} failed; not promoted'
        elif leave_dirty and target != branch:
            return (f'{target} needs a real merge — not promoted while the tree holds another '
                    "session's work")
        else:
            if git(root, 'checkout', '-q', target).returncode != 0:
                return f'checkout of {target} failed; not promoted'
            if git(root, 'merge', '--no-edit', '-q', source).returncode != 0:
                git(root, 'merge', '--abort')
                git(root, 'checkout', '-q', branch)
                return f'conflict merging {source} → {target} — aborted, branches untouched'
            git(root, 'checkout', '-q', branch)
        if git(root, 'push', '-q', 'origin', target).returncode != 0:
            return f'{target} merged but push failed'
    return ''


def promoted_line(root, branch: str) -> str:
    """What a successful promotion reports: where each branch now points, and what is unpushed."""
    shas = ''
    for name in ('main', 'develop', branch):
        if git(root, 'rev-parse', '--verify', '-q', name).returncode == 0:
            shas += f' {name}@{_out(root, "rev-parse", "--short", name)}'
    tracked = _out(root, 'for-each-ref', '--format=%(refname:short)%(upstream:track)', 'refs/heads')
    unpushed = sum(1 for line in tracked.splitlines() if 'ahead' in line)
    state = ' all pushed' if unpushed == 0 else f' {unpushed} branch(es) unpushed'
    return f'promoted ·{shas} ·{state}'
