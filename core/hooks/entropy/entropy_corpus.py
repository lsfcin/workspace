#!/usr/bin/env python3
# Which files the Tier 0 checks look at, and which of them are allowed to name what the
# checks forbid. Split from entropy_ledger.py 2026-07-30 at the 150-line warn: enumerating
# the corpus is a different job from asserting things about it.
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from platform_law import posix  # noqa: E402

# What a markdown link looks like, defined once. Two checks ask different questions of the same
# syntax — core/tools/test/workspace/test_pointer_integrity.py asks whether a target EXISTS and
# blocks, entropy_naming.untracked_routing_targets asks whether git CARRIES it and reports — and a
# second copy of the pattern is where those two would start disagreeing about what a link is.
LINK_RE = re.compile(r'!?\[[^\]]*\]\(([^)\s]+)\)')

SCANNED = {'.md', '.py', '.ts', '.tsx', '.js', '.jsx', '.sh', '.dart',
           '.yaml', '.yml', '.json', '.css', '.scss', '.tex', ''}

# Never walked: build output, caches, and the two directories that inflated every earlier
# measurement of this workspace (.venv 7.6 GB, .Trash-1000 6.6 GB).
SKIP_DIRS = {'.venv', 'node_modules', '.mypy_cache', '.pytest_cache', '.Trash-1000',
             '$RECYCLE.BIN', 'System Volume Information', 'outputs', 'tmp', 'models',
             'Downloads'}

def staged_added_files() -> list:
    """Only files this commit ADDS — the ratchet every Tier 0 gate shares.

    Renames count as adds of the new name: a file arriving under a new name is arriving,
    and the gates that read this all ask about the name and the content it lands with.
    Lives here rather than in a checker because three gates need it and the third copy is
    where the definitions start to disagree.
    """
    out = subprocess.run(['git', 'diff', '--cached', '--name-only', '--diff-filter=AR'],
                         capture_output=True, text=True).stdout
    return [Path(line) for line in out.splitlines()]


def tracked_files(root: Path, nested: bool = False) -> list:
    """Text files git tracks, relative to root. git is the inventory; find is not.

    `nested` also walks the 24 repos living inside the workspace. The dashboard wants
    them — entropy does not stop at a repo boundary. Tests do NOT: an assertion in this
    repo about another repo's content fails for reasons this repo cannot fix, and each
    nested repo runs its own verify.
    """
    files = []
    for repo in [root] + (sorted(nested_repos(root)) if nested else []):
        out = subprocess.run(['git', '-C', str(repo), 'ls-files'],
                             capture_output=True, text=True).stdout
        files += [repo / line for line in out.splitlines()
                  if Path(line).suffix.lower() in SCANNED]
    return files


def tracked_paths(root: Path, nested: bool = False) -> set:
    """EVERY path git tracks, with no extension filter — the inventory, not the corpus.

    `tracked_files` above answers "what may a check read", and drops anything outside SCANNED on
    the way. Asking it "does git carry this?" gets the wrong answer for every tracked `.pyi`,
    `.texif`, `.png` or `.tex`: 204 of them read as untracked the first time
    entropy_naming.untracked_routing_targets was pointed at it. Two questions, two functions.
    """
    paths = set()
    for repo in [root] + (sorted(nested_repos(root)) if nested else []):
        out = subprocess.run(['git', '-C', str(repo), 'ls-files'],
                             capture_output=True, text=True).stdout
        paths |= {(repo / line).resolve() for line in out.splitlines()}
    return paths


def owning_repo(path: Path, root: Path) -> Path:
    """The repo a file really belongs to. A nested repo's file is tracked THERE, and charging it
    to this one reports 27 papers and modules as untracked on every run.

    `path` itself counts, not only its parents: a repo belongs to itself. Asking about the
    DIRECTORY `code/aiwbot` — which is what a routing row for a nested project is — walked
    straight past its own `.git`, called root the owner, and root's .gitignore names every
    nested repo wholesale, so `code/CONTEXT.md` lost all 15 project rows at once.
    """
    return next((d.resolve() for d in [path, *path.parents] if (d / '.git').exists()),
                root.resolve())


def ignored_here(paths: list, root: Path) -> set:
    """Of these, the ones git is TOLD to ignore — the paths a clone never receives.

    `tracked_paths` answers what a clone has today; this answers what it will never get, and the
    routing generator needs the second question rather than the first. An untracked file that is
    merely new is one commit from being carried and must keep its row; an ignored one is carried
    by nothing, ever, and a row for it ships a table pointing at absence.

    A nested repo's file is never ignored *here*: root's .gitignore names those directories
    wholesale, and asking this repo about them would strip every project row out of
    `code/CONTEXT.md`. Same boundary `owning_repo` draws for the check above it.
    """
    mine = [p for p in paths if owning_repo(p, root) == root.resolve()]
    if not mine:
        return set()
    out = subprocess.run(['git', '-C', str(root), 'check-ignore', '--stdin'],
                         input='\n'.join(str(p) for p in mine),
                         capture_output=True, text=True).stdout
    return {Path(line).resolve() for line in out.splitlines()}


def nested_repos(root: Path, depth: int = 3) -> list:
    """Repos inside the workspace. Bounded walk — an unbounded one costs 14 GB of .venv
    and trash, which is how earlier counts of this workspace came out wrong twice."""
    found = []
    def walk(directory: Path, level: int):
        if level > depth:
            return
        for child in directory.iterdir():
            if not child.is_dir() or child.name.startswith('.') or child.name in SKIP_DIRS:
                continue
            if (child / '.git').exists():
                found.append(child)
            else:
                walk(child, level + 1)
    walk(root, 0)
    return found


# Generated mirrors: sync-skills rewrites these from core/skills on every run, so a prose
# finding inside one is unfixable in place and is already reported against the source it was
# copied from. Fixing the mirror is fixing the generator.
#
# `.zcode/skills/` joined 2026-08-24 — the mirror landed when ZCode was registered and this list
# did not follow it, so the new mirror's generated CONTEXT.md was counted as authored prose nobody
# could fix. Only the skills subtree is a mirror: `.zcode/config.json`, `CONTEXT.md` and `SPECS.md`
# are authored and stay in the corpus.
MIRRORS = ('.claude/', '.opencode/', '.github/', '.zcode/skills/')


def is_generated_mirror(path: Path) -> bool:
    # Matched against the SEAM's spelling, never str(). These markers carry `/`, so on a clone
    # where a path stringifies with `\` not one of them matched and every mirror was judged as
    # authored prose — findings against files nobody can edit, in the report that exists to list
    # only what someone can act on.
    return any(part in posix(path) for part in MIRRORS)


# The law, the check that enforces it, that check's tests, and the report that quotes the
# findings all have to be able to NAME a retired token. Nothing else may.
#
# The report moved inside ISSUES.md 2026-08-20, so the exemption follows it — and widens, since a
# file-level list cannot see block boundaries: the hand-written issues above the block may now name
# a retired token too. That is a real loosening and it is the honest one, because an issue is often
# ABOUT a name that should no longer exist.
#
# `core/SCHEMA.md` holds § Retired tokens itself, so it is the one law file that must be able to
# name what it retires. The vocabulary shard came home 2026-08-25 and its separate exemption went
# with it; `SCHEMA-layers.md` has no business naming a retired token and is deliberately absent.
ENFORCEMENT = ('core/SCHEMA.md', 'ISSUES.md')

# The ledger check's own tests, found by name instead of by path. Spelling the path out is
# what broke this exemption the moment core/tools/test was split (2026-07-31) — the same
# defect as the hard-coded sibling path below, one directory over.
_CHECKER_TESTS = ('core/tools/test/**/test_entropy_ledger.py*',
                  'core/tools/test/**/test_entropy_retired.py*')

# The checker and its stub are SIBLINGS of this file, so they are derived rather than
# spelled out. A hard-coded path here stops exempting them the moment the hooks directory
# moves — which is exactly what happened when the hooks moved into `core/` (2026-07-31).
_CHECKER = ('entropy_ledger.py', 'entropy_ledger.pyi')

# Since the entropy scatter every nested repo's ledger carries the same generated block the root's
# does, so the exemption that followed the report into ISSUES.md has to follow it into all of them.
# This is not a courtesy: the report's own section notes name a retired token and spell `[[slug]]`
# literally, so a ledger left unexempt is flagged by the very text the tool wrote into it — the
# check reporting on its own output. Derived from nested_repos rather than a `code/*` glob, which
# is how the exemption stayed correct when the scatter generalised (2026-08-25).
_LOCAL_LEDGER = 'ISSUES.md'


def enforcement_paths(root: Path) -> set:
    here = Path(__file__).resolve().parent
    return ({(root / name).resolve() for name in ENFORCEMENT}
            | {here / name for name in _CHECKER}
            | {p.resolve() for pattern in _CHECKER_TESTS for p in root.glob(pattern)}
            | {(repo / _LOCAL_LEDGER).resolve() for repo in nested_repos(root)})


# brain/memory holds cross-session agent memory, and its `[[slug]]` names ANOTHER MEMORY rather
# than a goal. A slug with no file yet is allowed there on purpose — it marks a memory worth
# writing later. Different vocabulary, different strictness, so the goal check cannot apply.
#
# Only the wiki-link check is relaxed. Retired tokens are still enforced there, and that is not
# hypothetical: the day the store moved into the workspace (2026-08-15) that check caught four
# memories still naming files and flows renamed in July — instructions a future session would have
# followed. Memory rots exactly like documentation, and nothing was watching it before.
MEMORY_DIR = 'brain/memory'


def wiki_exempt_paths(root: Path) -> set:
    return enforcement_paths(root) | {p.resolve() for p in (root / MEMORY_DIR).rglob('*.md')}
