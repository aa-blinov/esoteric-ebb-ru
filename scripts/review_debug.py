import json
import os
import sys

ROOT = r"C:\Users\justcomex\.minimax\workspace\esoteric-ebb-ru\esoteric-ebb-ru"
sys.path.insert(0, os.path.join(ROOT, "src", "ebru"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from llm_client import call_llm, extract_json_array  # noqa: E402
import review_labels as RL  # noqa: E402

labels = json.load(open(os.path.join(ROOT, "work", "short_labels.json"), encoding="utf-8"))
target = [l for l in labels if l["key"] in ("Menu_Button_Load", "Keybind_Reject", "Menu_Button_Credits")]
print("batch:", json.dumps(target, ensure_ascii=False))
user = json.dumps(target, ensure_ascii=False, indent=1)
txt = call_llm("MiniMax-M3", RL.SYSTEM, user, max_tokens=2000, temperature=0.2,
               cache_key="review|%s" % user)
print("--- raw ---")
print(txt[:1500])
print("--- parsed ---")
print(extract_json_array(txt))
