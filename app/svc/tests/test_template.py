from pathlib import Path
from pptx_template import parse_template
from fixtures.generate import build_template, build_source_pptx
from source_parser import parse_pptx
from planner import plan_slides


def test_template_parsing(tmp_path):
    tpl_path = tmp_path / 'brand_simple.pptx'
    build_template(tpl_path)
    meta = parse_template(tpl_path)
    assert 'layout_catalog' in meta
    assert len(meta['layout_catalog']) >= 5


def test_signature_extraction(tmp_path):
    src_path = tmp_path / 'mini_5slide.pptx'
    build_source_pptx(src_path)
    slides = parse_pptx(src_path)
    assert slides[1]['signature']['title'] is True
    assert slides[1]['signature']['bullets'] >= 1


def test_layout_matching(tmp_path):
    tpl_path = tmp_path / 't.pptx'
    build_template(tpl_path)
    tpl = parse_template(tpl_path)
    src_path = tmp_path / 's.pptx'
    build_source_pptx(src_path)
    slides = parse_pptx(src_path)
    plan = plan_slides(slides, tpl)
    assert len(plan) == len(slides)
    assert all('chosen_layout_id' in s for s in plan)
