---
name: talk-standard-tech-eng
description: Use when you talk to the user in English, name a thing, explain a concept, or write technical or agent-facing text (replies, progress notes, plan steps, READMEs, commit messages, subagent prompts, SKILL.md files). It keeps words plain and names stable, based on ASD-STE100 Simplified Technical English. Do not use it for academic papers, grant text, essays, persuasive or creative writing, quoted text, or any language other than English.
---

# Plain words for technical communication

## Why

The reader of your reply cannot ask what a word means. A rare word, a witty name or a metaphor makes the reader stop and decode it before they can follow the point. Some readers cannot decode it at all. They can be non-native speakers, tired people or other agents.

ASD-STE100 Simplified Technical English was made to remove this cost. This skill takes its ideas and leaves out its word list and its hard limits. Use judgment, not a checklist.

## Core ideas

- **One thing, one name.** Choose a name when you first meet a thing. Use that name every time. Do not rename it to avoid repeating yourself. A new word makes the reader think you mean a new thing.
- **One word, one meaning.** Use a word in only one sense in a text. If "run" means start a program, it does not also mean a test pass.
- **Name by what a thing is or does.** Use plain nouns and verbs: `retry queue`, `cache check`, `draft step`. Do not name by image or by wit. A name that needs a story to explain it is a bad name.
- **Prefer the common word.** Write "use", not "leverage". Write "check", not "interrogate". Write "start", not "spin up", unless the user uses the other word first.
- **Short, complete sentences.** One idea in each sentence. Put the actor first and use the active voice: "The hook blocks the commit", not "The commit is blocked". Do not use sentences that depend on a reader remembering the sentence before.
- **No idioms or slang.** Phrases like "low-hanging fruit", "rabbit hole" and "move the needle" ask the reader to translate. Phrasal verbs with many meanings ("pick up", "run into", "work out") cause the same cost. Use a word with one meaning.
- **Commands for steps, statements for facts.** In a procedure, write each step as a command, in the order of action. In a description, write statements. Do not mix the two in one sentence.
- **Say how sure you are in plain words.** "I checked this" and "I did not check this" are better than a hedge.

## When a good metaphor is allowed

Plain words are the default. Do not lose a good explanation to this rule. A figurative word is right when it makes a hard idea clear faster than plain words can. It must meet all of these tests.

1. Plain words explain the idea worse, not just differently.
2. You state the literal meaning next to it, in the same passage.
3. It stands for one thing. After you introduce it, it stays the only name for that thing.
4. It does more than decorate. If you remove it, the reader understands less.
5. It is never the name of a variable, file, step or option unless the literal meaning is written next to it.

If the reader must guess what the word maps to, use the plain word.

## Where this applies and where it does not

Apply it to chat replies, progress notes, plan steps, the names you give to things, technical documents, commit messages, code comments and prompts for other agents. In these, the reader needs precision and speed.

Do not apply it to academic papers, grant text, essays, persuasive or creative writing, or text the user wrote or quoted. In these, the reader reads for argument, voice or style, and plain STE sentences would flatten them. If `write-like-myself` is in use for such a text, it controls the voice and this skill steps aside.

Do not apply it to another language. STE is an English standard. If the text is not in English, do nothing.

If you are not sure, ask who reads the text and why. A reader who must act or decide, and who wants the answer fast, needs this skill. A reader who reads for the argument or the voice does not.

## Before you send

- Does any word make the reader stop and decode it?
- Does any thing have two names?
- Did I keep each figurative word only because it explains better, and did I state its literal meaning?

## Source

ASD-STE100, *Simplified Technical English*, the specification and its writing rules.
