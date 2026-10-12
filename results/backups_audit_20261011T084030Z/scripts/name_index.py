#!/usr/bin/env python3
"""Name-only traversal of mirror + exact historical blob locations; no bulk reads."""
import os,csv,json,subprocess,re
from pathlib import Path
OUT=Path(__file__).resolve().parents[1]; REPO=OUT.parents[1]
candidates=list(csv.DictReader((OUT/('candidates_refined.tsv' if (OUT/'candidates_refined.tsv').exists() else 'candidates.tsv')).open(),delimiter='\t'))
wanted={Path(x['path']).name for x in candidates};hist=json.loads((OUT/'history_paths.json').read_text());idx={n:{'history':[],'filesystem':[]} for n in wanted}
for p in hist:
 n=Path(p).name
 if n in idx:idx[n]['history'].append(p)
errors=[];files=0
for d,ds,fs in os.walk('/Volumes/memit/llm-database-poc-mirror',followlinks=False,onerror=lambda e:errors.append(str(e))):
 if Path(d)==OUT:ds.clear();continue
 ds[:]=[x for x in ds if x not in {'.git','.Spotlight-V100','.Trashes','.TemporaryItems','.fseventsd'}]
 for n in fs:
  files+=1
  if n in idx:idx[n]['filesystem'].append(str(Path(d)/n))
(OUT/'name_index.json').write_text(json.dumps(idx,ensure_ascii=True,separators=(',',':')))
p=subprocess.run(['git','log','--all','--raw','--no-abbrev','--no-renames','--root','--full-history','--diff-merges=first-parent','--format=COMMIT:%H','-z'],cwd=REPO,capture_output=True)
if p.returncode or not p.stdout:raise RuntimeError(p.stderr.decode())
parts=p.stdout.split(b'\0');locations={};commit=None;i=0
while i<len(parts):
 item=parts[i].strip(b'\n')
 if item.startswith(b'COMMIT:'):commit=item[7:].decode()
 elif item.startswith(b':'):
  fields=item.split();blob=fields[3].decode();i+=1;path=parts[i].decode('utf-8','surrogateescape')
  if blob!='0'*40 and blob not in locations:locations[blob]={'commit':commit,'path':path}
 i+=1
(OUT/'blob_locations.json').write_text(json.dumps(locations,ensure_ascii=True,separators=(',',':')))
print(json.dumps({'mirror_files_listed':files,'basenames':len(wanted),'history_locations':len(locations),'errors':errors}))
(OUT/'name_index_state.json').write_text(json.dumps({'mirror_files_listed':files,'basenames':len(wanted),'history_locations':len(locations),'errors':errors},indent=2))
