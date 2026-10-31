"""Export the Steam thumbnail and copy unmodified game screenshots.

The illustrated originals are generated separately; see image-prompts.md.
"""
from pathlib import Path
import shutil
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

# Steam's small cover needs a separate export from the full-resolution artwork.
with Image.open(OUT / "cover.png") as original:
    thumbnail = original.convert("RGB")
    thumbnail.thumbnail((195, 195), Image.Resampling.LANCZOS)
    thumbnail.save(OUT / "cover-195.png")

for filename in ("gameplay-ru.jpg", "options-ru.png"):
    shutil.copyfile(ROOT.parent / "screenshots" / filename, OUT / filename)
