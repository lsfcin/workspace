# The close report: what a session cost and what it left, shown to Lucas and never to the model.
#
# ZERO MODEL TOKENS (Lucas, 2026-11-23). Until 2026-11-19 roundup printed cost, size and trace into
# the agent's own context, the most expensive turn of the session paying to read what only Lucas
# reads; 71ebeac3 then dropped them with the rest of the old close. Now roundup only ARMS a marker,
# and the harness's end-of-turn hook DELIVERS the report on a channel the model never sees
# (Claude: Stop + systemMessage). This module is the harness-neutral half; the hook is a shim.
#
# THE HANDOFF CHECK. A session that edits four repositories owes each one with open threads its own
# handoff block; on 2026-11-23 one bundled them all under the repository it edited least, and the
# next session had to guess which file to take. So delivery waits until every repository the
# transcript proves was edited has a block from this session, asking the agent ONCE; after that
# the report goes out anyway and names what is still missing, because "nothing open" is legitimate.
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
STATE = Path(os.environ.get('WOS_STATE_DIR') or ROOT / 'outputs/state')
sys.path.insert(0, str(Path(__file__).resolve().parent))
from handoff import choose, path_for, transcript  # noqa: E402

SESSION_TOOLS = (('session/usage',), ('session/trace',), ('size',))


def marker(session: str) -> Path:
    return STATE / f'close-{session}.json'


def arm(session: str, agent: str) -> None:
    """Called by roundup: remember which repositories this session's transcript proves it edited."""
    log = transcript(session, agent, ROOT)
    info = choose(ROOT, ROOT, session, agent, log)
    edited = [r['key'] for r in info['repos'] if r['lines']]
    STATE.mkdir(parents=True, exist_ok=True)
    marker(session).write_text(json.dumps({'agent': agent, 'repos': edited, 'asked': False}),
                               encoding='utf-8', newline='\n')


def missing(session: str, agent: str, keys: list) -> list:
    """Repositories this session edited whose handoff carries no section of its own."""
    owner = json.dumps([agent, session])
    def has(key):
        path = path_for(ROOT, key)
        return path.exists() and f'<!-- handoff-session: {owner} -->' in path.read_text(encoding='utf-8')
    return [key for key in keys if not has(key)]


def render(session: str, keys: list, absent: list) -> str:
    """The report itself: every line a local reader prints, best-effort, nothing a model wrote."""
    lines = []
    for tool in SESSION_TOOLS:
        done = subprocess.run([sys.executable, str(ROOT / 'core/tools/wos' / tool[0]), '--session', session],
                              capture_output=True, text=True, encoding='utf-8', timeout=60)
        if done.returncode == 0 and done.stdout.strip():
            lines.append(done.stdout.strip())
    written = [k for k in keys if k not in absent]
    if written:
        lines.append('handoffs: ' + ' · '.join(f'core/run tools/wos/handoff --take {k}' for k in written))
    if absent:
        lines.append('sem handoff desta sessão: ' + ', '.join(absent))
    return '\n'.join(lines)


def deliver(session: str):
    """('ask', text) once while a handoff is missing, then ('show', report); None when unarmed."""
    path = marker(session)
    if not path.exists():
        return None
    info = json.loads(path.read_text(encoding='utf-8'))
    absent = missing(session, info['agent'], info['repos'])
    if absent and not info['asked']:
        path.write_text(json.dumps({**info, 'asked': True}), encoding='utf-8', newline='\n')
        return 'ask', ('Close report waiting: no handoff block from this session for '
                       + ', '.join(absent) + '. Write one per repository with open threads '
                       '(core/run tools/wos/handoff --write FILE --repo PATH), or say there is nothing open.')
    path.unlink()
    return 'show', render(session, info['repos'], absent)
