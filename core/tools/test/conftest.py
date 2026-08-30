# conftest.py — the one place the suite learns where things are: workspace root, core/tools,
# and the enforcement layer. Also registers the network marker for the video tests.
#
# Every test used to spell out `parents[3]` for the workspace root — nine copies of a depth,
# which is a number that changes the moment a test moves into a subdirectory. Import it from
# here instead; pytest loads this file before any test module.
import os, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
WORKSPACE_ROOT = HERE.parents[2]

# A git hook exports GIT_DIR, GIT_INDEX_FILE and friends, and every child process inherits them.
# Dozens of tests here build a throwaway repo in tmp_path and run git inside it; under those
# variables git ignores the cwd and operates on THIS repo instead. The tests then assert against
# the workspace's own history and fail — but only when the suite is run BY THE PRE-COMMIT HOOK,
# which is the one moment verify:fast is acting as a gate. Run by hand it is green, so the gate
# was red and its operator was told otherwise. Found 2026-08-19; the failure is loud (19 tests)
# and was invisible for as long as it existed because nobody reproduces a hook's environment.
for _var in ('GIT_DIR', 'GIT_INDEX_FILE', 'GIT_WORK_TREE', 'GIT_OBJECT_DIRECTORY',
             'GIT_ALTERNATE_OBJECT_DIRECTORIES', 'GIT_PREFIX', 'GIT_COMMON_DIR'):
    os.environ.pop(_var, None)

# Own directory first, so tests in subdirectories can `from conftest import WORKSPACE_ROOT`.
sys.path.insert(0, str(HERE))

# core/hooks and core/tools are each one root plus one directory per responsibility. Both
# are derived by scan, never listed: a spelled-out list would go stale the next time either
# is split, and the tests would fail for a reason that has nothing to do with what they
# assert. That is exactly what happened when core/tools/test itself was split.
HOOKS = WORKSPACE_ROOT / 'core/hooks'
TOOLS = WORKSPACE_ROOT / 'core/tools'


def _tree(root):
    """The root, then every directory under it that holds importable modules."""
    yield root
    for child in sorted(root.rglob('*')):
        if child.is_dir() and not any(part.startswith(('.', '_')) for part in
                                      child.relative_to(root).parts):
            yield child


for _dir in [*_tree(HOOKS), *_tree(TOOLS)]:
    sys.path.insert(0, str(_dir))


def git_lines(*args) -> list:
    """Lines of a git query against the workspace, minus the ratchet files themselves.

    Shared because a ratchet necessarily NAMES what it forbids: a test asserting nobody spells
    `/mnt/workspace` has to spell it to search for it, and would otherwise be its own only
    finding. Any path containing `_ratchet` is dropped for that reason — the rule is the file
    kind, not a list of filenames, so splitting the ratchets into a second file cannot silently
    make one of them count itself.
    """
    import subprocess
    done = subprocess.run(['git', *args], cwd=WORKSPACE_ROOT, capture_output=True, text=True)
    return [line for line in done.stdout.splitlines() if line and '_ratchet' not in line]


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "network: hits real network/models; excluded from verify:fast")
