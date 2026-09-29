# T1 pptx motion: a build shows what it means to show, lint names what a room would see wrong, and flatten turns every click into a page.
import io, pathlib, sys

import pytest

pptx = pytest.importorskip("pptx")
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "slides"))
import pptx_check, pptx_motion
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches


def _deck():
    prs = pptx.Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    return prs


def _node(slide, label, x):
    sh = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(3), Inches(2), Inches(2))
    sh.text_frame.text = label
    return sh


def _reopen(prs):
    buf = io.BytesIO(); prs.save(buf); buf.seek(0)
    return pptx.Presentation(buf)


def test_an_entrance_animates_the_whole_shape_not_only_its_label():
    prs = _deck(); s = prs.slides.add_slide(prs.slide_layouts[6])
    a = _node(s, "RNN", 1)
    pptx_motion.timeline(s, [[pptx_motion.fade_in(a)]])
    assert pptx_check.lint(_reopen(prs)) == []
    s._element.find(".//" + pptx_motion.q(pptx_motion.P, "bldP")).attrib.pop("animBg")
    assert any("animBg" in f for f in pptx_check.lint(prs))


def test_timing_ids_are_unique_across_clicks_and_triggers():
    prs = _deck(); s = prs.slides.add_slide(prs.slide_layouts[6])
    a, b = _node(s, "a", 1), _node(s, "b", 5)
    pptx_motion.timeline(s, [[pptx_motion.fade_in(a), pptx_motion.dim(b)], [pptx_motion.grow(a, 150)]],
                         triggers=[(b, [pptx_motion.spin(b, 90)])])
    ids = [c.get("id") for c in s._element.iter(pptx_motion.q(pptx_motion.P, "cTn"))]
    assert len(ids) == len(set(ids))


def test_a_move_and_a_scale_on_one_click_with_different_durations_is_flagged():
    prs = _deck(); s = prs.slides.add_slide(prs.slide_layouts[6])
    a = _node(s, "LSTM", 1)
    pptx_motion.timeline(s, [[pptx_motion.move(a, "M 0 0 L 0.2 0 E", dur=800), pptx_motion.grow(a, 150, dur=600)]])
    assert any("desync" in f for f in pptx_check.lint(prs))


def test_a_move_over_a_third_of_the_slide_is_flagged():
    prs = _deck(); s = prs.slides.add_slide(prs.slide_layouts[6])
    a = _node(s, "h", 1)
    pptx_motion.timeline(s, [[pptx_motion.move(a, "M 0 0 L 0.6 0 E")]])
    assert any("third" in f for f in pptx_check.lint(prs))


def test_a_morph_with_nothing_paired_is_flagged_and_a_named_pair_is_not():
    prs = _deck()
    s1, s2 = prs.slides.add_slide(prs.slide_layouts[6]), prs.slides.add_slide(prs.slide_layouts[6])
    pptx_motion.morph_key(_node(s1, "x", 1), "x")
    b = _node(s2, "x", 6)
    pptx_motion.transition(s2, "morph")
    assert any("nothing is paired" in f for f in pptx_check.lint(prs))
    pptx_motion.morph_key(b, "x")
    assert pptx_check.lint(_reopen(prs)) == []


def test_flatten_gives_one_page_per_click_in_order_with_each_state():
    prs = _deck()
    first = prs.slides.add_slide(prs.slide_layouts[6])
    s = prs.slides.add_slide(prs.slide_layouts[6])
    last = prs.slides.add_slide(prs.slide_layouts[6])
    a, b = _node(s, "a", 1), _node(s, "b", 5)
    x0 = b.left
    pptx_motion.timeline(s, [[pptx_motion.fade_in(a)], [pptx_motion.move(b, "M 0 0 L 0.1 0 E")], [pptx_motion.fade_out(a)]])
    assert pptx_check.flatten(prs) == 3
    prs = _reopen(prs)
    names = [[sh.text_frame.text for sh in sl.shapes] for sl in prs.slides]
    assert names == [[], ["b"], ["a", "b"], ["a", "b"], ["b"], []]
    moved = [sh for sh in prs.slides[3].shapes if sh.text_frame.text == "b"][0]
    assert moved.left == x0 + int(0.1 * prs.slide_width)
    assert all(sl._element.find(pptx_motion.q(pptx_motion.P, "timing")) is None for sl in prs.slides)


def test_a_back_link_returns_to_the_slide_the_talk_came_from():
    prs = _deck(); s = prs.slides.add_slide(prs.slide_layouts[6])
    btn = pptx_motion.link(_node(s, "voltar", 1))
    h = btn._element.find(".//" + pptx_motion.q(pptx_motion.A, "hlinkClick"))
    assert h.get("action") == "ppaction://hlinkshowjump?jump=lastslideviewed"
