#!/usr/bin/env python3
"""Real use: which skills load in everyday sessions, and on which prompts?

The routing eval checks prompts that were chosen for it. This script reads what happened instead. Claude Code
writes each session to a transcript, ~/.claude/projects/<project>/<session>.jsonl, and each subagent's work to
<session>/subagents/agent-<id>.jsonl. A skill load is a Skill tool call in those files. The script counts the
loads of this plugin's skills, splits them into main threads and subagents, and names the skills that never
loaded. With --prompts it shows the prompt before each load of one skill, so a wrong load on a real prompt can
be found and its description fixed.

    python dev/routing/usage.py                       # this plugin's skills
    python dev/routing/usage.py --all                 # every skill, from any plugin
    python dev/routing/usage.py --prompts wardrobe    # the prompt before each load of one skill

It reads only local files and costs nothing. It has three limits. The transcript format is internal to Claude
Code and can change. Conversations on claude.ai and the phone are not stored on this machine. Sessions of the
evals, which run in temporary folders, are left out.
"""
import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run import PLUGIN_DIR, PREFIX  # noqa: E402

ROOT = Path.home() / ".claude" / "projects"
EVAL_FOLDER = "-Temp-tmp"  # run.py and session.py work in tempfile.mkdtemp() folders, named tmp...
# Text that the app adds to a prompt (reminders, notices, browser instructions) comes wrapped in a tag.
ADDED = re.compile(r"<([A-Za-z_][\w-]*)>.*?</\1>", re.S)
WIDTH = 160  # characters of a prompt to show


def open_text(path):
    """Open a transcript, also when its path is longer than the 260 characters that Windows allows by default."""
    name = os.path.abspath(path)
    if os.name == "nt" and not name.startswith("\\\\?\\"):
        name = "\\\\?\\" + name
    return open(name, encoding="utf-8", errors="replace")


def prompt_text(entry):
    """The words of a prompt, or None when the line is a tool result, a notice or other text that no one typed."""
    if entry.get("type") != "user" or entry.get("isMeta") or "toolUseResult" in entry:
        return None
    if entry.get("promptSource") == "system":
        return None
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, list):
        content = " ".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    if not isinstance(content, str):
        return None
    return " ".join(ADDED.sub(" ", content).split()) or None


def read_loads(root, every=False):
    """Every skill load under root, once each, with its project, its thread, its date and the prompt before it.

    A transcript can hold the same call more than once: a later request repeats it, and a resumed or forked
    session copies the history into a new file. So only the assistant's own lines count, once for each call id.
    """
    loads, seen = [], set()
    for path in sorted(Path(root).rglob("*.jsonl")):
        parts = path.relative_to(root).parts
        if EVAL_FOLDER in parts[0]:
            continue
        thread = "subagent" if "subagents" in parts else "main"
        prompt = None
        with open_text(path) as lines:
            for line in lines:
                if '"user"' not in line and '"Skill"' not in line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                prompt = prompt_text(entry) or prompt
                if entry.get("type") != "assistant":
                    continue
                for block in (entry.get("message") or {}).get("content") or []:
                    if not isinstance(block, dict) or block.get("type") != "tool_use" or block.get("name") != "Skill":
                        continue
                    skill = str((block.get("input") or {}).get("skill", ""))
                    if block.get("id") in seen or not (every or skill.startswith(PREFIX)):
                        continue
                    seen.add(block.get("id"))
                    loads.append({
                        "skill": skill,
                        "project": parts[0],
                        "thread": thread,
                        "date": str(entry.get("timestamp", ""))[:10],
                        "prompt": prompt or "",
                    })
    return loads


def plugin_skills():
    """The names of this plugin's skills, with the plugin prefix."""
    return sorted(PREFIX + p.name for p in (PLUGIN_DIR / "skills").iterdir() if (p / "SKILL.md").is_file())


def never_loaded(loads, names):
    """The names among names that no load used."""
    used = {load["skill"] for load in loads}
    return [name for name in names if name not in used]


def table(loads):
    """One row for each skill: loads, how many in main threads and in subagents, and the date of the last one."""
    rows = []
    for skill, total in Counter(load["skill"] for load in loads).most_common():
        mine = [load for load in loads if load["skill"] == skill]
        main = sum(load["thread"] == "main" for load in mine)
        rows.append((skill, total, main, total - main, max(load["date"] for load in mine)))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT, help="the folder of Claude Code transcripts")
    parser.add_argument("--all", action="store_true", help="count every skill, not only this plugin's")
    parser.add_argument("--prompts", metavar="SKILL", help="show the prompt before each load of this skill")
    args = parser.parse_args()

    loads = read_loads(args.root, every=args.all)
    if args.prompts:
        wanted = args.prompts if ":" in args.prompts or args.all else PREFIX + args.prompts
        for load in sorted((x for x in loads if x["skill"] == wanted), key=lambda x: x["date"]):
            prompt = load["prompt"][:WIDTH] or "(no prompt found)"
            print(f"{load['date']}  {load['thread']:<8}  {load['project']}\n    {prompt}")
        return 0

    show = (lambda name: name) if args.all else (lambda name: name.removeprefix(PREFIX))
    print(f"{'skill':<40} {'loads':>5} {'main':>5} {'subagent':>8}  last")
    for skill, total, main_count, sub_count, last in table(loads):
        print(f"{show(skill):<40} {total:>5} {main_count:>5} {sub_count:>8}  {last}")
    if not args.all:
        missing = never_loaded(loads, plugin_skills())
        print("\nNever loaded: " + (", ".join(show(name) for name in missing) or "none"))
    print(f"\n{len(loads)} loads under {args.root}. Conversations on claude.ai and the phone are not stored here.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
