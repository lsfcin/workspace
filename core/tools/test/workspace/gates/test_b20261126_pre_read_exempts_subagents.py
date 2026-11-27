# b20261126-pre-read-exempts-subagents regression — pre-read.py exempts subagents (AD-13).
import json
import subprocess
import uuid

from conftest import WORKSPACE_ROOT

GATE = 'hooks/read/pre-read.py'


def _session(name: str) -> str:
    return f'{name}-{uuid.uuid4().hex[:12]}'


def _read(path, session: str, **extra) -> subprocess.CompletedProcess:
    payload = json.dumps({'session_id': session, 'tool_input': {'file_path': str(path)}, **extra})
    return subprocess.run(['sh', str(WORKSPACE_ROOT / 'core/run'), GATE], input=payload,
                          capture_output=True, text=True, check=False,
                          encoding='utf-8', errors='replace')


def test_subagent_read_on_unread_current_stub_is_exempt_while_main_session_blocks(tmp_path):
    source = tmp_path / 'stubbed.py'
    source.write_text('def f(x):\n    return x\n', encoding='utf-8', newline='\n')
    (tmp_path / 'stubbed.pyi').write_text('def f(x): ...\n', encoding='utf-8', newline='\n')

    sub = _read(source, _session('subagent-read'), agent_id='subagent-1')
    assert sub.returncode == 0, f'subagent read must be exempt (AD-13):\n{sub.stderr!r}'
    assert sub.stderr == '', f'subagent read must emit no stderr:\n{sub.stderr!r}'

    main = _read(source, _session('main-read'))
    assert main.returncode == 2, 'main-session read on unread current stub must still block'
    assert 'READ INTERFACE FIRST' in main.stderr
