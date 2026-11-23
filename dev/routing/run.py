#!/usr/bin/env python3
"""Routing eval: does each need find the skill that answers it?

The skills never name each other. A skill states what it needs as a question, and Claude finds the skill whose
description answers that question. This eval checks that match from the outside. Each case is a prompt in
which one need arises. The runner starts a fresh, headless Claude Code session with this repository's plugin
loaded in place of the installed copy, records every skill the session loads, and stops the session as soon as
it reaches for any other tool, because the routing is decided by then.

    python dev/routing/run.py                  # all cases
    python dev/routing/run.py wardrobe-coat    # chosen cases, by id
    python dev/routing/run.py --model sonnet   # another model

A wrong load, or no load, points to the description of the skill that should have answered: fix it there,
never in the prompt. Each case costs one short session (about 0.2-0.5 USD with the default model).
"""
import argparse
import contextlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PLUGIN_DIR = REPO / "plugins" / "yili-skills"
PREFIX = "yili-skills:"
# The installed copy is switched off, so only the working copy's skills are listed.
SETTINGS = json.dumps({"enabledPlugins": {"yili-skills@yili-skills": False}})
# Tools that do work are removed: the eval needs only the routing decision, and nothing should act.
DISALLOWED = ["Agent", "Bash", "PowerShell", "WebSearch", "WebFetch", "Write", "Edit", "NotebookEdit", "Workflow"]
PASSIVE = {"Skill", "ToolSearch"}  # tools a session may call before the routing is decided
TIMEOUT = 180


def claude_executable():
    """The CLI as a list of arguments. On Windows, npm installs a .cmd shim; call the binary behind it."""
    found = shutil.which("claude")
    if found and found.lower().endswith((".cmd", ".bat")):
        native = Path(found).parent / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe"
        return [str(native)] if native.exists() else ["cmd", "/c", found]
    return [found or "claude"]


@contextlib.contextmanager
def scratch_folder():
    """A temporary folder that is removed afterwards, if it can be.

    On Windows a killed session can still hold the folder for a moment. Python 3.11's TemporaryDirectory then
    recurses without end while it removes it, so remove it here and leave it behind if it is still in use.
    """
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def run_case(case, model):
    """Run one case and return the skills it loaded, the reason it stopped, and its cost."""
    loaded, stopped, cost, listed = [], "end", None, []
    expected = {PREFIX + name for name in case.get("expect", [])}
    patience, other_calls = case.get("patience", 0), 0  # tool calls allowed before the routing counts as decided
    with scratch_folder() as empty:  # no CLAUDE.md or project files to steer the choice
        settings = Path(empty) / "settings.json"
        settings.write_text(SETTINGS, encoding="utf-8")
        # The prompt goes in on stdin, so no shell ever parses it.
        command = [*claude_executable(), "-p", "--output-format", "stream-json", "--verbose",
                   "--no-session-persistence", "--max-budget-usd", "1.0",
                   "--plugin-dir", str(PLUGIN_DIR), "--settings", str(settings),
                   "--disallowedTools", ",".join(DISALLOWED)]
        if model:
            command += ["--model", model]
        process = subprocess.Popen(command, cwd=empty, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL, text=True, encoding="utf-8")
        process.stdin.write(case["prompt"])
        process.stdin.close()
        started = time.time()
        try:
            for line in process.stdout:
                if time.time() - started > TIMEOUT:
                    stopped = "timeout"
                    break
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("type") == "system" and event.get("subtype") == "init":
                    listed = [s for s in event.get("skills", []) if str(s).startswith(PREFIX)]
                elif event.get("type") == "assistant":
                    for block in event.get("message", {}).get("content", []):
                        if block.get("type") != "tool_use":
                            continue
                        if block.get("name") == "Skill":
                            loaded.append(str(block.get("input", {}).get("skill", "")))
                        elif block.get("name") not in PASSIVE:
                            other_calls += 1
                            if other_calls > patience:
                                stopped = f"reached for {block.get('name')}"
                    if expected and expected <= set(loaded):
                        stopped = "all expected skills loaded"
                    if stopped != "end":
                        break
                elif event.get("type") == "result":
                    cost = event.get("total_cost_usd")
                    break
        finally:
            process.kill()
            process.wait()
    return {"loaded": loaded, "stopped": stopped, "cost": cost, "listed": listed}


def verdict(case, outcome):
    """A case passes when every expected skill loaded and no forbidden one did."""
    ours = {name[len(PREFIX):] for name in outcome["loaded"] if name.startswith(PREFIX)}
    missing = [name for name in case.get("expect", []) if name not in ours]
    wrong = [name for name in case.get("forbid", []) if name in ours]
    return not missing and not wrong, missing, wrong


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("ids", nargs="*", help="case ids to run (default: all)")
    parser.add_argument("--model", help="model alias or name (default: the CLI's default)")
    args = parser.parse_args()

    cases = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))
    if args.ids:
        cases = [case for case in cases if case["id"] in args.ids]
    rows, passed, total_cost = [], 0, 0.0
    for case in cases:
        outcome = run_case(case, args.model)
        ok, missing, wrong = verdict(case, outcome)
        passed += ok
        total_cost += outcome["cost"] or 0.0
        rows.append({"id": case["id"], "ok": ok, "missing": missing, "wrong": wrong, **outcome})
        print(f"{'PASS' if ok else 'FAIL'}  {case['id']:<28} loaded={outcome['loaded']}  "
              f"stopped={outcome['stopped']}" + (f"  missing={missing}" if missing else "")
              + (f"  wrong={wrong}" if wrong else ""), flush=True)
        if not outcome["listed"]:
            print("      warning: no yili-skills were listed in the session; is the plugin loading?", flush=True)

    print(f"\n{passed}/{len(rows)} passed · about {total_cost:.2f} USD")
    out = HERE / "results" / f"{date.today().isoformat()}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"model": args.model or "default", "rows": rows}, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"saved {out.relative_to(REPO)}")
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
