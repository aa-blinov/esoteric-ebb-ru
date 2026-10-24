---
name: Esoteric Ebb RU
description: The typographic system of the Russian translation and the panel metrics it is measured against.
colors:
  accent: "#FF3959"
  panel-bg: "#141414"
  text: "#F2EDE4"
typography:
  body:
    fontFamily: "EB Garamond, PT Serif, Roboto, Ubuntu, serif"
    fontSize: "20px"
    fontWeight: 400
    lineHeight: 1.6
  title:
    fontFamily: "Noto Serif, serif"
    fontSize: "32px"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.02em"
  quote:
    fontFamily: "EB Garamond, serif"
    fontSize: "20px"
    fontStyle: italic
rounded:
  md: "8px"
spacing:
  sm: "8px"
  md: "16px"
---

# Design system: Esoteric Ebb RU

The game draws its own interface. What this repository designs is the text
that goes into it: the marks, the measures, and the limits the Russian has to
live inside.

## Overview

Two things decide whether a Russian line looks right in Esoteric Ebb: the
typography it carries, and the box it has to fit in. The game ships a serif
with full Cyrillic coverage, a panel layout that does not grow, and a
developer who measured his own English against it. The translation is measured
against the same numbers.

## Colors

The colour in the corpus is the game's own accent, `#FF3959`, used for the
ability names and the shout-lines. It arrives in the text as
`<color=#FF3959>` and is carried over unchanged. A translation has no palette
of its own; it does not add a colour that the English did not have.

## Typography

The rules below are the ones the editor pass applies, and the ones a hand
corrector applies.

- **Quotation marks.** Russian speech takes «ёлочки». Straight quotes were
  counted in the first build at 43,264 and are now at zero.
- **Dash.** The em dash, «—», with no space before it. A hyphen with spaces
  around it, the English habit, was reduced from 56 to 22.
- **Ellipsis.** One character, «…». The three-dot form was counted at 7,867
  and is now at zero.
- **Terminal punctuation.** A full stop before the closing guillemet, not after
  it: «Так и есть.»
- **Second person.** The game speaks to the player as «ты» in narration, in
  the rules and in the interface. A character may use «вы» when the character
  is formal, and that stays.

## Layout

The lore panel on the character screen is 541 px wide, and the text inside it
has about 500 px to work with. The display font spends about 0.70 em on a
capital letter, which gives the widths the measurement uses:

| Line | Size | Width | Panel |
| --- | --- | --- | --- |
| `EXTRA ITEMS` | 45 | 297 px | fits |
| `ДОПОЛНИТЕЛЬНЫЕ ПРЕДМЕТЫ` | 45 | 674 px | wraps |
| `ЛИШНИЕ ПРЕДМЕТЫ` | 45 | 454 px | fits |

The dialogue text size is the second lever. The game ships 24, which suits
English; at 24 the Russian text runs about 20 % longer than the English and
spills out of the panels. 20 brings it back to the English footprint, and the
setting is in the game's own options.

## Elevation & Depth

The game owns the depth. A translation adds no layer of its own, and the
`shadow` and `z-index` vocabulary of a web design system has no meaning here.

## Shapes

The game owns the shapes. The only measure the translation has to respect is
the width of the box a line lands in.

## Components

Two components carry text: the dialogue bubble, which grows with the text, and
the fixed panel, which does not. Only the second one constrains a
translation.

- **Dialogue bubble.** Any length is safe. 76,401 lines of dialogue live
  here.
- **Fixed panel.** The lore panel, the character sheet, the codex header. The
  width rule applies here, and the four lines that failed it were rewritten.

## Do's and Don'ts

- **Do** measure a line before it ships into a fixed panel.
- **Do** keep the game's own markup in the line, unchanged, in the same order.
- **Do** reuse the glossary word. A second variant for the same source line
  is a defect.
- **Don't** add a word that the English did not have. The Russian text is
  already longer; every addition costs a line.
- **Don't** shorten a line by dropping what it means. The width rule is
  solved by wording, not by cutting.
- **Don't** translate the incantations. The Latin of the game, «Manus arcana
  DOMINATUS», is part of its world.
