#!/usr/bin/env python3
# Tier 0 naming and placement, parsed from core/SCHEMA.md. Zero-token, deterministic.
#
# Scope is AUTHORED files only. The 91 tracked paths carrying spaces and accents are all
# received documents (.docx/.pdf/.html from the PPC process) whose names are their
# provenance — renaming them would destroy the link to the official source. The rule is
# about the corpus we write, so it checks the corpus we write.
#
# "Full words, not truncations" is NOT here: it is undecidable in general, so it is
# enforced by declaration instead — core/SCHEMA.md § Retired tokens, checked by
# entropy_ledger.py. A truncation becomes catchable the moment someone retires it.
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from platform_law import posix  # noqa: E402

# A finding is TEXT: it lands in ISSUES.md and is matched against baselines spelled with `/`.
# Spelled by the seam so the same file produces the same finding on every machine — a `\` here
# silently un-baselined every waiver and reported reviewed exceptions as new violations.
def _head(path) -> str:
    return posix(path)


AUTHORED = {'.md', '.py', '.ts', '.tsx', '.js', '.jsx', '.sh', '.dart',
            '.yaml', '.yml', '.json', '.css', '.scss', '.tex'}

# A leading underscore marks scaffolding (_template.md, _material/), a leading dot marks
# a config file (.agentrc.json); dots and underscores are allowed inside a stem because
# Python modules are snake_case by their own law, and `__init__` is mandated by it.
STEM_OK = re.compile(r'^[_.]?[a-z0-9]+([-_.][a-z0-9]+)*$|^__[a-z0-9]+__$')
# Scaffolding directories hold shapes, not instances: a template README.md is a template,
# not a claim that the directory is a repo.
SCAFFOLD_DIR = re.compile(r'^_')
UPPERCASE_MD = re.compile(r'^[A-Z][A-Z0-9_.-]*\.md$')
# The sanctioned second shape: ROADMAP-<slug>.md (AGENTS.md — a plan may live in a
# ROADMAP-<slug>.md referenced from the ROADMAP).
TYPE_SLUG = re.compile(r'^([A-Z][A-Z0-9_-]*)-([a-z0-9]+(?:-[a-z0-9]+)*)$')
DIR_OK = re.compile(r'^[_.]?[a-z0-9]+([-_.][a-z0-9]+)*$')
# academy/papers/<year>-<VENUE>-<slug>: the venue is an acronym and is uppercase in every
# citation of it. A convention that is correct in the outside world outranks ours.
PAPER_DIR = re.compile(r'^\d{4}-[A-Z0-9]+-[a-z0-9][a-z0-9_-]*$')
UNTYPEABLE = re.compile(r'\s|[^\x00-\x7f]')

# The JS/TS ecosystem names components PascalCase and hooks/utils camelCase. That is its
# law the way snake_case is Python's, and a checker that fights it just gets switched off.
JS_LIKE = {'.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs'}
JS_STEM = re.compile(r'^[A-Za-z][A-Za-z0-9]*(\.[A-Za-z0-9]+)*$')


def check_shape(path: Path, allowed: set) -> str | None:
    """Filename shape: lowercase instance, allowlisted type, or TYPE-slug."""
    if path.suffix not in AUTHORED:
        return None
    name = path.name
    if UNTYPEABLE.search(name):
        return (f'{_head(path)}: filename carries a space or a non-ASCII character.\n'
                f'   Authored files are kebab-case ASCII — they get typed, quoted and\n'
                f'   grepped constantly, and a space breaks all three.')
    if UPPERCASE_MD.match(name):
        return None  # a type name; type-gate.py owns the allowlist question
    stem = name[:-len(path.suffix)]
    if path.suffix in JS_LIKE and JS_STEM.match(stem):
        return None
    typed = TYPE_SLUG.match(stem)
    if typed and f'{typed.group(1)}.md' in allowed and path.suffix == '.md':
        return None
    if STEM_OK.match(stem):
        return None
    return (f"{_head(path)}: '{name}' is neither a lowercase instance nor a known type.\n"
            f'   Lowercase instances are kebab-case (snake_case for Python modules);\n'
            f'   a type is UPPERCASE.md, optionally TYPE-<slug>.md. The mixed\n'
            f'   <slug>.TYPE.md shape is retired (core/SCHEMA.md § The `.md` type system).')


def check_dirs(path: Path, root: Path) -> str | None:
    """Every directory holding authored files is lowercase — case-only differences are
    invisible on macOS and fatal on Linux, and a path is typed far more often than read."""
    if path.suffix not in AUTHORED:
        return None
    try:
        parts = path.resolve().relative_to(root).parts[:-1]
    except ValueError:
        parts = path.parts[:-1]
    bad = next(((i, p) for i, p in enumerate(parts)
                if not DIR_OK.match(p) and not PAPER_DIR.match(p)), None)
    if bad is None:
        return None
    index, name = bad
    # Anchor the finding on the DIRECTORY, not the file: one bad directory holding 82
    # files is one violation with one fix, and reporting it 82 times buries the other 81
    # findings on the dashboard.
    return (f"{'/'.join(parts[:index + 1])}: directory {name!r} is not lowercase "
            f'kebab-case.\n'
            f'   Directories are lowercase; only .md types are uppercase.')


def check_placement(path: Path, scopes: dict, root: Path) -> str | None:
    """A type that declares a scope in core/SCHEMA.md must live inside it."""
    scope = scopes.get(path.name)
    if scope is None or any(SCAFFOLD_DIR.match(p) for p in path.parts):
        return None
    parent = path.resolve().parent
    if scope == 'root':
        if parent != root.resolve():
            return (f'{_head(path)}: {path.name} is declared root-only in core/SCHEMA.md.\n'
                    f'   A second one competes with the first for the same authority.')
    elif scope == 'repo-root' and not (parent / '.git').exists():
        return (f'{_head(path)}: {path.name} is declared repo-root-only in core/SCHEMA.md.\n'
                f'   It answers "I just cloned this" — a directory nobody clones does\n'
                f'   not get one; describe it in CONTEXT.md instead.')
    return None
