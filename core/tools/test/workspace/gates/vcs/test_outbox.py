# b20261121-drive-by-lock regression: a note for another repo's ISSUES.md or ROADMAP.md waits in its outbox, and a session holds one repo unless it says --multi.
import subprocess
import sys

from conftest import WORKSPACE_ROOT, governed_repo

sys.path[:0] = [str(WORKSPACE_ROOT / 'core/hooks/git'), str(WORKSPACE_ROOT / 'core/hooks/session')]
import lock  # noqa: E402
import outbox  # noqa: E402

A, B = 'test-outbox-session-a', 'test-outbox-session-b'
TOOLS = WORKSPACE_ROOT / 'core/tools/wos'


def _tool(name, *args, session=A):
    return subprocess.run([sys.executable, str(TOOLS / name), *map(str, args), '--session', session],
                          capture_output=True, text=True, encoding='utf-8')


def test_a_note_waits_once_and_only_the_holder_clears_it(tmp_path):
    repo = governed_repo(tmp_path)
    lock.take(repo, B, 'theirs')
    first = _tool('note', repo, 'ISSUES.md', 'the gate is slow')
    again = _tool('note', repo, 'ISSUES.md', 'the gate is slow')
    assert first.returncode == 0 and again.returncode == 0 and len(outbox.pending(repo)) == 1
    note = outbox.pending(repo)[0]
    assert note['id'] in first.stdout and note['session'] == A and note['file'] == 'ISSUES.md'
    assert _tool('note', repo, 'README.md', 'x').returncode == 64   # only ISSUES.md and ROADMAP.md
    listed = _tool('note', repo, session=B)
    assert 'the gate is slow [src: agent ' in listed.stdout and note['id'] in listed.stdout
    assert _tool('note', repo, '--done', note['id']).returncode == 1 and outbox.pending(repo)
    assert _tool('note', repo, '--done', note['id'], session=B).returncode == 0
    assert not outbox.pending(repo)


def test_a_second_repo_takes_multi_and_a_note_needs_nothing(tmp_path):
    first, second = governed_repo(tmp_path, 'first'), governed_repo(tmp_path, 'second')
    lock.take(first, A, 'work')
    refusal, _ = lock.take(second, A, 'more')
    assert '[one-repo]' in refusal and 'wos/note' in refusal and '--multi' in refusal
    assert not lock.holder(second)[0]
    refusal, _ = lock.take(second, A, 'more', multi=True)
    assert not refusal and lock.holder(second)[0] == A


def test_a_refused_edit_of_a_notes_file_names_the_outbox(tmp_path):
    repo = governed_repo(tmp_path)
    lock.take(repo, B, 'theirs')
    assert 'wos/note' in lock.verdict(repo / 'ISSUES.md', A)[0]
    assert 'wos/note' not in lock.verdict(repo / 'code.py', A)[0]


def test_take_shows_what_waits_and_the_reminder_counts_it(tmp_path):
    import reminders   # noqa: PLC0415
    repo = governed_repo(tmp_path)
    outbox.add(repo, 'ROADMAP.md', 'build the thing', B)
    assert reminders.outbox().startswith('OUTBOX: ') and 'wos/note' in reminders.outbox()
    done = _tool('take', repo, 'work', session='test-outbox-take')   # A holds repos of other cases
    assert done.returncode == 0 and '1 note waits' in done.stdout and 'wos/note' in done.stdout


def test_a_move_carries_the_outbox(tmp_path):
    repo = governed_repo(tmp_path)
    outbox.add(repo, 'ISSUES.md', 'moved with it', B)
    assert _tool('move', repo, tmp_path / 'moved').returncode == 0
    assert [n['text'] for n in outbox.pending(tmp_path / 'moved')] == ['moved with it']
    assert not outbox.path(repo).exists()
