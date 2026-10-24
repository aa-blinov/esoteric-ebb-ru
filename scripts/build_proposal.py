"""Build the correction proposal: the systematic term fixes and the review's findings."""
import csv
import json
import os
import re

GAME = os.environ.get("EB_GAME_DIR", r"M:\SteamLibrary\steamapps\common\Esoteric Ebb")
ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"
base = os.path.join(GAME, "Esoteric Ebb_Data", "StreamingAssets", "Localization")

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
        pairs.append({"file": fn, "key": r[0], "en": en, "ru": ru.get(r[0], "")})

json.dump(pairs, open(os.path.join(ROOT, "work", "all_pairs.json"), "w", encoding="utf-8"),
          ensure_ascii=False)

proposals = {}

# --- the systematic ones -----------------------------------------------------
for p in pairs:
    en, ru = p["en"], p["ru"]
    if not en or not ru:
        continue
    new = ru
    # Constitution, the ability: "Устав" is a statute, not a physique
    if re.search(r"\bConstitution\b", en) and "Устав" in ru and "Телосложение" not in ru:
        new = re.sub(r"\bУстав\w*", lambda m: "Телосложение" + m.group(0)[5:], new)
    # Lawful, the alignment: "Законный" is a noun
    if re.search(r"\bLawful\b", en) and "Законный" in ru:
        new = new.replace("Законный", "Законопослушный")
    # warlock is the pact-maker; in Russian that is "колдун", while
    # "чародей" is the sorcerer
    if re.search(r"\bwarlock\b", en, re.I) and re.search(r"[Чч]ародей", ru):
        new = re.sub(r"[Чч]ародей\w*", lambda m: ("Колдун" if m.group(0)[0].isupper() else "колдун") + m.group(0)[7:], new)
    if new != ru:
        proposals[(p["file"], p["key"])] = {"ru": new, "why": "terminology"}

# --- the review's findings ---------------------------------------------------
review = json.load(open(os.path.join(ROOT, "work", "label_review.json"), encoding="utf-8"))
for key, item in review.items():
    hit = next((p for p in pairs if p["key"] == key), None)
    if not hit:
        continue
    proposals.setdefault((hit["file"], key), {})["ru"] = item["ru"]
    proposals[(hit["file"], key)]["why"] = proposals[(hit["file"], key)].get("why", "") + " | review: " + item.get("why", "")

lines = ["%s | %s" % (f, k) for (f, k) in sorted(proposals)]
out = []
for (f, k) in sorted(proposals):
    p = next(p for p in pairs if p["file"] == f and p["key"] == k)
    out.append("%s | %s" % (f, k))
    out.append("   EN: %s" % p["en"][:100].replace("\n", " "))
    out.append("   RU: %s" % p["ru"][:100].replace("\n", " "))
    out.append("   →  %s" % proposals[(f, k)]["ru"][:100].replace("\n", " "))
    out.append("      %s" % proposals[(f, k)]["why"][:110])
    out.append("")
open(os.path.join(ROOT, "work", "proposal.txt"), "w", encoding="utf-8").write("\n".join(out))
json.dump({"%s|%s" % (f, k): v for (f, k), v in proposals.items()},
          open(os.path.join(ROOT, "work", "proposal.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("proposals:", len(proposals))
