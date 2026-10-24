#!/usr/bin/env python
"""Literary editing pass: unify the voice across the whole translation.

Every batch is edited against the same voice bible, with the previous batch's
Russian text supplied as a continuity anchor, so the narration keeps one tone
from the first line to the last. Edits are validated (markup preserved, no
mixed script, nothing lost) and rolled back to the previous text if they fail.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from llm_client import call_llm, extract_json_array, specials  # noqa: E402
from qa_check import analyse  # noqa: E402

VOICE = open(os.path.join(ROOT, "src", "voice", "bible.md"), encoding="utf-8").read()
BASE = os.path.join(ROOT, "work", "corpus", "corpus.jsonl")
GLOSSARY_JSON = os.path.join(ROOT, "work", "corpus", "glossary_polished.json")

MAX_ITEMS = 30
WORKERS = int(os.environ.get("EB_WORKERS", "10"))
_lock = threading.Lock()


def log(*a):
    with _lock:
        print(*a, flush=True)


def load_meta():
    meta = {}
    for line in open(BASE, encoding="utf-8"):
        r = json.loads(line)
        meta[(r["file"], r["key"])] = {"speaker": r.get("speaker") or "", "en": r["en"]}
    return meta


def load_glossary():
    g = json.load(open(GLOSSARY_JSON, encoding="utf-8"))
    return {k: v for k, v in g.items() if k and v and len(k) <= 45}


def relevant_terms(texts, glossary, limit=180):
    blob = " ".join(texts).lower()
    hits = []
    for en, ru in glossary.items():
        if len(en) < 3:
            continue
        if en.lower() in blob:
            hits.append((en, ru))
    hits.sort(key=lambda x: -len(x[0]))
    return hits[:limit]


CORE_TERMS = [
    "Cleric", "Urth", "Urthfolk", "Norvik", "Norvikian", "Tolstad", "Freestrider",
    "Azgalist", "Azgal", "Snell", "Darrow", "Coinlord", "Jor", "Meek", "Sageleaf",
    "Kraaid", "Ettir", "Visken", "Modissa", "Gorm", "Waterlane", "Arcanist", "Azgalists",
    "Arcanists", "Azgalian", "Urthguard", "Undercoast", "Vourgeni", "Askan", "Askanii",
    "Reeds", "The Coast", "String", "Post", "Hedonists", "Operativism", "Patriarchs",
    "Simii", "Bugbear", "Roper", "Divinii Torum", "Golden Horde", "Gate Era", "Vox Operariorum",
]


def fmt_glossary(pairs):
    if not pairs:
        return ""
    return "\n\nГЛОССАРИЙ (обязательные переводы, не заменяй синонимами):\n" + \
        "\n".join("- %s → %s" % (a, b) for a, b in pairs)


SYSTEM = VOICE + """

Ты редактируешь существующий русский перевод. Для каждой строки:
- сохрани смысл, объём, характер и всю разметку;
- приведи строку к голосу, описанному выше;
- если строка уже в голосе — верни её без изменений;
- не переводи заново то, что уже хорошо переведено.
"""


def build_batches(rows, meta, glossary):
    """Contiguous batches inside each file, dialogue in scene order."""
    batches = []
    cur = []
    cur_file = None
    for i, r in enumerate(rows):
        if not r.get("ru"):
            continue
        if cur and (r["file"] != cur_file or len(cur) >= MAX_ITEMS):
            batches.append(cur)
            cur = []
        cur.append(i)
        cur_file = r["file"]
    if cur:
        batches.append(cur)
    return batches


def build_payload(idxs, rows, meta, glossary, prev_tail):
    """Build the exact system+user payload for a batch (shared by run and review)."""
    items = []
    for n, i in enumerate(idxs):
        r = rows[i]
        m = meta.get((r["file"], r["key"]), {"speaker": "", "en": r["en"]})
        items.append({"id": n, "en": m["en"], "ru": r["ru"], "speaker": m["speaker"]})
    payload = [{"id": it["id"], "en": it["en"], "ru": it["ru"]} for it in items]

    sysmsg = SYSTEM
    core = [(t, glossary[t]) for t in CORE_TERMS if t in glossary]
    hits = relevant_terms([it["en"] for it in items], glossary)
    seen = {t for t, _ in core}
    pairs = core + [(a, b) for a, b in hits if a not in seen]
    sysmsg += fmt_glossary(pairs)

    parts = []
    if prev_tail:
        parts.append("ПРЕДЫДУЩИЙ ФРАГМЕНТ (для связности интонации, не переводи его заново):\n" + prev_tail)
    parts.append("ГОВОРИТ: " + ", ".join(sorted({it["speaker"] or "повествование" for it in items})))
    parts.append("СТРОКИ:")
    parts.append(json.dumps(payload, ensure_ascii=False, indent=1))
    return items, sysmsg, "\n\n".join(parts)


def edit_batch(idxs, rows, meta, glossary, prev_tail):
    items, sysmsg, user = build_payload(idxs, rows, meta, glossary, prev_tail)

    try:
        import hashlib
        ck = "lit|%s|%s|%s" % ("MiniMax-M3",
                               hashlib.sha256(sysmsg.encode("utf-8")).hexdigest()[:16],
                               user)
        txt = call_llm("MiniMax-M3", sysmsg, user, max_tokens=16000, temperature=0.25,
                       cache_key=ck)
        arr = extract_json_array(txt)
    except Exception as e:
        log("  batch failed: %s" % e)
        return []
    if not arr or len(arr) != len(items):
        return []
    out = []
    for it, cand in zip(items, arr):
        if not isinstance(cand, str) or not cand.strip():
            continue
        if specials(cand) != specials(it["ru"]):
            continue
        if analyse(it["en"], cand):
            continue
        if cand == it["ru"]:
            continue
        # guard: a pure change of letter case is a defect, not an edit
        if cand.lower() == it["ru"].lower():
            continue
        out.append((it["id"], cand))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.path.join(ROOT, "work", "corpus", "corpus_ru_typo.jsonl"))
    ap.add_argument("--out", default=os.path.join(ROOT, "work", "corpus", "corpus_ru_lit.jsonl"))
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.src, encoding="utf-8")]
    meta = load_meta()
    glossary = load_glossary()
    log("rows=%d glossary=%d" % (len(rows), len(glossary)))

    batches = build_batches(rows, meta, glossary)
    if args.limit:
        batches = batches[:args.limit]
    log("batches: %d" % len(batches))

    changed = {}
    t0 = time.time()
    done = 0

    def prev_context(b):
        """Lines preceding this batch in the same file - the continuity anchor."""
        start = b[0]
        out = []
        for j in range(max(0, start - 6), start):
            ru = rows[j].get("ru")
            if ru:
                out.append(ru.replace("\n", " ")[:220])
        return "\n".join(out)

    def work(b):
        return b, edit_batch(b, rows, meta, glossary, prev_context(b))

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(work, b) for b in batches]
        for i, f in enumerate(as_completed(futs), 1):
            b, res = f.result()
            for pid, cand in res:
                changed[b[pid]] = cand
            done += 1
            if i % 20 == 0:
                el = time.time() - t0
                rate = done / max(el, 1e-6)
                log("  %d/%d batches, changed=%d, %.1f b/min, eta=%d min"
                    % (i, len(batches), len(changed), rate * 60,
                       int((len(batches) - done) / max(rate, 1e-6) / 60)))

    log("edited rows: %d" % len(changed))
    for i, cand in changed.items():
        rows[i]["ru"] = cand
    with open(args.out, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    log("wrote", args.out)


if __name__ == "__main__":
    main()
