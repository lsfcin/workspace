# T0 the shim contract (core/hooks/SPECS.md): every canonical script a provider shim spawns
# must exist. Zero-token, verify-fast.
#
# WHAT THIS PROVES, AND WHAT IT DOES NOT. It proves a path RESOLVES. It does not prove the gate
# fires, which is behavioural and a different test -- so green here means the shim can reach the
# gate, never that the gate works. Said plainly because this workspace's own rule is that a check
# proving a name is present is the weaker kind, and one of ours once passed wrongly on that shape.
#
# WHY IT EXISTS. The 2026-07-31 split moved scripts into read/, checks/ and facade/. All eleven of
# opencode's spawns kept pointing at core/hooks/<script> and were dead for weeks; nothing could
# have noticed, because a second runtime's coverage was claimed in a table rather than checked.
# Repointed 2026-08-18. When this test was written on 2026-08-19 it immediately found THREE MORE,
# in the Copilot shim, from the same split: read/facade-{tracker,gate,scan}.py. Two shims, one
# cause, found a day apart -- which is the argument for a test rather than for another careful
# reading.
import re

from conftest import WORKSPACE_ROOT

HOOKS = WORKSPACE_ROOT / 'core/hooks'

# One entry per shim: the files it spawns from, and how a spawn names its script. Derived by
# reading each shim, because the conventions genuinely differ -- opencode interpolates
# `${HOOKS}/`, Copilot passes a relative string to gate() or joins onto a HOOKS Path.
SHIMS = {
    'opencode': (
        [WORKSPACE_ROOT / '.opencode/plugins/workspace-policy.js',
         WORKSPACE_ROOT / '.opencode/wp-helpers.js'],
        re.compile(r'\$\{HOOKS\}/([A-Za-z0-9_./-]+\.(?:py|sh))'),
    ),
    'copilot': (
        [HOOKS / 'copilot/copilot-pre-tool.py',
         HOOKS / 'copilot/copilot-post-tool.py',
         HOOKS / 'copilot/copilot-session-start.py',
         HOOKS / 'copilot/copilot_shared.py'],
        re.compile(r'["\']((?:[A-Za-z0-9_-]+/)+[A-Za-z0-9_-]+\.(?:py|sh))["\']'),
    ),
    # Direct registration, no adapter: the config spawns canonical scripts by absolute path
    # (mirroring .claude/settings.json). Inert until workspace trust — see
    # core/experiments/zcode-hook-protocol.md — but the paths it names must resolve regardless.
    'zcode': (
        [WORKSPACE_ROOT / '.zcode/config.json'],
        re.compile(r'/mnt/workspace/core/hooks/([A-Za-z0-9_./-]+\.(?:py|sh))'),
    ),
    'codex': (
        [HOOKS / 'codex/codex-policy.py'],
        re.compile(r'"((?:read|checks|facade)/[A-Za-z0-9_./-]+\.(?:py|sh))"'),
    ),
}


def _spawned(shim: str) -> set:
    sources, pattern = SHIMS[shim]
    found = set()
    for source in sources:
        assert source.exists(), f'{shim}: shim file is gone -- {source}'
        found |= set(pattern.findall(source.read_text(encoding='utf-8')))
    return found


def test_every_shim_names_at_least_one_canonical_script():
    """Guards the guard: a regex that stopped matching would make both cases below vacuous."""
    for shim in SHIMS:
        count = len(_spawned(shim))
        assert count >= 5, (
            f'{shim}: found {count} script paths. The shim was rewritten and this pattern no '
            'longer reads it, so the resolution checks are passing on an empty set.'
        )


def test_opencode_spawns_only_scripts_that_exist():
    dead = sorted(p for p in _spawned('opencode') if not (HOOKS / p).exists())
    assert not dead, f'opencode shim spawns paths that do not resolve: {dead}'


def test_copilot_spawns_only_scripts_that_exist():
    dead = sorted(p for p in _spawned('copilot') if not (HOOKS / p).exists())
    assert not dead, f'copilot shim spawns paths that do not resolve: {dead}'


def test_zcode_spawns_only_scripts_that_exist():
    dead = sorted(p for p in _spawned('zcode') if not (HOOKS / p).exists())
    assert not dead, f'zcode shim spawns paths that do not resolve: {dead}'


def test_codex_spawns_only_scripts_that_exist():
    dead = sorted(p for p in _spawned('codex') if not (HOOKS / p).exists())
    assert not dead, f'codex shim spawns paths that do not resolve: {dead}'
