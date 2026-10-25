"""Write the hand-reviewed Strength lore text.

The description now wraps to ten lines at font size 22, and the entire three
line footnote stays visible in the fixed-height lore panel.
"""
import json
import os

ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"
BUDGET = 400

TEXTS = {
    "AbilityScoreInfo_Strength_LoreDesc":
        "<b><color=#FF3959>СИЛА</color></b> отражает природную мощь тела и тестостероновый склад ума. "
        "Тебе как мужчине подобает развивать тело и его возможности. Но зачем?\n\n"
        "Поиск смысла важен не меньше мастерства. К счастью, ты знаешь, за что стоишь.\n\n"
        "<b>Защищать невинных</b>. Вести слабых. Жертвовать собой, пока одни твои кости не ударятся о мостовую. "
        "Буквально <b>умереть</b>.",
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
