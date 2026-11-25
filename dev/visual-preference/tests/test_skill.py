"""The skill and its manual point only at files that exist, and quote only colours the tokens hold."""
import json
import re

import build
from test_structure import parse  # the repository's own SKILL.md parser

PATH = re.compile(r"(?<![\w/.-])((?:web|figures|latex|marks|templates)/[\w.-]+|tokens\.json|colormaps\.json)")
HEX = re.compile(r"#[0-9a-fA-F]{6}\b")


def texts():
    return {p.name: p.read_text(encoding="utf-8") for p in (build.SKILL / "SKILL.md", build.SKILL / "manual.md")}


def test_named_files_exist():
    for name, text in texts().items():
        for rel in set(PATH.findall(text)):
            assert (build.SKILL / rel).is_file(), f"{name} names {rel}"


def test_manual_colours_are_tokens():
    tokens = json.loads((build.SKILL / "tokens.json").read_text(encoding="utf-8"))
    known = {v.lower() for t in tokens["color"]["tokens"] for v in t["value"].values()}
    for name, text in texts().items():
        for h in HEX.findall(text):
            assert h.lower() in known, f"{name} quotes {h}, which no token holds"


def test_description_keeps_to_own_projects():
    description = parse(build.SKILL / "SKILL.md")[0]["description"]
    assert "own projects" in description
    assert "KIMKIM" in description and "Woodwell" in description


def test_manual_says_tailwind_files_are_copied():
    """Tailwind cannot build utilities from a remote file, so the manual must not send a reader to a link for it."""
    web = next(line for line in texts()["manual.md"].splitlines() if line.startswith("- **Web:**"))
    tail = web.split("Tailwind", 1)[1]
    assert "copy" in tail.lower()
