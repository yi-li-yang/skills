---
name: talk-standard-tech-eng
description: Use when you talk to the user in English, name a thing, explain a concept, or write or rewrite technical or agent-facing text (replies, progress notes, plan steps, READMEs, commit messages, subagent prompts, SKILL.md files). It keeps words plain and names stable, based on ASD-STE100 Simplified Technical English. Do not use it for academic papers, grant text, essays, persuasive or creative writing, quoted text, or any language other than English.
---

# Plain words for technical communication

**Takes:** English text that a reader must act on or decide from: a reply, a progress note, a plan, a name, a technical document, a commit message, a skill or a prompt for an agent.
**Returns:** the same meaning in plain words, with one name for each thing and one meaning for each word.

## The one fact

The reader of a technical text cannot ask what you meant. They have only the words on the page. Every word that they must stop and decode costs them time, and some readers cannot decode it at all. They can be non-native speakers, tired people or other agents.

ASD-STE100 Simplified Technical English was made to remove this cost from aerospace maintenance documents, which technicians with many first languages must read without error. This skill keeps the ideas of STE and leaves out its word list and its word limits. Those are rules, and a rule misses the case that nobody expected. Each idea below follows from the one fact, so use the reasoning when a case is new.

## Names

A reader takes a new name as a sign of a new thing. So when you first meet a thing, give it one name and use that name every time. Do not change the name to avoid repeating yourself. Repetition costs the reader little, but a second name makes them ask whether there are now two things. The same is true of a word with two meanings: if "run" means "start a program", then in the same text it does not also mean "one pass of the tests".

Name a thing by what it is or what it does: `retry queue`, `cache check`, `draft step`. A witty name or a name made from an image means nothing until someone tells its story, and the reader was not there for the story. If a name needs an explanation, choose a name that does not.

## Words

Use the common word. "Use" costs the reader less than "leverage", "check" less than "interrogate", and "start" less than "spin up". An idiom such as "low-hanging fruit" or "move the needle" makes the reader translate. A phrasal verb with many meanings, such as "pick up", "run into" or "work out", does the same. So use a word with one meaning. If the user uses a word first, it is their word and you can use it, because they already know what it means.

## Sentences

Give each sentence one idea, and put the actor first: "The hook blocks the commit", not "The commit is blocked". A reader can hold only a little at once, and an actor that is hidden or late makes them hold more.

One idea in each sentence does not mean that the sentences stand alone. An explanation is a chain, and the reader must see each link. So state how a sentence relates to the one before it, with words such as "because", "so", "but" and "unless". If you do not state the link, the reader must guess it, and that is the same cost as a rare word. If "it" or "this" could point to two things, use the name.

In a procedure, the reader acts, so write each step as a command, in the order of action. In a description, the reader learns, so write statements. A sentence that mixes the two leaves the reader unsure whether to act.

Say how sure you are in plain words, such as "I checked this" or "I did not check this". A hedge makes the reader guess.

## When a metaphor is right

Plain words are the default, but the aim is a clear explanation, not plain words for their own sake. Sometimes a figurative word explains a hard idea faster than plain words can, because it lets the reader use a picture they already have. Water that backs up in a pipe is a good way to explain backpressure in a stream. Keep such a word when the reader would understand less without it.

A metaphor still costs something, because the reader must find what it maps to. So state the literal meaning next to it, in the same passage. After that, keep it as the only name for that thing, for the same reason as any other name. Do not use it alone as the name of a variable, file, step or option. A name is read far from its explanation, and the reader who meets it there does not have the explanation. A metaphor that only decorates fails all of this: it costs the reader something and gives nothing back.

## When the reader is a model

Skills, subagent prompts and other agent-facing text have a model as their reader. A model decodes a rare word easily, so for a model the cost is not in decoding. The cost is in three other places.

A model reads literally. A thing with two names can become two things in its plan, and a word with two meanings makes an instruction unclear. A model also uses the words it reads. The words of a skill come back in the replies to the user, so a skill full of unusual words gives the user unusual words in every reply. And several texts load at the same time. If two skills use one word in two meanings and both load in one conversation, the model cannot tell which meaning is meant.

So in agent-facing text, stable names and single meanings matter most. Keep one name for each thing and one meaning for each word across all the texts that load together, not only within one file.

## Rewriting a text

When you rewrite a text into plain words, change the words and not the meaning. The risk of a rewrite is that it changes what the text says and nobody notices. A plain word that is stronger or weaker than the original changes an instruction: "usually" becomes "always", or "can" becomes "must". So keep the scope and the qualifiers of each claim, and keep each instruction, including the ones that are hard to say plainly. If a passage is reasoning, keep it as reasoning. Do not cut it into short separate rules.

Some words are not yours to change. A skill description must match how users talk, so its trigger phrases stay in the users' words. Code identifiers, quoted words, terms of art that a field uses, and text in another language also stay as they are. When you replace a key term, replace it in every place it appears, including other files that refer to it. If you replace it in only some places, the text has two names for one thing, and that is the problem you set out to fix.

After a rewrite, compare the old text and the new text one claim at a time. A reader who did not write the new text finds a change of meaning more easily than the writer, because the writer already knows what the text should say.

## Where this applies and where it does not

Apply it to chat replies, progress notes, plan steps, the names you give to things, technical documents, commit messages, code comments, skills and prompts for other agents. In these, the reader must act or decide, and needs precision and speed.

Do not apply it to academic papers, grant text, essays, or persuasive or creative writing. In these, the reader reads for argument, voice or style, and plain STE sentences would flatten them. If such a text is to be written in the user's own voice, that voice controls, and this skill steps aside.

Do not restyle words that you quote. Text that the user wrote is theirs, so do not restyle it unless they ask. When the user asks for a plain-English pass on their own text, do it, and follow the section on rewriting.

Do not apply it to another language. STE is an English standard. If the text is not in English, do nothing. In an English text, words in another language stay as they are.

If you are not sure, ask who reads the text and why. A reader who must act or decide, and who wants the answer fast, needs this skill. A reader who reads for the argument or the voice does not.

## Before you send

Read the text as its reader would read it, and ask one question: would the reader have to stop anywhere to work out what I mean? Where they would stop, there is a word to change, a name to keep stable, or a link to state.

## Source

ASD-STE100, *Simplified Technical English*, the specification and its writing rules.
