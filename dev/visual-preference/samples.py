"""Render review samples of every surface from the built files: a web page in both themes, figures in both themes,
a CV page, three social previews and a slide. Output goes to dev/visual-preference/build/samples/ (not committed).

    python dev/visual-preference/samples.py --fonts path/to/@fontsource

The brand faces are served by Google Fonts. A machine that cannot reach Google Fonts passes --fonts, the folder of
the @fontsource npm packages, and the samples load the faces from there instead.
"""
import argparse
import base64
import json
import shutil
import subprocess
import sys
from pathlib import Path

import build

HERE = Path(__file__).resolve().parent
OUT = HERE / "build" / "samples"
FACES = [("albert-sans", "Albert Sans", (400, 500, 600)), ("ibm-plex-mono", "IBM Plex Mono", (400, 500)),
         ("source-serif-4", "Source Serif 4", (400, 600))]


def local_faces_css(fonts: Path | None) -> str:
    if fonts is None:
        return f'@import url("{build.FONTS_URL}");'
    css = []
    for slug, family, weights in FACES:
        for w in weights:
            f = fonts / slug / "files" / f"{slug}-latin-{w}-normal.woff2"
            b = base64.b64encode(f.read_bytes()).decode()
            css.append(f"@font-face{{font-family:'{family}';font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2');}}")
    return "".join(css)


def install_ttfs(fonts: Path, dest: Path) -> list[Path]:
    """Convert the local faces to TTF for matplotlib and XeLaTeX."""
    from fontTools.ttLib import TTFont
    dest.mkdir(parents=True, exist_ok=True)
    made = []
    for slug, family, weights in FACES:
        for w in weights:
            f = TTFont(fonts / slug / "files" / f"{slug}-latin-{w}-normal.woff2")
            f.flavor = None
            p = dest / f"{slug}-{w}.ttf"
            f.save(p)
            made.append(p)
    return made


PAGE = """<!DOCTYPE html><html data-theme="@THEME@"><head><meta charset="utf-8"><style>@FACES@</style>
<style>@TOKENS@</style><style>
body { margin: 0; background: var(--ground); color: var(--ink); font-family: var(--font-sans); }
.page { max-width: var(--page); margin: 0 auto; padding: var(--space-12) var(--space-16); }
header { display: flex; align-items: center; justify-content: space-between; padding-bottom: var(--space-4); border-bottom: 1px solid var(--rule); }
header img { height: 22px; }
nav { display: flex; gap: var(--space-6); } nav a { color: var(--muted); text-decoration: none; font-size: 14px; }
nav a.on { color: var(--ink); box-shadow: inset 0 -2px 0 var(--lichen); padding-bottom: 6px; }
section { padding: var(--space-12) 0; border-bottom: 1px solid var(--rule); }
.lede { max-width: var(--measure); color: var(--ink); opacity: .9; }
.links a { color: var(--ink); margin-right: var(--space-6); text-underline-offset: 4px; text-decoration-color: var(--muted); }
.links a.primary { text-decoration-color: var(--lichen); text-decoration-thickness: 2px; }
.links a.focus { outline: var(--focus-width) solid var(--lichen); outline-offset: var(--focus-offset); }
.stats { display: flex; gap: var(--space-12); margin-top: var(--space-6); }
.stats b { display: block; font-family: var(--font-mono); font-size: 25px; font-weight: 500; }
.stats span { color: var(--muted); font-size: 14px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-8); align-items: start; }
.panel { background: var(--surface); border: 1px solid var(--rule); padding: var(--space-4) var(--space-6); }
.tabs { display: flex; gap: var(--space-6); border-bottom: 1px solid var(--rule); margin-bottom: var(--space-3); font-size: 14px; }
.tabs span { color: var(--muted); padding-bottom: 8px; } .tabs .on { color: var(--ink); box-shadow: inset 0 -2px 0 var(--lichen); }
table { width: 100%; border-collapse: collapse; margin-bottom: var(--space-4); }
td { padding: 6px 0; border-bottom: 1px solid var(--rule); } td + td { text-align: right; font-family: var(--font-mono); }
.btn { display: inline-block; background: var(--lichen); color: var(--ground); padding: 8px 14px; font-weight: 600; }
.act { margin-left: var(--space-4); color: var(--ink); text-decoration: underline; text-underline-offset: 4px; text-decoration-color: var(--muted); }
.field { border: 1px solid var(--edge); padding: 6px 8px; color: var(--muted); margin-top: var(--space-4); }
.legend { height: 12px; margin: var(--space-2) 0; }
.cap { color: var(--muted); font-size: 14px; }
.float { position: relative; height: 210px; background: linear-gradient(135deg, @MAP@); }
.float .panel { position: absolute; left: 16px; top: 16px; width: 220px; background: var(--raised); box-shadow: var(--float); }
</style></head><body><div class="page">
<header><img src="@WORDMARK@" alt="Yili Yang"><nav><a class="on">Work</a><a>Publications</a><a>CV</a></nav></header>
<section><div class="vp-label" style="color:var(--muted)">AI scientist · geospatial and remote sensing</div>
<div class="vp-display">Yili Yang</div>
<p class="lede vp-body">Machine learning for a changing Earth surface: permafrost, carbon and where people live.</p>
<div class="links"><a class="primary">Selected work</a><a class="focus">Publications (focused)</a><a>CV</a></div></section>
<section class="grid"><div><div class="vp-label" style="color:var(--muted)">Research · Woodwell Climate</div>
<div class="vp-h2">Mapping thaw slumps across the Arctic</div>
<p class="vp-body">A deep-learning system that finds retrogressive thaw slumps in satellite imagery, from training data to an open, citable map.</p>
<div class="stats"><div><b>19,068</b><span>slumps mapped</span></div><div><b>41.6M</b><span>tiles scanned</span></div><div><b>0.94</b><span>PR-AUC</span></div></div></div>
<div class="panel"><div class="tabs"><span class="on">Score</span><span>Rank</span><span>Evidence</span></div>
<table><tr><td>Transport</td><td>0.82</td></tr><tr><td>Green space</td><td>0.64</td></tr><tr><td>Cost of living</td><td>0.41</td></tr></table>
<span class="btn">Show the reasons</span><span class="act">Reset weights</span>
<div class="field">Search a postcode</div></div></section>
<section><div class="float"><div class="panel"><div class="vp-label" style="color:var(--muted)">Thaw probability</div>
<div class="legend" style="background:linear-gradient(90deg, @MAP@)"></div><div class="cap">0 to 1 · source: RTS v2</div></div></div></section>
</div></body></html>"""


def web(theme: str, faces: str, cmaps: dict) -> Path:
    stops = cmaps["maps"]["bamako"]["stops"][::32]
    css = (build.SKILL / "web" / "tokens.css").read_text(encoding="utf-8")
    mark = (build.SKILL / "marks" / f"wordmark-{theme}.svg").read_text(encoding="utf-8").split("\n", 1)[1]
    html = (PAGE.replace("@THEME@", theme).replace("@FACES@", faces).replace("@TOKENS@", css)
            .replace("@MAP@", ", ".join(stops)).replace("@WORDMARK@", "data:image/svg+xml;base64," + base64.b64encode(mark.encode()).decode()))
    path = OUT / f"web-{theme}.html"
    path.write_text(html, encoding="utf-8")
    return path


def figures(ttfs: list[Path]) -> list[Path]:
    script = f"""
import importlib.util, numpy as np, matplotlib
matplotlib.use("Agg")
from matplotlib import font_manager
for f in {[str(p) for p in ttfs]!r}: font_manager.fontManager.addfont(f)
spec = importlib.util.spec_from_file_location("vp", {str(build.SKILL / 'figures' / 'visual_preference.py')!r})
vp = importlib.util.module_from_spec(spec); spec.loader.exec_module(vp)
import matplotlib.pyplot as plt
rng = np.random.default_rng(3); x = np.arange(2010, 2026)
y, xx = np.mgrid[0:1:120j, 0:1.6:200j]
z = np.exp(-((xx-.6)**2+(y-.5)**2)/.08) + .6*np.exp(-((xx-1.2)**2+(y-.3)**2)/.03)
d = np.exp(-((xx-.4)**2+(y-.6)**2)/.05) - np.exp(-((xx-1.1)**2+(y-.4)**2)/.06)
for theme in ("light", "dark"):
    vp.use(theme)
    fig, axs = plt.subplots(1, 3, figsize=(13, 3.6), gridspec_kw={{"width_ratios": [1.3, 1, 1]}})
    for k in range(6):
        axs[0].plot(x, np.cumsum(rng.normal(.3, 1, len(x))) + k * 2.2, label=f"Site {{k+1}}")
    axs[0].set_title("Active-layer thickness by site"); axs[0].set_ylabel("Thickness (cm)"); axs[0].legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
    vp.mono_ticks(axs[0])
    im = axs[1].imshow(z, cmap="vp.bamako", origin="lower"); axs[1].set_title("Vegetation index (bamako)")
    dv = "vp.lisbon" if theme == "dark" else "vp.broc"
    axs[2].imshow(d, cmap=dv, vmin=-1, vmax=1, origin="lower"); axs[2].set_title(f"Change ({{dv[3:]}})")
    for a in axs[1:]: a.set_xticks([]); a.set_yticks([]); a.grid(False)
    fig.tight_layout(); fig.savefig({str(OUT)!r} + f"/figure-{{theme}}.png", dpi=150)
"""
    subprocess.run([sys.executable, "-c", script], check=True)
    return [OUT / "figure-light.png", OUT / "figure-dark.png"]


CV = r"""\documentclass[10pt]{article}
\usepackage[margin=18mm]{geometry}
\usepackage{visual-preference}
\pagestyle{empty}
\begin{document}
{\Huge\bfseries Yili Yang}\vpstop\par\smallskip
\vplabel{AI scientist \textperiodcentered{} geospatial and remote sensing}\par
\vprule
\section{Experience}
\textbf{Research scientist}, Woodwell Climate Research Center \hfill \vpnum{2022}\textendash\vpnum{2026}\par
Led pan-Arctic mapping of retrogressive thaw slumps: \vpnum{19,068} slumps mapped from \vpnum{41.6M} tiles, PR-AUC \vpnum{0.94}.
\section{Education}
\textbf{PhD, Petrophysics}, University of Edinburgh\par
\end{document}
"""


def cv(ttfs: list[Path]) -> Path | None:
    if not shutil.which("xelatex"):
        return None
    work = OUT / "cv"
    work.mkdir(exist_ok=True)
    shutil.copy(build.SKILL / "latex" / "visual-preference.sty", work)
    (work / "cv.tex").write_text(CV, encoding="utf-8")
    fontdir = Path.home() / ".fonts"
    fontdir.mkdir(exist_ok=True)
    for t in ttfs:
        shutil.copy(t, fontdir)
    subprocess.run(["fc-cache", "-f"], capture_output=True)
    subprocess.run(["xelatex", "-interaction=nonstopmode", "cv.tex"], cwd=work, capture_output=True, check=True)
    subprocess.run(["pdftoppm", "-png", "-r", "110", "-singlefile", "cv.pdf", str(OUT / "cv")], cwd=work, check=True)
    return OUT / "cv.png"


SOCIAL = [("skills", "Ways of thinking, written down for Claude", "lichen", "yi-li-yang/skills", "Claude Code plugin · 9 skills"),
          ("Livability Atlas", "Where should I live? Every area scored by your own weights", "amber", "yi-li-yang/Livability-Atlas", "Web app · London · open data"),
          ("Travel Log", "Flights and overland trips on a night-side globe", "signal", "yi-li-yang/travel-map", "Web app · visualisation")]


def social(faces: str) -> list[Path]:
    tokens, _ = build.load()
    c = build.colours(tokens, "dark")
    template = (build.SKILL / "templates" / "social-preview.html").read_text(encoding="utf-8")
    template = template.replace(f'<link rel="stylesheet" href="{build.FONTS_URL}">', f"<style>{faces}</style>")
    paths = []
    for name, line, accent, repo, kicker in SOCIAL:
        html = (template.replace("{{name}}", name).replace("{{line}}", line).replace("{{accent}}", c[accent])
                .replace("{{repo}}", repo).replace("{{kicker}}", kicker))
        p = OUT / f"social-{repo.split('/')[1]}.html"
        p.write_text(html, encoding="utf-8")
        paths.append(p)
    return paths


def shoot(pages: list[tuple[Path, int, int]]) -> None:
    js = """const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const jobs = %s;
for (const [f, w, h] of jobs) { const p = await b.newPage({ viewport: { width: w, height: h } });
await p.goto('file://' + f); await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: f.replace(/\\.html$/, '.png'), fullPage: true }); await p.close(); }
await b.close(); })();""" % json.dumps([[str(f), w, h] for f, w, h in pages])
    subprocess.run(["node", "-e", js], check=True)


def slide() -> Path | None:
    if not shutil.which("soffice"):
        return None
    import build_pptx
    from pptx import Presentation
    files = build_pptx.build_pptx(OUT / "pptx")
    prs = Presentation(files[0])
    s = prs.slides.add_slide(prs.slide_layouts[0])
    s.shapes.title.text = "Thaw slumps are mapped across the whole Arctic"
    s.placeholders[1].text = "19,068 slumps from 41.6M satellite tiles"
    deck = OUT / "pptx" / "sample.pptx"
    prs.save(deck)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(OUT / "pptx"), str(deck)],
                   capture_output=True, check=True, timeout=180)
    subprocess.run(["pdftoppm", "-png", "-r", "60", "-singlefile", str(OUT / "pptx" / "sample.pdf"), str(OUT / "slide")], check=True)
    return OUT / "slide.png"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", type=Path, help="folder of @fontsource packages, when Google Fonts is out of reach")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    faces = local_faces_css(args.fonts)
    ttfs = install_ttfs(args.fonts, OUT / "ttf") if args.fonts else []
    _, cmaps = build.load()
    pages = [(web(t, faces, cmaps), 1200, 900) for t in ("dark", "light")]
    pages += [(p, 1280, 640) for p in social(faces)]
    shoot(pages)
    figures(ttfs)
    cv(ttfs)
    slide()
    for p in sorted(OUT.glob("*.png")):
        print(p)


if __name__ == "__main__":
    main()
