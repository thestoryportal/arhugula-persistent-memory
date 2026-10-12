#!/usr/bin/env python3
"""Build reachable all-ref blob and history-path index, without git writes."""
import subprocess,csv,json,collections
from pathlib import Path
from datetime import datetime,timezone
OUT=Path(__file__).resolve().parents[1];REPO=OUT.parents[1]
def run(args):
 p=subprocess.run(['git']+args,cwd=REPO,capture_output=True)
 if p.returncode:raise RuntimeError(p.stderr.decode('utf-8','replace'))
 if not p.stdout:raise RuntimeError('Empty output '+str(args))
 return p.stdout
objects=run(['rev-list','--all','--objects'])
lines=objects.splitlines();oids=[x.split(b' ',1)[0] for x in lines]
p=subprocess.run(['git','cat-file','--batch-check=%(objectname) %(objecttype) %(objectsize)'],input=b'\n'.join(oids)+b'\n',cwd=REPO,capture_output=True)
if p.returncode:raise RuntimeError(p.stderr.decode())
checks=p.stdout.splitlines()
if len(checks)!=len(lines):raise RuntimeError('cat-file row mismatch')
blobs=0
with (OUT/'history_blobs.tsv').open('x',newline='') as f:
 w=csv.writer(f,delimiter='\t',lineterminator='\n');w.writerow(['git_blob_id','bytes','representative_history_path'])
 for obj,check in zip(lines,checks):
  parts=check.split()
  if len(parts)!=3:raise RuntimeError('invalid object '+repr(check))
  oid,kind,size=parts
  if kind==b'blob':w.writerow([oid.decode(),int(size),obj.partition(b' ')[2].decode('utf-8','surrogateescape')]);blobs+=1
# -z preserves path whitespace; --format= prevents commit text mixing into paths.
paths=run(['log','--all','--format=','--name-only','-z']).split(b'\0')
names=sorted({x.strip(b'\n').decode('utf-8','surrogateescape') for x in paths if x.strip(b'\n')})
(OUT/'history_paths.json').write_text(json.dumps(names,ensure_ascii=True))
refs=run(['show-ref']).decode();(OUT/'history_refs.txt').write_text(refs)
meta={'head':run(['rev-parse','HEAD']).decode().strip(),'objects':len(lines),'blobs':blobs,'history_paths':len(names),'built_utc':datetime.now(timezone.utc).isoformat(),'scope':'objects reachable from git rev-list --all (refs, not unreachable objects/reflog-only commits)'}
(OUT/'history_state.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta))
