"""The lore panel on the character screen is fixed height, and the pink notice
band is drawn over its last line. The Strength lore is the longest of the six
by a wide margin, and in Russian it runs two lines over the box.
"""
import json
import os

ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"
BUDGET = 375

TEXTS = {
    "AbilityScoreInfo_Strength_LoreDesc":
        "<b><color=#FF3959>СИЛА</color></b> отражает телесную мощь и мышление, "
        "напичканное тестостероном. Будучи мужчиной, ты считаешь должным совершенствовать "
        "тело. Но зачем?\n\n"
        "Поиск смысла не менее важен, чем тяга к мастерству. Ты уже знаешь своё дело.\n\n"
        "<b>Защищать невинных</b>. Вести слабых. Жертвовать собой, пока о мостовую не "
        "ударится лишь твоя кость. Буквально <b>умереть</b>.",
}


def main():
    for key, text in TEXTS.items():
        n = len(text)
        print("%-46s %d chars %s" % (key, n, "OK" if n <= BUDGET else "LONG"))
    over = {k: v for k, v in TEXTS.items() if len(v) > BUDGET}
    if over:
        raise SystemExit("over the budget")
    json.dump(TEXTS, open(os.path.join(ROOT, "work", "lore_hand.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("ok")


if __name__ == "__main__":
    main()
