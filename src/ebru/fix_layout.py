#!/usr/bin/env python
"""Layout fixes: shorten big-font runs that overflow the fixed-width lore panel.

The character-creation lore panel is ~541 px wide with ~500 px of usable text
width. Russian words are longer than English ones, so several big-font runs
(size=33..200) no longer fit and the block wraps into the neighbouring element.

Only the runs that actually overflow are touched; the markup (tags, order) is
preserved, except for one deliberate size reduction.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "work", "corpus", "corpus_ru_FINAL.jsonl")
DST = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "work", "corpus", "corpus_ru_FIX.jsonl")

# key -> new Russian text
FIXES = {
    # the reported overlap: "ДОПОЛНИТЕЛЬНЫЕ ПРЕДМЕТЫ" was ~666 px inside a 500 px panel
    "AbilityScoreInfo_Strength_Uses1":
        "<size=38>Большая Сила</size>\nпозволяет тебе снаряжать \n<size=45>ЛИШНИЕ ПРЕДМЕТЫ",

    # "Как стремительный Разбойник" -> shorter, same sense
    "AbilityScoreInfo_Dexterity_Uses2":
        "Вскрывать замки, Подкрасться, Уклоняться от ловушек, Бросать инициативу и быстро реагировать "
        "<size=35>Как дерзкий разбойник",

    # first line was 634 px (EN: 426 px) -> one line like the original
    "AbilityScoreInfo_Constitution_Uses3":
        "Твоя партия набрала 2% голосов на прошлой неделе, и\n<size=43>тебе всё равно",

    # "Азгалианского" at size 73 was ~504 px; size 62 brings it to ~430 px.
    # The emphasis stays on the same word, only the size is adapted to the panel.
    "AbilityScoreInfo_Wisdom_Uses3":
        "Эгалитарная надежда <size=62>Азгалианского <size=43>рабочего класса",
}


def main():
    rows = [json.loads(l) for l in open(SRC, encoding="utf-8")]
    applied = 0
    for r in rows:
        fix = FIXES.get(r["key"])
        if fix is None:
            continue
        r["ru"] = fix
        applied += 1
    with open(DST, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("applied:", applied, "of", len(FIXES))
    print("wrote", DST)


if __name__ == "__main__":
    main()
