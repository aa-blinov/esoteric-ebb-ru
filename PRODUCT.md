# Product

<!-- impeccable:product-schema 1 -->

## Platform

A data package. The artifact is a folder of twelve CSV files that a copy of
Esoteric Ebb reads from its own `StreamingAssets` directory. The pipeline that
builds it is Python 3.12 and runs on Windows, Linux and macOS.

## Users

A player who owns Esoteric Ebb on Steam and reads Russian. They copy one
folder into the game, choose "Русский" in the options, and play. A second
audience is the translator: someone who wants to change a line, check how a
term is rendered elsewhere, and see that the change does not break the game's
markup.

## Product Purpose

The game ships English, and a Chinese translation by the community. This
repository holds the Russian one: every string of the game, translated into
one voice and measured so that the text fits the panels it has to fit in.

Success is a player who finishes the game without a single line breaking the
layout, and without meeting two different Russian words for the same thing.

## Positioning

The game already has a localization pipeline, a template folder and a guide
for translators. This repository follows that pipeline instead of inventing a
second one: the folder it ships is the folder the developer asks a translator
to produce, so it loads through the same code path as the official languages.

The part a neighbour could not copy is the glossary and the width measurements.
Two thousand two hundred repeated lines had been translated differently in
different places; one canonical wording each, bound to a glossary of 1,838
terms, is what makes the whole game read as one text.

## Operating Context

The player installs the game from Steam. The language folder is copied into
`Esoteric Ebb_Data/StreamingAssets/Localization/Russian`. The game is started,
the language is picked in **Options → Language**, and the choice is written to
`SETTINGS.es3`.

Inside the game, **V** and **B** cycle through the installed languages, and
**Ctrl+R** re-reads the CSV files without a restart, which is what a
translator wants while working.

A translator edits `translation/Russian/*.csv` in a text editor, runs the
tests, and copies the folder back. The game reloads it on the next start.

## Capabilities and Constraints

- The game reads the CSV files at startup. A change needs a restart, or
  **Ctrl+R** inside a running game.
- The game owns the fonts. The translation can only use the glyphs the shipped
  fonts carry; Noto Serif, Liberation Sans and OpenDyslexic all carry the full
  Cyrillic range, which is enough for the whole corpus.
- The panels are fixed size. A line that is too long wraps and overlaps the
  next block. Width is therefore a hard constraint, checked per line.
- The game's own dialogue size setting is the only global lever. It starts at
  24, which suits English; 20 is the value the Russian text is measured
  against.
- The corpus is the English source of one build, 1.3.5.3 (Open Beta). A game
  update that adds or changes lines leaves the new keys in English.

## Brand Commitments

The voice of the translation: sober, a little dry, literary where the source
is literary and spoken where the source is spoken. No translator jokes, no
modernisms that the setting does not have, no bureaucratic filler. The rules
are written down in `docs/style-guide.md`, and the editor pass works from
them.

## Evidence on Hand

- `translation/Russian/*.csv`: the translation, 81,883 filled cells in twelve
  files.
- `src/`: the pipeline, eleven Python modules and the style code they read.
- `tests/`: the checks that run in CI.
- `docs/`: the style code, the glossary, the layout measurements.
- `docs/screenshots/`: the game in Russian, taken from the build.

What does not exist: a native Russian speaker who has read the whole game
end to end, and a translation reviewed by a second pair of eyes.

## Product Principles

1. **One voice.** A term has one Russian word in this game. A second variant
   is a defect, not a variation.
2. **The layout is part of the text.** A line that does not fit its panel is
   wrong, whatever it says. Width is measured, not guessed.
3. **Nothing is invented.** The glossary carries what the game means, not what
   sounds better.
4. **The pipeline is reproducible.** Every change to the translation goes
   through a script that can be run again, with its model calls cached.

## Accessibility & Inclusion

The game has three dialogue fonts and three interface sizes. Two of the
dialogue fonts, Josefin Sans and Ebberia, carry no Cyrillic, so the settings
screen tells a Russian player to pick EB Garamond or PT Serif. A Russian
player's first minute in the options screen therefore has to make a choice
that an English player never has to make; that is a gap in the game, not in
the translation.
