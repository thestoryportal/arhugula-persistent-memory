"""Freeze literal scope and v4 pins after sandbox/host evidence has settled; stdlib only."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
K=ROOT/'results/backup_gdrive_host_20261011/r12_package_20261011T024815Z'

def main():
    chosen=set((HERE/'selected_committed_paths.txt').read_text().splitlines())
    chosen.update((K/'scope_allowlist.txt').read_text().splitlines())
    # Discovery generates literal output. The exporter never uses discovery or globs.
    chosen.update(str(p.relative_to(ROOT)) for p in HERE.rglob('*') if p.is_file()
                  and 'operational_checks' not in p.relative_to(HERE).parts)
    chosen.update(str((HERE/p).relative_to(ROOT)) for p in ('scope_allowlist.txt','pins_v4.sha256','pins_v4.json'))
    (HERE/'scope_allowlist.txt').write_text('\n'.join(sorted(chosen))+'\n')
    self_pins={str((HERE/p).relative_to(ROOT)) for p in ('pins_v4.sha256','pins_v4.json')}
    files=[]
    for name in sorted(chosen-self_pins):
        path=ROOT/name
        if path.is_symlink() or not path.is_file() or path.stat().st_size>1000000:
            raise ValueError('candidate input must be regular and <=1 MB: '+name)
        files.append(dict(path=name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                          bytes=path.stat().st_size,mode=path.stat().st_mode&0o777))
    (HERE/'pins_v4.sha256').write_text(''.join(x['sha256']+'  '+x['path']+'\n' for x in files))
    metadata=dict(schema_version=4,supersedes=[dict(path=str((K/p).relative_to(ROOT)),
                  sha256=hashlib.sha256((K/p).read_bytes()).hexdigest()) for p in ('pins_v3.sha256','pins_v3.json')],
                  source_context=json.loads((HERE/'source_context.json').read_text()),
                  scope_contract='K12 amendment retained; complete index and commit path/type/blob/mode trees equal base plus literal source overlay; only parent=origin/master; verified commit bound to PR and remote heads and gate report; all nine input hashes retained',
                  operational_checks='Outside candidate scope; final gate receipts do not pin themselves',
                  self_pin_contract='The two pin files cannot hash themselves; candidate verifies exact source bytes and compares both manifests with this reviewed receipt',
                  files=files)
    (HERE/'pins_v4.json').write_text(json.dumps(metadata,indent=2,sort_keys=True)+'\n')
    for name in chosen:
        if (ROOT/name).stat().st_size>1000000: raise ValueError('evidence exceeds 1 MB: '+name)
    print('FROZEN',len(chosen),'literal scope paths;',len(files),'SHA-256 pins; bytes',sum((ROOT/n).stat().st_size for n in chosen))

if __name__=='__main__': main()
