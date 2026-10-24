#!/usr/bin/env python
"""Merge translated corpora, build the RU language folder and install it into the game.

  python finalize.py            # merge -> assemble -> install
  python finalize.py --no-install
"""
from __future__ import annotations

import csv
import io
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CORPUS_DIR = os.path.join(ROOT, "work", "corpus")
LOC = os.path.join(os.environ.get(
    "EB_GAME_DIR",
    r"C:\Program Files (x86)\Steam\steamapps\common\Esoteric Ebb"),
    "Esoteric Ebb_Data", "StreamingAssets", "Localization")
TPL = os.path.join(LOC, "Template")
GAME_RU = os.path.join(LOC, "Russian")
BUILD_RU = os.path.join(ROOT, "translation", "Russian")
CODE = "RU"

MISC_OVERRIDE = {
    "LanguageDropdown": "Русский",
    "FallbackLanguage": "EN",
    "DC": "DC",
    "dc_smallcaps": "dc",
}


def merge_corpora(out_path):
    merged = {}
    en_map = {}
    base = os.path.join(CORPUS_DIR, "corpus.jsonl")
    if os.path.exists(base):
        for line in open(base, encoding="utf-8"):
            r = json.loads(line)
            en_map[(r["file"], r["key"])] = r["en"]

    files = [f for f in os.listdir(CORPUS_DIR) if f.startswith("corpus_ru") and f.endswith(".jsonl")]
    # later files win: QA output must override raw translations
    files.sort(key=lambda f: (f.startswith("corpus_ru_q"), f))
    for fn in files:
        path = os.path.join(CORPUS_DIR, fn)
        n = 0
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                r = json.loads(line)
                if r.get("ru"):
                    key = (r["file"], r["key"])
                    merged[key] = r["ru"]
                    n += 1
        print("  %-28s +%d" % (fn, n))
    with open(out_path, "w", encoding="utf-8") as fh:
        for (f, k), v in merged.items():
            fh.write(json.dumps({"file": f, "key": k, "en": en_map.get((f, k), ""),
                                 "ru": v}, ensure_ascii=False) + "\n")
    print("merged unique strings:", len(merged))
    return merged


def read_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.reader(fh))


def build(translations, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    stats = {}
    for fn in sorted(os.listdir(TPL)):
        if not fn.endswith(".csv"):
            continue
        name = fn[:-4]
        rows = read_csv(os.path.join(TPL, fn))
        header = rows[0]
        header[-1] = CODE
        out_rows = [header]
        filled = empty = 0
        for r in rows[1:]:
            if not r:
                continue
            key = r[0]
            ru = translations.get((name, key), "")
            if name == "MiscTexts" and key in MISC_OVERRIDE:
                ru = MISC_OVERRIDE[key]
            if ru:
                filled += 1
            else:
                empty += 1
            out_rows.append(r[:-1] + [ru])
        stats[name] = {"rows": len(out_rows) - 1, "filled": filled, "empty": empty}
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\r\n", quoting=csv.QUOTE_MINIMAL)
        for row in out_rows:
            w.writerow(row)
        with open(os.path.join(out_dir, fn), "w", encoding="utf-8", newline="") as fh:
            fh.write(buf.getvalue())
    return stats


def install(build_dir, game_dir):
    if os.path.isdir(game_dir):
        shutil.rmtree(game_dir)
    shutil.copytree(build_dir, game_dir)
    return game_dir


def pick_source():
    """Use the newest QA round if present, else the plain merge."""
    rounds = []
    for fn in os.listdir(CORPUS_DIR):
        if fn.startswith("corpus_ru_r") and fn.endswith(".jsonl"):
            try:
                rounds.append((int(fn[len("corpus_ru_r"):-len(".jsonl")]), fn))
            except ValueError:
                pass
    if rounds:
        rounds.sort()
        return os.path.join(CORPUS_DIR, rounds[-1][1])
    return os.path.join(CORPUS_DIR, "corpus_ru_merged.jsonl")


if __name__ == "__main__":
    src = None
    if "--source" in sys.argv:
        src = sys.argv[sys.argv.index("--source") + 1]
    if not src:
        src = pick_source()
    print("source:", src)

    if "--merge-only" in sys.argv:
        merge_corpora(os.path.join(CORPUS_DIR, "corpus_ru_merged.jsonl"))
        sys.exit(0)

    tr = {}
    with open(src, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if r.get("ru"):
                tr[(r["file"], r["key"])] = r["ru"]
    print("source strings:", len(tr))

    print("\n=== build ===")
    st = build(tr, BUILD_RU)
    tot_f = sum(v["filled"] for v in st.values())
    tot_e = sum(v["empty"] for v in st.values())
    for k, v in sorted(st.items()):
        print("  %-16s rows=%-6d ru=%-6d fallback=%d" % (k, v["rows"], v["filled"], v["empty"]))
    print("  TOTAL ru=%d fallback=%d" % (tot_f, tot_e))

    if "--no-install" not in sys.argv:
        print("\n=== install into game ===")
        p = install(BUILD_RU, GAME_RU)
        print("installed:", p)
