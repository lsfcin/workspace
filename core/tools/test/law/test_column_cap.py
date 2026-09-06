# T0 column cap: how wide one authored .md line may be, and the four shapes exempt from it.
# Zero-token, runs in verify-fast.
#
# Split from test_file_law.py 2026-08-24 at the 200-line gate. The seam is the one that file
# already declares in its own header: it exists because "a code file" was defined five times, so
# it answers WHAT A FILE IS. How wide a line may be is a different question with different
# exemptions, and it had no coverage at all — both of the cap's original exemptions were untested
# law until the third was ruled.
#
# The law is core/hooks/file_law.py `over_column_cap`; the reasoning behind each exemption is
# core/hooks/limits.env § BLOCK_COLS. Neither is restated here — these only hold it to them.
from conftest import WORKSPACE_ROOT  # noqa: F401  (sets sys.path for the enforcement layer)

from file_law import load_limits, over_column_cap  # noqa: E402

LONG = 'x' * 200  # comfortably past any cap this suite passes in
COLS = load_limits()['BLOCK_COLS']


def test_an_ordinary_long_line_is_flagged() -> None:
    """The cap itself, before any exemption: this is what the other cases are exceptions to."""
    assert over_column_cap(f'# t\n{LONG}\n', COLS) == [2]


def test_a_long_table_row_is_exempt() -> None:
    """Wrapping a row stops it being a table — 15 of core/SCHEMA.md's 15 over-long lines were."""
    assert over_column_cap(f'| {LONG} |\n', COLS) == []


def test_a_long_line_in_a_fenced_block_is_exempt() -> None:
    """A directory tree or an aligned CLI listing carries its meaning in the columns."""
    assert over_column_cap(f'text\n```\n{LONG}\n```\n', COLS) == []


def test_prose_after_a_fence_closes_is_flagged_again() -> None:
    """The fence toggles; it does not switch the cap off for the rest of the file."""
    assert over_column_cap(f'```\n{LONG}\n```\n{LONG}\n', COLS) == [4]


def test_a_long_frontmatter_line_is_exempt() -> None:
    """Ruled 2026-08-24 (Lucas). Every reader of this block is a line regex, so a folded
    scalar is legal YAML and unreadable by us — which lands where unwrappable lands."""
    assert over_column_cap(f'---\ndescription: {LONG}\n---\n# t\n', COLS) == []


def test_the_exemption_covers_the_block_not_one_key() -> None:
    """`name:` and `allowed-tools:` are parsed by the same line regexes as `description:`."""
    assert over_column_cap(f'---\nallowed-tools: {LONG}\n---\n# t\n', COLS) == []


def test_a_description_line_in_the_BODY_is_not_exempt() -> None:
    """The bound is the whole ruling: the exemption is the leading block, not the word.

    Without this the exemption is reachable from authored prose, which is exactly the
    hollowing-out that frontmatter scoping exists to prevent.
    """
    assert over_column_cap(f'---\nname: t\n---\n# t\ndescription: {LONG}\n', COLS) == [5]


def test_only_the_LEADING_block_is_frontmatter() -> None:
    """A `---` rule mid-document is a horizontal rule, and opens nothing."""
    assert over_column_cap(f'# t\n---\ndescription: {LONG}\n---\n', COLS) == [3]


def test_an_unterminated_frontmatter_marker_exempts_nothing() -> None:
    """A stray opening `---` must not switch the cap off for the whole file."""
    assert over_column_cap(f'---\nname: t\n# t\n{LONG}\n', COLS) == [4]


def test_a_line_long_only_because_of_a_url_is_exempt() -> None:
    """The fourth exemption. A URL is one token; no rewrap makes it shorter, so the cap could only
    buy worse prose around an object that will not move."""
    url = 'https://example.org/' + 'p' * 150
    assert not over_column_cap(f'see the source ([fonte]({url})).', COLS)
    assert not over_column_cap(f'reference: <{url}>', COLS)


def test_a_relative_link_target_counts_the_same_way() -> None:
    """A repo path is as unbreakable as a URL, and heading text carrying one is the shape that
    actually tripped this — `.zcode/SPECS.md` § Measured answers."""
    assert not over_column_cap(
        '### Measured answers ([the record](../core/experiments/' + 'a' * 120 + '.md))', COLS)


def test_the_authored_half_is_still_measured_at_full_width() -> None:
    """The bound that keeps it from hollowing the cap out: a long sentence does not become legal
    by having a link dropped into it."""
    assert over_column_cap(f'{LONG} [x](https://example.org/y)', COLS) == [1]


def test_a_bare_word_with_a_slash_is_not_a_link() -> None:
    """Only a real target is subtracted — `](...)`, an autolink, or a scheme. Ordinary prose that
    happens to contain `core/hooks/` stays fully measured, or the exemption would swallow paths
    written inline as text."""
    assert over_column_cap('core/hooks/limits.env ' + LONG, COLS) == [1]
