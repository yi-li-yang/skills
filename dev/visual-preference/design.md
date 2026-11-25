# visual-preference: design

Status: Part A (stages 1–4) approved. Part B (stages 5–10, the look) approved stage by stage and recorded in section 8. The build plan is written next.
Date: 2026-11-25. Owner: Yili Yang.

## 1. Intent

Until now, Claude and design skills designed each of Yili's projects, and Yili did not take part. As a result, no two projects share a look, and most borrow another company's system: the personal site copies Linear's, travel-map carries a copy of Notion's design doc, and the Octopus email uses Octopus's colours.

Yili wants one personal style, decided once with him, that every project inherits. It should be built efficiently on existing skills and ready-made designs, and it should look better than what an agent improvises for each repo.

## 2. Goals, non-goals, anti-goals

**Goals**

- One visual system that is Yili's: his taste, recorded with the reasons behind it.
- A new repo gets the style in one step.
- An existing repo can be converted on its own, one at a time.
- Agents and other design skills can adapt the system to a surface it has not seen, using the manual and the skill.

**Non-goals**

- Covering every choice. The system fixes the critical choices only, and agents may improvise inside it.
- Strict enforcement. No automatic check, and no failing builds.
- Woodwell organisation repos.
- KIMKIM projects (another person's work on the same account).

**Anti-goals** (it has failed if this happens, even when it works technically)

- It looks like another company's system again.
- It overrides a journal's figure rules or an app's data colours that carry meaning.
- Keeping it up to date takes more effort than restyling each repo did.

## 3. Audience and coverage

- **Audience:** everyone. No reader is singled out, so the style must read well to a stranger at first glance.
- **Covers:** personal repos and the site (app interfaces, README images), papers, figures and talks (inside each journal's rules), the curriculum vitae (CV) and job applications.
- **Shape:** a family. Typefaces, neutrals, spacing and the mark are shared everywhere. Each project may choose its own accent colour and name.
- **Start:** from scratch. No earlier project look carries over.

## 4. Products (all in the first release)

| # | Product | Form |
|---|---|---|
| 1 | Manual: principles, voice, foundations, each with its reason, plus one short section per surface that exists now (web app, map or data app, README, figure, LaTeX document, slides or poster) | Markdown |
| 2 | Tokens and web files: one source file, built into CSS (Cascading Style Sheets) variables, a Tailwind version 3 preset and a Tailwind version 4 theme. Includes data palettes (categorical, sequential, diverging; colour-blind safe), shared by web apps, maps and figures | JavaScript Object Notation (JSON) source, generated text files |
| 3 | Marks: logo, favicon, social-preview template, README image frame | SVG (Scalable Vector Graphics) |
| 4 | Skill: applies and adapts the system, and writes a repo's `DESIGN.md` from one template | `SKILL.md` |
| 5 | Figure style: matplotlib style file plus colour maps | `.mplstyle`, Python |
| 6 | LaTeX style for the CV, letters and papers | `.sty` |
| 7 | Slide and poster templates | `.pptx`, built per release |
| 8 | Viewer: the Design System artifact on claude.ai | synced copy |

Cut for now, and added only when a real need shows: separate surface-guide documents, README / `PRODUCT.md` / `preview.json` templates, an advisory check script, a CI (continuous integration) workflow.

## 5. Approaches considered

1. **A separate `yi-li-yang/brand` repo that is also its own plugin.** Everything versions together, but it is a second plugin to manage.
2. **Assets in a brand repo, skill in `yili-skills`.** The skill and the standard version separately and can drift apart.
3. **A `DESIGN.md` copied into each repo.** Lightest, but the copies drift, which is the problem this project exists to stop.
4. **Chosen: everything in the existing `skills` repo, as one more skill in the `yili-skills` plugin.** Yili manages one repo, one plugin and one version line. The cost is that a brand release also bumps the plugin version, and the skill must follow that repo's rules (see section 7).

## 6. Structure, hosting, versions (decided)

```text
skills/
├─ plugins/yili-skills/skills/visual-preference/   installed; small text files only
│  ├─ SKILL.md          a way of seeing; values live in the files below
│  ├─ manual.md         principles, voice, foundations, surface sections
│  ├─ tokens.json       the one source
│  ├─ web/              tokens.css, tailwind-v3 preset, tailwind-v4 theme   (generated)
│  ├─ figures/          visual-preference.mplstyle, colormaps.py           (generated)
│  ├─ latex/            visual-preference.sty                              (generated)
│  ├─ marks/            logo, favicon, social preview, README frame (SVG)
│  └─ templates/        DESIGN-<accent>.md (one per accent), social-preview.html
└─ dev/visual-preference/                           not installed
   ├─ README.md
   ├─ build.py          tokens.json -> every generated file, and the .pptx
   └─ tests/
```

- **Web projects** load `web/tokens.css` (and Tailwind files) from jsDelivr at a pinned tag, for example `cdn.jsdelivr.net/gh/yi-li-yang/skills@visual-preference-v1.0.0/plugins/yili-skills/skills/visual-preference/web/tokens.css`.
- **LaTeX and Python projects** get copies from the skill, with the version written in the first line of each file.
- **Versions:** tags `visual-preference-vX.Y.Z`. The plugin version in `plugin.json` and `marketplace.json` bumps too. Each GitHub release attaches the slide and poster `.pptx` built from the tokens.
- **Fonts:** open-licence (SIL Open Font License) faces that Google Fonts serves. Web pages load them from Google Fonts. LaTeX and Python projects copy the font files from the font's own source. The skills repo stores no binary file.
- **Viewer:** Claude re-syncs the Design System artifact from the repo at each release. The page stays read-only, so the repo stays the one source.
- **Build:** runs locally, and the release is made with `gh`. No CI until a need shows.

## 7. Constraints found in the existing repos

- **`skills` repo rules (`CLAUDE.md`):**
  - A skill is a way of thinking, not rules, checklists or thresholds. So `SKILL.md` explains how Yili's work should look and why, and exact values stay in `tokens.json` and the generated files, the same way the wardrobe skill keeps its record.
  - The body opens with **Takes:** and **Returns:** lines, and `python -m pytest dev` checks this.
  - A skill never names another skill. When it needs one answered, it asks the question, for example *how do my words read?* for voice.
  - Plain Simplified Technical English. No non-English words in the skill.
  - Bump both version files on every change.
  - Development material stays out of the installed folder.
  - The privacy hooks in `.githooks/` stay on.
- **Skill scope:** the description must keep it to Yili's own projects. The same account is used for KIMKIM work, and Woodwell repos are out of scope.
- **Tailwind:** travel-map uses version 3.4 (a JavaScript config). Livability Atlas uses version 4.3 (a CSS theme). Both outputs are needed.
- **LaTeX engines:** the site repo builds the one-page CV with XeLaTeX, tailored CVs with Tectonic (also XeTeX-based), and the biosketch with pdfLaTeX. `fontspec` does not work in pdfLaTeX, so the style must load the brand faces under XeTeX and fall back to standard font packages under pdfLaTeX.
- **matplotlib:** the style must fall back cleanly (to DejaVu Sans) when the brand font is not installed, for example on a GPU virtual machine.
- **auto-generate-preview-image** says "no device frames, no added captions, no marketing overlays" and "each app keeps its own look". So the "README image frame" may only fix the canvas: size, background, corner radius and edge colour. It may not add chrome or text. This is decided in stage 9.
- **Design System artifact format:** its page reads tokens as lists (`{"tokens":[{"name","value","usage"}]}`), not the W3C Design Tokens format. *Claude's call:* `tokens.json` uses the artifact's list format, so the viewer sync is a plain copy.
- **Favicon and social preview:** browsers and GitHub need PNG (Portable Network Graphics) files in some places (Apple touch icon; GitHub's social-preview upload, 1280×640). *Claude's call:* the skill renders these PNGs inside each project from the SVG when that project needs them. None are stored in the skills repo.
- **Not read:** the private repos (bookkeeping-auto, price-watch) were not reachable in this session. Their surfaces are assumed to be web apps like the others.

## 8. Part B: the look (decided)

"Yili's pick" marks a choice Yili made from options he was shown. "Claude's call" marks a choice he delegated.

### 8.1 Taste (stage 5)

- **Presence:** professional and polished, good taste, not the cheap AI default. Not loud: the content comes first.
- **Home:** a dark screen; light is secondary. **Material:** natural and earthy. **Meaning:** abstract, with no literal Arctic, rock or Chinese imagery. **Density:** balanced.
- **References:** science editorial (Nature, The Economist graphics), field instruments (Arc'teryx, Leica), DJI, NASA, Apple, National Geographic.
- **Avoid:** emoji and sparkles, plus the researched AI-default list:
  - overused faces (Inter, Roboto, Arial, Open Sans, Geist, Plus Jakarta Sans, Space Grotesk, Fraunces)
  - purple-blue gradients, glow on dark, gradient text, pure `#000`
  - side-bar accent cards, soft-shadow card grids, glass as decoration, nested cards, icon-above-heading tiles
  - everything centred, uniform spacing, the hero-metric layout, decorative sparklines, bouncy motion

### 8.2 Principles and voice (stage 6, Claude's call; a higher principle wins a conflict)

1. **Readable by everyone:** WCAG AA contrast in both themes, colour never the only cue, colour-blind-safe palettes, works on a phone, reduced motion respected.
2. **The work leads:** the style frames the content and never competes with it. Maps, imagery and data carry the colour, and every element earns its place.
3. **Colour means something:** the accent marks the one focus or action, and data palettes mark data.
4. **Editorial clarity:** hierarchy from size, weight and space. Text aligned left, and captions, units and sources visible.
5. **Built like an instrument:** exact alignment, a strict scale, hairline rules, matte surfaces. No glow, glass or soft-shadow cards.

Voice: no new voice. Interface words follow Yili's existing plain-English writing rules.

### 8.3 Direction "Stone and Signal" (stage 7, Yili's pick)

- **Ground:** one shared stone-grey ground for every project (made greyer at the stage 13 review, at Yili's request).
- **Accents:** they rotate between projects, one per project and never mixed. Lichen green is home (site, CV, papers, mark, and the default for a new project); signal orange and amber are the others.
- **Details everywhere:** spaced capital labels, square corners, monospace numbers, hairline rules, no shadows, no glow.

### 8.4 Foundations (stage 8)

| Token | Dark (home) | Light (paper) | Use |
|---|---|---|---|
| ground | `#141413` | `#f4f2f0` | page |
| surface | `#1c1c1b` | `#ebe9e6` | panels |
| raised | `#242522` | `#ffffff` | floating panels |
| rule | `#363734` | `#d2d1cd` | dividers |
| edge | `#6e6f6c` | `#82837f` | control borders (3:1) |
| muted | `#a0a09d` (7.0:1) | `#5e5f5c` (5.7:1) | secondary text |
| ink | `#e8e7e3` (14.8:1) | `#1b1c1a` (15.3:1) | text |
| lichen (home) | `#a3b86c` | `#566a26` | accent |
| signal | `#e2652f` | `#b0441a` | accent |
| amber | `#e0a84a` | `#8a5d0c` | accent |

- **Type:**
  - Albert Sans 400/500/600 for text, interface and headings (Yili's pick from 21 faces).
  - IBM Plex Mono for numbers and code (Yili's pick). It is needed because Albert Sans has no tabular figures.
  - Source Serif 4 for headings in long documents only (Claude's call).
  - Noto Sans SC for Chinese text.
  - Sizes 12 (label), 14, 16 (body), 20, 25, 31, 49. Labels in capitals with +0.1em spacing. Line height 1.55 for text, 1.15 for headings. Text width at most 68 characters.
- **Space and shape:**
  - Spacing 4, 8, 12, 16, 24, 32, 48, 64, 96.
  - Corners 0, with circles only for dots.
  - No shadows, except one functional shadow for panels over maps or imagery.
- **Motion:** 120 ms for hover, 200 ms for panels, ease-out, no bounce; off for reduced motion. **Focus:** a 2px accent ring with a 2px gap. **Icons:** Tabler outline at 1.5px stroke (Yili's pick).
- **Data colour (Yili's picks, Claude's roles):**
  - **Groups:** Earth 6 (sky `#a9cfe6`, rust `#c4573a`, spruce `#4f9a7d`, sand `#d8c48e`, dusk `#8a7fb8`, ochre `#c9962e`). Rose `#d98ca0` and olive `#b0ac5a` are added only when a chart has 7–8 groups. In CAM02-UCS under three colour-vision simulations, Earth 6 scores 14.5 against Okabe–Ito's 11.0. The 8-colour set must be re-checked in the build.
  - **Sequential, chosen by meaning:** Crameri bamako as the default (land, vegetation), oslo (ice, snow, water), lajolla (heat, fire, intensity), bilbao (soil, sediment), plus a custom lichen ramp for small interface charts. Its lightness must be checked in the build.
  - **Diverging (Claude's call):** Crameri lisbon on dark pages, broc on light pages.

### 8.5 Mark (stage 9)

- **The mark is the square full stop** (Yili's pick from 11). It is one solid square in the accent. On its own it is the favicon and avatar; after a name it is a full stop. Its side is 0.22× the type size, it sits on the baseline, and the gap is 0.1× the size.
- **Project variants (Claude's call):** each project ends its name with the square in its own accent. Yili's name always keeps the lichen square.
- **Social preview (1280×640):**
  - a kicker in spaced capitals
  - the name plus its accent stop
  - a one-line purpose
  - a hairline
  - "Yili Yang" with the lichen stop
  - the repo path in IBM Plex Mono
- **README top (Claude's call):** app repos lead with the live preview image; non-app repos lead with the social card; never both.

### 8.6 Surface guides (stage 10, Claude's defaults, approved)

- **Web app / site:**
  - Dark by default; light follows the system setting.
  - 68-character column, 1200px page.
  - Hairline sections, not cards.
  - One filled accent button per view; other actions are underlined text.
- **Map or data app:**
  - The map fills the window, on a dark matte basemap tinted to stone.
  - Panels float at the edges on `raised` with the one functional shadow.
  - Data colour comes only from the data palettes. The accent marks selection and focus, never data.
  - Every value shows a number, a unit and a source.
- **Desktop widget:** compact (12–14px), monospace numbers, no glass (solid surface at 96%).
- **README:**
  - The top image, then one sentence on what it is, then install and use.
  - Images carry their own stone ground.
  - At most a licence badge and one status badge.
- **Scientific figure:**
  - Light in papers, where journal rules win; stone dark on the web and in slides.
  - Albert Sans text, IBM Plex Mono ticks.
  - No top or right spines, a light y-grid only.
  - At most one accent highlight.
  - Units on axes, source in the caption.
- **CV, letters, papers:**
  - Paper ground.
  - Source Serif 4 headings, Albert Sans text, IBM Plex Mono numbers.
  - Dark lichen only for rules and the stop.
  - pdfLaTeX fallback.
- **Slides:**
  - Dark by default, with a light variant for handouts.
  - One idea per slide, titles written as sentences, full-bleed figures.
  - Name and stop at the bottom left; the slide number in mono at the bottom right.
- **Poster:** light paper. **Email:** light, with charts in the figure style.

The working record of every choice, including the options shown, is kept in `dev/visual-preference/decisions.md`.

## 9. Left to the builder

- File names inside `web/`, `figures/` and `latex/`.
- The build script's language: Python, matching the `skills` repo's tests.
- How many tests. A few that check the generated files match the tokens, plus the repo's existing structure test.
- The wording of the skill, which goes through Yili's writing rules.

## 10. Next stages (C)

11 Build · 12 Write the skill and manual · 13 Verify with sample renders that Yili reviews · 14 Release · 15 Pilot on one repo · 16 Maintain.
