# T1 pdf relevance: a figure the text points at is described, a crest in the header is not, a figure nobody described keeps its image and OCR, and a described one is never asked twice. Zero-token, no network.
import threading

from PIL import Image

import describe
import pdf_cache
import pdf_figures
import pdf_relevance
import pdf_twin
from test_pdf_twin import fake_engine, make_pdf, offline  # noqa: F401 — the fixture runs here too

TABLE = {'bias': (0, 1, -0.5), 'threshold': (0, 1, 0.5), 'named': (0, 1, 1.5), 'margin': (0, 1, -2.0),
         'decorative': (0, 1, -3.0)}


def figure(tmp_path, box=None, size=(320, 240), decorative=False, order=0):
    png = tmp_path / f'f{order}.png'
    Image.new('RGB', size, (250, 250, 250)).save(png)
    return pdf_figures.Figure(f'p01-fig{order + 1}', 1, png, 'x', size, decorative=decorative, pages={1},
                              box=box, scale=2.0, order=order)


def test_the_context_is_the_text_on_each_side_of_the_figure_marker():
    page = 'antes\n<!-- figure -->\nmeio\n<!-- figure -->\ndepois'
    assert pdf_relevance.context(page, 1) == ('\nmeio\n', '\ndepois')


def test_a_caption_under_the_figure_is_described_whatever_the_score(tmp_path):
    sig = pdf_relevance.signals(figure(tmp_path), 'texto\n<!-- figure -->\nFigura 3 – Fluxo do processo', '')
    assert sig['caption'] == 1.0 and pdf_relevance.judge(sig, TABLE) == ('describe', 'caption')


def test_text_naming_the_figure_raises_the_score_and_a_header_crest_is_hidden(tmp_path):
    named = pdf_relevance.signals(figure(tmp_path), 'Veja a tela abaixo.\n<!-- figure -->', '')
    crest = pdf_relevance.signals(figure(tmp_path, box=[0.4, 0.01, 0.6, 0.08], decorative=True),
                                  '<!-- figure -->\nRESOLUÇÃO Nº 1', 'MINISTÉRIO DA EDUCAÇÃO')
    assert crest['margin'] == 1.0 and crest['boilerplate'] == 1.0
    assert pdf_relevance.judge(named, TABLE)[0] == 'describe'
    assert pdf_relevance.judge(crest, TABLE)[0] == 'hide'


def test_a_figure_inside_a_real_table_counts_but_not_in_a_one_row_layout_table(tmp_path):
    real = '| a | b |\n|---|---|\n| 1 | <!-- figure --> |\n| 2 | x |'
    layout = '| <!-- figure --> | UNIVERSIDADE FEDERAL |'
    assert pdf_relevance.signals(figure(tmp_path), real, '')['in_table'] == 1.0
    assert pdf_relevance.signals(figure(tmp_path), layout, '')['in_table'] == 0.0


def test_a_big_figure_off_the_margins_is_described_unless_it_is_a_page_of_text(tmp_path):
    sig = pdf_relevance.signals(figure(tmp_path, box=[0.1, 0.2, 0.9, 0.7]), '<!-- figure -->', '')
    assert pdf_relevance.judge(sig, TABLE)[0] == 'describe'
    page_of_text = pdf_relevance.signals(figure(tmp_path, box=[0, 0, 1, 1]), '<!-- figure -->', 'palavra ' * 300)
    assert pdf_relevance.judge(page_of_text, TABLE)[1] != 'area 1.00'


def test_describer_none_shows_what_would_have_been_described(tmp_path):
    action, why = pdf_relevance.verdict(figure(tmp_path), 'Figura 1\n<!-- figure -->', '', 'none', TABLE)
    assert (action, why) == ('show', 'describer none')


def test_a_figure_nobody_described_keeps_its_image_and_ocr_and_says_why(tmp_path, monkeypatch):
    monkeypatch.setattr(pdf_relevance, 'load', lambda: TABLE | {'bias': (0, 1, 9.0)})   # the score would describe it
    calls = []
    done = pdf_twin.build(make_pdf(tmp_path / 'res.pdf'), 'docling', 'none', _engine=fake_engine(),
                          _describe=lambda *a: calls.append(a), _ocr=lambda p: 'texto da figura')
    text = done['twin'].read_text(encoding='utf-8')
    assert calls == [] and 'described_by: none | why: describer none' in text
    assert '~~~text ocr\ntexto da figura\n~~~' in text and '[no description]' not in text


def test_an_answer_is_cached_as_it_lands_and_read_back_in_any_later_pdf(tmp_path, monkeypatch):
    monkeypatch.setattr(pdf_relevance, 'verdict', lambda *a: ('describe', 'test'))
    calls = []

    def said(image, describer, ocr_text):
        calls.append(image)
        return describe.Description('um fluxograma de três etapas', 'agy', None, False)
    cache = pdf_cache.Cache(tmp_path / 'c.jsonl')
    page = 'Figura 1\n'
    for name in ('a', 'b'):
        pdf_twin.build(make_pdf(tmp_path / f'{name}.pdf'), 'docling', _engine=fake_engine(page_md=page),
                       _describe=said, _ocr=lambda p: '', cache=cache)
    lines = (tmp_path / 'c.jsonl').read_text(encoding='utf-8').splitlines()
    assert len(calls) == 1 and len(lines) == 1 and 'um fluxograma de três etapas' in lines[0]


def test_a_flagged_answer_is_not_cached(tmp_path):
    cache = pdf_cache.Cache(tmp_path / 'c.jsonl')
    cache.put('k', describe.Description('talvez', 'agy', 0.1, True))
    assert cache.get('k') is None and not (tmp_path / 'c.jsonl').exists()


def test_figures_are_described_by_several_workers_at_once(tmp_path, monkeypatch):
    monkeypatch.setattr(pdf_relevance, 'verdict', lambda *a: ('describe', 'test'))
    together = threading.Barrier(pdf_twin.WORKERS)   # passes only if every worker is inside at once

    def slow(image, describer, ocr_text):
        together.wait(timeout=30)   # a backstop: one worker alone breaks the barrier and the build raises
        return describe.Description('uma tela', 'agy', None, False)
    pdf_twin.build(make_pdf(tmp_path / 'res.pdf'), 'docling', _describe=slow, _ocr=lambda p: '',
                   _engine=fake_engine(page_md='Figura 1\n', figures=pdf_twin.WORKERS))
    assert not together.broken
