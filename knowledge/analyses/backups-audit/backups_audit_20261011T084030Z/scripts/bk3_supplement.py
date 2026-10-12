#!/usr/bin/env python3
"""Supplement BK2 exact-line search with content anchors; source files read-only.

All text is streamed in <=64 KiB pieces. Research text and bounded ZIP members
are searched across the mirror and all indexed reachable historical blobs,
including historical text larger than BK2's 200 KiB exclusion. Numeric JSON
larger than 2 MiB is excluded with a receipt. Hits are candidates, not verdicts.
"""
import collections
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import time
import zipfile

OUT = Path(__file__).resolve().parents[1]
REPO = OUT.parents[1]
MIRROR = Path('/Volumes/memit/llm-database-poc-mirror')
BACKUP = Path('/Volumes/backups')
SKIP = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', '.next', '.cache', 'hf_cache', 'covariance_caches', '.Spotlight-V100', '.Trashes', '.TemporaryItems', '.fseventsd'}
TEXT = {'.md', '.txt', '.yaml', '.yml', '.py', '.bib', '.html', '.bak', '.rst', '.json', '.ipynb'}
WORD = re.compile(rb'[a-z0-9][a-z0-9_-]*')

def rows(name):
    with (OUT/name).open(newline='') as f:
        yield from csv.DictReader(f, delimiter='\t')

def grams(f):
    carry = []
    n = 1
    while True:
        b = f.readline(65536)
        if not b:
            break
        tokens = [(t,n) for t in WORD.findall(b.lower())]
        merged = carry + tokens
        for i in range(max(0, len(merged)-5)):
            g = b' '.join(t for t,_ in merged[i:i+6])
            if len(g) >= 40:
                yield g, merged[i][1]
        carry = merged[-5:]
        n += b.count(b'\n')

def members(path):
    if path.suffix.lower() == '.skill':
        with zipfile.ZipFile(path) as z:
            for m in z.infolist():
                if not m.is_dir():
                    if m.file_size > 200*1024:
                        raise ValueError('Oversize ZIP member '+m.filename)
                    with z.open(m) as f:
                        yield m.filename, dict(grams(f))
    else:
        with path.open('rb') as f:
            yield '', dict(grams(f))

def main():
    started=time.time()
    q=list(rows('program_search_queue.tsv'))
    docs={}; df=collections.Counter()
    for r in q:
        if r['search_evidence'] in {'EXACT-VERIFIED','FILESYSTEM-BYTE-IDENTICAL'}:
            continue
        for member, gs in members(BACKUP/r['backup']):
            key=r['inventory_row']+'!'+member
            docs[key]={'row':r['inventory_row'],'backup':r['backup'],'member':member,'grams':gs}
            df.update(gs)
    inv=collections.defaultdict(list)
    for key,d in docs.items():
        # Shared backups must still be searched: requiring df==1 would leave
        # duplicate/version-family documents with zero usable anchors.
        unique=[g for g in d['grams'] if df[g]==1]
        pool=unique if len(unique)>=32 else sorted(d['grams'],key=lambda g:(df[g],d['grams'][g]))
        if len(unique)>=32:
            selected=[unique[i*(len(unique)-1)//31] for i in range(32)]
        else:
            selected=pool[:32]
        d['anchors']={g:d['grams'][g] for g in selected}
        for g in selected:inv[g].append(key)
    best=collections.defaultdict(list);counts=collections.Counter();errors=[]
    def examine(f,source,member,custody,blob=''):
        found=collections.defaultdict(dict)
        for g,n in grams(f):
            for key in inv.get(g,()):found[key].setdefault(g,n)
        for key,hit in found.items():
            if len(hit)<2:continue
            e={'source':source,'member':member,'custody':custody,'blob':blob,'anchor_hits':len(hit),'anchor_total':len(docs[key]['anchors']),'pairs':[{'backup_line':docs[key]['anchors'][g],'counterpart_line':n,'anchor':g.decode()} for g,n in hit.items()]}
            best[key].append(e)
            best[key].sort(key=lambda x:(x['anchor_hits'],x['custody']=='worktree'),reverse=True)
            del best[key][8:]
    for directory,dirs,files in os.walk(MIRROR,followlinks=False):
        if Path(directory)==OUT:
            dirs.clear();continue
        dirs[:]=[d for d in dirs if d not in SKIP]
        for name in files:
            p=Path(directory)/name
            if p.suffix.lower() not in TEXT|{'.skill'}:continue
            try:
                if not p.is_file():continue
                if p.suffix.lower() in {'.json','.ipynb'} and p.stat().st_size>2*1024*1024:
                    counts['large_numeric_excluded']+=1;continue
                custody='worktree' if p.is_relative_to(REPO) else 'mirror-outside-worktree'
                if p.suffix.lower()=='.skill':
                    with zipfile.ZipFile(p) as z:
                        for m in z.infolist():
                            if m.is_dir():continue
                            if m.file_size>200*1024:raise ValueError('Oversize ZIP member '+m.filename)
                            with z.open(m) as f:examine(f,str(p),m.filename,custody)
                else:
                    with p.open('rb') as f:examine(f,str(p),'',custody)
                counts['filesystem_files_searched']+=1
            except (OSError,ValueError,zipfile.BadZipFile) as e:errors.append(str(p)+': '+str(e))
    for r in rows('history_blobs.tsv'):
        path=r['representative_history_path'];suffix=Path(path).suffix.lower();size=int(r['bytes'])
        if suffix not in TEXT|{'.skill'}:continue
        if suffix in {'.json','.ipynb'} and size>2*1024*1024:
            counts['large_historical_numeric_excluded']+=1;continue
        proc=subprocess.Popen(['git','cat-file','blob',r['git_blob_id']],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if suffix=='.skill':
            if size>200*1024:raise ValueError('Oversize historical ZIP')
            data=proc.stdout.read(200*1024+1)
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for m in z.infolist():
                    if not m.is_dir():
                        if m.file_size>200*1024:raise ValueError('Oversize historical member')
                        with z.open(m) as f:examine(f,path,m.filename,'reachable-history',r['git_blob_id'])
        else:examine(proc.stdout,path,'','reachable-history',r['git_blob_id'])
        err=proc.stderr.read(65536);rc=proc.wait()
        if rc:raise RuntimeError(err.decode())
        counts['historical_blobs_searched']+=1
    with (OUT/'program_anchor_evidence.jsonl').open('w') as f:
        for key,d in docs.items():
            rec={k:v for k,v in d.items() if k not in {'grams','anchors'}}
            rec.update(query=key,anchor_total=len(d['anchors']),anchors=[{'text':g.decode(),'backup_line':n} for g,n in d['anchors'].items()],hits=best[key])
            f.write(json.dumps(rec)+'\n')
    state={'counts':dict(counts),'errors':errors,'seconds':round(time.time()-started,2),'queries':len(docs),'limits':'Six-token anchors, punctuation/case/line-wrap independent; best eight candidates only; numeric JSON/IPYNB >2 MiB and dependency/cache trees excluded; no automatic uniqueness or chronology claim.'}
    (OUT/'program_anchor_state.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(state),flush=True)

if __name__=='__main__':main()
