import csv
import json
import os
import re

ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"
MANUAL = os.path.join(ROOT, "src", "voice", "manual_fixes.json")
T = os.path.join(ROOT, "translation", "Russian")

FIXES = {
    ("Dialogs.csv", "AR_Viira_948"):
        "Склонить колено перед меньшим злом — значит отбросить свою гордость и мужество.",
    ("Dialogs.csv", "JC_Urth_387"):
        "«На запоминание заклинания, Рагн, уходят часы.»",
    ("Dialogs.csv", "AR_Viira_Ivcx_322"):
        "«Да, за такое — чёрт с тобой.»",
    ("Dialogs.csv", "CB_Bondavol_849"):
        "«И после всех тех боёв с Вискеном я был далеко не в лучшей <shake>прррима</shake>-форме.»",
    ("Dialogs.csv", "GG_Miska_68"):
        "«Это не оправдание.»",
    ("Dialogs.csv", "GG_Miska_660"):
        "Он тут же снова поворачивается к Сагелисту с улыбкой. «Готова продолжить, ми леди.»",
    ("Dialogs.csv", "LP_Lisa_1305"):
        "«Вы, набожные чокнутые, вечно так болезненно реагируете.»",
    ("Dialogs.csv", "OP_Map_21"):
        "«— Должна быть тысячелетней. Посмотри на этих маленьких улиточных людей на ней.»",
    ("Dialogs.csv", "VL_Visken_1276"):
        "«Ты казался немного головокружительным.»",
    ("Dialogs.csv", "TE_Booths_97"):
        "«Возьми с собой. Покажи Старой Леди.»",
}

manual = json.load(open(MANUAL, encoding="utf-8"))
for (fn, key), text in FIXES.items():
    manual.setdefault(fn, {})[key] = text
json.dump(manual, open(MANUAL, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("manual fixes now:", sum(len(v) for v in manual.values()))

# apply them to the shipped CSVs
applied = 0
for fn, table in manual.items():
    path = os.path.join(T, fn)
    if not os.path.exists(path):
        continue
    rows = list(csv.reader(open(path, encoding="utf-8-sig", newline="")))
    out = []
    for r in rows:
        if r and r[0] in table:
            r[-1] = table[r[0]]
            applied += 1
        out.append(r)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        csv.writer(fh, lineterminator="\r\n").writerows(out)
print("csv rows rewritten:", applied)
