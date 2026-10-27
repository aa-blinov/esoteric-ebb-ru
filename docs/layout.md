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
| `ЛИШНИЕ ПРЕДМЕТЫ` (Russian, Noto Serif) | 45 | 495 px | fits within 500 px |

Russian needs more characters than English for the same thought, and the
difference is enough to push a display-size line out of the panel. The
measurements were taken against the real font data out of the game's assets:
`scripts/measure_width.py`.

## The lines that were rewritten

| Key | Before | After |
| --- | --- | --- |
| `AbilityScoreInfo_Strength_Uses1` | ДОПОЛНИТЕЛЬНЫЕ ПРЕДМЕТЫ | ЛИШНИЕ ПРЕДМЕТЫ |
| `AbilityScoreInfo_Dexterity_Uses2` | Как дерзкий разбойник | Как лихой плут |
| `AbilityScoreInfo_Constitution_Uses3` | Твоя политическая партия на прошлой неделе получила 2% голосов, и | Твоя партия набрала 2% за прошлую неделю, и |
| Third line of `AbilityScoreInfo_Strength_LoreFootNote` | `<b><size=33>DIVINE MISSION</b>` | `<b><size=25>U+200B</b>` (invisible) |

The Wisdom line keeps the word and lowers the size: the word was correct, the
box was not.

The Dexterity class label `Как лихой плут` measures 276 px in the selected
Noto Serif font at size 35. It fits the 325 px uses column.

## Glossary notes

`Glossary_Response_706` now reads «Толк» по-дворфски значит «переводчик».
At size 22, it measures 472 px in the game's Noto Serif font and fits the
500 px text area on one line. The revised `Glossary_Response_690` wraps to five
lines at the same size; its widest line measures 474 px.

The corrected glossary names were measured in the installed Noto Serif font
at size 22. The longest, «Ожерелье огненных шаров», measures 302 px; «Кланленды»
measures 128 px. Both fit within the 500 px panel.

The Urth terminology entries were measured in the same font at size 22. The
text wraps at spaces within the 500 px area:

| Key | Lines | Widest line |
| --- | ---: | ---: |
| `Glossary_Response_4` | 4 | 431 px |
| `Glossary_Response_104` | 5 | 483 px |
| `Glossary_Response_574` | 7 | 489 px |
| `Glossary_Response_575` | 9 | 484 px |
| `Glossary_Response_576` | 5 | 447 px |
| `Glossary_Response_577` | 7 | 485 px |

The Halfway entries use the same Noto Serif font at size 22. The long
description breaks into seven lines, and its widest line measures 475 px.
The shorter definitions use two and six lines, with widest lines of 469 px
and 486 px. The full name «Племя Моста на полпути» measures 281 px.

| Entry | Lines | Widest line |
| --- | ---: | ---: |
| `Glossary_Response_158` | 7 | 475 px |
| `Glossary_Response_406` | 2 | 469 px |
| `Glossary_Response_501` | 6 | 486 px |
| «Племя Моста на полпути» | 1 | 281 px |

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
| `AbilityScoreInfo_Charisma_Uses3` | `<size=63>аполитической</size>` | `<size=28>Аполитичная</size>` / `<size=40>силой природы` |

Five names keep their words and lose only their size. **Мужественность** is
fourteen letters, and at the size of the line above it the name is 570 px
against a column of about 400. Lowering the size to fit would have made it half
the size of the line above it, so the word is shortened to **мужество**, which
reads the same in this context.

### Charisma benefit

The first Charisma benefit shares its narrow 325 px text slot with an icon.
The old heading wrapped into two lines, and the explanatory line and store
note wrapped too. Together they pushed the lower text into the tab strip. The
first benefit occupies four lines. The third now uses a 28 px emphasized
adjective and a 40 px second line; live review confirmed that both words stay
intact and the text remains inside the panel:

| Line | Size | Width in the widest extracted font |
| --- | ---: | ---: |
| `Высокая Харизма` | 20 | 287 px |
| `сразу получаешь` | 22 | 316 px |
| `СКИДКУ` | 48 | 288 px |
| `в некоторых лавках` | 18 | 301 px |

All four lines fit the 325 px slot. The sizes and widths come from the real
font assets measured by `src/ebru/measure_width.py`. The installed copy was
reloaded in the running game with Ctrl+R.

## The lore column

The lore panel of the character screen is one column. The quote, the
description, the footnote and the heading of the uses follow each other, and
the pink bubble that carries the character's comment covers the foot of the
panel.

The Russian description is a line shorter than the English one, so the heading
of the uses, **Большая Сила**, rose far enough to be seen under the bubble.
The footnote was set in three short lines, with its all-caps phrase reduced to
size 25 to fit. The third line still showed through the black notice band in
the live panel, so it is now an invisible placeholder. The first two lines
(«Стань ФАНАТИКОМ. Верни свою честь.») and the separate black notice text
(`AbilityScoreInfo_Strength_LoreNotice`) stay visible.

### Strength description after the wording fix

The description has **371 characters including markup**. At font size **22**,
it wraps to **10 lines** in the live 1920 × 1080 screen. Pixel bounds of the
rendered text show a widest line of **497 px** in the roughly **500 px** text
column. The third line of the Strength footnote is replaced by a zero-width
space because it showed through the notice band. The first two footnote lines
remain in the translation, and the black notice text remains visible.

### Charisma footnote

The original Charisma footnote wrapped to seven lines, with its last line
running into the illustration above the magenta notice. The shortened wording
keeps the same five ideas: persuasive speech, factional affiliation, reality
shaped by will, the chameleon-like social operator, and the need to be loved.
At font size **20**, it wraps to **five lines** in the extracted Noto Serif
font; the widest line is **492 px** in the **500 px** text column. The separate
black notice (`AbilityScoreInfo_Charisma_LoreNotice`) remains visible.
After a full game restart, the character creation screen confirms that the last
line stays above the illustration and the black notice is unobstructed.

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

The size the translation is held to is **22**. At the default of 24 the
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

The earlier lowercase fix did not hold in the live HUD: a fresh screenshot
showed that the day label still wrapped into the clock. The pipeline had also
restored `День {0}` because the correction was not persisted as a manual fix.
The label is now `дн. {0}`; the abbreviation keeps the meaning while leaving
room for the day number on the HUD. After a full restart, a live 1920 × 1080
capture showed `дн. 1` on one line below the clock, with no overlap. The
saved-game summary uses the same key and also fits on one line.

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
English and spills out of the panels that the English just fits into. At 22 it
occupies the English footprint.

The setting lives in the game's own settings file:

```json
// %USERPROFILE%\AppData\LocalLow\Christoffer Bodegard\Esoteric Ebb\SETTINGS.es3
"FontSize" : { "__type" : "int", "value" : 22 }
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

At reference size 24 in the game's Klee One font, the intro skip label
`Пропустить` measures **240 px**. The shorter `Пропуск` measures **168 px**, a
30% reduction.
The black loading screen was also checked live: «Нажмите любую клавишу» and
the `100%` progress value stay clear of each other.

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

## The statistics of the character sheet

The panel of the character that stands on the right of the inventory lists
the statistics of the character. The names of the rows are right-aligned in a
column of about **170 px**, and every one of them has to stay on one line: a
name that breaks takes the line of the row below it.

| Name | Result |
| --- | --- |
| `Очки здоровья` | breaks after «Очки», «Здоровья» falls on the row of the dice |
| `Кубики здоровья` | breaks after «Кубики» |
| `Владение` | fits at 97 px in Noto Serif at size 20 |
| `Очки` | fits |
| `Кубики` | fits |
| `Бонус` | fits |

The name of the empty feat slot had the same trouble: «[Пустой слот для
умения]» needs 270 px in a row of 195 px, and the second line crossed the
rules of the rows below. It is «[Пустой слот]» now.

The description of the dice called them «Кости здоровья» while the name of
the row called them «Кубики здоровья». Both say «кубики» now.

## The tooltip of an item

The name of the type of an item is drawn in a plate that is one line tall and
about **215 px** wide, on the left edge of the screen. A name that does not
fit breaks, and its second line comes out under the plate.

| Name | Width | Result |
| --- | --- | --- |
| `КНИГА ЗАКЛИНАНИЙ` | 16 letters | breaks, «ЗАКЛИНАНИЙ» falls out of the plate |
| `ГРИМУАР` | 7 letters | fits |

The names of the types are short now: «Гримуар», «Ключевой», «Мод. СИЛ»,
«Мод. ЛОВ», «Мод. КОН», «Мод. ИНТ», «Мод. МДР» and «Мод. ХАР». The three
letters of the abilities are the ones the game itself uses in the rolls of
the spells.

## The notes of the session

The panel of the session notes carries a heading, a rule under it, and the
date of the save. The rule follows the heading and the date is written on the
same line, so the rule cuts the top off the digits of the date.

The date belongs to the game, and the heading is ours. The heading is written
in the size 38 now, so that the rule lifts off the date. The heading measured
about 34 px of cap height at the size 43.

## The light mode

The game rebuilds parts of the interface when the light mode is switched at
runtime. The panels it rebuilds take their text from the strings of the game
itself, and not from the folder of the language, and the Russian build shows
them in English: the column of examples next to the settings turns into
`When I play Ebb, I use text size 24...` while the same panel reads
«Когда я играю в Эбб, использую размер текста 24...» before the switch.

That the strings come from the game and not from the folder is easy to see:
a line of ours that is emptied shows the English original in its place, the
pink plate of the panel of the character sheet reads
`The Cleric's unique take on Strength.` as soon as the line is empty. The
game holds the English source in its own assets, and the developer put his
own Chinese into the same place, which is why the Chinese build keeps its
Chinese after the same switch.

The rest of the interface is not affected: the menus, the bar of the
character sheet, the clock and the game itself stay Russian after the
switch. A restart of the game reads the localization again, and the panel is
Russian again.

## The tagline of the title screen

The line under the title of the game comes from the caption of the panel of
Strength (`AbilityScoreInfo_Strength_LoreNotice`), which the developer uses as
the tagline of the game. The English source reads
`The Cleric's unique take on Strength.`, and the Russian reads
«Собственный подход Жреца к Силе.».

The line cannot be taken away by emptying it: a line of ours that is empty is
replaced by the English original of the game, as the panel of the character
sheet shows when its line is empty. A line that holds nothing but a
non-breaking space does the same, because the game trims the spaces before it
looks.

The zero width space (`U+200B`) is the one thing that keeps the game from
falling back to the English original: it is not a space, so the game does not
trim it, and the font draws nothing for it. The band of the title screen stays
and stays empty that way, and the band of pink of the panel of Strength does
the same.

The caption itself stays in Russian, because the panel of Strength shows it
as its caption and the player reads it there.

## The name of the proficiency

The mark next to the name of an ability says whether the character is
proficient in it. The English word is `Proficient`, and the lore of the game
speaks of proficiency in the words of the translation: «Ты владеешь двумя
характеристиками» (`Loading_Desc_Proficiency`) and «бонус владения»
(`SpellDescription_20`). The name is «Владение» now, the word the lore itself uses, and it fits the
room of the mark. The loading title and character sheet use the same label.
«Владение» measures **97 px** in the installed Noto Serif at size 20, within
the sheet's **170 px** column. «Умелый» was the word before, and the lore
never uses it.

## The card of the collected spells

The card that counts the spells of the character has a width of about **182 px**,
and the name of the card and the two names of the counts share it. The count
itself is drawn by the game and keeps the size of the panel, so a count of
two digits needs about 28 px next to the name.

| Name | Size | Width | Result |
| --- | --- | --- | --- |
| `КАНТРИПЫ 0` | 20 | 119 px | fits |
| `ЗАКЛИНАНИЯ 1` | 20 | 139 px | the name reaches the count |
| `ЗАКЛИНАНИЯ 12` | 20 | 156 px | the count and the name touch |
| `КАНТРИПЫ` | 16 | 95 px | fits |
| `ЗАКЛИНАНИЯ` | 16 | 111 px | fits |

The two names are written in the size 16 now. The size of the panel is 20, and
the tag of the size does change the name on this element, which was measured
on the screen of the game.

## Alignment labels

The character sheet gives each word of an alignment about **140 px** and draws
the names in capitals. In the game's Noto Serif at size 20, «НЕЙТРАЛЬНЫЙ»
measures **161 px**, «ХАОТИЧНЫЙ» measures **136 px**, and
«ЗАКОНОПОСЛУШНЫЙ» measures **228 px**. «НЕЙТРАЛЬНЫЙ» now uses size 16 and
measures **129 px**. «ХАОТИЧНЫЙ» uses size 19 and measures **129 px**. The
long lawful label is shortened to the canon term «ЗАКОННЫЙ», which measures
**121 px**. All nine options keep their two-line form and fit within the field.

## Checking a line yourself

```bash
python3 scripts/measure_width.py            # the widths of the known cases
python3 src/verify_final.py                 # the width of every line in the corpus
```


## The short name of the City Below

The area label uses the short name «Подгородье». In the installed Noto Serif
font at size 22, it measures **131 px**, within the **500 px** fixed panel. The
revised divine choice «Направь силу Урта.» measures **216 px** at the same size.
The sphinx-riddle line «ПРАЙМЛ-СТРУНА покажет, чего ты стоишь.» measures
**485 px**, within the 500 px area. The verse lines are separate dialogue entries,
so each one opens and closes its own guillemets.

The saved-game menu button uses the short label «Дальше»: the longer
«Продолжить» measures **127 px** in the installed Noto Serif at size 20 and
wraps over the save card in the running game. «Дальше» measures **79 px** at
the same size and stays on one line.

## Lore glossary measurements

All 723 non-empty glossary descriptions were checked against the installed
`NotoSerif-Regular` font at size 22, using the game's 500 px text area and
wrapping at spaces. No individual word is wider than the panel. The longest
description is `Glossary_Response_707`: it wraps to 15 lines, with a widest
line of about **496 px**. The revised Old Diminor entry wraps to 7 lines, with a widest
line of **469 px**. The restored ASAP explanation wraps to 6 lines, with a
widest line of **487 px**; the dwarf drill entry wraps to 5 lines, with a
widest line of **485 px**; the «секс» entry wraps to 2 lines, with a widest
line of **445 px**. Measurements use font assets extracted by
`src/ebru/measure_width.py` from the installed game.

The harmonized glossary labels «Пустяк» and «Почтальон» measure **78 px**
and **121 px** respectively in the same font at size 22, within the panel's
500 px width. The synchronized lore terms «Тростников» and «Ропер» measure
**130 px** and **66 px** respectively at the same size. «Тропа Подбережья»
measures **209 px** in the same font at size 22.


## Proofread wording

The Alfoz narrator line, window interaction choice, human-skulls popup, dragon
epitaph, worldview quotation, and Vicious Mockery description were proofread
against their English sources. At dialogue size 22, the unwrapped widths of
the Alfoz line, window choice, and human-skulls popup in the installed
`NotoSerif-Regular` font are **788 px**, **343 px**, and **716 px** respectively.
The dialogue and popup fields wrap at spaces; no font-size or panel change was
needed.

## Proofread wording

The Visken and Ost encounter dialogue through VL_Ost_760 was proofread against the English corpus. Wording corrections did not change font size, markup, or panel layout, so no new width measurement was needed.



## Proofread wording

The Visken encounter dialogue was proofread against the English corpus through VL_ViskenCheck_26 and the dockside conversation through WL_Avikness_115, and the bookbinder scene through WL_Bookbinder_343 and the opening corner-house scene through WL_CornerHouse_138 and the opening griffon scene through WL_Giorgio_248, the Milk Run through WL_MilkRun_115, and the Manius scene through WL_MittelHouse_102. Text edits preserved markup and the existing 500 px dialogue area; no new width measurement was required.


## Proofread wording

Dialogs.csv was proofread sequentially through WL_Window_52 against the English corpus. These edits changed wording only; no font, markup layout, or panel dimensions were changed, so no width remeasurement was needed.

EntityInfo.csv was proofread against the English corpus. Wording and names were corrected; markup tags were checked row by row. No layout-sensitive changes were made.

Feats.csv was proofread against the English corpus. Names, mechanics, and game terminology were corrected; no layout-sensitive changes were made.

Glossary.csv proofreading is in progress. The first 107 entries were revised against the English corpus; no layout-sensitive changes were made.

Glossary.csv proofreading now covers entries 1-160. The prose and terminology were checked against the English corpus and existing game dialogue; no layout-sensitive changes were made.

Glossary.csv proofreading now covers entries 1-430 against the English corpus. The short place name City Below follows the glossary form “Подгородье”; wording edits did not require layout changes.

Glossary.csv proofreading now covers entries 1-453 against the English corpus. These wording edits preserve the existing layout.

Glossary.csv proofreading now covers entries 1-477 against the English corpus. Text edits preserve the existing layout.

Glossary.csv proofreading now covers entries 1-503 against the English corpus. Text edits preserve the existing layout.

Glossary.csv proofreading now covers entries 1-529 against the English corpus. Text edits preserve the existing layout.

Glossary.csv proofreading now covers entries 1-553 against the English corpus. Text edits preserve the existing layout.

Glossary.csv proofreading now covers entries 1-577 against the English corpus. Text edits preserve the existing layout.

Glossary.csv proofreading now covers entries 1-600 against the English corpus. Text edits preserve the existing layout.

Glossary.csv proofreading now covers entries 1-623 against the English corpus. Text edits preserve the existing layout.

Glossary.csv proofreading now covers entries 1-647 against the English corpus. Text edits preserve the existing layout.

Glossary.csv proofreading now covers entries 1-670 against the English corpus. Text edits preserve the existing layout.

Glossary.csv proofreading now covers entries 1-693 against the English corpus. Text edits preserve the existing layout.

Glossary.csv proofreading now covers entries 1-717 against the English corpus. Text edits preserve the existing layout.

Glossary.csv proofreading is complete through entry 727 against the English corpus. The final edits changed wording and terms only; no layout measurements required updating.

ItemTexts.csv proofreading is in progress through ItemDesc_10. Wording edits preserve the existing layout.

ItemTexts.csv proofreading now covers ItemDesc_1–ItemDesc_45. Text edits preserve the existing layout.

ItemTexts.csv proofreading now covers ItemDesc_1–ItemDesc_65. Text edits preserve the existing layout.

ItemTexts.csv proofreading now covers ItemDesc_1–ItemDesc_85. Text edits preserve the existing layout.

ItemTexts.csv proofreading now covers ItemDesc_1–ItemDesc_100. Text edits preserve the existing layout.

ItemTexts.csv proofreading now covers ItemDesc_1–ItemDesc_120. Text edits preserve the existing layout.

ItemTexts.csv proofreading now covers ItemDesc_1–ItemDesc_140. Text edits preserve the existing layout.

ItemTexts.csv proofreading now covers ItemDesc_1–ItemDesc_174. Text edits preserve the existing layout.

ItemTexts.csv proofreading now covers descriptions through row 176 and names through ItemName_25. Text edits preserve the existing layout.

ItemTexts.csv proofreading covers all 387 rows. Text edits preserve the existing layout and markup; the Russian column is unchanged in width and row count.

Proofreading pass: all 387 rows of ItemTexts.csv reviewed; 185 reviewed corrections are synchronized with src/voice/manual_fixes.json. Five blank cells are intentionally empty in the source. No layout-width changes were made.

MiscTexts.csv was proofread against the English corpus through all 1,358 rows. UI terminology, journal prompts, endings and character notes were corrected; all edits are mirrored in src/voice/manual_fixes.json. The game assets were not available at the documented default install path, so no new font-width measurements were recorded in this pass.

NPCInfo.csv was proofread against the English corpus through all 95 rows. Dialogue wording and typography were corrected; manual fixes match the Russian CSV. Game-font width measurements were unavailable because the documented game install path is absent.

Popups.csv was proofread against the English corpus through all 247 rows. Lore terms and inspection text were corrected; the repeated drinks line matches NPCInfo.csv. The game fonts were unavailable for width measurement at the documented default path.

Popup_160 was reworked as a lyric fragment: «Она заперла меня и не даёт подняться…». The English wording matches the official soundtrack lyric, where it is a poetic fragment ([track listing and lyrics](https://andersbachbrianbatzkristianpaulsen.bandcamp.com/album/esoteric-ebb-vol-1-original-soundtrack)). Popup_194 has an empty English string, so its Russian cell uses U+200B to prevent the game from falling back to English or rendering placeholder quote marks.

QuestPoints.csv was proofread against the English corpus through all 295 data rows (268 populated quest entries). Wording, lore names, player address, grammar and joke timing were corrected; 145 manual fixes are synchronized. Markup tags were compared row by row. No new font-width measurements were recorded because the game assets are unavailable at the documented default path.

SheetInfo.csv proofreading is in progress. The Russian text column (third column) is being checked separately from speaker/stat fields. 126 wording corrections have been mirrored to manual_fixes.json; remaining rows and row-by-row markup verification are still pending.

SheetInfo.csv proofreading now covers all 351 populated rows. The Russian text column was checked separately from the speaker/stat columns; 135 corrections are synchronized in manual_fixes.json. Markup tags were compared row by row. No font-width measurements were made in this pass.

SpellTexts.csv was proofread through all 104 populated rows. Spell names, spell effects and spell metadata were checked against the English corpus; terminology and mechanical mistranslations were corrected. Markup was compared row by row, and the corrections are synchronized in manual_fixes.json. No new font-width measurements were made.

UIElements.csv was proofread through all 315 populated rows. UI terminology and onboarding text were aligned with the glossary and corrected; 78 changes are mirrored in manual_fixes.json. Markup tags were checked against the source, including intentional size markup. No new font-width measurements were made.


Earlier technical cross-file scan used CSV filenames that did not match the corpus file identifiers, so it failed to compare source markup for most rows. A corrected scan now maps corpus identifiers to CSV stems. The corrected source map covered 81,891 translated rows across all 12 CSVs. It found two lost emphasis tags: UP_Nessan_68 and JC_Gorm_611. Both lines were corrected and synchronized with manual_fixes.json. Intentional localized size overrides remain for UI fit. This technical check by itself does not establish literary or lore consistency; the subsequent source-paired proofreading is recorded below and reaches the final Dialogs.csv source index 76409. All 12 CSVs are now included in the completed proofreading pass.


Lore terminology follow-up: clarified Glossary_Response_48 and Glossary_Response_75 so Diminor is explicitly the historical name of the band now called Reeds, while Old Diminor is identified as a common historical form. The timing and context of the renaming are now stated plainly. Both corrections are mirrored in manual_fixes.json. No layout changes were made.


Markup audit correction: the source corpus uses file stems without `.csv`. The earlier filename-based comparison therefore skipped source lookups. The corrected comparison supplements work/corpus/final.jsonl with the original English corpus for nine omitted keys. After restoring emphasis in UP_Nessan_68 and JC_Gorm_611, no non-size tag or placeholder mismatches remain. Twenty-nine localized `<size=N>` differences in MiscTexts.csv and UIElements.csv are layout overrides; the Charisma uses text was checked in the running game, and the other overrides retain their existing documented measurements. The glossary matcher rows, CSV headers, and empty-source rows account for the remaining keys without a populated English translation.


Supplementary source-corpus review: checked nine populated rows absent from work/corpus/final.jsonl against the original English corpus: eight dialogue rows and SheetInfo.csv/IP_ROLLO_20. Reworked IP_ROLLO_20, whose opening clause had the wrong grammatical subject and whose wording obscured the economic argument. The revised text keeps the CAPITAL fragment and completes the explanation of the proposed ideology. The correction is synchronized with manual_fixes.json.


Supplementary source-corpus review: the original English corpus contains nine populated keys omitted from the final translation corpus. All were inspected; markup on JC_Gorm_611 and UP_Nessan_68 was restored. The SheetInfo.csv line IP_ROLLO_20 and the other seven dialogue lines were checked against their English source.

Charisma uses copy: the English source separates “Apolitical” and “Force of Nature” into two display lines. The Russian line now does the same, with «Аполитичная» at size 28 and «силой природы» at size 40. The CSV and manual fix agree. The live screen still showed the prior line after reload, so the final size adjustment needs a fresh game restart and visual confirmation.


Dialogs.csv proofreading continued through AR_CoastMap_43. Corrected an inconsistent formal address in the map aside, clarified that cities and roads are marked on the plains, restored the parallel joke about Norvik's size and lettering, and replaced a literal hair-splitting calque while preserving the deliberately surreal thought. Rephrased the linked magocracy fragments as «остатки» and checked their connection across the two lines. No layout-sensitive markup changed.


Dialogs.csv proofreading continued through AR_CoastMap_82. Refined the description of floating farmland, the map's great ravine, and the region's boundaries; corrected address consistency and polished the reflective passage about learning from other peoples. The lower-band line keeps the deliberately prejudiced in-world claim so the following rebuttal still works. No layout-sensitive markup changed.


Dialogs.csv proofreading continued through AR_HiddenFreestriderSafe_120. Corrected misplaced lines in the safe scene, restored the missing consequence of the port contract (the Freestriders gain control regardless of the election result), and tightened conversational phrasing. The dialogue copy is synced with manual_fixes.json and installed; no layout-sensitive markup changed.


Dialogs.csv proofreading continued through AR_HiddenFreestriderSafe_220. Corrected displaced dialogue in the safe scene, restored omitted election consequences, clarified the plane-specific reference to remaining material, and tightened the mephit combat narration. Related choices and repeated lines were checked against their individual English keys. CSV and manual fixes are synchronized and installed; no layout-sensitive markup changed.


Dialogs.csv proofreading continued through AR_HiddenFreestriderSafe_371. Exact repeated source lines across the safe and combat branches are now aligned to identical Russian text; restored the hairline of the crit/critical-hit joke («Какого крита?»), retained the mephit's dancing taunts, and clarified how elementals return to the Elemental Planes. The contract scene's omitted election consequence is included. No layout-sensitive markup changed.


Dialogs.csv Enc_Crossing_192-225 were checked against their exact keys after a repeated-source audit exposed a displaced sequence: several translations described adjacent events instead of their assigned source lines. Restored the correct order and wording for the fall, the Masked One's escape, the goblin's retelling, and the invisibility exchange. Installed CSV and manual fixes match. No layout-sensitive markup changed.


Dialogs.csv proofreading continued through AR_Viira_395. Refined the Viira dialogue and choices for natural address, the smoke mephit joke, terminology for the Geminate Orb, and the deliberately awkward flirtation exchange. Manual fixes match the CSV; installed localization refreshed. No markup-sensitive layout changes were made.


Dialogs.csv proofreading continued through AR_Viira_494. Refined the griffon banter and its deliberate euphemism, corrected address and agreement, clarified the Moonwatch reference using the glossary, and polished the reward exchange. One draft based on an assumed adjacent line was caught against the keyed English source and replaced with the correct source-paired text. CSV and manual fixes are synchronized and installed; no layout-sensitive markup changed.


Dialogs.csv proofreading continued through AR_Viira_540 and AR_Viira_Ivcx_469. Corrected gender agreement in Viira’s reward branch, refined the Vorpal Sword explanation and the griffon/hag dialogue, and kept world terms aligned with the project glossary. Source keys were checked before edits; the installed CSV matches the repository and manual fixes. No layout-sensitive markup changed.


Dialogs.csv proofreading continued through AR_Viira_730. Corrected the informant reference, Viira’s grammatical gender, and several inconsistent player addresses; clarified her explanation of hag work, the Yobu, and the smuggling arrangement. Checked the contiguous main-branch rows 1373-1608 and the keyed English source before editing. Installed CSV matches the repository and manual fixes. No layout-sensitive markup changed.


Dialogs.csv proofreading continued through AR_Viira_780. Clarified the informer and smuggling passages, corrected several grammatical and address errors, and edited the AEFA contract explanation. The italic tag on “Askanii” now matches the English key; install, repository, and manual-fix values agree. No layout-sensitive markup was otherwise changed.


Dialogs.csv proofreading continued through CB_Akzel_344. Refined the Akzel expedition dialogue, corrected several meaning and grammar issues, and aligned Kardemum sweets and snailfolk terminology with the glossary. Preserved the joke about the dwarf being a man of culture and the intentionally silly “adventure-quest” phrasing. Manual fixes are synchronized; no layout markup was changed.


Dialogs.csv proofreading continued through CB_Apartment_341. Refined the apartment encounter’s descriptions, the finders/robbers wordplay, and the dragon’s account of Esuth’s Hoard and the Time Pocket. Kept the Diminiorian language name and the established Coast, Gate, and Halfway Bridge Tribe terms aligned with the glossary. Manual fixes are synchronized; all markup tags in the reviewed apartment block match the English source.


Dialogs.csv proofreading continued through CB_BagofHolding_208. Refined the bag exploration, apple sequence, and coin reward dialogue; corrected the cut-hand line and the build-up to the apple joke. Added a distinct glossary entry for Pouch of Holding («мешочек хранения») so it is not confused with the Bag of Holding («сумка хранения»). Manual fixes match the CSV; source markup matches throughout this block.


Dialogs.csv proofreading continued through CB_Bondavol_900. Clarified the necromancy and String-cutting explanation, corrected the references to Visken and the vampire, and preserved the deliberately awkward Finger of Death innuendo. Standardized Demi-Lich as «полулич», Trade Prince as «торговый князь», and the Trifler wordplay as «Пустячник» across the translations and glossary. Manual corrections are synchronized; reviewed markup matches the English source.


Dialogs.csv proofreading continued from CB_HallwaySolution_908 through CB_LordPuu_224. Refined Snell’s exchange about the goblin genocide, preserved the bitter joke about gratitude, corrected the trap corridor descriptions, and polished the Golden Horde ambassador’s formal dialogue, and adapted the seclusion/suclusion mispronunciation joke as «уединение/суединение». Synced the reviewed HallwaySolution manual fixes to the CSV; the source markup matches across the reviewed block. No layout markup changed.


Dialogs.csv proofreading continued from CB_LordPuu_225 through CB_Questions_24. Refined the Ginnungagap warning, kept the mimic chest/breast wordplay in Russian, polished Moongore’s banter and threats, and clarified the Esuth clue and the Petrified Wizard’s era reference. Standardized «Скольжение», «Праймл-Струна», and «Колодец Праймла»; added the Dispel Magic and Hail Snail terms to the glossary. Source markup and manual fixes match across the reviewed rows. No layout markup changed.

Dialogs.csv proofreading continued from CB_Questions_25 through CB_Roper_235. Corrected question-room phrasing, aligned Spider Climb and Roper with the glossary, refined the Whitemane mural and the wall-side quest, and repaired the Esuth invocation. Repeated Roper lines now use matching Russian text; the dialogue and manual fixes are synchronized. No markup-sensitive layout changes were made.

Dialogs.csv proofreading continued through CB_SecretPassage_31. Corrected several mistranslations in the Roper fight (including the monster name, sling ammunition, and combat cues), preserved its repeated dialogue and humor, and polished the Strands scene around Ragn’s fall. Refined the Gelatinous Cube and sarcophagus lines; the folder uses the glossary’s «Рун-факел» spelling. Manual fixes are synchronized; no markup-sensitive layout changes were made.


Dialogs.csv proofreading continued through DS_Olzis_264. Refined the Deck of Many Things exchange, donation bowl and music scenes, then corrected the riddle and lore dialogue with Olzis. Standardized references to the Pillar of Jor and its Gate, clarified the sphinx riddle, and preserved the dark humor in the card outcomes and tavern banter. Manual fixes were recovered from the archived project map and synchronized against the current CSVs; a read-only audit found no mismatches. No markup-sensitive text was changed in this checkpoint, so no width measurement was needed.


On 2026-10-27, the documented size for `AbilityScoreInfo_Intelligence_Uses1` was missing from the shipped CSV; restored `<size=40>` for «подготовить». The same pass restored the recorded 26 px size on `Loading_Title_AbilityScore`. The fit table above remains the measurement reference. The test markup exceptions now match the active sizes for the Intelligence, Dexterity, and Charisma ability labels.

Dialogs.csv proofreading continued from Sir Triban through Ever-Glad. Corrected dialogue idioms, character agreement and the terms «Дальний Предел», «Праймл», «аберрация» and «Пустяк». Kept source markup unchanged.


Dialogs.csv proofreading continued from Ever-Glad through Lezionas. Corrected lore wording around the Eternal Float, the Gate War, the Toulin’catl, Bloodcity Bay and Gorgorian; repaired idioms and jokes in the contract and Iron Gate scenes. Synced the reviewed lines with manual fixes. No markup-sensitive layout changes were made, so no width measurement was needed.


Dialogs.csv proofreading continued through Isk-Urum_265. Kept the heartstrings and magical Strings joke, corrected inconsistent address and errors in the Iron Door exchange, and aligned terms for Toulin, the Tongues spell and the Jor spell slots. Manual fixes match the dialogue. No markup-sensitive layout changes were made, so no width measurement was needed.


Dialogs.csv proofreading continued through Isk-Urum_665. Clarified the survivor’s account of the Toulin destruction, the resurrection plan, the orb’s cooldown and joke, and his directions dialogue. Aligned rogue spellcaster references with «маг-отступник» and preserved the Hail Snail and Strings terms. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through Isk-Urum_965. Standardized Ebb terminology as «Эбб», clarified the distinction between Ebb and the general idea of ebbing, and polished the explanation of Jor’s Strings. Corrected several grammar and idiom issues while retaining the mind-reading humor. Manual fixes match the dialogue; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through Isk-Urum_1065. Preserved the lore distinction between “Ebb” («Эбб») and “Ebbing” («Отлив») in the spell discussion, and reviewed the apprentice history and political exchange. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through OP_Map_77. Fixed a speaker gender mismatch for Ettir, clarified Isk-Urum’s joke about democracy and standardized the Primal healing term. Manual fixes match the reviewed lines; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through PC_AzgalDoor_31. Reviewed the rest of the ancient map scene, including dragon names and history, and corrected a line that wrongly implied the long-gone Toulin were still alive. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through PC_AzgalDoor_131. Polished the door and political-alignment exchanges, normalized Russian class names, and corrected a pronoun error in Alfoz’s dialogue. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through PC_AzgalDoor_229. Reviewed Alfoz’s trust test and the argument about bourgeois politics, restoring the player’s garbled echo of “bourgeois” as a confused question. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through PC_AzgalDoor_324. Restored the missing Snell choice line and its stage direction, and refined the accountability and magic-choice wording. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through PC_Frey_72. Reviewed the remainder of Alfoz’s door scene and Frey’s introduction, including the player’s awkward first encounter with her; tightened the clothing description. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through PC_GhostDoor_19. Corrected Freydis’s feminine agreement and removed an unnecessarily gendered insult directed at the player; reviewed the magical intrusion and its humor. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through PC_Thal_56. Corrected Freydis’s political exchange, a strained stage direction, the explicit profanity and the escalating pressure on the jammed key; checked the magical-door aftermath and Thalassos’s scene. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through Q_Class_95. Fixed an unfinished clause, repaired class-description grammar, aligned the primal-caster reference with «Праймл-магия», and restored the meaning of the Cleric progression text. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through Q_Conflict_48. Corrected the repeated Cleric identity refrain and aligned the tavern-joke punchline with its setup, preserving the intervention that rejects it. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through Q_Ebb_40. Unified the «Мастер Струн» feat name across the glossary, dialogue and Feats.csv; its 24 px advance in the game font is 272 px, versus 344 px for the former label. Clarified several class-feature descriptions and kept the patron’s gender unspecified. Manual fixes are synchronized.

Dialogs.csv proofreading continued through Q_Election_83. Corrected a mistranslated «порядок» as «орден», fixed agreement and syntax in the election monologue, aligned emphasis markup, and matched the Communing Patron choice name to the feat screen. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through Q_Elf_7. Refined the election discussion, aligned all instances of “Hells yeah!” to one Russian equivalent, unified the Apolitical feat as «Аполитик» across dialogue and Feats.csv, and corrected several political-ideology terms. Manual fixes are synchronized.

Dialogs.csv proofreading continued through Q_Feathers_64. Corrected Urth’s gender in the elf tale, aligned Stage Street with «Сценическая улица», repaired an interrupted word, improved several economic lines and the border-policy reference, and reconciled the fragile-immortality rules text with the feat description. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through Q_Feathers_172. Improved several labor and trade lines, repaired the joke about supply and demand, clarified the argument about border policy, and tightened the bird’s character summary. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through Q_Gate_66. Aligned the remaining feat names and rule descriptions with the feat list, corrected agreement and phrasing in the paranoia tips, and checked the opening surreal prophecy for terminology and deliberate wordplay. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through Q_Lichhouse_13. Corrected the response to the “twist” joke, fixed the transcription of Shěn’s name, repaired agreement in the prophecy, and aligned the Dark Belly feature rules with the feat list. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through Q_Lichhouse_112. Refined several lines in the post-lich encounter, clarified the distinction between ordinary lichdom and the character’s possible path, and repaired a line about sacrifice and flesh. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through Q_Print_61. Smoothed the circulatory metaphor, separated an awkward sentence about the magical era, clarified the propaganda line and one point of contention, and kept AFF and VK in their glossary forms. Manual fixes are synchronized; no markup-sensitive layout changes were made, so no width measurement was needed.

Dialogs.csv proofreading continued through Q_Resistance_30. Aligned three feat names («Пропаганда в СМИ», «Единство людей и дворфов», «Азгалианская стойкость») across the feat list, glossary and dialogue; the longest label measures 485 px at Russian size 22 in KleeOne-Regular, within the 500 px panel. Corrected several lines in the slavery and sovereignty debate while preserving its deliberate irony and gull pun. Manual fixes are synchronized.

Dialogs.csv proofreading continued through Q_Resistance_130. Refined the history of the Reeds, the sovereignty argument and the Leviathan imagery; corrected the interrupted description of the hoped-for new human and kept the crude nationalist joke in Dex’s voice. Changed «Истинный норвикиец» to standard lowercase demonym capitalization in Feats.csv. No width-affecting wording changes were made to feature labels.

Dialogs.csv proofreading continued through Q_Riddle_88. Standardized «Позитивное покалывание» across feat UI and dialogue, corrected inconsistent player gender in the Riddle conversation, and restored the taunting advice about drawing from the Deck. Updated the English-to-Russian glossary. The feat labels retained the same measured wording.

Dialogs.csv proofreading continued through Q_Sea_68. Corrected feminine agreement in references to the protagonist and clarified the origin of the major Arcanist houses. Standardized the «Позитивное покалывание» effect text across Feats.csv and dialogue. No feat-label width changes were made.

Dialogs.csv proofreading continued through Q_Sea_168. Clarified the food-distribution example, repaired the narrative link into the Industrial Revolution, aligned terminology around Aberrations, and corrected feminine agreement across the protagonist’s choices and references. No feat-label width changes were made.

Dialogs.csv proofreading continued through Q_TeaShop_164. Aligned three feat names with Feats.csv, corrected the rules text for Friendly Company, and fixed protagonist agreement and several lines in the loneliness and tea-shop sequence. No feat-label wording changed, so no width measurement was needed.

Dialogs.csv proofreading continued through Q_Youth_200. Replaced the literal «flat hierarchy» calque with «менее жёсткая иерархия Азгалистов» and restored the missing setup for the joke about «мужское начало». No layout-sensitive labels changed.

Dialogs.csv proofreading continued through RM_Ladder_32. Reviewed the continuation of the gender-spectrum discussion and the opening ladder scene against their source lines. No layout-sensitive labels changed.

Dialogs.csv proofreading continued through RM_Rollo_167. Preserved the intentionally nonsensical «wrong peach» joke, clarified the apology for a mistaken ruling, and reviewed the ladder’s death-and-rescue sequence and the Resistance boys’ introduction. No layout-sensitive text changed.

Dialogs.csv proofreading continued through RM_Rollo_367. Reviewed the Resistance mission briefing, checked the Griffon spelling distinction, and verified that the current CSV and manual overrides preserve the scene’s jokes and terminology. No layout-sensitive text changed.

Dialogs.csv proofreading continued through RM_Rollo_467. Clarified the Rollo exchange after the ledger reveals the Magistrates’ sale of the city; the CSV and manual fixes now share the same wording. No layout-sensitive text changed.

Dialogs.csv proofreading continued through RM_Rollo_567. Corrected the player’s feminine agreement across the scene, restored the Azgalian nationalist choice, and clarified the Resistance’s opposition to the Azgalists and Freestriders. Refined the unemployment jab while preserving its humor.

Dialogs.csv proofreading continued through RM_Rollo_667. Repaired an idiom about earnings, aligned the character’s player-facing agreement with the scene, and normalized the choice restricting entry to Norvik. Checked the scene’s satirical list of acceptable immigrants against its original tone.

Dialogs.csv proofreading continued through RM_Rollo_763. Smoothed an over-formal line about appealing to the boys’ dreams and changed a stage direction to address the player directly. Checked the recruitment pitch and the deliberate «pussy up» wordplay.

Dialogs.csv proofreading continued through RM_Rollo_863. Confirmed Ragn is male from the source dialogue and corrected residual feminine forms in his responses. Refined the milk-drinking exchange, the collective shrug, the dwarf girl's description, and the heated exchange with Modissa. Manual fixes are synchronized; no layout-sensitive line changes were introduced.

Dialogs.csv proofreading continued through RM_Rollo_958. Corrected speaker gender, clarified the plan to publish and circulate the Waterlane documents, repaired several newspaper and spearhead metaphors, and fixed grammar in the skill descriptions. Manual fixes are synchronized; no layout-sensitive lines changed.

Dialogs.csv proofreading continued through RM_Rollo_1053. Clarified compromise proposals, repaired agreement and an extended broken-up sentence across rows, and corrected political terms around capital and housing. Preserved the abrupt humor of the skill checks and the debate. Manual fixes are synchronized; no tags or row structure changed.

Dialogs.csv proofreading continued through RM_Rollo_1152. Smoothed the political aftermath and the shift from debate to the fight, corrected several combat cues and gender forms, and translated the group's repeated cheer consistently. Manual fixes are synchronized; tags and segmented row structure remain intact.

Dialogs.csv proofreading continued through RM_Rollo_1253. Refined the aftermath of the fight, corrected a silver-spoon idiom and several choice prompts, and restored the awkward humor of the cleric breaking down in tears. Manual fixes are synchronized; markup and choice structure remain intact.

Dialogs.csv proofreading continued through RM_StorageRoom_35. Corrected the Rollo scene's angry and enchanted dialogue, preserved the mind-control joke, and refined the mill's back-room clues and lockpicking narration. The Meek translation follows the glossary; manual fixes are synchronized.

Dialogs.csv proofreading continued through RM_StorageRoom_133. Standardized Rollermill to the glossary's «Гильдодцы Скалолома», clarified the lockpick scene, and corrected the labor-union document and commentary. Manual fixes are synchronized; no markup was altered.

Dialogs.csv proofreading continued through RM_StressCube_57. Preserved existing polished translations in the storage-room lead-in, removed a repeated descriptor in the gear scene, and clarified a few action prompts. The item remains consistently «Антистрессовый куб»; manual fixes are synchronized.

Dialogs.csv proofreading continued through SH_Alfoz_78. Preserved earlier edits to the Stress Cube and Alfoz dialogue, corrected the iron-threat line, and clarified an election question and a repeated form of address. Manual fixes are synchronized.

Lore check: the English lore defines Outreach as Illym's term for its representatives in foreign lands, functioning as an embassy without formally establishing one. Replaced the misleading «Выездная работа» with «Представительство» across the glossary, dialogue, and Kullervo's character sheet; the Warden title now follows the same term.

Dialogs.csv proofreading continued through SH_Alfoz_178. Improved the account of Pinja and her Illym ties, clarified political vocabulary, and standardized references to the Outreach as «Представительство» across dialogue, glossary, and Kullervo's character sheet. Manual corrections for changed rows are synchronized.

Dialogs.csv proofreading continued through SH_Alfoz_278. Smoothed the dwarven-heritage exchange, corrected Alfoz's career and political phrasing, restored the geographic term «пояса» in his account of dwarven societies, and rendered Rikêdom in SH_Alfoz_225 as «королевства Выз-Ха», matching the established lore entry for Vyz-Kha. Manual fixes are synchronized.

Dialogs.csv proofreading continued through SH_Alfoz_378. Corrected the political idiom about staying on someone's good side, fixed a pronoun mismatch, clarified the Youth wing and the explosion account, and preserved the double joke in Curse-Mother by translating the dwarven slang as «тёща». Alfoz's PPG acronym now follows the in-game spelling. Manual fixes are synchronized.

Dialogs.csv proofreading continued through SH_Modissa_12. Corrected Alfoz's back-patting choice, restored the abrupt exclamation, and clarified the Belt of Dwarvenkind description using the established «Азгалист» term. Manual fixes are synchronized.

Dialogs.csv proofreading continued through SH_Modissa_62. Repaired the wordplay around «dick», clarified Modissa's challenge about violent retaliation, smoothed choice instructions, and corrected the press description. Manual fixes are synchronized.

Dialogs.csv proofreading continued through SH_Modissa_262. Repaired several lost jokes and gender forms, clarified the Orange Ledger reveal and League exposition, and kept recurring choices aligned. Manual fixes are synchronized for the edited rows.

Dialogs.csv proofreading continued through SH_Modissa_505. Improved the press-law exchange, corrected Alfoz movement phrasing and gender agreement, refined Modissa's work and literary references, and preserved the reveal about the cleric's mother. Manual fixes are synchronized.

Dialogs.csv proofreading continued through SH_Modissa_748. Improved the press-law exchange, restored idiomatic phrasing in Modissa's debate with Alfoz, corrected the male player-character's past-tense forms, and clarified the article and cartridge-fetching scene. Manual fixes are synchronized for edited rows.

Dialogs.csv proofreading continued through SO_Snurre_27. Refined the deliberately blunt book commentary, restored the loneliness in the Shadow Lord memory, and corrected the imperative title «Прокляни богов». Manual fixes are synchronized.

Dialogs.csv proofreading continued through SO_Snurre_127. Smoothed the invoice exchange, curiosity joke, Snurre alignment studies specialty, and psychoanalysis explanation. Manual fixes are synchronized.

Dialogs.csv proofreading continued through SO_Snurre_151. Refined the interruption and the joke setup, and clarified the allegory about alignment and consequences. Manual fixes are synchronized.

Dialogs.csv proofreading continued through SO_Snurre_327. Refined Snurre’s self-deprecating joke, the gender-neutral question about his rambling, the rumored foreword, and the collectors’ investment line. Manual fixes are synchronized.

Dialogs.csv proofreading continued through SO_Snurre_427. Restored the speaker’s blunt humor, corrected an informal address, clarified the promised support, and preserved Meek’s distinctive speech while fixing its grammar. Manual fixes are synchronized.

Dialogs.csv proofreading continued through SO_Snurre_527. Clarified the halfling comparison, fixed a plural clause about shared myths, restored the reference to the two sides of the ego, and removed an unintended implication that Snurre is human. Manual fixes are synchronized.

Dialogs.csv proofreading continued through SO_Snurre_627. Tightened the joke about untested claims, smoothed the discussion of bodily change, and corrected the legal and morphological phrasing. Manual fixes are synchronized.

Dialogs.csv proofreading continued through SO_Snurre_727. Clarified the distinction between alignment and intention, smoothed the hypothetical about repentance, and corrected a sentence about personality research. The emphasis markup on «намерений» is preserved. Manual fixes are synchronized.

Dialogs.csv proofreading continued through SO_Snurre_827. Restored the omitted description of people as fundamentally evil, clarified that «smaller folk» means physically smaller peoples, not fewer people, and that «folk» names the world’s many peoples. Manual fixes are synchronized.

Dialogs.csv proofreading continued through SO_Snurre_927. Restored the speaker’s rough tone in the soul discussion and clarified the comparison between resurrection and other severe trauma. The spell name «Говорить с мёртвыми» matches the canonical glossary and spell list. Manual fixes are synchronized.

Dialogs.csv proofreading continued through SO_Snurre_1027. Corrected the fist-bump choice to match the response animation and clarified the Living Library exchange. The translations preserve the humor and established names for City Below, Toulin'catl, Cividix, and Diminorian. No markup-sensitive layout changes were made.

Dialogs.csv proofreading continued through SO_Snurre_1127. Fixed a duplicated line, clarified the impact choice, restored the canonical Russian name Сивидикс, and aligned Lord Scholar with the established title «лорд-учёный». Corrected several lines in the Cividix exchange for idiom and address. No markup-sensitive layout changes were made.

Dialogs.csv proofreading continued through SO_Snurre_1227. Smoothed Cividix’s dialogue, restored the missing alternative in his question about Snurre, and clarified statements about the sixth edition, the Anima and Animus research, divine power, and the Coast War. Manual fixes are synchronized. No markup-sensitive layout changes were made.

Dialogs.csv proofreading continued through SO_Snurre_1327. Smoothed the spirit’s historical and political monologue, corrected the account of divine foresight and its reference to future, chance, and fate, and aligned the Ymian name with the glossary. Manual fixes are synchronized. No markup-sensitive layout changes were made.

Dialogs.csv proofreading continued through SO_Snurre_1427. Localized Cividix consistently as Сивидикс in this scene, clarified the description of the bound spirit and polished the aftermath dialogue while retaining Snell’s dry joke. Manual fixes are synchronized. No markup-sensitive layout changes were made.

Dialogs.csv proofreading continued through SO_Snurre_1527. Removed a duplicated speaker attribution in the revolutionary speech, tightened the rumor lines, and clarified the argument about death sentences and political power. Preserved the character’s intentionally abrasive satire. Manual fixes are synchronized; no markup-sensitive layout changes were made.

Dialogs.csv proofreading continued through SO_Snurre_1627. Corrected a displaced answer in the king-candidacy exchange, aligned the Agrarian Party name with the glossary, and smoothed the account of the suffragette movement. Preserved the political satire and humor. Manual fixes are synchronized; no markup-sensitive layout changes were made.

Dialogs.csv proofreading continued through SP_Bed_1. Clarified the punchline around the protagonist’s mother, corrected the response to Snurre’s exaggerated “dying to know,” and refined terminology in the Clanlands discussion. Capitalization of Golden Line follows the glossary. Manual fixes are synchronized; no markup-sensitive layout changes were made.
Dialogs.csv proofreading continued through SP_GlowstoneLantern_46. Corrected the silk-mattress description, the joke about being «dirty», bird-person and merman wording on Snell’s board, the Postwar Era phrase, and the lantern’s click and thumbs-up gestures. The term «Потустороннее» remains consistent with the existing translation; no new lore term was introduced. Manual fixes are synchronized; no markup-sensitive layout changes were made.
Dialogs.csv proofreading continued through SP_Snell_83. Corrected mistranslated or stiff lines in the darkvision exchange, Snell’s apartment conversation, and the internal debate about where the cleric lives. Reworked the idiom about not dying on a hill and preserved the awkward humor around the cleric living with their mother. Manual fixes are synchronized; no markup-sensitive layout changes were made.
Dialogs.csv proofreading continued through SP_Snell_183. Corrected the typo in the internal commentary, restored the sense of «truest thing», and clarified Snell’s explanation of anti-goblin prejudice. Existing manual fixes in this dialogue were checked against the source. Manual fixes are synchronized; no markup-sensitive layout changes were made.
Dialogs.csv proofreading continued through SP_Snell_283. Aligned the Halfway Bridge Tribe name with the glossary, clarified the path from youth recruitment to juvenile detention, and polished several lines in Snell’s account of the goblin tribes. Manual fixes are synchronized; the original emphasis tags remain intact.
Dialogs.csv proofreading continued through SP_Snell_383. Smoothed the jokes around the cleric’s awkward subject change, clarified Snell’s work for the Halfways, and improved the lines about his purpose and magical ability. Manual fixes are synchronized; existing markup remains intact.
Dialogs.csv proofreading continued through ST_Bars_92. Aligned the item names Адамантиум and Мешочек хранения with the glossary, corrected the lifting and spotting choices, and clarified the hammer’s light weight and impact. Manual fixes are synchronized; emphasis markup is preserved.
Dialogs.csv proofreading continued through ST_Lever_46. Replaced two literal «you have nothing» lines with the intended no-counterargument meaning, aligned every drawbridge reference with «подъёмный мост», and polished the lever joke and interaction text. Manual fixes are synchronized.
Dialogs.csv proofreading continued through ST_Notepad_90. Corrected three manual fixes that had been assigned to the wrong notepad keys, aligned Reedsian and Quillwell with the glossary, and clarified the note about the smuggling accounts. Manual fixes are synchronized; markup is preserved.
Dialogs.csv proofreading continued through ST_PebbleOfSending_93. Polished the letter-of-the-law exchange around the cursed notepad and the telepathic message thread, keeping the Sending Pebble and Sending Stone names consistent. Emphasis markup is preserved.
Dialogs.csv proofreading continued through ST_PotionBox_67. Corrected the plural reference to the unsafe potions and clarified the working-status joke; replaced the unexplained calque «фолктип» with «исходный вид» in the potion mechanics. Sending-item terminology remains aligned with the glossary.
Dialogs.csv proofreading continued through TE_Booths_5. Restored the source distinction between sympathizing and empathizing, smoothed the description of the gender-switch potion’s effect, and refined the protagonist’s reactions and Snell’s joke about his voice. Existing emphasis markup remains unchanged.
Dialogs.csv proofreading continued through TE_Booths_101. Clarified the tea shop booth search, aligned the brooch and charred-wood descriptions, and preserved Snell’s dry humor. Manual fixes are synchronized; no markup-sensitive layout changes were made.
Dialogs.csv proofreading continued through TE_Counter_62. Corrected inconsistent second-person address, booth terminology, and stiff wording across the tea cup and counter scenes; preserved Snell’s milk, green tea, and barista jokes. Manual fixes are synchronized; no markup-sensitive layout changes were made.
Dialogs.csv proofreading continued through TE_Counter_161. Corrected the hammer-and-nail joke, clarified the valve and smell sequences, retained the markup around the helmet sound effect, and preserved the absurd physical comedy. Manual fixes are synchronized; no markup-sensitive layout changes were made.
Dialogs.csv proofreading continued through TE_Frame_57. Polished the aftermath of the tea machine scene and corrected the ego exchange so the self-deprecating joke reads naturally; retained Snell’s imaginary-family punchline. Manual fixes are synchronized; source markup remains intact.
Dialogs.csv proofreading continued through TE_HiddenTeaShopSafe_39. Reconstructed the corrupted question-mark text in the frame and safe discovery scenes, restored the description of the hidden safe and the Diminorian access phrase, and preserved the original markup. The English source uses the unexplained label “LR”; it remains unchanged pending a lore reference.
Dialogs.csv proofreading continued through TE_IronDoor_31. Restored corrupted question-mark text in the trapped safe, its contents and note, and the iron-door investigation. Kept Hârdsten as Хардстен per the frozen glossary and retained spell-circle terminology and markup.
Dialogs.csv proofreading continued through TE_Pinja_88. Rebuilt the corrupted iron-door and table-investigation text, then restored the shift from comic bravado to the discovery of a victim. The deliberate wordplay and scene markup were checked against the English source.
Dialogs.csv proofreading continued through TE_Pinja_189. Restored the damaged autopsy dialogue, including the goblin’s nervousness, the victim’s examination and the chain that dissolves in an esoteric glow. Matched Lichhouse to the frozen glossary and preserved character voice and markup.
Dialogs.csv proofreading continued through TE_Pinja_288. Corrected the chain exchange, restored the damaged corpse-examination dialogue, and clarified the reveal that the victim was an elf. Checked the established Lichhouse and elven terms and preserved the shift into the investigation’s larger stakes.
Dialogs.csv proofreading continued through TE_Pinja_393. Restored corrupted dialogue about the political stakes, Visken’s report and the spell Speak with Dead, retaining Snell’s awkward euphemism and humor. During key-by-key verification, corrected a set of fixes that had been assigned to the following dialogue keys; the closing exchange now follows the source order.
Dialogs.csv proofreading continued through TE_Rubble_58. Corrected the aftermath exchange and restored the rubble investigation, including the realization that the blast came from nine beads of the Necklace of Fireballs. Matched the artifact name and historical account to the glossary.
Dialogs.csv proofreading continued through TE_Rubble_158. Restored the damaged explanation of why a fully charged Necklace of Fireballs was spent, preserved the fast-hag joke, and clarified Snell’s history and fireball theory. The Urth-bakery comparison was checked for Russian “также/так же” ambiguity.
Dialogs.csv proofreading continued through TE_ScorchedZines_84. Repaired the corrupted rubble dialogue, clarified the political context of the tea shop, and restored the magazine banter and Snell’s check-in about the Cleric’s condition. The pocket-watch clue and markup were preserved.
Dialogs.csv proofreading continued through TS_Alfoz_49. Restored the Esoteric Event sequence in which the Cleric becomes frozen and reaches for a String, repaired the secret-passage banter, and corrected the opening exchange with Alfoz. Preserved the established Azgalist and String terminology.
Dialogs.csv proofreading continued through TS_Alfoz_149. Polished the exchange about Azgal’s legacy, the Azgalist movement and Alfoz’s foreman title; aligned Urthguarders and Ashmask with the glossary and clarified that Azgal was a dwarf.
Dialogs.csv proofreading continued through TS_Alfoz_249. Checked the Azgalist rally dispute, the documents and the joke about a vote hinging on one’s manhood; capitalized Lichhouse consistently and retained the “Mr. Cityman” address.
Dialogs.csv proofreading continued through TS_Alfoz_349. Corrected the singular address to the Cleric, restored the meaning of the “we’re not in the wrong” reply, separated the two conflict-choice prompts, and tightened the paperwork exchange and escalating confrontation.
Dialogs.csv proofreading continued through TS_Alfoz_447. Refined the escalating provocation sequence, preserved the exaggerated “manhood” banter, and kept Alfoz’s attempt to rebrand a punch as a “joust.” Checked the full consequence branch, including the loss of trust and the Circle Square outcome.
Dialogs.csv proofreading continued through TS_Alfoz_536. Repaired the dwarf-shortness joke so the affectionate “shorty” wording works in Russian, clarified Alfoz’s shift from anger to negotiation, and corrected the idiom about fence-sitting.
Dialogs.csv proofreading continued through TS_Alfoz_636. Checked the resolution of the permit dispute, the friendship and mind-charm branches, and the exit beat. Preserved Alfoz’s self-deprecating “big mouth” line, the distinction between human and dwarf, and the choice to break the spell.
Dialogs.csv proofreading continued through TS_Alfoz_730. Checked the spell-reversal consequences and the escalation into grappling, clarifying the restraint, “stand down” command and struggle cadence while preserving the scene’s awkward physical comedy.
Dialogs.csv proofreading continued through TS_Alfoz_821. Polished the repeated headbutt contest, the beard and mother jokes, and the final broken-line victory declaration; corrected “like a brick” to describe the dwarf’s hard head.

Dialogs.csv proofreading continued through TS_AppleBranch_64. Refined Alfoz’s physical-alignment joke and the broken-line fall, and polished the apple-tree dialogue while preserving its dry humor.

Dialogs.csv proofreading continued through TS_Arn_Kiosk_23. Tightened the reveal of the tree’s prophecy and the kiosk boy’s awkward sales patter, keeping the scene’s deadpan humor.

Dialogs.csv proofreading continued through TS_Arn_Kiosk_126. Refined the kiosk boy’s stilted conversation and the reciprocal-bribe joke, keeping the awkward pauses and established Waterlane name.

Dialogs.csv proofreading continued through TS_Arn_Kiosk_176. Sharpened the kiosk boy’s political banter, the uneasy alliance over three coins, and the scene’s class satire while retaining the established faction names.

Dialogs.csv proofreading continued through TS_Arn_Kiosk_226. Checked campaign and election terminology against the project glossary, and polished the newspaper’s political headlines and missing-paladin exchange.

Dialogs.csv proofreading continued through TS_Arn_Kiosk_276. Polished the newspaper editorials, the three-party election coverage, Arn’s deliberate malapropism, and the joke about the cleric not being able to read.

Dialogs.csv proofreading continued through TS_Arn_Kiosk_326. Polished the iron-mask rumor and Arn’s account of the tea-shop explosion while preserving his hesitant, matter-of-fact delivery and the dry joke about bodies in the street.

Dialogs.csv proofreading continued through TS_Arn_Kiosk_376. Polished the blue-flame witness account and the transition from the iron-mask rumor to Mr. Drummer’s movements; “birdfolk” follows the established “птицелюд” wording.

Dialogs.csv proofreading continued through TS_Arn_Kiosk_426. Normalized “City Below” to the glossary term “Подгородье”, checked the merman wording, and refined the explanation of Arn’s “forenoon” vocabulary.

Dialogs.csv proofreading continued through TS_Arn_Kiosk_476. Refined the landlord and wages discussion, preserving the dry political satire and the boy’s confusion when the cleric pushes him toward rebellion.

Dialogs.csv proofreading continued through TS_Arn_Kiosk_523. Improved the bribe negotiation’s comic timing and cleaned up the gag where the cleric hands over lint instead of a crown.

Dialogs.csv proofreading continued through TS_Arn_Kiosk_573. Normalized Reedsian and River Run terminology to the glossary and preserved the escalating awkwardness of Arn’s account, including the intentionally rough swear word.

Dialogs.csv proofreading continued through TS_Arn_Kiosk_673. Corrected the child-threat sequence, tightened the scramble for stolen magazines, and fixed the grammatical case in the evil-versus-good joke.

Dialogs.csv proofreading continued through TS_Arn_Roof_14. Corrected the aftermath of the kiosk theft and carried the established Rollermill name into the next scene.

Dialogs.csv proofreading continued through TS_Arn_Roof_64. Tightened Arn’s hesitant answers and the Cleric’s mock interrogation, preserving the joke about avoiding political discourse.

Dialogs.csv proofreading continued through TS_Arn_Roof_106. Refined the sensitive conversation about Arn’s parents and loneliness, keeping the deliberately awkward “parallel positioning” joke.

Dialogs.csv proofreading continued through TS_Arn_Roof_156. Refined the emotional advice and sympathy/empathy exchange, and converted the remembered distance from feet to an approximate ten metres for natural Russian dialogue.

Dialogs.csv proofreading continued through TS_Arn_Roof_206. Refined the emotional reassurance and the Urthguard brotherhood parable while preserving the repeated “walls” metaphor and the awkward joke about giving life advice.

Dialogs.csv proofreading continued through TS_Bike_47. Confirmed the “Knock” spell and scarf name against the glossary, and polished the reunion-with-bike scene and its cowboy-film finale.

Dialogs.csv proofreading continued through TS_Bike_97. Preserved Meek’s broken speech and the intentionally pompous bike terminology, while making the bicycle-lock description idiomatic.

Dialogs.csv proofreading continued through TS_Bike_147. Kept the scene’s nervous “cool and smooth” exchange consistent and converted the fall height to an approximate ten metres, matching the earlier recounting.

Dialogs.csv proofreading continued through TS_BirdsNest_30. Refined the bicycle argument and the risk-reward banter around the bird’s nest, keeping the reference to the remembered spell consistent with the game’s lost-memory premise.

Dialogs.csv proofreading continued through TS_BirdsNest_80. Kept the taboo-word/reclamation joke consistent through the “be strong as a pussy” and “pussy up” lines, corrected emphasis casing, and checked regional names against the glossary.

Dialogs.csv proofreading continued through TS_BirdsNest_130. Checked the “DIP” death-status reference against later dialogue and aligned the duplicate line in Default_Pipe_88.

Dialogs.csv proofreading continued through TS_Braxo_50. Polished the devil’s caustic opening and his extortion exchange, keeping his contemptuous register distinct from Meek’s broken speech.

Dialogs.csv proofreading continued through TS_Braxo_100. Aligned the legal discussion with the frozen polymorphism terminology and restored the hearing/listening wordplay in the devil’s deliberately literal reply.

Dialogs.csv proofreading continued through TS_Braxo_150. Polished the gender-potion policy debate, keeping its legal distinctions and the devil’s crude comic aside, then preserved the deliberately overlong evil-origin story.

Dialogs.csv proofreading continued through TS_Braxo_200. Clarified the devil’s legal trade, work as a palace-connected scribe, and the contrast between his wicked nature and his everyday city ties.

Dialogs.csv proofreading continued through TS_Braxo_250. Refined the devil’s coarse complaints about infernal promotion and preserved the election joke about “the little guy” as a reference to Braxo’s tiny stature.

Dialogs.csv proofreading continued through TS_Braxo_300. Corrected the important distinction between Azgalian identity and Azgalist politics, and clarified Braxo’s legal reading of the Tolstad accord and the tea-shop site.

Dialogs.csv proofreading continued through TS_Braxo_350. Unified all Permission of Public Gathering references as “РПС”, added the abbreviation to the frozen glossary, and clarified Braxo’s legal definition of the permit.

Dialogs.csv proofreading continued through TS_Braxo_400. Kept the “киска/кискуй” wordplay consistent with the earlier scene and clarified the resurrection-law discussion without changing its divine-versus-necromantic distinction.

Dialogs.csv proofreading continued through TS_Braxo_450. Refined the devil’s mockery, clarified the law’s distinction between capital punishment and resurrection, and kept the resurrection status term DIP consistent.

Dialogs.csv proofreading continued through TS_Braxo_500. Matched hags to the glossary’s “Хаг” and adamantium to “Адамантиум”, and kept the Necklace of Fireballs abbreviated consistently as ООШ.

Dialogs.csv proofreading continued through TS_Braxo_550. Corrected the divine-era and currency references and clarified the financial-share explanation, preserving the devil’s teasing tone.

Dialogs.csv proofreading continued through TS_Braxo_600. Standardized the discussion of currency denominations, alignment, and the devil’s short-/small-minded pun.

Dialogs.csv proofreading continued through TS_Braxo_650. Checked “City Below” against its glossary short name “Подгородье” and aligned the crusade acronym with the localized name. Refined the legal explanation of Charm Person.

Dialogs.csv proofreading continued through TS_CatStatue_81. Preserved the Cat Statue scene’s intentionally botched Snell translations and aligned the statue’s Spanish-rendered Whitemane with the established Russian name Уайтмейн.

Dialogs.csv proofreading continued through TS_Ettir_135. Refined Chamăr’s political dialogue and the crab scene, kept Snell’s mistranslations comic, aligned Whitemane across the statue’s Spanish inscription, and preserved the deliberately grandiose angel-flattery joke with a Russian nonce word (“вечносно”).

Dialogs.csv proofreading continued through TS_GardenMonument_28. Corrected the supernatural ring movement, kept Ettir’s intentionally severe/dry voice and language jokes coherent, aligned Toulin’catl as Ulitniki, and normalized the buried item depth to metric units.

Dialogs.csv proofreading continued through TS_GoboGrafitti_12. Clarified the language-learning exchange with Ettir, corrected references to the Guard Tower, and reconciled the excavation scene with the established metric measurements and Ulitniki terminology.

Dialogs.csv proofreading continued through TS_GoboGrafitti_59. Preserved the graffiti joke and Meek’s broken speech, corrected the timeline reference to the Reconquest, and made the Gate Era architecture description clear in Russian.

Dialogs.csv proofreading continued through TS_Kull_446. Reconciled Pinja’Athena with the glossary spelling, sharpened the grammar gag and the political warning, and corrected combat narration where a punch, a failed grab, and a magical attack had been conflated.

Dialogs.csv proofreading continued through TS_Pocket_27 (CSV row index 61154). Repaired the broken divine-quest joke in Nearly’s flower-crown branch, checked goblin kinship and Nearly’s bard dialogue, aligned Oyu’s travel, trade, political history, and threat scenes with the setting, and began Pinja’s missing-paladin thread. This is an intermediate checkpoint; proofreading later reached the final source index 76409. No new layout measurement was required in this range.

Dialogs.csv proofreading continued through TS_Potion_111 (CSV row index 61964). Reviewed the time-pocket lore and gravity sequence, the gremlin and fish stories, the Vâttar dance branch, the poster scene, and the potion seller’s opening. Corrected the action/text mismatch in the waiting line, aligned local names, and changed item prices in dialogue choices to crowns. This is an intermediate checkpoint; proofreading later reached the final source index 76409.

Dialogs.csv proofreading continued through TS_TeaShopDoor_53 (CSV row index 63433). Corrected mismatched choice and reply keys in the potion seller and Sir Triban scenes, restored the centrifugal/centripetal correction joke and the fishy/fish-rampage callback, kept Ragn distinct from the Patriarch's mispronunciation Rang, and aligned repeated insults and proper names. Standardized 89 short-form City Below references across seven CSV files to the frozen «Подгородье» term while retaining the full «Город под городом» name where the source says “The City Below the City”. Added «Круглая площадь» and «Садовый тоннель» to the glossary. The approximate width scan flagged two dialogue lines; they were shortened, but the scan only ranks its 120 widest ratios and is not an in-game font measurement.

Dialogs.csv proofreading continued through TS_Viira_122 (CSV row index 64224). Corrected the ruined Kardemum Treat wording and the Thalassos fishing and landlord jokes, aligned Pillar Road to the glossary name «Колонная улица» across dialogue and quest text, and clarified Viira's North Wall article joke, the PPG process, and several speaker and gender mismatches. This is an intermediate checkpoint; proofreading later reached the final source index 76409. No new layout measurement was required in this range.

Dialogs.csv proofreading continued through UP_Gourgalash_610_E_HoleFoot (CSV row index 67475). Reviewed the Brrr fungal folk branches, Ettir recruitment, and the Gourgalash confrontation. Corrected direction and action text, repaired dialogue attribution and gender agreement, kept Core Crevice terminology consistent, and fixed a false revolver reference: Snell uses a sling and stones in this scene. No new layout measurement was required for this text-only range.


Dialogs.csv вычитана до UP_Nessan_236 (строка CSV 69731). В сценах Мериадока исправлены неверные пояснения к приветствию фристрайдеров, шутка о леди Гиа, неточности в расследовании невидимого человека и рассказе о Вратах Джора; политические термины сверены с глоссарием. В диалогах Нессы согласованы правильная и намеренно искажённые формы имени Коколорономоноросо, чтобы сохранить шутку о произношении. Проверка продолжается; замеры ширины в этом текстовом фрагменте не проводились.

Dialogs.csv вычитана до UP_RuinClimb_40 (строка CSV 70020). В сцене росписи уточнены обращение Иоместры, её ограничение на передачу сведений, формулировки о Струнах и Битве; в сцене подъёма исправлены несколько буквальных и неестественных оборотов. Проверка продолжается; замеры ширины для этого фрагмента не проводились.

Dialogs.csv вычитана до UP_WeirdVatte_66 (строка CSV 70220). В сценах подъёма по лозам и встречи со странным существом исправлены перепутанная реплика о заклинании, неточная высота падения, повелительные формы и несколько реплик с юмором; сохранена шутка о коленях Снелла и деловой лексике во внутреннем монологе. Проверка продолжается; замеры ширины не проводились.

Dialogs.csv вычитана до UP_Zombie_29 (строка CSV 70420). В развилках встречи с богглом исправлена строка, в которой вместо описания действия повторялся выбор диалога; «очарование» приведено к глоссарию. Уточнены несколько фраз о падении и подъёме после воздействия заклинания, а также повелительное наклонение в реплике о нежити. Продолжаю; замеры ширины не проводились.

Dialogs.csv вычитана до VL_AncientTome_87 (строка CSV 70520). В древнем томе выправлены формулировки о «Понимать языки», Дракономастерах Олд Диминора, Слове Силы и Пределе Джора. Уточнена важная строка Каэлума, где он говорит, что стал самим Джором; переформулировано изложение о «ягнятах» и последнем правящем драконе. Проверка продолжается.

Dialogs.csv вычитана до VL_Books_84 (строка CSV 70620). В сценах с томом и автобиографией поправлены формулировки о заклинании «Восстановление», учёбе на писца и «победах» Пракса; восстановлен смысл «пусть ведут те, кто учится». Выборы перелистывания и закрытия книги приведены к повелительному наклонению. На следующем этапе вычитка продолжилась со сказки о гноме и титане; она завершена до последнего исходного индекса 76409.

Dialogs.csv вычитана до VL_Books_184 (строка CSV 70720). В послесловии к «Собранным песнопениям Норвика» уточнено, что государство подавляло прежние племенные уклады; поправлены несколько стихотворных строк и формы выбора книги. Продолжаю далее по исходному тексту.

Dialogs.csv вычитана до VL_Meeting_75 (строка CSV 70820). В начале встречи с Вискеном исправлено видовое описание кобольда, имя Ост возвращено к форме из глоссария, а угроза молчания и реакция Жреца приведены к естественным репликам. Уточнено, что нападающие решились на засаду, потому что герой пришёл один. Проверка продолжается.

Dialogs.csv вычитана до VL_Meeting_175 (строка CSV 70920). Исправлены реплика о том, что большая часть плоти Крааида не подверглась некромантии, и передача шутки про «слегка нежить» без грамматической ошибки; уточнены реплики Оста, описание Утки и насмешка о воспоминаниях со Снеллом. Проверка продолжается.

Dialogs.csv вычитана до VL_Meeting_270 (строка CSV 71020). Исправлена реплика внутреннего голоса, который напоминает Жрецу о его собственной роли в установлении порядка; поправлены шутка с кодовым именем Утки, признание Оста, реплика о цене личества и формулировка о размытом вреде Вискена. Термин свитка «Астральная проекция» приведён к глоссарию.

Dialogs.csv вычитана до VL_Meeting_368 (строка CSV 71120). В сцене клятвы уточнено, что Вискен требует действовать в его интересах; группа Helpers теперь передана как «Помощники». Формула «Urth Be Blessed» приведена к естественному обращению «Урт, будь благословен». Также уточнены смысл заверения, слабое место и выгода, на которой держится организация.

Dialogs.csv вычитана до VL_Meeting_468 (строка CSV 71220). В ветке сделки исправлены несколько формулировок о взятке и шантаже, неоднозначное «уничтожить тебя по закону» заменено точным смыслом «уничтожить, не нарушая закона». Лорное ругательство «Hells yeah» передано с термином «Ады», а описание ухмылки Крааида сделано естественным по-русски.

Dialogs.csv вычитана до VL_Meeting_568 (строка CSV 71320). В сцене боя поправлены обращения к Жрецу, неверно переданный смысл фразы «ты и сам не понял», звук выстрела из арбалета, реакция на рану и несколько описаний атак. Сохранён переход к заклинанию «смазка» и комический тон реплик Крааида.

Dialogs.csv вычитана до VL_Meeting_660 (строка CSV 71420). В боевых ветках исправлена игра слов про возвращение Крааида «за добавкой», учтено отсутствие у Жреца руки, уточнены действия рыцаря и оборот для попытки отступить. Продолжаю эту сцену.

Dialogs.csv вычитана до VL_Meeting_747 (строка CSV 71520). В продолжающейся боевой сцене исправлено положение арбалета при выстреле, уточнено тяжёлое ранение от топора и передано чувство обречённости после отбрасывания. Выправлены последние реплики перед заклинанием «Палец смерти». Проверка продолжается.

Dialogs.csv вычитана до VL_Ost_25 (строка CSV 71620). В финале встречи поправлены реплики о полном контроле над слугами и тяжёлом топоре, а также завершён юмористический обмен Вискена со Смотрителем. В имени группы «Помощники» сохранено единообразие по глоссарию.

Dialogs.csv вычитана до VL_Ost_122 (строка CSV 71720). В разговоре со Снеллом и кобольдом восстановлена шутка о грамматической ошибке и придуман русский аналог каламбура про торговое «королевство»; вопрос о работе теперь соответствует ответу Оста «Не работа». Уточнено рассуждение о жалованье и крепостной зависимости.

Dialogs.csv вычитана до VL_Ost_223 (строка CSV 71820). В ветке торговли молоком уточнены жители Водного пути, вопрос о происшествии в чайной и рассуждение о жалованье; сохранены шутка Оста с «профи-табельным» молоком и его нарочито ломаные фразы.

Dialogs.csv вычитана до VL_Ost_320 (строка CSV 71920). Исправлены обращения к игроку в сцене с кровью (без неожиданного «вы»), прояснены шутки о «прагматичном бескорыстии» и предпринимательстве, отредактированы метафоры про кровь и попытку польстить Оста.

Dialogs.csv вычитана до VL_Ost_420 (строка CSV 72020). Исправлено ошибочное «ударить» вместо «схватить» незаряженный арбалет; «Charm» в реплике о магическом эффекте согласовано с термином «Очарование». Уточнена реплика о том, что кобольд почему-то верит Жрецу.

Dialogs.csv вычитана до VL_Ost_518 (строка CSV 72120). В сцене борьбы за арбалет уточнены команды и действия, сохранено грубое комическое оскорбление кобольда, исправлены реплики о попытке расшатать ящик и нарушить его равновесие.

Dialogs.csv вычитана до VL_Ost_609 (строка CSV 72220). В схватке за арбалет уточнено действие от резкого чиха Оста и исправлена сводка исхода «Ты вывел его из равновесия». Остальные юмористические варианты — дыхание в лицо, попытка облизать арбалет и притворные угрозы — оставлены с тем же комическим тоном.

Dialogs.csv вычитана до VL_Ost_699 (строка CSV 72320). В сцене с перекрёстным перехватом арбалета сглажены реплики о заимствовании и поражении. В мистическом переходе исправлено слово «Струны», восстановлена рифма «идти — плыть», а искажённый голос переведён на русский с сохранением эффекта сбоя и повтора; повторяющиеся строки синхронизированы.

Dialogs.csv вычитана до VL_Pinja_134 (строка CSV 72520). Продолжение голоса Струн синхронизировано с ранее локализованным повтором. В сцене с Пинджей уточнены имена и политические термины, поправлено обращение о сомнении, а голос тела не назван душой, способной узнавать новое: правило зеркального отражения памяти смерти сохранено.

Dialogs.csv вычитана до VL_Pinja_234 (строка CSV 72620). В сцене раскрытия Лизы согласованы женские формы слова «хага» (она — бывшая возлюбленная Пинджи), убрано добавленное переводом «империя» при обсуждении Иллим, а реплика Снелла «А ты завидуешь?» возвращена как подкол, а не как комментарий о самомнении.


### Вычитка Dialogs.csv: строки 72621-72740
Сверены реплики разговора о погибшей эльфийке и итоговые выводы расследования. Убрано неподтверждённое уточнение о «связном», термин Freestrider передан как «фристрайдер», уточнён смысл реплики об эзотерическом видении и алиби героя.


### Вычитка Dialogs.csv: строки 72741-72900
Сверена начальная сцена с Вискеном. В описании мостов восстановлено, что они соединяют Толстад с остальной частью города; длинная реплика о грядущих переменах упрощена без потери смысла.

### Вычитка Dialogs.csv: строки 72901-73220
Уточнены термины «Запределье» и «Астральная проекция», объяснение воскрешения и реплики о магии души. Исправлены имя Оста и несколько неестественных формулировок. Сохранена шутка о молочных побегушках и неловком общении с Вискеном.


### Вычитка Dialogs.csv: строки 73221-73340
Проверены объяснение Вискена о свитке Астральной проекции и сцена с мимиком. Согласованы название заклинания и терминология Струны; выправлены неестественные обороты, сохранены шутки о молочных побегушках и мнимой стоматологии.


### Вычитка Dialogs.csv: строки 73341-73380
Сверена сцена о загадке Ользис и похищении тела. Термин Door Hug заменён на разговорные «обнимашки с дверью», сохраняющие комический тон и значение выражения; обновлён глоссарий.


### Вычитка Dialogs.csv: строки 73381-73540
Проверены отчёт Вискена о теле эльфийки и разговор о его пропаже. Уточнено происхождение эльфийки, описание цепи и врождённого владения заклинанием; обороты и шутливые реплики приведены к естественному русскому.


### Вычитка Dialogs.csv: строки 73541-73620
Сверены разговоры о знакомом Вискена и подготовке к допросу тела. Уточнены «полулич», причина редкости заклинания и помилование гоблинских племён; выправлены выражения про доверчивое лицо и тайную комнату, сохранены самоироничные реплики.


### Вычитка Dialogs.csv: строки 73621-73660
Сверена сцена с рекомендациями Вискена. Имя переплётчика согласовано с ранее встречавшейся формой «Шэнь», а формулировка про Урта приведена к смыслу оригинала.


### Вычитка Dialogs.csv: строки 73661-73700
Проверены объяснения Вискена о подготовке заклинаний и молитвенных книгах. Выровнены обращения к переплётчику Шэню и местоположение святилища; поправлены реплики о том, кто распознал Жреца.


### Вычитка Dialogs.csv: строки 73701-73860
Проверены реплики о призвании героя и его прошлом. Синхронизирован термин «жрец тайной магии», сглажены места о бедности и воровстве, сохранена шутливая перебранка о классах и бюрократии.


### Вычитка Dialogs.csv: строки 73861-73900
Сверены реплики о нежити в подвале и магическом зубе. Уточнено, что герой указывает на порождение нежити внизу, а не называет так себя; исправлена фраза о лжи Вискена.


### Вычитка Dialogs.csv: строки 73901-74020
Сверены сцены с магическим зубом и нарушением Кодекса Костяной чистки. Исправлены обороты в сцене с Вискеном и термин Dagsbôter: по шведскому юридическому употреблению это дневной штраф, а не «дальнобой». В реплике о повышении уточнено, что герой расследует дело чайной.


### Вычитка Dialogs.csv: строки 74021-74060
Сверены последствия конфликта с Вискеном и его последующий разговор с героем. Уточнено описание головокружения и авторитета Вискена; сохранены комические реплики о сломанном кулаке и внезапном крике.


### Вычитка Dialogs.csv: строки 74061-74100
Сверены варианты вопросов к Вискену. Внутренний повтор «Мир — тлен» передан тем же словом в следующей реплике; уточнено описание правил гоблинов и хранения продуктов.


### Вычитка Dialogs.csv: строки 74101-74220
Сверены раскрытие природы Вискена и прощальные реплики. Повторено ключевое слово «тлен», исправлена поговорка о том, что Вискен считает Ост своим слугой, и согласовано название Податной гильдии.


### Вычитка Dialogs.csv: строки 74221-74300
Сверены политические взгляды Вискена и разговор о «разрыве» общества. Уточнены оттенки иронии, сохранён повтор метафоры «рвать», а финансовая защищённость приведена к единой формулировке в обеих репликах.


### Вычитка Dialogs.csv: строки 74301-74540
Сверены политические взгляды Вискена, его алиби и личные подробности. Подправлены реплики о войне и финансовой стабильности; сохранены шутки о кобольде, сломанном кулаке, бюрократической речи и подозрительной квартире в Дырах.


### Вычитка Dialogs.csv: строки 74541-74780
Сверены проверка карманов Вискена, переход к Водному пути и встреча с переплётчиком. Исправлена аббревиатура ВК по глоссарию, согласовано название фракции, а шутливые сценические указания о книгах и колоде приведены к естественному русскому.


### Вычитка Dialogs.csv: строки 74781-74900
Проверена первая встреча с переплётчиком. Птиценог/птицечеловек приведён к термину глоссария «птицелюд», обновлены реплики о Гильдии борьбы с вредителями и сохранена шутка с неуклюжим «гляну-проверю». Уточнены названия книжных стилей и обращения на «вы».

### Вычитка Dialogs.csv: строки 74901-75020
Сверены реплики о переплётчике, оплате и Гильдии борьбы с вредителями. Исправлены обращения, закреплён термин «Мешочек хранения», Primal приведено к «Праймл», а полурослики и народы более тёмных полос больше не смешиваются с птицелюдами. Сохранены шутка про перья и спор о частной и государственной службе.

### Вычитка Dialogs.csv: строки 75021-75100
Отредактированы реплики о борьбе с вредителями и сцена у дома ануранина. Восстановлены французские вставки героя и их русские пояснения; термин Подгородья сохранён.

### Вычитка Dialogs.csv: строки 75101-75140
В диалоге ануранина восстановлены французские фразы и сохранены русские пояснения. Сцена сверена с отсылкой на язык Урта.

### Вычитка Dialogs.csv: строки 75141-75180
Проверена сцена с ануранином. Сохранены французские вставки с русским переводом, а грубая реплика о подлизывании восстановлена без смягчения.

### Вычитка Dialogs.csv: строки 75181-75220
Проверены диалог о двери ануранина и сцена с грифоном. Сверено слово Common с глоссарием («общий язык»), сохранена французская игра с «местами интереса».

### Вычитка Dialogs.csv: строки 75221-75260
Сверена сцена с грифоном. Slog Dogs приведены к глоссарному «Слогдог»; подпись действия согласована с репликами о поглаживании.

### Вычитка Dialogs.csv: строки 75261-75300
Сверены повторные реплики о грифоне и передвижении по крыше. Второе упоминание Slog Dogs согласовано с глоссарным «Слогдог»; точнее передано первое касание крыла грифона.

### Вычитка Dialogs.csv: строки 75301-75340
Сверены реплики о пробуждении грифона и его угрозах. Сохранена нелепая колыбельная; выражение удивления приведено к естественному русскому восклицанию.

### Вычитка Dialogs.csv: строки 75341-75380
Отредактированы реплики гордого грифона: уточнены обращения, оскорбления и комментарии о гномах и грифонах.

### Вычитка Dialogs.csv: строки 75381-75420
Сверен спор о классе Жреца и других ролях героя. Уточнено, что герой научился общаться с грифоном за счёт магии, а его сравнение с гномьими слугами сохранено.

### Вычитка Dialogs.csv: строки 75421-75460
Сверены описания поездки грифона с моряками и его хозяина. Уточнены реплики о яркой одежде и понята шутка о том, что грифон не распознаёт оскорбление.

### Вычитка Dialogs.csv: строки 75461-75500
Отредактирована сцена Молочного рейса: уточнены пунктуация, выражение особого взгляда кобольда и его ломаная речь.

### Вычитка Dialogs.csv: строки 75501-75540
В сцене Молочного рейса валюта выравнена к форме «кроны». Recoup передано как «окупаемость» / «возврат вложений», что отделяет это от прибыли.

### Вычитка Dialogs.csv: строки 75541-75580
В повторных репликах Оста уточнено оскорбление в адрес члена Полпути. Поправлено обращение к кобольду, а не гоблину.

### Вычитка Dialogs.csv: строки 75581-75620
Проверены первые реплики у двери дома Миттеля. Сохранены шутки о мгновении и неожиданном тревожном приветствии; сверены обращения и имена.

### Вычитка Dialogs.csv: строки 75621-75660
Проверены продолжение сцены с Манием и дипломатическим иммунитетом. Торговая компания приведена к глоссарному названию «Асканий-Ридс».

### Вычитка Dialogs.csv: строки 75661-75700
Проверены шутки со Снеллом о названии горок и дипломатическая сцена у двери. Начато сверку знакомства с Норвикийским сопротивлением.

### Вычитка Dialogs.csv: строки 75701-75740
Сверена сцена с норвикийским сопротивлением. Поправлены пунктуация в атрибуции реплики, объяснено, что украли партию газет, и уточнёно оскорбление о ларперах.

### Вычитка Dialogs.csv: строки 75741-75780
Сверен диалог о нелегальной газете «Пение» и Азгалистском сопротивлении. Приведено к единому порядку название дворфской подруги.

### Вычитка Dialogs.csv: строки 75781-75820
В сцене с нелегальной газетой «Пение» сохранены резкие эпитеты, шутка о глупых детях и чувство неловкости от навязчивых объятий. Убраны буквальные обороты.

### Вычитка Dialogs.csv: строки 75821-75860
Проверен спор о нелегальной газете «Пение» и её распространении. Уточнено, что печать ведут на медных листах, и что речь о нелегальном издании. Название фильма приведено к глоссарной форме «Небесные пацаны».

### Вычитка Dialogs.csv: строки 75861-75900
Проверен диалог о выборах, сопротивлении и газете «Пение». Сохранены отсылки к социальному конфликту и сатира на ложную аполитичность.

### Вычитка Dialogs.csv: строки 75901-75940
Сверены реплики о демократии и божественном слове в политической сцене. Уточнена реплика о демократии как о необъятно сложном деле и восстановлена разговорная реакция на заговоры. Фраза о борьбе со злом приведена к смыслу «бороться со злыми силами».

### Вычитка Dialogs.csv: строки 75941-75980
Прояснено различие между Азгалами и Азгалистами по глоссарию. Термин «газеты» сверен в ветке о похищенной партии; возвращена игра слов на «хороший», чтобы не терять комизм вопроса о самочувствии.

### Вычитка Dialogs.csv: строки 75981-76020
Синхронизировано название газеты как «Пение Азгала»; согласовано название Азгалианской медной типографии с термином Azgalian. «Ларперы» заменены глоссарным «ролевики».

### Вычитка Dialogs.csv: строки 76021-76060
Проверена сцена с неоконтролируемой яростью героя и попыткой сжечь газеты. Уточнено замечание о законности и выправлена фраза о речи гоблина.

### Вычитка Dialogs.csv: строки 76061-76100
Сверена сцена с угрозой казни и голосованием. Уточнены грубоватые реплики, сохранены их чёрный юмор и нарастание ярости.

### Вычитка Dialogs.csv: строки 76101-76140
В сцене о законности и медной печати убрана калька. Уточнены действия и жесты в сцене давления на участников конфликта.

### Вычитка Dialogs.csv: строки 76141-76180
В сцене с прекращением расставлены паузы в реплике о поиске компромисса. Согласованы обращения к Модиссе и сихронизированы термины о газете.

### Вычитка Dialogs.csv: строки 76181-76220
Сверена сцена допроса под действием Зоны истины. Проверены обращения, имена и проверка правды; явных смысловых противоречий не обнаружено.

### Вычитка Dialogs.csv: строки 76221-76260
Синхронизированы дублирующиеся реплики о магии и обращение «Мистер Жрец»; исправлена строка, где вместо вопроса Ролло повторилось описание заклинания; проверена ветка с Гильдодцами Скалолома.

### Вычитка Dialogs.csv: строки 76261-76300
Проверена сцена с духом в мусорном баке. Primal сверен с глоссарием и другой репликой с духом Праймла; уточнены формулировки о перепалке с Гильдией фонарщиков и друидской помощи; проверено одноплечее пожатие.

### Вычитка Dialogs.csv: строки 76301-76409
Завершён хвост диалогов у мусорного бака, грузового люка и окна. Уточнены реплики о фонарях и помощи друида, выправлены описания жеста при заклинании и попытки проникновения через окно; исправлена ссылка на палец после неудачного взлома; сохранён юмор сцены.

### Вычитка EntityInfo.csv: строки 0-34
В первых описаниях объектов «первозданный дух» заменён на канонического «дух Праймла». Выправлены неестественные описания скелета, крысы и хижины на ножках.

### Вычитка EntityInfo.csv: строки 35-74
Исправлены две ошибки по ключам: описание пасти повторяло реплику о зелье, а строка о коробке повторяла отрицание о мимике.

### Вычитка EntityInfo.csv: строки 75-114
В трёх соседних описаниях о безопасности и заклинании тексты были смещены относительно исходника. Сверены с английским три отдельные подсказки.

### Вычитка EntityInfo.csv: строки 115-154
В описании зелья убрана калька «потребительский стандарт»; шутка передана естественной разговорной речью.

### Вычитка EntityInfo.csv: строки 155-194
Убраны кальки в описаниях сумки, зеркала и записки на свитке; два описания гоблинов сделаны естественнее.

### Вычитка EntityInfo.csv: строки 195-234
Устранено повторение предыдущего описания; уточнены подписи к ремонту корней и мастерству садовника; выправлено обращение к Саду в заметке Нессы.

### Вычитка EntityInfo.csv: строки 235-274
«Термин «мужчина-мерфолк» согласован с глоссарием. Уточнены описания доков и вывесок; убраны лишние точки в цитатах.

### Вычитка EntityInfo.csv: строки 275-314
Сверена «Эпоха тайной магии» с глоссарием. Выправлены кальки в описаниях окна, входов и грузового люка; уточнена надпись про игру гоблина на гитаре.

### Вычитка EntityInfo.csv: строки 315-354
Аббревиатура LR оставлена без расшифровки по глоссарию; выправлена ошибка в роде слова «вырезка»; уточнены подписи к надписи и предметам.

### Вычитка EntityInfo.csv: строки 355-394
Исправлена ошибка в переводе совета о профсоюзе: английское выражение означает нарушение правил. Уточнены направления и описания лестниц, выходов и рычага.

### Вычитка EntityInfo.csv: строки 395-434
В двух сюжетных описаниях гоблинов и дворфа перепутались соответствия ключей; сверены и исправлены.

### Вычитка EntityInfo.csv: строки 435-474
Магистр согласован в подписи к чёрному ходу и в диалоге Эттир; выправлены описания гоблина, инструмента и чайной.


### Вычитка EntityInfo.csv: строки 475-514
Подпись о древней реликвии сделана грамматически естественной. Лозунг строительной компании передан как её рекламный слоган; обе повторные строки синхронизированы.

### Вычитка EntityInfo.csv: строки 515-554
Подпись о судьбе переформулирована в естественное предупреждение.

### Вычитка EntityInfo.csv: строки 555-634
Имя «Лунная Кровь» согласовано с глоссарием. Выправлены описания гнезда и озёрной твари; подпись о участи приведена к естественной речи.

### Вычитка EntityInfo.csv: строки 635-714
Сверены имена с глоссарием. Уточнены названия сейфа Фристрайдеров и неисправных карманных мотоциклов; улучшено описание замёрзшего ростка.

### Вычитка EntityInfo.csv: строки 715-772
Названия «Куб стресса» и «Боевой молот» сверены с названиями предметов; Кабинки чайной названы по контексту; магическое «послание» согласовано с глоссарием.

### Вычитка Feats.csv: строки 0-103
Сверены названия особенностей и игровая механика с глоссарием. Название особенности передано как «Азгалианский дух»; финал случайного критического успеха сохраняет комическую реплику о кратком счастье.

### Вычитка Glossary.csv: строки 0-154
Термин о статусе гражданина уточнён: «гражданство». Согласованы термины Кланлендов и ярлства; уточнено число знатных семей в правительстве.

### Вычитка Glossary.csv: строки 155-234
Уточнено описание эльфов пояса Им: убрана несклоняемая калька. В статье о прежнем имени Тростников ясно связаны переименование и разные оценки этого названия.

### Вычитка Glossary.csv: строки 235-354
Исправлено склонение в названии законов; карманные мотоциклы сверены с термином в другом разделе.

### Вычитка Glossary.csv: строки 355-434
Выравнены названия Бюро посланий, Подводного побережья и мейфитов. Пороховое заклинание согласовано с его описанием; газета стала поддерживать Азгалов, а не Азгалистов.

### Вычитка Glossary.csv: строки 395-474
Синхронизированы названия пороховых рыцарей и заклинания; в статье об ожерелье уточнено число оставшихся бусин.

### Вычитка Glossary.csv: строки 475-514
В статье о земледельцах убрано обращение с противоположным смыслом; исправлено числовое согласование с названием валюты.

### Вычитка Glossary.csv: строки 515-594
Название игры с крокодилом согласовано с репликой в диалоге. Олд Диминор употреблён в предложном падеже; исправлена калька в статье о гедонистах; термин «Шёлк Има» сверен с глоссарием.

### Вычитка Glossary.csv: строки 595-834
Отредактированы справки об отражении света, шёлке Има и Камешке послания. Уточнены формулировки об эпохе промышленной революции, птицелюдах и документе для поездок между портами. Проверены статьи о праздниках, Джоре, народах Има и русалках.
Убрана латинская аббревиатура из объяснения прозвища «ролевик»; название Ветроломного хребта приведено к единой форме.
В статье об ИНУ удалено английское название; описание личей уточнено: их создают и поддерживают поглощением душ.
Уточнено описание основания Норвика в период Великого проекта; расщелина в районе Дваргби названа главной достопримечательностью района.
Исправлена смысловая подмена в статье об анурах: вместо описания драконьей культуры теперь указаны кочевой образ жизни, происхождение и прозвище народа.
Сверены статьи о денежных единицах, эпохах, магических существах и политических силах. Во второй статье об анурах исправлено ошибочно перенесённое описание политической партии: теперь речь идёт о лягушколюдях и жаболюдях.
В пояснении к уличной аббревиатуре убрано английское раскрытие; смысл шутки передан по-русски.
Сверены названия должностей магистратов и их обязанности. В статье о роде Ярн заменено латинское написание старой формы на кириллическое.

### Вычитка Glossary.csv: строки 595-674
Отредактированы справки об отражении света, шёлке Има и Камешке послания. Проверены статьи о праздниках, Городе под городом, монстрах и странниках; сюжетные сведения и шутливый тон сохранены.

### Вычитка Glossary.csv: строки 675-794
Проверены статьи о праздниках, Джоре, Име и птицелюдах.

### Вычитка Glossary.csv: строки 1475-1674
Сверены статьи о Совете Азгала, друидизме, поддворфах, магических предметах и мире Има. Уточнено обращение к старшим в Совете, значение старого английского слова и описание магически подтверждённого гендера; японская отсылка в справках о народе Има приведена к внутриигровому названию.

### Вычитка Glossary.csv: строки 1675-1754
Проверены статьи о фашизме, Ордене Первых Рыцарей, Уртгарде и Идущих Богах. Исправлена временная формулировка об Урте: он был последним известным Идущим Богом к моменту угасания.

### Вычитка Glossary.csv: строки 1755-1794
Сверены статьи о газетах Норвика, Реконкисте и дворфских землях. «Фонд воскрешения» и «Театральная улица» приведены к контексту; убрано лишнее упоминание отдельной эпохи в статье о роде Рёйкфолл.

### Вычитка Glossary.csv: строки 1795-1834
Проверены статьи об идеологиях, драконах и поселениях. Уточнено, как новые исторические сведения повлияли на оценки города Эван; высадка орков теперь отнесена к Джору как миру, а не к вымышленному царству.

### Вычитка Glossary.csv: строки 1835-1874
Сверены термины о церкви, географии и некромантии. «Литианский мор» заменён на «Литианскую топь», что соответствует описанию местности как болота.

### Вычитка Glossary.csv: строки 1875-1914
Исправлена формулировка об Оргро: он был одним из последних, кто сопротивлялся Урту, без неподтверждённого упоминания о других вождях. Убраны два ложных уточнения, что деревня Горони́т правится абишаем и что Выз-Ха — отдельное королевство.

### Вычитка Glossary.csv: строки 1915-1994
Проверены статьи о Вольных городах, идеологиях, троллях и поселениях Аскании. Смысл терминов и исторические события сверены с исходными описаниями; исправлений, требующих отдельной записи о ширине, в этом диапазоне не понадобилось.

### Вычитка Glossary.csv: строки 1995-2034
Название Upperdungeon приведено к уже употреблённой в описании форме «Верхнее подземелье». Проверены статьи о ярлствах, озере Примус и Великой черепахе.

### Вычитка Glossary.csv: строки 2035-2074
Сверены статьи о Выз-Ха, Тиделе, Валькириях и Вольных городах. Термины согласованы с описаниями экономических и религиозных институтов мира.

### Вычитка Glossary.csv: строки 2075-2114
Проверены статьи об азгалистских текстах, торговых путях и Директорате Цетсхли. Проверена связность терминов и сохранён юмор в справках о Звере Исканий и заклинаниях.

### Вычитка Glossary.csv: строки 2115-2154
Проверены справки о гиенолюдах, стали Нуллстил и невещественных планах. Формулировка о ценности уцелевшей стали согласована с исходным указанием «на Джоре».

### Вычитка Glossary.csv: строки 2155-2172
Завершена сверка заключительных статей о планах, Адах и выражении Je-baited. Шутливое отступление в последней статье сохранено.

ItemTexts.csv, строки ItemDesc_41–ItemDesc_100: вычитаны в сравнении с оригиналом. В ItemDesc_81 исправлена реакция Патриарха: английское *flip out* означает сильное раздражение, а не восторг; формулировка сохранена в src/voice/manual_fixes.json.

ItemTexts.csv, ItemDesc_122 и ItemDesc_124: выправлены регистр в названии книги и формулировка описания реестра.

ItemTexts.csv, названия предметов: исправлены значения ItemName_9, ItemName_11, ItemName_13, ItemName_28, ItemName_34 и ItemName_41; проверены строки и ключи по оригиналу.

ItemTexts.csv, названия предметов: уточнены формулировки ItemName_55, ItemName_57 и ItemName_82.

ItemTexts.csv: ItemName_120 приведено к русскому названию «брусника», ItemName_122 — к значению «замасленные инструкции».

ItemTexts.csv: названия и описания белой и жёлтой крыс приведены к грамматически согласованному женскому роду.

ItemTexts.csv: ItemVarModDesc_35 приведено к игровому термину «бонус мастерства».

ItemTexts.csv: завершена вычитка 386 пар. Терминология «аберрация» и «бонус мастерства» синхронизирована с глоссарием и остальными игровыми текстами.

MiscTexts.csv, строки 0-39: «Constitution» приведено к термину «Телосложение»; уведомления о предметах и этапах заданий переформулированы без ошибок падежа и пунктуации.

MiscTexts.csv, UI_Exhaustion: сокращение «выдох» исправлено на «ур. ист.» по игровому термину «истощение».

MiscTexts.csv: уведомления SpellSlot_Available и SpellClick_NoSlot приведены к термину «ячейки заклинаний» и грамматически согласованы с числительными.

MiscTexts.csv: в системных сообщениях синхронизировано понятие бонуса мастерства; дата приведена к русскому порядку «день, месяц, год».

MiscTexts.csv: в PillarScene_Constitution10_1 восстановлены «живот» и первобытный ужас из оригинала.

MiscTexts.csv: PillarScene_BigMessage_0 переформулирован так, чтобы герой, а не глаза, был ослеплён вспышкой; сохранено постепенное привыкание к свету.

MiscTexts.csv: в финальных репликах про свидания, варвара и муравья восстановлен смысл оригинала и сохранена комическая интонация.

MiscTexts.csv: финальные строки о Золотой Орде отредактированы для естественного русского синтаксиса с сохранением образа сияющего ока.

MiscTexts.csv: устранены грамматические сбои в заключительных характеристиках; в служебных сообщениях синхронизированы «ячейка заклинания» и «уровень истощения».

MiscTexts.csv: сообщения ExamineItem_* переведены с учётом игровых ячеек заклинаний и контекста лечения; сообщения о карманной краже отредактированы.

MiscTexts.csv: подтверждения произнесения и замены заклинаний синхронизированы с игровыми терминами; уточнён знак вопроса.

MiscTexts.csv: в подтверждении короткого отдыха указана кость хитов; уведомление о ладане использует термин «ячейка заклинания».

MiscTexts.csv: подпись кнопки SpellBook_Target приведена к общему переводу Cast — «Сотворить».

MiscTexts.csv: подсказки SpellTile_ShortRest_* приведены к обращению на «ты» и согласованы с терминами ОЗ, истощения и ячейки заклинания.
