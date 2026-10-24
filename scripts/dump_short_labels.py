import csv
import os

GAME = os.environ.get("EB_GAME_DIR", r"M:\SteamLibrary\steamapps\common\Esoteric Ebb")
ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"
base = os.path.join(GAME, "Esoteric Ebb_Data", "StreamingAssets", "Localization")

out = []
for fn in ("UIElements.csv", "MiscTexts.csv", "Feats.csv", "SheetInfo.csv", "SpellTexts.csv"):
    with open(os.path.join(base, "Official", fn), encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.reader(fh))
    header = rows[0]
    try:
        en_index = next(i for i, h in enumerate(header) if h.strip() == "EN")
    except StopIteration:
        continue
    off = {r[0]: (r[en_index] if len(r) > en_index else "") for r in rows[1:] if r}
    with open(os.path.join(base, "Russian", fn), encoding="utf-8-sig", newline="") as fh:
        ru = {r[0]: r[-1] for r in list(csv.reader(fh))[1:] if r}
    for k, en in off.items():
        en = (en or "").strip()
        r = (ru.get(k) or "").strip()
        if not en or len(en) > 40:
            continue
        out.append("%-44s | %-38s | %s" % (k, en, r))

open(os.path.join(ROOT, "work", "short_labels.txt"), "w", encoding="utf-8").write("\n".join(out))
print("short labels:", len(out))
