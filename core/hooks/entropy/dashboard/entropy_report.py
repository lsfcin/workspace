#!/usr/bin/env python3
# The entropy report: what the dashboard's findings look like on the page.
#
# Split from entropy-dashboard.py 2026-07-30, when that file crossed the 150-line warn.
# A tool that reports size signals is a poor place to ignore one.
#
# Since 2026-08-20 it renders a delimited BLOCK rather than a whole file: the measurements live
# inside ISSUES.md, under hand-written issues, because both answer the same question — what is
# currently untrue that we know about (core/SCHEMA.md § The `.md` type system).
from datetime import date

from platform_law import rel

START = '<!-- entropy:start -->'
END = '<!-- entropy:end -->'

# Only used when ISSUES.md is missing entirely — a clone gets it from git. It carries the type's own
# head so the file is a legal ISSUES.md from its first line rather than from its first run.
SEED = ('# Workspace issues\n'
        '> What is currently untrue that we know about: hand-written issues first, every measured\n'
        '> number inside its own generated block.\n')


def local_seed(repo: str) -> str:
    """The same head, for a code repo's own ledger — created on the first scatter, then authored."""
    return (f'# {repo.split("/")[-1]} issues\n'
            '> What is currently untrue that we know about in this repo: hand-written issues\n'
            '> first, every measured number inside its own generated block.\n')


def _rel(path, root) -> str:
    return rel(path, root)


SECTIONS = (
    ('types', 'Off-allowlist `.md` types', 'route via core/SCHEMA.md § four disposal routes'),
    ('inventories', 'CONTEXT.md hand-written inventories', 'the routing block owns inventory'),
    ('naming', 'Naming and placement', 'kebab-case ASCII, types where their scope allows'),
    ('routing', 'Routing tables pointing at files git does not carry',
     'a clone gets the table and not the file — track the target, or stop routing to it'),
    ('goals', 'Projects not declaring their goal', 'line 3 of a code/ CONTEXT.md'),
    ('wiki', 'Wiki-links naming nothing', 'a [[slug]] is a goal file or an item in one'),
    ('retired', 'Retired tokens still alive', 'a rename is unfinished until these are zero'),
    ('citations', 'Roadmap item numbers cited outside a roadmap',
     'a closed item is deleted — cite the SPECS.md/SCHEMA.md section that owns the rule'),
    ('duplicates', 'Items claimed by two ledgers', 'v1 criterion 2 — an item lives in one place'),
    ('size', 'Size signals', 'a signal for review, never a cap — do not summarize to fit'),
    ('stubs', 'Source files with no interface stub',
     'the read gate only fires when a stub exists — a missing one turns it off silently'),
    ('fanout', 'Directories holding too many files',
     'splitting costs one hop — pay it only when it removes more table than it adds'),
    ('finished', 'Prose describing finished work',
     'git is the history — cut it, or rewrite it as present-tense state'),
    ('undescribed', 'Unanswered scaffold placeholders',
     'a generator asked a question — answer it at the source, never by cutting the marker'),
    ('stores', 'Doubt stores missing their own discipline',
     'an experiment states its Method, Results, What changed and Limitations; a judged reference '
     'carries a source tier'),
    ('vendor', 'Ledgers naming a model where they mean a tier',
     'which model fills a tier is data — core/flows/craft/routing.md'),
    ('fields', 'Header fields naming code that is not there',
     'a field naming our own tree is a claim, and it is checked before a later session inherits '
     'it as fact — core/SCHEMA.md § Every field that names our own code is verified'),
    ('truncated', 'Truncated routing descriptions',
     'the source wrote past the bound — shorten it there, never edit the table'),
    ('misplaced', 'Constraints trapped in a CONTEXT.md head',
     'the only enforced-read type — move the contract to a sibling SPECS.md'),
    ('branches', 'Local branches holding unpromoted work',
     'promote when the work is green, or say which reason applies — /roundup Phase 5'),
    ('unpushed', 'Work that exists on this disk and nowhere else',
     'two machines share this workspace — push it, or give the repo a remote to push to: '
     'code/SPECS-git.md § Push policy'),
    ('locals', 'Local branches already merged into their base',
     'safe to delete, and purely local — `git -C <repo> branch -d <branch>`'),
    ('remotes', 'Remote branches already merged into their base',
     'safe to delete, and outward-facing — `git -C <repo> push origin --delete <branch>`, Lucas'),
)


def _index(counts: dict, here: int) -> list:
    """The root's index of the local ledgers, and the one collected number.

    The sum is computed from the counts the same run just wrote, so it cannot disagree with them.
    A repo may not write into it — that is the copied-count drift these checks exist to catch.
    The collected total lives HERE and not in the header: it is context for choosing which repo
    to open next, never this repo's debt.
    """
    scattered = sum(counts.values())
    out = ['', '### Findings per code repo', '',
           '*Each repo keeps its own `ISSUES.md` and fixes its own findings; this table only says '
           'which one to open next.*', '',
           '| Repo | Findings |', '|------|----------|']
    out += [f'| [`{repo}`]({repo}/ISSUES.md) | {counts[repo]} |' for repo in sorted(counts)]
    return out + [f'| **collected** | **{scattered + here}** |']


def render(findings: dict, scanned: int, root, name: str = '', index: dict = None,
           trend: str = '') -> str:
    total = sum(len(findings[key]) for key, _, _ in SECTIONS)
    scope = f'`{name}`' if name else 'the whole tree'
    # The headline is THIS repo's count, never the collected one. A reader can act on the number
    # in front of them and on nothing else: a nested repo's findings are fixed by opening that
    # repo, so charging them to this header made the figure grow with the number of repos scanned
    # rather than with this repo's debt (603 vs 33 on 2026-08-25) and nobody could act on either.
    scattered = sum(index.values()) if index else 0
    out = [START,
           '## Entropy',
           '',
           '> Generated by `core/hooks/entropy/dashboard/entropy-dashboard.py`, which scans '
           f'{scope}. Never edit inside this block, and never copy a count out of it — a copied '
           'number is the drift these checks exist to catch.',
           '',
           f'{date.today().isoformat()} · {scanned} tracked files scanned · '
           f'**{total} findings here**{trend}'
           + (f' · {scattered} more across {len(index)} nested repos, each in its own ISSUES.md'
              if index else ''), '',
           '| Check | Findings |', '|-------|----------|']
    out += [f'| {title} | {len(findings[key])} |' for key, title, _ in SECTIONS]
    if index:
        out += _index(index, total)
    for key, title, note in SECTIONS:
        items = findings[key]
        out += ['', f'### {title}', '', f'*{note}*', '']
        out += ['Clean.'] if not items else [
            f'- {_rel(i.splitlines()[0], root)}' for i in sorted(items)]
    return '\n'.join(out + ['', END]) + '\n'
