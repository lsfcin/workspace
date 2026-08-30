# T0 the OS-agnostic port's invariants (AD-0): the tree may not re-acquire the defects the port
# removed. Zero-token, runs in verify-fast.
#
# Split out of test_corpus_ratchet.py on 2026-08-29, which had carried these since the port began
# and said so: "they live here rather than in a file of their own ... they assert something about
# the WHOLE TREE". That reason was right about the DIRECTORY and wrong about the file. Being
# whole-tree is what puts both halves in workspace/; it is not what makes them one question. The
# corpus half asks whether the .md backlog is shrinking, this half asks whether the port is
# holding, and a file that answers two questions hits the line cap with neither of them finished.
#
# Every ceiling only ever goes down, and a ceiling of zero IS an assert. One ceiling per defect,
# never one shared: a shared number lets one defect grow while another shrinks and reports calm.
#
# I5 -- one branch, one codebase -- is deliberately absent. It is not a property of any file, and a
# test pretending to check it would be the weaker kind this workspace names. AD-9's law (no text
# read or write inheriting the OS encoding) is owed: the corpus is clean, but an exact check needs
# the ast walk the codemod used, and that belongs with the pre-commit pipeline being ported next.
from conftest import git_lines as _git

MACHINE_PATH_CEILING = 44         # `mnt/workspace` hardcoded in a versioned file; S6 drives it to 0
VENV_POSIX_CEILING = 19           # `.venv/bin`, which is `.venv/Scripts` elsewhere; S6 drives it to 0

# Neither reaches 0 by editing prose. What is left of the venv count is mostly SPECS text that
# EXPLAINS the two layouts, plus core/tools/deps.txt spelling the directory once per probe row --
# the one that is still a live defect. A ratchet that counts a sentence describing the defect the
# same as the defect will be gamed by rewording, so lower these by removing call sites, and expect
# a floor somewhere above zero made of the documents that have to name both spellings.

SEAM = 'core/hooks/platform_law.py'

# The venv seam, and exempt from the venv ceiling for the reason platform_law.py is exempt from the
# sys.platform one: naming both layouts is this file's entire job. A hooks config is data, read
# before any of our code runs, so it cannot ask a Python function which interpreter to use -- the
# launcher is where that question gets answered once for every harness shim in the tree, and since
# 2026-08-29 for every tool as well, which is why it sits in core/ rather than core/hooks/.
LAUNCHER = 'core/run'


def test_no_per_os_script_sits_beside_the_python():                                          # I1
    forks = _git('ls-files', '*.ps1', '*.bat', '*.cmd')
    assert not forks, (
        f'per-OS script forks are back: {forks}. Porting bash to Python removes the per-OS axis, '
        'it does not add a Windows arm -- all three forks this workspace ever had were broken by '
        f'the time the port found them. A platform difference goes in {SEAM}')


def test_only_the_seam_knows_what_an_os_is():                                                # I2
    knowing = sorted({f for f in _git('grep', '-lF', 'sys.platform', '--')
                      + _git('grep', '-lF', 'platform.system', '--') if f != SEAM})
    assert not knowing, (
        f'these name an operating system outside the seam: {knowing}. Ask {SEAM} instead, and '
        'add the answer there if it does not have one yet')


def test_a_path_that_becomes_data_is_spelled_by_the_seam():                                  # AD-8
    hand_rolled = sorted({f for f in _git('grep', '-l', 'str(.*relative_to', '--')
                          if f != SEAM})
    assert not hand_rolled, (
        f'these spell a relative path by hand: {hand_rolled}. str() of a relative_to hands back a '
        f'backslash on one machine and a slash on another; {SEAM} rel() is the one spelling')


def test_no_setup_shard_is_named_for_an_operating_system():                                  # I3
    shards = [f for f in _git('ls-files', 'SETUP-*.md')
              if any(name in f.lower() for name in ('windows', 'linux', 'macos', 'darwin'))]
    assert not shards, (
        f'SETUP shards are per FEATURE, never per OS: {shards}. A shard named for a system '
        'declares that system the exception and another the default')


def test_a_machine_path_does_not_spread():                                                   # I6
    live = len(_git('grep', '-lF', 'mnt/workspace', '--'))
    assert live <= MACHINE_PATH_CEILING, (
        f'{live} versioned files hardcode one machine path, up from {MACHINE_PATH_CEILING}. '
        'Resolve the root at run time -- every tool here already does')


def test_a_posix_only_venv_path_does_not_spread():                                           # I6
    live = len([f for f in _git('grep', '-lF', '.venv/bin', '--') if f != LAUNCHER])
    assert live <= VENV_POSIX_CEILING, (
        f'{live} versioned files name .venv/bin, up from {VENV_POSIX_CEILING}. That directory is '
        f'.venv/Scripts on Windows, and {SEAM} owns the difference')


def test_no_shell_hook_spawns_the_bare_word_python3():                                       # I6
    """Zero, not a ceiling — this one has been found three times by accident.

    `python3` is not a name Windows has: it reaches a Microsoft Store execution alias that prints
    an advert and exits without running anything. Every site that spelled it sat behind
    `2>/dev/null` or `|| exit 0`, so the failure was *green*. On 2026-08-29 that was true of
    post-edit.sh and all four stages it sources, read/pre-read.sh and session/precompact-wipe.sh —
    interface stubs, routing sync, lint, reminders and the interface-first gate had never once run
    on a Windows clone, and nothing anywhere said so.

    A ceiling would be the wrong shape. A hook that can only ever pass is indistinguishable from
    one that works, so the count may not creep by one; `core/run` answers the interpreter question
    and `core/run --python` covers the inline `-c` case that cannot go through it.
    """
    hits = _git('grep', '-nE', r'(^|[^/[:alnum:]._-])python3\b', '--', '*.sh')
    # A comment may name the word — this file's own history is written in them. Only a line that
    # would RUN it counts, so drop anything whose first non-blank character is `#`.
    live = sorted({line.split(':', 1)[0] for line in hits
                   if not line.split(':', 2)[-1].lstrip().startswith('#')})
    assert not live, (
        f'these shell files spawn the bare word python3: {live}. It resolves to a Store alias on '
        'Windows and fails green. Use `sh "$RUN" <core-relative path>`, or '
        '`"$(sh "$RUN" --python)" -c ...` for an inline script')


def test_no_document_teaches_a_tool_call_that_cannot_run():                                  # I6
    """A `core/tools/...` in COMMAND position is a call the reader will copy, and it fails.

    This is the standing cost of the prefix decision (S5): `core/run tools/web/search` is longer
    than `core/tools/web/search`, and the shorter spelling is the one a hand reaches for. Nothing
    else can catch it — the file exists, so every link checker and path resolver is happy; it
    simply has no shebang and no execute bit, because `core/run` is what starts it now.

    Scoped to the text that TEACHES. core/experiments/ is excluded on purpose: those files record
    a command that really was run on a date, and editing one to a spelling nobody used would
    falsify the record rather than fix anything.
    """
    hits = _git('grep', '-nE', r'^[[:space:]]*core/tools/[a-z]', '--',
                '*.md', ':!core/experiments/**', ':!.craft/**')
    live = sorted({line.split(':', 1)[0] for line in hits})
    assert not live, (
        f'these documents show a tool call in command position: {live}. Spell it '
        '`core/run tools/<family>/<leaf>` — the bare path has no shebang and will not run')
