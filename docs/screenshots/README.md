# Screenshots

The game in Russian, taken from the build in this repository.

| File | What it shows |
| --- | --- |
| `menu-ru.png` | The main menu. The menu reads «Новая игра», «Загрузка», «Настройки», «Авторы», «Выход», and the card on the right holds the saved game. |
| `options-ru.png` | The options screen: the language row, the limits of the saves, the dialogue size, the dialogue font, the interface size. |
| `character-ru.png` | The character sheet: the lore panel, the tabs, and the list of the abilities with the mark of proficiency. |
| `dialogue-ru.png` | The panel of the language in the dialogue font. This is the font that carries 76,401 lines of dialogue, and it holds the full Cyrillic range. |

## The dialogue fonts

The game lists seven. Two of them, Ebberia and Josefin Sans, carry no Cyrillic
at all, so a Russian player picks Ubuntu, EB Garamond, PT Serif, Roboto or
Open Dyslexic in the options. The game says so on the screen itself; the
screenshot shows the list.

The lore panel is a fixed box, 541 px wide. A Russian line that does not fit
it wraps and lands on the next block. The measurements behind the fix are in
[../layout.md](../layout.md).
