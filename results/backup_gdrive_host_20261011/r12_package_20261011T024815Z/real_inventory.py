"""Read-only backup roots inventory, using explicit operator HOME, never symlink traversal."""
import argparse
import hashlib
import json
from pathlib import Path
import stat

def inventory(home):
    home=Path(home)
    roots=set((home/'Library/Logs').glob('memit-gdrive-backup*'))
    roots.update(Path('/Library/Logs').glob('memit-gdrive-backup*'))
    roots.update([home/'Library/Logs/memit-gdrive-backup',home/'Library/Logs/memit-gdrive-backup-launch-state',
        home/'Library/Logs/memit-gdrive-backup-launch-journal',home/'Library/Logs/memit-gdrive-backup.lock',
        home/'Library/Logs/memit-gdrive-backup.log',home/'Library/Logs/memit-gdrive-backup.launchd.log',
        home/'Applications/MemitGdriveBackup.app',home/'Library/LaunchAgents',
        home/'Library/Application Support/memit-gdrive-backup',Path('/Library/Logs/memit-gdrive-backup')])
    rows=[]
    def visit(path):
        try: info=path.lstat()
        except FileNotFoundError:
            rows.append(dict(path=str(path),kind='absent')); return
        row=dict(path=str(path),mode=info.st_mode,size=info.st_size,mtime_ns=info.st_mtime_ns)
        if stat.S_ISREG(info.st_mode): row.update(kind='file',sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        elif stat.S_ISLNK(info.st_mode): row.update(kind='symlink',target=str(path.readlink()))
        elif stat.S_ISDIR(info.st_mode): row.update(kind='directory')
        else: row.update(kind='special')
        rows.append(row)
        if stat.S_ISDIR(info.st_mode):
            for child in sorted(path.iterdir()): visit(child)
    for root in sorted(roots): visit(root)
    return json.dumps(rows,sort_keys=True,indent=2)+'\n'

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('home',type=Path); parser.add_argument('output',type=Path)
    args=parser.parse_args(); args.output.write_text(inventory(args.home))
