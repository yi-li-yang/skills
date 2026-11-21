# Eval prompts

Run each prompt in a fresh session twice: with the skill installed and without it. Compare what each run read, what it brought back, and the tokens it used before it answered.

| # | Prompt | What good looks like |
| --- | --- | --- |
| 1 | What phrases does lesson 2 of this video teach? https://www.bilibili.com/video/BV1k94y1C7K9/ | The video has no captions. The run says so, finds lesson 2 (about 0:30), takes a frame there and reads the ten phrases from it. It does not guess them from the title. |
| 2 | In Steve Jobs' Stanford speech, what does he say the calligraphy class led to? https://www.youtube.com/watch?v=UF8uR6Z6KLc | The run searches the words for "calligraphy" or uses the chapters, and quotes the stretch with its timestamp (about 4:44). It does not read or send the whole transcript. |
| 3 | Is this robot vacuum review independent? (a review whose description or first minute names a sponsor or a gifted unit) | The finding lists the sponsor or the gift under who is speaking, with where it is stated. It gives the signal, not a verdict on the review. |
| 4 | What do owners say about this jacket after a winter? (a Xiaohongshu or forum post whose facts are in its photos) | The run reads the images, not only the text, and says which facts came from which photo. If the page needs a login, it uses the user's Chrome or says it could not reach the page. |
| 5 | What does this product cost right now? (a shop page with an add-to-cart button) | The run reads the price, the currency, the stock and the time it read them. It does not click anything that changes the page's state. |
| 6 | Which robot vacuums do long-term owners and independent testers rate in 2026, and why? | An open question: the answer maps the field and gives leads (models, reviewers, labs that come up again and again), with what each lead rests on. It stops when the map is clear, not after a fixed number of items. |

For token use, run prompt 2 with and without "most relevant first" and log the tokens used before the answer, as well as the answer's quality.
