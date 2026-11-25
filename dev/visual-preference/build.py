"""Build every generated file of the visual-preference skill from its two sources, tokens.json and colormaps.json.

    python dev/visual-preference/build.py            # write the files that changed
    python dev/visual-preference/build.py --check    # write nothing; exit 1 and name each stale file

A generated file is never edited by hand: its first line says so and names this script.
"""
import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SKILL = REPO / "plugins" / "yili-skills" / "skills" / "visual-preference"
SKILL_PATH = "plugins/yili-skills/skills/visual-preference"
FONTS_URL = ("https://fonts.googleapis.com/css2?family=Albert+Sans:wght@400;500;600"
             "&family=IBM+Plex+Mono:wght@400;500&family=Source+Serif+4:opsz,wght@8..60,600"
             "&family=Noto+Sans+SC:wght@400;500&display=swap")
OTHER_FAMILIES = ("spacing", "radius", "duration", "easing", "layout")


def load(root: Path = SKILL) -> tuple[dict, dict]:
    tokens = json.loads((root / "tokens.json").read_text(encoding="utf-8"))
    cmaps = json.loads((root / "colormaps.json").read_text(encoding="utf-8"))
    return tokens, cmaps


def header(tokens: dict, start: str, end: str = "") -> str:
    line = f"generated from tokens.json by dev/visual-preference/build.py · visual-preference {tokens['meta']['version']} · do not edit"
    return f"{start} {line}{(' ' + end) if end else ''}\n"


def cdn_url(tag: str, path: str) -> str:
    return f"https://cdn.jsdelivr.net/gh/yi-li-yang/skills@{tag}/{SKILL_PATH}/{path}"


def colours(tokens: dict, theme: str) -> dict[str, str]:
    return {t["name"]: t["value"][theme] for t in tokens["color"]["tokens"]}


def shadows(tokens: dict, theme: str) -> dict[str, str]:
    return {t["name"]: t["value"][theme] for t in tokens["shadow"]["tokens"]}


def plain(tokens: dict) -> dict[str, str]:
    return {t["name"]: t["value"] for f in OTHER_FAMILIES for t in tokens[f]["tokens"]}


def styles(tokens: dict):
    for group in tokens["type"]["groups"]:
        for s in group["styles"]:
            yield s.get("family", group["family"]), s


# ---------------------------------------------------------------------------------------------- web

def tokens_css(tokens: dict) -> str:
    def block(selector: str, theme: str, indent: str = "") -> str:
        lines = [f"{indent}{selector} {{", f"{indent}  color-scheme: {theme};"]
        lines += [f"{indent}  --{k}: {v};" for k, v in colours(tokens, theme).items()]
        lines += [f"{indent}  --{k}: {v};" for k, v in shadows(tokens, theme).items()]
        return "\n".join(lines + [f"{indent}}}"])

    fams = tokens["type"]["families"]
    root = [":root {"] + [f"  --{k}: {v};" for k, v in plain(tokens).items()]
    root += [f"  --font-{k}: {v};" for k, v in fams.items()]
    root += ["}"]
    classes = []
    for family, s in styles(tokens):
        decl = [f"font-family: var(--font-{family})", f"font-size: {s['fontSize']}", f"line-height: {s['lineHeight']}",
                f"font-weight: {s['fontWeight']}"]
        if "letterSpacing" in s:
            decl.append(f"letter-spacing: {s['letterSpacing']}")
        if s["name"] == "label":
            decl.append("text-transform: uppercase")
        if family == "mono":
            decl.append("font-variant-numeric: tabular-nums")
        classes.append(f".vp-{s['name']} {{ {'; '.join(decl)}; }}")
    parts = [
        header(tokens, "/*", "*/").rstrip(),
        "/* Load fonts.css (or the Google Fonts link inside it) before this file. Dark is home; light follows the",
        "   system setting, and data-theme=\"dark\" or \"light\" on <html> forces either. */",
        block(':root, [data-theme="dark"]', "dark"),
        block('[data-theme="light"]', "light"),
        "@media (prefers-color-scheme: light) {\n" + block(':root:not([data-theme="dark"])', "light", "  ") + "\n}",
        "\n".join(root),
        "@media (prefers-reduced-motion: reduce) {\n  :root { --fast: 0ms; --panel: 0ms; }\n}",
        "\n".join(classes),
    ]
    return "\n\n".join(parts) + "\n"


def fonts_css(tokens: dict) -> str:
    return header(tokens, "/*", "*/") + f'@import url("{FONTS_URL}");\n'


def tailwind_v4(tokens: dict) -> str:
    lines = [header(tokens, "/*", "*/").rstrip(),
             "/* Tailwind 4: import after tailwindcss and load tokens.css; utilities follow the active theme. */",
             "@theme inline {"]
    lines += [f"  --color-{k}: var(--{k});" for k in colours(tokens, "dark")]
    lines += [f"  --font-{k}: {v};" for k, v in tokens["type"]["families"].items()]   # literal: same name as tokens.css
    lines += [f"  --spacing-{t['name'].removeprefix('space-')}: var(--{t['name']});" for t in tokens["spacing"]["tokens"]]
    lines += ["  --radius-none: 0;", "  --radius-dot: 9999px;", "  --shadow-float: var(--float);",
              "  --ease-out: var(--out);", "  --container-measure: var(--measure);", "  --container-page: var(--page);", "}"]
    return "\n".join(lines) + "\n"


def tailwind_v3(tokens: dict) -> str:
    extend = {
        "colors": {k: f"var(--{k})" for k in colours(tokens, "dark")},
        "fontFamily": {k: [v] for k, v in tokens["type"]["families"].items()},
        "spacing": {t["name"].removeprefix("space-"): f"var(--{t['name']})" for t in tokens["spacing"]["tokens"]},
        "borderRadius": {"none": "0", "dot": "var(--radius-dot)"},
        "boxShadow": {"float": "var(--float)"},
        "transitionDuration": {"fast": "var(--fast)", "panel": "var(--panel)"},
        "transitionTimingFunction": {"out": "var(--out)"},
        "maxWidth": {"measure": "var(--measure)", "page": "var(--page)"},
    }
    body = json.dumps({"theme": {"extend": extend}}, indent=2)
    return header(tokens, "//") + "// Tailwind 3 preset: presets: [require('./tailwind-v3.cjs')], and load tokens.css.\nmodule.exports = " + body + ";\n"


def colormaps_js(tokens: dict, cmaps: dict) -> str:
    body = {name: {"kind": m["kind"], "use": m["use"], "stops": m["stops"]} for name, m in cmaps["maps"].items()}
    return (header(tokens, "//") + f"// {cmaps['credit']}\n"
            + "export const colormaps = " + json.dumps(body) + ";\n"
            + "export function colormap(name, t) {\n  const s = colormaps[name].stops;\n"
            + "  return s[Math.max(0, Math.min(s.length - 1, Math.round(t * (s.length - 1))))];\n}\n")



# ------------------------------------------------------------------------------------------- figures

EARTH6 = ["data-sky", "data-rust", "data-spruce", "data-sand", "data-dusk", "data-ochre"]
EARTH8 = ["data-glacier", "data-rust", "data-spruce", "data-sand", "data-dusk", "data-rose", "data-olive", "data-sky"]
ACCENTS = ("lichen", "signal", "amber")


def figure_rc(tokens: dict, theme: str) -> dict:
    """matplotlib settings for one theme. Papers are light and print on white, so the light figure ground is white."""
    c = colours(tokens, theme)
    ground = c["raised"] if theme == "light" else c["ground"]
    cycle = ", ".join(f"'{c[n].lstrip('#')}'" for n in EARTH6)
    return {
        "figure.facecolor": ground, "axes.facecolor": ground, "savefig.facecolor": ground, "savefig.dpi": 300,
        "text.color": c["ink"], "axes.labelcolor": c["ink"], "axes.titlecolor": c["ink"],
        "xtick.color": c["muted"], "ytick.color": c["muted"], "axes.edgecolor": c["muted"],
        "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "axes.grid.axis": "y",
        "grid.color": c["rule"], "grid.linewidth": 0.6, "axes.axisbelow": True,
        "axes.prop_cycle": f"cycler('color', [{cycle}])",
        "font.family": "sans-serif", "font.sans-serif": "Albert Sans, DejaVu Sans",
        "font.monospace": "IBM Plex Mono, DejaVu Sans Mono", "font.size": 10,
        "axes.titlesize": 11, "axes.titleweight": 600, "axes.titlelocation": "left", "axes.labelsize": 10,
        "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 9, "legend.frameon": False,
        "lines.linewidth": 1.75, "xtick.major.size": 0, "ytick.major.size": 0, "image.cmap": "vp.bamako",
    }


def mplstyle(tokens: dict, theme: str) -> str:
    rc = figure_rc(tokens, theme)
    rc = {k: (str(v).lstrip("#") if isinstance(v, str) and v.startswith("#") else v) for k, v in rc.items()}
    rc.pop("image.cmap")   # a style file cannot register colour maps; visual_preference.use() does
    lines = [f"{k}: {str(v).lower() if isinstance(v, bool) else v}" for k, v in rc.items()]
    return header(tokens, "#") + f"# {theme} theme; plt.style.use(this file). For the colour maps, use visual_preference.use().\n" + "\n".join(lines) + "\n"


def figure_module(tokens: dict, cmaps: dict) -> str:
    rc = {t: figure_rc(tokens, t) for t in ("dark", "light")}
    for t in rc:
        rc[t]["axes.prop_cycle"] = [colours(tokens, t)[n] for n in EARTH6]
    data = {
        "RC": rc,
        "GROUPS": {t: [colours(tokens, t)[n] for n in EARTH6] for t in ("dark", "light")},
        "GROUPS8": {t: [colours(tokens, t)[n] for n in EARTH8] for t in ("dark", "light")},
        "ACCENTS": {t: {a: colours(tokens, t)[a] for a in ACCENTS} for t in ("dark", "light")},
        "COLORMAPS": {n: m["stops"] for n, m in cmaps["maps"].items()},
    }
    body = "\n".join(f"{k} = {v!r}" for k, v in data.items())
    return header(tokens, "#") + FIGURE_MODULE.replace("@CREDIT@", cmaps["credit"]).replace("@DATA@", body)


FIGURE_MODULE = '''"""Yili Yang's figure style. Copy this file into a project, then:

    import visual_preference as vp
    vp.use("light")          # "light" for papers and email, "dark" for the web and slides
    plt.plot(...)            # lines take the Earth 6 group colours in order
    colors = vp.groups(8, "light")   # the group colours for n groups (up to 8) in one theme
    plt.imshow(z, cmap="vp.bamako")

Colour maps: @CREDIT@
"""
import warnings

import matplotlib
from cycler import cycler
from matplotlib import font_manager
from matplotlib.colors import ListedColormap

@DATA@

_warned = False


def _register() -> None:
    for name, stops in COLORMAPS.items():
        if f"vp.{name}" not in matplotlib.colormaps:
            matplotlib.colormaps.register(ListedColormap(stops, name=f"vp.{name}"))
            matplotlib.colormaps.register(ListedColormap(stops[::-1], name=f"vp.{name}_r"))


def _has(family: str) -> bool:
    return any(f.name == family for f in font_manager.fontManager.ttflist)


def use(theme: str = "light") -> None:
    """Apply the style for "light" or "dark" and register the colour maps as vp.<name>."""
    global _warned
    if theme not in RC:
        raise ValueError(f"theme must be 'light' or 'dark', not {theme!r}")
    _register()
    rc = dict(RC[theme])
    rc["axes.prop_cycle"] = cycler(color=rc["axes.prop_cycle"])
    rc["font.sans-serif"] = [f.strip() for f in rc["font.sans-serif"].split(",")]
    rc["font.monospace"] = [f.strip() for f in rc["font.monospace"].split(",")]
    if not _has("Albert Sans"):
        rc["font.sans-serif"] = ["DejaVu Sans"]
        rc["axes.titleweight"] = "bold"   # DejaVu Sans has no 600
        if not _warned:
            warnings.warn("Albert Sans is not installed; figures use DejaVu Sans. Install it from Google Fonts.",
                          stacklevel=2)
            _warned = True
    if not _has("IBM Plex Mono"):
        rc["font.monospace"] = ["DejaVu Sans Mono"]
    matplotlib.rcParams.update(rc)


def groups(n: int, theme: str = "light") -> list:
    """The colours for n groups: Earth 6 for up to six, Earth 8 for seven or eight. More than eight cannot be told
    apart by colour; label them or show fewer."""
    if theme not in RC:
        raise ValueError(f"theme must be 'light' or 'dark', not {theme!r}")
    if not 1 <= n <= 8:
        raise ValueError(f"{n} groups: colour can separate at most 8")
    return (GROUPS if n <= 6 else GROUPS8)[theme][:n]


def mono_ticks(ax) -> None:
    """Set the tick numbers of one axes in the monospace face, as the system sets every number."""
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_family("monospace")
'''


# --------------------------------------------------------------------------------------------- latex

def latex_sty(tokens: dict) -> str:
    """A LaTeX package: brand faces under XeTeX or LuaTeX (with open fallbacks), standard faces under pdfTeX."""
    light = colours(tokens, "light")
    defs = "\n".join(f"\\definecolor{{vp{k.replace('-', '')}}}{{HTML}}{{{v.lstrip('#').upper()}}}" for k, v in light.items())
    return header(tokens, "%") + r"""% Paper documents: CV, letters, papers. \usepackage{visual-preference}
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{visual-preference}[@VERSION@ Yili Yang's document style]
\RequirePackage{iftex}
\RequirePackage{xcolor}
\RequirePackage{titlesec}
@COLOURS@
\iftutex
  % The fallbacks load by file name, so they work where TeX's own fonts are not registered with the system.
  \RequirePackage{fontspec}
  \IfFontExistsTF{Albert Sans}{\setmainfont{Albert Sans}[BoldFont={* SemiBold}]}{\setmainfont{texgyreheros}[Extension=.otf, UprightFont=*-regular, BoldFont=*-bold, ItalicFont=*-italic, BoldItalicFont=*-bolditalic]}
  \IfFontExistsTF{Source Serif 4}{\newfontfamily\vpserif{Source Serif 4}[BoldFont={* SemiBold}]}{\newfontfamily\vpserif{texgyretermes}[Extension=.otf, UprightFont=*-regular, BoldFont=*-bold, ItalicFont=*-italic, BoldItalicFont=*-bolditalic]}
  \IfFontExistsTF{IBM Plex Mono}{\setmonofont{IBM Plex Mono}}{\setmonofont{lmmono10-regular.otf}}
  \newcommand{\vplabel}[1]{{\addfontfeatures{LetterSpace=10}\footnotesize\MakeUppercase{#1}}}
\else
  \RequirePackage[T1]{fontenc}
  \RequirePackage{lmodern}
  \RequirePackage[scaled=0.92]{helvet}
  \renewcommand{\familydefault}{\sfdefault}
  \newcommand{\vpserif}{\rmfamily}
  \newcommand{\vplabel}[1]{{\footnotesize\MakeUppercase{#1}}}
\fi
\newcommand{\vpnum}[1]{{\ttfamily #1}}
\newcommand{\vprule}{\par\noindent{\color{vplichen}\rule{\linewidth}{0.4pt}}\par}
\newcommand{\vpstop}{{\color{vplichen}\rule{0.22em}{0.22em}}}
\titleformat{\section}{\vpserif\Large\bfseries\color{vpink}}{}{0pt}{}
\titleformat{\subsection}{\vpserif\large\bfseries\color{vpink}}{}{0pt}{}
\AtBeginDocument{\color{vpink}}
\endinput
""".replace("@VERSION@", tokens["meta"]["version"]).replace("@COLOURS@", defs)



# --------------------------------------------------------------------------------------------- marks

GLYPHS = Path(__file__).resolve().parent / "glyphs.json"


def stop_geometry(advance: float, size: float) -> tuple[float, float, float]:
    """The square full stop after a word: side 0.22 of the type size, on the baseline, 0.1 of the size after it."""
    side = 0.22 * size
    return advance + 0.1 * size, -side, side


def svg(tokens: dict, view_box: str, body: str) -> str:
    return header(tokens, "<!--", "-->") + f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}">{body}</svg>\n'


def wordmark_svg(tokens: dict, theme: str) -> str:
    g = json.loads(GLYPHS.read_text(encoding="utf-8"))
    c = colours(tokens, theme)
    x, y, side = stop_geometry(g["advance"], g["unitsPerEm"])
    width = round(x + side)
    body = (f'<path fill="{c["ink"]}" d="{g["path"]}"/>'
            f'<rect x="{x:g}" y="{y:g}" width="{side:g}" height="{side:g}" fill="{c["lichen"]}"/>')
    return svg(tokens, f"0 -800 {width} 1100", body)


def mark_svg(tokens: dict, accent: str) -> str:
    return svg(tokens, "0 0 64 64", f'<rect width="64" height="64" fill="{colours(tokens, "dark")[accent]}"/>')


def favicon_svg(tokens: dict) -> str:
    c = colours(tokens, "dark")
    return svg(tokens, "0 0 64 64", f'<rect width="64" height="64" fill="{c["ground"]}"/>'
                                    f'<rect x="8" y="8" width="48" height="48" fill="{c["lichen"]}"/>')


def social_preview(tokens: dict) -> str:
    c = colours(tokens, "dark")
    return header(tokens, "<!--", "-->") + f"""<!-- 1280 x 640 social preview. Fill the slots, render at 1280 x 640, save as PNG for GitHub. -->
<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<link rel="stylesheet" href="{FONTS_URL}">
<style>
  html, body {{ margin: 0; }}
  .sp {{ width: 1280px; height: 640px; box-sizing: border-box; position: relative; padding: 88px 96px;
        background: {c["ground"]}; color: {c["ink"]}; font-family: "Albert Sans", system-ui, sans-serif; }}
  .kicker {{ font-size: 22px; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: {c["muted"]}; }}
  .name {{ font-size: 104px; font-weight: 600; letter-spacing: -0.02em; line-height: 1.05; margin-top: 26px; }}
  .stop {{ display: inline-block; width: 0.22em; height: 0.22em; margin-left: 0.1em; background: {{{{accent}}}}; }}
  .line {{ font-size: 34px; line-height: 1.3; margin-top: 22px; max-width: 960px; color: {c["ink"]}; opacity: 0.85; }}
  .foot {{ position: absolute; left: 96px; right: 96px; bottom: 72px; padding-top: 24px; border-top: 1px solid {c["rule"]};
          display: flex; justify-content: space-between; align-items: baseline; }}
  .who {{ font-size: 26px; font-weight: 600; }}
  .who .stop {{ background: {c["lichen"]}; }}
  .repo {{ font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 24px; color: {c["muted"]}; }}
</style></head>
<body><div class="sp">
  <div class="kicker">{{{{kicker}}}}</div>
  <div class="name">{{{{name}}}}<span class="stop"></span></div>
  <div class="line">{{{{line}}}}</div>
  <div class="foot"><span class="who">Yili Yang<span class="stop"></span></span><span class="repo">{{{{repo}}}}</span></div>
</div></body></html>
"""



# ------------------------------------------------------------------------------------------ DESIGN.md

def design_md(tokens: dict, cmaps: dict, accent: str, project: str) -> str:
    """A project's DESIGN.md, in the shape design skills read: front matter of values, then the rules in prose.
    A project carries exactly one accent."""
    if accent not in ACCENTS:
        raise ValueError(f"accent must be one of {', '.join(ACCENTS)}, not {accent!r}")
    dark, light = colours(tokens, "dark"), colours(tokens, "light")
    fams = tokens["type"]["families"]
    neutral = ["ground", "surface", "raised", "rule", "edge", "muted", "ink"]
    data = EARTH6 + [n for n in EARTH8 if n not in EARTH6]
    q = json.dumps   # a JSON string is a valid YAML scalar
    description = f"Built on Yili Yang's visual system {tokens['meta']['version']}. Dark is home; one accent: {accent}."
    lines = ["---", header(tokens, "#").rstrip(),
             "# Copy into the project as DESIGN.md and replace {{project}} with its name; change nothing else.",
             f"name: {q(project)}",
             f"description: {q(description)}",
             "colors:"]
    lines += [f"  {n}: {q(dark[n])}" for n in neutral] + [f"  accent: {q(dark[accent])}"]
    lines += [f"  {n}: {q(dark[n])}" for n in data]
    lines += ["colors-light:"] + [f"  {n}: {q(light[n])}" for n in neutral] + [f"  accent: {q(light[accent])}"]
    lines += [f"  {n}: {q(light[n])}" for n in data]
    lines += ["typography:"]
    for family, st in styles(tokens):
        lines += [f"  {st['name']}:", f"    fontFamily: {q(fams[family])}", f"    fontSize: {q(st['fontSize'])}",
                  f"    fontWeight: {st['fontWeight']}", f"    lineHeight: {st['lineHeight']}"]
        if "letterSpacing" in st:
            lines.append(f"    letterSpacing: {q(st['letterSpacing'])}")
    lines += ["rounded:", '  none: "0"', '  dot: "9999px"', "spacing:"]
    lines += [f"  {t['name']}: {q(t['value'])}" for t in tokens["spacing"]["tokens"]]
    lines += ["---", "", f"# Design System: {project}", "",
              f"This project uses Yili Yang's visual system, version {tokens['meta']['version']}. The values above come from it; "
              "change them there, not here. Its manual explains each choice.", "",
              f"**The accent is {accent}.** It marks the one focus or action in a view: the filled button, the selected tab, "
              "the focus ring, the full stop after the project's name. It is never used for data and never next to another accent.", "",
              "## Principles, in order", "",
              "1. **Readable by everyone.** Text at WCAG AA contrast in both themes; colour is never the only cue.",
              "2. **The work leads.** The interface stays in the stone neutrals; maps, images and data carry the colour.",
              "3. **Colour means something.** The accent marks focus or action; the data colours mark data.",
              "4. **Editorial clarity.** Hierarchy from size, weight and space; text aligned left; units and sources visible.",
              "5. **Built like an instrument.** Square corners, hairline rules, monospace numbers, matte surfaces: no glow, glass or soft shadow.", ""]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------------------------- build

def outputs(tokens: dict, cmaps: dict) -> dict[str, str]:
    return {
        "web/tokens.css": tokens_css(tokens),
        "web/fonts.css": fonts_css(tokens),
        "web/tailwind-v4.css": tailwind_v4(tokens),
        "web/tailwind-v3.cjs": tailwind_v3(tokens),
        "web/colormaps.js": colormaps_js(tokens, cmaps),
        "figures/visual-preference-dark.mplstyle": mplstyle(tokens, "dark"),
        "figures/visual-preference-light.mplstyle": mplstyle(tokens, "light"),
        "figures/visual_preference.py": figure_module(tokens, cmaps),
        "latex/visual-preference.sty": latex_sty(tokens),
        **{f"marks/mark-{a}.svg": mark_svg(tokens, a) for a in ACCENTS},
        "marks/favicon.svg": favicon_svg(tokens),
        "marks/wordmark-dark.svg": wordmark_svg(tokens, "dark"),
        "marks/wordmark-light.svg": wordmark_svg(tokens, "light"),
        "templates/social-preview.html": social_preview(tokens),
        **{f"templates/DESIGN-{a}.md": design_md(tokens, cmaps, a, "{{project}}") for a in ACCENTS},
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="write nothing; exit 1 if a generated file is stale")
    ap.add_argument("--root", type=Path, default=SKILL, help="the skill folder (for tests)")
    args = ap.parse_args(argv)
    stale = []
    for rel, text in outputs(*load(args.root)).items():
        path = args.root / rel
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == text:
            continue
        stale.append(rel)
        if not args.check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
    if args.check and stale:
        print("stale, run dev/visual-preference/build.py: " + ", ".join(stale), file=sys.stderr)
        return 1
    if stale and not args.check:
        print("wrote " + ", ".join(stale))
    return 0


if __name__ == "__main__":
    sys.exit(main())
