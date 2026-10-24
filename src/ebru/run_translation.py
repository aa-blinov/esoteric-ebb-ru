#!/usr/bin/env python
"""Mass translation driver for the Esoteric Ebb Russian localization.

Stages
  1. terms   - canonical game terms from Glossary.csv (spells, feats, items, places)
  2. names   - proper nouns, consistent transliteration
  3. bulk    - everything else, with the glossary injected per batch
  4. repair  - single-item retries for markup/placeholder mismatches

Results land in corpus/corpus_ru.jsonl. Fully resumable: every LLM call is disk-cached.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llm_client import call_llm, extract_json_array, specials  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CORPUS = os.path.join(ROOT, "work", "corpus", "corpus.jsonl")
OUT_RU = os.path.join(ROOT, "work", "corpus", "corpus_ru.jsonl")
GLOSSARY_JSON = os.path.join(ROOT, "work", "corpus", "glossary.json")

MAX_CHARS = int(os.environ.get("EB_MAX_CHARS", "3200"))
MAX_ITEMS = int(os.environ.get("EB_MAX_ITEMS", "35"))
WORKERS = int(os.environ.get("EB_WORKERS", "6"))

_print_lock = threading.Lock()


def log(*a):
    with _print_lock:
        print(*a, flush=True)


BASE_SYSTEM = """Ты — литературный переводчик игры Esoteric Ebb (изометрическая CRPG по мотивам настольной ролевой игры D&D, сеттинг «пост-арканепанк»: магия, религия, политические интриги, бюрократия).

Переводи английский текст на русский.

ЖЁСТКИЕ ПРАВИЛА:
1. Вход — JSON-массив строк. Выход — JSON-массив строк РОВНО той же длины, в том же порядке. Больше ничего: ни нумерации, ни комментариев, ни markdown-обёрток.
2. Разметку переноси СИМВОЛ В СИМВОЛ, в том же порядке и количестве:
   <i> </i> <b> </b> <u> </u> <s> </s> <shake> </shake> <wiggle> </wiggle> <size=NN> <color=#RRGGBB> и плейсхолдеры {0} {1} {CLERIC} {ROGUE} {WIZARD}.
   Если разметки нет в оригинале — не добавляй её.
3. Ничего не выдумывай: не добавляй пояснений, имён, фактов и оценочных слов, которых нет в оригинале.
4. Тон:
   - диалоги — живая разговорная речь, как у актёров; держи характер и манеру говорящего;
   - описания — плотный, образный, но ясный литературный текст;
   - лор/справки — точный, чуть архаичный, с характером;
   - интерфейс — коротко и по-делу, без пафоса.
5. Имена собственные, названия мест, божеств, орденов и заклинаний переводи по глоссарию, если он дан; иначе — транслитерацией. Сношениями не пользоваться.
6. Единообразие терминов важнее красивости: один и тот же термин — одно и то же слово во всём тексте.
7. Кавычки-ёлочки и тире — как в русской типографике, но внутри JSON-строк экранирование стандартное.
8. Длина: не сокращай смысл, но и не раздувай; объём реплики примерно как в оригинале.
9. НИКАКИХ английских слов в переводе не оставляй — переведи каждое слово. Допустимы только: имена собственные из глоссария, аббревиатуры вроде HWBT/IT и названия игровых команд вроде DM-Wants-To-Kill-Me.
10. Обращение на «ты»/«вы» выбирай по ситуации и не меняй его внутри одной реплики.
"""


def load_rows():
    rows = [json.loads(l) for l in open(CORPUS, encoding="utf-8")]
    for i, r in enumerate(rows):
        r["idx"] = i
    return rows


def make_batches(rows, max_chars=MAX_CHARS, max_items=MAX_ITEMS):
    """Contiguous batches inside each file so narrative context stays intact."""
    batches = []
    cur = []
    cur_chars = 0
    cur_file = None
    for r in rows:
        if cur and (r["file"] != cur_file
                    or len(cur) >= max_items
                    or cur_chars + len(r["en"]) > max_chars):
            batches.append(cur)
            cur = []
            cur_chars = 0
        cur.append(r)
        cur_chars += len(r["en"])
        cur_file = r["file"]
    if cur:
        batches.append(cur)
    return batches


def glossary_for(texts, glossary):
    """Glossary entries actually referenced by this batch."""
    blob = " ".join(texts).lower()
    hits = []
    for en, ru in glossary.items():
        if len(en) < 3:
            continue
        if en.lower() in blob:
            hits.append((en, ru))
    hits.sort(key=lambda x: len(x[0]), reverse=True)
    return hits[:60]


def fmt_glossary(hits):
    if not hits:
        return ""
    lines = "\n".join("- %s → %s" % (en, ru) for en, ru in hits)
    return "\n\nГЛОССАРИЙ (используй эти переводы, не выдумывай свои):\n" + lines


def translate_batch(batch, model, glossary, temperature=0.3, repair=False):
    srcs = [r["en"] for r in batch]
    user = json.dumps(srcs, ensure_ascii=False, indent=1)
    system = BASE_SYSTEM
    if not repair and glossary:
        system += fmt_glossary(glossary_for(srcs, glossary))
    if repair:
        system += ("\n\nВНИМАНИЕ: предыдущий ответ нарушил разметку. Верни массив той же длины, "
                   "где каждая строка содержит РОВНО те же теги и плейсхолдеры, что и исходная, "
                   "в том же порядке и количестве.")
    ck = "batch|%s|%s|%s" % (model, "repair" if repair else "main", user)
    out = call_llm(model, system, user, max_tokens=12000, temperature=temperature, cache_key=ck)
    arr = extract_json_array(out)
    if arr is None or len(arr) != len(srcs):
        return None
    return [x if isinstance(x, str) else str(x) for x in arr]


def check_item(src, dst):
    if dst is None:
        return "empty"
    if not dst.strip():
        return "empty"
    if specials(src) != specials(dst):
        return "markup"
    return "ok"


def stage_terms(rows, model, glossary_out):
    """Translate canonical glossary terms first (they anchor everything else)."""
    terms = [r for r in rows if r["file"] == "Glossary" and r["key"].startswith("Glossary_Term_")
             and len(r["en"]) <= 60]
    log("terms to translate:", len(terms))
    done = {}
    batches = make_batches(terms, max_chars=2200, max_items=25)
    out_lock = threading.Lock()

    def work(b):
        res = translate_batch(b, model, {})
        return b, res

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(work, b) for b in batches]
        n = 0
        for f in as_completed(futs):
            b, res = f.result()
            n += 1
            if res:
                for r, t in zip(b, res):
                    if check_item(r["en"], t) == "ok":
                        done[r["en"]] = t
            if n % 25 == 0:
                log("  terms batch %d/%d, translated=%d" % (n, len(batches), len(done)))
    json.dump(done, open(glossary_out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    log("terms done:", len(done), "->", glossary_out)
    return done


def stage_names(rows, model, glossary, names_out):
    """Transliterate proper nouns consistently."""
    cands = json.load(open(os.path.join(ROOT, "work", "corpus", "proper_nouns.json"), encoding="utf-8"))
    picked = [c["term"] for c in cands if c["count"] >= 3]
    log("name candidates:", len(picked))
    # cluster related forms (Freestrider/Freestriders) next to each other
    picked.sort(key=lambda t: (t.lower()[:4], t))
    picked = [p for p in picked if p.lower() not in {k.lower() for k in glossary}]
    rows_n = [{"file": "Names", "key": "N_%d" % i, "speaker": "", "en": p, "ru": None}
              for i, p in enumerate(picked)]
    batches = make_batches(rows_n, max_chars=2200, max_items=60)
    done = {}

    def work(b):
        return b, translate_batch(b, model, {})

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(work, b) for b in batches]
        n = 0
        for f in as_completed(futs):
            b, res = f.result()
            n += 1
            if res:
                for r, t in zip(b, res):
                    if check_item(r["en"], t) == "ok":
                        done[r["en"]] = t
            if n % 10 == 0:
                log("  names batch %d/%d translated=%d" % (n, len(batches), len(done)))
    json.dump(done, open(names_out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    log("names done:", len(done))
    return done


POLISH_SYSTEM = """Ты — редактор-стилист русского перевода игры Esoteric Ebb.

Тебе дан список терминов игры: английский термин и его текущий русский перевод.

Задача: вернуть УЛУЧШЕННЫЙ русский вариант каждого термина.

Требования:
1. Вход — JSON-массив пар [{"en": "...", "ru": "..."}]. Выход — JSON-массив строк РОВНО той же длины и порядка: только новые русские варианты.
2. Никаких пояснений, только JSON-массив.
3. Правь грамматику (согласование рода/числа/падежа), порядок слов и естественность; убирай канцеляризмы и кальки, если есть более русская формулировка.
4. Держи единообразие: однокоренные формы (Freestrider / Freestriders) — одна основа и правильная форма числа; Azgal / Azgalist / Azgalists — согласованно между собой.
5. Имена собственные — транслитерация или устоявшийся эквивалент; не переводи смысл имени.
6. Если текущий вариант уже хорош — верни его без изменений.
7. Термин должен оставаться КОРОТКИМ (обычно 1-2 слова) — это подписи в интерфейсе и справочник.
"""


def stage_polish(glossary, model, out_path):
    """Polish glossary wording; keeps the original on failure."""
    items = sorted(glossary.items())
    rows = [{"file": "Polish", "key": "P_%d" % i, "speaker": "", "en": en, "ru": ru}
            for i, (en, ru) in enumerate(items)]
    batches = make_batches(rows, max_chars=2400, max_items=25)
    out = {}
    for b in batches:
        srcs = [r["en"] for r in b]
        pairs = [{"en": r["en"], "ru": r["ru"]} for r in b]
        user = json.dumps(pairs, ensure_ascii=False, indent=1)
        try:
            txt = call_llm(model, POLISH_SYSTEM, user, max_tokens=8000, temperature=0.25,
                           cache_key="polish|%s|%s" % (model, user))
            arr = extract_json_array(txt)
        except Exception as e:
            log("  polish batch failed: %s" % e)
            arr = None
        if arr and len(arr) == len(srcs):
            for r, t in zip(b, arr):
                if isinstance(t, str) and t.strip() and check_item(r["en"], t) == "ok":
                    out[r["en"]] = t
                else:
                    out[r["en"]] = r["ru"]
        else:
            for r in b:
                out[r["en"]] = r["ru"]
    json.dump(out, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    changed = sum(1 for k in out if out[k] != glossary.get(k))
    log("polish: %d entries, %d changed" % (len(out), changed))
    return out


def stage_bulk(rows, model, glossary):
    batches = make_batches(rows, max_chars=MAX_CHARS, max_items=MAX_ITEMS)
    if os.environ.get("EB_REVERSE") == "1":
        batches = batches[::-1]
        log("REVERSE mode")
    log("bulk batches:", len(batches))
    results = {}
    problems = []
    done_ct = [0]
    t0 = time.time()

    def work(b):
        return b, translate_batch(b, model, glossary)

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(work, b) for b in batches]
        for i, f in enumerate(as_completed(futs), 1):
            b, res = f.result()
            if res is None:
                log("  !! batch failed, will redo small: %s" % [r["key"] for r in b][:3])
                for r in b:
                    problems.append(r["idx"])
                continue
            for r, t in zip(b, res):
                st = check_item(r["en"], t)
                if st == "ok":
                    results[r["idx"]] = t
                else:
                    problems.append(r["idx"])
            done_ct[0] += len(b)
            if i % 20 == 0:
                rate = done_ct[0] / max(1e-6, time.time() - t0)
                log("  %d/%d batches  items=%d  %.1f items/s  eta=%d min"
                    % (i, len(batches), done_ct[0], rate,
                       int((len(rows) - done_ct[0]) / max(rate, 1e-6) / 60)))
    return results, problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="minimax/MiniMax-M3")
    ap.add_argument("--stage", default="all", choices=["all", "terms", "bulk"])
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    model = args.model.split("/")[-1]

    rows = load_rows()
    if args.limit:
        rows = rows[:args.limit]
    log("rows:", len(rows))

    glossary = {}
    if os.path.exists(GLOSSARY_JSON):
        glossary = json.load(open(GLOSSARY_JSON, encoding="utf-8"))
        log("existing glossary entries:", len(glossary))

    if args.stage in ("all", "terms"):
        glossary.update(stage_terms(rows, model, GLOSSARY_JSON))
    log("glossary size:", len(glossary))

    if args.stage == "all":
        names_json = os.path.join(ROOT, "work", "corpus", "names.json")
        names = {}
        if os.path.exists(names_json):
            names = json.load(open(names_json, encoding="utf-8"))
            log("names loaded from cache:", len(names))
        else:
            names = stage_names(rows, model, glossary, names_json)
        glossary.update({k: v for k, v in names.items() if k not in glossary})
        json.dump(glossary, open(GLOSSARY_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        log("glossary with names:", len(glossary))

        polished_json = os.path.join(ROOT, "work", "corpus", "glossary_polished.json")
        if os.path.exists(polished_json):
            glossary = json.load(open(polished_json, encoding="utf-8"))
            log("polished glossary loaded:", len(glossary))
        else:
            glossary = stage_polish(glossary, model, polished_json)
        json.dump(glossary, open(GLOSSARY_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        log("final glossary:", len(glossary))

    results, problems = stage_bulk(rows, model, glossary)
    log("bulk translated:", len(results), "problems:", len(problems))

    # repair pass: retry failing items one by one
    if problems:
        log("repair pass over", len(problems), "items")
        fixed = 0
        for idx in problems:
            r = rows[idx]
            res = translate_batch([r], model, glossary, repair=True)
            if res and check_item(r["en"], res[0]) == "ok":
                results[idx] = res[0]
                fixed += 1
        log("repair fixed:", fixed, "still bad:", len(problems) - fixed)

    with open(os.environ.get("EB_OUT", OUT_RU), "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps({"idx": r["idx"], "file": r["file"], "key": r["key"],
                                 "en": r["en"], "ru": results.get(r["idx"])},
                                ensure_ascii=False) + "\n")
    log("wrote", OUT_RU)


if __name__ == "__main__":
    main()
