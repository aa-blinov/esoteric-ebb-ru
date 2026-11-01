"""Scan current shipped CSVs against the installed English source.

Set EB_GAME_DIR for another game installation. Reports go to work/full-audit.
Candidates require contextual review; counts are not counts of errors.
"""
from pathlib import Path
import os
import csv, json, re, collections

root=Path(__file__).resolve().parents[1]
official=Path(os.environ.get('EB_GAME_DIR', 'M:/SteamLibrary/steamapps/common/Esoteric Ebb'))/'Esoteric Ebb_Data/StreamingAssets/Localization/Official'
rows=[]
for p in sorted((root/'translation/Russian').glob('*.csv')):
    with p.open(encoding='utf-8-sig',newline='') as f: rr=list(csv.reader(f))
    with (official/p.name).open(encoding='utf-8-sig',newline='') as f: ee=list(csv.reader(f))
    ix=ee[0].index('EN'); en={r[0]:r[ix] for r in ee[1:] if r and len(r)>ix}
    for r in rr[1:]:
        if r: rows.append(dict(file=p.name,key=r[0],en=en.get(r[0],''),ru=r[-1]))
out=root/'work/full-audit';out.mkdir(exist_ok=True)
with (out/'pairs.jsonl').open('w',encoding='utf-8') as f:
    for r in rows: f.write(json.dumps(r,ensure_ascii=False)+'\n')
checks={
 'false_friends':(r'\b(penal|conscientious objector|gay(?:est)?|eventually|actually|sympathetic|pathetic|sensible|sensitive|officious|magazine|novel|accurate|literal|fabric|decade|billion|trillion)\b',None),
 'suspicious_ru':(None,r'добросовестн.{0,12}отказ|карательн|гейск|голуб.{0,8}крыс|не cares|полукров|полуорк|хоббит|магократ|магократи|Диминор|Урт'),
 'lost_negation':(r'\b(?:not|never|neither|nothing|nobody|no one|cannot|can.t|don.t|doesn.t|didn.t|won.t|wouldn.t)\b',r'^(?!.*(?:\bне\b|\bни\b|нет|нельзя|ник|нич|без|невоз|неспособ|отказ)).*$'),
}
counts={}
extra={
 'damaged_text':[r for r in rows if re.search(r'\?{3,}|\ufffd',r['ru']) and not re.search(r'\?{3,}',r['en'])],
 'expanded_short_source':[r for r in rows if 8<len(r['en'])<65 and len(r['ru'])>max(100,len(r['en'])*2.8)],
 'shortened_long_source':[r for r in rows if len(r['en'])>100 and len(r['ru'])<len(r['en'])*.55 and r['ru'].strip() and re.search('[A-Za-z]',r['en'])],
}
for name,found in extra.items():
    counts[name]=len(found)
    with (out/(name+'.json')).open('w',encoding='utf-8') as f: json.dump(found,f,ensure_ascii=False,indent=2)
for name,(a,b) in checks.items():
    found=[r for r in rows if (not a or re.search(a,r['en'],re.I)) and (not b or re.search(b,r['ru'],re.I))]
    counts[name]=len(found)
    with (out/(name+'.txt')).open('w',encoding='utf-8') as f:
        for r in found: f.write(f"{r['file']} {r['key']}\nEN {r['en']}\nRU {r['ru']}\n\n")
groups=collections.defaultdict(list)
for r in rows:
    if len(r['en'].strip())>25: groups[r['en'].strip()].append(r)
variants=[v for v in groups.values() if len({r['ru'] for r in v})>1]
with (out/'inconsistent.json').open('w',encoding='utf-8') as f: json.dump(variants,f,ensure_ascii=False,indent=2)
summary=dict(rows=len(rows),files=len({r['file'] for r in rows}),candidates=counts,inconsistent_long_groups=len(variants))
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
