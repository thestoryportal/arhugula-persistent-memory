"""Committed-byte export and exact backup candidate gate. No network or PR operations."""
import argparse
import hashlib
import os
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

def full_sha(value):
    if not isinstance(value,str) or not re.fullmatch(r'[0-9a-f]{40}',value):
        raise ValueError('requires full 40-hex SHA')
    return value

def commit_sha(root,value):
    full_sha(value)
    if git(root,'cat-file','-t',value).strip()!=b'commit':
        raise ValueError('SHA is not a commit')
    return value

def tree_entries(root,sha):
    result={}
    for row in git(root,'ls-tree','-r','-z',sha).split(b'\0'):
        if not row: continue
        meta,path=row.split(b'\t',1); mode,kind,blob=meta.decode('ascii').split()
        name=os.fsdecode(path)
        if name in result: raise ValueError('scope duplicate tree path')
        result[name]=(mode,kind,full_sha(blob))
    return result

def index_entries(root):
    result={}
    for row in git(root,'ls-files','-s','-z').split(b'\0'):
        if not row: continue
        meta,path=row.split(b'\t',1); mode,blob,stage=meta.decode('ascii').split()
        name=os.fsdecode(path)
        if stage!='0' or name in result: raise ValueError('scope unmerged or duplicate index path')
        result[name]=(mode,'commit' if mode=='160000' else 'blob',full_sha(blob))
    return result

def expected_tree(target,source):
    allowlist=paths(); unchanged=unchanged_paths(allowlist)
    source=commit_sha(target,source)
    base_sha=commit_sha(target,git(target,'rev-parse','origin/master').decode().strip())
    base=tree_entries(target,base_sha); source_tree=tree_entries(target,source)
    expected=dict(base)
    for name in allowlist:
        entry=source_tree.get(name)
        if not entry or entry[1]!='blob' or entry[0] not in ('100644','100755'):
            raise ValueError('scope rejects missing/nonregular source file: '+name)
        content=git(target,'cat-file','blob',entry[2])
        if name.startswith('results/') and len(content)>1000000:
            raise ValueError('scope evidence exceeds 1 MB: '+name)
        expected[name]=entry
    for name in unchanged:
        if base.get(name)!=expected[name]:
            raise ValueError('scope false unchanged declaration: '+name)
    changed={name for name in set(base)|set(expected) if base.get(name)!=expected.get(name)}
    if changed!=set(allowlist)-set(unchanged):
        raise ValueError('scope exact diff mismatch against declared unchanged paths')
    return base_sha,expected

def object_pins(target,actual):
    allowlist=paths(); unchanged=unchanged_paths(allowlist)
    # v3 is retained solely for the byte-identical K12 synthetic fixture contract.
    version='v4' if (HERE/'pins_v4.sha256').exists() else 'v3'
    pin_names=set()
    for line in (HERE/('pins_'+version+'.sha256')).read_text().splitlines():
        digest,name=line.split('  ',1)
        if name in pin_names or name not in allowlist or not re.fullmatch('[0-9a-f]{64}',digest):
            raise ValueError('invalid or out-of-scope pin: '+name)
        pin_names.add(name)
        # actual is the index or verified commit tree, never the working tree.
        data=git(target,'cat-file','blob',actual[name][2])
        if hashlib.sha256(data).hexdigest()!=digest: raise ValueError('pin mismatch: '+name)
    if not set(unchanged)<=pin_names: raise ValueError('scope unchanged input lacks SHA-256 pin')
    for suffix in ('sha256','json'):
        filename='pins_'+version+'.'+suffix; manifest=HERE/filename
        if manifest.exists():
            for name in allowlist:
                if name.endswith('/'+filename) and git(target,'cat-file','blob',actual[name][2])!=manifest.read_bytes():
                    raise ValueError('pin manifest mismatch: '+name)
    return len(pin_names)

def candidate_target(target):
    target=Path(target).resolve()
    if git(target,'branch','--show-current').decode().strip()!=BRANCH:
        raise ValueError('scope branch must be '+BRANCH)
    return target

def compare_tree(actual,expected,label):
    if actual!=expected:
        mismatch=sorted(name for name in set(actual)|set(expected) if actual.get(name)!=expected.get(name))
        raise ValueError('scope '+label+' tree mismatch: '+repr(mismatch))

def verify_staged(target,source):
    target=candidate_target(target); _,expected=expected_tree(target,source)
    actual=index_entries(target); compare_tree(actual,expected,'index')
    pins=object_pins(target,actual)
    try: git(target,'diff','--quiet','--no-ext-diff','--ignore-submodules=none')
    except ValueError as exc: raise ValueError('working tree differs from index: '+str(exc)) from exc
    if git(target,'ls-files','--others','-z'):
        raise ValueError('scope contains untracked files (including ignored files)')
    print('PASS exact index path/blob/type/mode tree, clean working tree and '+str(pins)+' object SHA-256 pins')

# Historical K12 API now delegates to the staged gate; no working-tree byte verifier remains.
def verify(target,source):
    verify_staged(target,source)

def verify_commit(target,source,sha,receipt_file=None):
    target=candidate_target(target); sha=commit_sha(target,sha)
    base_sha,expected=expected_tree(target,source)
    parents=git(target,'rev-list','--parents','-n','1',sha).decode().split()
    if parents!=[sha,base_sha]: raise ValueError('commit only parent must be origin/master')
    actual=tree_entries(target,sha); compare_tree(actual,expected,'commit')
    pins=object_pins(target,actual)
    receipt=Path(receipt_file) if receipt_file is not None else HERE/'operational_checks/verified_commit_sha.txt'
    receipt.parent.mkdir(parents=True,exist_ok=True)
    with receipt.open('x') as stream:
        stream.write(sha+'\n'); stream.flush(); os.fsync(stream.fileno())
    print('PASS exact commit path/blob/type/mode tree, single base parent and '+str(pins)+' object SHA-256 pins; verified SHA '+sha+' -> '+str(receipt))
    return sha

def verified_sha(receipt_file):
    value=Path(receipt_file).read_text()
    if not re.fullmatch(r'[0-9a-f]{40}\n?',value): raise ValueError('verified receipt requires full 40-hex SHA')
    return full_sha(value.rstrip('\n'))

def verify_pr_head(receipt_file,observed_head,observed_remote):
    sha=verified_sha(receipt_file); full_sha(observed_head); full_sha(observed_remote)
    if not sha==observed_head==observed_remote:
        raise ValueError('PR head binding mismatch: verified='+sha+' PR='+observed_head+' remote='+observed_remote)
    print('PASS verified commit = observed PR head = observed remote branch '+sha)
    return sha

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
    verify_staged(target,source)

def main():
    parser=argparse.ArgumentParser(description=__doc__); sub=parser.add_subparsers(dest='mode',required=True)
    creation=sub.add_parser('create'); creation.add_argument('source_repo'); creation.add_argument('source_commit'); creation.add_argument('candidate_path')
    for name in ('verify','verify-staged','verify-commit'):
        check=sub.add_parser(name); check.add_argument('candidate_path'); check.add_argument('source_commit')
        if name=='verify-commit': check.add_argument('commit_sha'); check.add_argument('--receipt-file',type=Path)
    binding=sub.add_parser('verify-pr-head'); binding.add_argument('verified_sha_file'); binding.add_argument('observed_head_sha'); binding.add_argument('observed_remote_sha')
    args=parser.parse_args()
    try:
        if args.mode=='create': create(args.source_repo,args.source_commit,args.candidate_path)
        elif args.mode=='verify-commit': verify_commit(args.candidate_path,args.source_commit,args.commit_sha,args.receipt_file)
        elif args.mode=='verify-pr-head': verify_pr_head(args.verified_sha_file,args.observed_head_sha,args.observed_remote_sha)
        else: verify_staged(args.candidate_path,args.source_commit)
    except (OSError,ValueError) as exc:
        print('FAIL '+str(exc),file=sys.stderr); return 1
    return 0
if __name__=='__main__': raise SystemExit(main())
