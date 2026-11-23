# workers.py — the one way a tool calls an outside worker (another harness's model): find it, call it, classify what came back, and log who answered.
#
# WHY ONE MODULE. panel/ask and describe.py each built their own vendor call — two ideas of where
# a binary lives, of what a spent quota looks like, of what a timeout leaves running. Their drift
# was found 2026-11-20 (describe's agy skipped the app-path fallback). core/tools/SPECS.md: a module
# imported by more than one family lives at this root.
#
# THE CATALOG IS DATA, THE IDS ARE DATA. Who exists, which id its harness resolves and in which
# order the panel tries them is core/workers.txt; what each model is good for is core/models.txt,
# joined by `model`. Nothing below names a model.
#
# A MISS IS CLASSIFIED, NEVER GUESSED. missing / no-login / quota / timeout / unknown / ok. An error
# matching no known mark is `unknown`, not `quota`: calling a broken call a spent quota hides it.
from __future__ import annotations

import os
import pathlib
import shutil
import signal
import statistics
import subprocess
import tempfile
import time
from typing import NamedTuple

ROOT = pathlib.Path(__file__).resolve().parents[2]
CATALOG = ROOT / 'core' / 'workers.txt'
MODELS = ROOT / 'core' / 'models.txt'
LOG = ROOT / 'core' / 'state' / 'workers.tsv'
TIMEOUT = 900
COOLDOWN_H = 6  # a quota miss keeps a worker out of the chain this long, unless an ok call clears it
HOME = pathlib.Path.home()
# $ENV, then PATH, then where the vendor's app installs it.
PLACES = {
    'codex': ('CODEX', ('/usr/lib/chatgpt/resources/codex',)),
    'agy': ('AGY', (str(HOME / '.local/bin/agy'),)),
    'opencode': ('OPENCODE', (str(HOME / '.opencode/bin/opencode'),)),
    'ollama': ('OLLAMA', ('/usr/local/bin/ollama',)),
    'claude': ('CLAUDE', (str(HOME / '.local/bin/claude'),)),
}
MARKS = {
    'quota': ('usage limit', 'resource_exhausted', 'quota reached', 'quota exceeded', 'rate limit'),
    'no-login': ('not logged in', 'please log in', 'unauthorized', 'login required'),
}
ANSWER_FLOOR = 400  # chars; every vendor's quota or login notice seen so far is under 200


class Result(NamedTuple):
    worker: str
    model: str
    status: str      # ok | missing | no-login | quota | timeout | unknown
    text: str        # the answer when ok, the evidence otherwise
    seconds: float


def table(path: pathlib.Path) -> list[dict]:
    """A hand-written TSV whose header is the last `# a\tb` comment line, as rows in file order."""
    rows, head = [], None
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('# ') and '\t' in line:
            head = line[2:].split('\t')
        elif line.strip() and not line.startswith('#') and head:
            rows.append(dict(zip(head, line.split('\t'))))
    return rows


def catalog() -> list[dict]:
    """core/workers.txt in file order, each row joined to its model's row in core/models.txt."""
    facts = {m['model']: m for m in table(MODELS)}
    return [{**facts.get(r['model'], {}), **r} for r in table(CATALOG)]


def models() -> dict:
    """{worker: the id its harness resolves}."""
    return {r['worker']: r['id'] for r in table(CATALOG)}


def cooling(worker: str, now: str = '') -> str:
    """When the worker's last logged call was a quota miss under COOLDOWN_H before `now`, its time; else ''."""
    last = ''
    if LOG.is_file():
        for line in LOG.read_text(encoding='utf-8').splitlines():
            f = line.split('\t')
            if len(f) >= 5 and f[1] == worker:
                last = f[0] if f[4] == 'quota' else ''
    stamp = lambda s: time.mktime(time.strptime(s, '%Y-%m-%dT%H:%M'))  # noqa: E731
    if last and stamp(now or time.strftime('%Y-%m-%dT%H:%M')) - stamp(last) < COOLDOWN_H * 3600:
        return last
    return ''


def chain(now: str = '') -> list[dict]:
    """The default panel chain: every row with a position, in that order, minus the spent ones."""
    return sorted((r for r in catalog() if r['chain'] != '-' and r['depleted'] == '-' and not cooling(r['worker'], now)),
                  key=lambda r: int(r['chain']))


def find(harness: str) -> str | None:
    env, places = PLACES[harness]
    for cand in (os.environ.get(env), shutil.which(harness), *places):
        if cand and os.access(cand, os.X_OK):
            return cand
    return None


def run(cmd: list[str], cwd: str | None = None, timeout: int = TIMEOUT) -> tuple[int, str]:
    """stdin closed (codex waits on it forever otherwise); stderr kept; on timeout the whole
    process group dies, so a harness's own children never outlive the call."""
    proc = subprocess.Popen(cmd, cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace',
                            start_new_session=True)
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.communicate()
        return 124, f'timed out after {timeout} s'
    return proc.returncode, (out or '') + (err or '')


def classify(code: int, text: str) -> str:
    """ok, or why this is no answer. agy prints a spent quota and may exit 0, so a short reply is
    searched for MARKS; a clean exit with a reply longer than ANSWER_FLOOR is an answer, whatever
    it talks about (argon's verdicts on quota and login were thrown away 2026-11-20 and 11-21)."""
    if code == 0 and len(text.strip()) > ANSWER_FLOOR:
        return 'ok'
    low = text.lower()
    for status, marks in MARKS.items():
        if any(m in low for m in marks):
            return status
    if code == 124:
        return 'timeout'
    if code == 127:
        return 'missing'
    if code != 0 or not text.strip():
        return 'unknown'
    return 'ok'


def _codex(exe, model, prompt, cwd):
    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp) / 'answer.md'
        code, log = run([exe, 'exec', '-s', 'read-only', '-m', model, '-C', cwd, '--ephemeral',
                         '-o', str(out), prompt])
        answer = out.read_text(encoding='utf-8') if out.exists() else ''
    return (0, answer) if code == 0 and answer.strip() else (code or 1, log)


def _agy(exe, model, prompt, cwd):
    return run([exe, '--disable-slash-commands', '--model', model, '-p', prompt], cwd=cwd)


def _opencode(exe, model, prompt, cwd):
    """--format json: the answer is the text parts of the event stream, never the pretty print."""
    import json
    code, raw = run([exe, 'run', '--pure', '--format', 'json', '-m', model, prompt], cwd=cwd)
    parts = []
    for line in raw.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get('type') == 'text':
            parts.append(event['part'].get('text', ''))
        if event.get('type') == 'error':
            return code or 1, line
    return (code, ''.join(parts)) if parts else (code or 1, raw)


def _ollama(exe, model, prompt, cwd):
    return run([exe, 'run', model, prompt], cwd=cwd)


ADAPTERS = {'codex': _codex, 'agy': _agy, 'opencode': _opencode, 'ollama': _ollama}


def call(worker: str, prompt: str, role: str = '-', cwd: str | None = None) -> Result:
    row = next(r for r in catalog() if r['worker'] == worker)
    model = row['id']
    start = time.monotonic()
    exe = find(row['harness'])
    if row['harness'] not in ADAPTERS:
        code, text = 127, f'{row["harness"]} is a host harness, not callable from here'
    elif not exe:
        code, text = 127, f'{row["harness"]} not found (${PLACES[row["harness"]][0]}, PATH, app place)'
    else:
        code, text = ADAPTERS[row['harness']](exe, model, prompt, cwd or str(ROOT))
    result = Result(worker, model, classify(code, text), text.strip(), round(time.monotonic() - start, 1))
    record(result, role)
    return result


def record(result: Result, role: str = '-') -> None:
    """One line per call — who answered, how long, why not. Local state, never committed."""
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        reason = '' if result.status == 'ok' else result.text.replace('\t', ' ').replace('\n', ' ')[-160:]
        with LOG.open('a', encoding='utf-8', newline='\n') as fh:
            fh.write(f'{time.strftime("%Y-%m-%dT%H:%M")}\t{result.worker}\t{result.model}\t{role}\t'
                     f'{result.status}\t{result.seconds}\t{reason}\n')
    except OSError:
        pass


def tally() -> dict:
    """{worker: (calls, ok share, median seconds of the ok ones)} from the call log."""
    seen: dict = {}
    if LOG.is_file():
        for line in LOG.read_text(encoding='utf-8').splitlines():
            f = line.split('\t')
            if len(f) >= 6:
                seen.setdefault(f[1], []).append((f[4], float(f[5])))
    return {w: (len(c), sum(s == 'ok' for s, _ in c) / len(c),
                statistics.median([t for s, t in c if s == 'ok'] or [0]))
            for w, c in seen.items()}


def live(row: dict) -> str:
    """Zero-token: is the binary there, and does it still answer --help."""
    if row['harness'] not in ADAPTERS:
        return 'host'
    exe = find(row['harness'])
    if not exe:
        return 'missing'
    code, _ = run([exe, '--help'], timeout=30)
    return 'ok' if code == 0 else f'--help exit {code}'
