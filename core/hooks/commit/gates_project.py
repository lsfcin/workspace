#!/usr/bin/env python3
# What a code/ project must declare before it can commit: verify contract, goal link, spec,
# branch shape, .md type, citations, gitlink.
#
# THREE FEATURES LIVE IN THIS ONE FILE -- verify-contract, verify-suite, project-contract -- so the
# slug-names-the-file rule cannot apply here and three registry rows name this path. Each switch is
# read ONCE at the top and treated as a flag, never acted on by returning early from the whole
# stage: a disabled feature must skip its own section, or it silently takes the sections after it
# down with it. That was a live bug in the sourced-bash version's shape.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import feature_law  # noqa: E402
from pre_commit import Blocked, git, spawn  # noqa: E402

CODE_SUFFIX = ('.js', '.jsx', '.ts', '.tsx', '.py', '.dart')
GOAL_LINE = r'^>\s*goal:\s*(\[[^]]+\]\([^)]+\)|none)\s*$'


def _under_code(commit) -> bool:
    """Whether the repo committing is a project under code/ -- asked of the MACHINERY root.

    The bash matched the string `/mnt/workspace/code/*`, which is the whole reason this pipeline
    could not run on any other clone. `toplevel` is the repo being committed; `root` is where the
    workspace lives; the question is whether the first sits inside `code/` of the second.
    """
    try:
        return commit.toplevel.relative_to(commit.root).parts[:1] == ('code',)
    except ValueError:
        return False


def _contract(commit) -> str:
    """Which verify:fast contract this project declares, if any.

    Discovery is stack-agnostic on purpose: an npm script or a Makefile target, either satisfies it.
    A new project opts in by naming a script rather than by wiring anything.
    """
    package = commit.toplevel / 'package.json'
    if package.is_file() and '"verify:fast"' in package.read_text(encoding='utf-8',
                                                                 errors='replace'):
        return 'npm run --silent verify:fast'
    makefile = commit.toplevel / 'Makefile'
    if makefile.is_file() and any(line.startswith('verify-fast:') for line in
                                  makefile.read_text(encoding='utf-8',
                                                     errors='replace').splitlines()):
        return 'make verify-fast'
    return ''


def project_contract(commit):
    verify_contract = feature_law.is_enabled('verify-contract')
    verify_suite = feature_law.is_enabled('verify-suite')
    project = feature_law.is_enabled('project-contract')

    staged_code = commit.matching(*CODE_SUFFIX, exclude=('.d.ts',))
    if staged_code:
        contract = _contract(commit)
        if verify_contract and not contract and _under_code(commit):
            raise Blocked(
                '⛔ No verify:fast contract found — every code/ project needs one.\n'
                '   Declare package.json "verify:fast" (npm) or a Makefile "verify-fast:" '
                'target (any stack).\n'
                '   No real tests yet? A passing stub is enough — see code/ROADMAP-verify.md G5.')
        if verify_suite and contract:
            _run_suite(commit, contract)

    if project and _under_code(commit):
        _goal_link(commit)
        _spec_declaration(commit)

    # Delegated gates carry their own guards, so they are not wrapped in a switch here.
    import gitflow_gate
    import gitlink_gate
    gitflow_gate.check(commit)

    if project:
        for gate in ('checks/type-gate.py', 'checks/citation-gate.py'):
            done = spawn(commit, f'core/hooks/{gate}')
            if done.returncode != 0:
                raise Blocked(done.stdout + done.stderr)

    gitlink_gate.check(commit)

    # Branch drift: warn, never block. A deliberate mid-session switch is legitimate.
    import branch_marker
    branch_marker.check(commit)


def _run_suite(commit, contract):
    """The project's own verify:fast. Red blocks the commit, and the output says which command.

    A RUNNER THAT IS NOT INSTALLED IS NOT A RED SUITE. `make` is absent on a stock Windows clone, and
    reporting that as "verify:fast is red — fix before committing" tells the operator their tests
    failed when nothing ran. That is precisely the shape this pipeline was ported to remove, so the
    missing runner warns and names its install instead of blocking on a result nobody produced.
    """
    import subprocess
    from shutil import which
    runner = contract.split()[0]
    if not which(runner):
        print(f'⚠  {runner} not found — verify:fast not run for {commit.toplevel.name}.')
        print(f'   Install it, or declare a contract this machine can run. SETUP.md § {runner}.\n')
        return
    print('→ verify:fast…')
    done = subprocess.run(contract, shell=True, cwd=commit.toplevel, capture_output=True,
                          text=True, encoding='utf-8', errors='replace')
    if done.returncode != 0:
        tail = '\n'.join((done.stdout + done.stderr).splitlines()[-30:])
        raise Blocked(f'{tail}\n⛔ verify:fast is red — fix before committing. '
                      f'Full output: {contract}')
    print('✓ verify:fast green')


def _goal_link(commit):
    """code/<proj>/CONTEXT.md line 3 declares which goal this project serves, or `none`."""
    import re
    if 'CONTEXT.md' not in commit.staged:
        return
    context = commit.toplevel / 'CONTEXT.md'
    lines = context.read_text(encoding='utf-8', errors='replace').splitlines()
    third = lines[2] if len(lines) > 2 else ''
    if not re.match(GOAL_LINE, third):
        raise Blocked(f"⛔ {commit.toplevel.name}/CONTEXT.md missing '> goal:' link on line 3.\n"
                      "   Add '> goal: [slug](../../brain/goals/<slug>.md)' or '> goal: none'.")


def _spec_declaration(commit):
    """A NEW module CONTEXT.md under code/ must declare '> spec: <file>' or '> spec: none'.

    Ratchet / boy-scout: only files this commit ADDS, so existing modules are grandfathered and a
    repo that inherited violations is not blocked on every commit. Mirrors the goal-link convention.
    """
    import re
    added = [p for p in git('diff', '--cached', '--name-only', '--diff-filter=A',
                            cwd=commit.toplevel).splitlines()
             if p == 'CONTEXT.md' or p.endswith('/CONTEXT.md')]
    for path in commit.existing(added):
        text = (commit.toplevel / path).read_text(encoding='utf-8', errors='replace')
        found = re.search(r'^>\s*spec:\s*(\S.*)$', text, re.MULTILINE)
        declared = found.group(1).strip() if found else ''
        if not declared:
            raise Blocked(f"⛔ {path} missing '> spec:' declaration (new module under code/).\n"
                          "   Add '> spec: SPEC.md' (author it from code/_templates/"
                          "module.SPEC.md),\n"
                          "   or '> spec: none' to opt out. See code/ROADMAP-spec-drive.md.")
        if declared != 'none' and not (commit.toplevel / Path(path).parent / declared).is_file():
            raise Blocked(f"⛔ {path} declares '> spec: {declared}' but "
                          f'{Path(path).parent}/{declared} is missing.\n'
                          '   Create it from code/_templates/module.SPEC.md, '
                          "or use '> spec: none'.")
