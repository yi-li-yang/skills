"""The DESIGN.md a project gets: the shape design skills read, with exactly one accent."""
import pytest
import yaml

import build


def front(text):
    return yaml.safe_load(text.split("---\n")[1])


@pytest.mark.parametrize("accent,hex_", [("lichen", "#a3b86c"), ("signal", "#e2652f"), ("amber", "#e0a84a")])
def test_accent_and_shape(accent, hex_):
    fm = front(build.design_md(*build.load(), accent=accent, project="Livability Atlas"))
    assert fm["name"] == "Livability Atlas"
    assert fm["colors"]["accent"] == hex_
    assert {"colors", "typography", "rounded", "spacing"} <= set(fm)
    others = {"lichen", "signal", "amber"} - {accent}
    assert not others & set(fm["colors"]), "a project carries one accent only"


def test_unknown_accent_is_refused():
    with pytest.raises(ValueError):
        build.design_md(*build.load(), accent="teal", project="x")


def test_template_file_is_the_home_accent():
    text = (build.SKILL / "templates" / "DESIGN.md").read_text(encoding="utf-8")
    assert front(text)["colors"]["accent"] == "#a3b86c"
    assert "{{project}}" in text
