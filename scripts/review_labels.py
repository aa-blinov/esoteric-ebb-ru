#!/usr/bin/env python
"""Review the short interface labels for contextually wrong translations.

A one-word label is the hard case: "Load" is «нагрузка» in a dictionary and
«загрузка» in a save menu, and the model that translated them in a batch had
nothing but the word itself. This pass asks for a second opinion on the
labels, with the file they live in as the context.
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"
sys.path.insert(0, os.path.join(ROOT, "src", "ebru"))
from llm_client import call_llm, extract_json_array  # noqa: E402

SYSTEM = """Ты — редактор интерфейса русского перевода игры Esoteric Ebb.

Перед тобой короткие подписи интерфейса: ключ, английский оригинал и текущий русский перевод.
Ключ говорит, где стоит подпись (Menu_Button_* — кнопка главного меню, Setting_* — заголовок
настройки, Keybind_* — клавиша, Item*/Spell*/*_name — название предмета, заклинания, умения).

Задача: найти переводы, которые формально верны, но неверны по смыслу в своём месте.
Типичные ошибки: «Load» в меню сохранений → «Нагрузка» вместо «Загрузка»; «Reject» → «Отвергнуть»
вместо «Отклонить»; существительное вместо глагола и наоборот.

ПРАВИЛА:
1. Вход — JSON-массив объектов {"key": "...", "en": "...", "ru": "..."}.
2. Выход — JSON-массив объектов ТОЛЬКО для тех ключей, где перевод нужно исправить:
   {"key": "...", "ru": "исправленный перевод", "why": "почему в одном предложении"}.
   Если всё верно, верни пустой массив.
3. Не трогай то, что переведено правильно. Не выдумывай новые формулировки ради стиля.
4. Учитывай, что это интерфейс: коротко, точно, в том же регистре, что и соседние подписи.
"""


def main():
    src = os.path.join(ROOT, "work", "short_labels.json")
    labels = json.load(open(src, encoding="utf-8"))
    print("labels:", len(labels))

    BATCH = 40
    batches = [labels[i:i + BATCH] for i in range(0, len(labels), BATCH)]
    found = {}
    lock = threading.Lock()

    def work(b):
        user = json.dumps(b, ensure_ascii=False, indent=1)
        try:
            txt = call_llm("MiniMax-M3", SYSTEM, user, max_tokens=8000, temperature=0.2,
                           cache_key="review2|%s" % user)
            arr = extract_json_array(txt)
        except Exception as exc:
            print("  batch error: %s" % exc, flush=True)
            return []
        out = []
        for item in arr or []:
            if isinstance(item, dict) and item.get("key") and item.get("ru"):
                out.append(item)
        return out

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=10) as ex:
        futs = [ex.submit(work, b) for b in batches]
        done = 0
        for f in as_completed(futs):
            for item in f.result():
                with lock:
                    found[item["key"]] = item
            done += 1
            if done % 10 == 0:
                print("  %d/%d batches, flagged=%d (%.0fs)"
                      % (done, len(batches), len(found), time.time() - t0), flush=True)

    print("flagged:", len(found))
    if not found:
        print("NOTHING FLAGGED - check the endpoint")
    with open(os.path.join(ROOT, "work", "label_review.json"), "w", encoding="utf-8") as fh:
        json.dump(found, fh, ensure_ascii=False, indent=1)

    lines = []
    for k in sorted(found):
        lines.append("%s" % k)
        lines.append("   EN: %s" % next((l["en"] for l in labels if l["key"] == k), ""))
        lines.append("   RU: %s" % next((l["ru"] for l in labels if l["key"] == k), ""))
        lines.append("   →  %s   (%s)" % (found[k]["ru"], found[k].get("why", "")))
        lines.append("")
    open(os.path.join(ROOT, "work", "label_review.txt"), "w", encoding="utf-8").write("\n".join(lines))
    print("written work/label_review.txt")


if __name__ == "__main__":
    main()
