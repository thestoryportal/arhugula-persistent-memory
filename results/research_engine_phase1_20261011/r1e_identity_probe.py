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
    rows = []
    def traversal_error(error):
        raise error
    for base, directories, files in os.walk(str(root), followlinks=False, onerror=traversal_error):
        for name in directories + files:
            path = Path(base) / name
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                text = os.readlink(str(path))
                target = path.resolve(strict=True)
                target_mode = target.stat().st_mode
                if stat.S_ISREG(target_mode):
                    rows.append([relative, 'symlink', text, str(target), 'file', file_sha256(target)])
                elif stat.S_ISDIR(target_mode):
                    if target != root and root not in target.parents:
                        raise ValueError('Stdlib directory symlink escapes inventory: ' + str(path))
                    rows.append([relative, 'symlink', text, str(target), 'directory'])
                else:
                    raise ValueError('Unsupported stdlib symlink target: ' + str(path))
            elif stat.S_ISREG(mode):
                rows.append([relative, file_sha256(path)])
            elif not stat.S_ISDIR(mode):
                raise ValueError('Unsupported stdlib entry: ' + str(path))
        # Internal directory targets are enumerated at their actual in-root paths.
        directories[:] = [name for name in directories if not (Path(base) / name).is_symlink()]
    h = hashlib.sha256()
    for row in sorted(rows):
        h.update((json.dumps(row, separators=(',', ':')) + '\n').encode('utf-8'))
    return {'directory': str(root), 'sha256': h.hexdigest(), 'file_count': len(rows)}


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
