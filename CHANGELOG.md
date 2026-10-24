# Changelog

All notable changes to Esoteric Ebb RU. Versions are ordered newest first.

## [Unreleased]

### Added

- Nothing yet.

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
