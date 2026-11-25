"""The figure style: matplotlib settings, colour maps and the font fallback, from a copy of the figures/ folder."""
import importlib.util
import subprocess
import sys

import pytest

import build

FIGURES = build.SKILL / "figures"
EARTH6_DARK = ["#a9cfe6", "#c4573a", "#4f9a7d", "#d8c48e", "#8a7fb8", "#c9962e"]


@pytest.fixture()
def vp():
    import matplotlib
    matplotlib.use("Agg")
    spec = importlib.util.spec_from_file_location("visual_preference", FIGURES / "visual_preference.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    yield module
    matplotlib.rcdefaults()


def test_use_light_and_dark(vp):
    import matplotlib as mpl
    vp.use("dark")
    assert mpl.rcParams["figure.facecolor"] == "#131512"
    assert mpl.rcParams["axes.spines.top"] is False and mpl.rcParams["axes.spines.right"] is False
    assert [c.lower() for c in mpl.rcParams["axes.prop_cycle"].by_key()["color"]] == EARTH6_DARK
    vp.use("light")
    assert mpl.rcParams["figure.facecolor"] == "#ffffff"
    assert mpl.rcParams["text.color"] == "#1a1d18"


def test_unknown_theme_is_refused(vp):
    with pytest.raises(ValueError):
        vp.use("sepia")


def test_colormaps_registered(vp):
    import matplotlib
    vp.use("light")
    for name in ("bamako", "oslo", "lajolla", "bilbao", "lichen", "lisbon", "broc"):
        assert f"vp.{name}" in matplotlib.colormaps


def test_style_files_load():
    import matplotlib.pyplot as plt
    for theme in ("dark", "light"):
        plt.style.use(str(FIGURES / f"visual-preference-{theme}.mplstyle"))
    import matplotlib
    matplotlib.rcdefaults()


def test_missing_font_falls_back(tmp_path):
    script = f"""
import importlib.util, matplotlib
matplotlib.use("Agg")
spec = importlib.util.spec_from_file_location("vp", {str(FIGURES / 'visual_preference.py')!r})
vp = importlib.util.module_from_spec(spec); spec.loader.exec_module(vp)
vp.use("light")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(); ax.plot([1, 2, 3]); ax.set_title("t")
fig.savefig({str(tmp_path / 'f.png')!r})
"""
    run = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    assert (tmp_path / "f.png").stat().st_size > 0
    assert run.stderr.count("Albert Sans is not installed") == 1
    assert "findfont" not in run.stderr
