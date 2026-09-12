#!/usr/bin/env python3
# The line-count gate: warn and block on authored lines, at the two numbers limits.env declares.
#
# Two callers, one implementation, which core/hooks/SPECS.md promises explicitly -- the pre-commit
# pipeline passes the staged files, and a bare run audits every tracked file in the repo.
#
# WHICH FILES ARE AUTHORED IS file_law.py'S ANSWER, never a regex here. This script carrying its own
# extension list is what let .sh and extensionless scripts past the gate for months, during which
# core/hooks/pre-commit itself reached 385 lines unblocked. The thresholds are limits.env's answer
# for the same reason.
#
# PROSE JOINED IT 2026-09-12 (Lucas: every folder, every authored type). limits.env has held one
# number for code and prose alike since 2026-08-18, but only the BLOCK half reached .md -- through
# pre-edit.py at write time and the entropy dashboard after the fact -- so the WARN, the half that
# asks for a look before a file is unreadable, existed for code alone.
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import feature_law  # noqa: E402
import file_law  # noqa: E402

for _stream in (sys.stdout, sys.stderr):
    _stream.reconfigure(encoding='utf-8', errors='replace')


# A file may waive the WARN by carrying this marker plus its reason, in whatever comment syntax it
# already uses. The BLOCK is never waivable: over that number a file is CUT, not excused. The reason
# travels with the file rather than sitting in a list somewhere else, because the reader who needs it
# is the one who just opened the file and found it long.
#
# It must OPEN a comment line. Naming the marker in prose is not claiming it: the sentence
# documenting this waiver, in core/hooks/SPECS.md, silently exempted that file the moment it was
# written — a gate a document switches off by describing it.
WARN_EXEMPT = re.compile(r'^\s*(?:#|//|%|<!--)\s*warn-exempt:', re.M)


def report(paths, root=None) -> tuple:
    """(lines of report, blocked) for `paths`. Never raises, never prints -- the caller decides.

    Returned rather than printed because the pre-commit pipeline must fold this into its own single
    reject path, and a checker that prints its own verdict cannot be composed into one.
    """
    limits = file_law.load_limits()
    warn, block = int(limits['WARN_LINES']), int(limits['BLOCK_LINES'])
    root = Path(root) if root else Path.cwd()
    lines, blocked, warned = [], False, False
    for path in paths:
        target = root / path
        # Code or prose, asked of the law rather than of a suffix. is_authored answers for our own
        # code and is_authored_prose for our own .md; both already waive vendored and generated.
        if not target.is_file() or not (file_law.is_authored(Path(path), root)
                                        or file_law.is_authored_prose(Path(path), root)):
            continue
        # A tool wrote it, so no authoring rule applies — the third answer file_law holds, and the
        # one this gate never asked for. `generated.txt` promises the cap is waived and the entropy
        # dashboard honours that; this did not, so the session close regenerated ARCHITECTURE.html
        # and was then refused permission to commit it. A generator that cannot settle its own
        # output leaves the artifact dirty on every close.
        if file_law.is_generated_artifact(target, root):
            continue
        text = target.read_text(encoding='utf-8', errors='replace')
        count = len(text.splitlines())
        if count >= block:
            lines.append(f'🚨 BLOCK: {path} ({count} lines)')
            blocked = True
        elif count >= warn and not WARN_EXEMPT.search(text):
            lines.append(f'⚠ WARN: {path} ({count} lines)')
            warned = True
    if blocked:
        lines.append(f'\nOne or more authored files exceed the block threshold ({block} lines).')
    elif warned:
        lines.append(f'\nOne or more authored files exceed the warn threshold ({warn} lines).')
    else:
        lines.append('No authored files exceed thresholds.')
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
