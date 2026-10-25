# AGENTS.md, the agent context for `Esoteric Ebb RU`

The Russian localization of Esoteric Ebb: twelve CSV files the game loads as a
language, and the pipeline that produced them.

## Run / build / test

```bash
python3 -m pip install -r requirements.txt   # httpx, fonttools, unitypy
python3 -m unittest discover -s tests         # validate the shipped CSV files
python3 src/build.py --stage all              # run the whole pipeline
python3 src/build.py --stage typography       # one stage
```

A pipeline run needs a model endpoint. `src/llm_client.py` reads it from
`Mavis`'s local runtime (`http://127.0.0.1:8080`) or from `LLM_BASE_URL` and
`LLM_API_KEY`; every call is cached under `work/cache/`, so a re-run costs
nothing until the prompt changes.

Installing into the game:

```bash
python3 src/build.py --install --game-dir "/c/Program Files (x86)/Steam/steamapps/common/Esoteric Ebb"
```

## Where things live

| Path | What it is |
| --- | --- |
| `translation/Russian/` | The twelve CSV files the game reads. This is the artifact. |
| `src/` | The pipeline: corpus extraction, translation, editing, canonicalisation, QA. |
| `src/voice/` | The style code the editor works from, and the frozen glossary. |
| `tests/` | The checks that run in CI and before every install. |
| `scripts/` | The installer, the width measurement, the scan for machine-written prose. |
| `docs/` | The style guide, the glossary, the layout measurements, the architecture. |
| `work/` | Scratch space: the corpus, the caches, the intermediate passes. Not committed. |

## Traps

- **The game reads the CSV files at startup.** A change to
  `translation/Russian/` needs a restart, or **Ctrl+R** inside a running game.
  Reloading does not re-create the language list, so a *new* folder needs a
  restart.
- **`LanguageCode` lives in the game's settings, not in the folder.**
  `%USERPROFILE%\AppData\LocalLow\Christoffer Bodegard\Esoteric Ebb\SETTINGS.es3`
  holds `"LanguageCode" : { "value" : "RU" }`. The game rewrites this file on
  exit, so edit it while the game is closed.
- **A folder name may not contain the word "Template".** The game reads every
  folder in `Localization/` as a language, and the template is not one.
- **The column code is the language code.** Every file in the folder ends with
  a column headed `RU`, and the header row is the first line of the file.
- **One English line, one Russian line.** The same source line appears in
  several places in the game, and the translation has to be the same in all of
  them. `src/canonicalise.py` enforces this; running it after any hand edit
  is the cheapest way to keep it true.
- **Width is measured, not estimated.** `scripts/measure_width.py` reads the
  real font metrics out of the game's assets. A line that passes the
  character-count check can still overflow the panel.
- **The game's dialogue size is the global lever.** `FontSize` in
  `SETTINGS.es3` is 24 in the original and 22 for the Russian text. Changing
  it invalidates the width measurements in `docs/layout.md`. The game writes
  its own value back when it leaves, so the file has to be checked afterwards.
- **The fonts are the game's.** Two of the seven dialogue fonts carry no
  Cyrillic at all: Ebberia and Josefin Sans. The game does not show a missing
  glyph in them, it draws a rune, and a Russian line comes out as a row of
  runes. Ebberia is the first entry of the list and the default, so the
  setting has to be corrected before the first line is readable.
  `scripts/install.py` moves the setting to Ubuntu when it finds one of the
  two.
- **An empty line is not an empty line.** The game falls back to the English
  original of its own assets when a cell is empty, and a cell of nothing but a
  space is trimmed before the lookup. The zero width space (`U+200B`) is the
  only thing that stays empty, and it is the only way to leave a line out on
  purpose.
- **The panels that the game rebuilds at runtime are filled from the game's
  own strings**, not from the folder of the language. The light mode rebuilds
  the panel of the examples, and it comes out in English, because the
  developer's own Chinese is in that place in his build.
- **Keep the markup.** `<i>`, `<b>`, `<size=N>`, `{CLERIC}` and the rest are
  checked row by row against the English source. A dropped tag is a broken
  line in the game, not a typo.
- **The English source is the yardstick.** `scripts/scan_ai_patterns.py`
  looks for the patterns of machine-written prose in the Russian and prints
  the lines next to their source. A Russian line that carries such a word is
  faithful when the source carries it too; rewriting it would only make it
  stranger.

## Style / safety rails

- **Comments explain *why*, never *what*.**
- **No emojis**, in any file. The house style bans them and the checker
  fails the build.
- **Do not add a dependency without a reason written down next to it.**
- **Do not remove functionality that looks intentional.** Ask first.
- **The translation's voice is fixed.** `docs/style-guide.md` is the contract
  with the editor; a hand edit that breaks it will be corrected by the next
  run of the editor pass.
- **A correction goes into the CSV file and into
  `src/voice/manual_fixes.json`**, or the next run of the pipeline will undo
  it.
- **A correction is measured and written down.** The measurement belongs in
  `docs/layout.md`, the change in `CHANGELOG.md`. The house check of the
  organisation lives in `golden-repo/scripts/`, outside this repository, and
  both of its checkers have to stay quiet.

## The workspace around the repository

The repository is worked on from a workspace one level up, where the game
lives and the helpers that drive it are kept. `../AGENTS.md` of that
workspace describes the layout, the order of the work and the traps of the
game window. Two of them matter most: the game reads the localization once,
at the start, and it rewrites its own settings file when it leaves.
