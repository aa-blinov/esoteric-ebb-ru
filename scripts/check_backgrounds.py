"""The background description box is fixed height, with the ability badges
drawn over its last line. The English fits by design; the Russian has to be
shorter to fit the same four lines.
"""
import csv
import json
import os

GAME = os.environ.get("EB_GAME_DIR", r"M:\SteamLibrary\steamapps\common\Esoteric Ebb")
ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"
base = os.path.join(GAME, "Esoteric Ebb_Data", "StreamingAssets", "Localization")

out = []
for fn in ("MiscTexts.csv", "Dialogs.csv", "SheetInfo.csv", "UIElements.csv", "QuestPoints.csv"):
    with open(os.path.join(base, "Official", fn), encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.reader(fh))
    idx = next((i for i, h in enumerate(rows[0]) if h.strip() == "EN"), None)
    if idx is None:
        continue
    off = {r[0]: (r[idx] if len(r) > idx else "") for r in rows[1:] if r}
    with open(os.path.join(base, "Russian", fn), encoding="utf-8-sig", newline="") as fh:
        ru = {r[0]: r[-1] for r in list(csv.reader(fh))[1:] if r}
    for k, en in off.items():
        if not k.startswith("PCBackground_") or not k.endswith("_desc"):
            continue
        r = ru.get(k, "")
        out.append({"file": fn, "key": k, "en": en, "ru": r,
                    "en_len": len(en), "ru_len": len(r),
                    "ratio": round(len(r) / max(1, len(en)), 2)})

out.sort(key=lambda x: -x["ratio"])
lines = ["%-46s %5s %5s %6s" % ("key", "EN", "RU", "ratio")]
for o in out:
    lines.append("%-46s %5d %5d %6.2f" % (o["key"], o["en_len"], o["ru_len"], o["ratio"]))
over = [o for o in out if o["ratio"] > 0.85]
lines.append("")
lines.append("over the 0.85 budget: %d of %d" % (len(over), len(out)))
lines.append("")
for o in over:
    lines.append("%s  (EN %d / RU %d)" % (o["key"], o["en_len"], o["ru_len"]))
    lines.append("   EN: %s" % o["en"])
    lines.append("   RU: %s" % o["ru"])
    lines.append("")

open(os.path.join(ROOT, "work", "backgrounds.txt"), "w", encoding="utf-8").write("\n".join(lines))
json.dump(out, open(os.path.join(ROOT, "work", "backgrounds.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("backgrounds:", len(out), " over budget:", len(over))
