# skills

The master repository for my Claude Code skills. One plugin (`plugins/yili-skills`) holds every skill; `dev/<skill>/` holds that skill's evals, research and tools, which are not installed.

- Write each skill as a way of thinking, not as rules, checklists or thresholds. A rule misses the case nobody expected and goes stale; the reasoning behind it still applies to a new case.
- Write skills in plain English, using the ideas of ASD-STE100 Simplified Technical English as `talk-standard-tech-eng` describes them, not the standard's word list or limits. A skill's words become Claude's words when it talks to me, and a model reads a skill literally, so give each thing one name and each word one meaning. Keep the reasoning connected. Keep trigger phrases, terms of art, non-English text, and any metaphor that explains better than plain words.
- Each skill answers one question about how I think, and no two skills answer the same one. A skill states what it needs as a question, at the moment and under the condition it arises, and never names another skill; Claude finds the skill that answers it from the descriptions. Each skill body opens with a `**Takes:**` line and a `**Returns:**` line. `python -m pytest dev` checks this.
- A skill lives in `plugins/yili-skills/skills/<name>/`. Keep development material out of that folder, because everything inside it is installed.
- Bump the version in both `plugins/yili-skills/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` when a skill changes, or installed copies will not update.
- `.githooks/` holds a privacy guard that blocks private writing material from commits and pushes. Run `git config core.hooksPath .githooks` in a new clone. It needs `dev/write-like-myself/tools/local.toml`, which is not committed; without it only the pattern and path rules run.
- Every skill's README is at `dev/<skill>/README.md`.
