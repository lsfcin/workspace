# b20260905 regression — one process asks the capability question once, and answers it the way
# nine processes did.
#
# The nine gates were nine `command` entries per harness, so every tool call spawned nine
# interpreters over one payload: 0.40 s on a Read that needs two of them. core/hooks/dispatch.py
# runs them in-process off core/hooks/gates.txt (0.054 s, 7.4x). Collapsing processes is only safe
# while the contract survives it, so what is checked here is the contract, never the speed: a
# blocking gate still exits 2 with its OWN words on stderr, a gate that dies takes only itself, and
# a gate the table calls `informs` cannot block.
#
# The case that earned this file is test_a_gate_guarded_by_dunder_main_actually_runs. The first
# working dispatcher exec'd each gate under the module name importlib gives it, so
# checks/heredoc-gate.py — the one gate ending `if __name__ == '__main__'` — imported cleanly, ran
# nothing, and the dispatcher exited 0. A silent pass wearing a success's coat, found by diffing a
# gate's own output against its output through here, which is what that test now does forever.
import json
import os
import subprocess

import pytest

from conftest import WORKSPACE_ROOT
from platform_law import interpreter, posix

DISPATCH = WORKSPACE_ROOT / 'core/hooks/dispatch.py'
TABLE = WORKSPACE_ROOT / 'core/hooks/gates.txt'
HOOKS = WORKSPACE_ROOT / 'core/hooks'
WS = posix(WORKSPACE_ROOT)


def rows() -> list[tuple[str, str, str]]:
	"""(capability, path, class) for every declared gate."""
	found = []
	for line in TABLE.read_text(encoding='utf-8').splitlines():
		line = line.strip()
		if line and not line.startswith('#'):
			cap, _, path, kind = (p.strip() for p in line.split('\t'))
			found.append((cap, path, kind))
	return found


def run(payload: dict, target=DISPATCH) -> subprocess.CompletedProcess:
	return subprocess.run([interpreter(), str(target)], input=json.dumps(payload),
	                      capture_output=True, text=True, encoding='utf-8',
	                      cwd=str(WORKSPACE_ROOT))


def call(tool: str, tool_input: dict, session: str) -> dict:
	return {'session_id': session, 'cwd': str(WORKSPACE_ROOT),
	        'tool_name': tool, 'tool_input': tool_input}


def with_table(table, session: str) -> subprocess.CompletedProcess:
	"""The dispatcher over a table of gates written for one case.

	A real gate cannot be asked to crash, or to block while its class says it informs, so the three
	cases below declare their own. WOS_GATES_TABLE is read by dispatch.table_path() and set nowhere
	else in the workspace.
	"""
	payload = call('Read', {'file_path': str(WORKSPACE_ROOT / 'AGENTS.md')}, session)
	return subprocess.run(
		[interpreter(), str(DISPATCH)], input=json.dumps(payload),
		capture_output=True, text=True, encoding='utf-8', cwd=str(WORKSPACE_ROOT),
		env={**os.environ, 'WOS_GATES_TABLE': str(table)})


def declare(table, *gates: tuple[str, str]) -> None:
	"""Write a table naming each (absolute gate path, class) in the order given."""
	lines = ['# capability\torder\tpath\tclass']
	lines += [f'read\t{(n + 1) * 10}\t{posix(path)}\t{kind}' for n, (path, kind) in enumerate(gates)]
	table.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')


@pytest.mark.parametrize('path', sorted({p for _, p, _ in rows()}))
def test_every_declared_gate_exists(path):
	"""The table is a registration, and a registration naming a dead file is the defect
	test_shim_paths.py exists to catch one layer up."""
	assert (HOOKS / path).is_file(), f'gates.txt names {path}, which is not there'


@pytest.mark.parametrize('cap,path,kind', rows())
def test_every_declared_gate_has_a_known_capability_and_class(cap, path, kind):
	assert cap in ('shell', 'read', 'write'), f'{path}: unknown capability {cap!r}'
	assert kind in ('blocks', 'informs'), f'{path}: unknown class {kind!r}'


def test_a_gate_guarded_by_dunder_main_actually_runs():
	"""The gate's own output, and its output through the dispatcher, say the same thing.

	checks/heredoc-gate.py is the only gate ending `if __name__ == '__main__'`, so it is the one
	that goes quiet if the dispatcher execs it under any other name. Compared rather than asserted
	against a fixed string: the point is that routing through here changes nothing.
	"""
	payload = call('Bash', {'command': f"cat > {WS}/probe.md <<'EOF'\nx\nEOF"}, 'b20260905-main')
	alone = run(payload, HOOKS / 'checks/heredoc-gate.py')
	through = run(payload)
	assert 'UNGATED WRITE' in alone.stdout, 'the gate itself went quiet — this test proves nothing'
	said = json.loads(through.stdout)['hookSpecificOutput']['additionalContext']
	assert 'UNGATED WRITE' in said


def test_a_block_keeps_its_own_words_and_its_own_exit_code():
	"""Exit 2 and the gate's stderr, passed through with nothing added.

	core/hooks/SPECS.md makes the reason the gate's own; a dispatcher that summarised, prefixed or
	re-wrapped it would be a second voice on one rejection.
	"""
	target = WORKSPACE_ROOT / 'core/hooks/hook_input.py'
	done = run(call('Read', {'file_path': str(target)}, 'b20260905-block'))
	assert done.returncode == 2
	assert 'CONTEXT GATE' in done.stderr
	assert 'DISPATCH' not in done.stderr


def test_a_capability_that_selects_nothing_runs_nothing():
	"""'other' is the whole saving: a Grep carries no command and no path, and pays for no gate."""
	done = run(call('Grep', {'pattern': 'x'}, 'b20260905-other'))
	assert done.returncode == 0
	assert done.stdout.strip() == ''
	assert done.stderr.strip() == ''


def informer(path, word: str):
	"""A gate whose whole job is to be heard."""
	path.write_text('# an informing gate\nimport json\n'
	                'print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",'
	                f' "additionalContext": "{word}"}}}}))\n', encoding='utf-8', newline='\n')
	return path


def test_a_broken_gate_takes_only_itself(tmp_path):
	"""Nine processes made isolation free; one process makes it a decision.

	A gate that raises must not block the call — exit 1, never 2, the rule core/run states for a
	half-installed clone — and the gates declared after it must still run.
	"""
	broken = tmp_path / 'broken-gate.py'
	broken.write_text('# a gate that dies\nraise RuntimeError("boom")\n',
	                  encoding='utf-8', newline='\n')
	table = tmp_path / 'gates.txt'
	declare(table, (broken, 'blocks'), (informer(tmp_path / 'after-gate.py', 'reached'), 'informs'))
	done = with_table(table, 'b20260905-broken')
	assert done.returncode == 1, 'a broken gate must never block the call it only observes'
	assert 'boom' in done.stderr
	assert 'reached' in done.stdout, 'the chain stopped at the corpse'


def test_an_informing_gate_that_blocks_is_refused(tmp_path):
	"""`informs` is a promise the table makes on a gate's behalf, and the dispatcher keeps it."""
	liar = tmp_path / 'liar-gate.py'
	liar.write_text('# a gate that blocks despite its class\n'
	                'import sys\nprint("nope", file=sys.stderr)\nsys.exit(2)\n',
	                encoding='utf-8', newline='\n')
	table = tmp_path / 'gates.txt'
	declare(table, (liar, 'informs'))
	done = with_table(table, 'b20260905-liar')
	assert done.returncode == 1, 'an informing gate does not get to block'
	assert 'DISPATCH' in done.stderr


def test_two_informing_gates_produce_exactly_one_json_document(tmp_path):
	"""Claude Code parses a hook's stdout as ONE document, so two would leave one unheard."""
	table = tmp_path / 'gates.txt'
	declare(table, (informer(tmp_path / 'first-gate.py', 'alpha'), 'informs'),
	        (informer(tmp_path / 'second-gate.py', 'beta'), 'informs'))
	done = with_table(table, 'b20260905-merge')
	assert done.stdout.strip(), f'nothing was said: rc={done.returncode} err={done.stderr}'
	said = json.loads(done.stdout)['hookSpecificOutput']['additionalContext']
	assert 'alpha' in said and 'beta' in said
