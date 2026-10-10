"""Read-only listing and SHA-256 receipt for the production paths in criterion 5."""
import hashlib
import json
from pathlib import Path
import stat
import sys

home = Path.home()
roots = sorted((home/"Library/Logs").glob("memit-gdrive-backup*"))
roots += [home/"Applications/MemitGdriveBackup.app", home/"Library/LaunchAgents"]
entries = []

def visit(path):
    try:
        info = path.lstat()
    except FileNotFoundError:
        entries.append({"path": str(path), "type": "absent"})
        return
    entry = {"path": str(path), "mode": stat.S_IMODE(info.st_mode), "mtime_ns": info.st_mtime_ns}
    if stat.S_ISLNK(info.st_mode):
        entry.update(type="symlink", target=str(path.readlink()))
    elif stat.S_ISDIR(info.st_mode):
        entry.update(type="directory")
    elif stat.S_ISREG(info.st_mode):
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024*1024), b""):
                digest.update(block)
        after = path.stat()
        if (info.st_ino, info.st_size, info.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
            raise RuntimeError("Production file changed during observation: "+str(path))
        entry.update(type="file", size_bytes=info.st_size, sha256=digest.hexdigest())
    else:
        entry.update(type="other")
    entries.append(entry)
    if stat.S_ISDIR(info.st_mode):
        for child in sorted(path.iterdir()):
            visit(child)

for root in roots:
    visit(root)
result = {"real_home": str(home), "backup_glob_roots": [str(p) for p in roots[:-2]],
          "entries": sorted(entries, key=lambda entry: entry["path"])}
Path(sys.argv[1]).write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
print("Read-only production listing:",len(entries),"entries ->",sys.argv[1])
