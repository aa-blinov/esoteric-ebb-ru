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
| AEFA | АЭФА |
| Arcane (magic type) | Тайный |
| Arcane Era | Эпоха тайной магии |
| Band (geographic division) | пояс |
| Bugbear | Багбир |
| Cleric | Жрец |
| City Below (short place name) | Подгородье |
| The City Below the City (full place name) | Город под городом |
| Clanlands (halfling federation) | Кланленды |
| Clanlands Deal | Соглашение о Кланлендах |
| Landed Urthfolk | Уртфолки-землевладельцы |
| Detect Alignment | Определить уравновешение |
| Constitution | Телосложение |
| Urth | Урт |
| Urthfolk | Уртфолки |
| Norvik | Норвик |
| Norvikian (person) | Норвикиец |
| Norvikians | Норвикийцы |
| Tolstad | Толстад |
| Freestrider | Фристрайдер |
| Greenroc | Гринрок |
| Golden Horde | Золотая Орда |
| Halfling | полурослик |
| Halfway Bridge | Мост на полпути |
| Halfway Bridge Tribe | Племя Моста на полпути |
| Halfway-Bridge Tribe | Племя Моста на полпути |
| Halfway Tribe | племя Полпути |
| Halfways | Полпути |
| Divine (adjective) | Божественный |
| Divinity (magic pillar) | Божественность |
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
| Sageleaf | Сагелист |
| Kraaid | Крааид |
| Ettir | Эттир |
| Visken | Вискен |
| Modissa | Модисса |
| Gorm | Горм |
| Waterlane | Водный путь |
| Arcanist | Арканист |
| Urthguard | Уртгард |
| Urthguarder | Уртгардовец |
| Undercoast | Подбережье |
| Vourgeni | Вургени |
| Askan | Аскан |
| Askanii | Аскании |
| String | Струна |
| Post | Почта |
| Postwar Era | Послевоенная эпоха |
| Primal (magic type) | Праймл |
| Primal magic | Первобытная магия |
| Primal String | Праймл-Струна |
| Hedonists | Гедонисты |
| Patriarchs | Патриархи |
| Simii | Симий |
| Divinii Torum | Дивинии Торум |
| Gate | Врата |
| Gate Era | Эпоха Врат |
| Gate of Jor | Врата Джора |
| Gate War | Война врат |
| Gates | Врата |
| High-Corporation | Крупная корпорация |
| High-Corporations | Крупные корпорации |
| Golden Horde | Золотая Орда |
| Reeds | Тростники |
| Fordnip | Форднип |
| Torna | Торна |
| Akzel | Акзел |
| Pinja | Пиндзя |
| Meek | Смиренный |
| Necklace of Fireballs | Ожерелье огненных шаров |
| NOF (item abbreviation) | ООШ |
| Olzis | Ользис |
| Rixbiter | Риксбайтер |
| Alfoz | Альфос |
| Snurre | Снурре |

Краткая форма `City Below` — «Подгородье»; полное название `The City Below the City` — «Город под городом». В подписи локации используется краткая форма, а в полном названии и описаниях — полная.

В загадке сфинкса три заглавных слова называют типы магии: `Arcane` — «тайный», `Primal` — «Праймл», `Divine` — «божественный». Сочетание `Primal String` закреплено как «Праймл-Струна»; название столпа магии `Divinity` передаётся существительным «Божественность».

## Character classes and creature names

| English source term | Russian |
| --- | --- |
| Barbarian | Варвар |
| Bard | Бард |
| Cleric | Жрец |
| Druid | Друид |
| Fighter | Боец |
| Mimic | Мимик |
| Mimics | Мимики |
| Paladin | Паладин |
| Ranger | Следопыт |
| Rogue | Плут |
| Rogue paladin | Паладин-отступник |
| Rogue sorcerer | Чародей-отступник |
| Rogue spellcaster | Маг-отступник |
| Rogue wizard | Волшебник-отступник |
| Sorcerer | Чародей |
| Warlock | Колдун |
| Wizard | Волшебник |

Названия классов в репликах склоняются по падежу и согласуются с полом персонажа: например, «колдуну», «колдунья», «чародейкой». Название класса передаётся как «Плут». Сочетание «маг-отступник» обозначает мага вне закона, а не класс «Плут». Если речь идёт о представителе другого класса, слово «отступник» ставится после названия класса: «паладин-отступник».

Название Кланлендов употребляется во множественном числе и склоняется: Кланленды, Кланлендов, Кланлендам, Кланлендами, о Кланлендах. Сокращение «ООШ» образовано от «Ожерелья огненных шаров» и не склоняется.

Имя Симий склоняется: Симий, Симия, Симию, Симием, о Симии. «Багбир» — название вида; нормативные формы: багбира, багбиру, багбиром, багбиры.

Имя Урт мужское: Урт, Урта, Урту, Уртом, об Урте. В повести об Иллим Урт назван мужчиной, а эльфийская богиня и её гнев относятся к Иллим. Название ордена «Уртгард» склоняется: Уртгард, Уртгарда, Уртгарду, Уртгардом, об Уртгарде. Член ордена называется «уртгардовец»: уртгардовец, уртгардовца, уртгардовцу, уртгардовцем, об уртгардовце; уртгардовцы, уртгардовцев, уртгардовцам, уртгардовцами, об уртгардовцах. «Уртфолк» склоняется: уртфолк, уртфолка, уртфолку, уртфолком, об уртфолке; уртфолки, уртфолков, уртфолкам, уртфолками, об уртфолках. «Уртфолки-землевладельцы» обозначает сословие. В винительном падеже имя бога принимает форму «Урта»: «встретить Урта», «воскресить Урта», «за Урта»; после «через» также нужно «Урта», а в предложном падеже — «об Урте». При обращении сохраняется форма «Урт».

Норвик склоняется: Норвик, Норвика, Норвику, Норвиком, о Норвике. Норвикиец склоняется: норвикиец, норвикийца, норвикийцу, норвикийцем, о норвикийце; норвикийцы, норвикийцев, норвикийцам, норвикийцами, о норвикийцах. Прилагательное имеет формы норвикийский, норвикийская, норвикийское и далее по роду, числу и падежу.

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
