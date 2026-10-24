# Layout

The game draws its interface in fixed boxes. A line of Russian that does not
fit its box wraps, and the wrapped part overlaps whatever sits below it. This
document records the measurements the translation is held to.

## The panel

The lore panel on the character-creation screen is **541 px** wide, which
leaves about **500 px** of text inside it. Two kinds of text live in the
game, and only one of them constrains a translation:

| Kind | Count | Constraint |
| --- | --- | --- |
| Dialogue bubble | 76,401 lines | None. The bubble grows with the text. |
| Fixed panel | 5,482 lines | The width above. |

## The font

The display font of the game spends about **0.70 em** on a capital letter.
That number comes from the game's own screen, not from an estimate, and it is
what the width rules use.

## What the measurement showed

The first build of the translation had these lines in the lore panel:

| Line | Size | Width | Result |
| --- | --- | --- | --- |
| `EXTRA ITEMS` (English) | 45 | 297 px | fits |
| `ДОПОЛНИТЕЛЬНЫЕ ПРЕДМЕТЫ` | 45 | 674 px | wraps, overlaps the line below |
| `Higher Strength` (English) | 38 | 286 px | fits |
| `Большая Сила` | 38 | 431 px | fits |

Russian needs more characters than English for the same thought, and the
difference is enough to push a display-size line out of the panel. The
measurements were taken against the real font data out of the game's assets:
`scripts/measure_width.py`.

## The four lines that were rewritten

| Key | Before | After |
| --- | --- | --- |
| `AbilityScoreInfo_Strength_Uses1` | ДОПОЛНИТЕЛЬНЫЕ ПРЕДМЕТЫ | ЛИШНИЕ ПРЕДМЕТЫ |
| `AbilityScoreInfo_Dexterity_Uses2` | Как стремительный Разбойник | Как дерзкий разбойник |
| `AbilityScoreInfo_Constitution_Uses3` | Твоя политическая партия на прошлой неделе получила 2% голосов, и | Твоя партия набрала 2% за прошлую неделю, и |
| `AbilityScoreInfo_Wisdom_Uses3` | `<size=73>Азгалианского` | `<size=62>Азгалианского` |

The last one keeps the word and lowers the size: the word was correct, the
box was not.

## The clock in the corner

The panel in the lower right corner of the game screen carries the time of day,
a rule, and the day it belongs to. The English label is `Day {0}`, which the
display font draws as **DAY 1** in 94 px.

The Russian `День {0}` needs 123 px. The label is one line high, so the number
wrapped onto a second line, the word rode up over the rule, and the number was
drawn below the panel.

The label is `день {0}` now. Lower case needs 107 px and fits on one line, and
the display font draws lower case as small capitals: the label reads **ДЕНЬ 1**,
the same shape as **DAY 1**. The same string builds the summary of a saved
game, where it reads `день 1 - 08:10`.

A non-breaking space between the word and the number does not help: the text
engine breaks the line at it as well.

## The global lever

The game has a "Dialog Text Size" preference, 24 by default and tuned by the
developer for English. At 24 the Russian text runs about 20 % longer than the
English and spills out of the panels that the English just fits into. At 20 it
occupies the English footprint.

The setting lives in the game's own settings file:

```json
// %USERPROFILE%\AppData\LocalLow\Christoffer Bodegard\Esoteric Ebb\SETTINGS.es3
"FontSize" : { "__type" : "int", "value" : 20 }
```

A Russian player can change it in **Options → Text**. The right-hand panel of
that screen shows the result live, which is the quickest way to judge whether
a setting is comfortable.

## The rest of the screen

The character sheet carries 74 labels whose Russian text outgrew the English
one. 23 of them were rewritten more compactly, with the meaning and the voice
kept; the rest are short labels where a difference of three characters does not
change the layout.

Five strings in the lore panel overlap their neighbours in the English build
as well: the badge row of the role description sits on top of the last line of
the text, and the game has always done that. The Russian is not the cause.

## Checking a line yourself

```bash
python3 scripts/measure_width.py            # the widths of the known cases
python3 src/verify_final.py                 # the width of every line in the corpus
```
