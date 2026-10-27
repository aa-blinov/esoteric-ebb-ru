# Эбб

A complete Russian localization of Esoteric Ebb: 81,891 translated lines in
twelve CSV files, installed as a language folder that the game loads next to
the English one.

[Русская версия этого описания](README_ru.md).

Esoteric Ebb ships its own localization pipeline. The game reads
`StreamingAssets/Localization/<Folder>/*.csv` at startup, and the developer
tells translators to copy the `Template` folder, fill it in, and keep the word
"Template" out of the name. This repository is that folder, filled in.

![The main menu in Russian](docs/screenshots/menu-ru.png)

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![CI](https://github.com/aa-blinov/esoteric-ebb-ru/actions/workflows/ci.yml/badge.svg)](https://github.com/aa-blinov/esoteric-ebb-ru/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12-blue)](src/)

---

## Quick start

Download the [v1.0.0 localization archive](https://github.com/aa-blinov/esoteric-ebb-ru/releases/download/v1.0.0/esoteric-ebb-ru-v1.0.0.zip)
and extract its `Russian` folder into the game's
`Esoteric Ebb_Data/StreamingAssets/Localization/` directory. Find the game
folder in Steam with **Manage → Browse local files**.

Alternatively, copy the folder from a source checkout:

```bash
git clone https://github.com/aa-blinov/esoteric-ebb-ru.git
cp -r esoteric-ebb-ru/translation/Russian \
  "/c/Program Files (x86)/Steam/steamapps/common/Esoteric Ebb/Esoteric Ebb_Data/StreamingAssets/Localization/"
```

Then in the game: **Options → Language → Русский**. The language also switches
with **V** and **B** while playing, and **Ctrl+R** re-reads the CSV files
without a restart.

The game writes its own preference, so the choice survives a restart. To set it
without touching the menu:

```json
// %USERPROFILE%\AppData\LocalLow\Christoffer Bodegard\Esoteric Ebb\SETTINGS.es3
"LanguageCode" : { "__type" : "string", "value" : "RU" }
```

## What it does

- **Every line of the game.** 81,891 strings across dialogue, the codex, spells,
  feats, items, quests, the character sheet and the interface. Every source
  line that carries text has a Russian one. Rows with an empty English source
  stay empty, except for the game's intentionally blank `Popup_194`, which uses
  a zero-width space so the game does not display its quote placeholder.
- **One voice for the whole game.** The terms were translated first and frozen
  in a glossary of 1,838 entries; every later pass was bound to that glossary.
  2,219 repeated lines that had been translated differently in different places
  were reduced to a single wording each.
- **Typography that survives the layout.** Russian needs a few characters more
  than English in the same box, and the game's panels are fixed size. The
  translation was measured against the real panel widths and the real font
  metrics; every line that did not fit was shortened or given a smaller size,
  and the dialogue text size was lowered so the Russian occupies the space the
  English did. `docs/layout.md` holds the measurements.
- **Inline markup left alone.** `<i>`, `<b>`, `<u>`, `<s>`, `<shake>`,
  `<wiggle>`, `<size=N>`, `<color=#RRGGBB>` and placeholders such as `{CLERIC}`
  are checked row by row against the English source. No row differs.
- **A repeatable pipeline.** The translation was built by a script that is in
  this repository, not by hand. It caches every model call, so a run can be
  interrupted and resumed without spending anything twice.

## Screenshots

| Main menu | Options |
| :---: | :---: |
| ![Main menu](docs/screenshots/menu-ru.png) | ![Options](docs/screenshots/options-ru.png) |

| Character creation | In-game scene |
| :---: | :---: |
| ![Character creation and Strength lore](docs/screenshots/character-ru.png) | ![Gameplay tooltip](docs/screenshots/gameplay-ru.jpg) |

## Configuration

| Setting | Value | What it does |
| --- | --- | --- |
| `LanguageCode` | `RU` | The language the game starts in. `EN` returns to English. |
| `FontSize` | `22` | Size of the dialogue text. The developer recommends 24 for English; at 24 the Russian takes a line more in the fixed panels, so 22 or 20 is the right size. |
| `UIFontSize` | `0` | Interface size: 0 ordinary, 1 large, 2 huge. Nothing below ordinary exists. |
| `FontIndex` | `6` | The dialogue font. 0 is Ebberia and 2 is Josefin Sans; neither of them carries any Cyrillic, and the game draws the Russian text of such a panel as a row of runes. The installer moves the setting to Ubuntu when it finds one of the two. |

Every one of these lives in `SETTINGS.es3` and survives a restart. The game
rewrites the file when it leaves, so the setting has to be changed while the
game is closed.

## Known issues

Two of them belong to the game and cannot be fixed by a translation.

- **The light mode empties one panel.** The game rebuilds parts of the
  interface when the light mode is switched at runtime, and the panels it
  rebuilds take their text from the strings of the game itself and not from
  the folder of the language. The column of examples next to the settings
  turns into English in the Russian build; the Chinese build keeps its
  Chinese, because the developer put his own Chinese in the same place. The
  rest of the interface stays Russian, and a restart reads the localization
  again.
- **A few strings of the developer are in Russian already.** The tooltip of a
  spell slot, the screen that blocks a session and a few numbers of the
  options carry the Russian of the developer, not the translation. The
  measurements are in `docs/layout.md`.

## Checking the voice

`scripts/scan_ai_patterns.py` reads every line of the localization, looks for
the patterns of machine-written prose in Russian, and prints the lines next to
their English source, together with the rate of the connectives and the em
dashes on both sides. The English source is the yardstick: a Russian line
that carries such a word is faithful when the source carries it too.

```bash
python3 scripts/scan_ai_patterns.py --verbose
```

## Install it on your own copy

**1. Take the folder.** The translation is the `translation/Russian/` folder of
this repository. It holds the twelve CSV files and nothing else.

**2. Put it next to the languages of the game.** Copy the folder into the
`Localization` folder of the game, so that the game sees three folders there:

```
Esoteric Ebb_Data\StreamingAssets\Localization\
├── Official\          English and Chinese, as the developer shipped them
├── ChineseCommunity\  A translation by the community
└── Russian\           ← the folder you copied
```

The path of the game depends on where Steam put it. The usual one is

```
C:\Program Files (x86)\Steam\steamapps\common\Esoteric Ebb\Esoteric Ebb_Data\StreamingAssets\Localization\
```

and on another drive it starts with the drive of that copy of Steam, for
example `D:\SteamLibrary\steamapps\common\Esoteric Ebb\...`. Right click the
game in Steam → Manage → Browse local files, and the folder is there.

**3. Start the game and pick the language.** `Options → Language → Русский`.
The keys `V` and `B` switch the language while the game runs, and `Ctrl+R`
reads the files again without a restart.

**4. If the language is not in the list,** two things are usually wrong. The
first line of every one of the twelve files has to name the language in its
last column:

```csv
ID,RU
```

and `MiscTexts.csv` has to carry these two lines:

```csv
ID,Speaker,RU
LanguageDropdown,,Русский
FallbackLanguage,,EN
```

`FallbackLanguage` is the language the game falls back to when a line is
empty, and it stays `EN` in the Russian folder: an empty line shows the
English original of the game, which is the wanted behaviour.

**5. Set the size and the font.** The file of the settings is

```
%USERPROFILE%\AppData\LocalLow\Christoffer Bodegard\Esoteric Ebb\SETTINGS.es3
```

and it is plain JSON. The three lines that matter are

```json
"LanguageCode" : { "__type" : "string", "value" : "RU" },
"FontSize"     : { "__type" : "int",    "value" : 22 },
"FontIndex"    : { "__type" : "int",    "value" : 6 }
```

`FontSize` sets the size of the dialogue text. The developer recommends 24 for
English; at 24 the Russian takes a line more in the fixed panels, so 22 or 20
is the right size. `FontIndex` picks the dialogue font, and 6 is Ubuntu.
The two fonts that carry no Cyrillic at all are Ebberia (0) and Josefin Sans
(2); the game draws a rune for every missing letter, so a Russian line in
them reads as a row of runes.

The game rewrites the file when it leaves, so the settings have to be changed
while it is closed.

**6. After a Steam update.** The update does not touch the `Russian` folder,
but if it is gone, copy it again from this repository. The current version is
always the folder in this repository.

## How it works

The game loads one folder per language. The columns inside a file are named by
language code, so a folder carries a single column:

```
StreamingAssets/Localization/
├── Official/          English and Chinese, as the developer shipped them
├── Template/          An empty folder with the right keys and the code F1
├── ChineseCommunity/  A translation by the community
└── Russian/           This repository
```

The pipeline that produced `Russian/` runs in six stages:

```
corpus ──▶ terms ──▶ names ──▶ bulk ──▶ edit ──▶ canon ──▶ QA
```

1. **Corpus.** The English CSVs are parsed into one JSON line per string.
2. **Terms and names.** The codex terms and the 1,319 proper nouns are
   translated first, grouped by stem so that singular and plural do not drift
   apart. The result is the glossary every later stage is bound to.
3. **Bulk.** The remaining 81,891 strings are translated in batches of about
   3,200 characters. Neighbouring lines of one dialogue go into the same batch,
   so the voice of a speaker survives. Each batch carries the glossary terms it
   needs.
4. **Edit.** An editor reads the finished translation against a written style
   code and rewrites what the code asks for: register, rhythm, agreement,
   typographic marks. 7,790 rows changed.
5. **Canon.** Repeated source lines are collapsed onto one wording each.
6. **QA.** Every row is checked for markup drift, for English words left
   inside Russian sentences, for unbalanced quotes and for width against the
   panel it has to fit in.

`docs/architecture.md` has the detail, `docs/style-guide.md` the style code the
editor works from, and `docs/layout.md` the measurements behind the width
rules.

## Development

```bash
python3 -m pip install -r requirements.txt   # httpx, fonttools, unitypy
python3 -m unittest discover -s tests         # check the shipped CSV files
python3 src/build.py --help                   # run the pipeline
```

The tests read `translation/Russian/*.csv` and fail on a missing key, a
changed markup set, a straight quote, a three-dot ellipsis or an English word
inside a Russian sentence. The same checks run in CI.

## License

[MIT](LICENSE), © Alexander Blinov.

Esoteric Ebb is by Christoffer Bodegård. This repository holds a fan
translation; the game, its text and its art stay with their authors.
