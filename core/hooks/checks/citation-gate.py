#!/usr/bin/env python3
# Tier 0: a roadmap item number is not a citable identifier outside the roadmap family.
#
# Why this is a check and not a paragraph. Completion is deletion in this workspace, so the
# day an item closes, every `Front 4.1` pointing at it becomes a pointer to nothing — or
# worse, to whatever item later takes that number. § How to read this has asked for durable
# pointers since 2026-08-15 and the corpus still reached 91 numbered citations across ~50
# files, including two pointing at Fronts 2 and 6, which have never existed. The rule was
# INDUCED; this is the ENFORCED half.
#
# It lives here rather than in entropy/ because the fanout gate said so: entropy/ was already
# at eight code files and the ratchet refused a ninth. That was the right refusal — the check
# belongs beside type-gate.py, which is the other Tier 0 vocabulary gate, and being here made
# it a commit-time BLOCK instead of one more line in a report nobody is obliged to read.
#
# Not a ratchet, unlike type-gate.py: the corpus was swept to zero on 2026-08-16, so every
# staged file is checked rather than only the ones a commit adds. A ratchet is what you use
# when you inherit violations, and there are none left to inherit.
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import feature_law  # noqa: E402

# `Front 9`, `Front 4.1`, `Front 10.1b` — the bare form is the larger half of the corpus and
# the one a decimals-only pattern misses. Hyphen and word boundaries both count, so
# `Front 4`-in-a-compound is caught the same way a retired token is.
CITATION = re.compile(r'(?<!\w)Front \d+(?:\.\d+[a-z]?)?(?!\w)')

# The pre-2026-08-16 spelling. This check owns the rename rather than
# core/SCHEMA.md § Retired tokens, because that table matches a bare word and
# `frente` is an
# ordinary Portuguese noun — it means a work front, and `branches/casinhas/CONTEXT.md` uses it
# that way in a table header about construction. A retired-token row would have failed on
# honest Portuguese prose on the day it was written, which SCHEMA.md's own note says trains
# people to ignore a check. Matching the *citation shape* instead keeps the word legal and the
# pointer illegal. Unlike CITATION this is a hit EVERYWHERE, roadmaps included: a rename is
# finished only when the old spelling appears nowhere.
RETIRED_SPELLING = re.compile(r'(?<!\w)Frente \d+(?:\.\d+[a-z]?)?(?!\w)')

# The ledger family may number its own items: that is what numbering is FOR, and a commit
# message may cite one too, because git keeps commits forever. Matched on filename, not path,
# so a `ROADMAP-<slug>.md` in any repo under the workspace is covered without enumeration.
LEDGER_NAMES = re.compile(r'^ROADMAP(-[a-z0-9-]+)?\.md$')

# The two documents that state the rule, the report that quotes findings, and this checker
# with its tests all have to be able to NAME the shape they forbid. Nothing else may.
# core/hooks/SPECS.md joined this list by failing the check the moment it documented the gate,
# which is the same argument core/SCHEMA.md was already on it for.
ENFORCEMENT = ('core/SCHEMA.md', 'core/hooks/SPECS.md', 'ISSUES.md')
# Derived from __file__, never spelled out: a hard-coded path here stops exempting this
# checker the moment the hooks directory moves, which is what happened to the sibling
# exemption in entropy_corpus.py when the hooks moved into core/ (2026-07-31).
_CHECKER = 'citation-gate.py'
_CHECKER_TESTS = 'core/tools/test/**/test_citation_gate.py*'

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]


def citation_exempt_paths(root: Path) -> set:
    """Files allowed to contain a Front number: the law, the report, and this check itself.

    A shard of an exempt file inherits the exemption, derived rather than listed. Enumerating
    them would fail the first time one of these documents outgrew the line cap, which is exactly
    what happened to `core/hooks/SPECS.md` — its § Git pre-commit section, which has to name the
    shape this gate forbids, moved into a sibling and stopped being exempt on arrival.
    """
    named = [root / name for name in ENFORCEMENT]
    return ({p.resolve() for p in named}
            | {s.resolve() for p in named for s in p.parent.glob(f'{p.stem}-*{p.suffix}')}
            | {Path(__file__).resolve().parent / _CHECKER}
            | {p.resolve() for p in root.glob(_CHECKER_TESTS)})


def staged_files() -> list:
    """Every file this commit touches, added or modified — not only what it adds."""
    out = subprocess.run(
        ['git', 'diff', '--cached', '--name-only', '--diff-filter=d'],
        capture_output=True, text=True, encoding='utf-8').stdout
    return [WORKSPACE_ROOT / line for line in out.splitlines()]


def citation_hits(files: list, exempt: set) -> list:
    """Item numbers cited outside a roadmap, plus the retired spelling cited anywhere."""
    exempt = {path.resolve() for path in exempt}
    hits = []
    for path in files:
        if path.resolve() in exempt:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        if match := RETIRED_SPELLING.search(text):
            line = text[:match.start()].count('\n') + 1
            hits.append(
                f'{path}: cites {match.group(0)!r} (line {line}).\n'
                f'   `Frente` was renamed to `Front` 2026-08-16 —\n'
                f'   core/SCHEMA.md § Vocabulary.\n'
                f'   Rename it, then apply the rule below: a number is legal only in ROADMAP*.md.')
            continue
        if LEDGER_NAMES.match(path.name):
            continue
        if match := CITATION.search(text):
            line = text[:match.start()].count('\n') + 1
            hits.append(
                f'{path}: cites {match.group(0)!r} (line {line}).\n'
                f'   A closed item is deleted, so its number becomes a dead pointer.\n'
                f'   Point at the SPECS.md or SCHEMA.md section that owns the rule, or\n'
                f'   name the concept. Numbering is legal only inside ROADMAP*.md.')
    return hits


def main() -> int:
    if not feature_law.is_enabled('citation-gate'):
        return 0  # switched off: a disabled gate does not block, and does not pretend it ran
    if not (WORKSPACE_ROOT / 'core/SCHEMA.md').exists():
        return 0  # not the workspace repo; nothing to enforce against
    staged = [p for p in staged_files() if p.exists()]
    hits = citation_hits(staged, citation_exempt_paths(WORKSPACE_ROOT))
    if hits:
        print('⛔ citation gate:')
        for hit in hits:
            print(f'   {hit}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
