#!/usr/bin/env python3
"""Save still frames from a video at chosen moments, so Claude can look at what the video shows.

    python3 frames.py <url> 12:40 13:05 1:02:30     one frame at each moment
    python3 frames.py <url> 12:40 --width 1024       larger frames (default: 768 pixels wide)
    python3 frames.py <url> 12:40 --out ./frames     the folder to save in (default: the system temp folder)

yt-dlp finds the video stream and ffmpeg seeks into it, so only a few seconds around each moment are
fetched, never the whole video. One line is printed per frame: the moment and the saved file. Read the
files as images. Choose the moments from a transcript stretch or a chapter: each frame costs about as much
as a page of text, so a frame is worth taking only where the picture holds what words cannot.

Needs yt-dlp, and ffmpeg on the PATH or the imageio-ffmpeg package, which bundles one.
Exit codes: 0 ok · 1 failed · 3 yt-dlp or ffmpeg missing · 4 blocked by the site.
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BLOCKED_HINTS = ("confirm you're not a bot", "confirm you’re not a bot", "http error 429", "too many requests")
DIRECT = ("https", "http")
STREAMED = ("m3u8_native", "m3u8")
MAX_HEIGHT = 720  # enough to read a meter or a label once scaled down; smaller streams seek faster


def parse_clock(text):
    """'12:40', '1:02:30', '95' or '95.5' -> seconds."""
    if not re.fullmatch(r"\d+(?::\d{1,2}){0,2}(?:\.\d+)?", str(text).strip()):
        raise ValueError(f"not a moment: {text!r} (use 12:40, 1:02:30 or seconds)")
    seconds = 0.0
    for part in str(text).strip().split(":"):
        seconds = seconds * 60 + float(part)
    return seconds


def label(seconds):
    """Seconds -> a file-safe label such as 12m40s or 1h02m30s."""
    seconds = int(seconds)
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    return f"{h}h{m:02d}m{s:02d}s" if h else f"{m}m{s:02d}s"


def choose_stream(info, max_height=MAX_HEIGHT):
    """(url, headers) of the video stream to seek in: a direct link before a streamed one, then the tallest
    picture up to max_height, then the smallest picture above it."""
    formats = [f for f in info.get("formats") or [info]
               if f.get("url") and f.get("vcodec") not in (None, "none")
               and (f.get("protocol") or "https") in DIRECT + STREAMED]
    if not formats:
        return None

    def rank(f):
        height = f.get("height") or 0
        fits = height <= max_height
        return (f.get("protocol", "https") in DIRECT, fits, height if fits else -height)
    best = max(formats, key=rank)
    headers = {**(info.get("http_headers") or {}), **(best.get("http_headers") or {})}
    return best["url"], headers


def ffmpeg_command(ffmpeg, url, headers, seconds, width, out):
    """Seek before opening the input, so ffmpeg reads only the few seconds around the moment."""
    command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{seconds:.3f}"]
    if headers:
        command += ["-headers", "".join(f"{key}: {value}\r\n" for key, value in headers.items())]
    return command + ["-i", url, "-frames:v", "1", "-vf", f"scale={width}:-2", "-q:v", "3", str(out)]


def find_ffmpeg():
    found = shutil.which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:  # not installed, or its bundled binary is missing
        return None


def fail(message, code):
    print(message, file=sys.stderr)
    sys.exit(code)


class Silent:  # our own one-line messages replace yt-dlp's log output
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass


def main():
    parser = argparse.ArgumentParser(description="Save still frames from a video at chosen moments.")
    parser.add_argument("url")
    parser.add_argument("moments", nargs="+", help="moments such as 12:40, 1:02:30 or 95")
    parser.add_argument("--width", type=int, default=768, help="frame width in pixels (default 768)")
    parser.add_argument("--out", help="folder to save the frames in (default: the system temp folder)")
    args = parser.parse_args()

    try:
        moments = [parse_clock(m) for m in args.moments]
    except ValueError as error:
        fail(f"failed: {error}", 1)
    try:
        import yt_dlp
    except ImportError:
        fail("frames.py needs yt-dlp. Ask the user before installing it: python3 -m pip install --user yt-dlp", 3)
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        fail("frames.py needs ffmpeg. Ask the user before installing it (for example: python3 -m pip install "
             "--user imageio-ffmpeg). Without it, describe the moment from the transcript and say no frame "
             "was seen.", 3)

    options = {"skip_download": True, "quiet": True, "no_warnings": True, "noplaylist": True,
               "logger": Silent(), "format": f"bv*[height<={MAX_HEIGHT}]/b[height<={MAX_HEIGHT}]/bv*/b"}
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(args.url, download=False)
    except yt_dlp.utils.DownloadError as error:
        if any(hint in str(error).lower() for hint in BLOCKED_HINTS):
            fail("blocked: the site refused requests from this network. Record the moment as a pointer.", 4)
        fail("failed: " + str(error).splitlines()[0], 1)
    except Exception as error:  # extractor bugs and site changes surface as arbitrary exceptions
        fail(f"failed: yt-dlp could not read this site ({type(error).__name__}: {error}).", 1)

    stream = choose_stream(info)
    if not stream:
        fail("failed: no video stream that ffmpeg can seek in. Record the moment as a pointer.", 1)
    url, headers = stream
    folder = Path(args.out) if args.out else Path(tempfile.gettempdir()) / "claude-frames"
    folder.mkdir(parents=True, exist_ok=True)
    duration = info.get("duration")
    saved = 0
    for seconds in moments:
        if duration and seconds > duration:
            print(f"{label(seconds)}  skipped: the video is only {label(duration)} long")
            continue
        out = folder / f"{info.get('id') or 'video'}-{label(seconds)}.jpg"
        result = subprocess.run(ffmpeg_command(ffmpeg, url, headers, seconds, args.width, out),
                                capture_output=True, text=True, timeout=120)
        if result.returncode == 0 and out.exists():
            print(f"{label(seconds)}  {out}")
            saved += 1
        else:
            reason = (result.stderr or "no frame written").strip().splitlines()[-1][:200]
            print(f"{label(seconds)}  failed: {reason}")
    if not saved:
        sys.exit(1)


if __name__ == "__main__":
    main()
