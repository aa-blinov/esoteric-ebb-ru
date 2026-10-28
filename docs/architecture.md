# Architecture

How the Russian translation is put together.

## The shape

The game is Unity 6 with IL2CPP. It reads its text from CSV files in
`Esoteric Ebb_Data/StreamingAssets/Localization/<Folder>/`, one folder per
language, one column per file. The English files live in `Official/`, the
developer keeps an empty `Template/` with the same keys, and the community
Chinese translation sits in `ChineseCommunity/`. The Russian folder follows
the same shape, with the column code `RU`.

The repository is therefore two things: the folder the game reads, and the
script that produced it.

| Module | What it is responsible for |
| --- | --- |
| `src/ebru/extract_corpus.py` | Parses the English CSVs into one JSON line per string. |
| `src/ebru/llm_client.py` | The model endpoint, the disk cache, the JSON reply parser. |
| `src/ebru/run_translation.py` | The three translation stages: terms, names, bulk. |
| `src/ebru/literary_pass.py` | The editor: rewrites the corpus against the style code. |
| `src/ebru/canonicalise.py` | Collapses repeated source lines onto one wording each. |
| `src/ebru/unify_address.py` | Brings the address in narration and rules to «ты». |
| `src/ebru/typo_normalise.py` | The typographic rules, applied to every row. |
| `src/ebru/compact_ui.py` | Shortens the character-screen labels that outgrew their boxes. |
| `src/ebru/fix_layout.py` | The four lines with a display size that did not fit. |
| `src/ebru/qa_check.py` | The language checks: mixed scripts, English left inside Russian. |
| `src/ebru/struct_qa.py` | The structural checks: quotes, markup, placeholders. |
| `src/ebru/verify_final.py` | The final report: typography, markup, address, repeats. |
| `src/ebru/build.py` | Runs the stages in order and writes `translation/Russian/`. |
| `src/voice/bible.md` | The style code the editor reads. |
| `src/voice/glossary.json` | The frozen terms, 1,838 of them. |

## The data flow

```
English CSVs
     │
     ▼
 corpus.jsonl          one line per string: file, key, speaker, en
     │
     ├──▶ terms ──▶ names ──▶ glossary.json
     │                        │
     ▼                        ▼
 bulk translation  ◀──────────┘   the batch carries the terms it needs
     │
     ▼
 literary pass      two rounds; the second reads the first round's text as context
     │
     ▼
 address unification  narration and rules to «ты»
     │
     ▼
 canonicalisation   one wording per source line
     │
     ▼
 typography + layout + compaction
     │
     ▼
 QA (language, structure, width)
     │
     ▼
 translation/Russian/*.csv
```

## Decisions worth knowing about

### The glossary is frozen before the body text is written

Terms and proper nouns are translated first, in small batches, and are not
touched again. Every later stage receives the glossary and is bound to it.

The cost is a stage at the front of the pipeline, and about two thousand model
calls that would otherwise have been made inside the bulk pass with a worse
result: a term decided in batch 40 and used in batch 2,000 is two words for one
thing.

### The bulk pass keeps neighbours together

Batches are cut inside a file, not across it, so the lines of one dialogue go
to the model together. The model sees who is speaking and what was said a
moment ago, and the voice of a character survives the translation.

The cost is that a batch has a variable number of items, and the prompt has to
be rebuilt for each.

### The second editorial round reads the first round's text

The editor runs twice. In the second round the preceding lines of the file are
part of the prompt, so the voice that was established in the first round
propagates forward instead of each batch deciding on its own.

The cost is one more pass over the corpus, and a dependency on the order of the
lines.

### Width is measured against the real font

The character-screen lore panel is 541 px wide with about 500 px of text
inside it. Whether a line fits depends on the glyphs, so
`src/ebru/measure_width.py` reads the advance widths out of the fonts the game
ships and computes the rendered width the way TextMeshPro does.

The cost is a dependency on the game's assets, and the measurements in
`docs/layout.md` go stale when the game updates its fonts.

### The dialogue size is a setting, not a decision in the text

The game has a "Dialog Text Size" preference, 24 by default. Russian needs
20 to occupy the space English occupies at 24. That is a preference in
`SETTINGS.es3`, not a tag in the text, and it affects English as well.

The cost: a Russian player sees smaller text than the developer intended, and
the setting has to be set once per installation.

## Boundaries

- **`src/ebru/llm_client.py` knows nothing about the game.** It calls an endpoint
  and caches the answers. Everything game-specific lives in the stages above
  it.
- **The stages do not import each other.** They read a file and write a file.
  A stage can be re-run on its own, and the intermediate files under `work/`
  are the record of what each one did.
- **`src/ebru/verify_final.py` and `src/ebru/measure_width.py` may read the game's
  assets; nothing else may.** The game is installed on one machine and not on
  another, and the pipeline has to run on both.
- **`tests/` never imports from `src/`.** The tests read the shipped CSV files
  as a user would, and check what the game would see.
