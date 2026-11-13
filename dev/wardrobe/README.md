# Wardrobe

A stylist's judgment for clothes. Given a person (height, build, colouring, style in their own words) and their wardrobe, it decides whether a candidate piece is worth buying: colour against their colouring, how many real outfits it makes with what they own, where its hem falls on their body, what the fibre and make are worth, and the cost per wear. It answers buy, wait or skip with the reason.

The skill carries method, not data. The wardrobe itself lives wherever the person keeps it (for example a page with a database, files, or memory), and the skill reads it from there.

It does not generate images. When an image-generation or try-on tool is connected, the skill uses it to show the outfit on the person, after asking; otherwise it says so and offers a proportion read and an outfit board, named as what they are.

## Install

This skill ships inside the `yili-skills` plugin. Install the plugin, not the skill alone. The steps for Claude Code and for claude.ai are in the [repository README](../../README.md).
