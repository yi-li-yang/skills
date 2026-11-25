# visual-preference Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `visual-preference` skill to the `yili-skills` plugin: Yili's visual system as one token source, the generated web, figure and LaTeX files, the marks, the templates, a manual and the skill that applies them. Then verify, release and sync the viewer.

**Architecture:** `tokens.json` and `colormaps.json` are the only hand-owned values. `dev/visual-preference/build.py` turns them into every generated file, and `--check` fails when a generated file is stale. Everything installed is small text. The `.pptx` files are built per release and attached to the GitHub release, never committed.

**Tech Stack:** Python 3.11+ (stdlib, `pytest`); build-only dependencies `cmcrameri`, `colorspacious`, `fonttools[woff]`, `python-pptx`, `matplotlib`; `xelatex` and `pdflatex` for the LaTeX test; Playwright (already installed) for sample renders.

**Spec:** `dev/visual-preference/design.md` (copy of `visual-preference-design.md`) and the choice log `dev/visual-preference/decisions.md`.

## Global Constraints

- Installed folder: `plugins/yili-skills/skills/visual-preference/`. Small text files only. No fonts, no images except SVG, no `.pptx`.
- Development material only in `dev/visual-preference/`.
- `python -m pytest dev` stays green, including the existing `dev/tests/test_structure.py`:
  - `name:` equals the folder name
  - description ≤ 1024 characters
  - `**Takes:**` and `**Returns:**` before the first `## `
  - no installed `.md` names another skill (`i-think-like-this`, `interview-me-before-answer`, `updated-domain-expert`, `digest-distill-information`, `research-before-buy`, `wardrobe` in backticks, `write-like-myself`, `talk-standard-tech-eng`)
  - `dev/visual-preference/README.md` exists
  - the versions match
- `tokens.json` uses the Design System list format: every family `{"tokens":[{"name","value","usage"}]}`, plus `color.themes` and the `type` shape. Names match `^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$` and are unique across families. There is no `motion` family; motion lives in `duration` and `easing`.
- Themes: `dark` first (home), `light` second.
- Exact colours: section 8.4 of the spec. Accents: `lichen` (home), `signal`, `amber`. Nothing else may be an accent.
- Type stacks:
  - `sans`: `"Albert Sans", system-ui, sans-serif`
  - `mono`: `"IBM Plex Mono", ui-monospace, monospace`
  - `serif`: `"Source Serif 4", Georgia, serif`
  - `cjk`: `"Noto Sans SC", sans-serif`

  All are served by Google Fonts, so `type.fonts` stays empty.
- Sizes 12/14/16/20/25/31/49 px. Line heights 1.55 for text and 1.15 for headings. Label letter-spacing 0.1em, capitals. Weights 400/500/600 only.
- Spacing 4, 8, 12, 16, 24, 32, 48, 64, 96 px. Radius `0` and `dot` = 9999px. Durations 120ms and 200ms, easing `cubic-bezier(0.2, 0.8, 0.2, 1)`. Focus ring 2px with a 2px offset. Measure 68ch, page 1200px.
- The one shadow, `float`: `0 8px 24px rgba(0,0,0,0.35)` on dark and `0 8px 24px rgba(26,29,24,0.18)` on light. It is for panels over maps or imagery only.
- Release tag `visual-preference-vX.Y.Z`. The first release is `visual-preference-v1.0.0`, with the plugin at `2.7.0`.
- jsDelivr URL pattern: `https://cdn.jsdelivr.net/gh/yi-li-yang/skills@{tag}/plugins/yili-skills/skills/visual-preference/{path}`.
- Every generated file's first line states the source and the version: `generated from tokens.json by dev/visual-preference/build.py · visual-preference {version} · do not edit`, as a comment in that file's syntax.
- Writing in installed files follows the repo's `CLAUDE.md`:
  - plain Simplified Technical English
  - a way of thinking, not rules or checklists
  - no non-English words
  - British spelling
- The skill applies to Yili's own projects only. It does not apply to Woodwell organisation repos or to KIMKIM projects.
- Colour maps are Fabio Crameri's Scientific colour maps. Credit them in `colormaps.json` and in the manual (cite Crameri, F. (2018), Scientific colour maps, Zenodo, doi:10.5281/zenodo.1243862).

## Review Focus

1. **Data colours on a light page.** Earth 6 was checked on the dark ground only, and papers are light. The light variants must reach 3:1 against `#f2f3ef` and stay distinct under colour-vision simulation (min ΔE ≥ 10.0). Covered by Task 1.
2. **A machine without the brand fonts** (GPU virtual machine, CI, pdfLaTeX biosketch). The figure style must still load with DejaVu Sans, and the LaTeX style must compile under `pdflatex`. Covered by Tasks 3 and 4.
3. **A token edited without a rebuild.** `build.py --check` must fail, naming the stale file. Covered by Task 2.
4. **A project asking for an accent outside the three, or for two accents.** `design_md(accent)` raises `ValueError`, and the skill text says one accent per project. Covered by Task 6.
5. **A pinned link that does not resolve** (tag or path typo). `cdn_url(tag, path)` is tested against real installed paths, and the release step fetches one URL. Covered by Tasks 2 and 10.

---

### Task 0: Branch and working records

**Files:**
- Create: `dev/visual-preference/README.md`, `dev/visual-preference/design.md`, `dev/visual-preference/decisions.md`, `dev/visual-preference/plan.md`, `dev/visual-preference/requirements.txt`

- [ ] **Step 1:** Clone the full repo (not shallow). Run `git switch -c visual-preference` and `git config core.hooksPath .githooks`.
- [ ] **Step 2:** Copy the design doc, the decision log and this plan in. In `README.md`, say what the skill is, how to rebuild (`python dev/visual-preference/build.py`), how to check (`python dev/visual-preference/build.py --check`, `python -m pytest dev`) and how to release (Task 10). In `requirements.txt`, pin the build-only dependencies to the versions installed when the task runs.
- [ ] **Step 3:** Run `python -m pytest dev -q`. Expected: the existing tests pass, because the skill folder does not exist yet.
- [ ] **Step 4:** Commit: `docs(visual-preference): design, decisions and plan`.

### Task 1: The token source

**Files:**
- Create: `plugins/yili-skills/skills/visual-preference/tokens.json`, `dev/visual-preference/derive_light_data.py`, `dev/visual-preference/tests/test_tokens.py`

**Interfaces:**
- Produces: `tokens.json`. These names are used by every later task:
  - colour tokens `ground`, `surface`, `raised`, `rule`, `edge`, `muted`, `ink`, `lichen`, `signal`, `amber`, `data-sky`, `data-rust`, `data-spruce`, `data-sand`, `data-dusk`, `data-ochre`, `data-rose`, `data-olive`, each with `dark` and `light` values
  - type groups `Text` (`label`, `small`, `body`, `h3`, `h2`, `h1`, `display`) and `Numbers` (`num`, `code`)
  - families `spacing` (`space-1`, `space-2`, `space-3`, `space-4`, `space-6`, `space-8`, `space-12`, `space-16`, `space-24`), `radius` (`radius-0`, `radius-dot`), `shadow` (`float`), `duration` (`fast`, `panel`), `easing` (`out`), `layout` (`measure`, `page`, `focus-width`, `focus-offset`)
- Produces: `dev/visual-preference/tests/colour.py` with `contrast(a: str, b: str) -> float` and `min_cvd_distance(hexes: list[str]) -> float`. The second returns the CAM02-UCS minimum pairwise ΔE across normal vision, deuteranomaly, protanomaly and tritanomaly at severity 100.

- [ ] **Step 1: Write the failing tests** in `test_tokens.py`:
  - `test_shape`: every family except `type` has a `tokens` list; names match the regex and are unique; `color.themes == [{"id":"dark","name":"Dark"},{"id":"light","name":"Light"}]`.
  - `test_spec_values`: the 10 neutral and accent tokens equal section 8.4 exactly, for example `ground == {"dark":"#131512","light":"#f2f3ef"}`. Dark data colours equal the spec, for example `data-sky.dark == "#a9cfe6"`.
  - `test_text_contrast`: for each theme, `ink` and `muted` reach ≥ 4.5 on `ground`, `surface` and `raised`; each accent reaches ≥ 4.5 on `ground` and `surface`; `edge` reaches ≥ 3.0 on `ground`.
  - `test_data_distinct`: for each theme, Earth 6 `min_cvd_distance ≥ 11.0` and Earth 8 `≥ 10.0`.
  - `test_light_data_contrast`: every light data colour reaches ≥ 3.0 on `#f2f3ef`.
  - `test_every_token_has_usage`.
- [ ] **Step 2:** Run `python -m pytest dev/visual-preference/tests/test_tokens.py -q`. Expected: FAIL, no `tokens.json`.
- [ ] **Step 3:** Implement `derive_light_data.py`. For each dark data colour, keep the CAM02-UCS hue and chroma, lower J′ until contrast on `#f2f3ef` is ≥ 3.0, then nudge the colours apart until `min_cvd_distance ≥ 10.0`. Print the hexes. Write them into `tokens.json` by hand, so they become source, and log them in `decisions.md` as "Claude's call, for Yili's review in Task 9".
- [ ] **Step 4:** Write `tokens.json` with every value from the Global Constraints and the spec, and a one-line `usage` per token taken from the spec's wording. Add `"meta": {"version": "1.0.0"}`.
- [ ] **Step 5:** Run the tests. Expected: PASS. If Earth 8 fails its dark check, report the measured value rather than change the spec colours.
- [ ] **Step 6:** Commit: `feat(visual-preference): token source`.

### Task 2: Colour maps, the build and the web files

**Files:**
- Create: `plugins/yili-skills/skills/visual-preference/colormaps.json`, `dev/visual-preference/build.py`, `dev/visual-preference/make_colormaps.py`, `dev/visual-preference/tests/test_build.py`
- Generated: `web/tokens.css`, `web/tailwind-v4.css`, `web/tailwind-v3.cjs`, `web/colormaps.js`

**Interfaces:**
- Consumes: `tokens.json` (Task 1).
- Produces:
  - `colormaps.json`: `{"credit": str, "maps": {name: {"kind": "sequential"|"diverging", "use": str, "stops": [hex × 256]}}}` with names `bamako`, `oslo`, `lajolla`, `bilbao`, `lichen`, `lisbon`, `broc`
  - in `build.py`: `load() -> tuple[dict, dict]`, `outputs(tokens, cmaps) -> dict[str, str]` (relative path → text), `cdn_url(tag: str, path: str) -> str`, and the `main(argv)` options `--check` and `--version X.Y.Z`

- [ ] **Step 1: Write the failing tests** in `test_build.py`:
  - `test_colormaps_credit`: the credit contains `"Crameri"` and `"10.5281/zenodo.1243862"`.
  - `test_sequential_monotonic`: CAM02-UCS J′ strictly rises (or falls) along each sequential map. For `lichen`, the steps are even (max step / min step ≤ 1.5).
  - `test_diverging_symmetric`: the J′ of `stops[i]` and `stops[255-i]` differs by ≤ 3.
  - `test_css_has_every_token`: every colour, spacing, radius, shadow, duration, easing and layout token appears as `--<name>:` in `web/tokens.css`. The light theme sits in `[data-theme="light"]` and in `@media (prefers-color-scheme: light)` under `:root:not([data-theme="dark"])`.
  - `test_tailwind_outputs`: `tailwind-v4.css` has an `@theme` block with `--color-lichen`. `tailwind-v3.cjs`, run through `node -e "require(...)"`, has `theme.extend.colors.lichen`.
  - `test_check_detects_stale`: edit a copy of `tokens.json` in a temporary folder and call `main(["--check", "--root", tmp])`. Expected: exit code 1, with the stale path in the message.
  - `test_cdn_url_resolves_to_installed_path`: `cdn_url("visual-preference-v1.0.0", "web/tokens.css")` ends with a path that exists under the installed folder.
- [ ] **Step 2:** Run them. Expected: FAIL.
- [ ] **Step 3:** Implement `make_colormaps.py`. Write the six Crameri maps from `cmcrameri` at 256 stops. Build `lichen` from `#1c2418` to `#f2f3e6` through `#a3b86c`, interpolated in CAM02-UCS with even J′.
- [ ] **Step 4:** Implement `build.py`. Write each output only when its text changes. `--check` compares without writing.
- [ ] **Step 5:** Run `python dev/visual-preference/build.py`, then run the tests. Expected: PASS.
- [ ] **Step 6:** Commit: `feat(visual-preference): colour maps, build and web files`.

### Task 3: The figure style

**Files:**
- Generated: `figures/visual-preference-dark.mplstyle`, `figures/visual-preference-light.mplstyle`, `figures/visual_preference.py`
- Test: `dev/visual-preference/tests/test_figures.py`

**Interfaces:**
- Produces `visual_preference.py`, a self-contained file that projects copy, with:
  - `use(theme: str = "light") -> None`: applies the style; registers the colour maps as `vp.bamako` and the others; falls back to DejaVu Sans with one warning when Albert Sans is missing
  - `GROUPS: list[str]`: Earth 6, then rose and olive
  - `ACCENTS: dict[str, str]`

- [ ] **Step 1: Write the failing tests:**
  - `test_use_light_and_dark`: after `use("dark")`, `rcParams["figure.facecolor"] == "#131512"`; `axes.spines.top` and `axes.spines.right` are off; `axes.prop_cycle` colours equal the dark Earth 6 in order.
  - `test_colormaps_registered`: `matplotlib.colormaps["vp.bamako"]` exists.
  - `test_missing_font_falls_back`: in a subprocess where no Albert Sans is installed, a plot saves to PNG with no exception and with one warning.
- [ ] **Step 2:** Run them. Expected: FAIL.
- [ ] **Step 3:** Extend `outputs()` to produce the three files from the tokens and colour maps:
  - tick labels in IBM Plex Mono, with DejaVu Sans Mono as the fallback
  - a light y-grid in `rule`
  - the line-width and size scale from the spec, at body 10pt for figures
- [ ] **Step 4:** Rebuild and run the tests. Expected: PASS.
- [ ] **Step 5:** Commit: `feat(visual-preference): figure style`.

### Task 4: The LaTeX style

**Files:**
- Generated: `latex/visual-preference.sty`
- Test: `dev/visual-preference/tests/test_latex.py`

- [ ] **Step 1: Write the failing tests.** `test_compiles_xelatex` and `test_compiles_pdflatex` compile a 10-line sample document (`\usepackage{visual-preference}`, a section, text, a number) in a temporary folder. Each must exit 0. Skip with a reason when the engine is missing.
- [ ] **Step 2:** Run them. Expected: FAIL.
- [ ] **Step 3:** Generate the `.sty`:
  - `\definecolor` for the light tokens and the dark lichen
  - under XeTeX or LuaTeX: `fontspec` with Albert Sans text, Source Serif 4 headings and IBM Plex Mono, falling back to TeX Gyre Heros, TeX Gyre Termes and Latin Modern Mono through `\IfFontExistsTF`
  - under pdfTeX: `helvet`, `mathptmx` and `lmodern`
  - section headings in the serif; rules in dark lichen
- [ ] **Step 4:** Rebuild and run the tests. Expected: PASS on the available engines.
- [ ] **Step 5:** Commit: `feat(visual-preference): LaTeX style`.

### Task 5: The marks and the social preview

**Files:**
- Generated: `marks/mark-lichen.svg`, `marks/mark-signal.svg`, `marks/mark-amber.svg`, `marks/favicon.svg`, `marks/wordmark-dark.svg`, `marks/wordmark-light.svg`
- Create: `templates/social-preview.html`
- Test: `dev/visual-preference/tests/test_marks.py`

**Interfaces:**
- Produces in `build.py`: `wordmark_svg(name: str, accent: str, theme: str) -> str`. The text is outlined to paths from the Albert Sans 600 glyphs. The square's side is 0.22 × the type size, it sits on the baseline, and the gap is 0.1 × the size.
- Produces `templates/social-preview.html`: 1280×640, with the slots `{{kicker}}`, `{{name}}`, `{{line}}`, `{{repo}}` and `{{accent}}`. It loads Google Fonts.

- [ ] **Step 1: Write the failing tests:**
  - every SVG parses as XML and has a `viewBox`
  - each mark contains only its accent hex
  - `favicon.svg` contains `#131512` and `#a3b86c`
  - the wordmarks contain no `<text>` element, so they need no font
  - the template contains every slot
- [ ] **Step 2:** Run them. Expected: FAIL.
- [ ] **Step 3:** Implement. Fetch the font with `fonttools` from the Google Fonts static TTF at build time; do not commit it.
- [ ] **Step 4:** Rebuild and run the tests. Expected: PASS.
- [ ] **Step 5:** Commit: `feat(visual-preference): marks and social preview`.

### Task 6: The DESIGN.md template

**Files:**
- Generated: `templates/DESIGN.md`
- Test: `dev/visual-preference/tests/test_design_md.py`

**Interfaces:**
- Produces in `build.py`: `design_md(accent: str, project: str) -> str`. It raises `ValueError` for any accent other than `lichen`, `signal` or `amber`. It writes front matter in the shape the Impeccable skill reads (`colors:`, `typography:`, `rounded:`, `spacing:`, as in Livability Atlas's `DESIGN.md`), then short prose: the principles, and one accent per project.
- `templates/DESIGN.md` is `design_md("lichen", "{{project}}")`.

- [ ] **Step 1: Write the failing tests:**
  - the front matter parses as YAML
  - `colors.accent` equals the accent's dark value
  - `design_md("teal", "x")` raises `ValueError`
  - there is one accent key only
- [ ] **Step 2:** Run them, implement, rebuild and run again. Expected: FAIL, then PASS.
- [ ] **Step 3:** Commit: `feat(visual-preference): DESIGN.md template`.

### Task 7: Slide and poster templates (built per release, not committed)

**Files:**
- Create: `dev/visual-preference/build_pptx.py`, `dev/visual-preference/tests/test_pptx.py`
- Ignore: add `dev/visual-preference/build/` to `.gitignore`.

**Interfaces:**
- Produces: `build_pptx(out_dir: Path) -> list[Path]`, which returns `slides.pptx` (dark masters plus a light handout master) and `poster-a0.pptx` (light).

- [ ] **Step 1: Write the failing tests:**
  - both files open in `python-pptx`
  - the slide master background is `#131512`
  - the layouts include `Title`, `Title and figure` and `Section`
  - the title font is `Albert Sans`
  - a footer shows "Yili Yang" and a lichen square
  - the poster is 841×1189 mm with a `#f2f3ef` background
- [ ] **Step 2:** Run them, implement, run again. Expected: FAIL, then PASS.
- [ ] **Step 3:** Commit: `feat(visual-preference): slide and poster builder`.

### Task 8: The manual, the skill and the plugin entries

**Files:**
- Create: `plugins/yili-skills/skills/visual-preference/manual.md`, `plugins/yili-skills/skills/visual-preference/SKILL.md`
- Modify:
  - `plugins/yili-skills/.claude-plugin/plugin.json` (version `2.7.0`, add the skill to the description)
  - `.claude-plugin/marketplace.json` (version `2.7.0` in both places, "Nine skills", add a `visual-preference` clause)
  - `README.md` (one table row)
  - `dev/routing/cases.json` (three cases)
- Test: the existing `dev/tests/test_structure.py`, plus `dev/visual-preference/tests/test_skill.py`

- [ ] **Step 1: Write the failing tests** in `test_skill.py`:
  - every path that `SKILL.md` or `manual.md` names under `web/`, `figures/`, `latex/`, `marks/` or `templates/`, and `tokens.json` and `colormaps.json`, exists
  - every hex value written in `manual.md` exists in `tokens.json`
  - the description contains the words "own projects"
- [ ] **Step 2:** Add the routing cases:
  - `visual-new-repo`: "Set up the look for my new repo, a small web app for my plant collection." Expect `visual-preference`.
  - `visual-figure`: "Make this matplotlib figure of permafrost thaw match my usual style." Expect `visual-preference`.
  - `visual-kimkim`: "For the KIMKIM project, design the colour scheme of a client's building facade." Forbid `visual-preference`.
- [ ] **Step 3:** Write `manual.md` from spec section 8:
  - principles in priority order, each with its reason
  - foundations with the reasons Yili gave or approved
  - one short section per surface (8.6)
  - how a project chooses its accent
  - the AI-default list as "why the system avoids these"
  - the colour-map credit

  Voice: if wording is in doubt, ask *how do my words read?* Never name a skill.
- [ ] **Step 4:** Write `SKILL.md`:
  - **Description:** use when styling, designing or restyling the visuals of Yili's own repos, sites, apps, figures, CV, papers, slides or posters, or when another task needs to know how his work should look. Not for Woodwell organisation repos or for KIMKIM work.
  - **Takes:** the project and its surface.
  - **Returns:** the applied system (files linked or copied with the version, a chosen accent, a `DESIGN.md`) and the critical choices it made.
  - **Body:** a way of seeing in a few short sections: what the system decides and what it leaves to judgement; how to start a new repo and how to convert one; links for the web, copies for LaTeX and Python; and when a surface is not covered, reason from the principles and say so.
- [ ] **Step 5:** Bump the versions and edit the descriptions and the README row.
- [ ] **Step 6:** Run `python -m pytest dev -q` and `python dev/visual-preference/build.py --check`. Expected: all pass, no stale files.
- [ ] **Step 7:** Commit: `feat(visual-preference): manual and skill; plugin 2.7.0`.

### Task 9: Verify with sample renders (stage 13, Yili reviews)

**Files:**
- Create: `dev/visual-preference/samples.py`. Its output goes to `dev/visual-preference/build/samples/`, which is ignored.

- [ ] **Step 1:** Implement `samples.py`. It renders:
  - a web page using `web/tokens.css`, in dark and light: header, project block, a panel with a table and a button, a hairline section, focus ring shown
  - a figure in the light and dark styles, with Earth 6 lines, a `vp.bamako` map and a `vp.lisbon` map
  - a one-page CV sample through `xelatex`
  - the social preview for three repos
  - one slide from `slides.pptx`, converted with LibreOffice if present, else skipped with a note
- [ ] **Step 2:** Run it. Send the images to Yili, together with the derived light data colours from Task 1, as "Claude's call, please confirm".
- [ ] **Step 3:** Fold Yili's corrections into `tokens.json` or the build, rebuild, rerun the tests and commit `fix(visual-preference): review changes`. Repeat until Yili approves.

### Task 10: Release and viewer (stage 14)

- [ ] **Step 1:** Push the branch and open a pull request with `gh api repos/yi-li-yang/skills/pulls`. The body is a summary plus the sample images. Yili merges.
- [ ] **Step 2:** After the merge:
  - tag `visual-preference-v1.0.0` on the merge commit and push the tag
  - run `build_pptx.py`
  - run `gh release create visual-preference-v1.0.0 dev/visual-preference/build/slides.pptx dev/visual-preference/build/poster-a0.pptx --notes-file dev/visual-preference/CHANGELOG.md` (create the CHANGELOG in this step)
- [ ] **Step 3:** Fetch `cdn_url("visual-preference-v1.0.0", "web/tokens.css")` and expect HTTP 200 with the version line. If the cloud session cannot reach jsDelivr, run the check in Yili's Chrome.
- [ ] **Step 4:** Sync the Design System artifact `fcf75c6b-c711-4b7b-83fa-de57a6a03951` by its type's from-code procedure:
  - `project/tokens.json` (copied)
  - `project/README.md` (the manual's brand-book parts)
  - the marks as an asset group `Marks`
  - `components/Cover/preview.html`
  - `project/design-system.json` last, with `"editing": "code"`, so the page is read-only
- [ ] **Step 5:** Tell Yili the release link, the artifact link and the jsDelivr base URL.

Stages 15 (pilot on one repo) and 16 (maintain) get their own short plan after release, because the pilot repo's needs decide them.
