# Interview Before Answer

A stance for questions where the right answer depends on what I value and how I decide. Claude first learns how I think about the domain (from memory, files and past decisions, and by interviewing me where that is not enough), then answers through that lens with the rigour of an expert, then argues against its own answer from the view of the field's masters, its first principles, and how such decisions usually fail.

It works in any domain. It carries no domain content: it teaches the agent how to map a new domain (purpose, decision model, hinges, limits, logistics) before it asks anything.

## Install

This skill ships inside the `yili-skills` plugin. Install the plugin, not the skill alone. The steps for Claude Code and for claude.ai are in the [repository README](../../README.md).

### Fallback: upload this one skill by hand

Only if you cannot add a marketplace. An uploaded copy does not update when the repository does, and it competes with the plugin's copy for the skill listing, so remove one of the two.

1. Build `interview-before-answer.skill` by zipping the skill folder, with the folder as the top level of the zip: `cd plugins/yili-skills/skills && zip -r interview-before-answer.skill interview-before-answer`.
2. In claude.ai, go to **Sidebar → Customize → Skills**, upload the file, and toggle it on. If a copy named `interview-before-answer` is already there, replace it.
