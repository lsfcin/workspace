# Repository/environment handoffs: names and edit counts come from local records, never a model.
import json
import os
import re
import subprocess
from collections import Counter
from pathlib import Path


def name_of(value: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')[:64] or 'workspace'


def identity(session: str = '', agent: str = '') -> tuple[str, str]:
    """Never infer the active session from the newest transcript in a shared directory."""
    if not session:
        if os.environ.get('CODEX_THREAD_ID') or os.environ.get('CODEX_SESSION_ID'):
            session = os.environ.get('CODEX_THREAD_ID') or os.environ['CODEX_SESSION_ID']
            agent = agent or 'chatgpt'
        elif os.environ.get('CLAUDE_SESSION_ID'):
            session, agent = os.environ['CLAUDE_SESSION_ID'], agent or 'claude'
    if not session or not agent:
        raise ValueError('No session identity: pass --session and --agent from the native session metadata.')
    return session, name_of(agent)


def records(path: Path):
    with path.open(encoding='utf-8') as stream:
        for line in stream:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue  # a live transcript can end with an unfinished record
            if isinstance(row, dict):
                yield row


def transcript(session: str, agent: str, cwd: Path, given: str = '') -> Path | None:
    if given:
        path = Path(given)
        # Supplied Claude logs name the session on each record; Codex names it in session_meta.
        owned = any(row.get('sessionId') == session or
                    (row.get('type') == 'session_meta' and row.get('payload', {}).get('id') == session)
                    for row in records(path))
        if not owned:
            raise ValueError('Transcript does not identify the requested session.')
        return path
    if agent == 'chatgpt':
        home = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex')))
        matches = list((home / 'sessions').glob(f'**/*-{session}.jsonl'))
    elif agent == 'claude':
        project = re.sub(r'[^A-Za-z0-9]', '-', str(cwd))
        matches = list((Path.home() / '.claude' / 'projects' / project).glob(f'{session}.jsonl'))
    else:
        matches = []
    if len(matches) > 1:
        raise ValueError('Multiple transcripts for this session; pass --transcript explicitly.')
    return matches[0] if matches else None


def patch_lines(text: str) -> Counter:
    """Count recorded additions + removals; headers and hunk context are not edits."""
    counts, path = Counter(), ''
    for line in text.splitlines():
        if line.startswith(('*** Add File: ', '*** Update File: ', '*** Delete File: ')):
            path = line.split(': ', 1)[1]
        elif line.startswith('*** Move to: '):
            path = line.split(': ', 1)[1]
        elif line.startswith('*** '):
            path = ''
        elif path and line.startswith(('+', '-')):
            counts[path] += 1
    return counts


def successful(output) -> bool:
    """Codex patch results need a positive success marker, not merely an absence of errors."""
    text = json.dumps(output) if not isinstance(output, str) else output
    return 'Success. Updated the following files:' in text and not any(
        word in text for word in ('"isError": true', 'Failed to', 'patch verification failed'))


def edits(path: Path, cwd: Path) -> Counter:
    counts, pending = Counter(), {}
    for row in records(path):
        if row.get('isSidechain'):
            continue
        if row.get('type') == 'turn_context':
            cwd = Path(row.get('payload', {}).get('cwd', cwd))
        payload = row.get('payload', {})
        if row.get('type') == 'response_item':
            kind = payload.get('type')
            if kind in ('custom_tool_call', 'function_call') and payload.get('name', '').split('.')[-1] == 'apply_patch':
                patch = payload.get('input', payload.get('arguments', ''))
                pending[payload.get('call_id')] = (patch_lines(patch), cwd)
            elif kind in ('custom_tool_call_output', 'function_call_output'):
                call = pending.pop(payload.get('call_id'), None)
                if call and successful(payload.get('output')):
                    changes, base = call
                    counts.update({str((base / name).resolve()): n for name, n in changes.items()})
        content = row.get('message', {}).get('content', [])
        for block in content if isinstance(content, list) else []:
            if block.get('type') == 'tool_use' and block.get('name') == 'Edit':
                args = block.get('input', {})
                name = args.get('file_path', '')
                n = len(args.get('old_string', '').splitlines()) + len(args.get('new_string', '').splitlines())
                pending[block.get('id')] = (Counter({name: n}), cwd)
            elif block.get('type') == 'tool_result':
                call = pending.pop(block.get('tool_use_id'), None)
                if call and not block.get('is_error'):
                    changes, base = call
                    counts.update({str((base / name).resolve()): n for name, n in changes.items() if name})
    return counts


def repository(path: Path) -> Path | None:
    while not path.is_dir() and path != path.parent:
        path = path.parent
    result = subprocess.run(['git', '-C', str(path), 'rev-parse', '--show-toplevel'],
                            capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        return None
    common = subprocess.run(['git', '-C', str(path), 'rev-parse', '--path-format=absolute', '--git-common-dir'],
                            capture_output=True, text=True, encoding='utf-8')
    git_dir = Path(common.stdout.strip())
    # Worktrees share a repository; aggregate their lines under the primary checkout.
    return git_dir.parent if common.returncode == 0 and git_dir.name == '.git' else Path(result.stdout.strip())


def choose(root: Path, cwd: Path, session: str, agent: str, log: Path | None) -> dict:
    """Git's shared dirty tree is never evidence of what one session changed."""
    totals, roots = Counter(), {}
    for name, n in edits(log, cwd).items() if log else []:
        path = Path(name)
        if path.is_relative_to(root / 'outputs'):
            continue
        parent = path.parent
        if parent not in roots:
            roots[parent] = repository(parent)
        repo = roots[parent]
        if repo and n:
            totals[str(repo)] += n
    chosen = Path(sorted(totals, key=lambda p: (-totals[p], p))[0]) if totals else repository(cwd)
    name = name_of(chosen.name if chosen else cwd.name)
    marker = '<!-- handoff-session: ' + json.dumps([agent, session]) + ' -->\n'
    target = root / 'outputs' / f'handoff-{name}-{agent}.md'
    return {'path': str(target), 'marker': marker,
            'repository': str(chosen) if chosen else '', 'agent': agent, 'session': session,
            'lines': dict(totals), 'basis': 'confirmed Edit/patch lines' if totals else 'working repository fallback',
            'limitation': 'Shell/script writes, full-file replacements and implicit deletions are not measurable from these records.'}


def publish(info: dict, text: str | None) -> None:
    """Latest publication wins for the pair; an older session cannot clear its replacement."""
    target, marker = Path(info['path']), info['marker']
    target.parent.mkdir(parents=True, exist_ok=True)
    lock = target.with_suffix('.lock')
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    temp = target.with_suffix('.tmp')
    try:
        if text is None:
            if target.exists() and not target.read_text(encoding='utf-8').startswith(marker):
                return  # another session has published a newer handoff for this pair
            target.unlink(missing_ok=True)
        else:
            temp.write_text(marker + text.removeprefix(marker), encoding='utf-8', newline='\n')
            temp.replace(target)
    finally:
        os.close(fd)
        temp.unlink(missing_ok=True)
        lock.unlink()
