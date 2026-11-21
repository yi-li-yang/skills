# Test prompts

Run each prompt twice, once with the skill and once without. Compare the outputs against the check.

| # | Prompt | What the skill must do |
| --- | --- | --- |
| 1 | Design a small pipeline that fetches web pages, cleans them and stores them. Name each stage. | Stage names are literal and stay the same through the answer. No witty names. |
| 2 | Explain what a race condition is to a new developer. | Plain sentences. Any metaphor is tied to the literal meaning and used once. |
| 3 | Explain backpressure in a streaming system. | A good metaphor (for example, water in a pipe) is kept, its literal meaning is stated, and it is not stripped. |
| 4 | Write a 150-word abstract for a paper on soil carbon turnover. | Not flattened into STE style. Normal academic voice. |
| 5 | Write a paragraph for a grant proposal that argues for funding a field trial. | Persuasive prose is kept. No STE flattening. |
| 6 | Write a short email that persuades a colleague to move a meeting. | Persuasive tone is kept. |
| 7 | Write a prompt for a subagent that reviews a pull request for security problems. | Steps are commands in order. One name for each thing. No idioms. |
| 8 | 请解释一下什么是缓存。 | The skill does not change the output. |
| 9 | Describe your progress after a long task (invent the task). | No idioms or slang. Facts and unknowns are stated plainly. |
| 10 | Rewrite this skill paragraph in plain English: "Open with one line: `🛒 research-before-buy 已启用 · 类型 · 决策轴`. This is the soul of the skill — become the category's expert, then decompose the price into substance and brand tax (溢价). Usually stop when nothing could flip the call; that's the flip test." | The meaning stays the same: "usually" is not made stronger, and no instruction is added or dropped. The status line and the Chinese text are not changed. "Soul of the skill" is replaced. "Brand tax" and "溢价" end up as one name. "Flip test" is kept, because the paragraph defines it. The reasoning stays as connected sentences, not a list of rules. |
| 11 | Write a short prompt for two subagents that work at the same time. One checks the links in a document, and one checks the spelling. | Each thing has one name across both prompts. No word has two meanings across the two prompts. |

## Trigger check

The skill must load for prompts 1, 2, 3, 7, 9, 10 and 11. For prompts 4, 5, 6 and 8, it must not load, or it must load and step aside.
