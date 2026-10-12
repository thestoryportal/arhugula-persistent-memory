#!/usr/bin/env python3
"""Compare every member in PROGRAM skill archives without executing any skill."""
import csv
import difflib
import json
from pathlib import Path
import zipfile

OUT=Path(__file__).resolve().parents[1]
ROOT=OUT.parents[1]

def load(path):
    with zipfile.ZipFile(path) as z:
        result={}
        for m in z.infolist():
            if m.is_dir():continue
            if m.file_size>200*1024:raise ValueError('Oversize member '+m.filename)
            result[m.filename]=z.read(m)
        return result

def main():
    with (OUT/'program_archive_comparisons.jsonl').open('w') as out:
        for r in csv.DictReader((OUT/'program_search_queue.tsv').open(),delimiter='\t'):
            b=Path('/Volumes/backups')/r['backup']
            if b.suffix!='.skill' or r['search_evidence'] in {'EXACT-VERIFIED','FILESYSTEM-BYTE-IDENTICAL'}:continue
            repo=ROOT/'skills'/b.name.lower().replace(' (1)','')
            bm=load(b)
            if not repo.is_file():
                e={'row':r['inventory_row'],'backup':r['backup'],'counterpart':None,'backup_members':list(bm),'result':'No same-role archive counterpart; content-search review required'}
            else:
                rm=load(repo)
                bl={str(Path(k).name):v for k,v in bm.items()};rl={str(Path(k).name):v for k,v in rm.items()}
                if len(bl)!=len(bm) or len(rl)!=len(rm):raise ValueError('Repeated logical member names')
                e={'row':r['inventory_row'],'backup':r['backup'],'counterpart':str(repo),'backup_members':list(bm),'repo_members':list(rm),'all_member_names_equal':set(bm)==set(rm),'logical_members_equal':set(bl)==set(rl),'members':[]}
                for member in sorted(set(bl)|set(rl)):
                    a=bl.get(member,b'');c=rl.get(member,b'')
                    diff=list(difflib.unified_diff(a.decode('utf8','replace').splitlines(),c.decode('utf8','replace').splitlines(),n=1))
                    e['members'].append({'member':member,'backup_bytes':len(a),'repo_bytes':len(c),'byte_equal':a==c,'whitespace_equal':b''.join(a.split())==b''.join(c.split()),'diff':diff})
            out.write(json.dumps(e)+'\n')
            print(r['inventory_row'],r['backup'],json.dumps({m['member']:('BYTE' if m['byte_equal'] else 'WHITESPACE' if m['whitespace_equal'] else 'DIVERGENT') for m in e.get('members',[])}))
            for m in e.get('members',[]):
                if not m['whitespace_equal']:print('\n'.join(m['diff'][:24]))

if __name__=='__main__':main()
