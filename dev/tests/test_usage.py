"""Check that usage.py counts each skill load once, in the right thread, and skips the evals' sessions.

    python -m pytest dev/tests
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "routing"))
import usage  # noqa: E402

PREFIX = usage.PREFIX


def prompt(text):
    return {"type": "user", "message": {"role": "user", "content": text}, "timestamp": "2026-11-20T10:00:00Z"}


def load(call_id, skill, kind="assistant", day="2026-11-20"):
    block = {"type": "tool_use", "id": call_id, "name": "Skill", "input": {"skill": PREFIX + skill}}
    return {"type": kind, "message": {"role": "assistant", "content": [block]}, "timestamp": f"{day}T10:00:01Z"}


def write(path, entries):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(e) for e in entries) + "\n", encoding="utf-8")


class Usage(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        root = Path(self.folder.name)
        session = root / "E--GitHub-project" / "s1.jsonl"
        write(session, [
            prompt("<system-reminder>context</system-reminder> Which kettle should I buy?"),
            load("call-1", "research-before-buy"),
            load("call-1", "research-before-buy"),  # the same call written again
            load("call-1", "research-before-buy", kind="api-request-blob"),  # and repeated in a later request
            {"type": "user", "toolUseResult": {}, "message": {"content": [{"type": "tool_result"}]}},
        ])
        write(session.with_suffix("") / "subagents" / "agent-a.jsonl", [
            prompt("Read what owners report about this kettle."),
            load("call-2", "digest-distill-information", day="2026-11-21"),
        ])
        write(root / "E--GitHub-project" / "s2-fork.jsonl", [load("call-1", "research-before-buy")])  # a fork's copy
        write(root / "C--Users-x-AppData-Local-Temp-tmpab12" / "s3.jsonl", [load("call-3", "wardrobe")])  # an eval
        self.loads = usage.read_loads(root)

    def tearDown(self):
        self.folder.cleanup()

    def test_each_call_counts_once_and_evals_are_skipped(self):
        self.assertEqual(sorted(x["skill"] for x in self.loads),
                         [PREFIX + "digest-distill-information", PREFIX + "research-before-buy"])

    def test_threads_dates_and_prompts(self):
        rows = {row[0]: row[1:] for row in usage.table(self.loads)}
        self.assertEqual(rows[PREFIX + "research-before-buy"], (1, 1, 0, "2026-11-20"))
        self.assertEqual(rows[PREFIX + "digest-distill-information"], (1, 0, 1, "2026-11-21"))
        prompts = {x["skill"]: x["prompt"] for x in self.loads}
        self.assertEqual(prompts[PREFIX + "research-before-buy"], "Which kettle should I buy?")

    def test_never_loaded(self):
        names = [PREFIX + "research-before-buy", PREFIX + "wardrobe"]
        self.assertEqual(usage.never_loaded(self.loads, names), [PREFIX + "wardrobe"])


if __name__ == "__main__":
    unittest.main()
