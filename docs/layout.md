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

## The lines that were rewritten

| Key | Before | After |
| --- | --- | --- |
| `AbilityScoreInfo_Strength_Uses1` | ДОПОЛНИТЕЛЬНЫЕ ПРЕДМЕТЫ | ЛИШНИЕ ПРЕДМЕТЫ |
| `AbilityScoreInfo_Dexterity_Uses2` | Как стремительный Разбойник | Как дерзкий разбойник |
| `AbilityScoreInfo_Constitution_Uses3` | Твоя политическая партия на прошлой неделе получила 2% голосов, и | Твоя партия набрала 2% за прошлую неделю, и |
| `AbilityScoreInfo_Strength_LoreFootNote` | `<size=33>БОЖЕСТВЕННУЮ МИССИЮ` | `<size=25>БОЖЕСТВЕННУЮ МИССИЮ` |

The Wisdom line keeps the word and lowers the size: the word was correct, the
box was not.

## The uses column

The third tab of the lore panel, **Польза**, is a narrow column. The English
names fit it; the Russian ones are a third wider, and a name that does not fit
is broken in two pieces: «НАЦИОНАЛИЗ» over «М», «МУЖЕСТВЕННО» over «СТЬ»,
«РЕСПУБЛИКА» over «НЕЦ», «ПОДГОТОВ» over «ИТЬ», «АЗГАЛИАНС» over «КОГО» and
«АПОЛИТИЧЕ» over «СКОЙ».

The column is not one width. The icons of the ability take room on both sides,
so СИЛА and МУДРОСТЬ are narrower than ИНТЕЛЛЕКТ. Every name was measured on
its own tab.

| Key | Before | After |
| --- | --- | --- |
| `AbilityScoreInfo_Strength_Uses3` | `<size=50>Национализм` | `<size=45>Национализм` |
| `AbilityScoreInfo_Strength_Uses4` | `Возросшая мужественность` | `Возрослое мужество` |
| `AbilityScoreInfo_Dexterity_Uses3` | `<size=55>Республиканец` | `<size=40>Республиканец` |
| `AbilityScoreInfo_Intelligence_Uses1` | `<size=65>Подготовить</size>` | `<size=40>Подготовить</size>` |
| `AbilityScoreInfo_Wisdom_Uses3` | `<size=62>Азгалианского` | `<size=44>Азгалианского` |
| `AbilityScoreInfo_Charisma_Uses3` | `<size=63>аполитической</size>` | `<size=42>аполитической</size>` |

Five names keep their words and lose only their size. **Мужественность** is
fourteen letters, and at the size of the line above it the name is 570 px
against a column of about 400. Lowering the size to fit would have made it half
the size of the line above it, so the word is shortened to **мужество**, which
reads the same in this context.

## The lore column

The lore panel of the character screen is one column. The quote, the
description, the footnote and the heading of the uses follow each other, and
the pink bubble that carries the character's comment covers the foot of the
panel.

The Russian description is a line shorter than the English one, so the heading
of the uses, **Большая Сила**, rose far enough to be seen under the bubble.
The footnote takes that line back. It is written as three lines of one
sentence each, and the name in capitals is one size smaller, so that it fits
the line and does not break in the middle of the phrase.

## The dialogue fonts

The game has seven fonts for the dialogue text: Ebberia, EB Garamond,
Josefin Sans, Open Dyslexic, PT Serif, Roboto and Ubuntu.

Two of them carry no Cyrillic: Ebberia and Josefin Sans. The game does not
show a missing glyph in them, it draws a rune, and a Russian line in either of
them comes out as a row of runes that cannot be read. Ebberia is the font of
the title of the game and the first entry of the list, so it is also the one
the game starts with: a Russian player has to change the setting before the
first line is readable. The installer moves the setting to Ubuntu when it
finds one of the two.

The other five draw the Russian well, and the player may pick any of them.

The font reaches further than the dialogue box. The description and the
footnote of the lore panel are drawn in the dialogue font, so the size of the
dialogue text decides how many lines they take and where the panel ends. The
quote, the tabs of the panel and the clock in the corner are drawn in the
display font of the game and do not move.

The size the translation is held to is **20**. At the default of 24 the
Russian description takes a line more than the English one, and the heading of
the uses rises under the bubble that covers the foot of the panel.

## The bar on top of the screen

The bar that names the open screen holds five names in a fixed height. The
English ones are one word each — `Questing`, `Inventory`, `Journal`,
`Spellbook`, `Sheet` — and the Russian ones were longer. «Поиск приключений»
broke into two lines and the second line fell out of the bar, and «Книга
заклинаний» ran past its right edge.

| Key | Before | After |
| --- | --- | --- |
| `Questing` | Поиск приключений | Задания |
| `Spellbook` | Книга заклинаний | Заклинания |
| `Keybind_Select` | Лист персонажа | Лист |

The two short names are the words the game itself uses: «выполняя ветви
заданий» and «используя заклинания».

## The buttons that hold one word

Two more buttons were narrower than their words. «Завершить» broke into
«ЗАВЕРШИ» and «ТЬ», and «Специализации» was flush with the edge of its panel.

| Key | Before | After |
| --- | --- | --- |
| `Menu_Button_Finish` | Завершить | Готово |
| `Sheet_Proficiencies` | Специализации | Профессии |
| `Menu_PreparingSpells_Collected` | Собранные заклинания | Собранные |
| `Menu_DeepStorage` | Глубокое хранилище | `<size=30>Глубокое хранилище</size>` |

The head of the panel that counts the collected cantrips and spells did not fit
the width of the panel, and the last letter was cut off.

The deep storage sits in a column of its own that is about 140 px wide. The
English name, `Deep Storage`, fits it. The Russian one is two words, and each
of them was a little too wide on its own: «Глубокое» broke into «ГЛУБОКО» and
«Е», and «хранилище» into «ХРАНИЛИ» and «ЩЕ». The size of the name is 30 now,
and both words fit the column and break at the space.

### What the translation cannot reach

The tooltip of a spell slot reads «ОТ ПРОВАЛА» over a number, and the two
overlap. None of the words in it are in the translation: «пр», «ОТ» and
«ПРОВАЛА» are in no Russian file of this repository, and they are in no string
of the game either, neither in UTF-8 nor in UTF-16. The developer ships a
partial Russian of their own in the assets, and the tooltip is drawn from it.

So there is nothing to shorten here. The only Russian word of that line that
belongs to the translation is `Failure`, and it already reads «Провал».

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

## The settings panel

The options panel has a column of labels on the left and a column of values on
the right. The value column is **140 px** wide and holds about ten Russian
letters; the label column is **216 px** and holds about eleven.

The English values are short: `Borderless`, `VSYNC`, `1920 x 1080`. The Russian
ones were not, and the panel breaks a word that does not fit: `Безрамочный`
became `Безрамочны` over `й`, and `ВЕРТИКАЛЬНАЯ СИНХРОНИЗАЦИЯ` took three lines
and rode up over the resolution above it.

| Key | Before | After |
| --- | --- | --- |
| `Settings_RefreshRate_VSync` | ВЕРТИКАЛЬНАЯ СИНХРОНИЗАЦИЯ | `VSYNC` + a non-breaking space |
| `Settings_DisplayMode_Option1` | Полноэкранный | Полный экран |
| `Settings_DisplayMode_Option2` | Безрамочный | Без рамки |

The refresh rate keeps the name the game's own English string uses. The two
display modes keep their meaning and lose only the letters that did not fit.

### The trailing space

The value of the refresh rate is written twice by the game, and the two
formats are not the same. The caption of the field reads `{0} ({1})` and shows
`VSYNC (144)`. The entries of the open list read `{0}({1})` and showed
`VSYNC(72)`, with no space at all.

The string therefore carries a space of its own. It is a non-breaking space,
`U+00A0`, and not an ordinary one:

- an ordinary space at the end of the cell is trailing whitespace, and the
  house style bans it;
- quoting the cell does not help. The game reads the CSV with its own reader,
  which drops the Russian localization when a cell is quoted, and the whole
  interface falls back to English.

The non-breaking space survives the reader, the renderer draws it as a space,
and the style check does not see it. The list entries read `VSYNC (72)` now,
and the caption reads `VSYNC (144)`, whose gap is a fraction wider than the
English one.

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

## The tips of the loading screen

While a save is loading, the game shows a tip: a title in orange, a rule under
it, and the text of the tip below. The rule is **499 px** wide, and the title
has to stay on one line above it. A title that does not fit breaks, and its
second line is drawn over the first line of the text.

The title is drawn in the size **35**, and the width of a line follows the
advance widths of the font:

```
width in px = size × (sum of the advance widths of the letters, in em)
```

The table was taken from four titles that were measured on the screen of
the game, and it is accurate to about one percent:

| Title | Measured | Computed |
| --- | --- | --- |
| `ЧЕРТЫ` | 120 px | 122 px |
| `ПОДГОТОВКА` | 240 px | 243 px |
| `ЗАКЛИНАНИЙ` | 239 px | 241 px |
| `ЭЗОТЕРИЧЕСКИЕ СОБЫТИЯ` | 499 px | 500 px |

Eleven of the Russian titles are wider than the rule. They keep their words and
get a smaller size, so that every one of them measures less than 478 px:

| Key | Size |
| --- | --- |
| `Loading_Title_AbilityScore` | 26 |
| `Loading_Title_AbilityScoreMod` | 26 |
| `Loading_Title_DivineIntervention` | 26 |
| `Loading_Title_SpellConcentration` | 27 |
| `Loading_Title_LockedChecks` | 29 |
| `Loading_Title_QuestingTree` | 29 |
| `Loading_Title_HiddenDialogChoices` | 29 |
| `Loading_Title_SituationalSpells` | 30 |
| `Loading_Title_EsotericEvents` | 33 |
| `Loading_Title_PreparingSpells` | 33 |
| `Loading_Title_SpellCasting` | 33 |

The line at the bottom of that screen had the same trouble. «Нажмите любую
клавишу, чтобы продолжить» is 41 characters and needs 566 px, and the rule
there is 500 px wide, so the word «ПРОДОЛЖИТЬ» fell on the rule. The prompt
is «Нажмите любую клавишу» now, and it measures 290 px.

Four tips were loaded and looked at on the screen of the game.
«ДРЕВО ПОИСКА ПРИКЛЮЧЕНИЙ» is one of the eleven titles of the table, and it
stays on one line. None of the four reached the line of text.

## The character sheet

The sheet of the character carries three panels of its own: the lore, the
benefits and the role. All three were checked with the Russian text in place.

The names of the six abilities fit their cards. «ТЕЛОСЛОЖЕНИЕ» is the longest
of them, and the engine shrinks that one on its own: it draws in a smaller
size than «СИЛА» or «МУДРОСТЬ», and it keeps its margins both sides.

The benefits panel fits as well. Its heading «Большая Сила» sits inside the
panel, the two lines below it stay on their own lines, and the notice bar at
the bottom reads «Механические преимущества Силы». The role panel carries a
list of fourteen points, and every one of them stays on a single line.

One thing on that screen belongs to the game and not to the translation. When
the sheet opens for the first time, the benefits panel is still drawn where it
was left, and the heading «Большая Сила» comes out under the notice bar of the
lore panel, half covered by it. The first click on any of the three tabs puts
the panel where it belongs, and the text stays there for the rest of the
session.

## The splash screen

The prompt on the first screen of the game is drawn over a painting, and the
painting is in front of the text on the left. The clear band of sky at the
height of the line runs from **x = 519** to **x = 1249**.

| Line | Size | Width | Result |
| --- | --- | --- | --- |
| `PRESS ANY BUTTON` (English) | 54 | 504 px | fits |
| `НАЖМИТЕ ЛЮБУЮ КНОПКУ` | 54 | 778 px | the first word goes under the cloud |
| `НАЖМИТЕ ЛЮБУЮ КНОПКУ` | 36 | 517 px | fits |

The line is centred, so the width is what decides the outcome. At size 36 the
Russian line measures the same as the English one and stays in the open sky.

## The panel of the background focus

The panel that describes the background of the character carries the name of
the background in a line of its own, with the date of the world above it. The
name is drawn in a display font that spends about **20 px** on a capital
letter, and the line holds about **340 px**.

The Russian names are longer than the English ones, and the longest three did
not fit:

| Name | Width | Result |
| --- | --- | --- |
| `ДВОРЦОВАЯ ПЕШКА` | 320 px | fits |
| `НОВОБРАНЕЦ УРТГАРДА` | 360 px | breaks, the second line lands on the date |
| `РЕВОЛЮЦИОННЫЙ ПИСЕЦ` | 390 px | breaks |
| `ЭЗОТЕРИЧЕСКИЙ ЭКСПЕРТ` | 430 px | breaks |

The names were rewritten instead of shrunk: «Эзотерик», «Писец революции» and
«Рекрут Уртгарда». Eight of the backgrounds were drawn and looked at on the
screen of the game, and every name of them stays on one line.

## The deep storage

The button of the deep storage carries an icon and the name in two lines, and
the text of the name has about **117 px** to work with. «ГЛУБОКОЕ ХРАНИЛИЩЕ»
needs 158 px at the size of 30, so the display font broke both words in the
middle and the second one fell out of the panel. The size of the name is 20
now, and the two words fit on their own lines.

## The names of the interaction

The icons that open around an object carry a name in a plate of about
**95 px**, and the plate belongs to the game. The names of the game are one
word each. Three of the Russian ones fit: «Войти», «Мелочь» and «Смотреть».

«Вступить в бой» needs **145 px** and came out of the plate on both sides.
The Chinese translation reads the same key as 交谈, a talk, and the icon
next to it is a speech bubble, so the name was not the right one to begin
with. It is «Говорить» now, and the name of the hand is «Взять».

## Checking a line yourself

```bash
python3 scripts/measure_width.py            # the widths of the known cases
python3 src/verify_final.py                 # the width of every line in the corpus
```
