#!/usr/bin/env python3
"""Read-only full volume inventory. Writes only the named audit folder.
Usage: python3 scripts/inventory.py [--resume]
Hashes regular-file contents by SHA256 and git hash-object --no-filters --stdin-paths.
Files >200 KiB are streamed in 1 MiB chunks; content inspection bounded to first 200 KiB.
Symlinks are inventoried without following directories; any unreadable/special entry is an explicit error.
"""
import os,sys,csv,json,hashlib,subprocess,stat,re,time,collections
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path('/Volumes/backups'); OUT=Path(__file__).resolve().parents[1]; REPO=OUT.parents[1]
SKIP={'.Spotlight-V100','.Trashes','.TemporaryItems','.fseventsd'}
PRIORITY=['llm-as-database','_archive_stale_pre_s2_5b','src','drive-download-20260515T023255Z-3-001','drive-download-20260804T131838Z-1-001','arhugula-vm-data']
SIGNAL=re.compile(rb'(?i)MEMIT|LARQL|compute_z|LLM.as.Database|covariance|RunPod|Qwen|AlphaEdit|spec.v1\.2|C10[ab-z0-9]')
TEXT={'.md','.txt','.py','.ipynb','.json','.yaml','.yml','.toml','.sh','.csv','.tsv','.html','.js','.ts','.tsx','.jsx','.xml','.bib','.sql','.rst','.log','.jsonl'}
VENDOR=re.compile(r'(^|/)(node_modules|\.git|\.venv|venv|__pycache__|\.next|\.cache|vendor|dist|build)(/|$)')
def utc(t):return datetime.fromtimestamp(t,timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def quote(p):return '"'+str(p).replace('\\','\\\\').replace('"','\\"').replace('\t','\\t').replace('\n','\\n').replace('\r','\\r')+'"'
def walk():
 tops=sorted(ROOT.iterdir(),key=lambda p:(0 if p.is_file() else 1,PRIORITY.index(p.name) if p.name in PRIORITY else len(PRIORITY),p.name))
 for top in tops:
  if top.name in SKIP:continue
  if top.is_dir():
   for d,ds,fs in os.walk(top,followlinks=False,onerror=lambda e:(_ for _ in ()).throw(e)):
    ds.sort();fs.sort()
    if Path(d)==ROOT/'datasets':ds[:]=[x for x in ds if x!='caselaw']
    for n in fs:yield Path(d)/n
  else:yield top

def classify(rel,sample):
 low=rel.lower();top=low.split('/')[0]; suffix=Path(rel).suffix.lower()
 if top in {'llm-as-database','_archive_stale_pre_s2_5b'}:return 'program','P'
 if VENDOR.search(rel):return 'unrelated','V'
 hits=SIGNAL.findall(sample) if suffix in TEXT or b'\x00' not in sample[:8192] else []
 if hits:return 'program','C'
 if re.search(r'llm.as.database|memit|larql|qwen|alphaedit|compute_z|covariance|runpod',low):return 'program','N'
 if top in {'agent-deployment-framework','agent-sdk-workshop','indydevdan-harness-research','meta-harness-architecture-template','layer-05-runtime-operations','soe-skills-all','codex-app-intel-repackager-main'}:return 'adjacent','T'
 if '/' not in rel and re.search(r'(agent|harness|skill|context.engineer|state.memory|tool.integration|validation.contract|observability|evaluation|reliability.recovery|model.routing|prompt|workflow|architecture|framework|council|runtime)',low):return 'adjacent','T'
 return 'unrelated','O'
def main():
 start=time.time();done=set();idx=0;counts=collections.Counter();bytes_total=0
 inv=OUT/'inventory.tsv';cl=OUT/'classification.tsv';cand=OUT/'candidates.tsv'
 resume='--resume' in sys.argv
 if resume and inv.exists():
  with inv.open() as f:
   for row in csv.DictReader(f,delimiter='\t'):done.add(row['path']);idx+=1;bytes_total+=int(row['bytes'])
  with cl.open() as f:
   for row in csv.DictReader(f,delimiter='\t'):counts[row['class']]+=1
 elif inv.exists():raise SystemExit('Refusing overwrite; use --resume')
 handles=[x.open('a' if resume else 'x',newline='') for x in (inv,cl,cand)]
 writers=[csv.writer(f,delimiter='\t',lineterminator='\n') for f in handles]
 if not resume:
  for w,h in zip(writers,[['path','bytes','mtime_utc','sha256','git_blob_id'],['inventory_row','class','reason_code'],['inventory_row','path','class','reason_code','signals']]):w.writerow(h)
 batch=[];errors=[]
 def flush():
  nonlocal idx,bytes_total
  if not batch:return
  inp='\n'.join(quote(ROOT/x[0]) for x in batch)+'\n'
  proc=subprocess.run(['git','hash-object','--no-filters','--stdin-paths'],input=inp,text=True,capture_output=True,cwd=REPO)
  if proc.returncode:raise RuntimeError('git hash-object failed: '+proc.stderr)
  ids=proc.stdout.splitlines()
  if len(ids)!=len(batch) or any(not re.fullmatch('[0-9a-f]{40}',x) for x in ids):raise RuntimeError('bad git hash output')
  for (rel,size,mtime,sha,kind,reason,signals),blob in zip(batch,ids):
   idx+=1;writers[0].writerow([rel,size,utc(mtime),sha,blob]);writers[1].writerow([idx,kind,reason]);counts[kind]+=1;bytes_total+=size
   if kind!='unrelated':writers[2].writerow([idx,rel,kind,reason,signals])
  for f in handles:f.flush()
  batch.clear()
  status={'phase':'inventory running','rows':idx,'bytes_hashed':bytes_total,'counts':dict(counts),'elapsed_seconds':round(time.time()-start),'updated_utc':utc(time.time()),'errors':errors}
  (OUT/'inventory_state.json').write_text(json.dumps(status,indent=2))
  if idx%8192==0:print(json.dumps(status),flush=True)
  disk=sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())
  if disk>195*1024*1024:raise RuntimeError('Output nearing 200 MiB limit; stop before adding more')
 try:
  for p in walk():
   rel=str(p.relative_to(ROOT))
   if rel in done:continue
   s=p.lstat()
   if not stat.S_ISREG(s.st_mode):
    errors.append({'path':rel,'error':'non-regular file; no dereference permitted','mode':s.st_mode});continue
   digest=hashlib.sha256();sample=b''
   with p.open('rb') as f:
    while True:
     b=f.read(1024*1024)
     if not b:break
     digest.update(b)
     if len(sample)<200*1024:sample+=(b[:200*1024-len(sample)])
   after=p.stat()
   if (s.st_size,s.st_mtime_ns,s.st_ino)!=(after.st_size,after.st_mtime_ns,after.st_ino):raise RuntimeError('Source changed while hashing: '+rel)
   kind,reason=classify(rel,sample)
   signals=','.join(sorted(set(x.decode('utf-8','replace') for x in SIGNAL.findall(sample))))[:250] if kind!='unrelated' else ''
   batch.append((rel,s.st_size,s.st_mtime,digest.hexdigest(),kind,reason,signals))
   if len(batch)>=256:flush()
  flush()
 finally:
  for f in handles:f.close()
  (OUT/'inventory_errors.json').write_text(json.dumps(errors,indent=2))
 (OUT/'inventory_complete.json').write_text(json.dumps({'rows':idx,'bytes_hashed':bytes_total,'counts':dict(counts),'errors':errors,'completed_utc':utc(time.time())},indent=2))
 print('INVENTORY COMPLETE',idx,dict(counts),flush=True)
if __name__=='__main__':main()
