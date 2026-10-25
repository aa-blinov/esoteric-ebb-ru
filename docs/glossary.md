# Glossary

The frozen wording of the game. Every stage of the pipeline is bound to this
list: the bulk translation carries the terms a batch needs, the editor is told
not to replace a glossary word with a synonym, and the canonicalisation pass
gives one source line one wording.

The machine-readable form is [../src/voice/glossary.json](../src/voice/glossary.json).

## The core terms

| English | Russian |
| --- | --- |
| Alignment | Уравновешение |
| Agrarian Party | Аграрная партия |
| Agricultural Party | Аграрная партия |
| Agrarian Rural Party | Сельская аграрная партия |
| Arcane Era | Эпоха тайной магии |
| Band (geographic division) | пояс |
| Cleric | Жрец |
| Detect Alignment | Определить уравновешение |
| Constitution | Телосложение |
| Urth | Урт |
| Urthfolk | Уртфолки |
| Norvik | Норвик |
| Norvikian | Норвикийцы |
| Tolstad | Толстад |
| Freestrider | Фристрайдер |
| Greenroc | Гринрок |
| Golden Horde | Золотая Орда |
| Halfling | полурослик |
| Dwarf | дворф |
| Dwarvish | дворфский |
| Hordefolk | ордынец |
| Horde (political entity) | Орда |
| Azgal | Азгал |
| Azgalist | Азгалист |
| Azgalian | Азгалианец |
| Snell | Снелл |
| Darrow | Дарроу |
| Coinlord | Владыка монет |
| Jor | Джор |
| Interband | межпоясный |
| Clanlands Deal | Соглашение о Кланлендсе |
| Sageleaf | Сагелист |
| Kraaid | Крааид |
| Ettir | Эттир |
| Visken | Вискен |
| Modissa | Модисса |
| Gorm | Горм |
| Waterlane | Водный путь |
| Arcanist | Арканист |
| Urthguard | Уртгард |
| Undercoast | Подбережье |
| Vourgeni | Вургени |
| Askan | Аскан |
| Askanii | Аскании |
| String | Струна |
| Post | Почта |
| Postwar Era | Послевоенная эпоха |
| Hedonists | Гедонисты |
| Patriarchs | Патриархи |
| Simii | Симий |
| Divinii Torum | Дивинии Торум |
| Gate Era | Эпоха Врат |
| Golden Horde | Золотая Орда |
| Reeds | Тростники |
| Fordnip | Форднип |
| Torna | Торна |
| Akzel | Акзел |
| Pinja | Пиндзя |
| Meek | Смиренный |
| Olzis | Ользис |
| Rixbiter | Риксбайтер |
| Alfoz | Альфос |
| Snurre | Снурре |

## Context and chronology

| Source phrase | Meaning in the game | Russian |
| --- | --- | --- |
| `Band` | одно из восьми географических делений | пояс |
| `band-aid` | устойчивое выражение | временная мера |
| `band together` | устойчивое выражение | сплотиться |
| `band-thing` | музыкальная группа | музыкальная группа |
| `a band of human refugees` | группа людей | группа человеческих беженцев |
| `band of unhappy dwarves` | группа дворфов | группа недовольных дворфов |
| `band of dwarves` | группа дворфов | группа дворфов |
| `band into chaos` | компания спутников | компанию в хаос |
| `iron band` | кольцо из железа | железное кольцо |
| `a horde of strange mimics` | множество существ | толпа странных мимиков |

По официальному описанию разработчика, игра начинается за пять дней до первых выборов в Норвике: Жреца отправляют расследовать взрыв чайной. Действие проходит на неделе выборов. Решения игрока влияют на судьбу Жреца и его отношения с фракциями; сам игрок обладает голосом обычного избирателя.

В повествовании даты указываются с полным названием эпохи. На коротких датных плашках `ПЭ` означает Послевоенную эпоху. По игровым записям, Эпоха тайной магии длилась 511 лет и завершилась за 27 лет до событий игры. Война на побережье началась в 398-м и закончилась в 481-м году этой эпохи, то есть завершилась за 57 лет до событий игры. В пророчестве «half myriad» означает пять тысяч лет; это число подтверждает официальный китайский текст той же строки.

## How a term is chosen

- A name that has a Russian form in the community translation keeps it.
- A made-up name is transliterated, in the same way everywhere, and the
  forms are grouped by stem so that singular and plural cannot drift apart.
- A game term is translated once and then left alone. The codex entries
  are translated first, for exactly this reason.

## The counts

| Set | Entries |
| --- | --- |
| Codex terms | 662 |
| Proper names | 1182 |
| Context notes | 9 |
| Total | 1853 |
