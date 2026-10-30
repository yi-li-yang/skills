# skills

The master repository for my Claude Code skills. One plugin (`plugins/yili-skills`) holds every skill; `dev/<skill>/` holds that skill's evals, research and tools, which are not installed.

- A skill lives in `plugins/yili-skills/skills/<name>/`. Keep development material out of that folder, because everything inside it is installed.
- Bump the version in both `plugins/yili-skills/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` when a skill changes, or installed copies will not update.
- `.githooks/` holds a privacy guard that blocks private writing material from commits and pushes. Run `git config core.hooksPath .githooks` in a new clone. It needs `dev/write-like-myself/tools/local.toml`, which is not committed; without it only the pattern and path rules run.
- Every skill's README is at `dev/<skill>/README.md`.
