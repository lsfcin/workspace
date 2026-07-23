#!/mnt/workspace/.venv/bin/python3
# video_relevance.py — rank brain/goals against ANY text (not just video) via local multilingual embeddings; import relevance() from anywhere
import functools, pathlib, re

_ROOT = pathlib.Path(__file__).resolve().parents[2]
GOALS_DIR = _ROOT / "brain" / "goals"
# Multilingual on purpose: goal files are PT-BR, video text is often EN. A monolingual
# encoder scores cross-language pairs near zero regardless of topic.
# -base, not -small: measured, see video.SETUP.md. -small mis-ranks short captions.
MODEL = "intfloat/multilingual-e5-base"
MAX_CHARS = 1500

# Auto-generated blocks carry no semantics — they'd make every goal look alike.
_BLOCK = re.compile(r"<!--\s*(stats|done|data|routing):start\s*-->.*?<!--\s*\1:end\s*-->", re.S)
_URL = re.compile(r"https?://\S+")
_NOISE = re.compile(r"[>*`|_#\[\]]")
_HEADER = re.compile(r"^#\s*\[([^\]]*)\]\s*(.*)$")
_SKIP = {"CONTEXT.md", "ARCHETYPE.md"}


def _clean(raw):
    t = _BLOCK.sub(" ", raw)
    t = _URL.sub(" ", t)
    t = _NOISE.sub(" ", t)
    return re.sub(r"\s+", " ", t).strip()[:MAX_CHARS]


def load_goals(goals_dir=None):
    """Read brain/goals/*.md into {slug, title, tags, path, text} records."""
    d = pathlib.Path(goals_dir or GOALS_DIR)
    if not d.is_dir():
        return []
    goals = []
    for p in sorted(d.glob("*.md")):
        if p.name in _SKIP:
            continue
        raw = p.read_text(encoding="utf-8", errors="replace")
        first = raw.splitlines()[0] if raw.strip() else ""
        m = _HEADER.match(first)
        title = (m.group(2) if m else first.lstrip("# ")).strip()
        tags = [x.strip() for x in m.group(1).split("|")] if m else []
        goals.append({"slug": p.stem, "title": title or p.stem, "tags": tags,
                      "path": str(p), "text": _clean(raw)})
    return goals


@functools.lru_cache(maxsize=2)
def _model(name):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(name)


def default_encoder(name=MODEL):
    """Lazy local encoder. Imported only when called, so tests inject a fake and stay offline."""
    model = _model(name)
    return lambda texts: model.encode(texts, normalize_embeddings=True, show_progress_bar=False)


def _dot(a, b):
    return float(sum(x * y for x, y in zip(a, b)))


def relevance(text, goals=None, top_n=5, encoder=None):
    """Rank goals by semantic similarity to `text`. Returns [{slug, title, score, margin}].

    `margin` = score minus the mean score across all goals. Prefer it over `score` for
    routing decisions: e5 similarities sit in a narrow high band (~0.75-0.90), so an
    absolute threshold is brittle while the spread above the mean is stable.
    """
    text = (text or "").strip()
    goals = load_goals() if goals is None else goals
    if not text or not goals:
        return []
    encode = encoder or default_encoder()
    # e5 requires these prefixes — without them the asymmetric query/passage training is wasted.
    vecs = list(encode([f"query: {text[:MAX_CHARS]}"] +
                       [f"passage: {g['title']}. {g['text']}" for g in goals]))
    q, rest = vecs[0], vecs[1:]
    scores = [_dot(q, v) for v in rest]
    mean = sum(scores) / len(scores)
    ranked = [{"slug": g["slug"], "title": g["title"], "path": g["path"],
               "score": round(s, 4), "margin": round(s - mean, 4)}
              for g, s in zip(goals, scores)]
    ranked.sort(key=lambda r: r["score"], reverse=True)
    return ranked[:top_n] if top_n else ranked


def format_matches(matches):
    """One line per match, for CLI output and /inbox route suggestions."""
    if not matches:
        return "(no goal matches)"
    return "\n".join(
        f"  {m['margin']:+.3f}  {m['slug']:<28} {m['title']}" for m in matches)
