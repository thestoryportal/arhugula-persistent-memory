#!/usr/bin/env python3
"""Persist bounded semantic extracts and candidate diffs; never decide UNIQUE.

Whole-body comparisons are restricted to files <=200 KiB. Larger documents
are reviewed as streamed sections and explicit content-search evidence.
"""
import collections
import csv
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

OUT=Path(__file__).resolve().parents[1]
ROOT=OUT.parents[1]
LIMIT=200*1024

def rows(name):
    with (OUT/name).open(newline='') as f:yield from csv.DictReader(f,delimiter='\t')

def extracts(p):
    chosen=[];heading=False;line=1;seen=0
    with p.open('r',errors='replace') as f:
        while True:
            s=f.readline(65536)
            if not s:break
            text=s.strip()
            isheading=bool(re.match(r'^#{1,6}\s|^\*\*[^*]+\*\*:|^>.*(?:Status|Version|Authored|Source|Supersedes)|^\s*def ',text))
            if text and (seen<6 or isheading or heading or re.search(r'\b(?:VERDICT|HALTED|CLOSED|supersedes|not recovered|lost with the pod)\b',text)):
                chosen.append({'line':line,'text':text[:1100],'truncated':len(text)>1100})
            heading=isheading
            if text:seen+=1
            line+=s.count('\n')
    return chosen

def body(hit):
    if hit.get('blob'):
        size=int(subprocess.check_output(['git','cat-file','-s',hit['blob']],cwd=ROOT,text=True))
        if size>LIMIT:return None
        data=subprocess.check_output(['git','cat-file','blob',hit['blob']],cwd=ROOT)
        if hit.get('member'):
            import io
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                m=z.getinfo(hit['member'])
                if m.file_size>LIMIT:raise ValueError('Oversize ZIP member')
                data=z.read(m)
        return data
    p=Path(hit['source'])
    if not p.is_absolute():p=ROOT/p
    if not p.is_file():return None
    if hit.get('member'):
        with zipfile.ZipFile(p) as z:
            m=z.getinfo(hit['member'])
            if m.file_size>LIMIT:raise ValueError('Oversize ZIP member')
            return z.read(m)
    if p.stat().st_size>LIMIT:return None
    return p.read_bytes()

def flatten(x,path=''):
    if isinstance(x,dict):
        for k,v in x.items():yield from flatten(v,path+'/'+k)
    elif isinstance(x,list):
        for i,v in enumerate(x):yield from flatten(v,path+'/'+str(i))
    else:yield path,x

def main():
    queue=list(rows('program_search_queue.tsv'))
    evidence=collections.defaultdict(list)
    for line in (OUT/'program_content_evidence.jsonl').open():
        r=json.loads(line);evidence[r['inventory_row']].append(r)
    anchors=collections.defaultdict(list)
    if (OUT/'program_anchor_evidence.jsonl').is_file():
        for line in (OUT/'program_anchor_evidence.jsonl').open():
            r=json.loads(line);anchors[r['row']].append(r)
    initial={r['inventory_row']:r for r in rows('matches.tsv') if r['class']=='program'}
    with (OUT/'program_document_review.jsonl').open('w') as review,(OUT/'program_pair_diffs.jsonl').open('w') as diffs:
        for r in queue:
            if r['search_evidence']=='EXACT-VERIFIED':continue
            key=r['inventory_row'];p=Path('/Volumes/backups')/r['backup']
            if p.suffix!='.skill':
                rec={'row':key,'backup':r['backup'],'bytes':p.stat().st_size,'extracts':extracts(p)}
                review.write(json.dumps(rec)+'\n')
            targets=[]
            old=initial[key]['repo_or_mirror_path']
            if old and initial[key]['match']=='SAME-NAME':targets.append({'source':old,'custody':'initial-basename','member':''})
            for ev in evidence[key]:
                for hit in ev['hits'][:2]:targets.append(hit)
            for ev in anchors[key]:
                for hit in ev['hits'][:2]:targets.append(hit)
            if key in {'216','415','489','102'}:targets.append({'source':str(ROOT/'reproducibility_manifest_merged_s236.json'),'custody':'worktree','member':''})
            done=set()
            for hit in targets:
                ident=(hit['source'],hit.get('member',''),hit.get('blob',''))
                if ident in done:continue
                done.add(ident)
                if p.suffix=='.skill':continue # archive receipt covers all members
                a=p.read_bytes() if p.stat().st_size<=LIMIT else None
                b=body(hit)
                e={'row':key,'backup':r['backup'],'counterpart':hit,'whole_diff_available':a is not None and b is not None}
                if a is not None and b is not None:
                    e['byte_equal']=a==b;e['whitespace_equal']=b''.join(a.split())==b''.join(b.split())
                    if p.suffix=='.json' and not hit.get('member'):
                        try:
                            aj=json.loads(a);bj=json.loads(b);al=dict(flatten(aj));bl=dict(flatten(bj))
                            common=set(al)&set(bl)
                            e['json']={'object_equal':aj==bj,'equal_leaves':sum(al[k]==bl[k] for k in common),'changed':{k:[al[k],bl[k]] for k in common if al[k]!=bl[k]},'backup_only':{k:al[k] for k in set(al)-set(bl)},'counterpart_only_count':len(set(bl)-set(al))}
                        except json.JSONDecodeError as err:e['json_error']=str(err)
                    aa=a.decode('utf8','replace').splitlines();bb=b.decode('utf8','replace').splitlines()
                    delta=list(difflib.unified_diff(aa,bb,n=1))
                    e['diff']=delta
                    e['removed_lines']=sum(s.startswith('-') and not s.startswith('---') for s in delta)
                    e['added_lines']=sum(s.startswith('+') and not s.startswith('+++') for s in delta)
                diffs.write(json.dumps(e)+'\n')
    print('Review extracts and diffs saved; manual semantic/version adjudication required.')

if __name__=='__main__':main()
