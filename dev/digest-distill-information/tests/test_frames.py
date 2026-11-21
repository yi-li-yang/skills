import importlib.util
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[3] / "plugins/yili-skills/skills/digest-distill-information/scripts"
spec = importlib.util.spec_from_file_location("frames", SCRIPTS / "frames.py")
frames = importlib.util.module_from_spec(spec)
spec.loader.exec_module(frames)


class MomentTests(unittest.TestCase):
    def test_moments(self):
        self.assertEqual(frames.parse_clock("12:40"), 760)
        self.assertEqual(frames.parse_clock("1:02:30"), 3750)
        self.assertEqual(frames.parse_clock("95.5"), 95.5)
        with self.assertRaises(ValueError):
            frames.parse_clock("12m40")

    def test_labels_are_file_safe(self):
        self.assertEqual(frames.label(760), "12m40s")
        self.assertEqual(frames.label(3750), "1h02m30s")


class StreamTests(unittest.TestCase):
    def test_direct_stream_up_to_720_wins(self):
        info = {"http_headers": {"User-Agent": "x"}, "formats": [
            {"url": "a", "vcodec": "none", "protocol": "https"},                      # audio only
            {"url": "b", "vcodec": "avc1", "height": 1080, "protocol": "https"},
            {"url": "c", "vcodec": "avc1", "height": 720, "protocol": "m3u8_native"},
            {"url": "d", "vcodec": "avc1", "height": 480, "protocol": "https", "http_headers": {"Referer": "r"}},
        ]}
        self.assertEqual(frames.choose_stream(info), ("d", {"User-Agent": "x", "Referer": "r"}))

    def test_smallest_above_the_limit_when_nothing_fits(self):
        info = {"formats": [{"url": "big", "vcodec": "vp9", "height": 2160, "protocol": "https"},
                            {"url": "mid", "vcodec": "vp9", "height": 1080, "protocol": "https"}]}
        self.assertEqual(frames.choose_stream(info)[0], "mid")

    def test_no_video(self):
        self.assertIsNone(frames.choose_stream({"formats": [{"url": "a", "vcodec": "none"}]}))


class CommandTests(unittest.TestCase):
    def test_seek_comes_before_the_input(self):
        command = frames.ffmpeg_command("ffmpeg", "U", {"Referer": "r"}, 760, 768, "out.jpg")
        self.assertLess(command.index("-ss"), command.index("-i"))
        self.assertEqual(command[command.index("-headers") + 1], "Referer: r\r\n")
        self.assertIn("scale=768:-2", command)
        self.assertEqual(command[-1], "out.jpg")


if __name__ == "__main__":
    unittest.main()
