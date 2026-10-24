#!/usr/bin/env python
"""Find repeated source strings that were translated inconsistently."""
from __future__ import annotations

import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "work", "corpus", "corpus_ru_hand.jsonl")

rows = [json.loads(l) for l in open(SRC, encoding="utf-8")]
rows = [r for r in rows if r.get("ru")]

groups = collections.defaultdict(set)
counts = collections.Counter()
for r in rows:
    en = (r["en"] or "").strip()
    if len(en) < 4:
        continue
    groups[en].add(r["ru"])
    counts[en] += 1

inconsistent = {k: v for k, v in groups.items() if len(v) > 1}
print("distinct EN strings:", len(groups))
print("repeated EN strings (n>1):", sum(1 for k in counts if counts[k] > 1))
print("INCONSISTENT groups (>1 RU variant):", len(inconsistent))
rows_affected = sum(counts[k] for k in inconsistent)
print("rows affected:", rows_affected)

out = []
for en, variants in sorted(inconsistent.items(), key=lambda kv: -counts[kv[0]])[:120]:
    out.append("EN (%d×): %s" % (counts[en], en[:120]))
    for v in sorted(variants):
        out.append("    → %s" % v[:120])
    out.append("")

open(os.path.join(ROOT, "inconsistent.txt"), "w", encoding="utf-8").write("\n".join(out))
print("wrote inconsistent.txt")

# also: how often do long dialogue lines repeat at all
rep = collections.Counter()
for en, n in counts.items():
    if n > 1 and len(en) > 25:
        rep[n] += 1
print("\nrepeated long lines by multiplicity:", dict(sorted(rep.items())))
