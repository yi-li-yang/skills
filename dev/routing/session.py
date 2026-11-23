#!/usr/bin/env python3
"""Run one whole headless session with this repository's plugin, and record how the skills were used.

The routing eval stops a session as soon as the routing is decided. This script lets a session run to the
end (or to its budget), so an eval can see what happens later: which skills load and when, in the main
session and inside subagents, what each subagent was asked, and what the final answer was.

    python dev/routing/session.py "Which kettle should I buy?" --out run.json
    python dev/routing/session.py "..." --without i-think-like-this         # as if that skill were missing
    python dev/routing/session.py "..." --rename digest-distill-information=read-any-material
    python dev/routing/session.py "..." --disallow Agent                      # no subagents, as on claude.ai
    python dev/routing/session.py "..." --swap research-before-buy/references/source-weighting.md=old.md
    python dev/routing/session.py "..." --allow "Bash(python *)" --path ../venv/Scripts   # let it run the scripts

Web search and web fetch are allowed by default, so research can run; every other tool that needs
permission is refused, because no one is there to answer a prompt.

--without, --rename and --swap work on a temporary copy of the plugin; the working copy is never changed.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run import PLUGIN_DIR, SETTINGS, claude_executable, scratch_folder  # noqa: E402


def prepared_plugin(workdir, without, renames, swaps):
    """A temporary copy of the plugin with skills removed, renamed or with files swapped."""
    copy = Path(workdir) / "yili-skills"
    shutil.copytree(PLUGIN_DIR, copy, ignore=shutil.ignore_patterns("__pycache__"))
    for name in without:
        shutil.rmtree(copy / "skills" / name)
    for pair in renames:
        old, new = pair.split("=", 1)
        skill = copy / "skills" / old
        text = (skill / "SKILL.md").read_text(encoding="utf-8").replace(f"name: {old}\n", f"name: {new}\n", 1)
        (skill / "SKILL.md").write_text(text, encoding="utf-8")
        skill.rename(copy / "skills" / new)
    for pair in swaps:
        target, source = pair.split("=", 1)
        shutil.copyfile(source, copy / "skills" / target)
    return copy


def summarise(block):
    """A short label for one tool call, enough to follow what the session did."""
    name, data = block.get("name"), block.get("input", {})
    if name == "Skill":
        return f"Skill {data.get('skill')}"
    if name == "Agent":
        return f"Agent [{data.get('subagent_type', '')}] {data.get('description', '')}: {str(data.get('prompt', ''))[:300]}"
    for key in ("query", "url", "command", "file_path", "pattern"):
        if key in data:
            return f"{name} {str(data[key])[:160]}"
    return name


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("prompt")
    parser.add_argument("--out", required=True, help="JSON file for the record")
    parser.add_argument("--budget", type=float, default=5.0, help="maximum USD for the session (5)")
    parser.add_argument("--timeout", type=int, default=1800, help="maximum seconds (1800)")
    parser.add_argument("--without", action="append", default=[], metavar="SKILL")
    parser.add_argument("--rename", action="append", default=[], metavar="OLD=NEW")
    parser.add_argument("--swap", action="append", default=[], metavar="PATH=FILE",
                        help="replace a file inside the plugin's skills folder")
    parser.add_argument("--disallow", action="append", default=[], metavar="TOOL")
    parser.add_argument("--allow", action="append", default=["WebSearch", "WebFetch"], metavar="TOOL",
                        help="tools to allow without a prompt (WebSearch and WebFetch always)")
    parser.add_argument("--path", help="a folder to put first on PATH, e.g. a venv with yt-dlp")
    parser.add_argument("--model")
    args = parser.parse_args()

    record = {"prompt": args.prompt, "without": args.without, "rename": args.rename, "swap": args.swap,
              "disallow": args.disallow, "allow": args.allow, "skills_listed": [], "steps": [], "result": None, "cost": None}
    with scratch_folder() as workdir:
        plugin = prepared_plugin(workdir, args.without, args.rename, args.swap)
        settings = Path(workdir) / "settings.json"
        settings.write_text(SETTINGS, encoding="utf-8")
        cwd = Path(workdir) / "cwd"
        cwd.mkdir()
        command = [*claude_executable(), "-p", "--output-format", "stream-json", "--verbose",
                   "--no-session-persistence", "--max-budget-usd", str(args.budget),
                   "--plugin-dir", str(plugin), "--settings", str(settings)]
        command += ["--allowedTools", ",".join(args.allow)]
        if args.disallow:
            command += ["--disallowedTools", ",".join(args.disallow)]
        env = dict(os.environ)
        if args.path:
            env["PATH"] = str(Path(args.path).resolve()) + os.pathsep + env.get("PATH", "")
        if args.model:
            command += ["--model", args.model]
        started = time.time()
        process = subprocess.Popen(command, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL, text=True, encoding="utf-8", env=env)
        process.stdin.write(args.prompt)
        process.stdin.close()
        try:
            for line in process.stdout:
                if time.time() - started > args.timeout:
                    record["stopped"] = "timeout"
                    break
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                kind = event.get("type")
                if kind == "system" and event.get("subtype") == "init" and not record["skills_listed"]:
                    record["skills_listed"] = [s for s in event.get("skills", []) if str(s).startswith("yili-skills:")]
                elif kind == "assistant":
                    where = "sub" if event.get("parent_tool_use_id") else "main"
                    for block in event.get("message", {}).get("content", []):
                        if block.get("type") == "tool_use":
                            record["steps"].append({"t": round(time.time() - started), "where": where,
                                                    "call": summarise(block)})
                elif kind == "result":
                    # A session that sent subagents to work in the background can end its turn before they finish,
                    # then continue when they report back. Keep reading: the last result is the final answer.
                    record.setdefault("results", []).append(event.get("result"))
                    record["result"] = event.get("result")
                    record["cost"] = event.get("total_cost_usd")
                    record["usage"] = event.get("usage")
                    record["turns"] = event.get("num_turns")
                    record["stopped"] = event.get("subtype")
        finally:
            process.kill()
            process.wait()
    record["seconds"] = round(time.time() - started)
    record["skills_loaded"] = [s["where"] + ":" + s["call"][6:] for s in record["steps"] if s["call"].startswith("Skill ")]
    Path(args.out).write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{record.get('stopped')} · {record['seconds']}s · {record['cost']} USD · loaded {record['skills_loaded']}")


if __name__ == "__main__":
    main()
