#!/usr/bin/env python
"""Structural QA: unbalanced guillemets, stray quotes, markup drift.

Every row is checked against the English original for:
  - the same inline markup and placeholders
  - balanced « » quoting
  - no leftover straight quotes
Damaged rows are sent to the model for a minimal repair.
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

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from llm_client import call_llm, extract_texts, specials  # noqa: E402

WORKERS = int(os.environ.get("EB_WORKERS", "10"))
_lock = threading.Lock()


def log(*a):
    with _lock:
        print(*a, flush=True)


SYSTEM = """Ты — корректор русского перевода игры Esoteric Ebb.

Тебе дан JSON-массив объектов {"id": N, "en": "английский оригинал", "ru": "испорченный перевод"}.

Почини строку:
1. Расставь «ёлочки» правильно: прямая речь в «ёлочках», вложенные реплики — внутри тех же кавычек или через „…“.
2. Убери посторонние или лишние кавычки.
3. Разметку перенеси символ в символ из английского оригинала: теги и плейсхолдеры должны
   совпадать по набору и порядку с оригиналом.
4. Смысл, объём и характер реплики не меняй. Ничего не добавляй и не убирай.
5. Выход — JSON-массив строк РОВНО той же длины: починенный перевод для каждой строки.
"""


def problems(en, ru):
    out = []
    if ru.count("«") != ru.count("»"):
        out.append("quotes")
    if '"' in ru:
        out.append("straight")
    if specials(ru) != specials(en):
        out.append("markup")
    return out


def repair(items):
    payload = [{"id": it["id"], "en": it["en"], "ru": it["ru"]} for it in items]
    user = json.dumps(payload, ensure_ascii=False, indent=1)
    try:
        txt = call_llm("MiniMax-M3", SYSTEM, user, max_tokens=8000, temperature=0.1,
                       cache_key="struct|%s|%s" % ("MiniMax-M3", user))
        arr = extract_texts(txt)
    except Exception as e:
        log("  repair batch failed: %s" % e)
        return []
    if not arr or len(arr) != len(items):
        return []
    res = []
    for it, cand in zip(items, arr):
        if not isinstance(cand, str) or not cand.strip():
            continue
        if specials(cand) != specials(it["en"]):
            continue
        if problems(it["en"], cand):
            continue
        res.append((it["id"], cand))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.path.join(ROOT, "work", "corpus", "corpus_ru_canon.jsonl"))
    ap.add_argument("--out", default=os.path.join(ROOT, "work", "corpus", "corpus_ru_struct.jsonl"))
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.src, encoding="utf-8")]
    bad = []
    for i, r in enumerate(rows):
        ru = r.get("ru") or ""
        if not ru:
            continue
        p = problems(r.get("en") or "", ru)
        if p:
            bad.append({"i": i, "id": len(bad), "en": r.get("en") or "", "ru": ru,
                        "p": ",".join(p)})
    log("rows with structural problems: %d / %d" % (len(bad), len(rows)))
    kinds = {}
    for b in bad:
        kinds[b["p"]] = kinds.get(b["p"], 0) + 1
    log("by kind: %s" % kinds)

    if bad:
        BATCH = 10
        batches = [bad[i:i + BATCH] for i in range(0, len(bad), BATCH)]
        fixed = {}
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            futs = [ex.submit(repair, b) for b in batches]
            done = 0
            for f in as_completed(futs):
                for pid, cand in f.result():
                    fixed[pid] = cand
                done += 1
                if done % 20 == 0:
                    log("  %d/%d batches, fixed=%d (%.0fs)"
                        % (done, len(batches), len(fixed), time.time() - t0))
        log("repaired: %d" % len(fixed))
        for b in bad:
            c = fixed.get(b["id"])
            if c:
                rows[b["i"]]["ru"] = c

    with open(args.out, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    log("wrote", args.out)

    left = sum(1 for r in rows if r.get("ru") and problems(r.get("en") or "", r["ru"]))
    log("remaining structural problems: %d" % left)


if __name__ == "__main__":
    main()
