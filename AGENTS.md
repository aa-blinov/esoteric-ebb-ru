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
| `scripts/` | Helpers for installing and for measuring panel widths. |
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
  `SETTINGS.es3` is 24 in the original and 20 for the Russian text. Changing
  it invalidates the width measurements in `docs/layout.md`.
- **The fonts are the game's.** Two of the seven dialogue fonts carry no
  Cyrillic at all. A Russian player has to pick EB Garamond or PT Serif in
  the options.
- **Keep the markup.** `<i>`, `<b>`, `<size=N>`, `{CLERIC}` and the rest are
  checked row by row against the English source. A dropped tag is a broken
  line in the game, not a typo.

## Style / safety rails

- **Comments explain *why*, never *what*.**
- **No emojis**, in any file. The house style bans them and the checker
  fails the build.
- **Do not add a dependency without a reason written down next to it.**
- **Do not remove functionality that looks intentional.** Ask first.
- **The translation's voice is fixed.** `docs/style-guide.md` is the contract
  with the editor; a hand edit that breaks it will be corrected by the next
  run of the editor pass.
