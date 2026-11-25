# visual-preference

The skill that holds how Yili's own work looks. It covers his repos, site, apps, figures, CV, papers, slides and posters. The installed folder, `plugins/yili-skills/skills/visual-preference/`, holds small text files only: the skill, the manual, the token source, and the files built from it.

- `design.md`: the design, which records why each choice was made and who made it.
- `decisions.md`: the working record of each stage of the design conversation.
- `plan.md`: the build plan.

## Build

Two files are hand-owned: `tokens.json` and `colormaps.json`. Every other file under `web/`, `figures/`, `latex/`, `marks/` and `templates/` is built from them, and its first line says so. Do not edit a built file. Edit the source, then rebuild.

```sh
pip install -r dev/visual-preference/requirements.txt
python dev/visual-preference/build.py          # rebuild the generated files
python dev/visual-preference/build.py --check  # fail if a generated file is stale
python -m pytest dev                           # all tests, the repository's own included
```

The slide and poster templates are `.pptx` files. They are built for each release and attached to it, never committed:

```sh
python dev/visual-preference/build_pptx.py     # writes dev/visual-preference/build/
```

## Release

1. Change `meta.version` in `tokens.json`, rebuild, and bump the plugin version in both manifests.
2. Merge, then tag the merge commit `visual-preference-vX.Y.Z` and push the tag.
3. `gh release create visual-preference-vX.Y.Z dev/visual-preference/build/*.pptx --notes-file dev/visual-preference/CHANGELOG.md`
4. Check that the jsDelivr link for `web/tokens.css` at the new tag answers.
5. Sync the Design System viewer from the repository.
