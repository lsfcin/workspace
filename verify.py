#!/usr/bin/env python3
# Usage: verify.py [fast|full] — this workspace's verification contract, the one the pre-commit
# gate discovers and /roundup runs at close.
#
# WHY THIS IS NOT A MAKEFILE TARGET ANY MORE. The contract used to be `make verify-fast`, and on a
# machine without `make` every commit printed a warning and ran nothing: the gate was fully green
# and fully blind (ISSUES.md B9). Installing `make` would not have fixed it, and that is the part
# worth keeping. The recipe named `.venv/bin/pytest` — which is `.venv/Scripts` on another machine —
# and globbed `core/hooks/*/*.sh` through a shell that is not everywhere. **A Makefile cannot ask
# platform_law.py anything**, so every per-machine answer inside one has to be spelled, and a
# spelled answer is the defect this port exists to remove. A Python entrypoint can just ask.
#
# Discovery is unchanged in spirit: core/hooks/commit/gates_project.py looks for this file first,
# then an npm "verify:fast", then a Makefile target, so a project keeps declaring a contract rather
# than wiring anything.
import subprocess
import sys
from pathlib import Path
from shutil import which

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'core/hooks'))
from platform_law import interpreter  # noqa: E402

SUITE = 'core/tools/test/'


def _run(command: list) -> int:
    """One step, with the child's stdin closed.

    NOT A DETAIL. A verification run is spawned from hooks, from /roundup and from CI, and a child
    that inherits an interactive stdin blocks there forever instead of failing — measured in this
    session, where the suite ran in 70s with stdin closed and hung indefinitely without it. A
    verifier that can hang is worse than one that can fail: nothing reports a hang.
    """
    return subprocess.run(command, cwd=ROOT, stdin=subprocess.DEVNULL).returncode


def shell_syntax() -> int:
    """`bash -n` over the shell hooks that are left, while any are.

    Skips loudly rather than failing when bash is absent: an uninstalled checker is not a red
    suite, and reporting it as one is the exact lie the missing `make` told. The arm retires
    itself — when the last .sh under core/hooks is ported, there is nothing here to check.
    """
    scripts = sorted(ROOT.glob('core/hooks/*.sh')) + sorted(ROOT.glob('core/hooks/*/*.sh'))
    if not scripts:
        return 0
    bash = which('bash')
    if not bash:
        print(f'⚠  bash not found — {len(scripts)} shell hook(s) not syntax-checked.')
        return 0
    return _run([bash, '-n', *[str(s) for s in scripts]])


def suite(network: bool) -> int:
    """T0 static + T1 unit. `full` adds the network-marked cases (live yt-dlp, real URLs)."""
    command = [interpreter(), '-m', 'pytest', SUITE, '-q']
    if not network:
        command += ['-m', 'not network']
    return _run(command)


def main(argv: list) -> int:
    level = argv[1] if len(argv) > 1 else 'fast'
    if level not in ('fast', 'full'):
        print(f'Usage: verify.py [fast|full] — got {level!r}', file=sys.stderr)
        return 64
    return shell_syntax() or suite(network=(level == 'full'))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
