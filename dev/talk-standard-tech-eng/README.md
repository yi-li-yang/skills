# talk-standard-tech-eng

This skill makes Claude use plain, stable English when it talks to me and when it writes technical or agent-facing text. Claude Code often names things and explains ideas with rare, odd or metaphorical words, and I have to decode them. The skill takes the ideas of ASD-STE100 Simplified Technical English and applies them where they help.

## How it works

The skill keeps the ideas of STE and drops its word list and hard limits. The main ideas are one name for each thing, one meaning for each word, short complete sentences, no idioms, and commands for steps.

It keeps room for a good metaphor. A figurative word is allowed when plain words explain the idea worse, when the literal meaning is stated next to it, and when it then stays the only name for that thing. It is never the name of a variable, file or step on its own.

It applies to chat replies, plan steps, names, technical documents, commit messages and prompts for other agents. It does not apply to academic papers, grant text, essays, persuasive or creative writing, quoted text, or any language other than English. For those texts, [write-like-myself](../write-like-myself/README.md) sets the voice.

## Install

The skill is part of the `yili-skills` plugin. See the [repository README](../../README.md) for the install commands. To use it with another agent, give it the file [SKILL.md](../../plugins/yili-skills/skills/talk-standard-tech-eng/SKILL.md) as instructions.

## Testing

The folder [evals](evals/) holds the test prompts. Each prompt is run with and without the skill, and the two outputs are compared. The tests check six things: stable names, metaphor use, metaphor preservation, exclusion of academic and persuasive text, agent-facing prompts, and non-English text.

## Licence

MIT.
