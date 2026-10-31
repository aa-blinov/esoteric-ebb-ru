"""Build installation diagrams; game screenshots remain unmodified."""
from pathlib import Path
import shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)
FONT_PATHS = (
    Path("C:/Windows/Fonts/segoeui.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
)
FONT = next((p for p in FONT_PATHS if p.is_file()), None)
if FONT is None:
    raise SystemExit("Install Segoe UI or DejaVu Sans to render Cyrillic")

BG, PANEL, FG, MUTED, ACCENT = "#071920", "#102e38", "#e6eedb", "#a5c3c6", "#f3a64b"


def text(draw, xy, value, size=23, fill=FG):
    font = ImageFont.truetype(str(FONT), size)
    box = draw.textbbox(xy, value, font=font)
    if box[2] > draw.im.size[0] - 12 or box[3] > draw.im.size[1] - 12:
        raise ValueError(f"Text exceeds canvas: {value}")
    draw.text(xy, value, font=font, fill=fill)


def card(filename, number, title, lines, footer):
    canvas = Image.new("RGB", (638, 380), BG)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((20, 20, 618, 360), radius=18, fill=PANEL)
    text(draw, (40, 32), f"{number} / {title}", 29, ACCENT)
    for index, line in enumerate(lines):
        text(draw, (40, 100 + index * 40), line)
    text(draw, (40, 316), footer, 17, MUTED)
    canvas.save(OUT / filename)


card("01-beta.png", "01", "Выберите ветку Steam", [
    "Библиотека → Esoteric Ebb → Свойства",
    "Бета-версии / Game Versions & Betas",
    "Localization Branch",
    "Дождитесь окончания обновления",
], "Схема установки. Названия в клиенте могут отличаться.")
card("02-download.png", "02", "Скачайте архив перевода", [
    "GitHub → Releases → последний релиз",
    "Откройте список Assets",
    "esoteric-ebb-ru-v1.0.2.zip",
    "Внутри: Russian / 12 CSV-файлов",
], "Схема установки. Source code для установки не нужен.")
card("03-folders.png", "03", "Перенесите папку Russian", [
    "Папка игры / Esoteric Ebb_Data /",
    "StreamingAssets / Localization /",
    "    Official /",
    "    Russian / UIElements.csv  (+ ещё 11 CSV)",
], "Схема папок. Переносите Russian из ZIP в Localization.")

cover = Image.new("RGB", (195, 195), BG)
d = ImageDraw.Draw(cover)
d.rounded_rectangle((7, 7, 187, 187), radius=16, outline=ACCENT, width=3)
text(d, (20, 31), "ESOTERICA", 25, ACCENT)
text(d, (20, 81), "РУССКИЙ", 27)
text(d, (20, 117), "ПЕРЕВОД", 27)
cover.save(OUT / "cover-195.png")

for filename in ("gameplay-ru.jpg", "options-ru.png"):
    shutil.copyfile(ROOT.parent / "screenshots" / filename, OUT / filename)
