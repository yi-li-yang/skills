# Interview Me Before Answer

A stance for questions where the right answer depends on what I value and how I decide. Claude first learns how I think about the domain (from memory, files and past decisions, and by interviewing me where that is not enough), then answers through that lens with the rigour of an expert, then argues against its own answer from the view of the field's masters, its first principles, and how such decisions usually fail.

It works in any domain. It carries no domain content: it teaches the agent how to map a new domain (purpose, decision model, hinges, limits, logistics) before it asks anything.

## When it runs, and when it asks

Claude decides when to use it. The test is whether knowing me better would change the answer. When it runs, the reply opens with a status line that names the domain, what Claude believes about how I think there, the stake, and what it decided:

```
🎙 interview-me-before-answer · domain: … · lens: … · stake: … · so: asking first | answering, guess named
```

The stake decides whether it asks. When little rides on the answer, it answers and names its guess about me, so I can correct it in a word. When much rides on it, when it cannot be undone, or when it knows nothing of how I think in that domain, it asks first and does not answer in the same reply. If I disagree with the lens or the stake, I say so and it changes course. To force it, type `/interview-me-before-answer`, or say "interview me first".

Test prompts are in [evals/prompts.md](evals/prompts.md).

## Install

This skill ships inside the `yili-skills` plugin. Install the plugin, not the skill alone. The steps for Claude Code and for claude.ai are in the [repository README](../../README.md).

### Fallback: upload this one skill by hand

Only if you cannot add a marketplace. An uploaded copy does not update when the repository does, and it competes with the plugin's copy for the skill listing, so remove one of the two.

1. Build `interview-me-before-answer.skill` by zipping the skill folder, with the folder as the top level of the zip: `cd plugins/yili-skills/skills && zip -r interview-me-before-answer.skill interview-me-before-answer`.
2. In claude.ai, go to **Sidebar → Customize → Skills**, upload the file, and toggle it on. If a copy named `interview-me-before-answer` is already there, replace it.
