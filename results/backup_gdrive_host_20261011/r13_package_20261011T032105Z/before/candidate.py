"""Committed-byte export and exact backup candidate gate. No network or PR operations."""
import argparse
import hashlib
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

HERE=Path(__file__).resolve().parent
BRANCH='backup-gdrive-r12'

def git(root,*args):
    proc=subprocess.run(['/usr/bin/git','-C',str(root),*args],capture_output=True)
    if proc.returncode:
        raise ValueError('git '+repr(args)+' failed: '+proc.stderr.decode('utf-8','replace'))
    return proc.stdout

def paths():
    value=(HERE/'scope_allowlist.txt').read_text().splitlines()
    if not value or value!=sorted(set(value)):
        raise ValueError('scope allowlist must be nonempty, sorted and unique')
    for name in value:
        if (not name or PurePosixPath(name).is_absolute() or '..' in PurePosixPath(name).parts or
                str(PurePosixPath(name))!=name or re.search(r'[\s*?\[\]\\]',name)):
            raise ValueError('scope requires literal normalized paths: '+name)
    return value

def unchanged_paths(allowlist):
    manifest=HERE/'scope_unchanged.txt'
    value=manifest.read_text().splitlines() if manifest.exists() else []
    if value!=sorted(set(value)) or not set(value)<=set(allowlist):
        raise ValueError('scope unchanged exceptions must be unique allowlisted paths')
    return value

def entries(root,source,allowlist):
    if not re.fullmatch(r'[0-9a-f]{40}',source): raise ValueError('source must be full commit SHA')
    if git(root,'cat-file','-t',source).strip()!=b'commit': raise ValueError('source is not a commit')
    result={}
    for name in allowlist:
        row=git(root,'ls-tree',source,'--',name).decode().strip()
        if not row: raise ValueError('scope source has no committed file: '+name)
        meta,path=row.split('\t',1); mode,kind,blob=meta.split()
        if path!=name or kind!='blob' or mode not in ('100644','100755'):
            raise ValueError('scope rejects nonregular file: '+name)
        data=git(root,'cat-file','blob',blob)
        if name.startswith('results/') and len(data)>1000000:
            raise ValueError('scope evidence exceeds 1 MB: '+name)
        result[name]=(int(mode,8)&0o777,data)
    return result

def verify(target,source):
    target=Path(target).resolve(); allowlist=paths()
    if git(target,'branch','--show-current').decode().strip()!=BRANCH:
        raise ValueError('scope branch must be '+BRANCH)
    actual=git(target,'diff','--name-only','-z','origin/master').decode().split('\x00')[:-1]
    unchanged=unchanged_paths(allowlist)
    changed=sorted(set(allowlist)-set(unchanged))
    if sorted(actual)!=changed:
        raise ValueError('scope exact diff mismatch: extra='+repr(sorted(set(actual)-set(changed)))+
                         '; missing='+repr(sorted(set(changed)-set(actual))))
    if git(target,'ls-files','--others','--exclude-standard','-z'):
        raise ValueError('scope contains untracked files')
    expected=entries(target,source,allowlist)
    for name in unchanged:
        row=git(target,'ls-tree','origin/master','--',name).decode().strip()
        if not row: raise ValueError('scope false unchanged declaration: '+name)
        meta,path=row.split('\t',1); mode,kind,blob=meta.split()
        if (path!=name or kind!='blob' or mode not in ('100644','100755') or
                expected[name]!=(int(mode,8)&0o777,git(target,'cat-file','blob',blob))):
            raise ValueError('scope false unchanged declaration: '+name)
    for name,(mode,data) in expected.items():
        path=target/name
        if path.is_symlink() or not path.is_file() or path.read_bytes()!=data or path.stat().st_mode&0o777!=mode:
            raise ValueError('source byte/mode mismatch: '+name)
    pin_names=set()
    for line in (HERE/'pins_v3.sha256').read_text().splitlines():
        digest,name=line.split('  ',1)
        if name in pin_names or name not in allowlist or not re.fullmatch('[0-9a-f]{64}',digest):
            raise ValueError('invalid or out-of-scope pin: '+name)
        pin_names.add(name)
        if hashlib.sha256((target/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('pin mismatch: '+name)
    if not set(unchanged)<=pin_names: raise ValueError('scope unchanged input lacks SHA-256 pin')
    # Pin files cannot hash themselves; compare their complete bytes to the reviewed receipt.
    for name in ('pins_v3.sha256','pins_v3.json'):
        path=HERE/name
        if path.exists():
            matches=[p for p in allowlist if p.endswith('/'+name)]
            for p in matches:
                if (target/p).read_bytes()!=path.read_bytes(): raise ValueError('pin manifest mismatch: '+p)
    print('PASS exact scope, committed bytes/modes, branch and '+str(len(pin_names))+' SHA-256 pins')

def create(repo,source,target):
    repo=Path(repo).resolve(); target=Path(target).resolve()
    allowlist=paths(); content=entries(repo,source,allowlist)
    if target.exists(): raise ValueError('candidate path must be fresh')
    git(repo,'worktree','add','-b',BRANCH,str(target),'origin/master')
    for name,(mode,data) in content.items():
        path=target/name; path.parent.mkdir(parents=True,exist_ok=True)
        if path.is_symlink(): raise ValueError('refusing symlink destination: '+name)
        path.write_bytes(data); path.chmod(mode)
    git(target,'add','-f','--',*allowlist)
    verify(target,source)

def main():
    parser=argparse.ArgumentParser(description=__doc__); sub=parser.add_subparsers(dest='mode',required=True)
    creation=sub.add_parser('create'); creation.add_argument('source_repo'); creation.add_argument('source_commit'); creation.add_argument('candidate_path')
    check=sub.add_parser('verify'); check.add_argument('candidate_path'); check.add_argument('source_commit')
    args=parser.parse_args()
    try:
        if args.mode=='create': create(args.source_repo,args.source_commit,args.candidate_path)
        else: verify(args.candidate_path,args.source_commit)
    except (OSError,ValueError) as exc:
        print('FAIL '+str(exc),file=sys.stderr); return 1
    return 0
if __name__=='__main__': raise SystemExit(main())
