#!/usr/bin/env python3
"""Append every excluded file symlink to inventory with explicit hash semantics.
For existing regular targets, git hash-object --no-filters <symlink> hashes the
referent; SHA256 likewise, and bytes/mtime are referent stat. Dangling targets
have blank hashes plus metadata exceptions, never fabricated IDs. No dir-link traversal.
"""
import csv,json,os,hashlib,subprocess,collections
from pathlib import Path
from datetime import datetime,timezone
OUT=Path(__file__).resolve().parents[1];ROOT=Path('/Volumes/backups');REPO=OUT.parents[1]
errors=json.loads((OUT/'inventory_errors.json').read_text());cache={};counts=collections.Counter();existing=set()
with (OUT/'inventory.tsv').open() as f:
 for r in csv.DictReader(f,delimiter='\t'):existing.add(r['path'])
rows=len(existing)
with (OUT/'inventory.tsv').open('a',newline='') as f,(OUT/'symlinks.tsv').open('x',newline='') as g:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');v=csv.writer(g,delimiter='\t',lineterminator='\n')
 v.writerow(['inventory_row','path','link_target','link_bytes','link_mtime_utc','status','hash_semantics'])
 for e in errors:
  rel=e['path'];p=ROOT/rel
  if rel in existing:raise RuntimeError('Supplement already appended: '+rel)
  s=p.lstat();target=os.readlink(p);sha='';blob='';size=s.st_size;mtime=s.st_mtime;status='DANGLING_TARGET'
  if p.is_file():
   real=str(p.resolve());follow=p.stat();size=follow.st_size;mtime=follow.st_mtime
   if real not in cache:
    h=hashlib.sha256()
    with p.open('rb') as q:
     while True:
      b=q.read(1024*1024)
      if not b:break
      h.update(b)
    cache[real]=h.hexdigest()
   sha=cache[real]
   proc=subprocess.run(['git','hash-object','--no-filters',str(p)],cwd=REPO,capture_output=True,text=True)
   if proc.returncode or len(proc.stdout.strip())!=40:raise RuntimeError(proc.stderr or 'Invalid git hash-object result')
   blob=proc.stdout.strip();status='HASHED_REFERENT'
  rows+=1;counts[status]+=1;w.writerow([rel,size,datetime.fromtimestamp(mtime,timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),sha,blob]);v.writerow([rows,rel,target,s.st_size,datetime.fromtimestamp(s.st_mtime,timezone.utc).isoformat(),status,'referent bytes' if sha else 'no content exists to hash'])
(OUT/'symlink_state.json').write_text(json.dumps({'appended_rows':len(errors),'final_inventory_rows':rows,'counts':dict(counts),'note':'file symlinks only; symlink directories were not followed, per name-only audit scope. Dangling entries cannot have SHA256 or git blob IDs.'},indent=2));print(dict(counts))
