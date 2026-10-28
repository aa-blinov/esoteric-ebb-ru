---
name: game-localization-pipeline
description: Plan, translate, edit, and validate a video game's localization as a coherent whole. Use when starting or continuing a game translation, building a glossary, translating large dialogue corpora, reconciling lore and terminology, or checking UI fit in the running game.
---

# Game localization pipeline

Use this reusable workflow to localize a game from source extraction through in-game validation. First inspect the project instructions, source format, existing translation, and game-specific skill. Treat the game profile as authoritative for commands and technical constraints; this skill supplies the sequence and quality gates. Never assume another game's file structure or behavior matches Esoteric Ebb.

## Working principles

- Translate from the original source with enough surrounding context to understand speaker, scene, mechanics, and narrative function.
- Do not invent lore to bridge a gap. Separate confirmed facts from interpretation, and ask for context or research primary sources when the distinction affects the translation.
- Keep a versioned glossary and style guide as working artifacts. A decision that exists only in chat will drift.
- Distinguish linguistic quality from technical validity and runtime display. Passing one does not prove the others.
- Preserve source keys, row order, variables, tags, formatting, and intentional blank behavior required by the game's loader.
- Record unresolved questions and validation limits. Do not call a release complete when key screens or checks remain unverified.

## Phase 0: map the project

Before translating, inspect repository guidance and identify:

1. The authoritative source language and source files, keys/IDs, encoding, line endings, and import/export route.
2. Translation target files and how the game selects a language.
3. Existing translations, terminology, voice rules, lore references, and prior review decisions.
4. Build, test, install, reload, screenshot, and packaging steps. Find out whether the game must restart to read changed text.
5. Runtime constraints: fonts and glyph coverage, text boxes, screen resolutions, markup, plural/gender rules, variables, and fallback behavior.
6. Which checks are automated, which require the game running, and which depend on a particular machine or paid model endpoint.

Write down the actual workflow and hazards in project documentation. Do not run a costly full translation pipeline just to inspect it. Do not change game settings, install files, or launch a model pipeline until the scope requires it.

## Phase 1: prepare context and terminology

1. Build an inventory of source strings with stable IDs and useful metadata: file, speaker, scene, neighboring lines, character limits, tags, variables, and translator notes.
2. Read the game's own narrative and mechanics sources. Review existing translations and canonical names before proposing equivalents.
3. Create a glossary before the bulk pass. Include source term, target term, part of speech or inflection policy, meaning in this game, context, rejected variants, and confidence/source.
4. Resolve high-impact terms first: character and place names, factions, classes, stats, recurring jokes, mechanics, and lore concepts. Keep a question list for ambiguous cases instead of silently guessing.
5. Write a short style guide: register, point of view, tense, dialogue punctuation, character voices, humor, profanity, capitalization, and what not to localize.
6. Add a small reviewed sample to test the glossary and style guide. Revise them before scaling if the sample sounds inconsistent.

## Phase 2: bulk translation

- Translate in context-preserving batches. Keep dialogue scenes and speaker identity together where possible; include a few neighboring lines when batch boundaries would hide a joke or referent.
- Supply the relevant glossary subset and style rules with each batch. Keep stable source IDs and require one output for every input.
- Keep source markup and placeholders intact. Validate output structure before accepting a batch.
- Cache model output by source, prompt, and glossary/style version where possible. Track skipped, failed, retried, and manually overridden rows.
- Do not treat machine output as final prose. Mark uncertainty and leave evidence for the editor.

## Phase 3: editorial passes

Make deliberate passes rather than asking one edit to solve every problem:

1. **Meaning and mechanics:** compare every changed line with the source. Correct omissions, false friends, broken instructions, wrong referents, and mismatched game rules.
2. **Literary voice:** remove calques and awkward syntax; preserve intent, pacing, speaker voice, emotional force, and humor. Keep a joke a joke, but do not invent a new joke to compensate for a lost pun.
3. **Narrative continuity and lore:** read related entries and scenes together. Reconcile names, chronology, factions, concepts, and character knowledge. Do not make the Russian text more certain than the source. Record unresolved source ambiguities.
4. **Terminology and repetition:** compare every term to the glossary and every repeated source string to its other translations. Canonicalize identical source lines when the game uses them as the same phrase; preserve differences when context changes meaning.
5. **Language and typography:** check grammar, agreement, declension, punctuation, quotes, spelling, unwanted source-language residue, and consistency of forms. Keep character voice exceptions intentional.
6. **Markup and data integrity:** compare tags, placeholders, row counts, IDs, CSV columns, encoding, and source alignment. Do not erase a line by leaving a cell empty unless the loader's fallback behavior has been confirmed.

Use human review for lore-sensitive, humorous, emotionally important, and mechanically consequential lines. Log durable corrections in the source of truth used by the pipeline, not only in generated output.

## Phase 4: automated QA

Choose checks that match the format and add regression coverage for recurring mistakes:

- source/target key coverage, duplicate IDs, row order, and unexpected blanks;
- tag, placeholder, escape, plural, gender, and format-string parity;
- glossary violations and inconsistent repeated strings;
- mixed scripts or accidental untranslated fragments;
- quotes, punctuation, encoding, forbidden control characters, and line endings;
- character limits and approximate width using the actual game font when available;
- build/import/export checks and the repository's style or content checks.

Inspect failures in context. A checker may flag a valid source-matching phrase or a deliberate exception; document the reason rather than weakening the checker wholesale. Keep automated checks repeatable in CI whenever they do not require the game itself.

## Phase 5: runtime and visual validation

1. Install the candidate into a known test copy or use the documented development loader. Confirm the target path before any installer that replaces files.
2. Reload the language the way this game requires. Confirm the running game is using the edited build, correct language, intended font, and intended settings.
3. Visit representative screens, then every screen affected by layout-sensitive edits. Include long strings, dialogue choices, names, loading hints, codex/lore panels, menus, and edge cases such as empty values or variables.
4. Check for clipping, wrapping, overlap, unreadable glyphs, bad line breaks, missing variables, tags rendered literally, fallback to source text, and text obscured by controls or artwork.
5. Capture evidence with resolution, font, language, build/revision, and screen context. If multiple game instances or stale screenshots are possible, verify the window/process and recapture.
6. Fix the cause at the narrowest layer: wording/line break first, per-string size/layout rule where supported, global font/settings only when justified. A global font-size change invalidates prior measurements and expands the visual regression scope.
7. Repeat the reload and visual check after each final edit. A width estimate is useful evidence but is not a visual pass.

## Phase 6: preserve and hand off

- Keep manual corrections in the pipeline's durable override source and update generated translation files through the documented process.
- Record terminology decisions in the glossary, voice decisions in the style guide, measured UI fixes in the layout record, and player-visible changes in the changelog.
- Report changed IDs/files, checks and commands run, runtime screens inspected, known exceptions, and remaining risks.
- Follow the repository's contribution and release rules. Do not commit, push, publish, overwrite a player's save, or send messages unless the user or project instructions authorize that action.

## Game-specific profile

For this repository, pair this workflow with [`esoteric-ebb-ru-translation`](../esoteric-ebb-ru-translation/SKILL.md). That profile names the actual CSV, glossary, manual-fix, measurement, installer, and test paths and records Esoteric Ebb-specific loader, font, settings, and capture behavior. Its project facts do not automatically apply to another game.
