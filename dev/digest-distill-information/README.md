# Digest and distill information

When I research something, I watch the review, I look at what the camera shows, I read the comments where owners correct the reviewer, and I look at the photos in an owner's post. This skill makes Claude take in material the same way, in any form, on any platform and in any language, and bring back only what bears on the question.

It answers one question: *what does the actual material say and show about this?* It does not decide what counts as evidence in a domain, how much a claim is worth, or what the final answer is. The skill that needs the material decides those, or Claude does.

## How it works

The asker gives a question (open or narrow), the kinds of evidence that would settle it, and what the answer is worth. The skill finds the items, takes in the most relevant first, and stops when the question is answered well enough for what it is worth:

- **Which item:** rank by how likely each item is to settle the question, using cheap signals (title, description, chapters, uploader, date, top comments). Open the top one first.
- **Which part:** go to the chapter or the transcript stretch that answers the question.
- **Which form:** words for what was said, a frame for what was shown.

It returns findings with their evidence and where they are (timestamps), who is speaking (sponsored, gifted, affiliate links), leads for the next question, gaps, and how the material was read.

## Tools

Both scripts are in `plugins/yili-skills/skills/digest-distill-information/scripts/`.

| Script | What it does | Needs |
| --- | --- | --- |
| `transcript.py <url> --info` | Details, chapters, description and caption tracks, without words | yt-dlp |
| `transcript.py <url> --grep <terms>` | Only the stretches that mention a term, with timestamps | yt-dlp |
| `transcript.py <url> --from 12:00 --to 15:30` | One stretch | yt-dlp |
| `transcript.py <url> --speech` | Speech-to-text when there are no captions | yt-dlp, faster-whisper |
| `frames.py <url> 12:40 13:05` | One frame per moment, 768 pixels wide, fetched by seeking (never the whole video) | yt-dlp, ffmpeg or imageio-ffmpeg |

Install what you want Claude to have: `python3 -m pip install --user yt-dlp imageio-ffmpeg`, and `faster-whisper` for speech-to-text. The skill tells Claude never to install them without asking. Details and words are cached in the system temp folder, so a second `--grep` on the same video does not fetch it again.

`transcript.py` began in `updated-domain-expert` (then called `expertise`), which read captions only. It moved here with `--info`, `--grep`, the time window, the cache and speech-to-text.

## Tests

```
python -m pytest dev/digest-distill-information
```

Live checks on 2026-11-21, with yt-dlp 2026.10.26 and imageio-ffmpeg in a separate environment:

- A YouTube video with captions (Steve Jobs' 2005 Stanford address, 15 minutes): `--info` gave the chapters and the caption tracks; `--grep dots` returned two stretches (0:42 and 4:44) instead of the full transcript; `--from 2:00 --to 2:40` returned one stretch; `frames.py` saved frames at 1:00 and 13:30 and skipped a moment past the end.
- A Bilibili video without captions (乡音计划《四川成都话入门100句》): `--info` worked; asking for words exited with code 5 and said that speech-to-text was not installed; `frames.py` at 0:30 saved a frame that shows lesson 2's ten phrases on screen, which no caption holds.

## Evals

[evals/prompts.md](evals/prompts.md) lists the cases, each to run with and without the skill.
