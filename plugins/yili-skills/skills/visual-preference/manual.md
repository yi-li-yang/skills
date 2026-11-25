# The manual

This is how Yili Yang's own work looks, and why. It covers his repos, his site, his apps and maps, and his figures, documents, slides and posters. Yili chose each part from options he was shown. Where he left a choice to judgement, the manual says so.

The system decides the choices that make the work recognisable and readable: the ground, the accent, the type, the data colours and the mark. Everything else is judgement, guided by the principles below. When a case is not covered here, reason from the principles in their order, and say which choice was made that way.

The values live in `tokens.json`. Every file under `web/`, `figures/`, `latex/`, `marks/` and `templates/` is built from it. This manual quotes values only to explain them.

## Principles, in order

When two principles pull apart, the higher one wins.

1. **Readable by everyone.** Text reaches WCAG AA contrast (4.5:1, or 3:1 for large text and control edges) in both themes. Colour is never the only cue: a value also has a position, a length, a label or a number. Data colours stay distinct under the common colour-vision deficiencies. Pages work on a phone, and motion stops when the reader asks for reduced motion. The audience is everyone, so this comes first.
2. **The work leads.** The style frames the content and never competes with it. Maps, images and data carry the colour, and the interface stays in the stone neutrals. Each element earns its place; when one is in doubt, remove it.
3. **Colour means something.** The accent marks the one focus or action in a view. The data colours mark data. A colour with no meaning is decoration, and the system has none.
4. **Editorial clarity.** Hierarchy comes from size, weight and space, as in a good science magazine. There are few type sizes, with clear steps between them. Text is aligned left. Captions, units and sources are always visible.
5. **Built like an instrument.** Alignment is exact, the scale is strict, rules are hairlines and surfaces are matte. Numbers are set in a monospace face so that their columns align. There is no glow, no glass and no soft-shadow card.

## Colour

### The ground

Every project shares one ground: a dark stone grey with the faintest green, natural and matte. Yili asked for it greyer than the first draft. Dark is home, because Yili works on a dark screen. A light theme exists for paper, papers and READMEs, and it follows the reader's system setting on the web.

| Token | Dark | Light | Used for |
|---|---|---|---|
| `ground` | #141413 | #f4f2f0 | the page |
| `surface` | #1c1c1b | #ebe9e6 | panels and quiet blocks |
| `raised` | #242522 | #ffffff | panels that float, for example over a map |
| `rule` | #363734 | #d2d1cd | hairline dividers (decoration only) |
| `edge` | #6e6f6c | #82837f | borders of controls; 3:1 on the ground |
| `muted` | #a0a09d | #5e5f5c | secondary text, labels, captions, axis text |
| `ink` | #e8e7e3 | #1b1c1a | text and the strongest marks |

Text is never pure white or pure black, and the ground is never pure black. A neutral tinted towards stone reads as a material; pure black reads as a default.

### The accents

There are three accents, and each project carries one of them, never two.

| Accent | Dark | Light | Character |
|---|---|---|---|
| `lichen` | #a3b86c | #566a26 | quiet and natural. **Home:** Yili's site, CV, papers and mark, and the default for a new project |
| `signal` | #e2652f | #b0441a | an instrument's signal. The most visible of the three |
| `amber` | #e0a84a | #8a5d0c | warm and editorial |

The accent marks the one focus or action in a view: the one filled button, the selected tab, the focus ring, the primary link's underline, and the full stop after the project's name. It is never a data colour, and it never fills a large area.

To choose a project's accent, start from lichen. Move to another accent when the project's data already uses a colour close to lichen (a vegetation map, for example), or when the project sits next to another of Yili's projects with the same accent and a reader would confuse the two. Record the choice in the project's `DESIGN.md`.

### Data colours

For groups (categories), use **Earth 6**, in this order: sky, rust, spruce, sand, dusk, ochre. For seven or eight groups, use **Earth 8**: glacier, rust, spruce, sand, dusk, rose, olive, sky. Earth 8 swaps ochre for glacier and adds two colours, because six colours plus two more does not stay distinct. More than eight groups are too many to tell apart by colour; label them, or show fewer.

| Group colour | Dark | Light |
|---|---|---|
| `data-sky` | #a9cfe6 | #48606e |
| `data-rust` | #c4573a | #9c3f27 |
| `data-spruce` | #4f9a7d | #307f67 |
| `data-sand` | #d8c48e | #9e8a59 |
| `data-dusk` | #8a7fb8 | #72679f |
| `data-ochre` | #c9962e | #9e7002 |
| `data-glacier` | #86b2d4 | #6490b0 |
| `data-rose` | #d98ca0 | #bc7387 |
| `data-olive` | #b0ac5a | #7a801b |

Both sets were measured in a perceptual colour space under simulated deuteranopia, protanopia and tritanopia. On either ground, Earth 6 stays more distinct than the Okabe–Ito set, which is the usual colour-blind standard. The light values are the dark ones, darkened to read on paper and spread apart again.

For continuous values, choose the colour map by what the data is:

| Map | Kind | Use |
|---|---|---|
| `bamako` | sequential | the default: land, vegetation, anything without a closer match |
| `oslo` | sequential | ice, snow and water |
| `lajolla` | sequential | heat, fire, intensity |
| `bilbao` | sequential | soil and sediment |
| `lichen` | sequential | small interface charts that carry the home accent |
| `lisbon` | diverging | below and above a middle, on dark pages: the middle sinks into the ground |
| `broc` | diverging | below and above a middle, on light pages and in papers |

Every map changes lightness evenly, so equal steps in the data look equal, and none depends on red against green. Use one map per figure. A meaningful scale that a project already has (a score from worse to better, for example) stays, if it meets the first principle.

The maps bamako, oslo, lajolla, bilbao, lisbon and broc are Fabio Crameri's Scientific colour maps: Crameri, F. (2018), Scientific colour maps, Zenodo, doi:10.5281/zenodo.1243862. Cite them in a paper that uses them. The values are in `colormaps.json`.

## Type

- **Albert Sans** sets text, interface and headings, in weights 400, 500 and 600 only. Yili chose it from 21 faces.
- **IBM Plex Mono** sets numbers and code. Albert Sans has no tabular figures, so a number in a table or a live readout would shift as it changes. Every number that sits in a column or changes is set in the monospace face.
- **Source Serif 4** sets headings in long documents only: papers, the CV, essays. Apps and READMEs use Albert Sans alone, so that they do not read as a magazine.
- **Noto Sans SC** sets Chinese text.

All four faces are open-licence faces served by Google Fonts.

| Style | Size | Line height | Weight | Use |
|---|---|---|---|---|
| label | 12px | 1.55 | 500 | capitals, letter-spacing 0.1em, over groups and sections |
| small | 14px | 1.55 | 400 | captions, notes, dense panels |
| body | 16px | 1.55 | 400 | reading and interface text |
| h3 | 20px | 1.15 | 600 | small headings |
| h2 | 25px | 1.15 | 600 | section headings |
| h1 | 31px | 1.15 | 600 | page headings |
| display | 49px | 1.15 | 600 | at most one per page: a name or a title |

A column of text is at most 68 characters wide.

## Space, shape, depth and motion

- **Space** steps are 4, 8, 12, 16, 24, 32, 48, 64 and 96px. Use space to group; a gap does the work that a box would otherwise do.
- **Corners** are square everywhere. Only a dot (a status dot, for example) is round.
- **Depth:** nothing casts a shadow, except a panel that floats over a map or an image, which uses the one `float` shadow so that it stays legible. Sections are divided by hairline rules, never by cards inside cards.
- **Motion** takes 120ms for hover and 200ms for panels, and always eases out. Nothing bounces. Motion stops for a reader who asks for reduced motion.
- **Focus:** a 2px ring in the accent, 2px from the control.
- **Icons** come from the Tabler outline set at a 1.5px stroke, in `ink` or `muted`, never in colour.

## The mark

The mark is a square full stop: one solid square in the accent. On its own, it is the favicon and the avatar. After a name, it ends the name like a full stop: "Yili Yang" with a lichen square. Its side is 0.22 of the type size, it sits on the baseline, and it starts 0.1 of the type size after the last letter.

Each project ends its own name with the same square in its own accent. Yili's name always keeps the lichen square, so every project points home.

The files are in `marks/`: `mark-lichen.svg`, `mark-signal.svg` and `mark-amber.svg` (the square alone), `favicon.svg` (the lichen square on the stone ground), and `wordmark-dark.svg` and `wordmark-light.svg` (the name with its stop, drawn as outlines, so that they need no font).

## Surfaces

**Web app or site.** Dark by default; light follows the reader's system setting. Pages are at most 1200px wide. Sections are divided by hairline rules, not cards. Each view has one filled button, in the accent; other actions are underlined text. Labels over groups are spaced capitals.

**Map or data app.** The map fills the window, on a dark, matte basemap tinted towards stone, with labels in `muted`. Panels float at the edges on `raised`, with the one `float` shadow. Data takes its colour only from the data colours. The accent marks selection and focus and never encodes data. Every value shows a number, a unit and a source.

**Desktop widget.** As a web app, but compact: 12–14px text, numbers in the monospace face, and a solid `surface` at 96% opacity instead of glass.

**README.** The first image is the app's own live preview. A repo with no app uses its social preview card instead; it never uses both. Then one sentence on what the project is, then how to install and use it. Images carry their own stone ground, so they read on GitHub's light and dark themes. Use at most two badges: the licence and one status.

**Scientific figure.** In a paper, the figure is light, on white, and the journal's own rules win. On the web and in slides it is dark, on stone. There are no top or right spines, only a light horizontal grid. Lines take the data colours in order, with at most one series picked out in the accent. Every axis has a unit, and the caption names the source.

**CV, letters and papers.** Paper ground and ink text. Headings are in Source Serif 4, text in Albert Sans, and numbers in IBM Plex Mono. The light lichen (#566a26) appears only in rules and in the stop.

**Slides.** Dark by default, because a dark slide is safe on most projectors; the light version is for printed handouts. Each slide carries one idea, its title is a sentence, and figures fill the slide. The name and its stop sit at the bottom left, and the slide number, in the monospace face, at the bottom right.

**Poster.** Light paper, because a dark poster prints muddy and uses a lot of ink. The type and the grid are the same as for slides, at a larger scale.

**Email** (for example, a daily price chart). Light, because mail apps differ. Charts use the figure style.

## What the system avoids, and why

These choices are what a design tool or a model makes when nobody has decided anything, so readers now take them as a sign that nobody did:

- the overused faces: Inter, Roboto, Arial, Open Sans, Geist, Plus Jakarta Sans, Space Grotesk, Fraunces
- purple-to-blue gradients, glowing accents on a dark ground, gradient text, and a pure black ground
- a coloured bar down one side of a card, grids of identical rounded cards with soft shadows, glass used as decoration, cards inside cards, and an icon tile above every heading
- everything centred, one spacing value everywhere, a big number with three small stats as a hero, and small charts that are decoration
- emoji and sparkles used as icons, and bouncy motion

The system does not avoid these by rule. Each one breaks a principle above: most of them add something that means nothing, or put the style ahead of the work.

## Using the files

The tag of a release is `visual-preference-v` followed by the version in `tokens.json` (for example `visual-preference-v1.0.0`).

- **Web:** load `web/fonts.css` and `web/tokens.css` from jsDelivr at the tag, for example `https://cdn.jsdelivr.net/gh/yi-li-yang/skills@visual-preference-v1.0.0/plugins/yili-skills/skills/visual-preference/web/tokens.css`. Then use the custom properties (`var(--ink)`, `var(--lichen)`, `var(--space-4)`) and the type classes (`.vp-body`, `.vp-label`, `.vp-num`). With Tailwind 4, also import `web/tailwind-v4.css`; with Tailwind 3, add `web/tailwind-v3.cjs` as a preset. For maps, `web/colormaps.js` exports the colour maps. Set `data-theme="dark"` or `data-theme="light"` on the page to fix a theme.
- **Python figures:** copy `figures/visual_preference.py` into the project, then call `use("light")` or `use("dark")`. The colour maps become `vp.bamako` and the others, and `mono_ticks(ax)` sets an axes' tick numbers in the monospace face. Without the fonts, it falls back to DejaVu Sans and says so once. `figures/visual-preference-light.mplstyle` and the dark one are the same settings as plain style files.
- **LaTeX:** copy `latex/visual-preference.sty` beside the document and add `\usepackage{visual-preference}`. It works under XeLaTeX, LuaLaTeX and Tectonic with the brand faces or their fallbacks, and under pdfLaTeX with standard faces. `\vpnum{}` sets a number, `\vprule` draws a lichen rule, `\vpstop` draws the stop, and `\vplabel{}` sets a spaced label.
- **A project's design record:** fill `templates/DESIGN.md` with the project's name and its accent, and keep it at the project's root, where design tools read it.
- **Social preview:** fill the slots in `templates/social-preview.html` (kicker, name, one line, repo, accent), render it at 1280 × 640, and save it as a PNG for the repo's settings.
- **Slides and posters:** the `.pptx` templates are attached to each release on GitHub.

A copied file names its version in its first line. When a newer version is released, copy again.
