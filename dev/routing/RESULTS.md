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

## Forcing the reasoning skill to load on a conflict: tried, then rolled back

On 2026-11-21 the reasoning skill was made to load whenever sources conflict. The cue in each asking skill said to load the answering skill even if Claude could answer the question itself, a disagreement became a standing condition at any phase, and the reasoning skill's description led with disagreement inside other tasks. It then loaded in 6 of 6 frying-pan runs (0 of 5 before), and when a conflict first appeared during research, and still not for a kettle with no conflict.

It was rolled back the same day. Claude settling a conflict itself is acceptable: the connections are soft by design, and every run reached the same sound call with or without the reasoning skill, so forcing it added loads and text without a better answer. Two small changes from that work were kept, because they help whenever the skills meet: the reasoning skill's `[Thought]` marker gives way when another skill sets how the reply opens, and the reading skill reports each side where items disagree instead of choosing quietly. The commit that forced the loading, `0d6ad47`, shows how to do it again if it is ever wanted.

## Net price and timing: before and after (2026-11-23)

The purchase skill gained `references/net-price-and-timing.md`: what the person pays in the end by each route (what comes off at checkout, what money comes back and on which condition, what the route costs), and whether to pay now or later. Whole sessions with `session.py`, default model (Opus 5.5). "Before" is version 2.1.0, without the file. "After" is version 2.2.0 before three wording fixes (one name for instalment plans, the sentence on variants, "recovered").

| Prompt | Before | After |
| --- | --- | --- |
| "I've already decided on the Sony WH-1000XM6. It's Black Friday week in the UK: should I buy now or wait, and how do I get them cheapest?" | Buy this week at £298 from Amazon or Currys. It read the price history (PriceSpy, deal articles), called the "was" price an anchor, ruled out marketplace sellers for warranty risk and named Section 75. Cashback was "usually a few percent", with no condition. 0.56 USD, 73 s. | Same call, now argued as a bet with a cost on each side: waiting saves about £15 at best, and the colour may sell out at £298. It compared routes (Currys with cashback, Amazon, marketplaces, price matching), said that a voucher code cancels the cashback and that claims are sometimes declined, and found that other colours cost more. It did not name Section 75 this time, did not ask which cards the person holds, and the only step after buying was the returns window, not a check that the cashback tracked. 0.73 USD, 100 s. |
| "亚马逊上一台 Ninja 双篮空气炸锅，黑五标着原价 £249.99，现在 £129.99。家里还没有空气炸锅，值得买吗？" | Mostly worth it, but check the model. It called £249.99 an anchor, read camelcamelcamel, split the call between the 7.6 L and 9.5 L models, and asked whether two drawers fit the household. 0.50 USD, 63 s. | Same call. It also saw that a sale started the question, worked out the saving against the usual price (about £50–70, not £120), named the likely regret (a thing the home never had often goes unused) and made the now-or-wait call. 0.51 USD, 62 s. |
| "Which kettle should I buy?" (after only, to check proportion) | — | Pass. Discounts got one line ("if one of them is on sale, buy it then") and no hunt for codes. The interview skill also loaded, from the question in Phase 0; the kettle run on 2026-11-21 loaded only the purchase skill, so this is run-to-run variation. 0.51 USD, 52 s. |

The routing eval passed 5 of 5 (0.42 USD): a purchase already chosen and a "was" price in Chinese both loaded the purchase skill, "How do cashback websites make money?" did not, and two old cases still passed.

What this shows:

- **Much of the price work happens without the new file.** The history check, the "was" price as an anchor, the model-number check and the seller risk were all in the runs before. So the file holds only what was missing, and its worked example names only this person's own routes.
- **The file changed what it was written for.** Money back now comes with its conditions, waiting is weighed against its cost, variants are priced separately, and the saving is counted against the usual price, not the "was" price.
- **Three parts did not show up in one run each:** the person's own cards, the ordered steps, and the checks after buying. One run per prompt cannot separate the file from run-to-run variation, and the connections are soft by design, so nothing was added to force them.

The routing runner crashed twice on Windows before these results. It removes the temporary folder of a session it has just stopped, and Python 3.11's `TemporaryDirectory` recurses without end when that folder is still locked. Both runners now use `scratch_folder()` in `run.py`, which leaves such a folder behind instead.

Cost: 1.06 USD before, 1.75 USD after, 0.42 USD for routing, and two routing runs that crashed early.

### Reading where deal hunters already did the work (same day)

The question was whether the skill uses third-party sites such as MoneySavingExpert well. In the five runs above, Claude read PriceSpy, camelcamelcamel and hotukdeals on its own but never MoneySavingExpert, and the skill did not say how to weigh such places. `net-price-and-timing.md` gained a section, "Who has already done the hunt". It names three kinds of place: price trackers; deal communities, whose comments hold what the post leaves out; and consumer-advice sites, which are strong for how a discount works and for renewals and weak for whether this item at this price is right. Each is weighed by who is paid when a reader buys.

| Prompt | Version | Outcome |
| --- | --- | --- |
| "My broadband contract with Virgin Media ends next month, and the renewal price they quoted is £62 a month. What should I do?" | Before the section | It used MoneySavingExpert on its own: the haggling poll, the forum thread of Virgin retention deals and the comparison tool. It set the new-customer price as the target, and named One Touch Switch and Ofcom's rule that rises are stated in pounds. 0.48 USD, 58 s. |
| Same | Section in the reference only | It never opened the reference, did not use MoneySavingExpert, and said it found no reports of Virgin retention offers this month. 0.43 USD, 49 s. |
| Same | One sentence added to Phase 5 of SKILL.md | It used MoneySavingExpert's guide to haggling with Virgin, the forum thread and the poll again. Same call as before the section. 0.43 USD, 46 s. |
| The XM6 prompt above | Latest version | It read the reference. From hotukdeals threads it found student and Blue Light prices and a refurbished listing. It picked Argos for a price guarantee that runs to 25 December, so buying now costs nothing if the price falls, and gave the dates to check the price after buying. It also said that the sites it used earn from readers but mostly report the same price. Still no Section 75 and no question about the person's cards. 0.72 USD, 89 s. |

What this shows:

- **Claude already uses these sites well when the question points at them:** MoneySavingExpert for a broadband renewal, and hotukdeals and the trackers for a product. One run each cannot show that the section adds to that.
- **A reference helps only when the work reaches it.** The broadband run went from SKILL.md straight to search and never opened `net-price-and-timing.md`. So the idea now also has one sentence in Phase 5 of SKILL.md, which always loads.
- **The latest product run used more of the file than the first run after the change did:** discounts for who is buying, price protection as a way to make buying now safe, dates to check after buying, and a weight on sources that earn from readers.

Cost: 2.06 USD for these four runs.
