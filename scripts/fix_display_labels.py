"""The display font is wide, and a handful of short labels are drawn in it in
narrow boxes: a word that does not fit wraps, and its tail lands on the next
line, under the element below.

The narrow ones on the character screen hold about eight characters.
"""
from __future__ import annotations

import json
import os

ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"

FIXES = {
    # the arrow button on the character screen
    "Menu_PreparingSpells_Finish": "Готово",
    # the tab between "Знания" and "Роль"
    "Menu_CharacterCreation_Uses": "Польза",
}


def main():
    import csv
    path = os.path.join(ROOT, "translation", "Russian", "UIElements.csv")
    rows = list(csv.reader(open(path, encoding="utf-8-sig", newline="")))
    applied = 0
    for r in rows:
        if r and r[0] in FIXES:
            r[-1] = FIXES[r[0]]
            applied += 1
    with open(path, "w", encoding="utf-8", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerows(rows)
    print("rows rewritten:", applied)

    manual_path = os.path.join(ROOT, "src", "voice", "manual_fixes.json")
    manual = json.load(open(manual_path, encoding="utf-8"))
    manual.setdefault("UIElements.csv", {}).update(FIXES)
    json.dump(manual, open(manual_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("manual fixes:", sum(len(v) for v in manual.values()))


if __name__ == "__main__":
    main()
