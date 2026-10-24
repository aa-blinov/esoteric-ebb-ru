#!/usr/bin/env python
"""Compact the character-screen texts that grew beyond their English original.

The character sheet and the lore panel have fixed-size boxes. Russian needs
more characters than English for the same thought, so several blocks spill
over. This pass rewrites just those strings into a tighter Russian wording
without changing the meaning, the voice or the markup.
"""
from __future__ import annotations

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

WORKERS = int(os.environ.get("EB_WORKERS", "8"))
_lock = threading.Lock()

PREFIXES = ("PCBackground_", "AbilityScoreInfo_", "SheetInfo_")
THRESHOLD = 1.08
ALLOWANCE = 6          # characters more than the English, max

SYSTEM = """Ты — редактор русского перевода игры Esoteric Ebb.

Некоторые подписи и описания на экране создания персонажа не помещаются в рамку:
русский текст получился длиннее английского оригинала. Нужно переписать их компактнее.

ПРАВИЛА:
1. Вход — JSON-массив объектов {"id": N, "en": "английский оригинал", "ru": "текущий перевод", "limit": N}.
   Выход — JSON-массив строк РОВно той же длины и порядка: новая русская версия.
2. Новая версия должна быть НЕ ДЛИННЕ limit символов (limit = длина английского оригинала плюс
   небольшой запас). Сокращай формулировку, а не смысл.
3. Сохрани характер и голос: литературный, чуть сухой, разговорный там, где это реплика.
4. Разметку перенеси символ в символ: теги и плейсхолдеры те же, в том же порядке.
5. Ничего не выдумывай и не убивай: если сократить нельзя, верни исходный вариант.
"""


def log(*a):
    with _lock:
        print(*a, flush=True)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "work", "corpus", "corpus_ru_FIX3.jsonl")
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "work", "corpus", "corpus_ru_COMPACT.jsonl")

    rows = [json.loads(l) for l in open(src, encoding="utf-8")]
    targets = []
    for i, r in enumerate(rows):
        if not r["key"].startswith(PREFIXES):
            continue
        en = r.get("en") or ""
        ru = r.get("ru") or ""
        if not en or not ru:
            continue
        if len(ru) > len(en) * THRESHOLD:
            targets.append({"i": i, "id": len(targets), "en": en, "ru": ru,
                            "limit": len(en) + ALLOWANCE})
    log("strings to compact: %d" % len(targets))
    if not targets:
        shutil_copy(src, dst)
        return

    BATCH = 12
    batches = [targets[i:i + BATCH] for i in range(0, len(targets), BATCH)]
    fixed = {}
    t0 = time.time()

    def work(b):
        payload = [{"id": t["id"], "en": t["en"], "ru": t["ru"], "limit": t["limit"]} for t in b]
        user = json.dumps(payload, ensure_ascii=False, indent=1)
        try:
            txt = call_llm("MiniMax-M3", SYSTEM, user, max_tokens=8000, temperature=0.2,
                           cache_key="compact|%s|%s" % ("MiniMax-M3", user))
            arr = extract_texts(txt)
        except Exception as e:
            log("  batch failed: %s" % e)
            return []
        if not arr or len(arr) != len(b):
            return []
        out = []
        for t, cand in zip(b, arr):
            if not isinstance(cand, str) or not cand.strip():
                continue
            if specials(cand) != specials(t["ru"]):
                continue
            if len(cand) > t["limit"]:
                continue
            if len(cand) >= len(t["ru"]):
                continue
            out.append((t["id"], cand))
        return out

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(work, b) for b in batches]
        done = 0
        for f in as_completed(futs):
            for pid, cand in f.result():
                fixed[pid] = cand
            done += 1
            if done % 5 == 0:
                log("  %d/%d batches, compacted=%d (%.0fs)"
                    % (done, len(batches), len(fixed), time.time() - t0))

    applied = 0
    for t in targets:
        c = fixed.get(t["id"])
        if c:
            rows[t["i"]]["ru"] = c
            applied += 1
    log("compacted: %d" % applied)

    with open(dst, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    log("wrote", dst)


def shutil_copy(a, b):
    import shutil
    shutil.copyfile(a, b)
    log("nothing to do, copied")


if __name__ == "__main__":
    main()
