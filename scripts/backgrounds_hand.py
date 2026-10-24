"""The background descriptions, written to fit the four lines their box holds.

Hand-written, because a model asked to compress a paragraph reliably loses
the voice before it loses the words. The budget is 130 characters: the text
area of the panel is 470 px, which holds about 38 characters a line, and the
ability badges are drawn over the fifth line.
"""
from __future__ import annotations

import json
import os

ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"
BUDGET = 130

TEXTS = {
    "PCBackground_KioskKid_desc":
        "Мать редко была дома и устроила тебя на работу после школы, чтобы не ввязывался в дурное. "
        "Ты ненавидишь запах газет.",

    "PCBackground_Acolyte_desc":
        "Умение переписывать вывело тебя к церковным обязанностям. Взят из рядовых, ты быстро "
        "показал преданность божественному городу.",

    "PCBackground_PalacePawn_desc":
        "Быстро растущий талант, ты часто оказывался среди интриг начальства, несмотря на все "
        "старания. Тебе это никогда не шло на пользу.",

    "PCBackground_RevolutionaryScribe_desc":
        "Разочарование. Город, где идеалы не соблюдаются. Ты выбрал зарождающуюся Демократию. "
        "Писал ночами ради <i>перемен и славы</i>.",

    "PCBackground_Trollkiller_desc":
        "Ты не помнишь, но хорошо знаешь, как умер отец. Иногда это воодушевляло. Иногда казалось, "
        "что достичь его невозможно.",

    "PCBackground_AzgalistActivist_desc":
        "«Друзья» вскоре показали тебе мятежное нутро Норвика. Подростком ты сеял хаос — и что "
        "хуже: <i>дворфскую пропаганду</i>.",

    "PCBackground_CrowdPleaser_desc":
        "Рано или поздно ты связался с не той компанией. Ты освоил их сленг и радикальную "
        "терминологию — лишь бы обрести настоящих друзей.",

    "PCBackground_LoreEnthusiast_desc":
        "Проводя время в одиночестве, ты часто оказывался в Библиотеке Дарроу. Странная история "
        "Царства Джора была твоим спутником.",

    "PCBackground_TowerApprentice_desc":
        "Вступление в Башни — честь для немногих. Но и страшное испытание, даже для тебя. Кто бы "
        "подумал, что лекции так выматывают?",

    "PCBackground_DeadCleric_desc":
        "Взросление в одиночестве. Неприятности. Обучение в Уртгарде. Жизнь Жрецу. Неужели всё "
        "это должно было кончиться в <i>Реке</i>?",

    "PCBackground_ArcaneProdigy_desc":
        "Впервые в жизни ты был природным дарованием. Кантрипы ты знал всегда, но настоящая магия "
        "— это было другое. Это была <i>сила</i>.",

    "PCBackground_EsotericExpert_desc":
        "Ночи напролёт ты искал эзотерическое знание. Одинокая жизнь. Твои открытия властям были "
        "не нужны, но ты не остановился. Никогда.",

    "PCBackground_AbjectApostate_desc":
        "Тебя никто не любит. Когда понизили за небрежность, никто не вступился. Но всё в порядке. "
        "Всё будет хорошо. Ты к этому привык.",

    "PCBackground_PunchingBag_desc":
        "Ты — сын фермера, выросший в городе. Конечно, ты оказался изгоем. Понадобилось время, "
        "чтобы научиться с этим справляться.",

    "PCBackground_LittleWeirdo_desc":
        "Для них ты был диковинкой: мальчик, готовый на всё ради внимания. <i>Ради одобрения</i>. "
        "Через два года ты научился этому.",
}


def main():
    for key, text in TEXTS.items():
        n = len(text)
        flag = "OK " if n <= BUDGET else "LONG"
        print("%s %-46s %d" % (flag, key, n))
    over = {k: v for k, v in TEXTS.items() if len(v) > BUDGET}
    if over:
        print("\nOVER THE BUDGET:")
        for k, v in over.items():
            print("  %s: %d" % (k, len(v)))
        raise SystemExit(1)
    json.dump(TEXTS, open(os.path.join(ROOT, "work", "backgrounds_hand.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("\nall within the budget")


if __name__ == "__main__":
    main()
