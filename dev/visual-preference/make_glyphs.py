"""Write glyphs.json: the outlined, kerned shape of "Yili Yang" in Albert Sans SemiBold (600), for the wordmark.

The build draws the wordmark from glyphs.json, so it needs neither the font nor a network. Run this once when the
name or the face changes, and commit the result. Albert Sans is under the SIL Open Font License; a logo drawn from
its outlines is artwork made with the font, which the licence allows.

    python dev/visual-preference/make_glyphs.py path/to/AlbertSans-SemiBold.(ttf|woff2)
"""
import json
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

OUT = Path(__file__).resolve().parent / "glyphs.json"
TEXT = "Yili Yang"


def main(font_path: str) -> None:
    font = TTFont(font_path)
    font.flavor = None
    tmp = Path(OUT.parent / "build")
    tmp.mkdir(exist_ok=True)
    ttf = tmp / "albert-sans-600.ttf"
    font.save(ttf)
    blob = hb.Blob.from_file_path(str(ttf))
    hbfont = hb.Font(hb.Face(blob))
    buf = hb.Buffer()
    buf.add_str(TEXT)
    buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": True})
    glyphset, order = font.getGlyphSet(), font.getGlyphOrder()
    pen, x = SVGPathPen(glyphset), 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        # SVG's y axis points down: flip the glyph about the baseline while placing it.
        glyphset[order[info.codepoint]].draw(TransformPen(pen, (1, 0, 0, -1, x + pos.x_offset, -pos.y_offset)))
        x += pos.x_advance
    upm = font["head"].unitsPerEm
    OUT.write_text(json.dumps({
        "text": TEXT, "font": "Albert Sans SemiBold (600)", "unitsPerEm": upm, "advance": x,
        "capHeight": font["OS/2"].sCapHeight, "descender": font["hhea"].descent, "path": pen.getCommands(),
    }, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT.name}: advance {x} of {upm} units per em")


if __name__ == "__main__":
    main(sys.argv[1])
