---
name: esoteric-ebb-ru-translation
description: Translate, revise, proofread, or QA Russian Esoteric Ebb text against its English source, lore, glossary, literary voice, and in-game layout. Use for dialogue, codex, item, UI, terminology, and overflow work in this repository.
---

# Russian localization for Esoteric Ebb

Use this profile for Russian localization of Esoteric Ebb. For the reusable translation method from glossary through editorial passes and runtime validation, also follow [the game localization pipeline](../game-localization-pipeline/SKILL.md). This profile supplies this game's facts and commands; it does not authorize unrelated changes, model calls, installation, commits, or releases.

The Russian custom language requires the game's **Localization Branch** beta, where the developer introduced the new text system and custom-language support. The beta is described as buggy; do not attribute unrelated game bugs to the translation or promise a bug-free build.

## Before changing text

1. Read the repository `AGENTS.md` and the relevant sections of `CONTRIBUTING_RU.md`.
2. Read `docs/style-guide.md` and `docs/glossary.md`. For layout-sensitive text, read `docs/layout.md` and use the real source row and neighboring dialogue for context.
3. Locate the exact English source key and check repeated occurrences. Do not infer lore or fill gaps with invented world details. When the game's own text and glossary do not settle a lore question, distinguish evidence from inference and use reliable primary sources only when needed or requested.
4. Follow the requested scope. For a review, report findings before editing unless the user asked for fixes. Do not rewrite unrelated strings.

## Translation and review

- Keep Esoteric Ebb's restrained literary voice, second-person narration, character-specific speech, and humor. Preserve an original joke without adding a new one.
- Keep established names and game terms from the glossary. One repeated English source string must have one consistent Russian rendering across files.
- Preserve placeholders and markup exactly, including order and spelling: `{0}`, `{CLERIC}`, `<i>`, `<b>`, `<size=N>`, colors, and other tags.
- Do not leave a cell empty to hide a line: the game falls back to English. Use `U+200B` only when the line must deliberately remain blank.
- First confirm that a string belongs to `translation/Russian/`. Some UI text is built from the game's own runtime strings and cannot be fixed by editing a localization CSV.
- Persist every hand correction in both the appropriate `translation/Russian/*.csv` file and `src/voice/manual_fixes.json`, then apply the manual fixes. Update tests for recurring regressions, `docs/layout.md` for measured layout changes, and `CHANGELOG.md` for player-visible changes.

## Layout and live-game checks

- Measure with the game's font assets and the correct panel width. Character count alone does not establish fit.
- Prefer a concise, natural label over changing global font size for one string. Any global `FontSize` change invalidates existing measurements and requires a wider visual review.
- A live check must use the changed CSV after the game reloads it. State clearly which screen and settings you checked; do not claim a visual pass from a stale capture or a different game instance.
- Do not close an active game session to force a restart unless it is safe to do so. The game can hold unsaved progress and rewrites settings on exit.

## Verification and reporting

Run the relevant unit tests and project checks after edits. For UI changes, install and inspect the localization only when the user's request calls for in-game verification and the target game directory is known. Check the GitHub `Check and test` and `House style` results for pull requests.

Report the keys and files changed, the checks run, and any live-game limitation separately. Never say that a translation is fully verified when only source text or a width estimate was checked.

For repository-specific commands, installation hazards, screenshots, and settings, read [the project workflow reference](references/project-workflow.md). Follow the glossary, style guide, and layout record as the maintained source of truth instead of copying their contents here.
