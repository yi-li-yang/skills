# Wardrobe

The person owns the taste: they decide what looks good, what suits them and what to buy. This skill does the two jobs they cannot easily do in a shop.

- **The wardrobe record.** A record of what they own (brand, size, composition, construction notes, price, date and shop, care, how often it is worn), kept wherever they keep it, for example a page with a database, files or memory. It reads the record before asking, and leaves a field empty rather than guess.
- **A textile and industry expert.** For a piece they are looking at: what it is made of and how, whether the make matches the price, the brand's strengths and weaknesses for that line from sourced evidence, where it lands on their measurements and what could be altered, what they already own like it, the cost per wear, and what to check by hand.

It does not judge looks and does not give buy, wait or skip. Colour and proportion appear only as facts against the person's own record, such as whether a colour is in the palette they were given. The sourced findings behind its rules, each with how far it can be trusted, are in [evidence.md](../../plugins/yili-skills/skills/wardrobe/evidence.md).

Until version 2.1.0 the skill was a stylist that judged colour, outfits and proportion and gave buy, wait or skip. The role changed at my request, in pull request #5.

It does not generate images. When an image-generation or try-on tool is connected and asked for, it gets a yes before sending a body photo to an outside model, and says that the image shows drape and colour roughly, not true fit.

## Install

This skill ships inside the `yili-skills` plugin. Install the plugin, not the skill alone. The steps for Claude Code and for claude.ai are in the [repository README](../../README.md).
