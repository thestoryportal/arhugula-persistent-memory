#!/bin/bash
# Verified archival only. Local removal is a separate operator-approved action.
set -euo pipefail
SCRIPT_DIR="$(/usr/bin/dirname "$0")"
exec "${ARCHIVE_PYTHON:-/usr/bin/python3}" - "$SCRIPT_DIR/.." "$@" <<'PY'
import fcntl
import hashlib
import os
from pathlib import Path
import subprocess
import sys

def digest(path):
    sha = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            sha.update(block)
            size += len(block)
    return sha.hexdigest(), size

def main():
    if len(sys.argv) < 3:
        raise ValueError('usage: archive_to_gdrive.sh <path...>')
    root = Path(os.environ.get('ARCHIVE_ROOT', sys.argv[1])).resolve(strict=True)
    remote = os.environ.get('ARCHIVE_DEST', 'gdrive:memit-archive').rstrip('/')
    rclone = os.environ.get('ARCHIVE_RCLONE', '/opt/homebrew/bin/rclone')
    manifest = Path(os.environ.get('ARCHIVE_MANIFEST', str(root/'docs/ARCHIVE_MANIFEST.tsv')))
    if not remote or any(char in remote for char in '\t\r\n'):
        raise ValueError('invalid archive destination')
    sources = []
    for raw in sys.argv[2:]:
        path = Path(raw).absolute()
        if path.is_symlink() or not path.is_file():
            raise ValueError('archive requires regular files: '+raw)
        source = path.resolve(strict=True)
        relative = source.relative_to(root).as_posix()
        if any(char in relative for char in '\t\r\n'):
            raise ValueError('path cannot be represented in archive TSV: '+repr(relative))
        sources.append((source, relative))
    for source, relative in sources:
        sha, size = digest(source)
        target = remote+'/'+relative
        parent = target.rsplit('/', 1)[0]
        # Existing objects stay intact; the download check admits identical bytes.
        subprocess.run([rclone, 'copy', str(source), parent+'/', '--immutable', '--ignore-existing', '--checksum'], check=True)
        subprocess.run([rclone, 'check', str(source), parent+'/', '--download', '--one-way'], check=True)
        if digest(source) != (sha, size):
            raise ValueError('source changed during archive verification: '+str(source))
        try:
            manifest.parent.mkdir(parents=True, exist_ok=True)
            with manifest.open('a+') as stream:
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
                stream.seek(0)
                header = stream.readline()
                if header and header != 'sha256\tsize_bytes\tremote_path\n':
                    raise ValueError('invalid manifest header')
                stream.seek(0, os.SEEK_END)
                stream.write(('' if header else 'sha256\tsize_bytes\tremote_path\n')+
                             sha+'\t'+str(size)+'\t'+target+'\n')
                stream.flush()
                os.fsync(stream.fileno())
        except (OSError, ValueError) as exc:
            raise ValueError('manifest publication failed: '+str(exc)) from exc
        print('archive_to_gdrive: VERIFIED '+target+' sha256='+sha+' bytes='+str(size)+'; local copy retained')
    return 0

try:
    sys.exit(main())
except (OSError, ValueError, subprocess.CalledProcessError) as exc:
    print('archive_to_gdrive: FAILED: '+str(exc).replace('\n', ' '), file=sys.stderr)
    sys.exit(1)
PY
