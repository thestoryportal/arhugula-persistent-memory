"""Read-only interpreter identity; the collector imports these same functions."""
import hashlib
import json
import os
from pathlib import Path
import platform
import stat
import sys
import sysconfig


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def stdlib_identity(directory=None):
    root = Path(directory or sysconfig.get_path('stdlib')).resolve(strict=True)
    paths = []
    for base, directories, files in os.walk(str(root), followlinks=False):
        directories[:] = [name for name in directories if not (Path(base) / name).is_symlink()]
        for name in files:
            path = Path(base) / name
            if stat.S_ISREG(path.lstat().st_mode):
                paths.append(path.relative_to(root).as_posix())
    h = hashlib.sha256()
    for relative in sorted(paths):
        row = json.dumps([relative, file_sha256(root / relative)], separators=(',', ':')) + '\n'
        h.update(row.encode('utf-8'))
    return {'directory': str(root), 'sha256': h.hexdigest(), 'file_count': len(paths)}


def interpreter_identity():
    executable = sys.executable
    realpath = os.path.realpath(executable)
    return {'executable': executable, 'realpath': realpath,
        'executable_sha256': file_sha256(realpath), 'version_info': list(sys.version_info),
        'machine': platform.machine(), 'mac_ver': list(platform.mac_ver()),
        'flags': {'isolated': sys.flags.isolated, 'dont_write_bytecode': sys.flags.dont_write_bytecode},
        'hostname': platform.node(), 'stdlib': stdlib_identity()}


if __name__ == '__main__':
    print(json.dumps(interpreter_identity(), sort_keys=True, allow_nan=False))
