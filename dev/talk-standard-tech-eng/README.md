# talk-standard-tech-eng

This skill makes Claude use plain, stable English when it talks to me and when it writes technical or agent-facing text. Claude Code often names things and explains ideas with rare, odd or metaphorical words, and I have to decode them. The skill takes the ideas of ASD-STE100 Simplified Technical English and applies them where they help.

## How it works

The skill keeps the ideas of STE and drops its word list and hard limits. It starts from one fact: the reader cannot ask what you meant. The main ideas follow from it. They are one name for each thing, one meaning for each word, common words, no idioms, one idea in each sentence with the link to the sentence before stated, and commands for steps. The skill gives the reasoning for each idea, not a checklist, so it still applies to a case it does not mention.

It keeps room for a good metaphor. A figurative word is allowed when plain words explain the idea worse. Its literal meaning is stated next to it, and it then stays the only name for that thing. It is never the name of a variable, file or step on its own.

When the reader is a model, the cost is not in decoding a rare word. A model reads names literally, it uses the words it reads in its replies, and several skills load at the same time. So in skills and agent prompts, stable names and single meanings matter most, across all the texts that load together.

When Claude rewrites a text into plain words, the skill tells it to change the words and not the meaning. Qualifiers, trigger phrases, code identifiers, quoted words, terms of art and non-English text stay. A replaced term is replaced in every file.

This repository uses the skill for every skill it holds. The rule is in [CLAUDE.md](../../CLAUDE.md).

It applies to chat replies, plan steps, names, technical documents, commit messages, skills and prompts for other agents. It does not apply to academic papers, grant text, essays, persuasive or creative writing, quoted text, or any language other than English. For those texts, [write-like-myself](../write-like-myself/README.md) sets the voice.

## Install

The skill is part of the `yili-skills` plugin. See the [repository README](../../README.md) for the install commands. To use it with another agent, give it the file [SKILL.md](../../plugins/yili-skills/skills/talk-standard-tech-eng/SKILL.md) as instructions.

## Testing

The folder [evals](evals/) holds the test prompts. Each prompt is run with and without the skill, and the two outputs are compared. The tests check eight things: stable names, metaphor use, metaphor preservation, exclusion of academic and persuasive text, agent-facing prompts, non-English text, rewriting without a change of meaning, and stable names across prompts that run together.

## Licence

MIT.
