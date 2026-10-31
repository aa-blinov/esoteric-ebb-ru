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

BG, FG, MUTED, ACCENT = "#f0ecdF", "#222b27", "#677064", "#b64c2a"


def text(draw, xy, value, size=23, fill=FG):
    font = ImageFont.truetype(str(FONT), size)
    box = draw.textbbox(xy, value, font=font)
    if box[2] > draw.im.size[0] - 12 or box[3] > draw.im.size[1] - 12:
        raise ValueError(f"Text exceeds canvas: {value}")
    draw.text(xy, value, font=font, fill=fill)


def sheet(number, title, subtitle):
    canvas = Image.new("RGB", (638, 420), BG)
    draw = ImageDraw.Draw(canvas)
    text(draw, (28, 17), number, 66, ACCENT)
    text(draw, (128, 34), title, 29)
    text(draw, (130, 78), subtitle, 17, MUTED)
    draw.line((30, 114, 608, 114), fill=FG, width=1)
    text(draw, (30, 388), "ESOTERICA  /  УСТАНОВКА ПЕРЕВОДА", 12, MUTED)
    text(draw, (496, 388), "СХЕМА", 12, MUTED)
    return canvas, draw


im, d = sheet("01", "Включите локализацию", "STEAM / СВОЙСТВА ИГРЫ")
for y, marker, label in [(143, "1", "Библиотека → Esoteric Ebb"),
                         (193, "2", "Свойства → Бета-версии"),
                         (243, "3", "Localization Branch")]:
    text(d, (36, y+2), marker, 19, ACCENT)
    text(d, (78, y), label, 27)
text(d, (78, 306), "Дождитесь обновления игры.", 20)
text(d, (78, 340), "Раздел также называется Game Versions & Betas.", 16, MUTED)
im.save(OUT / "01-beta.png")

im, d = sheet("02", "Скачайте ZIP перевода", "GITHUB / RELEASES / ASSETS")
# A file outline identifies the archive without imitating a browser window.
d.line([(38, 150), (88, 150), (111, 173), (111, 246), (38, 246), (38, 150)], fill=FG, width=2)
d.line([(88, 150), (88, 173), (111, 173)], fill=FG, width=2)
text(d, (47, 194), "ZIP", 23, ACCENT)
text(d, (139, 147), "esoteric-ebb-ru-v1.0.2.zip", 28)
text(d, (139, 194), "Внутри папка Russian", 23)
text(d, (139, 232), "и 12 файлов перевода.", 23)
d.line((30, 291, 608, 291), fill=MUTED, width=1)
text(d, (38, 311), "Source code .zip / .tar.gz", 22, MUTED)
text(d, (38, 345), "Эти архивы для установки не нужны.", 18, MUTED)
im.save(OUT / "02-download.png")

im, d = sheet("03", "Перенесите Russian", "ИЗ СКАЧАННОГО ZIP В ПАПКУ ИГРЫ")
text(d, (38, 137), "Esoteric Ebb_Data", 24)
d.line((49, 176, 49, 198, 72, 198), fill=MUTED, width=1)
text(d, (82, 180), "StreamingAssets", 24)
d.line((94, 220, 94, 242, 117, 242), fill=MUTED, width=1)
text(d, (127, 224), "Localization", 24)
d.line((139, 265, 139, 327), fill=MUTED, width=1)
d.line((139, 283, 161, 283), fill=MUTED, width=1)
d.line((139, 327, 161, 327), fill=ACCENT, width=2)
text(d, (172, 266), "Official", 24, MUTED)
text(d, (172, 309), "Russian", 26, ACCENT)
text(d, (287, 315), "← папку из ZIP сюда", 20, ACCENT)
im.save(OUT / "03-folders.png")

cover = Image.new("RGB", (195, 195), BG)
d = ImageDraw.Draw(cover)
text(d, (15, 9), "ESOTERICA", 21)
d.line((16, 44, 179, 44), fill=FG, width=1)
text(d, (10, 37), "RU", 94, ACCENT)
text(d, (17, 151), "РУССКИЙ ПЕРЕВОД", 16)
cover.save(OUT / "cover-195.png")

for filename in ("gameplay-ru.jpg", "options-ru.png"):
    shutil.copyfile(ROOT.parent / "screenshots" / filename, OUT / filename)
