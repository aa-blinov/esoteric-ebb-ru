import csv
import json
import os
import re

ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"
T = os.path.join(ROOT, "translation", "Russian")
OUT = os.path.join(ROOT, "tests", "allowed_latin.json")

SPECIAL = re.compile(r"<[^>]*>|\{[^{}]*\}")
WORD = re.compile(r"[^\W_]+", re.UNICODE)
ASCII = re.compile(r"^[A-Za-z][A-Za-z'\-]*$")
CYR = re.compile(r"[А-Яа-яЁё]")

words = {}
for fn in sorted(os.listdir(T)):
    if not fn.endswith(".csv"):
        continue
    for row in list(csv.reader(open(os.path.join(T, fn), encoding="utf-8-sig", newline="")))[1:]:
        cell = row[-1]
        if not cell or not CYR.search(cell):
            continue
        for tok in WORD.findall(SPECIAL.sub(" ", cell)):
            if ASCII.match(tok):
                words[tok.lower()] = words.get(tok.lower(), 0) + 1

# the words of the game: its organisations, its creatures, its titles, its keys
groups = {
    "organisations and offices": [
        "aefa", "aff", "cividix", "dip", "gsp", "lr", "nda", "dls", "nmbt",
        "pcg", "rf", "vk", "cbs", "flm", "ppg", "mhr", "hwbt", "ais",
    ],
    "creatures, spells and titles": [
        "umbrameexus", "felgentior", "magnum", "arcanus", "mitt", "ym", "giant",
        "carpe", "tenebras", "faux", "pas", "prôv", "torch", "nearly", "lady",
        "esoteric", "ebb", "act", "scene", "vii", "interlude", "let", "the",
        "chains", "be", "dust", "averia", "serif", "rogue", "du", "grin", "larp",
        "lingua", "dominans", "maior", "quam", "ullus", "rex", "vox",
        "operariorum", "bellum", "classium", "manifestum", "plebeium", "chalybs",
        "ddvaerg",
    ],
    "keys, marks and single letters": [
        "d20", "d4", "d6", "d8", "d10", "d12", "xp", "x", "c", "l", "r", "t",
        "s", "f", "i", "w", "q", "e", "g", "b", "n", "k", "v", "y", "z", "h", "j",
        "m", "p", "u", "a", "d", "o", "shift", "she", "it", "pc", "np", "ui",
        "hp", "mp", "dnd", "tv", "id", "dlc", "sdk", "api", "www", "http",
        "https", "com", "org", "steam", "lol", "rpg", "fps", "qa", "fqa", "fc",
        "co", "ahplc", "ost", "vol", "ii", "pe", "ro", "ar",
    ],
}

allowed = set()
for group in groups.values():
    allowed.update(group)

found = sorted(w for w in words if w not in allowed)
print("ascii words in the corpus: %d, not on the list: %s" % (len(words), found))

payload = {"note": "Latin words the game keeps in its own script, and the words "
                   "of the world's other languages.",
           "groups": groups}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=1)
print("wrote", OUT)
