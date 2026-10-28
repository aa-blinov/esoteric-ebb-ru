# Documentation

| Document | What it covers |
| --- | --- |
| [architecture.md](architecture.md) | How the translation is put together, and why each stage exists. |
| [style-guide.md](style-guide.md) | The voice the editor works from. The contract for any hand correction. |
| [glossary.md](glossary.md) | The frozen terms, and the rules that keep one term from having two words. |
| [layout.md](layout.md) | The panel widths the Russian is measured against, and the strings that failed them. |
| [release-process.md](release-process.md) | Versioning, release checks, tags and package publishing. |
| [../.agents/skills/game-localization-pipeline/SKILL.md](../.agents/skills/game-localization-pipeline/SKILL.md) | Reusable workflow for planning, translating, editing, and validating game localization. |
| [../.agents/skills/esoteric-ebb-ru-translation/SKILL.md](../.agents/skills/esoteric-ebb-ru-translation/SKILL.md) | Codex workflow for translating, editing, and checking Russian text in the game. |
| [screenshots/](screenshots/) | The game in Russian. |
| [../README.md](../README.md) | The front door: what it does and how to install it. |
| [../README_ru.md](../README_ru.md) | The same front door, in Russian. |

## Reading order

New here: [../README_ru.md](../README_ru.md), [../CONTRIBUTING_RU.md](../CONTRIBUTING_RU.md), then [architecture.md](architecture.md). Codex users can follow the [general localization pipeline](../.agents/skills/game-localization-pipeline/SKILL.md) and its [Esoteric Ebb profile](../.agents/skills/esoteric-ebb-ru-translation/SKILL.md).

Changing a line: [style-guide.md](style-guide.md) for the voice, then
[glossary.md](glossary.md) for the wording of the term you are touching.

Touching the layout: [layout.md](layout.md), then the measurements in
`src/ebru/measure_width.py`.

Working on the code: [architecture.md](architecture.md), then
[../AGENTS.md](../AGENTS.md) for the traps.
