# test_video_relevance.py — T1 unit tests for video_relevance (no model download, no network)
import video_relevance as vr

GOAL_A = """# [ craft | research | year ] always-on autonomous local AI

Run models locally, compatible with Claude Code.
https://example.com/paper.pdf

<!-- stats:start -->
last-touch: 2026-07-22
<!-- stats:end -->
"""

GOAL_B = """# [ fun | dance | year ] frevo

Passos de frevo, aulas semanais.
"""


def _write(tmp_path, **files):
    for name, body in files.items():
        (tmp_path / name).write_text(body, encoding="utf-8")
    return tmp_path


def test_load_goals_parses_header(tmp_path):
    d = _write(tmp_path, **{"local-ai.md": GOAL_A})
    (g,) = vr.load_goals(d)
    assert g["slug"] == "local-ai"
    assert g["title"] == "always-on autonomous local AI"
    assert g["tags"] == ["craft", "research", "year"]


def test_load_goals_strips_auto_blocks_and_urls(tmp_path):
    d = _write(tmp_path, **{"local-ai.md": GOAL_A})
    (g,) = vr.load_goals(d)
    assert "last-touch" not in g["text"]
    assert "stats:start" not in g["text"]
    assert "example.com" not in g["text"]
    assert "Run models locally" in g["text"]


def test_load_goals_skips_non_goal_files(tmp_path):
    d = _write(tmp_path, **{"local-ai.md": GOAL_A, "CONTEXT.md": "# ctx", "ARCHETYPE.md": "# a"})
    assert [g["slug"] for g in vr.load_goals(d)] == ["local-ai"]


def test_load_goals_missing_dir_is_empty():
    assert vr.load_goals("/nonexistent/goals") == []


class FakeEncoder:
    """Returns a fixed vector per text substring — no model, no network."""

    def __init__(self, table):
        self.table = table
        self.seen = []

    def __call__(self, texts):
        self.seen = list(texts)
        out = []
        for t in texts:
            vec = next((v for k, v in self.table.items() if k in t), [0.0, 0.0])
            out.append(vec)
        return out


def _goals():
    return [{"slug": "local-ai", "title": "local AI", "path": "a.md", "text": "run models locally"},
            {"slug": "frevo", "title": "frevo", "path": "b.md", "text": "passos de frevo"}]


def test_relevance_ranks_closest_goal_first():
    enc = FakeEncoder({"query:": [1.0, 0.0], "local AI": [0.9, 0.1], "frevo": [0.1, 0.9]})
    out = vr.relevance("a video about running llms on my own gpu", goals=_goals(), encoder=enc)
    assert [m["slug"] for m in out] == ["local-ai", "frevo"]
    assert out[0]["score"] > out[1]["score"]


def test_relevance_margin_is_relative_to_mean():
    enc = FakeEncoder({"query:": [1.0, 0.0], "local AI": [0.9, 0.1], "frevo": [0.1, 0.9]})
    out = vr.relevance("x", goals=_goals(), encoder=enc)
    assert sum(m["margin"] for m in out) == 0  # margins are mean-centred
    assert out[0]["margin"] > 0 > out[1]["margin"]


def test_relevance_applies_e5_prefixes():
    enc = FakeEncoder({"query:": [1.0, 0.0]})
    vr.relevance("some text", goals=_goals(), encoder=enc)
    assert enc.seen[0].startswith("query: ")
    assert all(t.startswith("passage: ") for t in enc.seen[1:])


def test_relevance_top_n_truncates():
    enc = FakeEncoder({"query:": [1.0, 0.0], "local AI": [0.9, 0.1], "frevo": [0.1, 0.9]})
    assert len(vr.relevance("x", goals=_goals(), top_n=1, encoder=enc)) == 1


def test_relevance_empty_text_returns_empty():
    enc = FakeEncoder({})
    assert vr.relevance("   ", goals=_goals(), encoder=enc) == []


def test_relevance_no_goals_returns_empty():
    enc = FakeEncoder({})
    assert vr.relevance("text", goals=[], encoder=enc) == []


def test_format_matches_handles_empty():
    assert vr.format_matches([]) == "(no goal matches)"


def test_format_matches_one_line_per_match():
    enc = FakeEncoder({"query:": [1.0, 0.0], "local AI": [0.9, 0.1], "frevo": [0.1, 0.9]})
    out = vr.format_matches(vr.relevance("x", goals=_goals(), encoder=enc))
    assert len(out.splitlines()) == 2
    assert "local-ai" in out
