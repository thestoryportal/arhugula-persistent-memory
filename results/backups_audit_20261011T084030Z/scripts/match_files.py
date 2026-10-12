#!/usr/bin/env python3
"""EXACT and SAME-NAME triage. No-name files remain CONTENT-PENDING, never auto-UNIQUE.
Byte hashes establish historical EXACT only. Same-name comparisons give evidence,
not chronological/version conclusions. Large files are never loaded whole.
"""
import csv,json,hashlib,subprocess,collections,re,difflib,os
from pathlib import Path
OUT=Path(__file__).resolve().parents[1];REPO=OUT.parents[1];ROOT=Path('/Volumes/backups')
def identity_match(blob,blobs):return 'EXACT' if blob in blobs else None
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  while True:
   chunk=f.read(1024*1024)
   if not chunk:break
   h.update(chunk)
 return h.hexdigest()
def norm(b):return re.sub(rb'\s+',b'',b)
def main():
 candidates={r['inventory_row']:r for r in csv.DictReader((OUT/'candidates_refined.tsv').open(),delimiter='\t')}
 blobs={r['git_blob_id']:r for r in csv.DictReader((OUT/'history_blobs.tsv').open(),delimiter='\t')}
 loc=json.loads((OUT/'blob_locations.json').read_text());names=json.loads((OUT/'name_index.json').read_text())
 # All recorded versions for a same basename, not only current representative path.
 versions=collections.defaultdict(list)
 for oid,entry in loc.items():versions[Path(entry['path']).name].append((oid,entry))
 cache={};counts=collections.Counter();details={};pending=[]
 with (OUT/'matches.tsv').open('w',newline='') as f:
  w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['inventory_row','class','match','comparison','repo_or_mirror_path','commit','evidence','same_name_candidate_count'])
  for i,r in enumerate(csv.DictReader((OUT/'inventory.tsv').open(),delimiter='\t'),1):
   key=str(i)
   if key not in candidates:continue
   c=candidates[key];blob=r['git_blob_id'];rel=r['path'];kind=c['class'];name=Path(rel).name
   exact=identity_match(blob,blobs)
   if exact:
    entry=loc.get(blob)
    if not entry:raise RuntimeError('Missing commit/path for exact blob '+blob)
    w.writerow([i,kind,'EXACT','historical byte-identical',entry['path'],entry['commit'],blob,0]);counts[(kind,'EXACT')]+=1;continue
   item=names.get(name,{'filesystem':[],'history':[]});paths=item['filesystem'];hist=item['history'];options=versions.get(name,[])
   if not paths and not hist and not options:
    w.writerow([i,kind,'CONTENT-PENDING','','','','No basename match; content/rename review required',0]);counts[(kind,'CONTENT-PENDING')]+=1;pending.append(rel);continue
   size=int(r['bytes']);backup=ROOT/rel;small=size<=200*1024;body=backup.read_bytes() if small else None;best=None;checks=[]
   # Real matching files only; no arbitrary mirror bulk reads.
   for target in paths:
    p=Path(target)
    if not p.is_file():continue
    target_size=p.stat().st_size
    result=None;ratio=0.0
    if target_size==size:
     k=('sha',target)
     if k not in cache:cache[k]=sha(p)
     if cache[k]==r['sha256']:result='identical outside reachable history';ratio=1.0
    if result is None and small and target_size<=200*1024:
     k=('body',target)
     if k not in cache:cache[k]=p.read_bytes()
     other=cache[k]
     if norm(body)==norm(other):result='identical-after-whitespace';ratio=1.0
     elif b'\0' not in body[:8192] and b'\0' not in other[:8192]:
      ratio=difflib.SequenceMatcher(None,body.splitlines(),other.splitlines(),autojunk=True).ratio();result='different; chronology requires review'
     else:result='different binary'
    if result:
     checks.append({'path':target,'comparison':result,'line_similarity':round(ratio,4),'bytes':target_size})
     score=(ratio,1 if target.startswith(str(REPO)+'/') else 0)
     if best is None or score>best[0]:best=(score,target,'',result,checks[-1])
     if result=='identical outside reachable history' and target.startswith(str(REPO)+'/'):break
   # Historical whitespace versions catch recovered docs with altered line endings.
   if small and (best is None or best[0][0]<1):
    for oid,entry in options:
     b=blobs.get(oid)
     if not b or int(b['bytes'])>200*1024:continue
     k=('blob',oid)
     if k not in cache:
      proc=subprocess.run(['git','cat-file','blob',oid],cwd=REPO,capture_output=True)
      if proc.returncode:raise RuntimeError(proc.stderr.decode())
      cache[k]=proc.stdout
     other=cache[k]
     if norm(body)==norm(other):
      result='identical-after-whitespace (history)';ratio=1.0
      best=((ratio,2),entry['path'],entry['commit'],result,{'blob':oid,'comparison':result});break
   total=len(paths)+len(hist)
   if best:
    _,target,commit,result,evidence=best
    w.writerow([i,kind,'SAME-NAME',result,target,commit,json.dumps(evidence,separators=(',',':')),total])
    details[key]={'backup':rel,'chosen':evidence,'other_comparisons':checks[:12],'checks_count':len(checks),'historical_versions':len(options)}
   else:w.writerow([i,kind,'SAME-NAME','UNCOMPARED: large/unreadable candidates require ranges or streamed comparison',paths[0] if paths else hist[0],'','No inference of duplication',total])
   counts[(kind,'SAME-NAME')]+=1
 (OUT/'match_details.json').write_text(json.dumps(details,ensure_ascii=True,separators=(',',':')))
 (OUT/'content_pending.json').write_text(json.dumps(pending,indent=2))
 (OUT/'match_state.json').write_text(json.dumps({'counts':{'|'.join(k):v for k,v in counts.items()},'status':'EXACT/SAME-NAME triage complete; CONTENT and version/gap review PENDING'},indent=2))
 print(json.dumps({'|'.join(k):v for k,v in counts.items()}))
if __name__=='__main__':main()
