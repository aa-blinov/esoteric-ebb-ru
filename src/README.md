# Source

The pipeline that produced `translation/Russian/`, and the two inputs it works
from: the style code and the frozen glossary.

| Path | What it is |
| --- | --- |
| `ebru/build.py` | The orchestrator. Runs the stages in order and writes the folder. |
| `ebru/llm_client.py` | The model endpoint, the disk cache, the JSON reply parser. |
| `ebru/extract_corpus.py` | The English CSVs into one JSON line per string. |
| `ebru/run_translation.py` | Terms, names and the bulk translation. |
| `ebru/literary_pass.py` | The editor: the corpus against the style code. |
| `ebru/unify_address.py` | Narration and rules to «ты». |
| `ebru/canonicalise.py` | One wording per repeated source line. |
| `ebru/typo_normalise.py` | The typographic rules, applied to every row. |
| `ebru/fix_layout.py` | The four lines with a display size that did not fit. |
| `ebru/compact_ui.py` | The character-screen labels that outgrew their boxes. |
| `ebru/fix_quotes.py`, `ebru/fix_quote_chain.py` | Quote structure, row by row and across a chain. |
| `ebru/fix_foreign.py` | English words left inside Russian sentences. |
| `ebru/qa_check.py`, `ebru/struct_qa.py` | The language and the structure checks. |
| `ebru/verify_final.py` | The final report: typography, markup, address, repeats, width. |
| `ebru/finalize.py` | The corpus into the twelve CSV files. |
| `voice/bible.md` | The style code the editor reads. |
| `voice/glossary.json` | The frozen terms, 1,838 of them. |

## Running it

```bash
python3 src/ebru/build.py --stage all --model minimax/MiniMax-M3
python3 src/ebru/build.py --stage all --install --game-dir "/path/to/Esoteric Ebb"
```

The endpoint comes from the environment:

| Variable | What it is | Default |
| --- | --- | --- |
| `EBRU_BASE_URL` | The endpoint the model is called at. | `http://127.0.0.1:8080/v1` |
| `EBRU_TOKEN` | The token for that endpoint. | read from the local runtime |
| `EBRU_CACHE_DIR` | Where the answers are cached. | `work/cache` |
| `EB_GAME_DIR` | The Esoteric Ebb installation. | the Steam path |

Every answer is cached under `work/cache/`, keyed by the prompt. A re-run of
a stage that has not changed costs nothing; a change to the prompt costs the
new calls and reuses the old ones.

## The stages

```
corpus ─▶ bulk ─▶ edit ─▶ address ─▶ canon ─▶ typography ─▶ layout
       ─▶ compact ─▶ quotes ─▶ qa ─▶ build
```

`edit` runs the editor twice. The second round reads the first round's text
as context, so the voice that the first round established carries forward.
