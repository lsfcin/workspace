# pdf_relevance.py — whether a figure is worth a vision call: the text around it first, then where it sits, how big it is and what its pixels look like.
#
# WHY. Every figure went to the vision model, 31 s each (2026-11-24): a crest, a signature and a
# screenshot cost the same. Lucas, 2026-11-25: read the text first, and let size, position, a table
# around it and a "veja a figura abaixo" weigh in. The panel (argon, codex) added the image's own
# strokes and asked for weights learned, not guessed: a logistic score over these signals, its
# weights DATA in relevance.tsv, trained by bench/relevance_train.py on figures labelled by hand.
#
# Three answers: `describe` (the vision call), `show` (image and OCR kept, `described_by: none`),
# `hide` (a crest or letterhead below the bar: no trace, as the old decorative cut did).
#
# WHAT IS NOT HERE. Weights trained on one collection say nothing about another, so the tool ships
# none: a collection brings its own PROFILE, a folder passed as `--relevance <dir>`:
#   relevance.tsv    the weights and the bar (required; written by bench/relevance_train.py --write)
#   decorations.txt  looks of its crests and logos, one hex hash per line (optional)
#   boilerplate.txt  words its letterheads repeat, one per line (optional)
# Without a profile no figure is scored: every one that is not decorative is described.
from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path

FIGURE = '<!-- figure -->'
WEIGHTS, DECORATIONS, BOILERPLATE = 'relevance.tsv', 'decorations.txt', 'boilerplate.txt'
WINDOW = 250          # characters of page text each side of the figure that are read
MARGIN = 0.18         # the header and footer bands, as a share of the page height (the panel's figure)
BIG = 0.18            # a figure this share of the page is content unless its OCR says it is a page of text
TEXT_PAGE_WORDS = 200
SAMPLE_SIDE = 200     # the crop is shrunk to this before its pixels are read

NAMED = re.compile(r'\b(figura|fig\.|imagem|ilustra\w*|tela|print|captura|quadro|fluxograma|organograma|'
                   r'gr[áa]fico|diagrama|esquema|mapa|figure|screen)', re.I)
POINTER = re.compile(r'\b(abaixo|acima|a seguir|ao lado|seguinte|clique|clicar|selecion\w*|bot[ãa]o|[íi]cone|'
                     r'menu|aba|janela|marque|below|above|click)\b', re.I)
CAPTION = re.compile(r'^\W*(figura|fig\.|quadro|imagem|gr[áa]fico|fonte|figure)\b', re.I)
WORD = re.compile(r'[a-zà-ÿ]{4,}', re.I)

NEAR = 20             # bits of the 256-bit average hash two crops of one crest differ by, at most (bench, 2026-11-25)

SIGNALS = ('named', 'pointer', 'caption', 'in_table', 'margin', 'edge', 'area', 'side', 'repeats', 'decorative',
           'ocr_words', 'boilerplate', 'ink', 'lines', 'colours', 'text_around', 'doc_figures', 'doc_big')


def area(fig) -> float:
    box = fig.box or [0.0, 0.0, 0.0, 0.0]   # an engine that does not say where: no position, no area
    return round(max(box[2] - box[0], 0) * max(box[3] - box[1], 0), 4)


def document(areas: list[float]) -> dict[str, float]:
    """What the whole PDF says about its figures, from the area of each distinct one: a manual of
    screenshots makes its small icons matter (the bench's hardest misses were toolbar icons)."""
    return {'doc_figures': round(math.log1p(len(areas)), 3),
            'doc_big': round(sum(a >= BIG for a in areas) / len(areas), 3) if areas else 0.0}


@dataclass(frozen=True)
class Profile:
    """One collection's relevance: its weights, its crests, its letterhead words."""
    table: dict
    looks: tuple[int, ...] = ()
    boilerplate: frozenset[str] = frozenset()


def _lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [ln.strip() for ln in path.read_text(encoding='utf-8').splitlines() if ln.strip() and not ln.startswith('#')]


def profile(folder: Path | None) -> Profile | None:
    """The profile in `folder`, or None (score nothing) when no folder is given."""
    if folder is None:
        return None
    if not (folder / WEIGHTS).exists():
        raise FileNotFoundError(f'{folder}: a relevance profile needs {WEIGHTS} (bench/relevance_train.py --write)')
    return Profile(load(folder / WEIGHTS), tuple(int(h, 16) for h in _lines(folder / DECORATIONS)),
                   frozenset(w.lower() for w in _lines(folder / BOILERPLATE)))


def known(look: str, known_looks: list[int]) -> bool:
    if not known_looks:
        return False
    mine = int(look, 2)
    return any(bin(mine ^ other).count('1') <= NEAR for other in known_looks)


def context(page_md: str, order: int) -> tuple[str, str]:
    """The page text just before and just after the figure's marker."""
    parts = page_md.split(FIGURE)
    if order + 1 >= len(parts):
        return page_md[-WINDOW:], ''
    return parts[order][-WINDOW:], parts[order + 1][:WINDOW]


def _adjacent_lines(before: str, after: str) -> list[str]:
    above = [ln for ln in before.splitlines() if ln.strip()][-1:]
    below = [ln for ln in after.splitlines() if ln.strip()][:1]
    return above + below


def _in_table(before: str, after: str) -> bool:
    """Inside a table of at least three rows, not on its first: a one-row layout table holds letterheads."""
    line = (before.rsplit('\n', 1)[-1] + after.split('\n', 1)[0]).strip()
    if not line.startswith('|'):
        return False
    above = [ln for ln in before.splitlines()[:-1] if ln.strip()]
    rows_above = 0
    for ln in reversed(above):
        if not ln.strip().startswith('|'):
            break
        rows_above += not set(ln.strip()) <= set('|-: ')
    rows_below = 0
    for ln in after.splitlines()[1:]:
        if not ln.strip().startswith('|'):
            break
        rows_below += 1
    return rows_above >= 1 and rows_above + rows_below + 1 >= 3


def _pixels(image: Path) -> tuple[float, float, float]:
    """ink: share of pixels off the background; lines: share of rows and columns crossed by a long
    stroke (boxes, grids, window frames); colours: how many distinct colours, log-scaled."""
    from PIL import Image
    with Image.open(image) as im:
        rgb = im.convert('RGB')
        rgb.thumbnail((SAMPLE_SIDE, SAMPLE_SIDE))
    grey = rgb.convert('L')
    w, h = grey.size
    px = list(grey.tobytes())
    background = max(set(p // 16 for p in px), key=[p // 16 for p in px].count) * 16 + 8
    off = [abs(p - background) > 40 for p in px]
    ink = sum(off) / len(off)
    rows = sum(sum(off[y * w:(y + 1) * w]) > 0.5 * w for y in range(h))
    cols = sum(sum(off[y * w + x] for y in range(h)) > 0.5 * h for x in range(w))
    raw = rgb.tobytes()
    colours = len({(raw[i] // 32, raw[i + 1] // 32, raw[i + 2] // 32) for i in range(0, len(raw), 3)})
    return round(ink, 3), round((rows + cols) / (w + h), 3), round(math.log1p(colours), 3)


def signals(fig, page_md: str, ocr_text: str, doc: dict | None = None, prof: Profile | None = None) -> dict[str, float]:
    """Every signal of one figure, as numbers; `fig` is a pdf_figures.Figure, `doc` is document()."""
    boilerplate, known_looks = (prof.boilerplate, prof.looks) if prof else (frozenset(), ())
    before, after = context(page_md, fig.order)
    near = before[-WINDOW:] + ' ' + after[:WINDOW]
    box = fig.box or [0.0, 0.0, 0.0, 0.0]
    words = [w.lower() for w in WORD.findall(ocr_text)]
    ink, lines, colours = _pixels(fig.source)
    return {
        'named': float(bool(NAMED.search(near))),
        'pointer': float(bool(POINTER.search(near))),
        'caption': float(any(CAPTION.search(ln) for ln in _adjacent_lines(before, after))),
        'in_table': float(_in_table(before, after)),
        'margin': float(fig.box is not None and (box[3] <= MARGIN or box[1] >= 1 - MARGIN)),
        'edge': round(min(box[1], 1 - box[3]), 4) if fig.box else 0.5,   # how far from the top or bottom edge
        'area': area(fig),
        'side': round(math.log1p(min(fig.size) / fig.scale), 3),
        'repeats': float(len(fig.pages)),
        'decorative': float(fig.decorative),
        'ocr_words': round(math.log1p(len(words)), 3),
        'boilerplate': round(sum(w in boilerplate for w in words) / len(words), 3) if words else 0.0,
        'ink': ink, 'lines': lines, 'colours': colours,
        'text_around': round(math.log1p(len(page_md.replace(FIGURE, '').strip())), 3),
        **(doc or {'doc_figures': 0.0, 'doc_big': 0.0}),
        'known': float(known(fig.look, list(known_looks))),   # a rule, not a weighed signal
    }


def load(path: Path) -> dict[str, tuple[float, float, float]]:
    """{signal: (mean, std, weight)}, plus `bias` and `threshold` in the weight column."""
    table = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip() and not line.startswith('#') and not line.startswith('signal\t'):
            name, mean, std, weight = line.split('\t')
            table[name] = (float(mean), float(std), float(weight))
    return table


def score(sig: dict[str, float], table: dict) -> float:
    """p(relevant) under the learned weights; a signal the table lacks weighs nothing."""
    z = table['bias'][2] + sum(table[k][2] * (v - table[k][0]) / (table[k][1] or 1)
                               for k, v in sig.items() if k in table)
    return 1 / (1 + math.exp(-z))


def judge(sig: dict[str, float], table: dict) -> tuple[str, str]:
    """('describe' | 'show' | 'hide', why). The rules first, the score for the rest."""
    if sig['caption']:
        return 'describe', 'caption'
    if sig.get('known'):
        return ('hide' if sig['decorative'] else 'show'), 'known decoration'
    if sig['area'] >= BIG and not sig['margin'] and sig['ocr_words'] < math.log1p(TEXT_PAGE_WORDS):
        return 'describe', f'area {sig["area"]:.2f}'
    p = score(sig, table)
    if p >= table['threshold'][2]:
        return 'describe', f'score {p:.2f}'
    return ('hide' if sig['decorative'] else 'show'), f'score {p:.2f}'


def verdict(fig, page_md: str, ocr_text: str, describer: str, prof: Profile | None,
            doc: dict | None = None) -> tuple[str, str]:
    """judge() under the profile; without one, every figure that is not decorative is described.
    `--describer none` turns every `describe` into `show`."""
    if prof is None:
        action, why = ('hide', 'decorative') if fig.decorative else ('describe', 'no profile')
    else:
        action, why = judge(signals(fig, page_md, ocr_text, doc, prof), prof.table)
    if action == 'describe' and describer == 'none':
        return 'show', 'describer none'
    return action, why
