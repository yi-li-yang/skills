---
name: visual-preference
description: >-
  Use when making, styling or restyling how Yili Yang's own projects look: his repos and READMEs, his site, web apps, maps and dashboards, his scientific figures, CV, letters, papers, slides and posters. Also use when another task needs to know how his work should look: colours, type, the mark, or the style of a chart. Not for Woodwell organisation repos or KIMKIM work, which belong to others and keep their own look.
---

# How Yili's work looks

**Takes:** a project of Yili's own and the surface to style (a new or existing repo, a page, an app, a map, a figure, a document, a talk), or a question about how his work should look.
**Returns:** the surface styled with his visual system: the files linked or copied at a stated version, one accent chosen for the project, a `DESIGN.md` for the project, and a short note of the choices made, with every choice the system did not decide marked as judgement.

Some steps below ask a question that this skill does not answer itself, written in italics, such as *how do my words read?* When you reach one and its condition holds, check whether one of your skills answers that question. If one does, load it and use its answer. If none does, answer the question yourself.

## What the system is

Yili chose his visual system himself, one stage at a time, from options he was shown. Before it existed, each of his projects borrowed another company's look. The system exists so that his work looks like his, and so that no project starts from a blank page again.

The system decides the critical choices only: the stone ground, the accent, the type, the data colours and the mark. Everything else is judgement, and the five principles in `manual.md` guide it. Read the manual before styling anything. It gives each value with its reason, and the reason is what lets a choice carry over to a case the manual does not cover.

The values live in `tokens.json`. The files that projects use are built from it, and each names its version in its first line. Use these files. Do not retype a value from the manual into a project, because a retyped value no longer follows the system when it changes.

## Applying it

**A new project.** Choose its accent: lichen, unless the manual's reasons point to signal or amber. Copy the `DESIGN.md` template for that accent into the project, so that any design tool starts from the system and not from its own defaults. Link or copy the files that the project's surfaces need, as "Using the files" in the manual describes, at the current tag. Then build the surface the way its section in the manual describes.

**An existing project.** First look at what it already has, and why. Replace the look that it borrowed or that a tool invented: its typefaces, neutrals, corners, shadows and accent. Keep what carries meaning, such as a score scale that a reader has learned, when it meets the first principle. Change one surface at a time, and check each one in both themes before moving on.

**A figure, a document or a talk.** Use the figure style, the LaTeX style or the slide template. A journal's own rules win over the system in a paper.

**Words.** Interface text, labels and README text follow Yili's own way of writing, not a separate voice. For the words, ask *how do my words read?*

## When the system does not say

A surface or a case that the manual does not cover still has an answer. Reason from the principles in their order: readable by everyone; the work leads; colour means something; editorial clarity; built like an instrument. Choose the plainest option that meets them. Then say, in the note you return, which choices were judgement, so that Yili can confirm them or add them to the system.

When the system and a request disagree (a second accent, a new colour, a shadow on a card), say which principle the request breaks and what it would cost, then do what Yili decides. He owns the taste; the system only records it.

## Checking the result

Before calling a surface done, look at it rendered, in both themes where it has two. Check that the text reads at AA contrast, that colour is never the only cue, that the accent marks exactly one thing per view, and that no number shifts as it changes. Look also for the patterns the manual lists under "What the system avoids, and why". A surface that looks like a default has drifted from the system.
