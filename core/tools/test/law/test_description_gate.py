# T0 description check: a file this commit adds must be able to describe itself. Zero-token, verify-fast.
#
# The check's whole design is that it holds no pattern table — it asks the routing generator
# whether it could describe the file, which is the same call whose empty return writes the
# placeholder. These tests exist to keep it that way: the moment it grows its own list of
# comment shapes, the two can disagree, and a disagreement between them is what put
# `← add first-line comment` inside the enforcement directory itself.
#
# It rides in type-gate.py rather than in a gate of its own: `core/hooks/checks/` is at the
# fanout cap, and a second standalone gate over the same staged-add set would have been a new
# file to say "and also this" — the ratchet, the corpus filters and the failure format are
# already there.
from conftest import WORKSPACE_ROOT  # the depth lives in one file, not nine

import importlib.util

import entropy_context

spec = importlib.util.spec_from_file_location(
    'type_gate', WORKSPACE_ROOT / 'core/hooks/checks/type-gate.py')
type_gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(type_gate)


def test_a_file_with_no_first_line_comment_owes_one(tmp_path):
    source = tmp_path / 'thing.py'
    source.write_text('x = 1\n', encoding='utf-8', newline='\n')
    assert entropy_context.check_description(source)


def test_a_described_file_owes_nothing(tmp_path):
    source = tmp_path / 'thing.py'
    source.write_text('# what this module is for\nx = 1\n', encoding='utf-8', newline='\n')
    assert entropy_context.check_description(source) is None


def test_a_shebang_is_not_a_description(tmp_path):
    """The generator skips the shebang before reading the first comment; so must the check."""
    source = tmp_path / 'runner.sh'
    source.write_text('#!/usr/bin/env bash\nrun\n', encoding='utf-8', newline='\n')
    assert entropy_context.check_description(source)
    source.write_text('#!/usr/bin/env bash\n# runs the thing\nrun\n', encoding='utf-8', newline='\n')
    assert entropy_context.check_description(source) is None


def test_a_file_the_routing_table_never_lists_is_not_asked(tmp_path):
    """The check's scope is exactly the generator's: a row that will never exist owes nothing."""
    for name in ('data.json', 'thing.pyi', 'CONTEXT.md'):
        path = tmp_path / name
        path.write_text('no description here\n', encoding='utf-8', newline='\n')
        assert entropy_context.check_description(path) is None, name


def test_the_message_names_the_shape_the_file_needs(tmp_path):
    source = tmp_path / 'thing.ts'
    source.write_text('const x = 1\n', encoding='utf-8', newline='\n')
    assert '// Short description' in entropy_context.check_description(source)


def test_the_gate_runs_it_over_what_the_commit_adds(tmp_path):
    """Wired into the ratchet, not just importable — the failure the wiring exists to produce."""
    source = tmp_path / 'thing.py'
    source.write_text('x = 1\n', encoding='utf-8', newline='\n')
    failures = type_gate.failures_for(source, {'CONTEXT.md'}, set(), {}, set())
    assert any('nothing to put in the routing table' in f for f in failures)
