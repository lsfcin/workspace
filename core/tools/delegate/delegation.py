# delegation.py — the delegation contract as text: read one, refuse what v0 cannot keep, build the worker's prompt from it, and read, flag and cut what came back. Pure: no call, no disk write.
#
# WHY YAML FRONTMATTER. A `key: value` block broke the moment a check command held a colon (panel
# argon, 2026-11-26, outputs/delegate-v0-contract-panel.md); a YAML frontmatter is parsed by a real
# parser and still reads as text. Lucas ruled it 2026-11-26.
#
# WHY THE PREFIX IS STABLE. Role pre-prompt, then the return format, then the task: every provider
# caches a prompt's prefix, so the part that never changes goes first (core/ROADMAP-workers.md).
#
# WHY NO CONFIDENCE. A worker's self-rated confidence is overconfident (Xiong et al. 2024); it lists
# its assumptions, what it did not verify and what of the task it left untouched, and any item in
# any of the three sends the answer to review.
from __future__ import annotations

import pathlib
import re

import yaml

CHARS_PER_TOKEN = 4
CONTEXT_TOKENS = 3000   # inline up to here; larger goes by path, to a worker that reads files
RETURN_TOKENS = 1500    # what the orchestrator reads of an answer; the rest stays in the full file
STATUSES = ('ok', 'blocked', 'split', 'fail')
LISTS = ('Assumptions', 'Unverified', 'Left untouched')
RETURN_FORMAT = '''Reply in exactly this shape, the headings verbatim:
status: ok | blocked | split | fail
## Answer
<the answer>
## Assumptions
- <each assumption you made>, or: none
## Unverified
- <each claim you did not check yourself>, or: none
## Left untouched
- <each part of the task you did not cover>, or: none
## Questions
<only when blocked: what you searched, then at most 3 questions>
## Subtasks
<only when split: one subtask per line, no deeper>
Never rate your own confidence.'''
# Only the contract's own headings split a text: a worker's `## Finding 1` stays inside its Answer (argon, 2026-11-26).
HEADINGS = ('Context', 'Last Failure', 'Answer', *LISTS, 'Questions', 'Subtasks')
_SECTION = re.compile(r'(?m)^## (' + '|'.join(HEADINGS) + r')[ \t]*\r?$')


def is_contract(text: str) -> bool:
    return text.startswith('---\n') and '\n---\n' in text[4:]


def sections(body: str) -> dict:
    """{heading: text} for every `## heading` in the body, in order."""
    parts = _SECTION.split(body)
    return {parts[i]: parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}


def parse(text: str) -> dict:
    """The frontmatter as a dict, `attempt` as (n, of), and the body's sections under 'sections'."""
    if not is_contract(text):
        raise ValueError('a contract starts with a --- YAML frontmatter --- block')
    head, body = text[4:].split('\n---\n', 1)
    c = yaml.safe_load(head) or {}
    n, _, of = str(c.get('attempt', '1/2')).partition('/')
    c['attempt'] = (int(n), int(of or 2))
    for key in ('read_paths', 'write_paths', 'checks'):
        c[key] = c.get(key) or []
    c['sections'] = sections(body)
    return c


def validate(c: dict, works: set, roles: set) -> None:
    """ValueError naming the first thing a v0 run cannot keep: read-only, answer mode, ≤2 tries."""
    missing = [k for k in ('goal', 'work', 'role', 'return') if not c.get(k)]
    n, of = c['attempt']
    problems = [f'missing {", ".join(missing)}' if missing else '',
                'v0 runs return: answer only' if c.get('return') != 'answer' else '',
                'v0 is read-only: write_paths must be empty' if c['write_paths'] else '',
                'checks run from v1 (artifact, patch), never on an answer' if c['checks'] else '',
                f'work {c.get("work")!r} is not in core/levels.txt' if c.get('work') not in works else '',
                f'role {c.get("role")!r} is not in core/tools/delegate/roles.txt' if c.get('role') not in roles else '',
                f'attempt {n}/{of}: at most 2 tries, and n ≤ of' if not 1 <= n <= of <= 2 else '',
                'attempt 2 needs a ## Last Failure section' if n > 1 and 'Last Failure' not in c['sections'] else '']
    if bad := next((p for p in problems if p), ''):
        raise ValueError(f'contract: {bad}')


def bundle(paths: list, root: pathlib.Path, budget: int = CONTEXT_TOKENS * CHARS_PER_TOKEN) -> tuple:
    """(inline text, paths left to read): each file inlined while the budget lasts, in order."""
    inline, by_path, used = [], [], 0
    for p in paths:
        f = root / p
        if not f.is_file():
            raise ValueError(f'contract: read_paths names {p}, which does not exist')
        text = f.read_text(encoding='utf-8', errors='replace')
        if used + len(text) <= budget:
            inline.append(f'### {p}\n{text}')
            used += len(text)
        else:
            by_path.append(p)
    return '\n\n'.join(inline), by_path


def prompt(c: dict, inline: str, by_path: list) -> str:
    """The return format, then the task: the caller puts the role's pre-prompt before it."""
    s = c['sections']
    task = [f'# Task\ngoal: {c["goal"]}\nwork: {c["work"]}  (attempt {c["attempt"][0]} of {c["attempt"][1]})']
    task += [f'## {k}\n{s[k]}' for k in ('Context', 'Last Failure') if k in s]
    task += [f'## Files\n{inline}'] if inline else []
    task += [f'## Files to read yourself\n' + '\n'.join(by_path)] if by_path else []
    return f'{RETURN_FORMAT}\n\n' + '\n\n'.join(task) + '\n'


def read(text: str) -> dict:
    """status, the check (- or bad-format), and whether any of the three lists sends it to review."""
    first = next((l for l in text.splitlines() if l.strip()), '')
    first = first.replace('*', '').replace('`', '').strip().lower()
    status = first.partition(':')[2].strip() if first.startswith('status:') else ''
    s = sections(text)
    items = lambda k: [l for l in s.get(k, '').splitlines() if l.strip().lstrip('-* ').strip('.()').lower() not in ('', 'none', 'n/a')]  # noqa: E731
    asked = [l for l in items('Questions') if l.rstrip().endswith('?')]  # what it searched is prose, not a question
    bad = (status not in STATUSES or not s.get('Answer') or not all(k in s for k in LISTS)
           or (status == 'blocked' and not 1 <= len(asked) <= 3)
           or (status == 'split' and not items('Subtasks')))
    return {'status': status or '-', 'check': 'bad-format' if bad else '-',
            'review': any(items(k) for k in LISTS)}


def cut(text: str, limit: int = RETURN_TOKENS, full: str = '') -> str:
    """At most `limit` tokens: the Answer's middle goes, its head and tail and every other field stay."""
    room = limit * CHARS_PER_TOKEN
    if len(text) <= room:
        return text
    heads = [h for h in _SECTION.finditer(text)]
    at = next((i for i, h in enumerate(heads) if h.group(1) == 'Answer'), None)
    start, end = (heads[at].end() + 1, heads[at + 1].start() if at + 1 < len(heads) else len(text)) if at is not None else (0, len(text))
    mark = f'\n[… cut — the full answer: {full}]\n'
    keep = max(0, room - (len(text) - (end - start)) - len(mark))
    return text[:start] + text[start:start + keep // 2] + mark + text[end - keep // 2:end] + text[end:]
