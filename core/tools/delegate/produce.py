# produce.py — the artifact mode: pick the route ladder, run each route in its own copy, hold it to the contract's checks, retry with the evidence, and hand the orchestrator a report instead of the files.
#
# WHY THE REPORT IS ALL THE ORCHESTRATOR READS. Its context is re-read every turn, and cache reads
# are 59% of the bill (core/experiments/output-cost.md): delegation pays only when the orchestrator
# never opens what the worker wrote. Paths, hashes, check results and the three lists, nothing else.
#
# WHY A FAILURE NEVER COMES BACK AS FILES. The panel's (argon, 2026-11-26) biggest cost risk is the
# orchestrator rescuing a failed worker by reading its files; a retry gets the wrapper's evidence in
# ## Last Failure instead, and after `of` tries the next route takes the task in a fresh copy.
from __future__ import annotations

import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import delegation  # noqa: E402
import sandbox  # noqa: E402
import workers  # noqa: E402

MAX_RUNGS = 4  # a ceiling per run: at most this many routes, `of` tries each
RUNS = workers.ROOT / 'core' / 'state' / 'delegations.tsv'


def ladder(job: str = 'coder') -> list:
    """The routes that write files, one per harness, cheapest first: free, outside subscriptions,
    then the Claude quota (Lucas, 2026-11-26); the `job` first within a harness. Provisional until
    the work → route table (core/ROADMAP-workers.md § v1)."""
    seen, out = set(), []
    for r in sorted(workers.catalog(), key=lambda r: (r['harness'] == 'claude', r['cost'] != 'free', r['job'] != job)):
        if r.get('tools') == 'tools' and r['depleted'] == '-' and r['harness'] not in seen and not workers.cooling(r['worker']):
            seen.add(r['harness'])
            out.append(r)
    return out


def produced(text: str, works: set, roles: dict, rows=None, caller=workers.call, root=workers.ROOT, box=sandbox) -> tuple:
    """An artifact run: (status, the report the orchestrator reads). `roles` maps a role to its pre-prompt."""
    c = delegation.parse(text)
    delegation.validate(c, works, set(roles))
    inline, by_path = delegation.bundle(c['read_paths'], root)
    pre = f'{roles[c["role"]]}\n\n' if c['role'] != '-' else ''
    tried, last, of, start = [], c['sections'].get('Last Failure', ''), c['attempt'][1], datetime.datetime.now()
    for row in (rows if rows is not None else ladder())[:MAX_RUNGS]:
        copy = box.make(root)
        try:
            for n in range(1, of + 1):
                cc = {**c, 'attempt': (n, of), 'sections': {**c['sections'], **({'Last Failure': last} if last else {})}}
                r = caller(row['worker'], pre + delegation.prompt(cc, inline, by_path), c['role'],
                           cwd=str(copy), write=True, judge=lambda t: delegation.read(t)['check'])
                if r.status != 'ok':
                    tried.append(f'{row["worker"]}: {r.status}')
                    break
                seen, changed = delegation.read(r.text), box.changed(copy)
                if seen['status'] in ('blocked', 'split'):
                    return report(c, seen['status'], tried + [f'{row["worker"]}: {seen["status"]}'], r.text, [], [], start)
                out, failed = delegation.outside(changed, c['write_paths']), [x for x in box.check(copy, c['checks']) if x[1]]
                if changed and not out and not failed:
                    files = box.bring(copy, root, changed)
                    return report(c, 'ok', tried + [f'{row["worker"]}: ok on try {n}'], r.text, files, c['checks'], start)
                last = delegation.failure(out, failed, changed)
                tried.append(f'{row["worker"]} try {n}: {last.splitlines()[0][:100]}')
        finally:
            box.drop(copy)
    return report(c, 'fail', tried, last, [], [], start)


def report(c: dict, status: str, tried: list, answer: str, files: list, passed: list, start, log=None) -> tuple:
    """What enters the orchestrator's context, and one row in core/state/delegations.tsv with its size in tokens."""
    s = delegation.sections(answer)
    lines = [f'status: {status}', 'route: ' + ' → '.join(tried or ['none left'])]
    lines += [f'wrote {p} {h}' for p, h in files] + [f'check passed: {x}' for x in passed]
    if status == 'ok':
        lines += [f'## {k}\n{s[k][:400]}' for k in delegation.LISTS if s.get(k, 'none').strip('-* .').lower() != 'none']
    elif status == 'fail':
        lines += [f'## Last Failure\n{answer[-1200:]}']
    else:
        lines += [s.get('Questions') or s.get('Subtasks', '')]
    text = '\n'.join(lines) + '\n'
    tokens = (len(text) + len(c.get('goal', ''))) // delegation.CHARS_PER_TOKEN
    log = log or RUNS
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open('a', encoding='utf-8', newline='\n') as fh:
        fh.write('\t'.join([f'{start:%Y-%m-%dT%H:%M}', c['work'], status, ' → '.join(tried).replace('\t', ' '),
                            f'{(datetime.datetime.now() - start).total_seconds():.0f}', str(tokens), c['goal'][:80]]) + '\n')
    return status, text
