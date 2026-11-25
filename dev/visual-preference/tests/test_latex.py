"""The LaTeX style compiles under XeLaTeX (brand fonts or their fallbacks) and under pdfLaTeX (standard fonts)."""
import shutil
import subprocess

import pytest

import build

STY = build.SKILL / "latex" / "visual-preference.sty"
SAMPLE = r"""\documentclass{article}
\usepackage{visual-preference}
\begin{document}
\section{Mapping thaw slumps}
Text in the body face, with a number: \vpnum{19,068} slumps.
\vprule
\end{document}
"""


@pytest.mark.parametrize("engine", ["xelatex", "pdflatex"])
def test_compiles(engine, tmp_path):
    if not shutil.which(engine):
        pytest.skip(f"{engine} is not installed")
    shutil.copy(STY, tmp_path / STY.name)
    (tmp_path / "sample.tex").write_text(SAMPLE, encoding="utf-8")
    run = subprocess.run([engine, "-interaction=nonstopmode", "-halt-on-error", "sample.tex"], cwd=tmp_path,
                         capture_output=True, text=True, timeout=180)
    assert run.returncode == 0, run.stdout[-2000:]
    assert (tmp_path / "sample.pdf").stat().st_size > 0


def test_colours_come_from_tokens():
    text = STY.read_text(encoding="utf-8")
    assert r"\definecolor{vpink}{HTML}{1B1C1A}" in text
    assert r"\definecolor{vplichen}{HTML}{566A26}" in text


def test_xelatex_without_any_system_fonts(tmp_path):
    """A CI image may register no TeX fonts with fontconfig. The fallbacks must still load, by file name."""
    if not shutil.which("xelatex"):
        pytest.skip("xelatex is not installed")
    import glob
    import os
    dejavu = next(iter(glob.glob("/usr/share/fonts/truetype/dejavu")), None)
    if dejavu is None:
        pytest.skip("no DejaVu folder to build a minimal fontconfig")
    conf = tmp_path / "fonts.conf"
    conf.write_text(f'<?xml version="1.0"?><fontconfig><dir>{dejavu}</dir><cachedir>{tmp_path / "fc"}</cachedir></fontconfig>')
    shutil.copy(STY, tmp_path / STY.name)
    (tmp_path / "sample.tex").write_text(SAMPLE, encoding="utf-8")
    env = dict(os.environ, FONTCONFIG_FILE=str(conf), HOME=str(tmp_path))
    run = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "sample.tex"], cwd=tmp_path,
                         capture_output=True, text=True, timeout=180, env=env)
    assert run.returncode == 0, run.stdout[-2000:]
