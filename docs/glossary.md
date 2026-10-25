# Glossary

The frozen wording of the game. Every stage of the pipeline is bound to this
list: the bulk translation carries the terms a batch needs, the editor is told
not to replace a glossary word with a synonym, and the canonicalisation pass
gives one source line one wording.

The machine-readable form is [../src/voice/glossary.json](../src/voice/glossary.json).

## The core terms

| English | Russian |
| --- | --- |
| Cleric | Жрец |
| Constitution | Телосложение |
| Urth | Урт |
| Urthfolk | Уртфолки |
| Norvik | Норвик |
| Norvikian | Норвикийцы |
| Tolstad | Толстад |
| Freestrider | Фристрайдер |
| Azgal | Азгал |
| Azgalist | Азгалист |
| Azgalian | Азгалианец |
| Snell | Снелл |
| Darrow | Дарроу |
| Coinlord | Владыка монет |
| Jor | Джор |
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
| Hedonists | Гедонисты |
| Patriarchs | Патриархи |
| Simii | Симий |
| Divinii Torum | Дивинии Торум |
| Gate Era | Эпоха Врат |
| Golden Horde | Золотая орда |
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

## How a term is chosen

- A name that has a Russian form in the community translation keeps it.
- A made-up name is transliterated, in the same way everywhere, and the
  forms are grouped by stem so that singular and plural cannot drift apart.
- A game term is translated once and then left alone. The codex entries
  are translated first, for exactly this reason.

## The counts

| Set | Entries |
| --- | --- |
| Codex terms | 660 |
| Proper names | 1178 |
| Total | 1838 |
