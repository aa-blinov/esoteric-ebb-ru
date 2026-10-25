#!/usr/bin/env python
"""Measure the real rendered width of the lore-panel strings in the game's own fonts.

Extracts the real TrueType data of the UI fonts from the Unity assets and
computes advance widths the way TextMeshPro does (advance / unitsPerEm * size).
"""
from __future__ import annotations

import io
import os

import UnityPy
from fontTools.ttLib import TTFont

DATA = os.path.join(os.environ.get(
    "EB_GAME_DIR",
    r"C:\Program Files (x86)\Steam\steamapps\common\Esoteric Ebb"),
    "Esoteric Ebb_Data")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "work", "fonts")
os.makedirs(OUT, exist_ok=True)

PANEL_PX = 500.0
USES_TEXT_PX = 325.0


def extract_fonts():
    found = {}
    for name in ("sharedassets0.assets", "resources.assets"):
        path = os.path.join(DATA, name)
        if not os.path.exists(path):
            continue
        env = UnityPy.load(path)
        for obj in env.objects:
            if obj.type.name != "Font":
                continue
            try:
                f = obj.read()
                fname = getattr(f, "m_Name", "?")
                data = None
                for attr in ("m_FontData", "font"):
                    v = getattr(f, attr, None)
                    if isinstance(v, (bytes, bytearray)) and len(v) > 2000:
                        data = bytes(v)
                        break
                    if isinstance(v, list) and v and all(isinstance(x, int) for x in v[:8]):
                        data = bytes(v)
                        break
                if data:
                    found[fname] = data
            except Exception:
                continue
    return found


def measure(tt_bytes, text, size):
    tt = TTFont(io.BytesIO(tt_bytes), fontNumber=0, lazy=True)
    upem = tt["head"].unitsPerEm
    cmap = tt.getBestCmap()
    hmtx = tt["hmtx"]
    total = 0
    missing = []
    for ch in text:
        cp = ord(ch)
        gname = cmap.get(cp)
        if gname is None:
            missing.append(ch)
            continue
        adv = hmtx[gname][0]
        total += adv
    tt.close()
    return (total / upem) * size, missing


def main():
    fonts = extract_fonts()
    print("fonts extracted:", len(fonts))
    for k, v in sorted(fonts.items()):
        print("  %-32s %d bytes" % (k, len(v)))

    # the lore panel display font candidates
    cases = [
        ("EXTRA ITEMS", 45, "AbilityScoreInfo_Strength_Uses1"),
        ("ДОПОЛНИТЕЛЬНЫЕ ПРЕДМЕТЫ", 45, "AbilityScoreInfo_Strength_Uses1 (old RU)"),
        ("ЛИШНИЕ ПРЕДМЕТЫ", 45, "AbilityScoreInfo_Strength_Uses1 (new RU)"),
        ("Higher Strength", 38, "Uses1"),
        ("Большая Сила", 38, "Uses1"),
        ("Высокая Харизма", 20, "Charisma Uses1 heading; 325 px text slot"),
        ("сразу получаешь", 22, "Charisma Uses1 body; 325 px text slot"),
        ("СКИДКУ", 48, "Charisma Uses1 highlight; 325 px text slot"),
        ("в некоторых лавках", 18, "Charisma Uses1 note; 325 px text slot"),
    ]

    out = ["panel usable width: %.0f px" % PANEL_PX, ""]
    for fname, data in sorted(fonts.items()):
        try:
            tt = TTFont(io.BytesIO(data), fontNumber=0, lazy=True)
            fam = tt["name"].getDebugName(1)
            tt.close()
        except Exception:
            fam = "?"
        out.append("--- font %s (%s) ---" % (fname, fam))
        for text, size, label in cases:
            try:
                w, missing = measure(data, text, size)
            except Exception as e:
                out.append("    %-28s error %s" % (text, e))
                continue
            limit = USES_TEXT_PX if "325 px text slot" in label else PANEL_PX
            mark = "OK " if w <= limit else "OVER"
            out.append("    [%s] %-30s size=%-3d  ~%6.0f px  %s"
                       % (mark, text, size, w, label))
            if missing:
                out.append("        missing glyphs: %s" % "".join(missing))
        out.append("")

    open(os.path.join(OUT, "width_measure.txt"), "w", encoding="utf-8").write("\n".join(out))
    print("\nwritten fonts/width_measure.txt")


if __name__ == "__main__":
    main()
