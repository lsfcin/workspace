# T1 agora: the ROADMAP's "now" is pointers only, and every entry and close point shows or checks it.
import importlib.util
import subprocess
from pathlib import Path

import pytest
from conftest import WORKSPACE_ROOT

_spec = importlib.util.spec_from_file_location('agora', WORKSPACE_ROOT / 'core/tools/wos/close/agora.py')
agora = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(agora)

POINTER = '- [now] — first'
BLOCK = '**🔴 [now] Finish this work** (Lucas, 2026-11-26)\n*Done when* — it passes.'
NEXT = '### Next action\n'
ISSUE = 'b20261110-handoff-gate-prose'


def git(repo: Path, *args: str) -> None:
    subprocess.run(['git', '-C', str(repo), *args], check=True)


@pytest.fixture
def repo(tmp_path):
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    (tmp_path / 'ROADMAP.md').write_text(
        f'# Roadmap\n\n## Agora\n\n{POINTER}\n\n## Work\n\n{BLOCK}\n\n'
        '**🟡 An untagged item**\nIts body.\n', encoding='utf-8', newline='\n')
    (tmp_path / 'ISSUES.md').write_text(
        f'- **An open issue** `{ISSUE}`\n', encoding='utf-8', newline='\n')
    git(tmp_path, 'add', 'ROADMAP.md', 'ISSUES.md')
    return tmp_path


def test_agora_checks_each_pointer(repo):
    roadmap = repo / 'ROADMAP.md'
    roadmap.write_text(roadmap.read_text(encoding='utf-8').replace(
        POINTER, '- [unknown] — missing\n\n- no pointer'), encoding='utf-8', newline='\n')
    errors = agora.problems(repo)
    assert len(errors) == 2
    assert any('[unknown]' in error for error in errors)
    assert any('no [tag]' in error for error in errors)
    assert agora.handoff_problems(NEXT + 'none', repo) == errors


def test_agora_refuses_more_than_three_lines(repo):
    roadmap = repo / 'ROADMAP.md'
    roadmap.write_text(roadmap.read_text(encoding='utf-8').replace(
        POINTER, '\n'.join([POINTER] * 4)), encoding='utf-8', newline='\n')
    assert len(agora.problems(repo)) == 1
    assert 'maximum 3' in agora.problems(repo)[0]


def test_only_tracked_roadmaps_in_this_repo_define_items(repo):
    folder = repo / 'docs'
    folder.mkdir()
    extra = folder / 'ROADMAP-extra.md'
    extra.write_text('## Agora\n**🔴 [decoy] Not an item**\n\n'
                     '## Later\n**🟢 [later] Second item**\nBody.\n\n## End\nIgnored.\n',
                     encoding='utf-8', newline='\n')
    git(repo, 'add', 'docs/ROADMAP-extra.md')
    nested = repo / 'nested'
    subprocess.run(['git', 'init', '-q', str(nested)], check=True)
    (nested / 'ROADMAP.md').write_text('**🔴 [nested] Other repo**\n', encoding='utf-8', newline='\n')
    git(nested, 'add', 'ROADMAP.md')
    (repo / 'ROADMAP-untracked.md').write_text('**🔴 [untracked] Ignore**\n', encoding='utf-8', newline='\n')
    assert agora.roadmaps(repo) == [repo / 'ROADMAP.md', extra]
    assert agora.defined(repo) == {'now': BLOCK, 'later': '**🟢 [later] Second item**\nBody.'}
    assert agora.item(repo, 'now') == BLOCK
    assert agora.item(repo, 'unknown') is None


@pytest.mark.parametrize('action', ['Continue [now].', f'Check `{ISSUE}`.', 'none'])
def test_next_action_accepts_a_tag_an_issue_or_none(repo, action):
    assert agora.issue_ids(repo) == {ISSUE}
    assert agora.handoff_problems(NEXT + action, repo) == []


def test_next_action_refuses_unknown_tags_even_with_a_valid_pointer(repo):
    assert any('[unknown]' in error for error in agora.handoff_problems(NEXT + '[unknown]', repo))
    errors = agora.handoff_problems(NEXT + '[now] and [unknown]', repo)
    assert len(errors) == 1 and '[unknown]' in errors[0]


@pytest.mark.parametrize('action', ['nonetheless', '`b20261110-unknown`', '<!-- [now] -->'])
def test_next_action_needs_a_pointer_in_its_own_section(repo, action):
    errors = agora.handoff_problems(NEXT + action + '\n### Worked on\n[now]\n', repo)
    assert len(errors) == 1 and 'must cite' in errors[0]


def test_handoff_refuses_open_threads_and_other_extra_sections(repo):
    errors = agora.handoff_problems(NEXT + 'none\n### Open threads\n### Retrospective\n', repo)
    assert errors == ['Open threads is gone: move each thread to its ROADMAP or ISSUES, or drop it',
                      'Unexpected handoff header: ### Retrospective']


def test_size_excludes_state_and_markers(repo):
    head = NEXT + 'none\n\n### Worked on\n'
    visible = head + 'é' * (599 - len(head)) + '\n'
    padding = 'x' * 1000
    tail = f'<!-- {padding} -->### State\n{padding}'
    assert len(visible) == 600
    assert agora.handoff_problems(visible + tail, repo) == []
    errors = agora.handoff_problems('\n' + visible + tail, repo)
    assert len(errors) == 1
    assert '601' in errors[0] and 'point at ROADMAP/ISSUES instead of restating them' in errors[0]


@pytest.mark.parametrize('roadmap_exists', [True, False])
def test_handoff_and_brief_require_an_agora_header(repo, roadmap_exists):
    path = repo / 'ROADMAP.md'
    if roadmap_exists:
        path.write_text('## Work\n', encoding='utf-8', newline='\n')
    else:
        path.unlink()
    assert agora.agora(repo) == []
    assert agora.brief(repo) == (
        f'No ## Agora in {repo.name}/ROADMAP.md: rank one before planning (≤3 [tag] pointers).\nISSUES: 1 open')
    assert agora.handoff_problems(NEXT + 'none', repo) == [
        f'the close creates {repo.name}/ROADMAP.md with a ## Agora before handing off']


def test_brief_includes_agora_issues_and_planning_prompt_after_commit(repo):
    assert agora.age(repo) is None
    git(repo, '-c', 'user.name=Test', '-c', 'user.email=test@example.org',
        '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Add roadmap')
    days = agora.age(repo)
    assert isinstance(days, int)
    assert agora.agora(repo) == [POINTER]
    assert agora.brief(repo).splitlines() == [
        f'## Agora — {repo.name} (ROADMAP.md, last changed {days}d ago)', POINTER, 'ISSUES: 1 open',
        "The plan picks: the handoff's Next action or an Agora item, and says why. "
        'Read the whole ROADMAP; if the Agora is wrong, re-rank it before working.',
    ]


def test_empty_agora_and_no_roadmap_or_issues(repo):
    path = repo / 'ROADMAP.md'
    path.write_text('## Agora\n', encoding='utf-8', newline='\n')
    assert agora.agora(repo) == []
    assert agora.handoff_problems(NEXT + 'none', repo) == []
    assert agora.brief(repo).startswith(f'## Agora — {repo.name} (ROADMAP.md)\n')
    path.unlink()
    (repo / 'ISSUES.md').unlink()
    assert agora.brief(repo) == ''
    assert agora.issue_ids(repo) == set()
