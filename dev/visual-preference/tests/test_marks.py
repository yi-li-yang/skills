"""The marks and the social preview template."""
import re
import xml.etree.ElementTree as ET

import pytest

import build

MARKS = build.SKILL / "marks"
HEX = re.compile(r"#[0-9a-fA-F]{6}")


def svgs():
    return sorted(MARKS.glob("*.svg"))


def test_marks_exist():
    names = {p.name for p in svgs()}
    assert names == {"mark-lichen.svg", "mark-signal.svg", "mark-amber.svg", "favicon.svg",
                     "wordmark-dark.svg", "wordmark-light.svg"}


@pytest.mark.parametrize("path", svgs(), ids=lambda p: p.name)
def test_svg_parses_with_viewbox(path):
    root = ET.fromstring(path.read_text(encoding="utf-8").split("\n", 1)[1])
    assert root.get("viewBox")


@pytest.mark.parametrize("accent,hex_", [("lichen", "#a3b86c"), ("signal", "#e2652f"), ("amber", "#e0a84a")])
def test_mark_is_only_its_accent(accent, hex_):
    text = (MARKS / f"mark-{accent}.svg").read_text(encoding="utf-8")
    assert {h.lower() for h in HEX.findall(text)} == {hex_}


def test_favicon_is_stop_on_stone():
    text = (MARKS / "favicon.svg").read_text(encoding="utf-8")
    assert {h.lower() for h in HEX.findall(text)} == {"#131512", "#a3b86c"}


@pytest.mark.parametrize("theme,ink,stop", [("dark", "#e5e8e1", "#a3b86c"), ("light", "#1a1d18", "#566a26")])
def test_wordmark_is_outlined(theme, ink, stop):
    text = (MARKS / f"wordmark-{theme}.svg").read_text(encoding="utf-8")
    assert "<text" not in text
    assert {h.lower() for h in HEX.findall(text)} == {ink, stop}


def test_stop_proportions():
    """The square's side is 0.22 of the type size, it sits on the baseline, and the gap is 0.1 of the size."""
    size = 100
    x, y, side = build.stop_geometry(advance=500, size=size)
    assert side == pytest.approx(0.22 * size)
    assert x == pytest.approx(500 + 0.1 * size)
    assert y + side == pytest.approx(0)


def test_social_preview_slots():
    text = (build.SKILL / "templates" / "social-preview.html").read_text(encoding="utf-8")
    for slot in ("{{kicker}}", "{{name}}", "{{line}}", "{{repo}}", "{{accent}}"):
        assert slot in text
    assert "fonts.googleapis.com" in text
