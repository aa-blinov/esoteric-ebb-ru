#!/usr/bin/env python
"""QA pass over the translated corpus.

Flags and repairs two defect classes:
  1. mixed-script words  - "Кcantрипы": Latin letters glued to Cyrillic
  2. untranslated words  - "В Whenever кто-то": English word left in Russian

Both are real defects the model produces occasionally; both break immersion or
render as stray glyphs in the game.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llm_client import call_llm, extract_json_array, specials  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CORPUS_RU = os.path.join(ROOT, "work", "corpus", "corpus_ru.jsonl")

CYR = re.compile(r"[Ѐ-ӿ]")
LAT = re.compile(r"[A-Za-z]")
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)

# tokens that legitimately stay Latin
ALLOW = {
    "hwbt", "it", "dm", "wants", "to", "kill", "me", "pc", "np", "ui", "hp", "mp",
    "dnd", "tv", "id", "dlc", "sdk", "api", "www", "http", "https", "com", "org",
    "steam", "twitch", "youtube", "discord", "reddit", "esotericebb", "eb",
    "russian", "english", "uk", "us", "eu", "pdr",
}


def mixed_script_word(tok: str) -> bool:
    return bool(CYR.search(tok) and LAT.search(tok))


def latin_words(text: str):
    return [w for w in WORD.findall(text or "") if LAT.match(w[0])]


def analyse(en: str, ru: str):
    """Return list of defect reasons."""
    reasons = []
    if not ru:
        return ["empty"]
    for w in WORD.findall(ru):
        if mixed_script_word(w):
            reasons.append("mixed:" + w)
    en_lat = {w.lower() for w in latin_words(en)}
    for w in latin_words(ru):
        lw = w.lower()
        if lw in ALLOW:
            continue
        if lw in en_lat:
            continue
        reasons.append("untranslated:" + w)
    return reasons


REPAIR_SYSTEM = """Ты — редактор русского перевода игры Esoteric Ebb.

Дан JSON-массив объектов: {"en": "английский оригинал", "ru": "текущий русский перевод", "problem": "описание дефекта"}.

Исправь перевод:
1. В русском тексте не должно остаться английских слов. Если слово срослось с русским («vastных», «Тыreally», «fascинирующая») — переведи это место полностью заново: «vastных» → «огромных», «Тыreally» → «Ты реально», «fascинирующая» → «захватывающая».
2. Никаких латинских букв внутри русских слов. Латиницей допустимы только имена собственные из глоссария и аббревиатуры (HWBT, IT).
3. Сохрани смысл, объём и характер реплики; не добавляй и не убирай ничего.
4. Разметку переноси символ в символ: <i> <b> <u> <s> <shake> <wiggle> <size=NN> <color=#RRGGBB> и плейсхолдеры {0} {CLERIC}.
5. Выход — JSON-массив строк РОВНО той же длины и порядка: только исправленные русские переводы. Без комментариев.
"""


def repair_one(item, model, attempt=1):
    payload = [{"en": item["en"], "ru": item["ru"], "problem": item["problem"]}]
    user = json.dumps(payload, ensure_ascii=False)
    try:
        txt = call_llm(model, REPAIR_SYSTEM, user, max_tokens=2000, temperature=0.2 + 0.1 * (attempt - 1),
                       cache_key="qa|%s|%d|%s" % (model, attempt, user))
        arr = extract_json_array(txt)
    except Exception:
        return None
    if arr and len(arr) == 1 and isinstance(arr[0], str) and arr[0].strip():
        cand = arr[0]
        if specials(cand) == specials(item["en"]) and not analyse(item["en"], cand):
            return cand
    return None


def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "MiniMax-M3"
    src = sys.argv[2] if len(sys.argv) > 2 else CORPUS_RU
    dst = sys.argv[3] if len(sys.argv) > 3 else CORPUS_RU
    rows = [json.loads(l) for l in open(src, encoding="utf-8")]
    bad = []
    for i, r in enumerate(rows):
        reasons = analyse(r["en"], r["ru"] or "")
        if reasons:
            bad.append({"i": i, "en": r["en"], "ru": r["ru"],
                        "problem": ", ".join(reasons[:3])})
    print("total rows:", len(rows))
    print("flagged:", len(bad))
    kinds = {}
    for b in bad:
        k = b["problem"].split(":")[0]
        kinds[k] = kinds.get(k, 0) + 1
    print("by kind:", kinds)

    sample = "\n\n".join("%-55s | %s" % (b["en"][:55], b["problem"]) for b in bad[:40])
    open(os.path.join(ROOT, "qa_sample.txt"), "w", encoding="utf-8").write(sample)

    if not bad:
        with open(dst, "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("no defects; corpus written unchanged ->", dst)
        return
    fixed = 0
    t0 = time.time()
    attempt = int(os.environ.get("EB_QA_ATTEMPT", "1"))
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(repair_one, b, model, attempt): b for b in bad}
        for i, f in enumerate(as_completed(futs), 1):
            res = f.result()
            if res:
                fixed += 1
                futs[f]["ru"] = res
            if i % 25 == 0:
                print("  repaired %d/%d (%.0fs)" % (i, len(bad), time.time() - t0), flush=True)
    print("repaired:", fixed, "of", len(bad))

    # rewrite corpus with fixes (index-based, exact)
    for b in bad:
        rows[b["i"]]["ru"] = b["ru"]
    with open(dst, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("corpus updated")


if __name__ == "__main__":
    main()
