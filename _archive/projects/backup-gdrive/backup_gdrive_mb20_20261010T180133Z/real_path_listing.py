"""Read-only real HOME inventory; never follows directory symlinks."""
import hashlib
import json
from pathlib import Path
import stat
import sys

home = Path.home()
roots = sorted((home/"Library/Logs").glob("memit-gdrive-backup*"))
roots += [home/"Applications/MemitGdriveBackup.app", home/"Library/LaunchAgents"]
rows = []
def visit(path):
    if not path.exists() and not path.is_symlink():
        rows.append({"path": str(path), "kind": "absent"})
        return
    info = path.lstat()
    row = {"path": str(path), "mode": info.st_mode, "size": info.st_size,
           "mtime_ns": info.st_mtime_ns}
    if stat.S_ISREG(info.st_mode):
        row.update(kind="file", sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    elif stat.S_ISLNK(info.st_mode):
        row.update(kind="symlink", target=str(path.readlink()))
    elif stat.S_ISDIR(info.st_mode):
        row.update(kind="directory")
    else:
        row.update(kind="special")
    rows.append(row)
    if stat.S_ISDIR(info.st_mode):
        for child in sorted(path.iterdir()):
            visit(child)
for path in roots:
    visit(path)
Path(sys.argv[1]).write_text(json.dumps(rows, indent=2, sort_keys=True)+"\n")
