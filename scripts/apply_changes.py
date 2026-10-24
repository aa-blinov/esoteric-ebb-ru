"""Apply the terminology fixes and the reviewed label corrections.

The reviewer's findings are applied except where they are a matter of taste
rather than an error: the game capitalises its ability names, the potion
"Pot" is a cauldron in this game's alchemy, and a few one-word titles were
already right. The skip list below names each of those.
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"
sys.path.insert(0, os.path.join(ROOT, "src", "ebru"))
from llm_client import extract_json_array  # noqa: E402

WORK = os.path.join(ROOT, "work")

# keys the review flagged but the translation is right
SKIP = {
    "ItemName_29",            # Pot: a cauldron in this game's alchemy
    "ItemName_62",            # Boots of Elvenkind: "эльфийская кровь" is fine
    "ItemName_71",            # Movable Rod: "подвижный" is fine
    "ItemName_75",            # Tiny Dictator: the capital matches the neighbours
    "ItemName_82",            # Hex Weekly: fine as it stands
    "ItemName_91",            # The Undercommon: a proper name, do not invent one
    "ItemVarModDesc_47",      # Отклонений: the category names are capitalised
    "ItemVarModDesc_51",      # fine
    "ItemVarModDesc_59",      # fine
    "ItemVarModDesc_61",      # дворфов is correct
    "Boon_Consitution",       # КРЕПКИЙ is fine
    "BlockMessage_Barkskin",  # кора дерева is a fine description of the spell
    "Boon_Name_0",            # хиты: the term the game uses
    "Boon_Name_8",            # хиты: the term the game uses
    "Check",                  # проверка: the term of the system
    "Area_PC",                # a place name
    "Area_RM",                # a place name
    "Area_UP",                # fine
    "BG_ALFOZ_3",             # Master: the game says "Мастер Альфоса"
    "BG_ARN_1",               # детский рабочий is the established phrase
    "BG_EVER_18",             # Trifler: ambiguous
    "BG_FREY_5",              # Noble: дворянин is right
    "FEAT_LEYLINE_CHA",       # магическая линия is the game's term
    "FEAT_LICH_INT",          # "Почти личдом" matches the neighbouring naming
    "FEAT_MUSH_DEX",          # fine
    "FEAT_PRINT_INT",         # fine
    "FEAT_UNITY_WIS",         # fine
    "Choice_VOICE_Nat20",     # fine
    "Choice_WEAL_Fail",       # fine
    "BadEnding_Books_1",      # the title case follows the English
    "BadEnding_Finger_1",     # the title case follows the English
    "BadEnding_Gel_1",        # fine
    "BadEnding_Genocide_1",   # the colour tag has to stay where it is
    "BadEnding_Gorm_1",       # the title case follows the English
    "BadEnding_Roper_1",      # the name follows the glossary
    "BadEnding_Skeleton_1",   # the title case follows the English
    "BadEnding_Well_2",       # fine
    "AbilityScoreInfo_Charisma_RoleLow_Title",   # the ability is Харизма
    "AbilityScoreInfo_Charisma_UsesNotice",      # the ability is Харизма
    "AbilityScoreInfo_Charisma_LoreNotice",      # the ability is Харизма
    "AbilityScoreInfo_Charisma_Notice",          # the ability is Харизма
}

# the reviewer's own mistakes, corrected by hand
OVERRIDE = {
    "ItemName_11": "Садовое яблоко",
    "Bark_DS_DivineRiddle": "<shake>ОТКРЫВАЙ!</shake>",
    "AbilityScoreInfo_Wisdom_RoleLow_Point1": "Наивный дурак.",
    "AbilityScoreInfo_Charisma_RoleHigh_Point5": "Обожает контролировать людей разумом.",
    "Menu_Button_Load": "Загрузка",
}

# the reviewer's findings that only change the case of a name
CASE_ONLY = re.compile(r"^(\s*«?\w)", re.UNICODE)


def is_case_only(old, new):
    return old.lower() == new.lower()


def main():
    pairs = json.load(open(os.path.join(WORK, "all_pairs.json"), encoding="utf-8"))
    review = json.load(open(os.path.join(WORK, "label_review.json"), encoding="utf-8"))

    changes = {}
    skipped = []

    # the systematic terminology
    for p in pairs:
        en, ru = p["en"], p["ru"]
        if not en or not ru:
            continue
        new = ru
        if re.search(r"\bConstitution\b", en) and "Устав" in ru and "Телосложение" not in ru:
            new = re.sub(r"\bУстав(\w*)", lambda m: "Телосложение" + m.group(1), new)
        if re.search(r"\bLawful\b", en) and "Законный" in ru:
            new = new.replace("Законный", "Законопослушный")
        if re.search(r"\bwarlock\b", en, re.I) and re.search(r"[Чч]ародей", ru):
            new = re.sub(r"[Чч]ародей(\w*)",
                         lambda m: ("Колдун" if m.group(0)[0].isupper() else "колдун") + m.group(1), new)
        if new != ru:
            changes[(p["file"], p["key"])] = new

    # the review
    for key, item in review.items():
        hit = next((p for p in pairs if p["key"] == key), None)
        if not hit:
            continue
        if key in SKIP:
            skipped.append(key)
            continue
        old = hit["ru"]
        new = item["ru"]
        if new == old or is_case_only(old, new):
            skipped.append(key)
            continue
        if not new.strip():
            continue
        changes[(hit["file"], key)] = new

    # the hand overrides
    for key, text in OVERRIDE.items():
        hit = next((p for p in pairs if p["key"] == key), None)
        if hit:
            changes[(hit["file"], key)] = text

    print("changes: %d, skipped: %d" % (len(changes), len(skipped)))
    json.dump({"%s|%s" % (f, k): {"file": f, "key": k, "ru": v}
               for (f, k), v in changes.items()},
              open(os.path.join(WORK, "changes.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # show the ones that came from the review, for the record
    lines = []
    for (f, k), v in sorted(changes.items()):
        p = next(p for p in pairs if p["file"] == f and p["key"] == k)
        lines.append("%s | %s" % (f, k))
        lines.append("   EN: %s" % p["en"][:110].replace("\n", " "))
        lines.append("   RU: %s" % p["ru"][:110].replace("\n", " "))
        lines.append("   →  %s" % v[:110].replace("\n", " "))
        lines.append("")
    open(os.path.join(WORK, "changes.txt"), "w", encoding="utf-8").write("\n".join(lines))
    print("written work/changes.txt")


if __name__ == "__main__":
    main()
