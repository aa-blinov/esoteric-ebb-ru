#!/usr/bin/env python
"""Canonicalisation: one source line -> one Russian rendering, everywhere.

Repeated lines that were translated differently in different places are the
classic symptom of a translation that does not read as one voice. This pass
picks a single canonical Russian wording for each repeated source line and
applies it to every occurrence.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from llm_client import call_llm, extract_texts, specials  # noqa: E402
from qa_check import analyse  # noqa: E402

VOICE = open(os.path.join(ROOT, "src", "voice", "bible.md"), encoding="utf-8").read()
WORKERS = int(os.environ.get("EB_WORKERS", "10"))
_lock = threading.Lock()


def log(*a):
    with _lock:
        print(*a, flush=True)


SYSTEM = VOICE + """

ЗАДАЧА: для каждой английской реплики, которая в игре встречается несколько раз, выбрать ОДИН
канонический русский вариант — тот, что звучит лучше всего и подходит в большинстве случаев.

Правила:
- Вход — JSON-массив объектов {"en": "английская реплика", "variants": [{"ru": "вариант", "n": 5}, ...]}.
- Выход — JSON-массив строк РОВНО той же длины: канонический русский перевод для каждой реплики.
- Варианты, встречающиеся чаще, обычно лучше — но выбирай самый удачный по голосу.
- Для коротких междометий выбери нейтральный вариант, который уместен в большинстве случаев.
- Не меняй смысл реплики и не добавляй ничего нового.
- Разметку сохрани ровно как в английском оригинале: теги и плейсхолдеры те же, в том же порядке.
- Типографика: «ёлочки», многоточие «…», тире «—», точка перед закрывающей кавычкой.
"""


def canonicalise(groups):
    """groups: list of (en, [(ru, count), ...])"""
    items = []
    for en, variants in groups:
        items.append({"en": en, "variants": [{"ru": ru, "n": n} for ru, n in variants]})
    payload = json.dumps(items, ensure_ascii=False, indent=1)
    try:
        txt = call_llm("MiniMax-M3", SYSTEM, payload, max_tokens=8000, temperature=0.2,
                       cache_key="canon|%s|%s" % ("MiniMax-M3", payload))
        arr = extract_texts(txt)
    except Exception as e:
        log("  canon batch failed: %s" % e)
        return []
    if not arr or len(arr) != len(items):
        return []
    out = []
    for it, cand in zip(items, arr):
        if not isinstance(cand, str) or not cand.strip():
            continue
        if specials(cand) != specials(it["en"]):
            continue
        if analyse(it["en"], cand):
            continue
        out.append((it["en"], cand))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.path.join(ROOT, "work", "corpus", "corpus_ru_lit2.jsonl"))
    ap.add_argument("--out", default=os.path.join(ROOT, "work", "corpus", "corpus_ru_canon.jsonl"))
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.src, encoding="utf-8")]
    variants = collections.defaultdict(collections.Counter)
    for r in rows:
        en = (r.get("en") or "").strip()
        ru = (r.get("ru") or "").strip()
        if not en or not ru:
            continue
        variants[en][ru] += 1

    groups = []
    for en, ctr in variants.items():
        if len(ctr) > 1:
            groups.append((en, ctr.most_common()))
    log("inconsistent groups: %d" % len(groups))

    BATCH = 10
    batches = [groups[i:i + BATCH] for i in range(0, len(groups), BATCH)]
    canon = {}
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(canonicalise, b) for b in batches]
        done = 0
        for f in as_completed(futs):
            for en, ru in f.result():
                canon[en] = ru
            done += 1
            if done % 20 == 0:
                el = time.time() - t0
                log("  %d/%d batches, canonical=%d (%.0fs)" % (done, len(batches), len(canon), el))

    log("canonical decisions: %d" % len(canon))

    applied = 0
    for r in rows:
        en = (r.get("en") or "").strip()
        c = canon.get(en)
        if c and r.get("ru") != c:
            r["ru"] = c
            applied += 1
    log("rows rewritten to canonical: %d" % applied)

    with open(args.out, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    log("wrote", args.out)


if __name__ == "__main__":
    main()
