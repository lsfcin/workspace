# crossing.py — what crosses into the public repo and what does not: the floor, the claims,
# and the import closure that turns a claim on one file into the files it cannot run without.
#
# THE ORPHAN LIST IS THE POINT, not a by-product. A file no feature claims is not merely absent
# from the public repo — it is a file this workspace carries without being able to say what for,
# which is the cutting campaign's input (ROADMAP.md § Portability). So nothing crosses by default
# and "unowned" is reported rather than waved through (Lucas, 2026-09-15).
from __future__ import annotations
import ast, pathlib, subprocess
from typing import NamedTuple

ROOT = pathlib.Path(__file__).resolve().parents[4]
FLOOR = ROOT / 'core/public.txt'
REGISTRY = ROOT / 'core/features.txt'


class Floor(NamedTuple):
    target: pathlib.Path
    roots: tuple[str, ...]
    files: tuple[str, ...]
    absent: dict[str, str]


def floor() -> Floor:
    target, roots, files, absent = None, [], [], {}
    for line in FLOOR.read_text(encoding='utf-8').split('\n'):
        if line.startswith('#') or not line.strip() or line.startswith('kind\t'):
            continue
        kind, path, reason = line.split('\t', 2)
        if kind == 'target':
            target = ROOT / path
        elif kind == 'root':
            roots.append(path)
        elif kind == 'file':
            files.append(path)
        elif kind == 'absent':
            absent[path] = reason
    assert target is not None, f'{FLOOR} names no target'
    return Floor(target, tuple(roots), tuple(files), absent)


def tracked() -> list[str]:
    """What a clone would get. The .gitignore allowlist already answers this question for the whole
    workspace, and asking git rather than re-deriving it is what keeps one answer in one place."""
    out = subprocess.run(['git', '-C', str(ROOT), 'ls-files'],
                         capture_output=True, text=True, encoding='utf-8', check=True)
    return out.stdout.split('\n')


def eligible(f: Floor) -> set[str]:
    """Tracked AND under the floor. Still not crossing — nothing crosses until a feature claims it."""
    return {p for p in tracked() if p and
            (p in f.files or any(p.startswith(r + '/') for r in f.roots))}


class Claim(NamedTuple):
    path: str
    feature: str


def claims() -> list[Claim]:
    """Every file a general-scoped feature names as its switch. A `lucas` row claims nothing: the
    capability is bound to one of Lucas's projects, so the public repo has no use for its files."""
    rows = REGISTRY.read_text(encoding='utf-8').split('\n')
    out = []
    for line in rows:
        if line.startswith('#') or '\t' not in line or line.startswith('name\t'):
            continue
        col = line.split('\t')
        if len(col) < 7 or col[5] != 'general':
            continue
        for path in col[6].split(','):
            path = path.strip()
            # `n/a <reason>` is machine state no code here authors, and `-` is a finding the
            # registry already counts. Neither names a file.
            if path and path != '-' and not path.startswith('n/a'):
                out.append(Claim(path, col[0]))
    return out


def _imports(path: pathlib.Path) -> set[str]:
    """Module names this file imports. An extensionless tool entrypoint is Python too, so it is
    parsed the same way — core/hooks/file_law.py's is_tool_entrypoint is the definition of which
    files those are, and the shape is what says so, never an extension."""
    try:
        tree = ast.parse(path.read_text(encoding='utf-8'))
    except (OSError, SyntaxError, UnicodeDecodeError):
        return set()
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name.split('.')[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module.split('.')[0])
    return names


# Where a sibling module is looked for. These are the directories the tools and hooks insert into
# sys.path themselves, so the list is a reading of what the code does rather than a policy.
SEARCH = ('core/tools', 'core/hooks', 'core/tools/wos', 'core/tools/verify')


def _resolve(name: str, importer: str, pool: set[str]) -> str | None:
    here = str(pathlib.PurePosixPath(importer).parent)
    for directory in (here, *SEARCH):
        candidate = f'{directory}/{name}.py'
        if candidate in pool:
            return candidate
    return None


def closure(seeds: list[str], pool: set[str]) -> set[str]:
    """A claim on one file pulls in what that file cannot run without. Without this every feature
    would have to restate its own import graph in the registry, and a registry that restates what
    the code already says is the drift these checks exist to catch."""
    reached, queue = set(), [s for s in seeds if s in pool]
    while queue:
        current = queue.pop()
        if current in reached:
            continue
        reached.add(current)
        for name in _imports(ROOT / current):
            found = _resolve(name, current, pool)
            if found and found not in reached:
                queue.append(found)
    return reached


class Report(NamedTuple):
    crossing: set[str]
    orphans: set[str]
    unclaimed_imports: list[tuple[str, str]]
    by_feature: dict[str, set[str]]


# A generated interface is not authored and so is claimed by nobody, but it is worthless apart from
# the file it describes and the read gate hands it to an agent INSTEAD of that file. So it is
# paired, never claimed: it crosses exactly when its source does, and a feature that had to name
# both would be restating what the generator already knows.
GENERATED = {'.py': '.pyi', '.ts': '.d.ts'}


def _paired(crossing: set[str], pool: set[str]) -> set[str]:
    out = set()
    for path in crossing:
        for suffix, stub in GENERATED.items():
            if path.endswith(suffix) and (candidate := path[:-len(suffix)] + stub) in pool:
                out.add(candidate)
    return out


def report() -> Report:
    f = floor()
    pool = eligible(f)
    seeds = claims()
    # A `file` row is substrate: SETUP.md § substrate names the category — what every feature runs
    # on, which installs no feature and gets no registry row. The floor names each one with its
    # reason, and that IS the claim; asking a feature to claim verify.py would invent an owner.
    crossing = closure([c.path for c in seeds] + list(f.files), pool)
    crossing |= _paired(crossing, pool)
    by_feature: dict[str, set[str]] = {}
    for claim in seeds:
        if claim.path in pool:
            by_feature.setdefault(claim.feature, set()).add(claim.path)
    # An import that leaves the pool is a feature reaching for a file the floor refuses, which is
    # a finding about the claim and not about the file.
    escaping = []
    for path in sorted(crossing):
        for name in _imports(ROOT / path):
            if _resolve(name, path, pool) is None and (ROOT / f'{name}.py').exists():
                escaping.append((path, name))
    return Report(crossing, pool - crossing, escaping, by_feature)
