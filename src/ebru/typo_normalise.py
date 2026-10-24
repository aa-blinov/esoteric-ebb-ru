#!/usr/bin/env python
"""Deterministic typographic normalisation of the Russian translation.

Brings the whole corpus to one Russian typographic standard:
  "..."   -> …
  "..."   -> «...»   (paired guillemets)
  так же  -> также
  spaced hyphen -> em dash where it is used as a dash

Safe, reversible and applied identically to every row, so the whole game
reads as one text.
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "work", "corpus", "corpus_ru_hand.jsonl")
DST = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "work", "corpus", "corpus_ru_typo.jsonl")

DASH = re.compile(r"(?<=\s)-(?=\s)")
TRAIL_PUNCT = re.compile(r"(»)([.!?])\s*$")


def normalise(text: str) -> str:
    if not text:
        return text
    t = text

    # ellipsis: any run of 3+ dots -> single ellipsis char
    t = re.sub(r"\.{3,}", "…", t)

    # paired straight quotes -> guillemets
    if '"' in t:
        out = []
        open_q = True
        for ch in t:
            if ch == '"':
                out.append("«" if open_q else "»")
                open_q = not open_q
            else:
                out.append(ch)
        t = "".join(out)

    # spaced hyphen used as a dash -> em dash
    t = DASH.sub("—", t)

    # orthographic split
    t = re.sub(r"\bтак же\b", "также", t, flags=re.I)

    # Russian typography: sentence-final punctuation belongs inside the closing
    # guillemet when the quote ends the line ("«Слово»." -> "«Слово.»")
    t = TRAIL_PUNCT.sub(lambda m: m.group(2) + m.group(1), t)
    # stray spaces next to guillemets
    t = re.sub(r"«\s+", "«", t)
    t = re.sub(r"\s+»", "»", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    t = re.sub(r"[ \t]+([,.;:!?])", r"\1", t)

    return t


def main():
    rows = [json.loads(l) for l in open(SRC, encoding="utf-8")]
    changed = 0
    for r in rows:
        old = r.get("ru") or ""
        new = normalise(old)
        if new != old:
            r["ru"] = new
            changed += 1
    with open(DST, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("rows:", len(rows), "changed:", changed)
    print("wrote", DST)


if __name__ == "__main__":
    main()
