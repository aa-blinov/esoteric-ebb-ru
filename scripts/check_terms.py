import csv
import json
import os
import re

GAME = os.environ.get("EB_GAME_DIR", r"M:\SteamLibrary\steamapps\common\Esoteric Ebb")
base = os.path.join(GAME, "Esoteric Ebb_Data", "StreamingAssets", "Localization")
OUT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru\work"

# every English line of the game, with the Russian beside it
pairs = []
for fn in sorted(os.listdir(os.path.join(base, "Official"))):
    if not fn.endswith(".csv"):
        continue
    with open(os.path.join(base, "Official", fn), encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.reader(fh))
    header = rows[0]
    idx = next((i for i, h in enumerate(header) if h.strip() == "EN"), None)
    if idx is None:
        continue
    with open(os.path.join(base, "Russian", fn), encoding="utf-8-sig", newline="") as fh:
        ru = {r[0]: r[-1] for r in list(csv.reader(fh))[1:] if r}
    for r in rows[1:]:
        if not r:
            continue
        en = r[idx] if len(r) > idx else ""
        pairs.append((fn, r[0], en, ru.get(r[0], "")))

for term in ("Sorcerer", "Warlock", "Constitution", "Roper", "Barkskin", "Hit Points", "Lawful"):
    out = ["===== %s =====" % term]
    n = 0
    for fn, key, en, ru in pairs:
        if term.lower() in (en or "").lower():
            out.append("%-16s %-34s EN: %s" % (fn[:16], key[:34], en[:95]))
            out.append("%-16s %-34s RU: %s" % ("", "", ru[:95]))
            n += 1
            if n >= 8:
                break
    out.append("   (matches shown: %d)" % n)
    out.append("")
    open(os.path.join(OUT, "term_%s.txt" % re.sub(r"\W+", "_", term)), "w", encoding="utf-8").write("\n".join(out))

print("done")
