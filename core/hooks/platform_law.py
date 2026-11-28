#!/usr/bin/env python3
# The platform boundary: the one file in this workspace allowed to know what an operating system is.
#
# Sibling of file_law.py / schema_law.py / feature_law.py — one module owns one question so the
# answer cannot drift: this one, what the machine underneath is.
#
# WHY A BOUNDARY AND NOT A PER-OS FORK. Porting bash to Python removes the per-OS axis rather than
# adding a Windows arm: all three per-OS forks this workspace ever had were broken by the time the
# port found them. So `sys.platform` appears HERE and nowhere else, held at zero by
# core/tools/test/workspace/ceilings/test_port_ceiling.py.
#
# ONLY WHAT HAS A CALLER — an API written before its call site is a guess later readers mistake for
# a decision. Every name below is imported or spawned from outside this file.
import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from functools import cache
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]

# The one place a platform question is answered by name. Every other module asks a function here.
_WINDOWS = sys.platform == 'win32'
_DARWIN = sys.platform == 'darwin'

POSIX_VENV_BIN = '.venv/bin'         # the boundary publishes its DATA, not only its behaviour: these
WINDOWS_VENV_BIN = '.venv/Scripts'   # were re-spelled in 20 files, which is what the ceilings count
AUTHORING_ROOT = '/mnt/workspace'    # named ONCE, so a checker can search without self-finding


def venv_script(name: str, venv: str = '.venv') -> Path:
    """A console script inside the venv — pytest, stubgen, yt-dlp, pip. Two differences in one
    answer: the directory (bin vs Scripts) and the suffix; by hand, a check misreports a present dep.
    `venv` names a sibling venv with the same layout: `.venv-pdf` holds the PDF engines, whose ~120
    packages the venv every hook starts on should not carry (core/tools/pdf/requirements-pdf.txt)."""
    bin_dir = (WINDOWS_VENV_BIN if _WINDOWS else POSIX_VENV_BIN).replace('.venv', venv, 1)
    return WORKSPACE_ROOT / bin_dir / (f'{name}.exe' if _WINDOWS else name)


def interpreter() -> str:
    """The Python that should run a script we spawn. Never `python3`: on Windows the bare word is a
    Store advert that exits 9009, a silent pass wearing a failure's coat. `sys.executable` is the
    venv's on every platform and needs no PATH."""
    return sys.executable


def session_state(name: str) -> Path:
    """A session-scoped scratch file — the markers a gate writes in one hook and reads in the next.

    WHY THE REPOSITORY AND NOT THE TEMP DIRECTORY. **A session outlives a reboot; the temp directory
    does not** (2026-09-22: a resumed session found its markers wiped and re-read its whole chain).
    `.gitignore` treats `core/` as an allowlist, so state stays out of git. A function, not a
    constant: six hooks once spelled `/tmp/...` by hand, which Windows aims at `C:\\tmp`.
    """
    folder = Path(os.environ.get('WOS_SESSION_STATE') or WORKSPACE_ROOT / 'core' / 'state')
    folder.mkdir(parents=True, exist_ok=True)
    return folder / name


def system_temp() -> Path:
    """The system temp directory, named here alone (never session state): tmpfs here, so it is RAM."""
    return Path(tempfile.gettempdir())


def scratch_root(tree: bool = False) -> Path:
    """Where temp that grows with its input lives, never the temp directory: tmpfs here, so a leak is
    RAM (4 GB of them starved every worker, 2026-11-27). A copied TREE goes to /var/tmp, native disk;
    a blob (video, archive) to the state folder, a FUSE disk with room but slow on small files. Under
    the suite WOS_SESSION_STATE holds both. session-prune.py deletes what a killed process left."""
    tree = tree and not _WINDOWS and not os.environ.get('WOS_SESSION_STATE')
    folder = Path('/var/tmp/wos') if tree else session_state('tmp')
    folder.mkdir(parents=True, exist_ok=True)
    return folder


@contextmanager
def scratch(prefix: str):
    """A folder under scratch_root() for the block, where every mkdtemp and child process inside it
    lands too (tempfile.tempdir, TMPDIR); deleted on the way out, whatever happened."""
    folder = tempfile.mkdtemp(prefix=prefix, dir=scratch_root())
    saved = tempfile.tempdir, os.environ.get('TMPDIR')
    tempfile.tempdir = os.environ['TMPDIR'] = folder
    try:
        yield Path(folder)
    finally:
        tempfile.tempdir = saved[0]
        os.environ.pop('TMPDIR') if saved[1] is None else os.environ.update(TMPDIR=saved[1])
        shutil.rmtree(folder, ignore_errors=True)


def install_command(directory, name: str, source: str) -> None:
    """Put python `source` in `directory` so the bare word `name` runs it once that dir is on PATH.
    The boundary's, because Windows has none of shebang, execute bit or extensionless lookup
    (CreateProcess resolves through PATHEXT): one question, two mechanisms."""
    directory = Path(directory)
    if not _WINDOWS:
        target = directory / name
        target.write_text(f'#!{sys.executable}\n{source}', encoding='utf-8', newline='\n')
        target.chmod(0o755)
        return
    (directory / f'{name}.py').write_text(source, encoding='utf-8', newline='\n')
    (directory / f'{name}.cmd').write_text(
        f'@echo off\r\n"{sys.executable}" "%~dp0{name}.py" %*\r\n', encoding='utf-8', newline='\n')


def package_install(name: str) -> list:
    """The command that installs a system package, whichever manager this machine actually has.

    `name` does not change: the boundary absorbs three managers so core/tools/deps.txt keeps one name
    per dependency. Windows pins `--source winget`: bare `winget install gh` is ambiguous against the
    msstore source and refuses, and the pin also skips the Store's interactive terms prompt.
    """
    if _WINDOWS:
        return ['winget', 'install', '--moniker', name, '--source', 'winget',
                '--accept-source-agreements', '--accept-package-agreements']
    if _DARWIN:
        return ['brew', 'install', name]
    return ['sudo', 'apt-get', 'install', '-y', name]


def posix(path) -> str:
    """`path` spelled the one way this workspace spells a path that has become DATA: a routing row,
    a registry key, an ISSUES.md line. A backslash on one machine and a slash on another make two
    workspaces that disagree about their own contents. `Path` is for touching disk; this is for text.
    """
    return Path(path).as_posix()


def rel(path, root=WORKSPACE_ROOT) -> str:
    """`path` relative to `root`, in that same vocabulary. Tolerant on purpose: a path already
    relative comes back unchanged, and one outside `root` comes back whole rather than raising."""
    target = Path(path)
    if not target.is_absolute():
        return target.as_posix()
    try:
        return target.relative_to(Path(root)).as_posix()
    except ValueError:
        return target.as_posix()


@cache
def real_git() -> str:
    """The git this machine installed, never the branch-lock wrapper in front of it on PATH
    (core/hooks/git/git): a candidate that IS the wrapper's file is skipped, so it never finds itself."""
    wrapper = WORKSPACE_ROOT / 'core/hooks/git/git'
    for folder in os.environ.get('PATH', '').split(os.pathsep):
        found = Path(folder) / ('git.exe' if _WINDOWS else 'git')
        if found.is_file() and os.access(found, os.X_OK) and not (wrapper.exists() and found.samefile(wrapper)):
            return str(found)
    return 'git'


def ancestors(pid: int = 0) -> list:
    """(pid, start, name) for `pid` (this process by default) and each parent up to init. The start
    time, in ticks since boot, tells a live process from a later one that reused its pid. Linux reads
    /proc; a machine without it answers [] — no process is then known to be an agent's."""
    found, pid = [], pid or os.getpid()
    while pid > 1:
        try:
            stat = Path(f'/proc/{pid}/stat').read_text(encoding='utf-8', errors='replace')
        except OSError:
            break
        fields = stat[stat.rindex(')') + 2:].split()   # the name may hold spaces and parentheses
        found.append((pid, fields[19], stat[stat.index('(') + 1:stat.rindex(')')]))
        pid = int(fields[1])
    return found


def is_repo(path) -> bool:
    """Whether `path` roots a git repo: `.git` is a FILE (worktree, submodule) or a dir holding HEAD.
    An EMPTY `.git` is not one — the Codex sandbox (bubblewrap) leaves those as mount points."""
    dot = Path(path) / '.git'
    return dot.is_file() or (dot / 'HEAD').is_file()


def _restrict(path: Path, posix_mode: int, windows_grant: str) -> None:
    """Owner-only access, by whatever mechanism this machine actually has. Not os.chmod everywhere:
    on Windows it accepts 0o600 and changes nothing, a false green on a secret. So ACLs there:
    break inheritance, grant the user alone. Raises: a secret written loose does not become safe."""
    if not _WINDOWS:
        # Already right means no write: a sandboxed worker (Codex) sees ~/.config read-only.
        if path.stat().st_mode & 0o777 != posix_mode:
            os.chmod(path, posix_mode)
        return
    user = os.environ.get('USERNAME') or Path.home().name
    done = subprocess.run(['icacls', str(path), '/inheritance:r',
                           '/grant:r', f'{user}:{windows_grant}', '/Q'],
                          capture_output=True, text=True, encoding='utf-8')
    if done.returncode != 0:
        raise OSError(f'could not restrict {path} to {user}: '
                      f'{done.stderr.strip() or done.stdout.strip()}')


def is_owner_only(path) -> bool:
    """Whether `path` is really readable by its owner alone — asked, not assumed. On Windows st_mode
    is synthesised from the read-only attribute and cannot fail, so the ACL is read back instead."""
    path = Path(path)
    if not _WINDOWS:
        return path.stat().st_mode & 0o077 == 0
    done = subprocess.run(['icacls', str(path)], capture_output=True, text=True, encoding='utf-8')
    if done.returncode != 0:
        return False
    user = (os.environ.get('USERNAME') or Path.home().name).lower()
    granted = set()
    for line in done.stdout.splitlines():   # "<path> PRINCIPAL:(perms)", then "  PRINCIPAL:(perms)"
        entry = line.replace(str(path), '', 1).strip()
        if entry and ':' in entry:
            granted.add(entry.rsplit(':', 1)[0].strip().split('\\')[-1].lower())
    return bool(granted) and granted <= {user}


def secure_dir(path) -> None:
    """A directory only its owner may enter — the 700 of SETUP-accounts.md, on either system."""
    _restrict(Path(path), 0o700, '(OI)(CI)F')


def secure_file(path) -> None:
    """A file only its owner may read — the 600 of SETUP-accounts.md, on either system."""
    _restrict(Path(path), 0o600, 'F')


@contextmanager
def locked(path):
    """Hold an exclusive lock on `path` for the block; the operating system releases it on death.

    The file is the lock's NAME and is never deleted: a process that deleted it would leave the
    next two holding locks on two different files. A crashed holder leaves nothing stale behind.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'a+b') as handle:
        if _WINDOWS:
            import msvcrt
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            if _WINDOWS:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)
