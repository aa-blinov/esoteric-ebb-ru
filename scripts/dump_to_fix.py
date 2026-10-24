import csv
import json
import os

ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"
GAME = os.environ.get("EB_GAME_DIR", r"M:\SteamLibrary\steamapps\common\Esoteric Ebb")
OFF = os.path.join(GAME, "Esoteric Ebb_Data", "StreamingAssets", "Localization", "Official")
RU = os.path.join(ROOT, "translation", "Russian")

KEYS = {
    "Dialogs.csv": ["CB_Kraaid_682", "Enc_Below_168", "Enc_Below_236", "EP_Rix_Lisa_141",
                    "EP_Rollo_Arn_122", "EP_Snell_401", "Ettir_Companion_130", "GG_Miska_1249",
                    "GG_Nessan_325", "GG_Nessan_612", "GT_Bedroll_46", "GT_Bedroll_49",
                    "GT_Calendar_98", "OP_EverGlad_188", "OP_EverGlad_940", "OP_EverGlad_942",
                    "Q_Gate_124", "Q_Riddle_106", "Q_Youth_241", "SO_Literature_28",
                    "SO_Snurre_1609", "TE_Booths_80", "TE_Counter_177", "TE_Pinja_405",
                    "TE_Rubble_63", "TS_Alfoz_187", "TS_Arn_Kiosk_588", "TS_Arn_Kiosk_709",
                    "TS_Braxo_385", "TS_FlowerYard_29", "TS_ImposingTree_103", "TS_Kull_467",
                    "TS_Nearly_529", "TS_Oyu_313", "TS_TeaShopDoor_4"],
    "Glossary.csv": ["Glossary_Response_203", "Glossary_Response_257", "Glossary_Response_648",
                      "Glossary_Response_690"],
    "SheetInfo.csv": ["IP_FREY_15"],
    "SpellTexts.csv": ["SpellDescription_15"],
}

out = []
for fn, keys in KEYS.items():
    en_rows = {r[0]: r for r in list(csv.reader(open(os.path.join(OFF, fn), encoding="utf-8-sig", newline="")))[1:]}
    ru_rows = {r[0]: r for r in list(csv.reader(open(os.path.join(RU, fn), encoding="utf-8-sig", newline="")))[1:]}
    for key in keys:
        en = en_rows.get(key)
        ru = ru_rows.get(key)
        out.append("%s | %s" % (fn, key))
        out.append("  EN: %s" % (en[4] if en and len(en) > 4 else ""))
        out.append("  RU: %s" % (ru[-1] if ru else ""))
        out.append("")

open(os.path.join(ROOT, "work", "to_fix.txt"), "w", encoding="utf-8").write("\n".join(out))
print("written work/to_fix.txt")
