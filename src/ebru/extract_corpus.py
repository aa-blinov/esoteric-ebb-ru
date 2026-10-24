#!/usr/bin/env python
"""Extract all EN strings from the Official localization CSVs into a JSONL corpus.

Also inventories inline markup / placeholders so the translation stage can
reproduce them byte-exactly.
"""
import os
import csv
import json
import re
import sys
import collections

LOC = os.path.join(os.environ.get(
    "EB_GAME_DIR",
    r"C:\Program Files (x86)\Steam\steamapps\common\Esoteric Ebb"),
    "Esoteric Ebb_Data", "StreamingAssets", "Localization")
OFF = os.path.join(LOC, "Official")
OUT = os.path.join(ROOT, "work", "corpus")
os.makedirs(OUT, exist_ok=True)

# files where a translated column exists, and the column layout
PLACEHOLDER = re.compile(r"\{[^{}]*\}")
DOLLAR = re.compile(r"\$[A-Za-z_][A-Za-z0-9_]*")
TAG = re.compile(r"</?[A-Za-z][^>]*>")
SPECIAL = re.compile(r"<[^>]*>|\{[^{}]*\}|\$[A-Za-z_][A-Za-z0-9_]*")

stats = collections.OrderedDict()
ph_counter = collections.Counter()
tag_counter = collections.Counter()
dollar_counter = collections.Counter()
rows_out = []

for fn in sorted(os.listdir(OFF)):
    if not fn.lower().endswith(".csv"):
        continue
    path = os.path.join(OFF, fn)
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.reader(fh))
    header = rows[0]
    body = rows[1:]
    name = fn[:-4]

    en_idx = None
    for i, h in enumerate(header):
        if h.strip() == "EN":
            en_idx = i
            break
    if en_idx is None:
        print("!! no EN column in", fn, header)
        continue

    n_filled = 0
    n_empty = 0
    total_chars = 0
    for r in body:
        if len(r) <= en_idx:
            continue
        en = r[en_idx]
        key = r[0]
        speaker = ""
        if len(r) > 2 and header[2].strip() == "Speaker":
            speaker = r[2]
        if not en.strip():
            n_empty += 1
            continue
        n_filled += 1
        total_chars += len(en)
        for m in SPECIAL.findall(en):
            if m.startswith("{"):
                ph_counter[m] += 1
            elif m.startswith("$"):
                dollar_counter[m] += 1
            else:
                tag_counter[m] += 1
        rows_out.append({
            "file": name,
            "key": key,
            "speaker": speaker,
            "en": en,
            "ru": None,
        })
    stats[name] = {
        "header": header,
        "rows": len(body),
        "filled": n_filled,
        "empty": n_empty,
        "en_chars": total_chars,
    }
    print("%-16s rows=%-6d filled=%-6d empty=%-5d en_chars=%d" % (name, len(body), n_filled, n_empty, total_chars))

print("\n=== unique {placeholders}: %d ===" % len(ph_counter))
for k, v in ph_counter.most_common(40):
    print("  %-30s %d" % (k, v))

print("\n=== unique $VARS: %d ===" % len(dollar_counter))
for k, v in dollar_counter.most_common(40):
    print("  %-30s %d" % (k, v))

print("\n=== unique tags: %d ===" % len(tag_counter))
for k, v in tag_counter.most_common(60):
    print("  %-45s %d" % (k, v))

with open(os.path.join(OUT, "corpus.jsonl"), "w", encoding="utf-8") as fh:
    for row in rows_out:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
print("\ncorpus rows:", len(rows_out))

with open(os.path.join(OUT, "stats.json"), "w", encoding="utf-8") as fh:
    json.dump(stats, fh, ensure_ascii=False, indent=2)
