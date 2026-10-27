# Contributing

Esoteric Ebb RU is a community-maintained Russian localization. Contributions
to wording, lore consistency, layout fixes, tests and documentation are welcome.

## Before editing

- Read the [style guide](docs/style-guide.md) and [glossary](docs/glossary.md)
  before changing Russian text.
- Check [layout measurements](docs/layout.md) before changing fixed-width UI.
- Find the English source row and its other occurrences. Identical English
  source strings should keep identical Russian translations.
- Open an issue first for a large rewrite, a terminology change affecting many
  files, or a change to the pipeline or release process.

## Translation changes

1. Edit the relevant file in `translation/Russian/`.
2. Add the correction to `src/voice/manual_fixes.json` so a pipeline run will
   preserve it.
3. Keep placeholders and markup identical to the English source. Preserve CSV
   columns and use the zero-width space only for a line that must stay blank.
4. Add or update a test when the fix addresses a recurring regression. Record
   a measured layout change in `docs/layout.md` and a player-visible change in
   `CHANGELOG.md`.
5. For a layout change, install the folder into a local game copy, restart the
   game or use Ctrl+R, and include a screenshot with the resolution and font
   settings.

## Checks

From the repository root:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/scan_ai_patterns.py --verbose
```

The `Check and test` and `House style` GitHub Actions workflows run on every
pull request. The house-style checker is maintained in the companion
`golden-repo`; when that repository is checked out beside this one, run:

```bash
python ../golden-repo/scripts/housecheck.py .
python ../golden-repo/scripts/anti_ai.py --dir .
```

For font measurements, set `EB_GAME_DIR` to a local game installation and run
`python src/ebru/measure_width.py`. To install the localization locally, close
the game first, set `EB_GAME_DIR`, and run `python scripts/install.py`.

## Pull requests

- Work on a focused branch; do not push directly to `main` for proposed
  changes.
- Describe the player-facing result, list the affected keys, and give enough
  source or lore context to review the Russian wording.
- Include screenshots for visible layout changes and the exact check results.
- Keep unrelated translation edits out of the same pull request.
- Wait for both required workflows to pass and respond to review comments
  before merging.

## Code changes

- CI uses Python 3.12 and `unittest`; follow the surrounding module and test
  conventions.
- Keep changes focused and deterministic. Do not change generated CSV output
  without updating the source fix or the pipeline that produces it.
- Keep workflow permissions minimal. Explain any new dependency or external
  action in the pull request.
- There is no automatic formatter or linter configured. Match the surrounding
  style and run the tests before opening a pull request.

Use [CONTRIBUTING_RU.md](CONTRIBUTING_RU.md) for the same instructions in
Russian. See [the release process](docs/release-process.md) for versioning and
publishing.
