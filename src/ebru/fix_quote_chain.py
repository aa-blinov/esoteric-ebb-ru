#!/usr/bin/env python
"""Second quote pass: repair speech chains using the English quote depth.

Walks the rows in order tracking the English quote depth (a row that starts
with " opens a speech, a row that ends with " closes one) and makes the
Russian guillemets follow the same chain.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "work", "corpus", "corpus_ru_final6.jsonl")
DST = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "work", "corpus", "corpus_ru_final7.jsonl")


def main():
    rows = [json.loads(l) for l in open(SRC, encoding="utf-8")]
    report = []

    # pass 1: find rows that close a speech but never opened one
    for i, r in enumerate(rows):
        en = (r.get("en") or "").strip()
        ru = r.get("ru") or ""
        if not en or not ru:
            continue
        en_open = en.startswith('"')
        en_close = en.endswith('"')
        ru_open = ru.count("«")
        ru_close = ru.count("»")
        if en_close and not en_open and ru_close == 0 and ru_open == 0:
            # this row ends the speech -> it must carry the closing guillemet
            stripped = ru.rstrip()
            r["ru"] = stripped + "»" + ru[len(stripped):]
            report.append("CLOSE  %s / %s: %s" % (r["file"], r["key"], r["ru"][:110]))

    # pass 2: a closing guillemet with no opening anywhere before it -> open the
    # preceding row that the English says opens the speech
    depth = 0
    for i, r in enumerate(rows):
        en = (r.get("en") or "").strip()
        ru = r.get("ru") or ""
        if not en or not ru:
            continue
        ru_open = ru.count("«")
        ru_close = ru.count("»")
        if ru_close > depth and ru_open == 0:
            # find the row that opens this speech
            for j in range(i - 1, max(-1, i - 6), -1):
                pj = rows[j]
                pe = (pj.get("en") or "").strip()
                if pe.startswith('"'):
                    if "«" not in (pj.get("ru") or ""):
                        pj["ru"] = "«" + (pj.get("ru") or "").lstrip()
                        report.append("OPEN   %s / %s: %s" % (pj["file"], pj["key"], pj["ru"][:110]))
                    break
        depth += ru_open - ru_close
        if depth < 0:
            depth = 0

    with open(DST, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    open(os.path.join(ROOT, "quote_chain.txt"), "w", encoding="utf-8").write("\n".join(report))
    print("chain repairs:", len(report))
    print("wrote", DST)


if __name__ == "__main__":
    main()
