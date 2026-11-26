# workers.py — the one way a tool calls an outside worker (another harness's model): find it, call it, classify what came back, and log who answered.
#
# WHY ONE MODULE. delegate/ask and describe.py each built their own vendor call — two ideas of where
# a binary lives, of what a spent quota looks like, of what a timeout leaves running.
# core/tools/SPECS.md: a module imported by more than one family lives at this root.
#
# THE CATALOG IS DATA, THE IDS ARE DATA. Who exists, which id its harness resolves and in which
# order the panel tries them is core/workers.txt; what each model is good for is core/models.txt,
# joined by `model`. Nothing below names a model.
#
# A MISS IS CLASSIFIED, NEVER GUESSED. missing / no-login / quota / timeout / unknown / ok. An error
# matching no known mark is `unknown`, not `quota`: calling a broken call a spent quota hides it.
from __future__ import annotations

import json
import os
import pathlib
import shutil
import statistics
import sys
import tempfile
import time
from typing import NamedTuple

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import worker_guard  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
CATALOG = ROOT / 'core' / 'workers.txt'
MODELS = ROOT / 'core' / 'models.txt'
LOG = ROOT / 'core' / 'state' / 'workers.tsv'
TIMEOUT = 900  # the ceiling, and the deadline of a worker with too few ok calls to measure
FLOOR_S, MIN_OK = 120, 5
COOLDOWNS_H = (6, 24, 72)  # the 1st, 2nd, 3rd+ quota miss in a row keeps a worker out this long; an ok call clears the run
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
    status: str      # ok | missing | no-login | quota | timeout | busy | unknown
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


def calls() -> list[list[str]]:
    """The call log as rows of at least 6 fields: 7 before the `check` column (2026-11-26), 8 after."""
    lines = LOG.read_text(encoding='utf-8').splitlines() if LOG.is_file() else []
    return [f for f in (line.split('\t') for line in lines) if len(f) >= 6]


def cooling(worker: str, now: str = '') -> str:
    """The worker's last quota miss while still cooling before `now`, else ''. Only an ok ends a run of misses."""
    last, run = '', 0
    for f in calls():
        if f[1] == worker and f[4] in ('quota', 'ok'):
            last, run = (f[0], run + 1) if f[4] == 'quota' else ('', 0)
    stamp = lambda s: time.mktime(time.strptime(s, '%Y-%m-%dT%H:%M'))  # noqa: E731
    hours = COOLDOWNS_H[min(run, len(COOLDOWNS_H)) - 1] if run else 0
    if last and stamp(now or time.strftime('%Y-%m-%dT%H:%M')) - stamp(last) < hours * 3600:
        return last
    return ''


def deadline(worker: str) -> int:
    """min(ceiling, max(floor, 3 × p90)) of the worker's ok calls; the ceiling under MIN_OK of them."""
    oks = [float(f[5]) for f in calls() if f[1] == worker and f[4] == 'ok']
    return TIMEOUT if len(oks) < MIN_OK else int(min(TIMEOUT, max(FLOOR_S, 3 * statistics.quantiles(oks, n=10)[-1])))


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
    """stdout then stderr of `cmd`, run through worker_guard.spawn: stdin closed (codex waits on it
    forever otherwise), refused when the machine has no memory for it, and dead with its whole tree
    at the deadline or when this caller dies."""
    code, out, err = worker_guard.spawn(cmd, cwd=cwd, timeout=timeout)
    return code, out + err


def classify(code: int, text: str) -> str:
    """ok, or why this is no answer. agy prints a spent quota and may exit 0, so a short reply is
    searched for MARKS; a clean exit with a reply longer than ANSWER_FLOOR is an answer, whatever it says."""
    if code == 0 and len(text.strip()) > ANSWER_FLOOR:
        return 'ok'
    low = text.lower()
    for status, marks in MARKS.items() if code != 124 else ():  # a timeout's stream may say 'rate limit' anywhere
        if any(m in low for m in marks):
            return status
    by_code = {124: 'timeout', worker_guard.BUSY: 'busy', 127: 'missing'}
    return by_code.get(code) or ('unknown' if code != 0 or not text.strip() else 'ok')


def _codex(exe, model, prompt, cwd, timeout, write=False):
    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp) / 'answer.md'
        code, log = run([exe, 'exec', '-s', 'workspace-write' if write else 'read-only', '-m', model, '-C', cwd,
                         '--ephemeral', '-o', str(out), prompt], timeout=timeout)
        answer = out.read_text(encoding='utf-8') if out.exists() else ''
    return (0, answer) if code == 0 and answer.strip() else (code or 1, log)


def _opencode(exe, model, prompt, cwd, timeout, write=False):
    """--format json: the answer is the text parts of the event stream, never the pretty print."""
    code, raw = run([exe, 'run', '--pure', '--format', 'json', *['--auto'][:write], '-m', model, prompt], cwd=cwd, timeout=timeout)
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


# write=True only in delegate's isolated copy (delegate/sandbox.py). claude: clean context, no project hooks, no parent session id.
ADAPTERS = {'codex': _codex, 'opencode': _opencode,
            'agy': lambda exe, model, prompt, cwd, timeout, write=False: run(
                [exe, '--disable-slash-commands', *['--mode', 'accept-edits'][:2 * write], '--model', model, '-p', prompt], cwd=cwd, timeout=timeout),
            'claude': lambda exe, model, prompt, cwd, timeout, write=False: run(
                ['env', '-u', 'CLAUDE_CODE_SESSION_ID', '-u', 'CLAUDECODE', exe, '-p', '--model', model, '--permission-mode',
                 ('default', 'acceptEdits')[write], '--setting-sources', 'user', '--no-session-persistence', prompt], cwd=cwd, timeout=timeout),
            'ollama': lambda exe, model, prompt, cwd, timeout, write=False: run([exe, 'run', model, prompt], cwd=cwd, timeout=timeout)}


def call(worker: str, prompt: str, role: str = '-', cwd: str | None = None, judge=None, write: bool = False) -> Result:  # judge(text) -> check
    row = next(r for r in catalog() if r['worker'] == worker)
    model = row['id']
    start = time.monotonic()
    exe = find(row['harness'])
    if row['harness'] not in ADAPTERS:
        code, text = 127, f'{row["harness"]} is a host harness, not callable from here'
    elif not exe:
        code, text = 127, f'{row["harness"]} not found (${PLACES[row["harness"]][0]}, PATH, app place)'
    else:
        code, text = ADAPTERS[row['harness']](exe, model, prompt, cwd or str(ROOT), deadline(worker), write)
    result = Result(worker, model, classify(code, text), text.strip(), round(time.monotonic() - start, 1))
    record(result, role, judge(result.text) if judge and result.status == 'ok' else '')
    return result


def record(result: Result, role: str = '-', check: str = '') -> None:
    """One line per call — who answered, how long, why not, which check failed. `check` is derived (a miss is
    timeout or infra, an ok is empty or -); only the caller knows a format, so bad-format is passed in, never derived — a free-text debate has none."""
    ok, s = result.status == 'ok', result.status
    check = check or (('-' if result.text.strip() else 'empty') if ok else 'timeout' if s == 'timeout' else 'infra')
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        reason = '' if ok else result.text.replace('\t', ' ').replace('\n', ' ')[-160:]
        with LOG.open('a', encoding='utf-8', newline='\n') as fh:
            fh.write(f'{time.strftime("%Y-%m-%dT%H:%M")}\t{result.worker}\t{result.model}\t{role}\t'
                     f'{s}\t{result.seconds}\t{reason}\t{check}\n')
    except OSError:
        pass


def tally() -> dict:
    """{worker: (calls, ok share, median seconds of the ok ones)} from the call log."""
    seen: dict = {}
    for f in calls():
        seen.setdefault(f[1], []).append((f[4], float(f[5])))
    return {w: (len(c), sum(s == 'ok' for s, _ in c) / len(c),
                statistics.median([t for s, t in c if s == 'ok'] or [0]))
            for w, c in seen.items()}


# The command that lists what a harness offers today, first column = the id it resolves.
OFFERS = {'agy': ['models'], 'opencode': ['models'], 'ollama': ['list'], 'codex': ['debug', 'models']}


def _ids(text: str) -> set:
    """The model ids in a codex catalog JSON, first object only: run() appends stderr after it."""
    try:
        return {m['slug'] for m in json.JSONDecoder().raw_decode(text.lstrip())[0]['models']}
    except (ValueError, KeyError, TypeError):
        return set()


def offered(harness: str) -> set | None:
    """Zero-token: the ids this harness offers right now, or None when it cannot say."""
    exe = find(harness)
    if harness not in OFFERS or not exe:
        return None
    code, text = run([exe, *OFFERS[harness]], timeout=60)
    if harness == 'codex':  # its two catalogs disagreed within an hour (2026-11-23): union, hidden ids too
        cache = pathlib.Path(os.environ.get('CODEX_HOME', HOME / '.codex')) / 'models_cache.json'
        return (_ids(text) | _ids(cache.read_text(encoding='utf-8') if cache.is_file() else '')) or None
    return {line.split()[0] for line in text.splitlines() if line.strip()} if code == 0 else None


def live(row: dict, offers: dict | None = None) -> str:
    """Zero-token: is the binary there, does it answer --help, and does it still offer the id.
    `offers` caches offered() per harness across rows."""
    if row['harness'] not in ADAPTERS:
        return 'host'
    exe = find(row['harness'])
    if not exe:
        return 'missing'
    code, _ = run([exe, '--help'], timeout=30)
    if code != 0:
        return f'--help exit {code}'
    offers, h = ({} if offers is None else offers), row['harness']
    have = offers[h] if h in offers else offers.setdefault(h, offered(h))
    return 'ok' if have is None or row['id'] in have else f'{row["id"]} no longer offered'
