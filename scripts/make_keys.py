#!/usr/bin/env python
"""Write the key manifest the tests read.

The manifest holds the row order and the inline markup of every key of the
English source. It is the shape of the game, not its text: the dialogue keys
are identifiers, and the markup tells the test what a Russian row has to
carry. The game itself has to be installed for this to run.
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOC = os.path.join(
    os.environ.get("EB_GAME_DIR", r"C:\Program Files (x86)\Steam\steamapps\common\Esoteric Ebb"),
    "Esoteric Ebb_Data", "StreamingAssets", "Localization")
OFFICIAL = os.path.join(LOC, "Official")
OUT = os.path.join(ROOT, "translation", "keys.json")

SPECIAL = re.compile(r"<[^>]*>|\{[^{}]*\}")


def main():
    if not os.path.isdir(OFFICIAL):
        print("the game is not installed at %s" % LOC)
        print("set EB_GAME_DIR to the Esoteric Ebb directory")
        sys.exit(1)
    manifest = {}
    for fn in sorted(os.listdir(OFFICIAL)):
        if not fn.endswith(".csv"):
            continue
        rows = list(csv.reader(open(os.path.join(OFFICIAL, fn), encoding="utf-8-sig", newline="")))
        header = rows[0]
        en_index = next((i for i, h in enumerate(header) if h.strip() == "EN"), None)
        entries = []
        for r in rows[1:]:
            if not r:
                continue
            en = r[en_index] if en_index is not None and len(r) > en_index else ""
            # A source cell that carries only markup has no text to translate,
            # and no markup for the translation to carry either.
            visible = SPECIAL.sub("", en).strip()
            entries.append([r[0], "".join(SPECIAL.findall(en)) if visible else "",
                            bool(visible)])
        manifest[fn] = entries
        print("%-16s %d rows" % (fn, len(entries)))
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, separators=(",", ":"))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
