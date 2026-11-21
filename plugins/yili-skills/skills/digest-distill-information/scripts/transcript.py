#!/usr/bin/env python3
"""Print what a video says, so Claude can read it: its details, its chapters and its words.

    python3 transcript.py <url> --info                     details, chapters and caption tracks; no words
    python3 transcript.py <url> --grep suction kPa         only the stretches that mention a term
    python3 transcript.py <url> --from 12:00 --to 15:30    one stretch
    python3 transcript.py <url> [--timestamps]             every word, in paragraphs
    python3 transcript.py <url> --speech                   no captions: transcribe the audio on this computer

--lang ja picks the caption language. --context 30 sets the seconds kept on each side of a --grep match.

The words come from the video's own captions (human-made first, then automatic) through yt-dlp, which reads
YouTube, Bilibili, Vimeo and many other sites. Only the caption file is downloaded, except with --speech,
which downloads the audio and needs the faster-whisper package. Details and words are cached in the system
temp folder, so a second call on the same video does not fetch it again.

Exit codes: 0 ok · 1 failed · 3 yt-dlp missing · 4 blocked by the site · 5 no captions (try --speech, or
record the video as a pointer: who, what, link, timestamp).
"""
import argparse
import hashlib
import json
import re
import sys
import tempfile
import time
from pathlib import Path

BLOCKED_HINTS = ("confirm you're not a bot", "confirm you’re not a bot", "http error 429", "too many requests")
FORMAT_PREFERENCE = ("json3", "vtt", "srt")
CACHE = Path(tempfile.gettempdir()) / "claude-transcripts"
INFO_FIELDS = ("id", "title", "channel", "uploader", "upload_date", "webpage_url", "duration", "view_count",
               "like_count", "comment_count", "description", "chapters", "language", "subtitles",
               "automatic_captions")
SPEECH_MODEL = "small"
INFO_TTL = 3 * 3600  # caption links in the details expire after some hours
DESCRIPTION_LIMIT = 3000


def parse_json3(data):
    """YouTube json3 captions -> [(start_seconds, text)]."""
    cues = []
    for event in data.get("events", []):
        text = "".join(seg.get("utf8", "") for seg in event.get("segs") or []).strip()
        if text:
            cues.append((event.get("tStartMs", 0) / 1000, " ".join(text.split())))
    return cues


def parse_vtt(text):
    """WebVTT or SRT captions -> [(start_seconds, text)], with rolling-caption repeats removed."""
    cues, start, last = [], 0.0, None
    stamp = re.compile(r"(?:(\d+):)?(\d{2}):(\d{2})[.,](\d{3})\s+-->")
    for raw in text.splitlines():
        line = raw.strip()
        m = stamp.match(line)
        if m:
            h, mnt, s, ms = (int(g or 0) for g in m.groups())
            start = h * 3600 + mnt * 60 + s + ms / 1000
            continue
        if not line or line.isdigit() or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            continue
        line = " ".join(re.sub(r"<[^>]+>", "", line).split())  # drop inline timing/style tags
        if line and line != last:
            cues.append((start, line))
            last = line
    return cues


def clock(seconds):
    """Seconds -> m:ss, or h:mm:ss for an hour or more."""
    seconds = int(seconds or 0)
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def parse_clock(text):
    """'12:40', '1:02:30' or '95' -> seconds."""
    parts = [float(p) for p in str(text).strip().split(":")]
    seconds = 0.0
    for part in parts:
        seconds = seconds * 60 + part
    return seconds


def render(cues, timestamps=False, window=60):
    """Group cues into paragraphs of about `window` seconds."""
    paragraphs, current, block_start = [], [], None
    for start, text in cues:
        if block_start is None:
            block_start = start
        if start - block_start >= window and current:
            paragraphs.append((block_start, " ".join(current)))
            current, block_start = [], start
        current.append(text)
    if current:
        paragraphs.append((block_start, " ".join(current)))
    out = []
    for start, text in paragraphs:
        prefix = f"[{int(start // 60):02d}:{int(start % 60):02d}] " if timestamps else ""
        out.append(prefix + text)
    return "\n\n".join(out)


def within(cues, start=None, end=None):
    """Keep the cues that start inside [start, end]."""
    return [(t, text) for t, text in cues
            if (start is None or t >= start) and (end is None or t <= end)]


def stretches(cues, terms, context=30.0):
    """The parts of the transcript that mention any term, each widened by `context` seconds on both sides.

    Overlapping parts are merged, so each stretch reads as one passage. Matching ignores case, and it also
    works for text without spaces between words, such as Chinese or Japanese.
    """
    needles = [term.lower() for term in terms if term.strip()]
    hits = [t for t, text in cues if any(n in text.lower() for n in needles)]
    windows = []
    for t in hits:
        lo, hi = max(0.0, t - context), t + context
        if windows and lo <= windows[-1][1]:
            windows[-1][1] = max(windows[-1][1], hi)
        else:
            windows.append([lo, hi])
    return [(lo, hi, " ".join(text for t, text in cues if lo <= t <= hi)) for lo, hi in windows]


def pick_track(info, lang=None):
    """Choose (kind, language, formats): human captions before automatic ones, original language first."""
    manual, auto = info.get("subtitles") or {}, info.get("automatic_captions") or {}
    native = info.get("language")
    if lang:
        wanted = [lang]
    else:
        wanted = [native, f"{native}-orig", "en", "en-orig"] if native else ["en", "en-orig"]
    for kind, tracks in (("human", manual), ("automatic", auto)):
        for code in wanted + [c for c in tracks if c.endswith("-orig")]:
            if code in tracks:
                return kind, code, tracks[code]
            # A human track is often labelled with a variant of the language, such as en-GB or en-x7Yq2.
            variant = next((c for c in tracks if kind == "human" and c.startswith(f"{code}-")), None)
            if variant:
                return kind, variant, tracks[variant]
    if manual and not lang:  # human captions in another language still beat nothing
        code = next(iter(manual))
        return "human", code, manual[code]
    return None


def describe_tracks(info):
    """One line on which captions exist, so Claude knows before asking for words."""
    manual = sorted((info.get("subtitles") or {}).keys())
    auto = info.get("automatic_captions") or {}
    parts = []
    if manual:
        parts.append("human in " + ", ".join(manual[:12]) + (" …" if len(manual) > 12 else ""))
    if auto:
        native = info.get("language") or next((c[:-5] for c in auto if c.endswith("-orig")), None)
        parts.append(f"automatic (spoken language: {native})" if native else "automatic")
    return "Captions: " + ("; ".join(parts) if parts else "none (try --speech, or record a pointer)")


def header(info, url, full=False):
    """Title, who and when, chapters; with full=True also the description and the caption tracks."""
    date = info.get("upload_date") or ""
    if len(date) == 8:
        date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
    who = info.get("channel") or info.get("uploader") or ""
    facts = [who, date, clock(info.get("duration")) if info.get("duration") else ""]
    for key, label in (("view_count", "views"), ("like_count", "likes"), ("comment_count", "comments")):
        if info.get(key) is not None:
            facts.append(f"{info[key]:,} {label}")
    lines = [f"# {info.get('title', '')}", " · ".join(f for f in facts if f) + f" · {info.get('webpage_url') or url}"]
    chapters = info.get("chapters") or []
    if chapters:
        lines.append("Chapters: " + " | ".join(f"[{clock(c.get('start_time'))}] {c.get('title', '')}"
                                               for c in chapters))
    if full:
        lines.append(describe_tracks(info))
        description = (info.get("description") or "").strip()
        if len(description) > DESCRIPTION_LIMIT:
            description = description[:DESCRIPTION_LIMIT] + " … (cut)"
        if description:
            lines += ["", "Description:", description]
    return "\n".join(lines)


def fail(message, code):
    print(message, file=sys.stderr)
    sys.exit(code)


def cache_path(url, name):
    CACHE.mkdir(parents=True, exist_ok=True)
    return CACHE / f"{hashlib.sha1(url.encode('utf-8')).hexdigest()[:16]}.{name}.json"


def load_cached(url, name):
    path = cache_path(url, name)
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
    return None


def save_cached(url, name, value):
    try:
        cache_path(url, name).write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass  # a cache that cannot be written only costs a second fetch


class Silent:  # our own one-line messages replace yt-dlp's log output
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass


def ytdlp():
    try:
        import yt_dlp
    except ImportError:
        fail("transcript.py needs yt-dlp. Ask the user before installing it: python3 -m pip install --user yt-dlp", 3)
    return yt_dlp


def guarded(action):
    """Run a yt-dlp call and turn its failures into one-line messages with exit codes."""
    yt_dlp = ytdlp()
    try:
        return action(yt_dlp)
    except yt_dlp.utils.DownloadError as error:
        message = str(error).lower()
        if any(hint in message for hint in BLOCKED_HINTS):
            fail("blocked: the site refused requests from this network (common on cloud servers). "
                 "Run it from a home connection, or record the video as a pointer instead.", 4)
        fail("failed: " + str(error).splitlines()[0], 1)
    except Exception as error:  # extractor bugs and site changes surface as arbitrary exceptions
        fail(f"failed: yt-dlp could not read this site ({type(error).__name__}: {error}). "
             "Record the video as a pointer instead.", 1)


def options(**extra):
    return {"skip_download": True, "quiet": True, "no_warnings": True, "noplaylist": True, "logger": Silent(),
            **extra}


def fetch_info(url, fresh=False):
    """The video's details, from the cache when possible."""
    info = None if fresh else load_cached(url, "info")
    if info is not None and time.time() - info.get("_fetched", 0) > INFO_TTL:
        info = None
    if info is None:
        def extract(yt_dlp):
            with yt_dlp.YoutubeDL(options()) as ydl:
                return ydl.extract_info(url, download=False)
        full = guarded(extract)
        info = {key: full.get(key) for key in INFO_FIELDS}
        info["_fetched"] = time.time()
        save_cached(url, "info", info)
    return info


def fetch_captions(url, info, lang):
    """(cues, note) from the chosen caption track, or None when the video has no captions."""
    track = pick_track(info, lang)
    if not track:
        return None
    kind, code, formats = track
    cached = load_cached(url, f"captions-{code}")
    if cached is not None:
        return [tuple(c) for c in cached], f"Words: {kind} captions, language '{code}'"
    fmt = next((f for pref in FORMAT_PREFERENCE for f in formats if f.get("ext") == pref), None)
    if not fmt:
        fail(f"failed: no readable caption format for '{code}'.", 1)

    def download(yt_dlp):
        with yt_dlp.YoutubeDL(options()) as ydl:
            return ydl.urlopen(fmt["url"]).read().decode("utf-8", "replace")
    body = guarded(download)
    cues = parse_json3(json.loads(body)) if fmt.get("ext") == "json3" else parse_vtt(body)
    save_cached(url, f"captions-{code}", cues)
    return cues, f"Words: {kind} captions, language '{code}'"


def speech_available():
    try:
        import faster_whisper  # noqa: F401
        return True
    except ImportError:
        return False


def transcribe(url, lang):
    """(cues, note) from local speech-to-text: download the audio, then run faster-whisper on it."""
    cached = load_cached(url, f"speech-{SPEECH_MODEL}")
    note = (f"Words: speech-to-text on this computer (faster-whisper {SPEECH_MODEL}), not captions. "
            "Names, numbers and model codes may be wrong; check them against frames or the description.")
    if cached is not None:
        return [tuple(c) for c in cached], note
    if not speech_available():
        fail("no captions, and speech-to-text needs the faster-whisper package. Ask the user before installing "
             "it (python3 -m pip install --user faster-whisper); otherwise record the video as a pointer.", 5)
    from faster_whisper import WhisperModel

    folder = Path(tempfile.mkdtemp(prefix="claude-audio-"))

    def download(yt_dlp):
        opts = options(skip_download=False, format="bestaudio/best", outtmpl=str(folder / "audio.%(ext)s"))
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.extract_info(url, download=True)
    guarded(download)
    audio = next(folder.glob("audio.*"), None)
    if audio is None:
        fail("failed: the audio could not be downloaded. Record the video as a pointer instead.", 1)
    model = WhisperModel(SPEECH_MODEL, compute_type="int8")
    segments, _ = model.transcribe(str(audio), language=lang)
    cues = [(round(s.start, 2), " ".join(s.text.split())) for s in segments if s.text.strip()]
    save_cached(url, f"speech-{SPEECH_MODEL}", cues)
    return cues, note


def main():
    parser = argparse.ArgumentParser(description="Print what a video says: details, chapters and words.")
    parser.add_argument("url")
    parser.add_argument("--info", action="store_true", help="details, chapters, description and caption tracks only")
    parser.add_argument("--grep", nargs="+", metavar="TERM", help="print only the stretches that mention a term")
    parser.add_argument("--context", type=float, default=30.0, help="seconds kept on each side of a match (30)")
    parser.add_argument("--from", dest="start", help="start of the stretch, e.g. 12:00")
    parser.add_argument("--to", dest="end", help="end of the stretch, e.g. 15:30")
    parser.add_argument("--lang", help="caption language code, e.g. en, ja, zh-Hans (default: the video's own)")
    parser.add_argument("--timestamps", action="store_true", help="prefix each paragraph with [mm:ss]")
    parser.add_argument("--speech", action="store_true", help="transcribe the audio here when there are no captions")
    args = parser.parse_args()

    info = fetch_info(args.url)
    print(header(info, args.url, full=args.info))
    if args.info:
        return

    found = fetch_captions(args.url, info, args.lang)
    if found is None:
        if not args.speech:
            installed = "installed" if speech_available() else "not installed"
            fail(f"no captions{f' in {args.lang!r}' if args.lang else ''}. Speech-to-text (faster-whisper) is "
                 f"{installed}: add --speech to transcribe the audio, or record the video as a pointer.", 5)
        found = transcribe(args.url, args.lang)
    cues, note = found
    print(note)

    start = parse_clock(args.start) if args.start else None
    end = parse_clock(args.end) if args.end else None
    cues = within(cues, start, end)
    if args.grep:
        parts = stretches(cues, args.grep, args.context)
        print(f"{len(parts)} stretch(es) mention {', '.join(args.grep)}.\n")
        if not parts:
            print("Nothing matched. Try other words, the words of the video's own language, or the chapters.")
        for lo, hi, text in parts:
            print(f"[{clock(lo)}–{clock(hi)}] {text}\n")
        return
    print()
    print(render(cues, args.timestamps or start is not None or end is not None))


if __name__ == "__main__":
    main()
