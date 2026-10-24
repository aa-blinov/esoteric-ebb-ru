#!/usr/bin/env python
"""Fix English words left inside Russian sentences ("тысячи лет old").

These slipped past the language QA because the word also exists in the
English source, so the QA treated it as an allowed proper noun.
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

TAG = re.compile(r"<[^>]*>|\{[^{}]*\}")
WORD = re.compile(r"[A-Za-z][A-Za-z'\-]{1,}")
CYR = re.compile(r"[А-Яа-яЁё]")

SYSTEM = """Ты — редактор русского перевода игры Esoteric Ebb.

В русских предложениях остались английские слова. Для каждой строки перечислены именно эти
слова — их ОБЯЗАТЕЛЬНО нужно заменить на русские эквиваленты. Ни одно из перечисленных слов
не должно остаться в ответе.

ПРИМЕРЫ:
  EN: "Who cares about the halflings?"   RU: "Кому вообще cares о полувеках?"
  → "Кому вообще дело до полувеков?"
  EN: "Do not worry about simple items."   RU: "Не worry about простые предметы."
  → "Не волнуйся из-за простых предметов."
  EN: "A vast labyrinth."   RU: "Это vast, неукротимый лабиринт."
  → "Это огромный, неукротимый лабиринт."

ПРАВИЛА:
1. Вход — JSON-массив объектов {"id": N, "en": "английский оригинал", "ru": "перевод",
   "words": ["английские слова, которые нужно заменить"]}.
   Выход — JSON-массив строк РОВНО той же длины и порядка: исправленный перевод.
2. Заменяй ТОЛЬКО перечисленные слова и те слова, без которых предложение рассыпается.
   Весь остальной текст — буква в букву, включая порядок слов, знаки препинания и теги.
3. Имена собственные (топонимы, имена персонажей, названия, аббревиатуры, заклинания) оставь
   как есть, если они есть в глоссарии; игровые термины переведи по глоссарию.
4. Разметку перенеси символ в символ: теги и плейсхолдеры те же, в том же порядке.
5. Не добавляй и не убирай ничего по смыслу.
"""


def allowed_tokens():
    out = set()
    for fn in ("glossary_polished.json", "names.json"):
        p = os.path.join(ROOT, "work", "corpus", fn)
        if os.path.exists(p):
            data = json.load(open(p, encoding="utf-8"))
            for k in data:
                for tok in WORD.findall(k):
                    out.add(tok.lower())
    out |= {"hwbt", "it", "dm", "pc", "np", "ui", "hp", "mp", "dnd", "tv", "id", "dlc",
            "sdk", "api", "www", "http", "https", "com", "org", "steam", "ais", "d20",
            "d4", "d6", "d8", "d10", "d12", "lol", "mhr", "rpg", "fps", "xp", "ppg",
            "ar", "pe", "ro", "rogue", "cleric", "warlock", "barbarian", "druid",
            "fighter", "rogue", "ranger", "monk", "paladin", "sorcerer", "wizard"}
    return out


def log(*a):
    with _lock:
        print(*a, flush=True)


def foreign_words(ru, allowed):
    clean = TAG.sub(" ", ru or "")
    if not clean.strip() or not CYR.search(clean):
        return []
    return [w for w in WORD.findall(clean) if w.lower() not in allowed]


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "work", "corpus", "corpus_ru_final9.jsonl")
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "work", "corpus", "corpus_ru_final10.jsonl")
    allowed = allowed_tokens()

    rows = [json.loads(l) for l in open(src, encoding="utf-8")]
    targets = []
    for i, r in enumerate(rows):
        ws = foreign_words(r.get("ru") or "", allowed)
        if ws:
            targets.append({"i": i, "id": len(targets), "ru": r["ru"], "en": r.get("en") or "",
                            "w": ws})
    log("rows with foreign words: %d" % len(targets))

    BATCH = 10
    batches = [targets[i:i + BATCH] for i in range(0, len(targets), BATCH)]
    fixed = {}
    t0 = time.time()

    def work(b):
        payload = [{"id": t["id"], "en": t["en"], "ru": t["ru"], "words": t["w"]} for t in b]
        user = json.dumps(payload, ensure_ascii=False, indent=1)
        try:
            txt = call_llm("MiniMax-M3", SYSTEM, user, max_tokens=8000, temperature=0.15 + 0.1 * (int(os.environ.get("EB_ATTEMPT","1")) - 1),
                           cache_key="foreign|%s|%s|%s" % ("MiniMax-M3", os.environ.get("EB_ATTEMPT","1"), user))
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
            if foreign_words(cand, allowed):
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
            if done % 10 == 0:
                log("  %d/%d batches, fixed=%d (%.0fs)"
                    % (done, len(batches), len(fixed), time.time() - t0))

    applied = 0
    for t in targets:
        c = fixed.get(t["id"])
        if c:
            rows[t["i"]]["ru"] = c
            applied += 1
    log("rows fixed: %d" % applied)

    with open(dst, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    log("wrote", dst)


if __name__ == "__main__":
    main()
