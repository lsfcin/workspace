# Read a repository's current ROADMAP priorities and check its handoff pointers.
import re
import subprocess
from datetime import date
from pathlib import Path

TAG = re.compile(r'\[([a-z0-9-]+)\]')
ITEM = re.compile(r'^\*\*[^\x00-\x7f\s]+\s+' + TAG.pattern + r'.*?\*\*')
ISSUE_ID = r'b[0-9]{8}-[a-z0-9-]+'
HANDOFF_HEADERS = {'Next action', 'Worked on', 'Decided without asking', 'State'}


def _git(repo: Path, *args: str) -> str:
    try:
        result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True,
                                text=True, encoding='utf-8')
    except (OSError, UnicodeError):
        return ''
    return result.stdout if result.returncode == 0 else ''


def _lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding='utf-8').splitlines()
    except FileNotFoundError:
        return []


def roadmaps(repo: Path) -> list[Path]:
    paths = _git(repo, 'ls-files', '-z', '--', ':(glob)**/ROADMAP*.md')
    return [repo / name for name in paths.split('\0') if name]


def defined(repo: Path) -> dict[str, str]:
    items = {}
    for path in roadmaps(repo):
        lines = _lines(path)
        in_agora, start, tag = False, 0, None
        for end, line in enumerate([*lines, '## ']):
            if not line.startswith(('**', '## ')):
                continue
            if tag:
                items[tag[1]] = '\n'.join(lines[start:end]).rstrip()
            if line.startswith('## '):
                in_agora = line.rstrip() == '## Agora'
            start, tag = end, ITEM.match(line) if not in_agora else None
    return items


def _agora_lines(repo: Path) -> list[str] | None:
    lines = _lines(repo / 'ROADMAP.md')
    for index, line in enumerate(lines):
        if line.rstrip() == '## Agora':
            pointers = []
            for line in lines[index + 1:]:
                if line.startswith('## '):
                    break
                if line.strip():
                    pointers.append(line)
            return pointers
    return None


def has_agora(repo: Path) -> bool:
    return _agora_lines(repo) is not None


def agora(repo: Path) -> list[str]:
    return _agora_lines(repo) or []


def issue_ids(repo: Path) -> set[str]:
    return set(re.findall(rf'`({ISSUE_ID})`', '\n'.join(_lines(repo / 'ISSUES.md'))))


def _problems(lines: list[str], items: dict[str, str]) -> list[str]:
    errors = []
    if len(lines) > 3:
        errors.append(f'## Agora has {len(lines)} lines (maximum 3)')
    for line in lines:
        tags = TAG.findall(line)
        if not tags:
            errors.append(f'## Agora line has no [tag]: {line}')
        errors.extend(f'## Agora tag [{tag}] is not defined in this repo' for tag in tags if tag not in items)
    return errors


def problems(repo: Path) -> list[str]:
    return _problems(agora(repo), defined(repo))


def handoff_problems(text: str, repo: Path) -> list[str]:
    lines = _agora_lines(repo)
    items = defined(repo)
    errors = _problems(lines or [], items)
    if lines is None:
        errors.append(f'the close creates {Path(repo).resolve().name}/ROADMAP.md with a ## Agora before handing off')

    visible = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    parts = re.split(r'^### (.*)$', visible, flags=re.M)
    next_action = []
    for heading, body in zip(parts[1::2], parts[2::2]):
        heading = heading.rstrip()
        if heading == 'Open threads':
            errors.append('Open threads is gone: move each thread to its ROADMAP or ISSUES, or drop it')
        elif heading not in HANDOFF_HEADERS:
            errors.append(f'Unexpected handoff header: ### {heading}')
        elif heading == 'Next action':
            next_action.append(body)
    body = '\n'.join(next_action)
    tags = set(TAG.findall(body))
    errors.extend(f'Next action tag [{tag}] is not defined in this repo' for tag in sorted(tags - items.keys()))
    cited_issues = set(re.findall(rf'(?<![\w-]){ISSUE_ID}(?![\w-])', body))
    if not (tags & items.keys() or re.search(r'\bnone\b', body, re.I) or cited_issues & issue_ids(repo)):
        errors.append('Next action must cite a defined ROADMAP [tag], an existing ISSUES id, or none')

    count = len(re.split(r'^### State[ \t]*\r?$', visible, maxsplit=1, flags=re.M)[0])
    if count > 600:
        errors.append(f'Handoff has {count} characters (maximum 600): point at ROADMAP/ISSUES instead of restating them')
    return errors


def age(repo: Path) -> int | None:
    log = _git(repo, 'log', '-1', '--format=%cs', '-L', '/^## Agora/,+5:ROADMAP.md')
    match = re.search(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', log, re.M)
    try:
        return (date.today() - date.fromisoformat(match[0])).days if match else None
    except ValueError:
        return None


def brief(repo: Path) -> str:
    issues_path = repo / 'ISSUES.md'
    if not (repo / 'ROADMAP.md').is_file() and not issues_path.is_file():
        return ''
    issues = sum(line.startswith('- **') for line in _lines(issues_path))
    issues_line = f'ISSUES: {issues} open'
    lines = _agora_lines(repo)
    if lines is None:
        return f'No ## Agora in {Path(repo).resolve().name}/ROADMAP.md: rank one before planning (≤3 [tag] pointers).\n{issues_line}'
    days = age(repo)
    changed = f', last changed {days}d ago' if days is not None else ''
    heading = f'## Agora — {Path(repo).resolve().name} (ROADMAP.md{changed})'
    plan = ("The plan picks: the handoff's Next action or an Agora item, and says why. "
            'Read the whole ROADMAP; if the Agora is wrong, re-rank it before working.')
    return '\n'.join([heading, *lines, issues_line, plan])


def item(repo: Path, name: str) -> str | None:
    return defined(repo).get(name)
