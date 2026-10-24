"""Apply the reviewed corrections to the shipped CSVs and to the manual fixes."""
from __future__ import annotations

import csv
import json
import os
import re

ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"
WORK = os.path.join(ROOT, "work")
T = os.path.join(ROOT, "translation", "Russian")
MANUAL = os.path.join(ROOT, "src", "voice", "manual_fixes.json")
SPECIAL = re.compile(r"<[^>]*>|\{[^{}]*\}")


def main():
    changes = json.load(open(os.path.join(WORK, "changes.json"), encoding="utf-8"))
    by_file = {}
    for entry in changes.values():
        by_file.setdefault(entry["file"], {})[entry["key"]] = entry["ru"]

    applied = 0
    rejected = []
    for fn, table in by_file.items():
        path = os.path.join(T, fn)
        if not os.path.exists(path):
            continue
        rows = list(csv.reader(open(path, encoding="utf-8-sig", newline="")))
        out = []
        for r in rows:
            if r and r[0] in table:
                new = table[r[0]]
                if "".join(SPECIAL.findall(new)) != "".join(SPECIAL.findall(r[-1])):
                    rejected.append("%s: %s (markup)" % (fn, r[0]))
                else:
                    r[-1] = new
                    applied += 1
            out.append(r)
        with open(path, "w", encoding="utf-8", newline="") as fh:
            csv.writer(fh, lineterminator="\n").writerows(out)

    print("rows rewritten:", applied)
    if rejected:
        print("rejected for markup:")
        for r in rejected:
            print("  ", r)

    # the corrections belong to the source, not to the output
    manual = json.load(open(MANUAL, encoding="utf-8"))
    for fn, table in by_file.items():
        manual.setdefault(fn, {}).update(table)
    json.dump(manual, open(MANUAL, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("manual fixes:", sum(len(v) for v in manual.values()))


if __name__ == "__main__":
    main()
