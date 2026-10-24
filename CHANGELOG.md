# Changelog

All notable changes to Esoteric Ebb RU. Versions are ordered newest first.

## [Unreleased]

### Added

- Nothing yet.

## 0.11.0 (2026-10-25)

### Fixed

- **The prompt on the splash screen fits the sky.** The line «Нажмите любую
  кнопку» is 778 px wide in the display font of the game, and the English
  «Press Any Button» is 504 px. The text is centred, and the Russian one
  reached under the cloud on the left: only «Е ЛЮБУЮ КНОПКУ» could be read.
  The size of the line is 36 now, and it measures 517 px.
- **The declension of «Телосложение».** Two lines of the loading tips read
  «проверку Телосложениеа» and «модификатора Телосложениеа». The word is a
  feminine noun, and both lines now read «Телосложения».
- **The category of the cantrips keeps one case.** The name was written
  «КантРИПЫ», with the last four letters in capitals, which the decorative
  font of the game draws at full height in the middle of a word. It is
  «Кантрипы» now, and the glossary carries the same spelling.

## 0.10.0 (2026-10-24)

### Fixed

- **The deep storage keeps its words.** The name sits in a column of about
  140 px, and both Russian words were a little too wide on their own:
  «Глубокое» broke into «ГЛУБОКО» and «Е», and «хранилище» into «ХРАНИЛИ» and
  «ЩЕ». The size of the name is 30 now and the words break at the space.
- **The overlap in the tooltip of a spell slot is not ours.** The words «пр»,
  «ОТ» and «ПРОВАЛА» are in no Russian file of this repository and in no
  string of the game either: the developer ships a partial Russian of their own
  in the assets. The only word of that line that belongs to the translation is
  `Failure`, and it reads «Провал».

## 0.9.0 (2026-10-24)

### Fixed

- **The names on the bar on top of the screen stay inside it.** The English
  names are one word each, and the Russian ones were longer: «ПОИСК» and
  «ПРИКЛЮЧЕНИЙ» fell out of the bar, «КНИГА» and «ЗАКЛИНАНИЙ» ran past its
  right edge. The names are now «ЗАДАНИЯ», «ИНВЕНТАРЬ», «ЖУРНАЛ»,
  «ЗАКЛИНАНИЯ» and «ЛИСТ».
- **Two more buttons hold their word.** «Завершить» broke into «ЗАВЕРШИ» and
  «ТЬ», and «Специализации» was flush with the edge of its panel. They are
  «Готово» and «Профессии» now.
- **The head of the collected spells panel fits.** «Собранные заклинания» did
  not fit the width of the panel and the last letter was cut off.

## 0.8.0 (2026-10-24)

### Fixed

- **The names in the uses of an ability no longer break in half.** The third
  tab of the lore panel is narrow, and the Russian names are a third wider than
  the English ones. Six of them came out in two pieces: «НАЦИОНАЛИЗ» over «М»,
  «МУЖЕСТВЕННО» over «СТЬ», «РЕСПУБЛИКА» over «НЕЦ», «ПОДГОТОВ» over «ИТЬ»,
  «АЗГАЛИАНС» over «КОГО» and «АПОЛИТИЧЕ» over «СКОЙ». Five names keep their
  words and lose only their size; «мужественность» is fourteen letters and
  cannot be made to fit at a readable size, so it becomes «мужество».

### Measured

The uses column is about 400 px wide on the narrow tabs and about 500 px on the
wide one, and each name was measured on its own tab. The measurements are in
`docs/layout.md`.

## 0.7.0 (2026-10-24)

### Fixed

- **The heading of the uses of Strength no longer peeks out from under the
  bubble.** The lore panel is one column, and the Russian description is a line
  shorter than the English one, so «Большая Сила» rose up under the pink bubble
  that covers the foot of the panel. The footnote takes that line back: three
  lines of one sentence each, and the name in capitals one size smaller, so it
  no longer breaks in the middle of the phrase.

### Changed

- `src/ebru/measure_width.py` had no `ROOT` in it and did not run on its own.

### Checked

- The seven fonts of the dialogue text — Ebberia, EB Garamond, Josefin Sans,
  Open Dyslexic, PT Serif, Roboto and Ubuntu — all draw the Russian without a
  missing glyph.
- The dialogue font reaches the lore panel of the character screen: the
  description and the footnote are drawn in it, and so the size of the dialogue
  text decides how many lines they take. The size the translation is held to
  is 20, and the measurements are in `docs/layout.md`.

## 0.6.0 (2026-10-24)

### Fixed

- **The graphics panel no longer breaks its words.** The column of values is
  140 px wide and holds about ten Russian letters. «Безрамочный» broke into
  «Безрамочны» and «й», and «ВЕРТИКАЛЬНАЯ СИНХРОНИЗАЦИЯ» took three lines and
  rode up over the resolution above it. The refresh rate is `VSYNC` now, the
  name the game's own English string uses, and the two display modes are
  «Полный экран» and «Без рамки».
- **The entries of the refresh rate list are spaced.** The game writes the
  caption of the field as `{0} ({1})` and the entries of the open list as
  `{0}({1})`, so the list showed «VSYNC(72)» without a space. The string
  carries a non-breaking space of its own now, and the list reads «VSYNC (72)».

### Measured

The value column of the settings panel is 140 px and the label column 216 px.
The English values fit on one line; the Russian ones did not. The measurements
are in `docs/layout.md`.

## 0.5.0 (2026-10-24)

### Fixed

- **The day label under the clock no longer breaks.** The Russian `День {0}` is
  123 px wide, the line it is drawn in holds less than that, so the number
  wrapped onto a second line and the word rode up over the rule under the
  clock. The label is `день {0}` now: it fits on one line, and the display font
  draws lower case as small capitals, so it reads «ДЕНЬ 1» beside the clock, the
  same shape as the English «DAY 1».

### Measured

The label under the clock is 94 px wide in English. The Russian «День 1» needs
123 px and «день 1» needs 107 px, which is what the line holds. The
measurements are in `docs/layout.md`.

## 0.4.0 (2026-10-24)

### Fixed

- **The narrow arrow button on the character screen no longer wraps.** It
  takes its label from the menu strings, and the display font is wide: nine
  letters did not fit, so the word broke and its tail landed under the
  divider. «Продолжить» is «Дальше» and «Завершить» is «Готово».
- **The tab between "Знания" and "Роль" no longer wraps.** «Применения» is
  «Польза».
- **The lore of Strength fits the panel again.** At 390 characters it is
  exactly as wide as the 451 characters of the English original, because a
  Cyrillic letter costs about 0.52 em and an English one about 0.45.

### Measured

The display font breaks a word that does not fit, and the tail lands under
whatever is below. The narrow boxes on the character screen hold about
eight characters. The scripts that check the lengths are in `scripts/`.

## 0.3.0 (2026-10-24)

### Fixed

- **The background descriptions no longer run under the ability badges.** The
  panel that holds a character's past is four lines tall and the badges are
  drawn over the fifth. The Russian needs about a line more than the English
  does, so seventeen backgrounds were rewritten to fit; the two longest are
  now a third shorter than their source.
- **The lore of Strength no longer pushes its footnote out of the panel.** It
  was the longest of the six by a wide margin, and the last line of the
  footnote ended up behind the notice band.

### Measured

The panel that holds a character's past is 541 px wide with a text area of
about 470 px, which fits four lines of roughly 38 characters. The ability
badges are drawn over the fifth. The budget for a background description is
therefore 130 characters, and the scripts that check it are in `scripts/`.

## 0.2.0 (2026-10-24)

### Fixed

- **Short interface labels read in context.** A one-word label is the hard
  case: the model that translated them in a batch had nothing but the word
  itself, and the dictionary sense is often the wrong one. 1,656 short labels
  were reviewed against their English source, and 173 corrections went in.
- `Menu_Button_Load` read «Нагрузка» in the main menu, where the game itself
  says «Загрузить файл». It reads «Загрузка» now.
- **Constitution** was «Устав», a statute, where the ability is a physique.
  It is «Телосложение» everywhere, in the character sheet and in the text.
- **Lawful** was «Законный», a noun. The alignment is «Законопослушный».
- **Warlock** and **sorcerer** were both «чародей». A warlock is «колдун»
  in this game's Russian, and «чародей» belongs to the sorcerer.
- Forty lines that had an English word inside a Russian sentence, and nine
  that had never been translated at all, including a whole paragraph of
  Rollo's article.
- The term **lesser** is now «младший» throughout, the game's own way of
  ranking things.

### Changed

- The repository carries the review scripts, so the same pass can be run over
  a new build of the game.

## 0.1.0 (2026-10-24)

### Added

- The first release: a complete Russian translation of Esoteric Ebb, 81,883
  lines in twelve CSV files, installable by copying one folder into the game's
  localization directory.
- A glossary of 1,838 terms and proper names, frozen before the body text was
  translated and bound to every later pass.
- A literary editing pass over the whole corpus: 7,790 rows rewritten against
  a written style code, and 2,219 repeated lines collapsed onto a single
  wording each.
- A typography pass: 43,264 straight quotes and 7,867 three-dot ellipses
  replaced by the Russian forms.
- A width pass against the fixed panels of the character screen, and a
  dialogue text size of 20 instead of 24, so the Russian occupies the space
  the English did.
- A test suite that fails on a missing key, a changed markup set, a straight
  quote, a three-dot ellipsis or an English word inside a Russian sentence.
