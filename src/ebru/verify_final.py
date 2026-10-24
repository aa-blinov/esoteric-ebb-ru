#!/usr/bin/env python
"""Final verification of the installed Russian localization."""
from __future__ import annotations

import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FINAL = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "work", "corpus", "corpus_ru_final.jsonl")
BASE = os.path.join(ROOT, "work", "corpus", "corpus.jsonl")

meta = {}
for line in open(BASE, encoding="utf-8"):
    r = json.loads(line)
    meta[(r["file"], r["key"])] = (r.get("speaker") or "", r["en"])

rows = [json.loads(l) for l in open(FINAL, encoding="utf-8")]
out = []
w = out.append

VY = re.compile(r"\b(вы|вам|вас|ваш|ваша|ваше|ваши|вами|ваших|вашего|вашей)\b", re.I)
TY = re.compile(r"\b(ты|тебе|тебя|твой|твоя|твоё|твои|твоим|твоих|твоего|твоей)\b", re.I)
SPECIAL = re.compile(r"<[^>]*>|\{[^{}]*\}")

w("file: %s" % os.path.basename(FINAL))
w("rows: %d" % len(rows))

# --- typography --------------------------------------------------------------
c = collections.Counter()
for r in rows:
    ru = r.get("ru") or ""
    c['straight quote "'] += ru.count('"')
    c["«"] += ru.count("«")
    c["»"] += ru.count("»")
    c["period outside  »."] += len(re.findall(r"»\.", ru))
    c["period inside   .»"] += len(re.findall(r"\.»", ru))
    c["... (three dots)"] += ru.count("...")
    c["… (ellipsis)"] += ru.count("…")
    c["— em dash"] += ru.count("—")
    c["так же"] += len(re.findall(r"\bтак же\b", ru, re.I))
    c["spaced hyphen"] += len(re.findall(r"(?<![\w])-(?![\w])", ru))
    if ru.count("«") != ru.count("»"):
        c["UNBALANCED rows"] += 1
    if "  " in ru:
        c["double space rows"] += 1
    if re.search(r"\s+[,.;:!?]", ru):
        c["space before punct rows"] += 1

w("\n=== typography ===")
for k, v in sorted(c.items()):
    w("  %-24s %d" % (k, v))

# --- markup integrity -------------------------------------------------------
bad_markup = 0
for r in rows:
    ru = r.get("ru") or ""
    if not ru:
        continue
    en = meta.get((r["file"], r["key"]), ("", r.get("en") or ""))[1]
    if SPECIAL.findall(ru) != SPECIAL.findall(en):
        bad_markup += 1
w("\n=== markup ===")
w("  rows whose markup differs from EN: %d" % bad_markup)

# --- address ----------------------------------------------------------------
addr = collections.defaultdict(lambda: {"ty": 0, "vy": 0})
narr_vy = []
for r in rows:
    ru = r.get("ru") or ""
    if not ru:
        continue
    sp = meta.get((r["file"], r["key"]), ("", ""))[0]
    if VY.search(ru):
        addr[r["file"]]["vy"] += 1
        if not sp or sp == "OBJ":
            narr_vy.append(r)
    if TY.search(ru):
        addr[r["file"]]["ty"] += 1
w("\n=== address ===")
w("%-16s %8s %8s" % ("file", "ты", "вы"))
for f in sorted(addr):
    w("%-16s %8d %8d" % (f, addr[f]["ty"], addr[f]["vy"]))
w("  narrative rows still using 'вы': %d" % len(narr_vy))
for r in narr_vy[:12]:
    w("    %s / %s : %s" % (r["file"], r["key"], (r.get("ru") or "")[:90]))

# --- repeated lines ---------------------------------------------------------
variants = collections.defaultdict(set)
for r in rows:
    en = (r.get("en") or "").strip()
    if en and r.get("ru"):
        variants[en].add(r["ru"])
incons = {k: v for k, v in variants.items() if len(v) > 1}
w("\n=== repeated lines ===")
w("  distinct EN: %d | inconsistent groups: %d" % (len(variants), len(incons)))
for k, v in list(incons.items())[:15]:
    w("    EN: %s" % k[:90])
    for x in sorted(v):
        w("       → %s" % x[:90])

# --- leftovers --------------------------------------------------------------
w("\n=== leftovers ===")
empty = sum(1 for r in rows if not (r.get("ru") or "").strip())
w("  empty translations: %d" % empty)
latin_only = 0
for r in rows:
    ru = r.get("ru") or ""
    if ru and not re.search(r"[А-Яа-яЁё]", ru):
        latin_only += 1
w("  rows without any Cyrillic: %d" % latin_only)

open(os.path.join(ROOT, "final_verification.txt"), "w", encoding="utf-8").write("\n".join(out))
print("written final_verification.txt")
