import json
import os
import re
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rows = [json.loads(l) for l in open(ROOT + r"\work\corpus\corpus_ru_final9.jsonl", encoding="utf-8")]

gl = json.load(open(ROOT + r"\work\corpus\glossary_polished.json", encoding="utf-8"))
names = json.load(open(ROOT + r"\work\corpus\names.json", encoding="utf-8"))

allowed = set()
for k in list(gl.keys()) + list(names.keys()):
    for tok in re.findall(r"[A-Za-z][A-Za-z'\-]*", k):
        allowed.add(tok.lower())
allowed |= {"hwbt", "it", "dm", "pc", "np", "ui", "hp", "mp", "dnd", "tv", "id", "dlc",
            "sdk", "api", "www", "http", "https", "com", "org", "steam", "ais", "d20",
            "d4", "d6", "d8", "d10", "d12", "d20", "lol", "mhr", "rpg", "fps", "xp"}

WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")
CYR = re.compile(r"[А-Яа-яЁё]")

hits = []
for r in rows:
    ru = r.get("ru") or ""
    if not ru or not CYR.search(ru):
        continue
    for m in WORD.finditer(ru):
        w = m.group(0)
        if w.lower() in allowed:
            continue
        hits.append((r, w))
        break

print("rows with a foreign word embedded in Russian:", len(hits))
c = collections.Counter(w for _, w in hits)
print("most common:", c.most_common(25))

out = []
for r, w in hits[:80]:
    out.append("KEY: %s / %s   [%s]" % (r["file"], r["key"], w))
    out.append("  EN: %s" % (r.get("en") or "")[:120])
    out.append("  RU: %s" % (r.get("ru") or "")[:120])
    out.append("")
open(ROOT + r"\foreign_words.txt", "w", encoding="utf-8").write("\n".join(out))
print("written foreign_words.txt")
