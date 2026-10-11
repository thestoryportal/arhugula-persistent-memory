"""Synthetic-only RED adapter of v2's missing complete-diff gate; not reviewed code."""
from pathlib import Path
import hashlib
import subprocess
import sys

HERE=Path(__file__).resolve().parent
def git(root,*args):
    return subprocess.run(['/usr/bin/git','-C',str(root),*args],check=True,capture_output=True).stdout

def main():
    mode,*args=sys.argv[1:]
    root=Path(args[0]).resolve()
    root.relative_to('/private/tmp')
    if mode=='create':
        root,source,target=args; target=Path(target)
        git(root,'worktree','add','-b','backup-gdrive-r12',str(target),'origin/master')
        for name in (HERE/'scope_allowlist.txt').read_text().splitlines():
            path=target/name; path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(git(root,'show',source+':'+name))
        git(target,'add','--',*(HERE/'scope_allowlist.txt').read_text().splitlines())
    else: target=root
    for line in (HERE/'pins_v3.sha256').read_text().splitlines():
        digest,name=line.split('  ',1)
        if hashlib.sha256((target/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('pin mismatch '+name)
    print('PASS pins; v2 has no complete diff assertion')
if __name__=='__main__': main()
