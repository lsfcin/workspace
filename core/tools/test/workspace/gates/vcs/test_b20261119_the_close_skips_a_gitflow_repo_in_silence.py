# b20261119 regression — the close skipped a gitflow repo in silence.
#
# academy/administration runs feature → develop → main by choice, but the close promoted only the
# workspace and direct children of code/, while the branch gate covered code/ at any depth: two
# copies of one scope, and a repo outside both was listed as worked and never said to be skipped.
# The scope now has one declaration, core/hooks/gitflow.txt, and every caller asks gitflow_law.
from gitflow_law import enforced


def test_the_workspace_and_its_projects_are_covered(tmp_path):
	assert enforced(tmp_path, tmp_path)
	assert enforced(tmp_path / 'code/x', tmp_path)


def test_a_repo_that_chose_gitflow_is_covered(tmp_path):
	"""The bug itself: declared, so the gate blocks there and the close promotes there."""
	assert enforced(tmp_path / 'academy/administration', tmp_path)


def test_an_undeclared_repo_stays_exempt(tmp_path):
	"""Overleaf owns the paper repos; a star matches one segment, never a nested repo."""
	assert not enforced(tmp_path / 'academy/papers/p', tmp_path)
	assert not enforced(tmp_path / 'code/x/inner', tmp_path)
	assert not enforced(tmp_path.parent, tmp_path)
