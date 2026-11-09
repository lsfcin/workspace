#!/usr/bin/env python3
# The repos a session worked in, and at its close: verify, push, promote each nested one.
#
# Split out of core/tools/wos/roundup 2026-09-09, at the second recurrence of b20260831. The sweep
# lived in the caller as one function that answered "is there anything to push" with a string that
# was empty both when there was nothing and when the question could not be asked. Six projects held
# 22 unpushed commits each while every close called them quiet, and nine held develop 22 commits
# ahead of main while close/branches.py already said code/* projects promote. Both halves are here
# now, where the difference between an empty answer and a failed question is a returncode.
import json
import re
from pathlib import Path

import branches
from artifacts import git, out
from handoff import edits, identity, records, transcript

COMMIT = re.compile(r'\bgit\s+(?:-C\s+\S+\s+)?commit\b')
MOVE = re.compile(r'(?:\bcd\s+|\bgit\s+-C\s+)("[^"]+"|\S+)')


def push(repo, branch: str) -> str:
    """'' when the remote already has this branch, else 'pushed' or 'failed'.

    A branch with no upstream is the case that went blind: `git log @{upstream}..HEAD` FAILS
    there, and the caller read the failure as an empty answer. It gets one, with `-u`, so the
    next close can ask.
    """
    tracked = git(repo, 'rev-parse', '--abbrev-ref', '@{upstream}').returncode == 0
    if tracked and not out(repo, 'log', '--oneline', '@{upstream}..HEAD'):
        return ''
    args = ('push', '-q', 'origin', 'HEAD') if tracked else ('push', '-q', '-u', 'origin', branch)
    return 'pushed' if git(repo, *args).returncode == 0 else 'failed'


def session_log(root: Path) -> Path | None:
    """This session's own transcript, or None when the harness does not say which one it is."""
    try:
        session, agent = identity()
        return transcript(session, agent, root)
    except ValueError:
        return None


def _commit_dir(command: str, cwd: Path) -> Path | None:
    """Where a shell command committed, or None if it did not."""
    commit = COMMIT.search(command)
    if not commit:
        return None
    moves = MOVE.findall(command[:commit.end()])
    return cwd / moves[-1].strip('"\';&') if moves else cwd


def _touched_paths(log: Path, cwd: Path) -> set:
    """Every path this session edited or committed in: the transcript, never the clock.

    Commit timestamps were the first answer and the wrong one: sessions run in parallel, so a
    commit made during this session is not a commit made BY it.
    """
    paths = {Path(name) for name in edits(log, cwd)}
    for row in records(log):
        if row.get('isSidechain'):
            continue
        payload = row.get('payload') if isinstance(row.get('payload'), dict) else {}
        cwd = Path(row.get('cwd') or payload.get('cwd') or cwd)
        content = row.get('message', {}).get('content', [])
        for block in content if isinstance(content, list) else []:
            if block.get('type') == 'tool_use' and block.get('name') in ('Write', 'NotebookEdit'):
                paths.add(Path(block['input'].get('file_path') or block['input'].get('notebook_path', '')))
            elif block.get('type') == 'tool_use' and block.get('name') == 'Bash':
                paths.add(_commit_dir(block['input'].get('command', ''), cwd))
        if payload.get('type') == 'function_call':
            try:
                args = json.loads(payload.get('arguments') or '{}')
            except json.JSONDecodeError:
                continue
            command = args.get('cmd') or args.get('command') or ''
            paths.add(_commit_dir(command if isinstance(command, str) else ' '.join(command),
                                  Path(args.get('workdir') or cwd)))
    return {path for path in paths if path and str(path) != '.'}


def session_repos(root: Path, log: Path) -> set:
    """The repos this session worked in: `root` itself and/or its nested projects."""
    from entropy_corpus import nested_repos
    top = root.resolve()
    nested = [repo.resolve() for repo in nested_repos(root)]
    found = set()
    for path in _touched_paths(log, root):
        full = (root / path).resolve()
        if full.is_relative_to(top):
            found.add(max((r for r in nested if full.is_relative_to(r)),
                          key=lambda r: len(r.parts), default=top))
    return {root if repo == top else repo for repo in found}


def sweep(root: Path, repos, verify, promote: bool = True) -> str:
    """Verify, push and promote the nested projects in `repos`, and say what happened.

    Only the ones this session worked in (Lucas, 2026-11-09): this used to walk every project and
    promote each with no verify run, and any debt it left is counted by branch_debt regardless. A
    repo with no remote is named, never pushed: that one cannot be fixed from here.
    """
    from platform_law import posix
    worked, pushed, promoted, stuck, homeless = [], [], [], [], []
    for repo in sorted(repos):
        name = posix(repo.relative_to(root.resolve()))
        branch = out(repo, 'rev-parse', '--abbrev-ref', 'HEAD')
        worked.append(f'{name} on {branch}')
        if not out(repo, 'remote', 'get-url', 'origin'):
            homeless.append(name)
            continue
        git(repo, 'fetch', '--quiet')
        landed = push(repo, branch)
        if landed:
            (pushed if landed == 'pushed' else stuck).append(name)
        if not promote or not branches.gitflow(root, repo):
            continue
        if verify(repo)[0] == 'red':
            stuck.append(f'{name} — verify red, not promoted')
            continue
        was = out(repo, 'rev-parse', 'main')
        refused = branches.promote(repo, branch)
        if refused:
            stuck.append(f'{name} — {refused}')
        elif out(repo, 'rev-parse', 'main') != was:
            promoted.append(name)
    said = [f'worked: {", ".join(worked)}' if worked else '',
            f'{len(pushed)} pushed' if pushed else '',
            f'{len(promoted)} promoted' if promoted else '',
            f'{len(stuck)} failed: {", ".join(stuck)}' if stuck else '',
            f'{len(homeless)} with no remote: {", ".join(homeless)}' if homeless else '']
    return ' · '.join(part for part in said if part)
