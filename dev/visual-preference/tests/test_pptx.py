"""The slide and poster templates, built per release."""
import pytest
from pptx import Presentation
from pptx.util import Emu, Mm

import build_pptx


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("pptx")
    return {p.name: p for p in build_pptx.build_pptx(out)}


def master_fill(prs):
    bg = prs.slide_master.element.find(".//{http://schemas.openxmlformats.org/presentationml/2006/main}bg")
    return bg.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr").get("val").lower()


def theme_fonts(prs):
    import re
    part = prs.slide_master.part.part_related_by("http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme")
    xml = part.blob.decode("utf-8")
    major = re.search(r"<a:majorFont><a:latin typeface=\"([^\"]+)\"", xml).group(1)
    minor = re.search(r"<a:minorFont><a:latin typeface=\"([^\"]+)\"", xml).group(1)
    return major, minor


def test_files(built):
    assert set(built) == {"slides-dark.pptx", "slides-light.pptx", "poster-a0.pptx"}


@pytest.mark.parametrize("name,ground", [("slides-dark.pptx", "131512"), ("slides-light.pptx", "f2f3ef")])
def test_slides(built, name, ground):
    prs = Presentation(built[name])
    assert master_fill(prs) == ground
    assert {l.name for l in prs.slide_layouts} == {"Title", "Title and figure", "Section"}
    assert theme_fonts(prs) == ("Albert Sans", "Albert Sans")
    texts = [sp.text_frame.text for sp in prs.slide_master.shapes if sp.has_text_frame]
    assert "Yili Yang" in texts
    stops = [sp for sp in prs.slide_master.shapes if sp.shape_type == 1 and sp.name == "stop"]
    assert len(stops) == 1
    assert str(stops[0].fill.fore_color.rgb).lower() in {"a3b86c", "566a26"}


def test_poster(built):
    prs = Presentation(built["poster-a0.pptx"])
    assert abs(prs.slide_width - Mm(841)) < Emu(36000) and abs(prs.slide_height - Mm(1189)) < Emu(36000)
    assert master_fill(prs) == "f2f3ef"
