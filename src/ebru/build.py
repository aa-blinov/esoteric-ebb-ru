#!/usr/bin/env python
"""The translation pipeline, stage by stage.

    python3 src/ebru/build.py --stage all
    python3 src/ebru/build.py --stage typography
    python3 src/ebru/build.py --install --game-dir "/path/to/Esoteric Ebb"

Every stage reads one JSONL file and writes another. Nothing is written
straight into the shipped folder: the last stage builds the CSVs from the
final corpus, and the tests read those CSVs.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
WORK = os.path.join(ROOT, "work")
CORPUS = os.path.join(WORK, "corpus")
GAME_DIR_DEFAULT = os.environ.get(
    "EB_GAME_DIR", r"C:\Program Files (x86)\Steam\steamapps\common\Esoteric Ebb")


def py(script, *args):
    path = os.path.join(HERE, script)
    cmd = [sys.executable, path] + [str(a) for a in args]
    print("  $ %s %s" % (os.path.basename(script), " ".join(str(a) for a in args)), flush=True)
    subprocess.run(cmd, check=True, cwd=ROOT)


def stage_corpus():
    os.makedirs(CORPUS, exist_ok=True)
    py("extract_corpus.py")


def stage_bulk(model):
    py("run_translation.py", "--src", os.path.join(CORPUS, "corpus.jsonl"),
       "--out", os.path.join(CORPUS, "bulk.jsonl"), "--stage", "all", "--model", model)


def stage_edit(model):
    py("literary_pass.py", "--src", os.path.join(CORPUS, "bulk.jsonl"),
       "--out", os.path.join(CORPUS, "edit1.jsonl"))
    py("literary_pass.py", "--src", os.path.join(CORPUS, "edit1.jsonl"),
       "--out", os.path.join(CORPUS, "edit2.jsonl"))


def stage_address():
    py("unify_address.py", "--src", os.path.join(CORPUS, "edit2.jsonl"),
       "--out", os.path.join(CORPUS, "address.jsonl"))


def stage_canon():
    py("canonicalise.py", "--src", os.path.join(CORPUS, "address.jsonl"),
       "--out", os.path.join(CORPUS, "canon.jsonl"))


def stage_typography():
    py("typo_normalise.py", os.path.join(CORPUS, "canon.jsonl"),
       os.path.join(CORPUS, "typo.jsonl"))


def stage_layout():
    py("fix_layout.py", os.path.join(CORPUS, "typo.jsonl"),
       os.path.join(CORPUS, "layout.jsonl"))


def stage_compact():
    py("compact_ui.py", os.path.join(CORPUS, "layout.jsonl"),
       os.path.join(CORPUS, "compact.jsonl"))
    py("typo_normalise.py", os.path.join(CORPUS, "compact.jsonl"),
       os.path.join(CORPUS, "compact2.jsonl"))


def stage_quotes():
    py("fix_quotes.py", os.path.join(CORPUS, "compact2.jsonl"),
       os.path.join(CORPUS, "quotes.jsonl"))
    py("fix_quote_chain.py", os.path.join(CORPUS, "quotes.jsonl"),
       os.path.join(CORPUS, "chain.jsonl"))


def stage_qa(model):
    py("qa_check.py", model, os.path.join(CORPUS, "chain.jsonl"),
       os.path.join(CORPUS, "qa.jsonl"))
    py("struct_qa.py", "--src", os.path.join(CORPUS, "qa.jsonl"),
       "--out", os.path.join(CORPUS, "struct.jsonl"))
    py("verify_final.py", os.path.join(CORPUS, "struct.jsonl"))


def stage_build():
    py("finalize.py", "--source", os.path.join(CORPUS, "struct.jsonl"))


def install(game_dir):
    src = os.path.join(ROOT, "translation", "Russian")
    dst = os.path.join(game_dir, "Esoteric Ebb_Data", "StreamingAssets", "Localization", "Russian")
    import shutil
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print("installed: %s" % dst)


STAGES = {
    "corpus": stage_corpus,
    "bulk": stage_bulk,
    "edit": stage_edit,
    "address": stage_address,
    "canon": stage_canon,
    "typography": stage_typography,
    "layout": stage_layout,
    "compact": stage_compact,
    "quotes": stage_quotes,
    "qa": stage_qa,
    "build": stage_build,
}

ORDER = ["corpus", "bulk", "edit", "address", "canon", "typography",
         "layout", "compact", "quotes", "qa", "build"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage", default="all",
                    help="one stage, or 'all' for the whole pipeline")
    ap.add_argument("--model", default="minimax/MiniMax-M3",
                    help="the model the translation stages call")
    ap.add_argument("--install", action="store_true",
                    help="copy the finished folder into the game")
    ap.add_argument("--game-dir", default=GAME_DIR_DEFAULT,
                    help="the Esoteric Ebb installation directory")
    args = ap.parse_args()

    os.makedirs(CORPUS, exist_ok=True)
    names = ORDER if args.stage == "all" else [args.stage]
    for name in names:
        if name not in STAGES:
            print("unknown stage: %s" % name)
            print("stages: %s" % ", ".join(ORDER))
            sys.exit(2)
        print("\n=== %s ===" % name, flush=True)
        STAGES[name](args.model)

    if args.install:
        print("\n=== install ===")
        install(args.game_dir)


if __name__ == "__main__":
    main()
