#!/usr/bin/env python
"""Unify the address in non-dialogue text: the game speaks to the player as 'ты'.

Narration, rules, UI and codex entries all address the player. The game already
addresses the protagonist as 'ты' everywhere in speech, so the impersonal
'вы' in descriptive text was the last inconsistency in the voice.

Character dialogue is never touched: a formal 'вы' there is the speaker's
character, not the narrator.
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

BASE = os.path.join(ROOT, "work", "corpus", "corpus.jsonl")
VY = re.compile(r"\b(вы|вам|вас|ваш|ваша|ваше|ваши|вами|ваших|вашего|вашей)\b", re.I)
WORKERS = int(os.environ.get("EB_WORKERS", "8"))
_lock = threading.Lock()


def log(*a):
    with _lock:
        print(*a, flush=True)


SYSTEM = """Ты приводишь русский перевод игры Esoteric Ebb к единому обращению.

Игра — погружение от второго лица: и повествование, и правила, и интерфейс обращаются к игроку
на «ты». Твоя задача: в перечисленных строках заменить обращение «вы» (вы, вам, вас, ваш, ваша,
ваше, ваши и производные) на «ты» (ты, тебе, тебя, твой, твоя, твоё, твои и производные) —
с правильным согласованием по падежу, числу и роду.

ЖЁСТКИЕ ПРАВИЛА:
1. Ничего, кроме формы обращения, не меняй. Слова, порядок, объём, характер — как есть.
2. Согласуй падеж: «к вам» → «к тебе», «вам» → «тебе», «ваш» → «твой», «ваша» → «твоя»,
   «ваше» → «твоё», «ваши» → «твои», «вы» → «ты», «вас» → «тебя».
3. Форма единственного числа: «вы» во множественном числе меняй на «вы» только если речь
   о группе людей; обращение к игроку всегда «ты».
4. Разметку сохрани символ в символ: теги и плейсхолдеры те же, в том же порядке.
5. Вход — JSON-массив объектов {"id": N, "ru": "строка"}. Выход — JSON-массив строк РОВНО той же
   длины: исправленные строки.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.path.join(ROOT, "work", "corpus", "corpus_ru_lit2.jsonl"))
    ap.add_argument("--out", default=os.path.join(ROOT, "work", "corpus", "corpus_ru_ty.jsonl"))
    args = ap.parse_args()

    meta = {}
    for line in open(BASE, encoding="utf-8"):
        r = json.loads(line)
        meta[(r["file"], r["key"])] = (r.get("speaker") or "", r["en"])

    rows = [json.loads(l) for l in open(args.src, encoding="utf-8")]
    targets = []
    for i, r in enumerate(rows):
        ru = r.get("ru") or ""
        if not ru or not VY.search(ru):
            continue
        sp, en = meta.get((r["file"], r["key"]), ("", r.get("en") or ""))
        if sp and sp != "OBJ":
            continue           # character dialogue: leave the address alone
        targets.append({"i": i, "id": len(targets), "ru": ru, "en": en,
                        "file": r["file"], "key": r["key"]})

    by_file = collections.Counter(t["file"] for t in targets)
    log("rows to unify: %d" % len(targets))
    log("by file: %s" % dict(by_file))

    items = [{"id": t["id"], "ru": t["ru"]} for t in targets]
    BATCH = 15
    batches = [items[i:i + BATCH] for i in range(0, len(items), BATCH)]
    fixed = {}
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(call_batch, b) for b in batches]
        done = 0
        for f in as_completed(futs):
            for pid, cand in f.result():
                fixed[pid] = cand
            done += 1
            if done % 10 == 0:
                log("  %d/%d batches, fixed=%d (%.0fs)"
                    % (done, len(batches), len(fixed), time.time() - t0))

    applied = 0
    for t in targets:
        c = fixed.get(t["id"])
        if not c:
            continue
        if specials(c) != specials(t["ru"]):
            continue
        if VY.search(c):
            continue
        rows[t["i"]]["ru"] = c
        applied += 1
    log("rows switched to 'ты': %d" % applied)

    with open(args.out, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    log("wrote", args.out)


def call_batch(batch):
    payload = json.dumps(batch, ensure_ascii=False, indent=1)
    try:
        txt = call_llm("MiniMax-M3", SYSTEM, payload, max_tokens=8000, temperature=0.1,
                       cache_key="ty|%s|%s" % ("MiniMax-M3", payload))
        arr = extract_texts(txt)
    except Exception as e:
        log("  ty batch failed: %s" % e)
        return []
    if not arr or len(arr) != len(batch):
        return []
    out = []
    for it, cand in zip(batch, arr):
        if isinstance(cand, str) and cand.strip():
            out.append((it["id"], cand))
    return out


if __name__ == "__main__":
    main()
