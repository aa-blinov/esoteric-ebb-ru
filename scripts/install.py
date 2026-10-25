#!/usr/bin/env python
"""Install the finished translation into the game.

The repository stores the CSV files with LF endings; the game is on Windows,
so the installed copy gets CRLF, like the files the developer shipped.

The installer also looks at the settings file of the game. Two of the seven
dialogue fonts carry no Cyrillic at all: Ebberia (0) and Josefin Sans (2). The
game draws a Russian line in either of them as a row of runes, so the setting
is moved to Ubuntu (6), which carries the whole range.
"""
from __future__ import annotations

import io
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "translation", "Russian")
GAME = os.environ.get(
    "EB_GAME_DIR", r"C:\Program Files (x86)\Steam\steamapps\common\Esoteric Ebb")
DST = os.path.join(GAME, "Esoteric Ebb_Data", "StreamingAssets", "Localization", "Russian")
SETTINGS = os.path.expandvars(
    r"%USERPROFILE%\AppData\LocalLow\Christoffer Bodegard\Esoteric Ebb\SETTINGS.es3")

# the fonts of the dialogue that carry no Cyrillic
FONTS_WITHOUT_CYRILLIC = (0, 2)
FONT_WITH_CYRILLIC = 6


def fix_font():
    """Move the dialogue font to one that can draw the Russian text."""
    if not os.path.isfile(SETTINGS):
        return "no settings file"
    with io.open(SETTINGS, encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r'("FontIndex"\s*:\s*\{\s*"__type"\s*:\s*"int",\s*"value"\s*:\s*)(\d+)', text)
    if not m:
        return "no font index"
    if int(m.group(2)) not in FONTS_WITHOUT_CYRILLIC:
        return "font index %s kept" % m.group(2)
    text = text[:m.start()] + m.group(1) + str(FONT_WITH_CYRILLIC) + text[m.end():]
    with io.open(SETTINGS, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    return "font index %s moved to %d" % (m.group(2), FONT_WITH_CYRILLIC)


def main():
    if not os.path.isdir(SRC):
        print("nothing to install: %s" % SRC)
        sys.exit(1)
    if os.path.isdir(DST):
        shutil.rmtree(DST)
    os.makedirs(DST)
    total = 0
    for name in sorted(os.listdir(SRC)):
        if not name.endswith(".csv"):
            continue
        raw = open(os.path.join(SRC, name), "rb").read()
        raw = raw.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        with open(os.path.join(DST, name), "wb") as fh:
            fh.write(raw)
        total += 1
    print("installed %d files into %s" % (total, DST))
    print(fix_font())


if __name__ == "__main__":
    main()
