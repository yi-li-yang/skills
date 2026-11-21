# Results

Runs on 2026-11-21, Claude Code 2.1.329, default model (Opus 5.5), with this repository's plugin loaded in place of the installed copy. Costs are what the CLI reported.

## Routing eval

`python dev/routing/run.py`: 11 of 12 cases passed on the first run (about 1.18 USD).

- Each skill loaded for its own prompt: a purchase, a clothing buy, getting up to speed on a field, a stated need for "what an expert in this category knows now", a job decision, two conflicting tests, a video link, a request for what owners and labs actually show, an email, a concept to explain. `What is 17 times 23?` loaded none of the skills, as it should.
- The one failure was the case where two skills need each other (a coat that suits me, and which shop to buy it from). The runner stopped the session at its first other tool call, after the clothing skill had loaded and before the purchase skill could. Such cases now take a `patience` count. A rerun with patience still loaded only the clothing skill, because the routing runs have no web tools and the session ended without shopping research. The full session below, with web tools, loaded both.

## Whole sessions

`python dev/routing/session.py`, with web search and web fetch allowed.

| Run | What it checks | Skills loaded | Outcome |
| --- | --- | --- | --- |
| Coat: does it suit me, and where to buy it | Two skills that need each other | the clothing skill, then 25 s later the purchase skill; each once | Pass. Each answered its own question once, and neither loaded again. |
| Kettle, low stakes | A purchase with nothing to resolve | the purchase skill only | Pass. Four searches, a safe default, no other skill. |
| Frying pan, two sources disagree | The question *which evidence do I believe?* should find its skill | the purchase skill only, in five runs | **Not met.** In every run Claude settled the conflict itself, from how the coatings work, and did not load the reasoning skill. All four briefs reached the same call. |
| Same, with the reasoning skill removed | A missing skill | the purchase skill | Pass. Same call, same reasoning. |
| Same, with no subagents | No agents, as on claude.ai | the purchase skill | Pass. Same call. |
| Same, with the old `source-weighting.md` | Weighting A/B | the purchase skill | Same call. The old file's run searched once more and named the test method behind the conflict; the new file's runs searched less. One pair of runs cannot separate the file from run-to-run variation. |
| Material request, with the reading skill renamed | A rename | the renamed skill | Pass. It was found by its description alone. |
| Robot vacuum under 600 pounds, cat, hard floors (first run) | Research in waves; needs inside the purchase skill and inside subagents | main: the purchase skill, then the expert skill; each of the three research subagents: the reading skill and the reasoning skill | The purchase skill asked what an expert in the category knows now, and the expert skill loaded. It sent three subagents (independent tests, what owners report going wrong, UK prices before Black Friday); each found both skills from its brief alone. The record stopped at the main turn's first result, while the subagents were still working, so the final brief and any second wave were not seen. The session script now keeps reading until the session ends. 4.1 USD before the cut. |
| Robot vacuum, second run, same prompt | The same | the purchase skill only | A different path: no subagents and no other skill. Five web searches, then a full brief from what the search results said (0.55 USD, 79 s). The purchase skill had judged search results enough. It now says that a search result about a review is a lead, not evidence, and that an unknown that could change the call is settled by what the review, the owner's report or the test itself says and shows. |
| Get up to speed on how a robot vacuum holds up after a year (capped at 4 USD) | Needs inside the expert skill's research briefs | main: the expert skill; each of its four research subagents: the reading skill and the reasoning skill | Pass for routing. The brief states its two questions, and all four subagents found both skills from them. They read owner reports, tester reviews and German and Chinese communities through web search and fetch (105 calls); none ran the video scripts. A check agent then verified the claims against their sources. Writing the briefing to the home folder was refused by the eval's permissions, so it went to the session's scratchpad. 2.66 USD, 328 s. |
| Robot vacuum, third run, after the evidence change | Does the purchase skill now read the material itself? | the purchase skill only | Partly. It sent two page-reading subagents to report "what their actual tests show (not marketing)" and found that two testers disagree about hair tangling, but it used a subagent type that can only fetch pages, so no skill could load and no video was read. 0.83 USD, 163 s. The purchase skill now says to give each research subagent the question as written, to tell it to check its skills, and to use a subagent that can use skills and run scripts. |
| Robot vacuum, fourth run, after the brief change | The full chain | main: the purchase skill, then the expert skill; each of the three research subagents: the reading skill and the reasoning skill | Pass. Three general-purpose subagents (UK line-up and prices, pet-hair and rug tests, dock size and reliability) each found both skills. The brief rests on test data, such as one tester's hair-wrap test and obstacle scores, and names what it could not confirm. No video was opened: the subagents ranked text test pages first. 3.48 USD, 307 s. |

## Reading material: with and without the reading skill

| Prompt | Without the skill | With the skill |
| --- | --- | --- |
| What phrases does lesson 2 of this Bilibili video teach? (no captions) | Could not answer: read the page, the danmaku and the comments through the API, then said it cannot watch video. 0.32 USD. | Found that there are no captions, took frames at 0:05, 0:30 and 0:55, found lesson 2 at 0:30 and read all ten phrases from the frame. It said it read the screen and did not hear the audio. 0.37 USD, 38 s. A first run could not open the frames, because the eval session had no permission to read files outside its folder; the skill now says to save frames where the session can read them. |
| What maintenance problems did this reviewer report after a year, and where? (a 19-minute YouTube review with 952 views) | Could not answer. It tried YouTube's caption endpoint, two third-party transcript sites and two Invidious mirrors, and its yt-dlp commands were refused, because the eval allowed only `python` commands. 0.42 USD, 66 s. In an interactive session it could have asked to run yt-dlp, so this part of the gap comes from the eval's permissions. | Used the chapters and searched the words; returned the routine upkeep with timestamps (10:55–11:40), the one recurring jam from another chapter (9:34) and the verdict (16:43), quoting only the reviewer's key words. 0.42 USD, 30 s. |
| What does Jobs say the calligraphy class led to? (the 2005 Stanford speech) | Fetched Stanford's transcript; correct. | Answered from memory without opening anything; correct. A famous video is a poor test, so this case was replaced by the review above. |

YouTube refused caption downloads from this network with HTTP 429 for some minutes during the runs. The script now retries twice and then reports the block, and the skill records a pointer when that happens.

## What this shows

- **Routing by question works.** Every skill loads for its own question, a renamed skill is still found, and two skills that need each other each answer once.
- **Subagents find skills from their brief.** Whenever a brief stated the questions, all 10 research subagents across three sessions loaded the reading skill, and 9 of them also loaded the reasoning skill.
- **Inside a running skill, Claude often answers a need itself.** In five purchase runs with conflicting sources, Claude settled the conflict without loading the reasoning skill. In two of four robot-vacuum runs it did not send research subagents at all. The connections are soft, so every one of these runs still gave a sound answer, but a need is not guaranteed to fire.
- **Removing a skill, renaming one, or taking subagents away did not break a run.**
- **Video reading works when the question is about a video** (the Bilibili and YouTube cases). In purchase research the subagents ranked text test pages above videos, so no video was opened there.

Total cost of the runs above: about 21 USD (18.91 for whole sessions, 1.79 for the routing eval), plus three sessions that were stopped early.
