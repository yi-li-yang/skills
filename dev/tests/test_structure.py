"""Check the shape of the installed skills, so that a rename or a stray reference fails before a commit.

The skills find each other by the question each one answers, never by name (see CLAUDE.md). A skill that
names another skill is wired to it: a rename or a removal then breaks it, and a second skill that answers the
same question is never found. These tests keep the wiring out, and check what a skill needs to load at all.

    python -m pytest dev/tests
"""
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PLUGIN = REPO / "plugins" / "yili-skills"
SKILLS = PLUGIN / "skills"
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")  # the Agent Skills specification
LOCAL_FILE = re.compile(r"(?<![\w/.-])((?:references|templates|scripts)/[\w.-]+)")


def parse(skill_md):
    """Split a SKILL.md into its frontmatter fields and its body. Handles plain and folded (>-) values."""
    text = skill_md.read_text(encoding="utf-8").replace("\r\n", "\n")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not match:
        raise AssertionError(f"{skill_md}: no frontmatter")
    fields, key = {}, None
    for line in match.group(1).splitlines():
        top = re.match(r"^([\w-]+):\s*(.*)$", line)
        if top:
            key, value = top.groups()
            fields[key] = "" if value in (">-", ">", "|", "|-") else value.strip()
        elif key and line.startswith(" "):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields, match.group(2)


def skill_folders():
    return sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())


def installed_text(folder):
    """All text a skill installs: its description and every Markdown file in its folder."""
    fields, _ = parse(folder / "SKILL.md")
    texts = [fields.get("description", "")]
    texts += [p.read_text(encoding="utf-8") for p in sorted(folder.rglob("*.md"))]
    return "\n".join(texts)


def mentions(text, name):
    """True if the text refers to the skill by name.

    A hyphenated name never occurs as ordinary English, so any whole-token use counts. A one-word name such as
    'wardrobe' is also an ordinary word, so only a use that reads as a reference counts: in backticks, after a
    slash, or after the plugin's prefix.
    """
    if "-" in name:
        return re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", text) is not None
    return re.search(rf"`{re.escape(name)}`|/{re.escape(name)}\b|yili-skills:{re.escape(name)}\b", text) is not None


class SkillShape(unittest.TestCase):
    def test_there_are_skills(self):
        self.assertTrue(skill_folders(), f"no skills found under {SKILLS}")

    def test_name_matches_folder_and_spec(self):
        for folder in skill_folders():
            name = parse(folder / "SKILL.md")[0].get("name", "")
            with self.subTest(skill=folder.name):
                self.assertEqual(name, folder.name, "the name: line must match the folder")
                self.assertRegex(name, NAME, "lowercase letters, digits and single hyphens only")
                self.assertLessEqual(len(name), 64)

    def test_description_exists_and_fits(self):
        for folder in skill_folders():
            description = parse(folder / "SKILL.md")[0].get("description", "")
            with self.subTest(skill=folder.name):
                self.assertTrue(description, "the description is how the skill is found")
                self.assertLessEqual(len(description), 1024, "the Agent Skills limit")

    def test_contract_comes_first(self):
        """The body opens with what the skill takes and what it returns, before its first section."""
        for folder in skill_folders():
            body = parse(folder / "SKILL.md")[1]
            head = body.split("\n## ", 1)[0]
            with self.subTest(skill=folder.name):
                self.assertRegex(head, r"(?m)^\*\*Takes:\*\* \S", "no **Takes:** line before the first section")
                self.assertRegex(head, r"(?m)^\*\*Returns:\*\* \S", "no **Returns:** line before the first section")

    def test_no_skill_names_another(self):
        """A need is stated as a question. Naming another skill wires the two together."""
        names = [folder.name for folder in skill_folders()]
        for folder in skill_folders():
            text = installed_text(folder)
            for other in names:
                if other == folder.name:
                    continue
                with self.subTest(skill=folder.name, names=other):
                    self.assertFalse(mentions(text, other),
                                     f"{folder.name} names {other}; state the question it needs answered instead")

    def test_local_files_exist(self):
        """Every references/, templates/ or scripts/ path a skill mentions is installed with it."""
        for folder in skill_folders():
            for md in sorted(folder.rglob("*.md")):
                for path in LOCAL_FILE.findall(md.read_text(encoding="utf-8")):
                    with self.subTest(skill=folder.name, file=md.name, path=path):
                        self.assertTrue((folder / path).exists(), f"{path} is mentioned but not in {folder.name}/")

    def test_every_skill_has_a_dev_readme(self):
        for folder in skill_folders():
            with self.subTest(skill=folder.name):
                self.assertTrue((REPO / "dev" / folder.name / "README.md").is_file())


class Manifests(unittest.TestCase):
    def test_versions_match(self):
        """Installed copies update only when the version changes, and both manifests must carry it."""
        plugin = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        market = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        versions = {plugin["version"], market["metadata"]["version"], market["plugins"][0]["version"]}
        self.assertEqual(len(versions), 1, f"versions differ: {versions}")


if __name__ == "__main__":
    unittest.main()
