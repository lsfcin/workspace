# T0 corpus ratchets (core/SCHEMA.md § Placement): the .md corpus may not accumulate more of the three
# defects no link-checker can see. Zero-token, runs in verify-fast.
#
# These sit here rather than beside the checks they call because they assert something
# about the WHOLE TREE, not about one piece of machinery: test_entropy_ledger.py and
# test_entropy_context.py own whether each check fires correctly, this owns whether the
# backlog is shrinking. Same split as test_pointer_integrity.py beside it.
#
# Every ceiling only ever goes down. Each is paired with a staleness test, because a ratchet
# nobody lowers is just a baseline, and a baseline is where drift hides.
#
# A ceiling per defect, never one shared ceiling: until 2026-08-15 the placeholder marker was
# counted as finished-work prose, and 70 markers could have masked 70 new corpses without the
# number moving. One ratchet per thing the report names.
import entropy_context
import entropy_ledger
from conftest import WORKSPACE_ROOT
from file_law import load_limits

HEAD_WARN = load_limits()['CONTEXT_HEAD_WARN']

# Inherited backlog: corpses and trapped heads (core/SCHEMA.md § Placement) plus generator markers.
# The wos half of the corpse and head queues is drained; what remains in both is nested-repo
# work, which cannot ride a wos commit — so these two stop falling here.
#
# The marker queue fell 69 → 55 on 2026-08-15 without a single file being described by hand:
# the generator learned to read a multi-line module docstring and the `core/hooks` data files
# (core/hooks/SPECS.md § The `CONTEXT.md` routing block). Markers answered by closing a
# generator gap are the cheapest kind, and they are indistinguishable here from ones answered
# by writing prose — which is the point.
FINISHED_CEILING = 0
UNDESCRIBED_CEILING = 3
MISPLACED_CEILING = 1

# The margin lets one cut land without forcing a test edit; a real drain pass trips it.
FINISHED_SLACK = 10
UNDESCRIBED_SLACK = 10
MISPLACED_SLACK = 5


def _files() -> list:
    return entropy_ledger.tracked_files(WORKSPACE_ROOT, nested=True)


def _finished() -> int:
    return len(entropy_ledger.finished_work_hits(
        _files(), entropy_ledger.enforcement_paths(WORKSPACE_ROOT)))


def _undescribed() -> int:
    return len(entropy_ledger.unanswered_placeholders(
        _files(), entropy_ledger.enforcement_paths(WORKSPACE_ROOT)))


def _misplaced() -> int:
    return sum(1 for path in _files()
               if entropy_context.check_misplaced_answer(path, HEAD_WARN))


def test_prose_describing_finished_work_does_not_grow():
    live = _finished()
    assert live <= FINISHED_CEILING, (
        f'{live} corpses, up from {FINISHED_CEILING}. Cut the prose describing work that '
        f'landed, or rewrite it as present-tense state — ISSUES.md § Prose describing '
        f'finished work')


def test_unanswered_placeholders_do_not_grow():
    live = _undescribed()
    assert live <= UNDESCRIBED_CEILING, (
        f'{live} CONTEXT.md carrying an unanswered placeholder, up from '
        f'{UNDESCRIBED_CEILING}. Answer it at the source — the described file\'s '
        f'first-line comment — never by deleting the marker (core/hooks/SPECS.md)')


def test_constraints_in_context_heads_do_not_grow():
    live = _misplaced()
    assert live <= MISPLACED_CEILING, (
        f'{live} constrained heads, up from {MISPLACED_CEILING}. CONTEXT.md is the only '
        f'enforced-read type — move the contract to a sibling SPECS.md and leave one '
        f'pointer (core/SCHEMA.md § Placement)')


def test_the_ceilings_are_not_stale():
    finished, undescribed, misplaced = _finished(), _undescribed(), _misplaced()
    assert FINISHED_CEILING - finished <= FINISHED_SLACK, (
        f'finished-work is down to {finished} — lower FINISHED_CEILING to match, so the '
        f'ratchet keeps holding the new ground')
    assert UNDESCRIBED_CEILING - undescribed <= UNDESCRIBED_SLACK, (
        f'placeholders are down to {undescribed} — lower UNDESCRIBED_CEILING to match')
    assert MISPLACED_CEILING - misplaced <= MISPLACED_SLACK, (
        f'misplaced is down to {misplaced} — lower MISPLACED_CEILING to match')


# ---------------------------------------------------------------------------------------------
# The OS-agnostic port's invariants (AD-0). They live here rather than in a file of their own for
# the reason this file already gives: they assert something about the WHOLE TREE, and a ratchet
# whose ceiling is zero IS an assert. One ceiling per defect, never one shared.
#
# I5 -- one branch, one codebase -- is deliberately absent. It is not a property of any file, and a
# test pretending to check it would be the weaker kind this workspace names. AD-9's law (no text
# read or write inheriting the OS encoding) is owed: the corpus is clean, but an exact check needs
# the ast walk the codemod used, and that belongs with the pre-commit pipeline being ported next.
MACHINE_PATH_CEILING = 105        # `mnt/workspace` hardcoded in a versioned file; S5 drives it to 0
VENV_POSIX_CEILING = 72           # `.venv/bin`, which is `.venv/Scripts` elsewhere; S4 drives it to 0

SEAM = 'core/hooks/platform_law.py'

# The venv seam, and exempt from the venv ceiling for the reason platform_law.py is exempt from the
# sys.platform one: naming both layouts is this file's entire job. A hooks config is data, read
# before any of our code runs, so it cannot ask a Python function which interpreter to use -- the
# launcher is where that question gets answered once for every harness shim in the tree.
LAUNCHER = 'core/hooks/run'


def _git(*args) -> list:
    """Lines of a git query, minus this file -- a ratchet necessarily names what it forbids."""
    import subprocess
    done = subprocess.run(['git', *args], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
    return [line for line in done.stdout.splitlines()
            if line and 'test_corpus_ratchet' not in line]


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
