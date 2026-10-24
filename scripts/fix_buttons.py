"""The narrow arrow button on the character screen takes its label from the
menu strings, and the display font is wide: nine letters do not fit and the
word wraps, pushing the tail under the divider.

  "Продолжить" -> "Дальше"
  "Завершить"  -> "Готово"
"""
import json
import os

ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"

FIXES = {
    "Menu_Button_Continue": "Дальше",
    "Menu_PreparingSpells_Finish": "Готово",
}


def main():
    path = os.path.join(ROOT, "translation", "Russian", "UIElements.csv")
    import csv
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
