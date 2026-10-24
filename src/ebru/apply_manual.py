#!/usr/bin/env python
"""Apply the hand-written corrections to the corpus and to the shipped CSVs.

`src/voice/manual_fixes.json` holds the lines that the model kept getting
wrong: an English word fused into a Russian sentence, a term that had to
follow the glossary, a line that had to lose ten characters to fit its panel.
They are part of the source, not a patch on top of it, so a rebuild keeps
them.
"""
from __future__ import annotations

import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIXES = os.path.join(ROOT, "src", "voice", "manual_fixes.json")
TRANSLATION = os.path.join(ROOT, "translation", "Russian")


def load_fixes():
    with open(FIXES, encoding="utf-8") as fh:
        return json.load(fh)


def apply_to_corpus(src, dst, fixes):
    rows = [json.loads(l) for l in open(src, encoding="utf-8")]
    applied = 0
    for r in rows:
        table = fixes.get(r["file"])
        if not table:
            continue
        new = table.get(r["key"])
        if new is not None and new != r.get("ru"):
            r["ru"] = new
            applied += 1
    with open(dst, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return applied


def apply_to_csv(fixes):
    applied = 0
    for name, table in fixes.items():
        path = os.path.join(TRANSLATION, name)
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
            w = csv.writer(fh, lineterminator="\r\n")
            w.writerows(out)
    return applied


def main():
    fixes = load_fixes()
    if len(sys.argv) > 2:
        applied = apply_to_corpus(sys.argv[1], sys.argv[2], fixes)
        print("corpus rows rewritten:", applied)
    else:
        applied = apply_to_csv(fixes)
        print("csv rows rewritten:", applied)


if __name__ == "__main__":
    main()
