#!/usr/bin/python3
"""Intel half of step 1; sent on stdin, stdlib only, no route to the M3.

inventory [--root PATH]; verify GEN MANIFEST_SHA256 [--root PATH]
The default root is ~/memit_copy. --root exists for local fixture execution.
"""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import traceback

CAP = 250_000_000_000
FLOOR = 80_000_000_000


def safe_path(value):
    if not isinstance(value, str) or not value or '\x00' in value:
        raise ValueError('invalid relative path')
    p = PurePosixPath(value)
    if p.is_absolute() or any(x in ('', '.', '..') for x in value.split('/')):
        raise ValueError('unsafe relative path: %r' % value)
    return value


def generation(value):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,99}', value):
        raise ValueError('invalid generation')
    return value


def checked(root, relative, make=False):
    """No component of a write/read path may redirect through a symlink."""
    root = Path(root).absolute()
    safe_path(relative)
    current = Path(root.anchor)
    for part in root.parts[1:] + tuple(relative.split('/')):
        current = current / part
        if current.is_symlink():
            raise ValueError('symlink in recovery-area path: %s' % current)
    if make:
        (root / relative).mkdir(parents=True, exist_ok=True)
    return root / relative


def digest_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def inventory(root):
    root = Path(root).absolute()
    checked(root, 'objects/sha256')
    seen = set()
    used = 0
    if root.exists():
        for directory, dirs, files in os.walk(root, followlinks=False):
            for name in ['.'] + dirs + files:
                p = Path(directory) if name == '.' else Path(directory) / name
                s = p.lstat()
                key = (s.st_dev, s.st_ino)
                if key not in seen:
                    used += max(s.st_size, s.st_blocks * 512)
                    seen.add(key)
    objects = root / 'objects/sha256'
    digests = []
    if objects.exists():
        for p in objects.iterdir():
            if not re.fullmatch(r'[0-9a-f]{64}', p.name) or not stat.S_ISREG(p.lstat().st_mode):
                raise ValueError('invalid object-store entry: %s' % p)
            digests.append(p.name)
    probe = root
    while not probe.exists():
        probe = probe.parent
    result = subprocess.run(['/bin/df', '-kP', str(probe)], capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        raise ValueError('df failed: rc=%s %s' % (result.returncode, result.stderr))
    lines = result.stdout.strip().splitlines()
    if len(lines) != 2:
        raise ValueError('malformed df output: %r' % result.stdout)
    fields = lines[1].split()
    if len(fields) < 6 or not fields[3].isdigit():
        raise ValueError('malformed df free bytes: %r' % lines[1])
    free = int(fields[3]) * 1024
    return {'digests': sorted(digests), 'recovery_bytes': used, 'free_bytes': free}


def write_json(path, value):
    data = (json.dumps(value, sort_keys=True) + '\n').encode()
    with open(path, 'wb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def verify(root, gen, manifest_sha256):
    gen = generation(gen)
    incoming = checked(root, 'incoming/' + gen)
    checked(root, 'incoming/' + gen + '/data')
    manifest = checked(root, 'incoming/' + gen + '/manifest.jsonl.gz')
    if digest_file(manifest) != manifest_sha256:
        raise ValueError('manifest SHA-256 mismatch')
    with gzip.open(manifest, 'rt', encoding='utf-8') as f:
        rows = [json.loads(line) for line in f]
    control = json.loads(checked(root, 'incoming/' + gen + '/control.json').read_text())
    if control['manifest_sha256'] != manifest_sha256:
        raise ValueError('control/manifest mismatch')
    changed = set(control['changed_paths'])
    paths = set()
    by_path = {}
    sizes = {}
    for row in rows:
        path = safe_path(row['path'])
        if path in paths:
            raise ValueError('duplicate manifest path')
        paths.add(path)
        by_path[path] = row
        if row['kind'] == 'file':
            d = row['sha256']
            if not re.fullmatch(r'[0-9a-f]{64}', d) or type(row['size']) is not int or row['size'] < 0:
                raise ValueError('invalid file record')
            if d in sizes and sizes[d] != row['size']:
                raise ValueError('inconsistent digest size')
            sizes[d] = row['size']
        elif row['kind'] == 'symlink':
            if not isinstance(row['target'], str) or '\x00' in row['target']:
                raise ValueError('invalid link target')
        else:
            raise ValueError('invalid manifest kind')
    for path in paths:
        if any('/'.join(path.split('/')[:i]) in paths for i in range(1, len(path.split('/')))):
            raise ValueError('manifest leaf is a parent of another path')
    if not changed.issubset(paths):
        raise ValueError('unknown changed path')
    verified = {}
    missing = []
    # Validate every object before publishing any: a corrupt partial cannot enter objects/.
    for row in rows:
        if row['path'] in changed or row['kind'] != 'file':
            continue
        d = row['sha256']
        if d in verified:
            continue
        obj = checked(root, 'objects/sha256/' + d)
        if obj.exists():
            candidate = obj
        else:
            representative = control['representatives'].get(d)
            if representative is None:
                missing.append(row['path'])
                continue
            representative = safe_path(representative)
            rep = by_path.get(representative)
            if rep is None or rep['kind'] != 'file' or rep['sha256'] != d:
                raise ValueError('invalid digest representative')
            if representative in changed:
                missing.append(row['path'])
                continue
            candidate = checked(root, 'incoming/' + gen + '/data/' + representative)
            if not candidate.exists():
                missing.append(row['path'])
                continue
        if not stat.S_ISREG(candidate.lstat().st_mode):
            raise ValueError('object is not a regular file')
        if candidate.stat().st_size != row['size'] or digest_file(candidate) != d:
            raise ValueError('object SHA-256 mismatch: %s (%s)' % (row['path'], d))
        verified[d] = candidate
    checked(root, 'objects/sha256', make=True)
    for d, candidate in verified.items():
        obj = checked(root, 'objects/sha256/' + d)
        if candidate != obj:
            candidate.chmod(0o444)
            candidate.rename(obj)
        else:
            obj.chmod(0o444)
    directory = checked(root, 'generations/' + gen, make=True)
    stored_manifest = checked(root, 'generations/' + gen + '/manifest.jsonl')
    raw = ''.join(json.dumps(row, sort_keys=True) + '\n' for row in rows).encode()
    if stored_manifest.exists() and stored_manifest.read_bytes() != raw:
        raise ValueError('generation manifest is immutable')
    if not stored_manifest.exists():
        with open(stored_manifest, 'xb') as f:
            f.write(raw)
    tree = checked(root, 'generations/' + gen + '/tree', make=True)
    count = 0
    for row in rows:
        path = row['path']
        if path in changed or (row['kind'] == 'file' and row['sha256'] not in verified):
            continue
        # Parents must be directories; final symlink leaves are checked separately.
        parent = str(PurePosixPath(path).parent)
        if parent != '.':
            checked(root, 'generations/' + gen + '/tree/' + parent, make=True)
        target = tree / path
        if row['kind'] == 'symlink':
            if os.path.lexists(target):
                if not target.is_symlink() or os.readlink(target) != row['target']:
                    raise ValueError('existing tree link differs: ' + path)
            else:
                target.symlink_to(row['target'])
        else:
            obj = checked(root, 'objects/sha256/' + row['sha256'])
            checked(root, 'generations/' + gen + '/tree/' + path)
            if target.exists():
                if not os.path.samefile(target, obj):
                    raise ValueError('existing tree file differs: ' + path)
            else:
                os.link(obj, target)
        count += 1
    actual = set()
    for folder, dirs, files in os.walk(tree, followlinks=False):
        for name in files + [d for d in dirs if (Path(folder) / d).is_symlink()]:
            actual.add(str((Path(folder) / name).relative_to(tree)))
    expected = {r['path'] for r in rows if r['path'] not in changed and
                (r['kind'] == 'symlink' or r['sha256'] in verified)}
    # A late M3 mutation can arrive after a frozen tree has been published.
    # Preserve those verified links, label the generation INCOMPLETE, and
    # never delete or replace them. Validate them before counting the census.
    for path in actual & changed:
        row = by_path[path]
        target = tree / path
        if row['kind'] == 'symlink':
            parent = str(PurePosixPath(path).parent)
            if parent != '.':
                checked(root, 'generations/' + gen + '/tree/' + parent)
            if not target.is_symlink() or os.readlink(target) != row['target']:
                raise ValueError('changed tree link differs')
        else:
            checked(root, 'generations/' + gen + '/tree/' + path)
            obj = checked(root, 'objects/sha256/' + row['sha256'])
            if not os.path.samefile(target, obj) or digest_file(target) != row['sha256']:
                raise ValueError('changed tree file differs')
        expected.add(path)
    if actual != expected:
        raise ValueError('generation tree census differs')
    measured = inventory(root)
    hash_changes = control.get('changed_during_hash', [])
    receipt = {'gen': gen, 'status': 'COMPLETE' if len(actual) == len(rows) and not changed and not missing and not hash_changes else 'INCOMPLETE',
               'manifest_sha256': manifest_sha256, 'manifest_paths': len(rows), 'paths': len(actual),
               'objects': len(verified), 'bytes': sum(r['size'] for r in rows if r['path'] in expected and r['kind'] == 'file'),
               'changed_paths': sorted(changed | set(hash_changes)), 'missing_paths': sorted(set(missing)), **measured}
    write_json(checked(root, 'generations/' + gen + '/receipt.json'), receipt)
    # Record measured values before evaluating the final gate.
    if measured['recovery_bytes'] > CAP or measured['free_bytes'] < FLOOR:
        raise ValueError('post-verify budget exceeded: %s' % json.dumps(measured))
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['inventory', 'verify'])
    parser.add_argument('gen', nargs='?')
    parser.add_argument('manifest_sha256', nargs='?')
    parser.add_argument('--root', default=str(Path.home() / 'memit_copy'))
    args = parser.parse_args()
    try:
        result = inventory(Path(args.root)) if args.mode == 'inventory' else verify(Path(args.root), args.gen, args.manifest_sha256)
        print(json.dumps(result, sort_keys=True))
        return 0
    except Exception as exc:
        result = {'status': 'HALTED', 'phase': args.mode, 'gen': args.gen, 'error': str(exc), 'traceback': traceback.format_exc()}
        # Existing incoming directory is the only receiver error sink.
        if args.gen is not None:
            folder = checked(Path(args.root), 'incoming/' + generation(args.gen))
            if folder.is_dir():
                write_json(checked(Path(args.root), 'incoming/' + args.gen + '/halt.json'), result)
        print(json.dumps(result, sort_keys=True))
        return 3


if __name__ == '__main__':
    sys.exit(main())
