# skills

My Claude Code skills in one repository. Install once, and every skill is available; update once, and every skill updates.

## Skills

| Skill | What it does | Fires when |
| --- | --- | --- |
| [prompt-to-think](plugins/yili-skills/skills/prompt-to-think/SKILL.md) | A thinking framework: intellectual honesty, first principles, inversion, anti-fragility, taste. | Tackling a hard problem, checking assumptions, or shaping an answer that matters. |
| [write-like-myself](plugins/yili-skills/skills/write-like-myself/SKILL.md) | Writes the way I would, built on how readers read rather than on lists of rules. | Writing or editing any text a person will read. |
| [talk-standard-tech-eng](plugins/yili-skills/skills/talk-standard-tech-eng/SKILL.md) | Keeps Claude's English plain and its names stable, using the ideas of ASD-STE100, and keeps a good metaphor when it explains better. | Claude talks to me, names a thing, or writes technical or agent-facing text. Not for academic, persuasive or creative writing, or other languages. |
| [expertise](plugins/yili-skills/skills/expertise/SKILL.md) | Brings Claude up to date on a topic with parallel research agents and saves a sourced, dated briefing. | Working on something that has moved since training, or `/expertise <topic>`. |
| [research-before-buy](plugins/yili-skills/skills/research-before-buy/SKILL.md) | Runs the research, compare and find loop for a non-trivial purchase. | Deciding what to buy or how, when the choice is hard. |
| [interview-before-answer](plugins/yili-skills/skills/interview-before-answer/SKILL.md) | Learns how I think about a domain, interviewing me if needed, answers through that lens with expert rigour, then argues against the answer from the masters' view. | A question, decision or task where my own judgment matters. Not for facts or lookups. |
| [wardrobe](plugins/yili-skills/skills/wardrobe/SKILL.md) | Judges a clothing buy against the person's colouring, body and what they already own: colour, outfits it makes, where the hem falls, material, cost per wear. | Deciding whether to buy a piece of clothing, shoes, a bag or jewellery, or what goes with something owned. |

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
.githooks/                          privacy guard for write-like-myself, see dev/write-like-myself
```

## Add a skill

1. Create `plugins/yili-skills/skills/<name>/SKILL.md` with `name` and `description` in the frontmatter. The description is what makes it fire, so say when to use it and when not to.
2. Put anything that is not part of the skill itself (evals, research, scripts for development) in `dev/<name>/`, so it is not installed.
3. Add a row to the table above.
4. Bump `version` in `plugins/yili-skills/.claude-plugin/plugin.json` and in `.claude-plugin/marketplace.json`. Installed copies only update when the version changes.
5. Run `git config core.hooksPath .githooks` once per clone, so the privacy guard runs. New skills are checked by it until they are listed in `UNGUARDED` in `dev/write-like-myself/tools/guard.py`.

## History

Each skill began in its own repository, and its full history was imported under `dev/<skill>/`: [prompt-to-think](https://github.com/yi-li-yang/prompt-to-think), [write-like-myself](https://github.com/yi-li-yang/write-like-myself), [deep-research](https://github.com/yi-li-yang/deep-research) (now `expertise`) and [research-before-buy](https://github.com/yi-li-yang/research-before-buy). Those repositories now point here and are no longer updated.

## Licence

MIT.
