#!/usr/bin/env python
"""Targeted fix for the few rows with surplus or nested guillemets.

  A. "…».»"  -> "….»"     surplus closing quote at the end of a bubble
  B. nested guillemets -> „…“   (Russian convention for a quote inside a quote)
Nothing else is touched.
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "work", "corpus", "corpus_ru_final.jsonl")
DST = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "work", "corpus", "corpus_ru_final2.jsonl")


def fix_nested(ru: str) -> str:
    """Outer guillemets stay, inner ones become „…“."""
    if ru.count("«") <= 1:
        return ru
    out = []
    depth = 0
    for ch in ru:
        if ch == "«":
            depth += 1
            out.append("«" if depth == 1 else "„")
        elif ch == "»":
            out.append("»" if depth <= 1 else "“")
            depth = max(0, depth - 1)
        else:
            out.append(ch)
    return "".join(out)


def fix_surplus(ru: str) -> str:
    """«…».» -> «….» (one quote too many at the end)."""
    return re.sub(r"»\.»\s*$", ".»", ru.rstrip())


def fix_missing_close(en: str, ru: str) -> str:
    """The English closes a quote here, the Russian must close it too."""
    if not en.strip().endswith('"'):
        return ru
    if "»" in ru:
        return ru
    stripped = ru.rstrip()
    return stripped + "»" + ru[len(stripped):]


def main():
    rows = [json.loads(l) for l in open(SRC, encoding="utf-8")]
    changed = 0
    report = []
    for r in rows:
        ru = r.get("ru") or ""
        if not ru:
            continue
        en = r.get("en") or ""
        new = fix_nested(ru)
        new = fix_surplus(new)
        new = fix_missing_close(en, new)
        if new != ru:
            r["ru"] = new
            changed += 1
            report.append("KEY: %s / %s\n  OLD: %s\n  NEW: %s" % (r["file"], r["key"], ru[:130], new[:130]))
    with open(DST, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    open(os.path.join(ROOT, "quote_fix.txt"), "w", encoding="utf-8").write("\n".join(report))
    print("rows changed:", changed)
    print("wrote", DST)


if __name__ == "__main__":
    main()
