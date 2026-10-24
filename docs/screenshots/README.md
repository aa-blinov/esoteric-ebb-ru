# Screenshots

The game in Russian, taken from the build in this repository.

| File | What it shows |
| --- | --- |
| `menu-ru.png` | The main menu. The menu reads «Новая игра», «Нагрузка», «Настройки», «Авторы», «Выход». |
| `options-ru.png` | The options screen: the language row, the dialogue size, the dialogue fonts, the interface size. |
| `character-ru.png` | The character sheet: the abilities, the lore panel, the class choice. |
| `dialogue-ru.png` | The language panel in the dialogue font. This is the font that carries 76,401 lines of dialogue, and it holds the full Cyrillic range. |

## The dialogue fonts

The game lists seven. Two of them, Ebberia and Josefin Sans, carry no Cyrillic
at all, so a Russian player picks EB Garamond or PT Serif in the options. The
game says so on the screen itself; the screenshot shows the list.

The lore panel is a fixed box, 541 px wide. A Russian line that does not fit
it wraps and lands on the next block. The measurements behind the fix are in
[../layout.md](../layout.md).
