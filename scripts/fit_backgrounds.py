"""Rewrite the background descriptions to fit the box they are drawn in.

The description box on the character screen holds four lines, and the ability
badges are drawn over the fifth. The English fits by design; the Russian has
to be shorter than its English source to land in the same four lines.
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"
sys.path.insert(0, os.path.join(ROOT, "src", "ebru"))
from llm_client import call_llm, extract_json_array  # noqa: E402

BUDGET = 135
SPECIAL = re.compile(r"<[^>]*>|\{[^{}]*\}")

SYSTEM = """Ты — переводчик игры Esoteric Ebb. Сейчас правишь описание предыстории персонажа.

Это описание рисуется в рамке шириной 470 пикселей, куда помещаются ЧЕТЫРЕ строки.
Пятую строку перекрывают значки характеристик. Английский оригинал в такую рамку влезает,
а русский текст — длиннее по ширине, поэтому его нужно сократить, не потеряв смысла.

ЗАДАЧА: напиши русский текст не длиннее {budget} символов.

ПРАВИЛА:
1. Сохрани смысл полностью: что случилось с героем, чем он кончился, что он чувствует.
2. Сохрани интонацию: сухо, с сухой иронией, без пафоса и без сюсюканья.
3. Не выдумывай новых фактов. Не добавляй имён, если их не было.
4. Разметку перенеси из исходного русского текста как есть: {markup}
5. Выход — JSON-массив строк РОВНО той же длины: исправленный текст для каждой строки.
"""


def main():
    src = os.path.join(ROOT, "work", "backgrounds.json")
    items = json.load(open(src, encoding="utf-8"))
    targets = [i for i in items if len(i["ru"]) > BUDGET]
    print("backgrounds over the budget:", len(targets))

    def work(batch):
        payload = [{"id": n, "en": it["en"], "ru": it["ru"],
                    "limit": BUDGET} for n, it in enumerate(batch)]
        user = json.dumps(payload, ensure_ascii=False, indent=1)
        system = SYSTEM.replace("{budget}", str(BUDGET)).replace("{markup}", "сохрани теги и плейсхолдеры из исходника")
        try:
            txt = call_llm("MiniMax-M3", system, user, max_tokens=8000, temperature=0.3,
                           cache_key="bg|%s|%s" % (system, user))
            arr = extract_json_array(txt)
        except Exception as e:
            print("  batch failed: %s" % e)
            return []
        out = []
        for it, cand in zip(batch, arr or []):
            if isinstance(cand, str) and cand.strip():
                out.append((it, cand))
        return out

    BATCH = 6
    batches = [targets[i:i + BATCH] for i in range(0, len(targets), BATCH)]
    results = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(work, b) for b in batches]
        done = 0
        for f in as_completed(futs):
            for it, cand in f.result():
                results[it["key"]] = cand
            done += 1
            if done % 2 == 0:
                print("  %d/%d batches, %d rewritten" % (done, len(batches), len(results)), flush=True)

    accepted = {}
    rejected = []
    for it in targets:
        cand = results.get(it["key"])
        if not cand:
            rejected.append((it["key"], "no answer"))
            continue
        if len(cand) > BUDGET:
            rejected.append((it["key"], "%d chars" % len(cand)))
            continue
        if "".join(SPECIAL.findall(cand)) != "".join(SPECIAL.findall(it["ru"])):
            rejected.append((it["key"], "markup"))
            continue
        if re.search(r"[A-Za-z]", cand.replace("Averia", "")):
            rejected.append((it["key"], "latin"))
            continue
        accepted[it["key"]] = cand

    print("accepted: %d, rejected: %d" % (len(accepted), len(rejected)))
    for k, why in rejected:
        print("   rejected", k, why)

    lines = []
    for it in targets:
        lines.append("%s" % it["key"])
        lines.append("   EN: %s" % it["en"])
        lines.append("   OLD (%d): %s" % (len(it["ru"]), it["ru"]))
        new = accepted.get(it["key"], "")
        lines.append("   NEW (%d): %s" % (len(new), new))
        lines.append("")
    open(os.path.join(ROOT, "work", "backgrounds_new.txt"), "w", encoding="utf-8").write("\n".join(lines))
    json.dump(accepted, open(os.path.join(ROOT, "work", "backgrounds_new.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("written work/backgrounds_new.txt")


if __name__ == "__main__":
    main()
