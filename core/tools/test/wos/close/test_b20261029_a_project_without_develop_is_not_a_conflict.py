# b20261029 regression — a project with no develop branch has nothing to promote, not a conflict.
#
# code/rastro-da-banca is a teaching repo whose commit history IS the content, so it never had a
# develop. promote() skipped the feature → develop hop for the missing target, then ran
# develop → main anyway: the merge of a branch that does not exist failed, and the close reported
# "conflict merging develop → main" — a conflict nobody could find, on a repo nothing should touch.
import os
import subprocess
import sys

from conftest import WORKSPACE_ROOT

sys.path.insert(0, str(WORKSPACE_ROOT / 'core/tools/wos/close'))
import branches  # noqa: E402

ENV = {**os.environ, 'GIT_AUTHOR_NAME': 't', 'GIT_AUTHOR_EMAIL': 't@t',
       'GIT_COMMITTER_NAME': 't', 'GIT_COMMITTER_EMAIL': 't@t'}


def _git(repo, *args):
	return subprocess.run(['git', *args], cwd=repo, env=ENV, capture_output=True, text=True,
	                      encoding='utf-8', check=True).stdout.strip()


def test_a_repo_without_develop_promotes_nothing_and_says_nothing(tmp_path):
	origin, repo = tmp_path / 'origin.git', tmp_path / 'repo'
	_git(tmp_path, 'init', '-q', '--bare', str(origin))
	_git(tmp_path, 'init', '-q', '-b', 'main', str(repo))
	_git(repo, 'commit', '-q', '--allow-empty', '-m', 'first')
	_git(repo, 'remote', 'add', 'origin', str(origin))
	_git(repo, 'push', '-q', 'origin', 'main')
	_git(repo, 'checkout', '-q', '-b', 'feature/x')
	_git(repo, 'commit', '-q', '--allow-empty', '-m', 'work')
	main = _git(repo, 'rev-parse', 'main')

	assert branches.promote(repo, 'feature/x', leave_dirty=False) == ''
	assert _git(repo, 'rev-parse', 'main') == main
