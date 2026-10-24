import json
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rows = [json.loads(l) for l in open(ROOT + r"\work\corpus\corpus_ru_lit2.jsonl", encoding="utf-8")]

paren_to_quote = 0
quote_to_paren = 0
ok_paren = 0
examples = []
for r in rows:
    en = (r.get("en") or "").strip()
    ru = (r.get("ru") or "").strip()
    if not en or not ru:
        continue
    if en.startswith("(") and en.endswith(")"):
        if ru.startswith("«") and ru.endswith("»"):
            paren_to_quote += 1
            if len(examples) < 12:
                examples.append((en, ru))
        elif ru.startswith("(") and ru.endswith(")"):
            ok_paren += 1
    if en.startswith("«") or en.startswith('"'):
        if ru.startswith("("):
            quote_to_paren += 1

out = ["=== stage-direction brackets ==="]
out.append("EN '(...)' -> RU '«...»'  : %d" % paren_to_quote)
out.append("EN '(...)' -> RU '(...)'  : %d" % ok_paren)
out.append("EN quote -> RU '(...)'      : %d" % quote_to_paren)
out.append("")
for en, ru in examples:
    out.append("EN: %s" % en[:110])
    out.append("RU: %s" % ru[:110])
    out.append("")
open(ROOT + r"\brackets_audit.txt", "w", encoding="utf-8").write("\n".join(out))
print("paren->quote:", paren_to_quote, " kept:", ok_paren, " quote->paren:", quote_to_paren)
