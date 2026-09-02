#!/usr/bin/env python3
# What a file IS, and which rules apply to it. The numeric-law sibling of schema_law.py:
# that module parses core/SCHEMA.md, this one owns the file-shape law every size, fanout
# and line-count check reads.
#
# Why it exists (2026-07-31): "a code file" was defined FOUR times — check-line-counts.sh,
# entropy-dashboard.py, workspace_meta.py and workspace_scanner.py each carried their own
# extension list, and no two agreed. `.sh` and extensionless executables were invisible to
# the BLOCKING gate, which is how core/hooks/pre-commit reached 385 lines and
# core/tools/wos/sync-skills 341 without ever being stopped. One definition, one home.
import fnmatch
import sys
from pathlib import Path
from platform_law import rel as _rel

HERE = Path(__file__).resolve().parent
LIMITS_FILE = HERE / 'limits.env'
VENDORED_FILE = HERE / 'vendored.txt'
GENERATED_FILE = HERE / 'generated.txt'
EXTENSIONLESS_FILE = HERE / 'extensionless.txt'

# Things the line cap and the fanout signal apply to. Prose types (.md, .yaml, .toml) are
# NOT here: their size is a signal, never a cap. `.tex` is code on purpose — a paper
# section file is authored under the same 200-line rule (academy/papers/SPECS.md § File size).
CODE_EXTS = {'.js', '.jsx', '.ts', '.tsx', '.py', '.dart', '.sh',
             '.html', '.css', '.scss', '.tex'}

# A stub is generated FROM its source and rides in the routing table's Interface column.
GENERATED = ('.pyi', '.d.ts', '.dart.api', '.texif')

# Files that ARE their own interface, so nothing generates one beside them and the read gate
# never fires on one. It was spelled out identically in four places — stubgen, both facade
# hooks and the routing scanner — already drifting in NAME (FACADES vs FACADE_NAMES), which is
# how a fifth copy nearly got written without anyone noticing the other four. It belongs to the
# question this module owns, what a file IS, and `index.dart` joining once proves the set moves.
FACADES = {'index.ts', 'index.tsx', 'index.js', 'index.jsx', '__init__.py', 'index.dart'}

# How a file of each kind declares what it is. One home, because it used to have three —
# pre-edit.py held two dicts and gates/source-quality.sh a shell case-list, and only the
# shell one ran at commit time, only as a warning, and only over code extensions.
EXAMPLE_COMMENT = {
    '.py': '# Short description',      '.js': '// Short description',
    '.ts': '// Short description',     '.tsx': '// Short description',
    '.jsx': '// Short description',    '.dart': '// Short description',
    '.sh': '# Short description',      '.css': '/* Short description */',
    '.scss': '/* Short description */', '.html': '<!-- Short description -->',
    '.yaml': '# Short description',    '.yml': '# Short description',
    '.toml': '# Short description',    '.env': '# Short description',
    '.txt': '# Short description',     '.tex': '% Short description of this section',
    '.md': '# Title of this document',
}


def is_tool_entrypoint(path: Path) -> bool:
    """An extensionless CLI under core/tools/, by SHAPE — not by the shebang that named one
    machine's venv and made all 33 unrunnable elsewhere. `core/run` starts them now."""
    return not path.suffix and '/core/tools/' in f'/{path.as_posix()}'


def is_code_file(path: Path) -> bool:
    """One definition. An extension, a core/tools CLI, or a shebang.

    The last two arms close the old blind spot: pre-commit and the core/tools CLIs are real
    code, named by git or by our own convention. Dropping those shebangs took 31 files out
    of the line cap and the fanout signal in one edit.
    """
    if path.name.endswith(GENERATED):
        return False
    if path.suffix in CODE_EXTS:
        return True
    if path.suffix:
        return False
    try:
        return is_tool_entrypoint(path) or path.open('rb').read(2) == b'#!'
    except OSError:
        return False


def load_limits() -> dict:
    """Every numeric limit, from the one file that holds them."""
    limits = {}
    for line in LIMITS_FILE.read_text(encoding='utf-8').splitlines():
        line = line.split('#', 1)[0].strip()
        if '=' in line:
            key, value = line.split('=', 1)
            limits[key.strip()] = int(value.strip())
    return limits


def _lines(path: Path) -> list:
    if not path.exists():
        return []
    return [ln.strip() for ln in path.read_text(encoding='utf-8').splitlines()
            if ln.strip() and not ln.startswith('#')]


def allowed_extensionless() -> set:
    """Basenames an external tool dictates, so they cannot carry an extension."""
    return set(_lines(EXTENSIONLESS_FILE))


def is_vendored(path: Path, root: Path) -> bool:
    """True for third-party files we did not author and must not police.

    17 of the 28 files over the line cap are conference templates (sigconf, iclr). Holding
    someone else's LaTeX class to our authoring rules makes the finding list 60% noise and
    would make every paper uncommittable. Same shape as gitignore-exceptions.txt: a named,
    reviewed list, never a heuristic.
    """
    try:
        rel = _rel(path.resolve(), root)
    except ValueError:
        return False
    return any(fnmatch.fnmatch(rel, p) for p in _lines(VENDORED_FILE))


def is_generated_artifact(path: Path, root: Path) -> bool:
    """True for a file one of OUR tools writes — see core/hooks/generated.txt.

    A generated artifact is code by extension and authored by nobody, so the authoring rules
    read it as a violation the moment it is staged: ARCHITECTURE.html is 400-odd lines of HTML
    and the line cap would block the commit that first carried it. The cap is right and the file
    is right; what was missing was the third answer, that a tool wrote it. Kept separate from
    is_vendored on purpose — that list is about provenance we do not own, this one is about
    provenance we do.
    """
    try:
        rel = _rel(path.resolve(), root)
    except ValueError:
        return False
    return any(fnmatch.fnmatch(rel, p) for p in _lines(GENERATED_FILE))


def is_authored(path: Path, root: Path) -> bool:
    """True when our authoring rules apply: code, ours, and written by a person. The one question
    every size and shape gate actually asks, so they ask it in one place."""
    return (is_code_file(path) and not is_vendored(path, root)
            and not is_generated_artifact(path, root))


def over_column_cap(text: str, cols: int) -> list:
    """Line numbers of prose lines longer than `cols`. The one definition every reader uses.

    Three shapes are exempt: a **markdown table row**, anything inside a **fenced code block**,
    and the **leading YAML frontmatter block**. Why each, and why the third is not a hollow-out,
    is in limits.env § BLOCK_COLS — the one home for this rule's reasoning.
    """
    over, fenced = [], False
    lines = text.splitlines()
    end = 0
    if lines and lines[0].strip() == '---':
        for number, line in enumerate(lines[1:], 2):
            if line.strip() == '---':
                end = number
                break
    for number, line in enumerate(lines, 1):
        if number <= end:  # the leading frontmatter block, closed by its own `---`
            continue
        if line.lstrip().startswith('```'):
            fenced = not fenced
            continue
        if not fenced and len(line) > cols and not line.lstrip().startswith('|'):
            over.append(number)
    return over


def is_authored_prose(path: Path, root: Path) -> bool:
    """The prose twin, for the gates that hold .md to the same line cap (2026-08-18).

    A separate predicate rather than a wider is_authored, because two of that function's callers
    must stay code-only: entropy_fanout counts MODULES in a directory — a flat collection of
    documents is a legitimate shape, and brain/goals/ is 57 files — and `--filter-code` feeds the
    shell line gate. It lives here rather than in the two gates that ask it, for the reason the
    whole module exists: the same question answered in two files drifts.
    """
    return (path.suffix == '.md' and not is_vendored(path, root)
            and not is_generated_artifact(path, root))


def main() -> int:
    """`--filter-code` keeps stdin paths that are code, so the shell gate shares this law."""
    if '--filter-code' not in sys.argv:
        print('usage: file_law.py --filter-code < paths', file=sys.stderr)
        return 2
    root = HERE.parents[1]
    for line in sys.stdin:
        candidate = Path(line.strip())
        if not line.strip():
            continue
        full = candidate if candidate.is_absolute() else root / candidate
        if is_authored(full, root):
            print(line.strip())
    return 0


if __name__ == '__main__':
    sys.exit(main())
