# T1 pdf figures: a logo repeated on every page is one decorative figure, distinct figures stay distinct, and the audit's word coverage counts what the twin kept. Zero-token, no network.
from PIL import Image, ImageDraw

import pdf_figures
import pdf_meta


def crop(path, shade, mark=None, size=(320, 240)):
    im = Image.new('RGB', size, (shade, shade, shade))
    if mark:
        ImageDraw.Draw(im).rectangle(mark, fill=(255 - shade, 0, 0))
    im.save(path)
    return str(path)


def test_the_same_image_on_many_pages_is_one_decorative_figure(tmp_path):
    logo = [{'page': p, 'file': crop(tmp_path / f'logo{p}.png', 30, (10, 10, 150, 100))} for p in (1, 2, 3)]
    chart = {'page': 2, 'file': crop(tmp_path / 'chart.png', 220, (60, 20, 250, 200))}
    figures = pdf_figures.name_all([logo[0], logo[1], chart, logo[2]], total_pages=3)
    assert [f.name for f in figures] == ['p01-fig1', 'p02-fig1', 'p02-fig2', 'p03-fig1']
    assert [f.same_as for f in figures] == [None, 'p01-fig1', None, 'p01-fig1']
    assert [f.decorative for f in figures] == [True, True, False, True]


def test_an_image_on_one_page_of_a_short_pdf_is_content(tmp_path):
    figures = pdf_figures.name_all([{'page': 1, 'file': crop(tmp_path / 'a.png', 30)}], total_pages=1)
    assert not figures[0].decorative


def test_a_small_image_is_decorative_even_on_one_page_and_a_big_one_is_content(tmp_path):
    crest = {'page': 1, 'file': crop(tmp_path / 'crest.png', 30, (10, 10, 60, 60), size=(94, 93)), 'scale': 150 / 72}
    photo = {'page': 1, 'file': crop(tmp_path / 'photo.png', 200, (10, 10, 60, 60), size=(151, 90)), 'scale': 150 / 72}
    small, big = pdf_figures.name_all([crest, photo], total_pages=1)
    assert small.size == (94, 93) and small.decorative
    assert not big.decorative


def test_the_size_limit_is_in_page_points_whatever_scale_the_engine_rendered_at(tmp_path):
    """Docling crops at 2 px per point: a 60 pt crest is a 120 px file and still decorative."""
    crest = {'page': 1, 'file': crop(tmp_path / 'c.png', 30, size=(120, 118)), 'scale': 2.0}
    chart = {'page': 1, 'file': crop(tmp_path / 'g.png', 200, (10, 10, 90, 90), size=(320, 240)), 'scale': 2.0}
    small, big = pdf_figures.name_all([crest, chart], total_pages=1)
    assert small.decorative and not big.decorative


def test_a_repeat_of_a_decorative_figure_is_decorative(tmp_path):
    first, again = pdf_figures.name_all(
        [{'page': p, 'file': crop(tmp_path / f'{p}.png', 30, (5, 5, 50, 50), size=(100, 100)), 'scale': 2.0} for p in (1, 2)], 9)
    assert first.decorative and again.decorative and again.same_as == first.name


def test_a_repeat_links_to_its_first_appearance_and_is_not_described_again(tmp_path):
    first, again = pdf_figures.name_all(
        [{'page': p, 'file': crop(tmp_path / f'{p}.png', 30, (5, 5, 90, 90))} for p in (1, 2)], 2)
    assert pdf_figures.block(again, 'img/p01-fig1.jpg') == (
        '![p02-fig1](img/p01-fig1.jpg)\n\n<!-- figure p02-fig1 | same image as p01-fig1 -->\n')


def test_coverage_counts_each_word_as_often_as_the_reference_has_it():
    assert pdf_meta.coverage('art art art lei', 'art lei') == 0.5
    assert pdf_meta.coverage('art lei', 'art art lei lei extra words') == 1.0


def test_text_layer_is_judged_page_by_page():
    full, empty = 'palavra ' * 20, ''
    assert pdf_meta.text_layer([full, full]) == 'born-digital'
    assert pdf_meta.text_layer([empty, empty]) == 'scanned'
    assert pdf_meta.text_layer([full, empty]) == 'mixed'
