# b20260913 regression — the close may not publish a finding against the branch it is merging.
#
# Every session close wrote `feature/x is N ahead of main` into ISSUES.md and then merged
# feature/x into main. The finding was true at the instant it was computed and false by the time
# anyone read it, and the commit carrying it was the last thing keeping it true. Reordering does
# not cure it: the block is written on the feature branch so that it rides into develop, and after
# promotion the Git Flow gate leaves no branch a commit could carry it on.
#
# The cure is a NAME threaded from the only caller that knows one. These cases pin both halves —
# the branch being promoted is excused, and every OTHER branch still answers the same question, so
# the excuse cannot widen into "the close stops counting branches".
from pathlib import Path

from branch_debt import unmerged_branches

from vcs_repos import commit, git, repo  # noqa: F401 — pytest fixtures


def test_the_branch_this_close_is_promoting_is_not_a_finding(repo):
	"""The bug itself: ahead of main, and about to stop being so."""
	git(repo, 'checkout', '-q', '-b', 'feature/x')
	commit(repo, 'work.txt')
	assert unmerged_branches(repo, 'feature/x') == []


def test_naming_one_branch_does_not_excuse_another(repo):
	"""The excuse is one branch wide. A close that stopped counting would be the worse bug."""
	git(repo, 'checkout', '-q', '-b', 'feature/x')
	commit(repo, 'work.txt')
	git(repo, 'checkout', '-q', 'main')
	git(repo, 'checkout', '-q', '-b', 'feature/forgotten')
	commit(repo, 'other.txt')
	signal, = unmerged_branches(repo, 'feature/x')
	assert 'feature/forgotten' in signal, signal


def test_naming_no_branch_reports_every_one_of_them(repo):
	"""A bare run — the pre-commit path, and anyone auditing by hand — promotes nothing."""
	git(repo, 'checkout', '-q', '-b', 'feature/x')
	commit(repo, 'work.txt')
	signal, = unmerged_branches(repo)
	assert 'feature/x' in signal, signal


def test_the_close_only_names_a_branch_it_will_actually_merge():
	"""The three facts roundup holds before it regenerates, as the expression it passes.

	Read as source rather than run: reaching the real arm means running a whole session close.
	What must not drift is that ALL THREE still gate the name — a verdict of red, an explicit
	--no-promote, or a repo outside gitflow scope each mean no merge follows, and excusing the
	branch then would hide real debt rather than an artifact of ordering.
	"""
	roundup = (Path(__file__).resolve().parents[4] / 'wos/roundup').read_text(encoding='utf-8')
	line, = [ln for ln in roundup.splitlines() if ln.strip().startswith('promoting = ')]
	for fact in ("verdict != 'red'", 'not no_promote', 'gitflow'):
		assert fact in line, f'{fact} no longer gates the excused branch: {line}'
	assert 'artifacts.regenerate(root, leave_dirty, clean, promoting)' in roundup
