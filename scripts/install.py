#!/usr/bin/env python
"""Install the finished translation into the game.

The repository stores the CSV files with LF endings; the game is on Windows,
so the installed copy gets CRLF, like the files the developer shipped.
"""
from __future__ import annotations

import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "translation", "Russian")
GAME = os.environ.get(
    "EB_GAME_DIR", r"C:\Program Files (x86)\Steam\steamapps\common\Esoteric Ebb")
DST = os.path.join(GAME, "Esoteric Ebb_Data", "StreamingAssets", "Localization", "Russian")


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


if __name__ == "__main__":
    main()
