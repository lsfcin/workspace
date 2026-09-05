# b20260831 regression — a project's commits reach its remote, and the session close is where.
#
# Committing in the workspace made the ledger scatter write AND commit a regenerated ISSUES.md into
# every nested repo it touched — 25 in one go on 2026-08-31 — and push none. The commits were
# correct; they simply stayed on this disk, which is exactly what code/SPECS-git.md § Push policy
# forbids. Worse, it happened BEHIND the session: nobody typed those commits, so nobody thought to
# push them, and the audit that found it had to push 25 repos by hand twenty minutes after
# declaring the tree clean.
#
# Ruled 2026-09-04 (Lucas): the ghost commit is gone — each repo writes and stages its own ledger
# in its own commit (test_b5_ledger_commits.py) — and the push is a sweep at session close, where a
# person is present to read what happened. A repo with no remote is NAMED, never silently skipped:
# that one cannot be fixed from here, and the old failure was precisely a repo nothing reported on.
import importlib.machinery
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import WORKSPACE_ROOT

ENV = {**os.environ, 'GIT_AUTHOR_NAME': 't', 'GIT_AUTHOR_EMAIL': 't@t',
       'GIT_COMMITTER_NAME': 't', 'GIT_COMMITTER_EMAIL': 't@t'}


@pytest.fixture
def roundup():
	"""The close tool loaded as a module — it is extensionless, so import needs the path spelled."""
	for directory in ('core/tools/wos/close', 'core/hooks', 'core/tools/verify',
	                  'core/hooks/entropy'):
		sys.path.insert(0, str(WORKSPACE_ROOT / directory))
	loader = importlib.machinery.SourceFileLoader('roundup_cli',
	                                              str(WORKSPACE_ROOT / 'core/tools/wos/roundup'))
	spec = importlib.util.spec_from_loader('roundup_cli', loader)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


def _git(repo, *args):
	return subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True,
	                      encoding='utf-8', env=ENV)


def _workspace(tmp_path, with_remote=True) -> Path:
	"""A throwaway workspace holding one nested project, with a bare origin of its own.

	Its own repo and its own origin: nothing here touches the real workspace, which is the law
	core/tools/test/wos/CONTEXT.md states.
	"""
	root, project = tmp_path / 'ws', tmp_path / 'ws/code/proj'
	project.mkdir(parents=True)
	subprocess.run(['git', 'init', '-q', str(root)], check=True)
	subprocess.run(['git', 'init', '-q', str(project)], check=True)
	(project / 'file.py').write_text('# a file\nx = 1\n', encoding='utf-8', newline='\n')
	_git(project, 'add', '.')
	_git(project, 'commit', '-qm', 'work nobody has seen', '--no-verify')
	if with_remote:
		origin = tmp_path / 'origin.git'
		subprocess.run(['git', 'init', '-q', '--bare', str(origin)], check=True)
		_git(project, 'remote', 'add', 'origin', str(origin))
		_git(project, 'push', '-q', '--set-upstream', 'origin', 'HEAD')
		(project / 'file.py').write_text('# a file\nx = 2\n', encoding='utf-8', newline='\n')
		_git(project, 'commit', '-qam', 'the commit that used to stay on this disk', '--no-verify')
	return root


def test_a_project_ahead_of_its_remote_is_pushed(tmp_path, roundup) -> None:
	root = _workspace(tmp_path)
	project = root / 'code/proj'
	assert _git(project, 'log', '--oneline', '@{upstream}..HEAD').stdout.strip(), 'setup is wrong'

	said = roundup.projects(root)

	assert '1 pushed' in said, said
	assert not _git(project, 'log', '--oneline', '@{upstream}..HEAD').stdout.strip(), (
		'the sweep reported a push that did not happen')


def test_a_project_with_no_remote_is_named(tmp_path, roundup) -> None:
	"""Nothing here can fix it, so the only honest act is to say which repo it is."""
	said = roundup.projects(_workspace(tmp_path, with_remote=False))
	assert 'no remote' in said and 'code/proj' in said, said


def test_a_project_already_pushed_says_nothing(tmp_path, roundup) -> None:
	"""A close that reports on every quiet repo is a close nobody reads to the end."""
	root = _workspace(tmp_path)
	roundup.projects(root)
	assert roundup.projects(root) == ''
