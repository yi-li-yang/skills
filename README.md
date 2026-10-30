# skills

My Claude Code skills in one repository. Install once, and every skill is available; update once, and every skill updates.

## Skills

| Skill | What it does | Fires when |
| --- | --- | --- |
| [prompt-to-think](plugins/yili-skills/skills/prompt-to-think/SKILL.md) | A thinking framework: intellectual honesty, first principles, inversion, anti-fragility, taste. | Tackling a hard problem, checking assumptions, or shaping an answer that matters. |
| [write-like-myself](plugins/yili-skills/skills/write-like-myself/SKILL.md) | Writes the way I would, built on how readers read rather than on lists of rules. | Writing or editing any text a person will read. |
| [expertise](plugins/yili-skills/skills/expertise/SKILL.md) | Brings Claude up to date on a topic with parallel research agents and saves a sourced, dated briefing. | Working on something that has moved since training, or `/expertise <topic>`. |
| [research-before-buy](plugins/yili-skills/skills/research-before-buy/SKILL.md) | Runs the research, compare and find loop for a non-trivial purchase. | Deciding what to buy or how, when the choice is hard. |

## Install

```
/plugin marketplace add yi-li-yang/skills
/plugin install yili-skills@yili-skills
```

## Update

```
/plugin marketplace update yili-skills
```

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
