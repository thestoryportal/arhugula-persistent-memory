#!/usr/bin/env python3
"""Exercise EXACT before any fallback; verify real duplicate bytes and commit/path."""
import csv,json,hashlib,subprocess
from pathlib import Path
from match_files import identity_match
OUT=Path(__file__).resolve().parents[1];REPO=OUT.parents[1]
index={r['git_blob_id']:r for r in csv.DictReader((OUT/'history_blobs.tsv').open(),delimiter='\t')}
locations=json.loads((OUT/'blob_locations.json').read_text())
name='ConnectedPapers-for-AlphaEdit%3A-Null%20Space-Constrained-Knowledge-Editing-for-Language-Models.bib'
backup=Path('/Volumes/backups')/name;repo=REPO/'research_and_specs'/name
assert backup.stat().st_size<=200*1024 and repo.stat().st_size<=200*1024
assert backup.read_bytes()==repo.read_bytes(),'Control is not byte-identical'
def git(args):
 p=subprocess.run(['git']+args,cwd=REPO,capture_output=True,text=True)
 if p.returncode or not p.stdout.strip():raise RuntimeError(p.stderr or 'Empty git result')
 return p.stdout.strip()
blob=git(['hash-object','--no-filters',str(backup)]);repo_blob=git(['hash-object','--no-filters',str(repo)])
fallback_calls=0
def route(oid):
 global fallback_calls
 if identity_match(oid,index)=='EXACT':return 'EXACT'
 fallback_calls+=1
 return 'UNIQUE_CANDIDATE'
assert route(blob)=='EXACT';assert fallback_calls==0;assert blob==repo_blob
loc=locations[blob];tree=git(['ls-tree',loc['commit'],'--',loc['path']]);assert blob in tree
receipt={'backup_path':str(backup),'repo_path':str(repo),'bytes':backup.stat().st_size,'sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),'git_blob_id':blob,'result':'EXACT','unique_fallback_calls':fallback_calls,'location':loc,'ls_tree_receipt':tree,'byte_identity_verified':True}
(OUT/'positive_control.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
