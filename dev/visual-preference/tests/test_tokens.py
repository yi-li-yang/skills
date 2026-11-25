"""The token source: its shape, the values the design fixed, and the contrast and distinctness they must keep."""
import json
import re
from pathlib import Path

import pytest

from colour import contrast, min_cvd_distance

SKILL = Path(__file__).resolve().parents[3] / "plugins" / "yili-skills" / "skills" / "visual-preference"
NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
EARTH6 = ["data-sky", "data-rust", "data-spruce", "data-sand", "data-dusk", "data-ochre"]
# Seven or eight groups take the whole Earth 8 set (K2), which swaps ochre for glacier: K1 plus rose and olive
# alone measures 5.0, far below the 10.0 an eight-colour set needs.
EARTH8 = ["data-glacier", "data-rust", "data-spruce", "data-sand", "data-dusk", "data-rose", "data-olive", "data-sky"]
ACCENTS = ["lichen", "signal", "amber"]


@pytest.fixture(scope="module")
def tokens():
    return json.loads((SKILL / "tokens.json").read_text(encoding="utf-8"))


def colours(tokens):
    return {t["name"]: t["value"] for t in tokens["color"]["tokens"]}


def families(tokens):
    return {k: v for k, v in tokens.items() if isinstance(v, dict) and "tokens" in v}


def test_shape(tokens):
    assert tokens["color"]["themes"] == [{"id": "dark", "name": "Dark"}, {"id": "light", "name": "Light"}]
    assert set(tokens["type"]) >= {"fonts", "families", "groups"}
    assert "motion" not in tokens
    seen = []
    for family in families(tokens).values():
        assert isinstance(family["tokens"], list)
        for t in family["tokens"]:
            assert NAME.match(t["name"]), t["name"]
            seen.append(t["name"])
    assert len(seen) == len(set(seen)), "a token name is used twice"


def test_spec_values(tokens):
    c = colours(tokens)
    expected = {
        "ground": ("#131512", "#f2f3ef"), "surface": ("#1a1d19", "#e8eae4"), "raised": ("#22261f", "#ffffff"),
        "rule": ("#333832", "#cfd3ca"), "edge": ("#6b7168", "#7f857a"), "muted": ("#9ca29a", "#5b6158"),
        "ink": ("#e5e8e1", "#1a1d18"), "lichen": ("#a3b86c", "#566a26"), "signal": ("#e2652f", "#b0441a"),
        "amber": ("#e0a84a", "#8a5d0c"),
    }
    for name, (dark, light) in expected.items():
        assert c[name] == {"dark": dark, "light": light}, name
    dark_data = {"data-sky": "#a9cfe6", "data-rust": "#c4573a", "data-spruce": "#4f9a7d", "data-sand": "#d8c48e",
                 "data-dusk": "#8a7fb8", "data-ochre": "#c9962e", "data-rose": "#d98ca0", "data-olive": "#b0ac5a",
                 "data-glacier": "#86b2d4"}
    for name, dark in dark_data.items():
        assert c[name]["dark"] == dark, name


@pytest.mark.parametrize("theme", ["dark", "light"])
def test_text_contrast(tokens, theme):
    c = {k: v[theme] for k, v in colours(tokens).items()}
    for ground in ("ground", "surface", "raised"):
        for text in ("ink", "muted"):
            assert contrast(c[text], c[ground]) >= 4.5, (theme, text, ground)
    for accent in ACCENTS:
        for ground in ("ground", "surface"):
            assert contrast(c[accent], c[ground]) >= 4.5, (theme, accent, ground)
    assert contrast(c["edge"], c["ground"]) >= 3.0, theme


@pytest.mark.parametrize("theme", ["dark", "light"])
def test_data_distinct(tokens, theme):
    c = colours(tokens)
    assert min_cvd_distance([c[n][theme] for n in EARTH6]) >= 11.0
    assert min_cvd_distance([c[n][theme] for n in EARTH8]) >= 10.0


def test_light_data_contrast(tokens):
    c = colours(tokens)
    for name in sorted(set(EARTH6 + EARTH8)):
        assert contrast(c[name]["light"], "#f2f3ef") >= 3.0, name


def test_every_token_has_usage(tokens):
    for family in families(tokens).values():
        for t in family["tokens"]:
            assert t.get("usage"), t["name"]
