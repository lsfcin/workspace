# b20260901-a-bash-tool-costs-thirty-seconds-a-commit-here regression.
#
# `sync-skills --check` cost 22.0 s on a Windows clone with the mirrors in sync, and
# core/hooks/commit/generators.py runs the tool TWICE, so every commit touching a skill paid ~30 s.
# The cause was fork, not work: ~300 forks at ~48 ms each under Git Bash -- a `basename` per skill
# per mirror, a `cmp` per copy, a `grep` per frontmatter field, and one whole Python interpreter per
# command file inside render_command. Nobody had measured it, and on Linux nobody would feel it.
#
# The fix was the port, and these hold the two things that could bring the cost back: a bash tool
# reappearing under core/tools/, and the check quietly becoming slow again.
import ast
import subprocess
import time

from conftest import WORKSPACE_ROOT

# Generous on purpose. The measured figure is ~0.3 s and the bash was 22 s, so anything in between
# is a decisive verdict; a tight bound would only turn a loaded CI box into a red suite. This
# catches an ORDER OF MAGNITUDE, which is the only thing that went wrong last time.
CEILING_SECONDS = 5.0


def test_no_bash_tool_remains_under_core_tools():
    """The port's own thesis (test_port_ratchet.py): porting bash to Python removes the per-OS
    axis. These two were the half of B12 that was left undecided -- the launcher learned to
    dispatch on the shebang, and *why these two were still bash* never got an answer."""
    listed = subprocess.run(['git', 'ls-files', 'core/tools'], cwd=WORKSPACE_ROOT,
                            capture_output=True, text=True, encoding='utf-8')
    shell = [line for line in listed.stdout.splitlines() if line.endswith('.sh')]
    assert not shell, f'bash is back under core/tools/: {shell}'


def test_the_mirror_check_is_not_slow_again():
    """The number the SessionStart heal depends on. A hook that runs before every session may not
    cost 22 s, which is exactly why the heal was blocked on this port."""
    started = time.monotonic()
    done = subprocess.run(['sh', str(WORKSPACE_ROOT / 'core/run'), 'tools/wos/sync-skills',
                           '--check'],
                          cwd=WORKSPACE_ROOT, stdin=subprocess.DEVNULL, capture_output=True,
                          text=True, timeout=180, encoding='utf-8', errors='replace')
    elapsed = time.monotonic() - started
    assert done.returncode == 0, done.stdout + done.stderr
    assert elapsed < CEILING_SECONDS, (
        f'sync-skills --check took {elapsed:.1f}s (ceiling {CEILING_SECONDS}s, measured 0.3s after '
        f'the port, 22.0s as bash). Something reintroduced per-item process spawning.')


def test_the_check_does_not_spawn_a_process_per_skill():
    """The shape of the old cost, asserted on the source rather than on the clock: these modules
    may not shell out at all. A timing bound alone would pass on a fast machine while the defect
    sat there waiting for a slow one.

    PARSED, NOT GREPPED. The first version of this looked for the word `subprocess` with comment
    lines stripped, and mirror.py's own docstring says "the cache the bash needed to avoid a
    subprocess buys nothing" -- prose about the fix reading as the defect. An import is a syntax
    node, so ask the syntax.
    """
    for relative in ('core/tools/wos/skills/mirror.py', 'core/tools/wos/skills/validate.py',
                     'core/tools/wos/sync-skills'):
        tree = ast.parse((WORKSPACE_ROOT / relative).read_text(encoding='utf-8'))
        imported = {alias.name.split('.')[0]
                    for node in ast.walk(tree) if isinstance(node, ast.Import)
                    for alias in node.names}
        imported |= {node.module.split('.')[0]
                     for node in ast.walk(tree)
                     if isinstance(node, ast.ImportFrom) and node.module}
        assert 'subprocess' not in imported, (
            f'{relative} imports subprocess; the port exists to stop spawning per item')
