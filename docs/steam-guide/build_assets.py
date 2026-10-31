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

# The guide editor rejects individual images above 2 MB, even in an 8 MB batch.
UPLOAD = OUT / "steam"
UPLOAD.mkdir(exist_ok=True)
for stem in ("01-beta", "02-download", "03-folders"):
    with Image.open(OUT / f"{stem}.png") as original:
        original.convert("RGB").save(
            UPLOAD / f"{stem}.jpg", quality=94, optimize=True, subsampling=0
        )
for filename in ("gameplay-ru.jpg", "options-ru.png"):
    shutil.copyfile(OUT / filename, UPLOAD / filename)
for path in UPLOAD.iterdir():
    if path.stat().st_size > 2_000_000:
        raise ValueError(f"Steam upload exceeds 2 MB: {path.name}")
