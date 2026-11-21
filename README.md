# skills

My Claude Code skills in one repository. Install once, and every skill is available; update once, and every skill updates.

## How the skills are written

This is a personal set of ways to think through different parts of my life and work. Each skill describes a way of thinking and does not set rules. A rule is hard: it misses the case nobody expected, and it goes out of date. A way of thinking still applies to a case it has not seen, so each skill gives its reasoning and leaves the judgment to Claude.

The skills are written in plain English, based on the ideas of ASD-STE100 Simplified Technical English (see [talk-standard-tech-eng](plugins/yili-skills/skills/talk-standard-tech-eng/SKILL.md)). Claude reads a skill literally and then uses its words when it talks to me. So each thing has one name, each word has one meaning, and a metaphor stays only when it explains better than plain words.

## Skills

Each skill answers one question about how I think, and no two skills answer the same one.

| Skill | The question it answers | Fires when |
| --- | --- | --- |
| [i-think-like-this](plugins/yili-skills/skills/i-think-like-this/SKILL.md) | How do I reason, and how do I judge what is true, including what I am told? | A hard problem, an answer that matters, a claim to judge before believing it, or a decision that could fail. |
| [interview-me-before-answer](plugins/yili-skills/skills/interview-me-before-answer/SKILL.md) | Who is asking, and how do they decide? | A question, decision or task where my own judgment matters. Not for facts or lookups. |
| [updated-domain-expert](plugins/yili-skills/skills/updated-domain-expert/SKILL.md) | What does an expert in this field know now? Saves a sourced, dated briefing. | Working on something that has moved since training, or `/yili-skills:updated-domain-expert <topic>`. |
| [digest-distill-information](plugins/yili-skills/skills/digest-distill-information/SKILL.md) | What does the actual material say and show: review videos, owner posts and photos, comment threads, reports, pages that need a browser, in any language? | An answer depends on real material that a search snippet cannot hold. |
| [research-before-buy](plugins/yili-skills/skills/research-before-buy/SKILL.md) | How do I decide a purchase? | Deciding what to buy or how, when the choice is hard. |
| [wardrobe](plugins/yili-skills/skills/wardrobe/SKILL.md) | What is this piece made of, how well is it made, how does it fit me, and what do I already own like it? It keeps my wardrobe record; taste stays mine. | Recording clothes I own, looking at a piece of clothing, shoes, a bag or jewellery, or asking about a fabric, a make or a brand. |
| [write-like-myself](plugins/yili-skills/skills/write-like-myself/SKILL.md) | How do my words read when I write? | Writing or editing any text a person will read. |
| [talk-standard-tech-eng](plugins/yili-skills/skills/talk-standard-tech-eng/SKILL.md) | How do Claude's technical words stay plain? | Claude talks to me, names a thing, or writes technical or agent-facing text. Not for academic, persuasive or creative writing, or other languages. |

Version 2.0.0 renamed three skills: `prompt-to-think` is now `i-think-like-this`, `interview-before-answer` is now `interview-me-before-answer`, and `expertise` is now `updated-domain-expert`.

## How the skills find each other

No skill names another skill, and none ranks above another. When a skill reaches a point where it needs a different question answered, it asks that question in plain words, at that moment and only when its condition holds. For example, `research-before-buy` asks *how does this person decide here?* only when the call depends on what I value and nothing on record says it. Such questions are written in italics, and a skill that asks them says once, near its top, to check whether another skill answers them. Claude sees every skill's description all the time, so it finds the skill that answers the question. This is how I work too: when I am deciding a purchase and start to wonder what a fabric is really worth, I just ask that other question.

Four properties keep this robust:

1. **A need is a question, not a name.** A rename, a new skill or a removed skill breaks nothing. Whichever installed skill answers the question takes it; if none does, Claude answers it itself.
2. **Orthogonality makes the match exact.** Each question has one skill that answers it, so a need never matches two skills.
3. **The description is the interface.** Each description says when its question arises, and each skill body opens with what it takes and what it returns. When a need misses its skill, the fix goes into the description of the skill that should have answered, never into the skill that asked.
4. **Every connection is soft, and none can loop.** A skill adds my way of thinking; it is never the only path to an answer, so a missed match gives an answer that is less like me but still correct. A question already being answered in a conversation is not asked again, so two skills can each need the other once.

Two checks keep it true: `dev/tests/test_structure.py` fails if a skill names another one or lacks its contract, and `dev/routing/run.py` checks from outside that each need loads the skill that answers it.

## Install

**Claude Code**

```
/plugin marketplace add yi-li-yang/skills
/plugin install yili-skills@yili-skills
```

**claude.ai**: open **Customize → Plugins → Add marketplace**, enter `yi-li-yang/skills`, then install `yili-skills`. Per [Anthropic's Cowork documentation](https://claude.com/docs/cowork/guide/plugins), a plugin you install is saved to your account, so its skills are also available in chat and in Claude Code. If you uploaded one of these skills by hand earlier, remove that copy so it does not compete with the plugin's.

## Update

**Claude Code**

```
/plugin marketplace update yili-skills
```

**claude.ai**: on the marketplace, select **Check for updates**, or turn on **Sync automatically**.

All skills come in one plugin, so one update refreshes them all. Each skill still fires on its own from its description; to call one by hand, use `/yili-skills:<skill>`.

## Layout

```
.claude-plugin/marketplace.json     the marketplace: one plugin
plugins/yili-skills/                the plugin that gets installed
  .claude-plugin/plugin.json
  skills/<skill>/SKILL.md           one folder per skill
dev/<skill>/                        evals, research, tools and notes; never installed
dev/tests/                          structure test for every skill
dev/routing/                        routing eval: does each need find its skill?
.githooks/                          privacy guard for write-like-myself, see dev/write-like-myself
```

## Add a skill

1. Decide the one question the skill answers, and check that no other skill answers it.
2. Create `plugins/yili-skills/skills/<name>/SKILL.md` with `name` and `description` in the frontmatter. The description is what makes it fire, so say when its question arises and when not to use it, not how it works. Open the body with a `**Takes:**` line and a `**Returns:**` line.
3. Where the skill needs another question answered, ask the question in plain words. Never name another skill.
4. Put anything that is not part of the skill itself (evals, research, scripts for development) in `dev/<name>/`, with a `README.md`, so it is not installed.
5. Add a row to the table above, add a case to `dev/routing/cases.json`, and run `python -m pytest dev`.
6. Bump `version` in `plugins/yili-skills/.claude-plugin/plugin.json` and in `.claude-plugin/marketplace.json`. Installed copies only update when the version changes.
7. Run `git config core.hooksPath .githooks` once per clone, so the privacy guard runs. New skills are checked by it until they are listed in `UNGUARDED` in `dev/write-like-myself/tools/guard.py`.

## History

Each skill began in its own repository, and its full history was imported under `dev/<skill>/`: [prompt-to-think](https://github.com/yi-li-yang/prompt-to-think) (now `i-think-like-this`), [write-like-myself](https://github.com/yi-li-yang/write-like-myself), [deep-research](https://github.com/yi-li-yang/deep-research) (later `expertise`, now `updated-domain-expert`) and [research-before-buy](https://github.com/yi-li-yang/research-before-buy). Those repositories now point here and are no longer updated.

## Licence

MIT.
