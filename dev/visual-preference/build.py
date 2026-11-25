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
    lines += [f"  --font-{k}: var(--font-{k});" for k in tokens["type"]["families"]]
    lines += [f"  --spacing-{t['name'].removeprefix('space-')}: var(--{t['name']});" for t in tokens["spacing"]["tokens"]]
    lines += ["  --radius-none: 0;", "  --radius-dot: var(--radius-dot);", "  --shadow-float: var(--float);",
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


# --------------------------------------------------------------------------------------------- build

def outputs(tokens: dict, cmaps: dict) -> dict[str, str]:
    return {
        "web/tokens.css": tokens_css(tokens),
        "web/fonts.css": fonts_css(tokens),
        "web/tailwind-v4.css": tailwind_v4(tokens),
        "web/tailwind-v3.cjs": tailwind_v3(tokens),
        "web/colormaps.js": colormaps_js(tokens, cmaps),
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
