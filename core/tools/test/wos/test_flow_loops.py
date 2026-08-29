# T0 the flow layer's loop bound (core/flows/CONTEXT.md § Rules that hold for every flow): a step
# that declares a loop must declare its numeric cap. Zero-token, no network.
#
# WHY THIS RULE AND NOT THE ONE THAT WAS PROPOSED. core/flows/craft/SPECS.md rejected a gate
# demanding an adversarial review step: an adversary always finds something, so demanding the step
# without demanding a bound builds the death loop the source itself warns about. Requiring the
# BOUND is what makes requiring the step safe, and it is true of every flow rather than of one
# technique.
#
# Sourced, not imported: the validator is a shell fragment that `sync-skills` supplies $WORKSPACE
# to, and the probe runs it against a throwaway tree rather than against core/flows — a test that
# asserted on the real corpus would pass the day somebody deleted the rule's last violator.
import subprocess

from conftest import WORKSPACE_ROOT
from platform_law import posix

VALIDATOR = WORKSPACE_ROOT / 'core/tools/wos/skills/validate.sh'

BOUNDED = """---
description: d
args: a
type: utility
confirm: none
---
## Execution Loops
Return to the plan step while FATALs remain. **Iteration cap: at most 3 passes.**
"""

UNBOUNDED = """---
description: d
args: a
type: utility
confirm: none
---
## Execution Loops
Return to the plan step and re-review until the review passes.
"""

# The law files name the rule's own words. They state it; they do not run it.
STATES_THE_RULE = 'Loops are bounded: every loop declares an exit condition and an iteration cap.\n'


def _validate(tmp_path, files: dict) -> subprocess.CompletedProcess:
    flows = tmp_path / 'core' / 'flows'
    flows.mkdir(parents=True)
    for name, body in files.items():
        (flows / name).write_text(body, encoding='utf-8')
    # posix(), not str(): both paths become TEXT inside a bash command, where a backslash is an
    # escape. The Windows spelling arrived with every separator eaten, so bash reported the
    # validator missing and the case read as the rule having stopped firing.
    script = f'WORKSPACE={posix(tmp_path)}; source {posix(VALIDATOR)}; validate_flow_loops'
    return subprocess.run(['bash', '-c', script], capture_output=True, text=True)


def test_a_loop_with_a_numeric_cap_passes(tmp_path):
    out = _validate(tmp_path, {'bounded.md': BOUNDED})
    assert out.returncode == 0, out.stdout + out.stderr


def test_a_loop_with_no_number_is_rejected(tmp_path):
    """"Until the review passes" is exactly the wording that made this workspace's own adversarial
    review the unbounded case, so it is the wording the probe uses."""
    out = _validate(tmp_path, {'unbounded.md': UNBOUNDED})
    assert out.returncode == 1, out.stdout
    assert 'unbounded.md' in out.stdout
    assert 'no numeric cap' in out.stdout


def test_a_flow_declaring_no_loop_is_never_asked_for_a_cap(tmp_path):
    """Most flows run start to finish. A gate that asked all of them for a number would be a gate
    against the word `iteration` rather than against a hang."""
    out = _validate(tmp_path, {'straight.md': '---\ndescription: d\n---\nRun it once.\n'})
    assert out.returncode == 0, out.stdout


def test_the_files_that_state_the_rule_are_not_judged_by_it(tmp_path):
    """CONTEXT.md and SPECS.md spell out `iteration cap` because they declare the law. Judging them
    by it makes the law its own first violation, which is how a checker teaches people to add
    exemptions instead of caps."""
    out = _validate(tmp_path, {'CONTEXT.md': STATES_THE_RULE, 'SPECS.md': STATES_THE_RULE})
    assert out.returncode == 0, out.stdout


def test_the_real_flow_corpus_is_clean():
    """The rule is in force, so core/flows must satisfy it. This is the row that turns the check
    from a capability into a fact about the workspace."""
    script = f'WORKSPACE={posix(WORKSPACE_ROOT)}; source {posix(VALIDATOR)}; validate_flow_loops'
    out = subprocess.run(['bash', '-c', script], capture_output=True, text=True)
    assert out.returncode == 0, out.stdout + out.stderr
