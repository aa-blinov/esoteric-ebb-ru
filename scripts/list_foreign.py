import csv
import json
import os
import re
import collections

ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"
T = os.path.join(ROOT, "translation", "Russian")

LEGIT = {
    "hwbt", "it", "dm", "pc", "np", "ui", "hp", "mp", "dnd", "tv", "id", "dlc",
    "sdk", "api", "www", "http", "https", "com", "org", "steam", "ais", "d20",
    "d4", "d6", "d8", "d10", "d12", "lol", "mhr", "rpg", "fps", "xp", "ppg",
    "ar", "pe", "ro", "qa", "cbs", "flm", "tt", "ost", "vol",
    "act", "scene", "interlude", "let", "be", "dust", "averia", "serif",
    "prôv", "carpe", "tenebras", "faux", "pas", "rogue",
}

gl = json.load(open(os.path.join(ROOT, "src", "voice", "glossary.json"), encoding="utf-8"))
for k in gl:
    for t in re.findall(r"[A-Za-z][A-Za-z'\-]+", k):
        LEGIT.add(t.lower())

SPECIAL = re.compile(r"<[^>]*>|\{[^{}]*\}")
WORD = re.compile(r"[A-Za-z][A-Za-z'\-]+")
CYR = re.compile(r"[А-Яа-яЁё]")

rows_out = []
for fn in sorted(os.listdir(T)):
    if not fn.endswith(".csv"):
        continue
    for i, row in enumerate(list(csv.reader(open(os.path.join(T, fn), encoding="utf-8-sig", newline="")))[1:], 1):
        cell = row[-1]
        if not cell or not CYR.search(cell):
            continue
        bad = [w for w in WORD.findall(SPECIAL.sub(" ", cell)) if w.lower() not in LEGIT]
        if bad:
            rows_out.append({"file": fn, "row": i, "key": row[0], "words": bad, "cell": cell})

print("rows with genuine foreign words:", len(rows_out))
words = collections.Counter(w for r in rows_out for w in r["words"])
print(words.most_common())

with open(os.path.join(ROOT, "work", "foreign_manual.json"), "w", encoding="utf-8") as fh:
    json.dump(rows_out, fh, ensure_ascii=False, indent=1)

lines = []
for r in rows_out:
    lines.append("%s | %s | %s" % (r["file"], r["key"], ",".join(r["words"])))
    lines.append("   %s" % r["cell"])
    lines.append("")
open(os.path.join(ROOT, "work", "foreign_manual.txt"), "w", encoding="utf-8").write("\n".join(lines))
print("written work/foreign_manual.txt")
