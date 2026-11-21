import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"
SCRIPTS = ROOT.parent.parent / "plugins/yili-skills/skills/digest-distill-information/scripts"
spec = importlib.util.spec_from_file_location("transcript", SCRIPTS / "transcript.py")
transcript = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transcript)


class ParseTests(unittest.TestCase):
    def test_vtt_drops_tags_and_rolling_repeats(self):
        cues = transcript.parse_vtt((FIXTURES / "youtube_auto.vtt").read_text())
        self.assertEqual([text for _, text in cues], [
            "hello everyone welcome",
            "to the patch review",
            "first the jungle changes",
        ])
        self.assertEqual(cues[-1][0], 65.11)

    def test_srt_is_parsed_like_vtt(self):
        cues = transcript.parse_vtt((FIXTURES / "plain.srt").read_text())
        self.assertEqual(cues, [(1.0, "Sharpen the blade first."),
                                (3.5, "Then set the chipbreaker close to the edge.")])

    def test_json3_skips_empty_events_and_normalises_spaces(self):
        cues = transcript.parse_json3(json.loads((FIXTURES / "youtube.json3").read_text()))
        self.assertEqual(cues, [(0.0, "hello everyone"), (2.1, "welcome to the review")])


class RenderTests(unittest.TestCase):
    def test_paragraphs_split_by_window_with_timestamps(self):
        cues = [(0, "a"), (30, "b"), (61, "c")]
        self.assertEqual(transcript.render(cues, timestamps=True), "[00:00] a b\n\n[01:01] c")
        self.assertEqual(transcript.render(cues), "a b\n\nc")


class TrackTests(unittest.TestCase):
    def test_human_captions_in_native_language_win(self):
        info = {"language": "ja", "subtitles": {"ja": ["h-ja"]},
                "automatic_captions": {"ja-orig": ["a-ja"], "en": ["a-en"]}}
        self.assertEqual(transcript.pick_track(info), ("human", "ja", ["h-ja"]))

    def test_automatic_original_language_beats_translation(self):
        info = {"language": "ja", "subtitles": {}, "automatic_captions": {"en": ["a-en"], "ja-orig": ["a-ja"]}}
        self.assertEqual(transcript.pick_track(info), ("automatic", "ja-orig", ["a-ja"]))

    def test_human_variant_of_the_language_beats_automatic(self):
        info = {"language": "en", "subtitles": {"ar": ["h-ar"], "en-eEY6OEpapPo": ["h-en"]},
                "automatic_captions": {"en": ["a-en"]}}
        self.assertEqual(transcript.pick_track(info), ("human", "en-eEY6OEpapPo", ["h-en"]))

    def test_requested_language_and_no_captions(self):
        info = {"language": "en", "subtitles": {"en": ["h-en"]}, "automatic_captions": {}}
        self.assertIsNone(transcript.pick_track(info, lang="de"))
        self.assertIsNone(transcript.pick_track({"subtitles": {}, "automatic_captions": {}}))


class ClockTests(unittest.TestCase):
    def test_clock_round_trip(self):
        self.assertEqual(transcript.clock(760), "12:40")
        self.assertEqual(transcript.clock(3750), "1:02:30")
        self.assertEqual(transcript.parse_clock("12:40"), 760)
        self.assertEqual(transcript.parse_clock("1:02:30"), 3750)
        self.assertEqual(transcript.parse_clock("95"), 95)


class StretchTests(unittest.TestCase):
    CUES = [(0, "intro and sponsor"), (40, "suction test starts"), (60, "it drops to 15 kPa"),
            (200, "battery after a year"), (500, "final SUCTION verdict")]

    def test_matches_merge_into_one_stretch(self):
        parts = transcript.stretches(self.CUES, ["suction", "kpa"], context=30)
        self.assertEqual([(lo, hi) for lo, hi, _ in parts], [(10, 90), (470, 530)])
        self.assertEqual(parts[0][2], "suction test starts it drops to 15 kPa")

    def test_case_and_scripts_without_spaces(self):
        cues = [(5, "吸力测试开始"), (90, "电池")]
        self.assertEqual(len(transcript.stretches(cues, ["吸力"])), 1)
        self.assertEqual(transcript.stretches(self.CUES, ["nothing"]), [])

    def test_window(self):
        self.assertEqual(transcript.within(self.CUES, 50, 300), [(60, "it drops to 15 kPa"), (200, "battery after a year")])


class HeaderTests(unittest.TestCase):
    INFO = {"title": "Robot vacuum after a year", "channel": "Owner Lab", "upload_date": "20260301",
            "duration": 2400, "view_count": 12000, "webpage_url": "https://example.com/v",
            "chapters": [{"start_time": 0, "title": "Intro"}, {"start_time": 760, "title": "Suction test"}],
            "description": "Bought with my own money. " * 3, "language": "en",
            "subtitles": {}, "automatic_captions": {"en-orig": [], "de": []}}

    def test_short_header_has_chapters_not_description(self):
        text = transcript.header(self.INFO, "u")
        self.assertIn("Owner Lab · 2026-03-01 · 40:00 · 12,000 views · https://example.com/v", text)
        self.assertIn("[12:40] Suction test", text)
        self.assertNotIn("Description", text)

    def test_info_header_adds_tracks_and_description(self):
        text = transcript.header(self.INFO, "u", full=True)
        self.assertIn("Captions: automatic (spoken language: en)", text)
        self.assertIn("Bought with my own money.", text)

    def test_no_captions_is_said(self):
        self.assertIn("none", transcript.describe_tracks({"subtitles": {}, "automatic_captions": {}}))


if __name__ == "__main__":
    unittest.main()
