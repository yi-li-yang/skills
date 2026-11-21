# Test prompts

Run each prompt in a fresh session, with no notes about the person's view in that domain unless the row says so. These check judgment, not rules: read each reply and ask whether a thoughtful adviser would have asked or answered at that stake.

| # | Prompt | What the skill should do |
| --- | --- | --- |
| 1 | Should I leave my job to go independent? | Fires. High stake, hard to undo, no lens on record: status line, a hypothesis, a few questions aimed at the hinges, and no answer yet. |
| 2 | How should I split my savings between my pension and my ISA? | Fires. High stake: asks first, unless memory already holds how the person thinks about money, in which case it names that lens and answers. |
| 3 | Which of these two names is better for my side project: Tidewell or Ledgerline? | Fires. Low stake: answers, names the guess about what the person wants from the name, and shows where the answer would fork. |
| 4 | Should I learn Rust or Go next? | Fires. Medium stake: answers with the fork made explicit ("if you want X, Rust; if Y, Go"), or asks one or two questions at most. |
| 5 | Is index investing still a good idea? | Fires, though it looks factual. Answers the general case and frames it by who is asking (horizon, goal), naming the guess. |
| 6 | How long does it take to learn Japanese? | Fires, though it looks factual. The answer depends on the goal and the hours; it names the guess or shows the range by goal. |
| 7 | What is the capital of Peru? | Does not fire, or fires and answers plainly with no status line. |
| 8 | Fix this failing test (paste any small failing test). | Does not fire. |
| 9 | Interview me first: how should I plan my week? | Fires and asks, even though the stake is small, because the person asked to be interviewed. |
| 10 | Which robot vacuum should I buy? | research-before-buy fires; this skill may run alongside it and supply the lens. |

## Trigger check

The status line is the signal. It must appear for prompts 1 to 6 and 9, and must not appear for 7 and 8. For each reply where it appears, check that the "stake" and "so" parts match the reasoning in the reply.
