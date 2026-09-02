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
# test pretending to check it would be the weaker kind this workspace names.
#
# The encoding law is no longer owed: it is held next door by test_encoding_ratchet.py, which is
# also where it is now WRITTEN, because the "AD-9" this file used to cite named no section that
# existed. It was owed here with the guess "the corpus is clean". It was not -- the ast walk found
# 304 inheriting call sites in 113 files the first time one was pointed at the tree, and two of them
# were failing this suite on a Windows clone while reading as an unrelated TypeError.
from conftest import git_lines as _git
from platform_law import AUTHORING_ROOT, POSIX_VENV_BIN

SEAM = 'core/hooks/platform_law.py'

# THE NEEDLES COME FROM THE SEAM, WHICH IS WHY THESE ARE NUMBERS AND NOT BUDGETS (2026-08-30).
#
# Both counts used to sit at 44 and 19 with a comment predicting "a floor somewhere above zero made
# of the documents that have to name both spellings". That floor was not a fact about the problem,
# it was the shape of the answer: platform_law.py branched on these two strings without EXPORTING
# them, so every consumer re-spelled the literal -- deps.txt in 17 probe rows, wos/deps,
# wos/permissions, and these tests. The ceilings were counting that duplication.
#
# The seam publishes its data now, the consumers ask, and what is left is one file each:
MACHINE_PATH_CEILING = 1   # the seam, which names the authoring root so a checker can search for it
VENV_POSIX_CEILING = 1     # core/run, below -- and it is a paradox, not an exemption

# A ceiling of one with a named holder is a law; a ceiling of nineteen is an allowance a real defect
# can hide inside. If either number has to rise, the thing to write down is WHY that file cannot
# ask, not a bigger number.
#
# RECORDS ARE EXCLUDED BY RULE, ONCE. test_no_document_teaches_a_tool_call_that_cannot_run already
# dropped core/experiments/ and .craft/ because "editing one to a spelling nobody used would falsify
# the record rather than fix anything". Its two siblings did not, which made the same file a finding
# for one question and exempt for another -- the asymmetry was the bug, not the paths.
#
# A record is anything whose value is that it says what WAS true: an experiment's log, a craft
# loop file, a captured page, and brain/, which is Lucas's own capture and journal. `academy/**.html`
# is a page saved from the university's site — not ours to rewrite at all.
RECORDS = (':!core/experiments/**', ':!.craft/**', ':!*.log', ':!brain/**', ':!academy/**/*.html')

# The venv seam, and exempt from the venv ceiling for the reason platform_law.py is exempt from the
# sys.platform one: naming both layouts is this file's entire job. A hooks config is data, read
# before any of our code runs, so it cannot ask a Python function which interpreter to use -- the
# launcher is where that question gets answered once for every harness shim in the tree, and since
# 2026-08-29 for every tool as well, which is why it sits in core/ rather than core/hooks/.
LAUNCHER = 'core/run'


# THE SHELL THAT MAY STAY IN THE ENFORCEMENT LAYER, named one by one. The bash ban was scoped to
# core/tools/ (test_b20260901_a_bash_tool_costs...), leaving the hooks — the hot path, where a fork
# costs ~50x more under Git Bash than here — with no ratchet at all. Two of them were still spelling
# `/tmp` by hand on a mount claim nothing could check: that is what an unratcheted debt looks like.
#
# Two reasons earn a place, and neither is "it works": SPAWNED BY NAME by something outside this
# workspace (git, .claude/settings.json, a harness), or SOURCED as a fragment into post-edit.sh,
# sharing its shell state. An equality assert, not a subset — a NEW shell fails, and so does a
# REMOVED one, because a name that has been paid off leaves the list instead of sitting in it.
SHELL_ALLOWED = {
    'core/hooks/post-edit.sh',                  # name dictated by .claude/settings.json
    'core/hooks/postedit/interfaces.sh',        # sourced fragment
    'core/hooks/postedit/lint.sh',              # sourced fragment
    'core/hooks/postedit/reminders.sh',         # sourced fragment
    'core/hooks/postedit/sync.sh',              # sourced fragment
    'core/hooks/session/start-session.sh',      # neutral entrypoint, spawned by name
    'core/hooks/copilot/copilot-agent.sh',      # provider shim entrypoint
    'core/hooks/zcode/probe.sh',                # hook-protocol probe, run by hand
    'core/hooks/zcode/probe-deny.sh',           # hook-protocol probe, run by hand
}


def test_the_enforcement_layer_holds_no_unearned_shell():                                    # I1
    live = set(_git('ls-files', 'core/hooks/*.sh', 'core/hooks/**/*.sh'))
    assert live == SHELL_ALLOWED, (
        f'added: {sorted(live - SHELL_ALLOWED)}; paid off: {sorted(SHELL_ALLOWED - live)}. Shell in '
        'a hook costs a fork per call and cannot import the law modules, so it re-spells what they '
        'own. Port it, or say in SHELL_ALLOWED which of the two reasons it meets')


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
    live = _git('grep', '-lF', AUTHORING_ROOT.lstrip('/'), '--', *RECORDS)
    assert len(live) <= MACHINE_PATH_CEILING, (
        f'{len(live)} versioned files hardcode the authoring machine\'s root, over '
        f'{MACHINE_PATH_CEILING}: {live}. Resolve the root at run time -- every tool here already '
        f'does -- or ask {SEAM} for the string if you must name it')


def test_a_posix_only_venv_path_does_not_spread():                                           # I6
    live = [f for f in _git('grep', '-lF', POSIX_VENV_BIN, '--', *RECORDS) if f != SEAM]
    assert len(live) <= VENV_POSIX_CEILING, (
        f'{len(live)} versioned files name the POSIX venv bin directory, over '
        f'{VENV_POSIX_CEILING}: {live}. It is {SEAM}\'s WINDOWS_VENV_BIN elsewhere -- ask '
        '`venv_script(name)` for a console script, or the two constants if you need both names')


def test_the_launcher_is_the_only_thing_that_cannot_ask():
    """The one file left naming the venv layout, and why it can never be zero.

    `core/run` is `sh`, and its whole job is to find the interpreter. It cannot import
    platform_law to learn where the interpreter lives, because importing anything requires the
    interpreter it exists to find. That is a bootstrap paradox, not an exemption granted to a file
    somebody did not want to fix -- and it is worth one test of its own, because the honest floor
    of a ratchet is a claim that should fail loudly if it stops being true.
    """
    live = [f for f in _git('grep', '-lF', POSIX_VENV_BIN, '--', *RECORDS) if f != SEAM]
    assert live == [LAUNCHER], (
        f'expected the launcher alone to name the venv layout, found {live}. If a NEW file needs '
        f'it, it almost certainly wants {SEAM}.venv_script() instead')


def test_no_shell_hook_spawns_the_bare_word_python3():                                       # I6
    """Zero, not a ceiling — this one has been found three times by accident.

    `python3` is not a name Windows has: it reaches a Microsoft Store execution alias that prints
    an advert and exits without running anything. Every site that spelled it sat behind
    `2>/dev/null` or `|| exit 0`, so the failure was *green*. On 2026-08-29 that was true of
    post-edit.sh and all four stages it sources, the interface-first read gate and the precompact
    wipe (both shell then, both Python since 2026-09-02) — interface stubs, routing sync, lint,
    reminders and that gate had never once run on a Windows clone, and nothing anywhere said so.

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
