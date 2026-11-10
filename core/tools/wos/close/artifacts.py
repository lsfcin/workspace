#!/usr/bin/env python3
# The generated artifacts a session close regenerates, and what happens to each one afterwards.
#
# Imported by core/tools/wos/roundup. It was `artifacts.sh`, SOURCED — a fragment that could only
# work because it shared the caller's shell variables, so running it any other way silently did
# nothing. Here the caller passes what each function needs and the coupling is in the signature.
#
# Every artifact follows one rule: regenerate, then commit it by path, whatever else the tree holds.
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

WOS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WOS.parents[1] / 'hooks/routing'))
sys.path.insert(0, str(WOS.parents[1] / 'hooks'))
from blocks import markers, replace_block  # noqa: E402
from platform_law import interpreter  # noqa: E402

DASHBOARD = 'core/hooks/entropy/dashboard/entropy-dashboard.py'
CLOSE_WRITES = ('ARCHITECTURE.html', 'core/read-matrix.tsv', 'ISSUES.md', 'PROJECTS.md')
MIXED = ('ISSUES.md', 'PROJECTS.md')   # generated blocks beside hand-written text
BLOCK = re.compile(r'<!-- (\w+):start -->.*?<!-- \1:end -->', re.DOTALL)
INBOX, BOT_SIGNATURE = 'brain/INBOX.md', '— via aiwbot'


def git(repo, *args) -> subprocess.CompletedProcess:
    return subprocess.run(['git', *args], cwd=repo, capture_output=True, text=True,
                          encoding='utf-8', errors='replace')


def out(repo, *args) -> str:
    """What git said, or nothing. Four callers had a private copy of these two lines.

    It answers "" for a command that FAILED as well as for one that said nothing, which is
    load-bearing where the question has no answer and fatal where it does — the reason six
    projects went 22 commits unpushed. Ask the returncode when the difference matters.
    """
    done = git(repo, *args)
    return done.stdout.strip() if done.returncode == 0 else ''


def spawn(root, *command) -> subprocess.CompletedProcess:
    """A child of the close: stdin closed, and no bytecode written.

    STDIN, because a child that inherits an interactive one waits there instead of failing, and a
    close that can HANG is worse than one that can go red — nothing reports a hang. BYTECODE,
    because these children import from the tree the close is about to inspect for uncommitted work:
    the dashboard alone leaves a __pycache__ beside the block writer it loads, and a tool that
    judges a tree may not dirty it first.
    """
    return subprocess.run(command, cwd=root, capture_output=True, text=True,
                          encoding='utf-8', errors='replace', stdin=subprocess.DEVNULL,
                          env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})


def hand_edited(repo, name: str) -> bool:
    """Whether a file holding generated blocks differs from HEAD OUTSIDE those blocks."""
    head = git(repo, 'show', f'HEAD:{name}')
    if name not in MIXED or head.returncode:
        return False
    now = (Path(repo) / name).read_text(encoding='utf-8', errors='replace')
    return BLOCK.sub('', head.stdout).split() != BLOCK.sub('', now).split()   # a new block moves blank lines


def dirt(repo) -> list:
    """Uncommitted paths the close cannot settle itself — what someone still has to answer for.

    NUL-delimited, so a rename or a path with spaces is one entry, and every untracked file is
    named rather than its directory. A status that fails raises: it is never a clean tree.
    """
    done = git(repo, 'status', '--porcelain', '-z', '--untracked-files=all')
    if done.returncode != 0:
        raise RuntimeError(f'git status failed in {repo}: {done.stderr.strip()}')
    fields, names = iter(done.stdout.split('\0')), []
    for field in fields:
        if field:
            names.append(field[3:])
            if field[0] in 'RC':
                next(fields, None)   # a rename's old path follows its new one
    return [name for name in names if name not in CLOSE_WRITES or hand_edited(repo, name)]


def commit_captures(root) -> None:
    """Commit brain/INBOX.md when all it holds is what the chat bot appended.

    Added lines alone prove nothing — a session may be drafting an entry — so every added
    paragraph must end in the bot's own signature, and one removed line disqualifies the file.
    """
    lines = git(root, 'diff', 'HEAD', '-U0', '--', INBOX).stdout.splitlines()
    added = [l[1:] for l in lines if l.startswith('+') and not l.startswith('+++')]
    if any(l.startswith('-') and not l.startswith('---') for l in lines) or not added:
        return
    entries = [e.strip().splitlines() for e in '\n'.join(added).split('\n\n') if e.strip()]
    if all(entry[-1].startswith(BOT_SIGNATURE) for entry in entries):
        settle(root, INBOX, 'chore(inbox): captures from the chat bot')


def settle(repo, name: str, message: str) -> str:
    """Commit one artifact BY PATH; the suffix its caller appends to a status line.

    Silent and empty when the artifact did not move, which is the common case and the point:
    deterministic output means a file changes when the WORKSPACE changed, never merely because a
    generator ran. `--only` is what makes this safe over someone else's staged work, and is why
    nothing is ever rolled back: a rollback only applied to a clean file, so an artifact already
    dirty stayed dirty and blocked the next close (2026-11-09).
    """
    tracked = git(repo, 'ls-files', '--error-unmatch', name).returncode == 0
    if tracked and git(repo, 'diff', '--quiet', 'HEAD', '--', name).returncode == 0:
        return ''
    if hand_edited(repo, name):
        return f' · not committed: {name} has hand edits'
    if (git(repo, 'add', name).returncode
            or git(repo, 'commit', '-q', '--only', '-m', message, '--', name).returncode):
        return f' · commit failed, {name} left dirty'
    return ''


def write_block(target: Path, name: str, body: str) -> None:
    """One generated block, rewritten in place, its neighbours untouched.

    Imported rather than shelled out to. The bash piped into `python3 blocks.py`, which is both a
    second process and the bare word this port exists to remove — and it meant the close could only
    write a block on a machine where that name resolved to the right interpreter.
    """
    start, end = markers(name)
    text = target.read_text(encoding='utf-8') if target.exists() else ''
    block = '\n'.join((start, body.strip(), end))
    target.write_text(replace_block(text, block, start, end), encoding='utf-8', newline='\n')


def verify_block(target: Path, label: str, verdict: str, log: str) -> None:
    """The verification result, into ISSUES.md beside the entropy findings.

    A red suite and a drift finding are both answers to "what is currently untrue that we know
    about" (core/SCHEMA.md § The `.md` type system). This is the only thing that may write it: the
    suite already ran, and re-running it to report it would double the one cost the pre-commit gate
    exists to keep small.
    """
    body = ['## Verification', '',
            '> Generated by `core/tools/wos/roundup` at session close. The suite is the authority; '
            'this is its last result, never a claim that it is still true.', '',
            f'{date.today().isoformat()} · `{label}` · **{verdict}**']
    if verdict == 'red':
        body += ['', '```', '\n'.join(log.splitlines()[-20:]), '```']
    write_block(target, 'verify', '\n'.join(body))


def regenerate(root: Path, promoting: str = '') -> tuple:
    """(entropy, diagram) — both rewritten, then settled.

    `promoting` comes from the CALLER for the same shape of reason: this close runs the dashboard
    BEFORE it merges, so without a name the block published a finding against the close's own
    branch every single time. Only roundup holds the three facts that decide whether the merge
    happens — the verify verdict, --no-promote, and whether the repo is in gitflow scope — so it
    passes the name and this step only relays it. branch_debt.unmerged_branches carries the rest.
    """
    dashboard = [interpreter(), str(root / DASHBOARD)]
    if promoting:
        dashboard += ['--promoting', promoting]
    if spawn(root, *dashboard).returncode == 0:
        # The count AND how it moved are both read out of the header the dashboard just wrote.
        # roundup used to compute a second delta of its own, against the session immediately
        # before it — which is how "flat" got written into hand-off after hand-off while the real
        # number climbed 95 → 645. Matched to the closing stars: a pattern anchored on
        # "findings**" printed no entropy line at all (fixed 2026-08-25).
        found = re.search(r'\*\*(\d+ findings[^*]*)\*\*( \([^)]*\))?',
                          (root / 'ISSUES.md').read_text(encoding='utf-8', errors='replace'))
        entropy = (found.group(1) + (found.group(2) or '')) if found else ''
    else:
        entropy = 'regen failed'
    entropy += settle(root, 'ISSUES.md', 'chore(issues): regenerate the entropy and verify '
                      'blocks at session close')

    # THE MATRIX IS FOLDED BEFORE THE DIAGRAM, and the order is the whole answer to what looked like
    # a conflict: the page must be a pure function of the repository, and a per-session number is
    # not. Folded into a tracked file first, it becomes one — so the picture may read it and
    # `architecture --check` still means what it meant. The hook only appends; this is the one
    # place the matrix is written, which is what keeps parallel sessions from losing rows in it.
    # BOTH PATHS COME FROM `root`, never from the module's own defaults: a fold that defaulted to
    # WORKSPACE_ROOT would write the REAL matrix from inside a throwaway repo — the b20260902 shape,
    # a test dirtying a tree it does not own. The guard is what makes the import safe to reach at
    # all: this file is copied into sandboxes carrying only part of core/hooks/, and a sandbox has
    # neither events nor a matrix, so there nothing runs and nothing is imported.
    events, matrix = root / 'core/reads.tsv', root / 'core/read-matrix.tsv'
    if events.exists() or matrix.exists():
        sys.path.insert(0, str(WOS.parents[1] / 'hooks/read'))
        import read_matrix
        read_matrix.fold(events, matrix)
        settle(root, 'core/read-matrix.tsv', 'chore(reads): fold this session\'s reads into the matrix')

    drawn = spawn(root, interpreter(), str(WOS / 'diagram/architecture'))
    text = drawn.stdout + drawn.stderr
    if drawn.returncode == 0:
        hit = [line for line in text.splitlines() if 'routing blocks' in line]
        diagram = hit[0].strip() if hit else ''
    else:
        diagram = f'regen incomplete · {text.count("UNPARSED")} unparsed routing block(s)'
    return entropy, diagram + settle(root, 'ARCHITECTURE.html',
                                     'chore(diagram): regenerate at session close')
