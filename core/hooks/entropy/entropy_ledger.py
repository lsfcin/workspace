#!/usr/bin/env python3
# Tier 0 ledger and vocabulary checks, parsed from core/SCHEMA.md. Zero-token, deterministic.
#
# Two assertions that make two recurring bugs catchable instead of re-discovered:
#   retired tokens  — a rename is finished only when its old spelling appears nowhere
#                     (core/SCHEMA.md § Retired tokens). This is what makes an
#                     incomplete rename visible at the generator instead of at the leaves.
#   duplicate slugs — a work item lives in exactly one ledger; a copy is a bug
#                     (ROADMAP.md header). This is v1 criterion 2, verified by scan.
import re
from pathlib import Path

from entropy_corpus import (enforcement_paths, is_generated_mirror,  # noqa: F401
                            tracked_files)

# A bracketed slug is an item ID only in item position: after the bullet and the optional
# checkbox, decoration allowed. Elsewhere in prose it is a reference to an item that lives
# somewhere else, which is exactly what a single ledger is supposed to produce.
ITEM_SLUG = re.compile(
    r'^\s*(?:[-*>]+\s*)*(?:\[[ xX]\]\s*)*\**`?\[([a-z0-9][a-z0-9-]+)\](?!\()', re.M)


# A URL is quoted, not written. Somebody else chose those words and no rename of ours can reach
# them, so a captured link whose slug happens to contain a retired token is not an unfinished
# rename — it is evidence. Found 2026-08-24 when an INBOX capture turned the suite red and the
# check's own advice was to delete the line, which would have deleted Lucas's capture.
_URL = re.compile(r'<?https?://\S+')


def retired_hits(files: list, retired: dict, exempt: set) -> list:
    """Every surviving occurrence of a retired token, in content or in a filename."""
    exempt = {path.resolve() for path in exempt}
    # Hyphen is a boundary, not a word character: a retired token survives just as much
    # inside `fable-loop-engineering.md` as it does standing alone, and that compound
    # form is how an unfinished rename actually hides at the leaves.
    patterns = {token: re.compile(rf'(?<!\w){re.escape(token)}(?!\w)')
                for token in retired}
    hits = []
    for path in files:
        if path.resolve() in exempt:
            continue
        try:
            text = _URL.sub(lambda m: ' ' * len(m.group()), path.read_text(encoding='utf-8'))
        except (OSError, UnicodeDecodeError):
            continue
        for token, pattern in patterns.items():
            where = 'filename' if pattern.search(path.name) else None
            if not where and pattern.search(text):
                where = f'line {text[:pattern.search(text).start()].count(chr(10)) + 1}'
            if where:
                hits.append(f'{path}: retired token {token!r} survives ({where}).\n'
                            f'   Renamed to {retired[token]!r} — core/SCHEMA.md § Retired\n'
                            f'   tokens. If this line only *explains* the rename, delete it:\n'
                            f'   git holds the history.')
    return hits


def item_slugs(path: Path) -> set:
    """Slugs this file claims as items — bracketed, in item position."""
    try:
        return set(ITEM_SLUG.findall(path.read_text(encoding='utf-8')))
    except (OSError, UnicodeDecodeError):
        return set()


def duplicate_slugs(namespaces: dict) -> dict:
    """Slug -> the namespaces claiming it, for every slug claimed by more than one.

    Namespace, not file, is the unit. A goal file's achievement slugs (`build-mvp`,
    `mvp-scope`, `first-class`) are private vocabulary repeated across sibling goals by
    design — six startapps all having a `build-mvp` is not six copies of one item. What
    criterion 2 forbids is the *same work item* tracked in two different ledgers, so the
    caller declares the namespaces and all goal files share one.
    """
    owners = {}
    for namespace, ledgers in namespaces.items():
        for ledger in ledgers:
            for slug in item_slugs(ledger):
                owners.setdefault(slug, {})[namespace] = ledger
    return {slug: claims for slug, claims in owners.items() if len(claims) > 1}


STRIKETHROUGH = re.compile(r'~~[^~\n]+~~')
CODE_SPAN = re.compile(r'`[^`\n]*`')
DATED_REPORT = re.compile(
    r'\b(?:shipped|landed|deleted|removed|fixed|closed|merged|completed|resolved|retired)\b'
    r'[^.\n]{0,40}?\b20\d\d-\d\d-\d\d\b', re.I)
SETTLED = re.compile(r'\bSETTLED\b')
# Horizontal whitespace only: `\s` would swallow the preceding blank lines and report the
# finding against the top of the file instead of the line the reader has to go fix.
TICKED_ITEM = re.compile(
    r'^[ \t]*(?:[-*>]+[ \t]*)*(?:\d+[a-z]?\.[ \t]*)?(?:\[[xX]\]|✅)', re.M)
LEDGER_FILES = {'ROADMAP.md', 'GOALS.md', 'ISSUES.md'}
PLACEHOLDER = '← add'


def finished_work_hits(files: list, exempt: set) -> list:
    """Prose describing work that already landed — the corpse no link-checker can see.

    Completion is deletion (core/SCHEMA.md § No archive types): a ledger's length should
    measure remaining work. AGENTS.md bans strikethrough and SCHEMA bans the ticked item,
    both law with nothing enforcing them; the dated report is the general case.
    """
    exempt = {path.resolve() for path in exempt}
    hits = []
    for path in files:
        if path.suffix != '.md' or path.resolve() in exempt or is_generated_mirror(path):
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        # Strikethrough is read in PROSE only: inside a code span those four characters are DATA,
        # since a document about markdown must be able to write the spelling it converts. Position,
        # not presence — the test the vendor-directive check already applies to a model name.
        for label, match in (
            ('strikethrough', STRIKETHROUGH.search(CODE_SPAN.sub('', text))),
            ('a dated completion report', DATED_REPORT.search(text)),
            ('a SETTLED marker', SETTLED.search(text)),
            # A tick is a corpse only in a ledger; elsewhere the glyph is a legend marker,
            # which is how core/SCHEMA.md flags a required frontmatter field.
            ('a ticked item', TICKED_ITEM.search(text) if path.name in LEDGER_FILES else None),
        ):
            if not match:
                continue
            hits.append(f'{path}:{text[:match.start()].count(chr(10)) + 1}: {label} — '
                        f'prose describing finished work.\n'
                        f'   Cut it; git is the history (core/SCHEMA.md § No archive types).\n'
                        f'   Keep a line only if the next session needs it to *extend* the\n'
                        f'   work, and write that line as present-tense state.')
    return hits


def unanswered_placeholders(files: list, exempt: set) -> list:
    """A generator or a template asked a question, and nobody answered it.

    Split out of finished_work_hits 2026-08-15, where it was 70 of the 105 findings and
    carried that check's remediation — "cut it; git is the history". That advice is wrong
    here and acting on it is worse than ignoring it: the marker is not a record of
    finished work, it is a live request, and the generator writes it again on the next
    save. Three scaffolds emit the same glyph — the routing generator for a source file
    with no first-line comment and for a CONTEXT.md with no blurb, the refs template for
    its own unfilled field — and all three are answered at the source, never by deleting
    the marker.

    Counted per file rather than per row, so the number means "files that lie to a reader"
    and matches the enforced-read unit: whoever opens this CONTEXT.md pays for all of them.
    """
    exempt = {path.resolve() for path in exempt}
    hits = []
    for path in files:
        if path.name != 'CONTEXT.md' or path.resolve() in exempt:
            continue
        if is_generated_mirror(path):
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        if (rows := text.count(PLACEHOLDER)) == 0:
            continue
        line = text[:text.index(PLACEHOLDER)].count(chr(10)) + 1
        hits.append(f'{path}:{line}: {rows} unanswered placeholder(s).\n'
                    f'   Answer at the source — the described file\'s first-line comment,\n'
                    f'   this file\'s own blurb, or the template field. Deleting the marker\n'
                    f'   only makes the generator write it again on the next save.')
    return hits


WIKI_LINK = re.compile(r'\[\[([a-z0-9][a-z0-9-]*)\]\]')


def goal_vocabulary(goals_dir: Path) -> set:
    """Every name a `[[slug]]` is allowed to use: a goal file, or an item inside one.

    Decided 2026-07-30 (Lucas). Both halves are real pointers — `[[spec-driven-development]]`
    names the file, `[[prompt-dsl]]` names an item living inside `craft-flows.md` — and both
    are resolvable by scan, which is the only property a checker needs.
    """
    vocabulary = set()
    for goal in goals_dir.glob('*.md'):
        vocabulary.add(goal.stem)
        vocabulary |= item_slugs(goal)
    return vocabulary


def wiki_link_hits(files: list, vocabulary: set, exempt: set) -> list:
    """Every `[[slug]]` naming neither a goal file nor an item inside one."""
    exempt = {path.resolve() for path in exempt}
    hits = []
    for path in files:
        if path.suffix != '.md' or path.resolve() in exempt:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        for slug in sorted(set(WIKI_LINK.findall(text)) - vocabulary):
            hits.append(f'{path}: [[{slug}]] names no goal file and no item in one.\n'
                        f'   A `[[slug]]` points at brain/goals/<slug>.md or at a bracketed\n'
                        f'   item inside a goal file. Fix the slug, or write the goal.')
    return hits
