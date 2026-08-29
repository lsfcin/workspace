#!/usr/bin/env python3
# The platform seam: the one file in this workspace allowed to know what an operating system is.
#
# Sibling of file_law.py / schema_law.py / feature_law.py, and the same shape as all three: one
# module owns one question so the answer cannot drift. file_law says what a file IS, schema_law what
# a name MAY BE, feature_law what is ON, and this one what the machine underneath is.
#
# WHY A SEAM AND NOT A PER-OS FORK. Porting bash to Python is not adding a Windows implementation,
# it is removing the per-OS axis. The workspace already ran the experiment: it holds exactly three
# per-OS forks and all three are broken — start-session.ps1 prints a WORKSPACE.md that does not
# exist, .agentrc.json points at that broken file, and caveman's activate.js names a statusline
# script absent from the repo. Three of three is not luck, it is the failure mode. So the rule is
# not "branch carefully", it is `sys.platform` appears HERE and nowhere else, and a ratchet in
# core/tools/test/workspace/test_corpus_ratchet.py holds the count at zero everywhere else.
#
# ONLY WHAT HAS A CALLER. `.venv/bin` vs `.venv/Scripts`, the package manager and the link strategy
# belong to this seam and have no caller yet — they arrive with the de-bash work that needs them. An
# API written before its call site is a guess that later readers mistake for a decision.
#
# `interpreter()` was cut on that rule and put back the same session, which is worth recording: its
# ~20 callers are SPAWN sites, not imports, so a search for uses found none. A seam function can be
# load-bearing without any module naming it.
import os
import subprocess
import sys
import tempfile
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]

# The one place a platform question is answered by name. Every other module asks a function here.
_WINDOWS = sys.platform == 'win32'
_DARWIN = sys.platform == 'darwin'


def interpreter() -> str:
    """The Python that should run a script we spawn.

    `python3` is not a name Windows has. The bare word reaches an App Execution Alias that prints an
    advert for the Microsoft Store and exits 9009, so a gate spawned that way never runs at all and
    the caller reads the advert as the gate's own output -- a silent pass wearing a failure's coat.
    `sys.executable` is the interpreter already running, which is the venv's on every platform, and
    it needs no PATH to be right.
    """
    return sys.executable


def session_state(name: str) -> Path:
    """A session-scoped scratch file — the markers a gate writes in one hook and reads in the next.

    WHY THIS IS A SEAM QUESTION AND NOT A CONSTANT. Six hooks spelled `/tmp/claude_<x>_<sid>.txt`
    by hand. `/tmp` is not a directory Windows has: Python anchors a leading slash to the current
    drive, so every one of those writes aimed at `C:\\tmp`, which does not exist. The write raised
    inside a PostToolUse hook, whose exit status nothing reads, and the matching read then found
    nothing — so the context gate could never be satisfied by reading anything, and no message
    anywhere said why. A gate that can only ever block is the mirror of one that can only ever
    pass, and it cost this session a deadlock against its own enforcement layer to find.

    `tempfile.gettempdir()` is the same directory `/tmp` names on POSIX, so the markers do not move
    there, and it is what Git Bash already maps `/tmp` to here -- which is what keeps the shell
    halves that still spell `/tmp` (read/pre-read.sh, session/precompact-wipe.sh) agreeing with
    these until they are ported.
    """
    return Path(tempfile.gettempdir()) / name


def install_command(directory, name: str, source: str) -> None:
    """Put python `source` in `directory` so the bare word `name` runs it once that dir is on PATH.

    WHY THIS IS THE SEAM'S AND NOT THE CALLER'S. Faking a binary is POSIX muscle memory — write a
    file, give it a shebang, chmod +x — and none of the three mechanisms exists on Windows: the
    execute bit is not a permission there, a shebang is inert, and CreateProcess resolves a bare
    name only through PATHEXT, so an extensionless file is not findable at all. The caller does not
    want a shebang; it wants `name` to run. That is one question with two mechanisms, which is
    exactly what this module is for.
    """
    directory = Path(directory)
    if not _WINDOWS:
        target = directory / name
        target.write_text(f'#!{sys.executable}\n{source}', encoding='utf-8')
        target.chmod(0o755)
        return
    (directory / f'{name}.py').write_text(source, encoding='utf-8')
    (directory / f'{name}.cmd').write_text(
        f'@echo off\r\n"{sys.executable}" "%~dp0{name}.py" %*\r\n', encoding='utf-8')


def package_install(name: str) -> list:
    """The command that installs a system package, whichever manager this machine actually has.

    THE POINT IS THAT `name` DOES NOT CHANGE. core/tools/deps.txt says a dependency's name is spelled
    "exactly as the install command spells it" -- a contract that was only ever true because one kind
    of machine had read the file. Three managers, three spellings, and the row would have to fork.
    So the seam absorbs the difference and the registry keeps one name per dependency.

    WHY THE WINDOWS ARM PINS ITS SOURCE. `winget install gh` is ambiguous and refuses: the msstore
    source offers unrelated apps matching those letters, and winget exits asking the caller to refine
    rather than installing anything. Pinning --source winget makes the moniker exact -- verified
    against the live index, not assumed -- and it also skips the Store's terms prompt, which is
    interactive and would hang a non-interactive install.
    """
    if _WINDOWS:
        return ['winget', 'install', '--moniker', name, '--source', 'winget',
                '--accept-source-agreements', '--accept-package-agreements']
    if _DARWIN:
        return ['brew', 'install', name]
    return ['sudo', 'apt-get', 'install', '-y', name]


def posix(path) -> str:
    """`path` spelled the one way this workspace spells a path that has become DATA.

    pathlib solved the filesystem; it did not solve the vocabulary. A routing table row, a registry
    key, an ISSUES.md line and a comparison against features.txt are all text, and text spelled with
    a backslash on one machine and a slash on another makes two workspaces that disagree about their
    own contents. `Path` is for touching disk; this is for everything a path is written into.

    Not a concession to any one system: it is what makes the routing table and the entropy dashboard
    byte-identical across machines, which test_the_output_is_deterministic already demands and today
    passes only because every machine that has run it was the same kind.
    """
    return Path(path).as_posix()


def rel(path, root=WORKSPACE_ROOT) -> str:
    """`path` relative to `root`, in that same vocabulary, whatever shape it arrived in.

    Tolerant on purpose, because every call site this replaced was: a path already relative comes
    back unchanged, and one outside `root` comes back whole rather than raising. The scatter's
    finding heads arrive both ways, and a spelling fix that introduced a new exception would be a
    worse bug than the one it closed.
    """
    target = Path(path)
    if not target.is_absolute():
        return target.as_posix()
    try:
        return target.relative_to(Path(root)).as_posix()
    except ValueError:
        return target.as_posix()


def _restrict(path: Path, posix_mode: int, windows_grant: str) -> None:
    """Owner-only access, by whatever mechanism this machine actually has.

    WHY THIS IS NOT os.chmod EVERYWHERE. On Windows os.chmod only toggles the read-only attribute;
    it accepts 0o600, returns cleanly, and changes nothing about who can read the file. That is a
    false green, and a false green on a secret is worse than no call at all — the caller is told the
    thing is protected. Windows has no POSIX mode, it has ACLs, so the Windows arm breaks inherited
    permissions and grants the current user alone.

    Raises rather than warning. A secret written loose does not become safe later, so the caller
    that cannot protect a file needs to hear about it before it writes one.
    """
    if not _WINDOWS:
        os.chmod(path, posix_mode)
        return
    user = os.environ.get('USERNAME') or Path.home().name
    done = subprocess.run(['icacls', str(path), '/inheritance:r',
                           '/grant:r', f'{user}:{windows_grant}', '/Q'],
                          capture_output=True, text=True)
    if done.returncode != 0:
        raise OSError(f'could not restrict {path} to {user}: '
                      f'{done.stderr.strip() or done.stdout.strip()}')


def is_owner_only(path) -> bool:
    """Whether `path` is really readable by its owner alone — asked, not assumed.

    `st_mode & 0o077 == 0` is a POSIX question. On Windows st_mode is synthesised from the
    read-only attribute, so it answers the same for a file one user may read and for one the whole
    machine may — and a check that cannot fail is the worst thing to point at a secret. Read the
    ACL back instead.
    """
    path = Path(path)
    if not _WINDOWS:
        return path.stat().st_mode & 0o077 == 0
    done = subprocess.run(['icacls', str(path)], capture_output=True, text=True)
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
