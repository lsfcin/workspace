#!/usr/bin/env python3
# The outbox: a note for a repo's ISSUES.md or ROADMAP.md, left by a session that does not hold it.
#
# A drive-by note used to take the whole repo, and held it until a manual claim (b20261121-drive-by-lock).
# Now it waits here, untracked, one JSON row per note under a flock, and the repo's holder folds it in:
# `take` shows what waits, `roundup` lists it, and only the holder clears it — folded, dismissed, or left
# for later when the file sits at its cap (panels codex + argon, Lucas 2026-11-24). Per machine: the
# queue lives in core/state, which no clone shares.
import hashlib
import json
import re
import time
from pathlib import Path

from platform_law import locked, session_state


def path(repo) -> Path:
    return session_state('outbox_' + re.sub(r'[^A-Za-z0-9]', '_', str(Path(repo).resolve())) + '.jsonl')


def pending(repo) -> list:
    """Every note waiting for `repo`, oldest first."""
    rows = path(repo).read_text(encoding='utf-8').splitlines() if path(repo).is_file() else []
    return [json.loads(row) for row in rows if row.strip()]


def add(repo, file: str, text: str, session: str, origin: str = '') -> str:
    """Queue a note; the same text for the same file waits once. Returns its id, a short hash."""
    repo = Path(repo).resolve()
    note = hashlib.sha256(f'{repo}\0{file}\0{text}'.encode()).hexdigest()[:8]
    with locked(path(repo).with_suffix('.flock')):
        if all(row['id'] != note for row in pending(repo)):
            with path(repo).open('a', encoding='utf-8', newline='\n') as rows:
                rows.write(json.dumps({'id': note, 'ts': time.time(), 'session': session, 'repo': str(repo),
                                       'from': origin, 'file': file, 'text': text}, ensure_ascii=False) + '\n')
    return note


def _write(repo, rows: list) -> None:
    if rows:
        path(repo).write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows),
                              encoding='utf-8', newline='\n')
    else:
        path(repo).unlink(missing_ok=True)


def done(repo, ids) -> list:
    """Clear the notes named; returns the ids that were waiting."""
    with locked(path(repo).with_suffix('.flock')):
        rows = pending(repo)
        _write(repo, [row for row in rows if row['id'] not in ids])
    return [row['id'] for row in rows if row['id'] in ids]


def rekey(src, dst) -> None:
    """After a repo's folder moved (core/tools/wos/move): its notes follow, naming the new path."""
    rows = pending(src)
    path(src).unlink(missing_ok=True)
    _write(dst, pending(dst) + [{**row, 'repo': str(Path(dst).resolve())} for row in rows])


def everywhere() -> list:
    """(repo, notes) for every repo something waits for."""
    found = []
    for queue in sorted(session_state('outbox_').parent.glob('outbox_*.jsonl')):
        rows = [json.loads(row) for row in queue.read_text(encoding='utf-8').splitlines() if row.strip()]
        if rows:
            found.append((Path(rows[0]['repo']), rows))
    return found


def line(note: dict) -> str:
    """A note as its file will carry it."""
    day = time.strftime('%Y-%m-%d', time.localtime(note['ts']))
    return f'{note["id"]}  {note["file"]}: {note["text"]} [src: agent {day}]'
