# Personal brand system: decisions log

## Stage 1: Purpose and scope (approved for now, 2026-11-25; revisit if a problem emerges)

- Why: until now Claude and design skills designed each project without Yili. One personal style, decided once with Yili, shared by every project, built efficiently on existing skills and ready-made designs, better looking than per-repo improvising.
- For whom: everyone. No audience singled out; the style must read well to a stranger at first glance.
- Covers: personal repos and site (apps, README images); papers, figures, talks (inside each journal's rules); CV and job applications.
- Does not cover: Woodwell organisation repos; KIMKIM projects (another person's work on the same account).
- Shape: a family. Shared typefaces, neutrals, spacing and mark; each project may pick its own accent and name.
- Start: from scratch. No earlier project look carries over.
- Deliverable: a complete system (manual, skill, documentation, standards) so other projects and agents can adapt it.
- Done when: a new repo gets the style in one step; existing repos can be converted one at a time.
- Strictness: the system decides the critical choices only, not everything. Agents may improvise inside it. No strict automatic enforcement.

## Stage 2: Product list (approved, 2026-11-25). All in the first release.

Core
1. Manual: principles, voice, foundations, each with its reason. One short section per surface that exists now: web app, map/data app, README, figure, LaTeX document, slides/poster.
2. Tokens + web files: one source file, built into CSS variables and a Tailwind preset. Includes data palettes (categorical, sequential, diverging; colour-blind safe) shared by web apps, maps and figures.
3. Marks: logo, favicon, social preview, README image frame (SVG).
4. Skill: applies and adapts the system; writes a repo's DESIGN.md from one template.
Science and documents
5. Figure style: matplotlib style + colour maps.
6. LaTeX style: CV, letters, papers.
7. Slide and poster templates (.pptx).
Helper
8. Viewer: the Design System artifact, where Yili sees and judges the look in stages 7-9.
Cut for now (YAGNI; add when a real need shows): separate surface-guide documents (folded into manual); README, PRODUCT.md, preview.json templates; advisory check script and CI workflow.
Plumbing: build script (tokens -> files), a few tests, a version tag.
User note on core list: "not limited to above". User asked: only essentials, don't overengineer, YAGNI; Claude's judgement on helpers.

## Stage 3: Structure, hosting, versions (approved, 2026-11-25)

- One repo (skills), one plugin (yili-skills), one new skill named visual-preference (user's choice of name).
- Installed folder plugins/yili-skills/skills/visual-preference/, small text files only: SKILL.md, manual.md, tokens.json, web/, figures/, latex/, marks/, templates/DESIGN.md.
- Not installed: dev/visual-preference/ (build script, tests, .pptx builder, README).
- Projects: web loads a pinned jsDelivr link; LaTeX and Python get copies from the skill, version noted at the top.
- Versions: tags visual-preference-vX.Y.Z; plugin version bumps too; each release attaches slide and poster .pptx built from the tokens.
- Claude's calls (approved): open-licence fonts on Google Fonts, no binary in repo; viewer re-synced at each release and read-only; skill fires for Yili's own projects only (not Woodwell repos, not KIMKIM); build runs locally, release via gh, no CI until needed.

## Stage 4: Written design (approved, 2026-11-25)
- Part A design in /mnt/user-data/outputs/visual-preference-design.md. Build plan moved to after stage 10.

## Stage 5: Taste (approved, 2026-11-25)
- Presence: professional and polished, good taste, not the cheap AI default; not loud, content first.
- Home theme: dark screen; light exists as secondary. No glow.
- Material: natural and earthy. Meaning: abstract (no literal Arctic, rock or Chinese imagery). Density: balanced.
- References: science editorial (Nature, The Economist graphics), field instruments (Arc'teryx, Leica), DJI, NASA, Apple, National Geographic.
- Avoid: emoji and sparkles; researched AI-default list (overused faces Inter/Roboto/Arial/Open Sans/Geist/Plus Jakarta/Space Grotesk/Fraunces; purple-blue gradients; glow on dark; gradient text; pure #000; side-bar accent cards; soft-shadow rounded card grids; glass as decoration; nested cards; icon-above-heading tiles; everything centred; uniform spacing; hero-metric layout; decorative sparklines; bouncy motion).
- Type: Albert Sans for text, interface and headings (user pick from 21 faces). Claude's calls (approved): Source Serif 4 headings only in long documents and editorial pages (papers, CV, essays); a monospace for code and numeric table columns because Albert Sans has no tabular figures (choose in stage 8).

## Stage 6: Principles and voice (delegated to Claude's professional judgement, 2026-11-25)
Principles, in priority order (a higher one wins a conflict):
1. Readable by everyone: text at WCAG AA contrast in both themes, colour never the only cue, colour-blind-safe palettes, works on a phone, reduced motion respected.
2. The work leads: the style frames content and never competes; maps, imagery and data carry the colour; the interface stays in earthy neutrals; every element earns its place.
3. Colour means something: the accent marks the one focus or action; data palettes mark data; nothing decorative, no gradient for show.
4. Editorial clarity: hierarchy from size, weight and space; few sizes with clear steps; text aligned left; captions, units and sources visible.
5. Built like an instrument: exact alignment, strict type and spacing scale, hairline rules, matte surfaces, numbers set precisely; no glow, glass or soft-shadow cards.
Scope note (manual intro, not a principle): the system decides critical choices; the rest is judgement.
Voice: no new voice; interface words follow Yili's existing plain-English writing rules (British spelling as in his repos).

## Stage 7: Direction "Stone and Signal" (approved, 2026-11-25)
- Shared ground for every project: green-grey stone dark, matte. Draft: ground #131512, surface #1a1d19, rule #333832, muted #9ca29a, ink #e5e8e1 (tune in stage 8).
- Accents rotate between projects, one per project, never mixed: lichen green #a3b86c (HOME: site, CV, papers, mark, default for new projects), signal orange #e2652f, amber #e0a84a. Each gets a darker twin for the light theme.
- Details everywhere: spaced capital labels, square corners, monospace numbers, hairline rules, no shadows, no glow.
- User liked all of 12 colourways' look generally; picked Moss, Signal, Spruce and amber; asked to rotate them between projects.

## Stage 8: Foundations (in progress)
- Monospace: IBM Plex Mono (numbers and code). Icons: Tabler (outline).
- Data colours round 1 (Okabe-Ito, Tol light, batlow, lapaz, viridis, vik, roma, berlin): user rejected all. Round 2 built: earthy categorical sets optimised for colour-blind distinctness in CAM02-UCS on the stone ground (K1 Earth 6 score 14.5; K2 Earth 8 10.4; K3 accent-led 6 11.9; Okabe-Ito scores 11.0), Crameri sequential (bamako, oslo, lajolla, bilbao, nuuk) plus a custom lichen ramp, Crameri diverging (vanimo, managua, lisbon dark-middle; broc, cork, bam light-middle).
- APPROVED stage 8 (2026-11-25). Dark: ground #131512, surface #1a1d19, raised #22261f, rule #333832, edge #6b7168, muted #9ca29a, ink #e5e8e1. Light: ground #f2f3ef, surface #e8eae4, raised #ffffff, rule #cfd3ca, edge #7f857a, muted #5b6158, ink #1a1d18. Accents dark/light: lichen #a3b86c/#566a26 (home), signal #e2652f/#b0441a, amber #e0a84a/#8a5d0c.
- Data: groups Earth 6 (sky #a9cfe6, rust #c4573a, spruce #4f9a7d, sand #d8c48e, dusk #8a7fb8, ochre #c9962e) + rose #d98ca0, olive #b0ac5a for 7-8 groups (Earth 8 set: glacier #86b2d4 replaces sky as first? -> use K2 order: glacier, rust, spruce, sand, dusk, rose, olive, sky). Sequential by meaning: bamako default, oslo ice/snow/water, lajolla heat/fire/intensity, bilbao soil/sediment, custom lichen ramp for small UI charts (verify lightness in stage 11). Diverging: lisbon dark pages, broc light pages.
- Type: Albert Sans 400/500/600; IBM Plex Mono numbers+code; Source Serif 4 document headings; Noto Sans SC for Chinese. Sizes 12 label,14,16 body,20,25,31,49. Labels caps +0.1em. LH 1.55 text, 1.15 headings. Max 68ch.
- Spacing 4,8,12,16,24,32,48,64,96. Corners 0; circles only for dots. No shadows; one functional shadow for panels over maps/imagery.
- Motion 120ms hover, 200ms panels, ease-out, no bounce, off for reduced motion. Focus 2px accent ring, 2px offset. Icons Tabler outline 1.5px.

## Stage 9: Mark (approved, 2026-11-25)
- Mark: the square full stop. One solid square in the accent; alone = favicon/avatar; after a name = full stop ("Yili Yang" + lichen square). Picked from 11 options (A).
- Project variants (Claude's call): projects end their name with the same square in their own accent; Yili's name always keeps the lichen square.
- Sizes (refine in build): square side 0.22 x type size, on baseline, gap 0.1 x size. Favicon: square on stone ground, 2px margin at 16px.
- Social preview 1280x640: spaced-capital kicker, name + accent stop, one-line purpose, hairline, "Yili Yang" + lichen stop, repo path in IBM Plex Mono.
- README top (Claude's call): app repos lead with the live preview image (auto-generate-preview-image rules); non-app repos lead with the social preview card; never both.

## Stage 10: Surface guides (approved, 2026-11-25)
Screens: web app/site dark default, light follows system; 68ch column, 1200px page; hairline sections not cards; one filled accent button per view, other actions underlined text; spaced capital labels. Map/data app: map fills window; dark matte stone-tinted basemap, muted labels; panels float on raised with the one functional shadow; data colour only from data palettes; accent marks selection/focus never data; every value number+unit+source. Desktop widget: compact 12-14px, mono numbers, no glass (solid surface 96%). README: top = live app image or social card for non-app repos; one sentence what it is, then install/use; images carry own stone ground; at most licence + one status badge.
Print/talks: figures light in papers (journal rules win), stone dark on web/slides; Albert text, Plex Mono ticks; no top/right spines, light y-grid; data palettes, at most one accent highlight; units on axes, source in caption. CV/letters/papers: paper ground; Source Serif 4 headings, Albert text, Plex Mono numbers; dark lichen #566a26 only for rules and the stop; pdfLaTeX fallback. Slides: dark default, light for handouts; one idea per slide, sentence titles, full-bleed figures; name+stop bottom left, mono slide number bottom right. Poster: light paper. Email: light; chart uses figure style.

## Part B design approved; build plan approved (2026-11-25)
- Plan: /mnt/user-data/outputs/visual-preference-plan.md. Execution: native (Claude builds every task in this session), one fresh reviewer at the end.
- Delivery: Yili grants this session write access to yi-li-yang/skills; Claude pushes a branch and opens a PR.

## Build notes (stage 11)
- Earth 8 = the whole K2 set (glacier, rust, spruce, sand, dusk, rose, olive, sky). K1 plus rose and olive measured 5.0, below the 10.0 an eight-colour set needs. Claude's call; for Yili's review in Task 9.
- Light-theme data colours, derived by dev/visual-preference/derive_light_data.py (hue within 20 degrees, chroma 0.7-1.6x, 3:1 to 6:1 on paper, Earth 6 >= 11.0 and Earth 8 >= 10.0 under colour-vision simulation). Claude's call; for Yili's review in Task 9:
  sky #48606e, rust #9c3f27, spruce #307f67, sand #9e8a59, dusk #72679f, ochre #9e7002, glacier #6490b0, rose #bc7387, olive #7a801b.

## Stage 13 review (2026-11-25)
- Yili asked for "more grey". Shown four levels (current; greyer neutrals; plus softer colour; plus muted colour) with their colour-blind cost. Yili picked B: greyer neutrals only (chroma x0.45 in CAM02-UCS); accents and data colours unchanged, so no accessibility cost.
  New neutrals dark/light: ground #141413/#f4f2f0, surface #1c1c1b/#ebe9e6, raised #242522/#ffffff, rule #363734/#d2d1cd, edge #6e6f6c/#82837f, muted #a0a09d/#5e5f5c, ink #e8e7e3/#1b1c1a.
