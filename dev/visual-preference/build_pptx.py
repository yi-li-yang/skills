"""Build the slide and poster templates from tokens.json, for a release. They are attached to the GitHub release,
never committed.

    python dev/visual-preference/build_pptx.py        # writes dev/visual-preference/build/*.pptx
"""
import copy
import re
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.util import Mm, Pt

import build

OUT = Path(__file__).resolve().parent / "build"
THEME_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme"
KEEP = {"Title Slide": "Title", "Title and Content": "Title and figure", "Section Header": "Section"}


def rgb(hex_colour: str) -> RGBColor:
    return RGBColor.from_string(hex_colour.lstrip("#").upper())


def set_background(element, hex_colour: str) -> None:
    """Give a master or layout a solid background."""
    csld = element.find(qn("p:cSld"))
    old = csld.find(qn("p:bg"))
    if old is not None:
        csld.remove(old)
    bg = csld.makeelement(qn("p:bg"), {})
    pr = bg.makeelement(qn("p:bgPr"), {})
    fill = pr.makeelement(qn("a:solidFill"), {})
    fill.append(fill.makeelement(qn("a:srgbClr"), {"val": hex_colour.lstrip("#").upper()}))
    pr.append(fill)
    pr.append(pr.makeelement(qn("a:effectLst"), {}))
    bg.append(pr)
    csld.insert(0, bg)


def set_theme(prs, c: dict[str, str]) -> None:
    """Theme fonts and colours: every placeholder and new text box inherits them."""
    part = prs.slide_master.part.part_related_by(THEME_REL)
    xml = part.blob.decode("utf-8")
    xml = re.sub(r'(<a:majorFont><a:latin typeface=")[^"]*', r"\1Albert Sans", xml)
    xml = re.sub(r'(<a:minorFont><a:latin typeface=")[^"]*', r"\1Albert Sans", xml)
    slots = {"dk1": c["ink"], "lt1": c["ground"], "dk2": c["muted"], "lt2": c["surface"], "accent1": c["lichen"],
             "accent2": c["data-sky"], "accent3": c["data-rust"], "accent4": c["data-spruce"], "accent5": c["data-sand"],
             "accent6": c["data-dusk"], "hlink": c["lichen"], "folHlink": c["muted"]}
    for slot, value in slots.items():
        xml = re.sub(rf"<a:{slot}>.*?</a:{slot}>", f'<a:{slot}><a:srgbClr val="{value.lstrip("#").upper()}"/></a:{slot}>', xml,
                     flags=re.S)
    part._blob = xml.encode("utf-8")


def keep_layouts(prs) -> None:
    """Keep three layouts, renamed; remove the rest."""
    layouts = prs.slide_layouts
    for layout in list(layouts):
        if layout.name in KEEP:
            layout.name = KEEP[layout.name]
        else:
            layouts.remove(layout)


def colour_text(prs, ink: str) -> None:
    for shape in prs.slide_master.placeholders:
        for p in shape.text_frame.paragraphs:
            p.font.color.rgb = rgb(ink)


def add_footer(prs, c: dict[str, str], stop: str) -> None:
    """Name and stop at the bottom left of the master. Masters cannot add shapes directly, so the shapes are made on
    a scratch slide and moved."""
    scratch = prs.slides.add_slide(prs.slide_layouts[0])
    w, h = prs.slide_width, prs.slide_height
    box = scratch.shapes.add_textbox(Mm(12), h - Mm(14), Mm(60), Mm(8))
    box.name = "name"
    run = box.text_frame.paragraphs[0].add_run()
    run.text = "Yili Yang"
    run.font.size, run.font.bold, run.font.color.rgb = Pt(12), True, rgb(c["ink"])
    square = scratch.shapes.add_shape(MSO_SHAPE.RECTANGLE, Mm(36.5), h - Mm(9.6), Mm(1.2), Mm(1.2))
    square.name = "stop"
    square.fill.solid()
    square.fill.fore_color.rgb = rgb(stop)
    square.line.fill.background()
    tree = prs.slide_master.shapes._spTree
    for shape in (box, square):
        tree.append(copy.deepcopy(shape._element))
    rid = prs.slides._sldIdLst[-1].rId
    prs.part.drop_rel(rid)
    del prs.slides._sldIdLst[-1]
    # Slide number in the monospace face, bottom right.
    for ph in prs.slide_master.placeholders:
        if ph.placeholder_format.type is not None and "SLIDE_NUMBER" in str(ph.placeholder_format.type):
            ph.left, ph.top, ph.width, ph.height = w - Mm(32), h - Mm(14), Mm(20), Mm(8)
            for p in ph.text_frame.paragraphs:
                p.font.name, p.font.size, p.font.color.rgb = "IBM Plex Mono", Pt(10), rgb(c["muted"])


def slides(theme: str) -> Presentation:
    tokens, _ = build.load()
    c = build.colours(tokens, theme)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Mm(338.67), Mm(190.5)   # 16:9
    set_theme(prs, c)
    set_background(prs.slide_master.element, c["ground"])
    keep_layouts(prs)
    colour_text(prs, c["ink"])
    add_footer(prs, c, c["lichen"])
    return prs


def poster() -> Presentation:
    tokens, _ = build.load()
    c = build.colours(tokens, "light")
    prs = Presentation()
    prs.slide_width, prs.slide_height = Mm(841), Mm(1189)          # A0 portrait
    set_theme(prs, c)
    set_background(prs.slide_master.element, c["ground"])
    keep_layouts(prs)
    colour_text(prs, c["ink"])
    add_footer(prs, c, c["lichen"])
    return prs


def build_pptx(out_dir: Path = OUT) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    made = []
    for name, prs in (("slides-dark.pptx", slides("dark")), ("slides-light.pptx", slides("light")),
                      ("poster-a0.pptx", poster())):
        path = out_dir / name
        prs.save(path)
        made.append(path)
    return made


if __name__ == "__main__":
    for p in build_pptx(Path(sys.argv[1]) if len(sys.argv) > 1 else OUT):
        print(p)
