# T0 the web-retry gate: a curl/wget that failed hands the agent the next things to try.
#
# preg.ufrpe.br (2026-11-21) is the case: a verify error 20 and a 502 after 90 s read as "the site
# is down", when the server only stalled a client calling itself curl and omitted its intermediate.
# Silence matters as much as firing — a loose 502 in some other output, a curl that worked, a
# command that fetches nothing — and so does saying it once per host and kind.
import json
import subprocess
import uuid

import pytest

from conftest import WORKSPACE_ROOT
from platform_law import interpreter

GATE = WORKSPACE_ROOT / 'core/hooks/checks/web-retry.py'
URL = 'https://preg.ufrpe.br/'


def run(command: str, stdout: str = '', stderr: str = '', error: str = '',
        session: str = '', event: str = 'PostToolUse') -> str:
	"""The context the gate would inject, or '' when it stays silent."""
	payload = {'tool_name': 'Bash', 'cwd': str(WORKSPACE_ROOT), 'hook_event_name': event,
	           'session_id': session or uuid.uuid4().hex, 'tool_input': {'command': command},
	           'tool_response': {'stdout': stdout, 'stderr': stderr}}
	if error:
		payload['error'] = error
	done = subprocess.run([interpreter(), str(GATE)], input=json.dumps(payload),
	                      capture_output=True, text=True, encoding='utf-8')
	assert done.returncode == 0, f'the gate must never block: {done.stderr}'
	if not done.stdout.strip():
		return ''
	return json.loads(done.stdout)['hookSpecificOutput']['additionalContext']


@pytest.mark.parametrize('stdout,stderr,error,hint', [
	('', '', 'Exit code 60\ncurl: (60) SSL certificate problem: unable to get local issuer certificate', 'AIA'),
	('', 'curl: (28) Operation timed out after 30002 milliseconds', '', 'User-Agent'),
	('/ 000 0\n/br/resolucoes 000 0\n', '', '', 'User-Agent'),
	('', 'curl: (6) Could not resolve host: preg.ufrpe.br', '', 'Wayback'),
	('HTTP/2 503\nserver: nginx\n', '', '', 'User-Agent'),
])
def test_a_failed_fetch_is_handed_what_to_try_next(stdout, stderr, error, hint):
	said = run(f'curl -sS -w "%{{http_code}}" {URL}', stdout, stderr, error)
	assert 'preg.ufrpe.br' in said and hint in said


def test_the_certificate_hint_never_offers_insecure():
	said = run(f'curl {URL}', error='curl: (60) SSL certificate problem')
	assert 'Never -k' in said


@pytest.mark.parametrize('command,stdout', [
	(f'curl -s -o /dev/null -w "%{{http_code}}" {URL}', '200\n'),
	('grep -c 502 server.log', '502 lines matched\n'),
	(f'echo {URL}', 'HTTP/2 503\n'),
	(f'curl -s {URL} | wc -l', '503\n'),
])
def test_success_and_loose_numbers_stay_silent(command, stdout):
	assert run(command, stdout) == ''


def test_it_says_it_once_per_host_and_kind():
	session = uuid.uuid4().hex
	err = 'curl: (28) Operation timed out'
	assert run(f'curl {URL}', stderr=err, session=session)
	assert run(f'curl -A x {URL}', stderr=err, session=session) == ''
	assert 'AIA' in run(f'curl {URL}', stderr='curl: (60) SSL certificate problem', session=session)


def test_a_failed_call_is_heard_on_its_own_event():
	said = run(f'curl {URL}', error='curl: (60) SSL certificate problem', event='PostToolUseFailure')
	assert 'AIA' in said
