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


def rescale(prs, width, height, type_scale: float = 1.0) -> None:
    """Resize the page, and move and resize every master and layout shape with it. The default template is 4:3
    (254 x 190.5 mm); without this its placeholders stay in a corner of a larger page. type_scale also scales the
    master's text sizes, for a poster."""
    sx, sy = width / prs.slide_width, height / prs.slide_height
    prs.slide_width, prs.slide_height = width, height
    for owner in [prs.slide_master] + list(prs.slide_layouts):
        for shape in owner.shapes:
            # A layout placeholder without its own position inherits the master's, which is already rescaled.
            if shape._element.find(".//" + qn("a:xfrm")) is None or shape.width is None:
                continue
            shape.left, shape.top = int(shape.left * sx), int(shape.top * sy)
            shape.width, shape.height = int(shape.width * sx), int(shape.height * sy)
    if type_scale != 1.0:
        for owner in [prs.slide_master] + list(prs.slide_layouts):
            for node in owner.element.iter():
                if node.get("sz") and node.tag.endswith(("defRPr", "rPr", "endParaRPr")):
                    node.set("sz", str(int(int(node.get("sz")) * type_scale)))


def share_left_edge(prs) -> None:
    """On the title layout, the subtitle starts where the title starts."""
    for layout in prs.slide_layouts:
        phs = {ph.placeholder_format.idx: ph for ph in layout.placeholders}
        if layout.name == "Title" and 0 in phs and 1 in phs:
            width = phs[0].width
            phs[1].left, phs[1].width = phs[0].left, width


def align_left(prs) -> None:
    """Principle 4: text is aligned left. The default template centres some placeholders; make them left."""
    for element in [prs.slide_master.element] + [layout.element for layout in prs.slide_layouts]:
        for node in element.iter():
            if node.get("algn") == "ctr":
                node.set("algn", "l")


def colour_text(prs, ink: str) -> None:
    for shape in prs.slide_master.placeholders:
        for p in shape.text_frame.paragraphs:
            p.font.color.rgb = rgb(ink)


def add_footer(prs, c: dict[str, str], stop: str, scale: float = 1.0) -> None:
    """Name and stop at the bottom left of the master. Masters cannot add shapes directly, so the shapes are made on
    a scratch slide and moved."""
    scratch = prs.slides.add_slide(prs.slide_layouts[0])
    w, h = prs.slide_width, prs.slide_height
    box = scratch.shapes.add_textbox(int(Mm(12) * scale), h - int(Mm(14) * scale), int(Mm(60) * scale), int(Mm(8) * scale))
    box.name = "name"
    run = box.text_frame.paragraphs[0].add_run()
    run.text = "Yili Yang"
    run.font.size, run.font.bold, run.font.color.rgb = Pt(12 * scale), True, rgb(c["ink"])
    # The stop: 0.22 of the type size, on the baseline, 0.1 of the size after the name.
    side = Pt(12 * scale * 0.22)
    square = scratch.shapes.add_shape(MSO_SHAPE.RECTANGLE, int(Mm(36.5) * scale), h - int(Mm(9.6) * scale), side, side)
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
            ph.left, ph.top = w - int(Mm(32) * scale), h - int(Mm(14) * scale)
            ph.width, ph.height = int(Mm(20) * scale), int(Mm(8) * scale)
            for p in ph.text_frame.paragraphs:
                p.font.name, p.font.size, p.font.color.rgb = "IBM Plex Mono", Pt(10 * scale), rgb(c["muted"])


def slides(theme: str) -> Presentation:
    tokens, _ = build.load()
    c = build.colours(tokens, theme)
    prs = Presentation()
    set_theme(prs, c)
    set_background(prs.slide_master.element, c["ground"])
    keep_layouts(prs)
    rescale(prs, Mm(338.67), Mm(190.5))                           # 16:9
    colour_text(prs, c["ink"])
    add_footer(prs, c, c["lichen"])
    share_left_edge(prs)
    align_left(prs)
    return prs


def poster() -> Presentation:
    tokens, _ = build.load()
    c = build.colours(tokens, "light")
    prs = Presentation()
    set_theme(prs, c)
    set_background(prs.slide_master.element, c["ground"])
    keep_layouts(prs)
    scale = 841 / 254                                             # the same grid, at A0 width
    rescale(prs, Mm(841), Mm(1189), type_scale=scale)             # A0 portrait
    colour_text(prs, c["ink"])
    add_footer(prs, c, c["lichen"], scale=scale)
    share_left_edge(prs)
    align_left(prs)
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
