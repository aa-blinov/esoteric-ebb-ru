import json
import os
import re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- measure the lore panel width from a native screenshot -------------------
im = Image.open(os.path.join(ROOT, "ru_game1.png")).convert("RGB")
w, h = im.size
row = 600
px = im.load()
left = right = None
for x in range(100, 700):
    r, g, b = px[x, row]
    dark = r < 40 and g < 40 and b < 40
    if dark and left is None:
        left = x
    if dark:
        right = x
print("panel dark span at y=%d: x=%s..%s  width=%s" % (row, left, right,
      (right - left) if left is not None else None))
PANEL = 500
print("panel width:", PANEL)

# --- estimate rendered width of every size-tagged run -------------------------
TAG = re.compile(r"<(/?)size(?:=(\d+))?>")


def runs(text):
    out = []
    cur = None
    pos = 0
    for m in TAG.finditer(text):
        chunk = text[pos:m.start()]
        if chunk.strip():
            out.append((cur, chunk.strip()))
        cur = None if m.group(1) else int(m.group(2) or 0)
        pos = m.end()
    if text[pos:].strip():
        out.append((cur, text[pos:].strip()))
    return out


# display font: average advance of caps ~0.62 em, lowercase ~0.52 em
def width(text, size):
    wpx = 0.0
    for ch in text:
        if ch == " ":
            wpx += 0.28
        elif ch.isupper():
            wpx += 0.66
        elif ch.islower():
            wpx += 0.52
        else:
            wpx += 0.5
    return wpx * size


rows = [json.loads(l) for l in open(os.path.join(ROOT, "work", "corpus", "corpus_ru_FIX.jsonl"), encoding="utf-8")]
report = []
bad = []
for r in rows:
    en = r.get("en") or ""
    ru = r.get("ru") or ""
    if "<size" not in ru and "<size" not in en:
        continue
    en_max = max([width(t, s or 20) for s, t in runs(en)] or [0])
    ru_max = max([width(t, s or 20) for s, t in runs(ru)] or [0])
    en_big = max([width(t, s) for s, t in runs(en) if s] or [0])
    ru_big = max([width(t, s) for s, t in runs(ru) if s] or [0])
    report.append("KEY: %s" % r["key"])
    report.append("  EN: %s" % en.replace("\n", " | ")[:160])
    report.append("  RU: %s" % ru.replace("\n", " | ")[:160])
    report.append("  widest line: EN %.0f px | RU %.0f px   (panel %d px)" % (en_max, ru_max, PANEL))
    report.append("  widest BIG run: EN %.0f | RU %.0f" % (en_big, ru_big))
    if ru_max > PANEL or ru_big > PANEL:
        bad.append(r["key"])
        report.append("  <<< OVERFLOWS PANEL")
    report.append("")

open(os.path.join(ROOT, "panel_fit.txt"), "w", encoding="utf-8").write("\n".join(report))
print("\nstrings that overflow the panel:", len(bad))
for k in bad:
    print("  ", k)
