#!/usr/bin/env python3
# PostToolUse, capability `shell` — a web fetch that failed once is a lead, not a verdict.
#
# WHY THIS EXISTS (Lucas, 2026-11-21). A session gave up on preg.ufrpe.br after three curl runs:
# a TLS verify error 20, then a 502 after 90 s. The site was up in Lucas's browser all along. The
# server stalls any client that says it is curl; with a browser User-Agent it answered in 0.6 s,
# and the missing intermediate certificate was one AIA download away. The session asked Lucas to
# save the pages by hand instead. The lesson holds for every tree, so it lives where every shell
# call passes, and it is free until it fires: a norm would bill every session for it.
#
# WHAT COUNTS AS A FAILURE is a diagnosis the tool itself printed — `curl: (28)`, `SSL certificate
# problem`, wget's `ERROR 503`, an HTTP status line — or a bare status code printed by a `-w
# '%{http_code}'` the command asked for. A loose 502 in some other output is not one (the panel's
# point, 2026-11-21). Once per host and kind per session, through hook_input.announced.
#
# LIMIT: only curl and wget. A fetch through Python or a WebFetch tool is not seen here.
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import feature_law  # noqa: E402
import scoreboard  # noqa: E402
from hook_input import announced, capability, command_only, parse_stdin  # noqa: E402

FETCH = re.compile(r'(?:^|[\s;|&(`$])(?:rtk\s+)?(curl|wget)\b')
HOST = re.compile(r'https?://([^/\s"\'<>:]+)')
CURL_CODE = re.compile(r'curl: \((\d+)\)')
CERT = re.compile(r'SSL certificate problem|unable to get local issuer|verify result: [^\n]*\(2[01]\)'
                  r'|certificate verify failed|Unable to establish SSL', re.I)
STATUS = re.compile(r'HTTP/[\d.]+ (403|429|5\d\d)\b|ERROR (403|429|5\d\d)\b')
# A status printed by -w: the code at the start of a line, as a `-w '%{http_code} ...'` writes it.
WCODE = re.compile(r'^\s*(?:\S+\s)?(000|403|429|5\d\d)\b', re.M)

HINTS = {
	'cert': 'the server may omit its intermediate: read the AIA URL '
	        '(openssl s_client -connect HOST:443 | openssl x509 -noout -ext authorityInfoAccess), '
	        'add that certificate to a --cacert bundle. Never -k.',
	'filtered': 'the server may be filtering the client: retry with a browser User-Agent (-A) and '
	            'Accept headers, then a longer --max-time, -4 or -6, --http1.1.',
	'unreachable': 'try another host (www., ww2.), an official mirror, the Wayback copy '
	               '(web.archive.org/web/2026/URL) or another network before concluding.',
}
KIND_OF_CODE = {'6': 'unreachable', '7': 'unreachable', '28': 'filtered', '35': 'cert',
                '52': 'filtered', '56': 'filtered', '60': 'cert'}


def kinds(command: str, output: str) -> list[str]:
	"""Which failure kinds this fetch's own output diagnoses, in HINTS order."""
	found = {KIND_OF_CODE[c] for c in CURL_CODE.findall(output) if c in KIND_OF_CODE}
	if CERT.search(output):
		found.add('cert')
	if STATUS.search(output) or ('http_code' in command and WCODE.search(output)):
		found.add('filtered')
	return [k for k in HINTS if k in found]


def response_text(raw: dict) -> str:
	"""stdout, stderr and a failure's error string, whichever the harness sent."""
	resp = raw.get('tool_response')
	parts = [str(raw.get('error') or '')]
	if isinstance(resp, dict):
		parts += [str(resp.get('stdout') or ''), str(resp.get('stderr') or '')]
	elif resp:
		parts.append(str(resp))
	return '\n'.join(parts)


def main() -> int:
	if not feature_law.is_enabled('web-retry'):
		return 0
	raw, tool, data, session, _ = parse_stdin()
	if capability(tool, data) != 'shell':
		return 0
	command = command_only(str(data.get('command') or ''))
	if not FETCH.search(command):
		return 0
	hosts = HOST.findall(command) or ['?']
	fresh = [k for k in kinds(command, response_text(raw))
	         if not announced(session, 'web_retry', f'{hosts[0]}:{k}')]
	if not fresh:
		return 0
	scoreboard.record('web-retry', 'found')
	lines = [f'⚠ WEB FETCH FAILED ({hosts[0]}): a first failure is not proof the site is down.']
	lines += [f'- {HINTS[k]}' for k in fresh]
	lines.append('- Say what you tried before you call it unreachable or hand it to Lucas.')
	event = str(raw.get('hook_event_name') or 'PostToolUse')
	print(json.dumps({'hookSpecificOutput': {'hookEventName': event,
	                                         'additionalContext': '\n'.join(lines)}}))
	return 0


if __name__ == '__main__':
	sys.exit(main())
