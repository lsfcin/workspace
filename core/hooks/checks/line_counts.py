#!/usr/bin/env python3
# The line-count gate: warn at 150 code lines, block at 200.
#
# Two callers, one implementation, which core/hooks/SPECS.md promises explicitly -- the pre-commit
# pipeline passes the staged files, and a bare run audits every tracked file in the repo.
#
# WHICH FILES ARE CODE IS file_law.py'S ANSWER, never a regex here. This script carrying its own
# extension list is what let .sh and extensionless scripts past the gate for months, during which
# core/hooks/pre-commit itself reached 385 lines unblocked. The thresholds are limits.env's answer
# for the same reason.
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import feature_law  # noqa: E402
import file_law  # noqa: E402

for _stream in (sys.stdout, sys.stderr):
    _stream.reconfigure(encoding='utf-8', errors='replace')


def report(paths, root=None) -> tuple:
    """(lines of report, blocked) for `paths`. Never raises, never prints -- the caller decides.

    Returned rather than printed because the pre-commit pipeline must fold this into its own single
    reject path, and a checker that prints its own verdict cannot be composed into one.
    """
    limits = file_law.load_limits()
    warn, block = int(limits.get('WARN_LINES', 150)), int(limits.get('BLOCK_LINES', 200))
    root = Path(root) if root else Path.cwd()
    lines, blocked, warned = [], False, False
    for path in paths:
        target = root / path
        if not target.is_file() or not file_law.is_code_file(Path(path)):
            continue
        # A tool wrote it, so no authoring rule applies — the third answer file_law holds, and the
        # one this gate never asked for. `generated.txt` promises the cap is waived and the entropy
        # dashboard honours that; this did not, so the session close regenerated ARCHITECTURE.html
        # and was then refused permission to commit it. A generator that cannot settle its own
        # output leaves the artifact dirty on every close.
        if file_law.is_generated_artifact(target, root):
            continue
        count = len(target.read_text(encoding='utf-8', errors='replace').splitlines())
        if count >= block:
            lines.append(f'🚨 BLOCK: {path} ({count} lines)')
            blocked = True
        elif count >= warn:
            lines.append(f'⚠ WARN: {path} ({count} lines)')
            warned = True
    if blocked:
        lines.append(f'\nOne or more code files exceed the block threshold ({block} lines).')
    elif warned:
        lines.append(f'\nOne or more code files exceed the warn threshold ({warn} lines).')
    else:
        lines.append('No code files exceed thresholds.')
    return lines, blocked


def main() -> int:
    # Off means it stops rejecting, not that it fails. Same arm, same reason, as every other gate.
    if not feature_law.is_enabled('line-limit'):
        return 0
    argv = sys.argv[1:]
    if argv == ['--from-stdin']:
        paths = [line.strip() for line in sys.stdin if line.strip()]
    elif argv:
        paths = argv
    else:
        done = subprocess.run(['git', 'ls-files'], capture_output=True, text=True,
                              encoding='utf-8', errors='replace')
        paths = done.stdout.splitlines()
    lines, blocked = report(paths)
    print('\n'.join(lines))
    return 1 if blocked else 0


if __name__ == '__main__':
    sys.exit(main())
