# sandbox.py — the isolated copy a writing worker runs in: make it, list what the worker changed, run the checks there, and bring back only what passed.
#
# WHY A COPY AND NOT THE TREE. A worker never touches its checks nor writes outside write_paths
# (core/ROADMAP-workers.md); in a copy that holds by construction, and nothing reaches the workspace
# until the wrapper's checks are green (Lucas, 2026-11-26). No worktree: core/hooks/git/SPECS.md.
#
# WHY A FRESH GIT REPO IN IT. `git status` is then the one honest list of what the worker changed,
# deleted or created, and the same base serves the patch mode later (git diff).
from __future__ import annotations

import hashlib
import pathlib
import shutil
import subprocess
import tempfile

CHECK_TIMEOUT = 600
TAIL = 1200  # chars of a failed check's output a retry gets; the rest is noise to a fresh session
_GIT = ['git', '-c', 'core.hooksPath=/dev/null', '-c', 'commit.gpgsign=false',
        '-c', 'user.name=delegate', '-c', 'user.email=delegate@localhost']


def _git(copy: pathlib.Path, *args: str) -> str:
    return subprocess.run([*_GIT, '-C', str(copy), *args], check=True, capture_output=True, text=True, encoding="utf-8").stdout


def make(root: pathlib.Path) -> pathlib.Path:
    """A copy of `root`'s tree as the orchestrator sees it — tracked files with their uncommitted
    edits, and new files not yet tracked (a worker once blocked on modules never committed,
    2026-11-26) — with the interpreter linked in so `core/run` works, committed as the base."""
    copy = pathlib.Path(tempfile.mkdtemp(prefix='delegate-'))
    tree = subprocess.run(['git', '-C', str(root), 'stash', 'create'], capture_output=True, text=True, encoding="utf-8").stdout.strip() or 'HEAD'
    archive = subprocess.run(['git', '-C', str(root), 'archive', tree], check=True, capture_output=True).stdout
    subprocess.run(['tar', '-x', '-C', str(copy)], input=archive, check=True)
    new = subprocess.run(['git', '-C', str(root), 'ls-files', '-z', '--others', '--exclude-standard'],
                         check=True, capture_output=True, text=True, encoding="utf-8").stdout.split('\0')
    for p in filter(None, new):
        if (root / p).is_file():
            (copy / p).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / p, copy / p)
    if (root / '.venv').exists():
        (copy / '.venv').symlink_to(root / '.venv')
    _git(copy, 'init', '-q')
    _git(copy, 'add', '-A')
    _git(copy, 'commit', '-q', '-m', 'base')
    return copy


def changed(copy: pathlib.Path) -> list[str]:
    """Every path the worker modified, created or deleted, relative to the copy."""
    out = []
    for line in _git(copy, 'status', '--porcelain', '-uall', '--no-renames').splitlines():
        out.append(line[3:].strip('"'))
    return sorted(out)


def check(copy: pathlib.Path, checks: list) -> list[tuple]:
    """(command, exit code, output tail) per check, run in the copy by the wrapper, never the worker."""
    results = []
    for cmd in checks:
        try:
            p = subprocess.run(cmd, shell=True, cwd=copy, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=CHECK_TIMEOUT)
            results.append((cmd, p.returncode, (p.stdout + p.stderr)[-TAIL:]))
        except subprocess.TimeoutExpired:
            results.append((cmd, 124, f'timed out after {CHECK_TIMEOUT} s'))
    return results


def bring(copy: pathlib.Path, root: pathlib.Path, paths: list) -> list[tuple]:
    """Copy each path back to `root` (or delete it there, when the worker deleted it): (path, sha256[:12] or 'deleted')."""
    done = []
    for p in paths:
        src, dst = copy / p, root / p
        if src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            done.append((p, hashlib.sha256(src.read_bytes()).hexdigest()[:12]))
        else:
            dst.unlink(missing_ok=True)
            done.append((p, 'deleted'))
    return done


def drop(copy: pathlib.Path) -> None:
    shutil.rmtree(copy, ignore_errors=True)
