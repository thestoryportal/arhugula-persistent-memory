"""Read-only sizing, stdlib only. Run with -I -B; stdout <= 131072 bytes.

Pinned-stub probe mode may use this file as its verified identity member.
No identity is established by this sizing result; no collector is constructed.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import time
import types

MAX_SUMMARY_BYTES = 131072
MAX_OLD_FILES = 128
COLLECTOR_SHA256 = '0f71117106f639c55a3d7bc588d252a947c188218c3ee7c8f4f8698c60a5aa2d'
MANIFEST_SHA256 = '748fc72aa49bcdb963d99b89bbc29859237d1bbd32b84b8e05fd38d07bd9df3f'
OLD_ROOTS = ['/private/tmp/r1h-intel-provisioning-v7',
             '/private/tmp/r1h-intel-window-registration-v7']
FUTURE_COLLECTOR_ROW_BYTES = 65536
FUTURE_COLLECTOR_ENTRIES = 64
METADATA = ['mode', 'uid', 'gid', 'logical_bytes', 'allocated_bytes', 'device', 'inode']
DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW


def load_collector(raw):
    if hashlib.sha256(raw).hexdigest() != COLLECTOR_SHA256:
        raise ValueError('collector pin differs')
    module = types.ModuleType('r1m_pinned_collector')
    module.VERIFIED_PROBE = {'interpreter_identity': lambda: None, 'stdlib_identity': lambda: None}
    exec(compile(raw, '<r1m:pinned-collector>', 'exec'), module.__dict__)
    return module


def output_bytes(value):
    raw = (json.dumps(value, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')
    if len(raw) > MAX_SUMMARY_BYTES:
        raise ValueError('summary bound exceeded')
    return raw


def parent_fd(path):
    """Open every ancestor as a directory, refusing all symlink ancestors."""
    if not path.is_absolute() or '..' in path.parts or path == Path('/'):
        raise ValueError('absolute non-root inventory path required')
    fd = os.open('/', DIR_FLAGS)
    try:
        for component in path.parts[1:-1]:
            next_fd = os.open(component, DIR_FLAGS, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        return fd
    except BaseException:
        os.close(fd)
        raise


def observe_root(root, collector_root, registration_root, chunk_bytes, api):
    """Rows mirror C:882-939; encoding is exclusively C.encoded()."""
    result = {'root': root, 'rows': 0, 'row_bytes': 0, 'hash_chunks': 0,
              'walk_remaining_calls': 0, 'by_kind': {}, 'newest_mtime_ns': 0,
              'newest_ctime_ns': 0, 'witness_sum': 0}
    path = Path(root)

    def emit(row, s=None, walked=True, refused_target=None):
        result['rows'] += 1
        result['walk_remaining_calls'] += int(walked)
        result['row_bytes'] += len(api.encoded(row))
        kind = row['kind']
        bucket = result['by_kind'].setdefault(kind, {'count': 0, 'encoded_path_bytes': 0,
            'encoded_target_bytes': 0, 'regular_file_bytes': 0, 'metadata': {}})
        bucket['count'] += 1
        bucket['encoded_path_bytes'] += len(api.encoded(row['path']))
        target_text = row.get('target', refused_target)
        bucket['encoded_target_bytes'] += len(api.encoded(target_text)) if target_text is not None else 0
        for key in METADATA:
            if key in row:
                limits = bucket['metadata'].setdefault(key, [row[key], row[key]])
                limits[0], limits[1] = min(limits[0], row[key]), max(limits[1], row[key])
        if s is not None and stat.S_ISREG(s.st_mode):
            bucket['regular_file_bytes'] += row['logical_bytes']
        witness = dict(row)
        if refused_target is not None:
            witness['refused_target'] = refused_target
        if s is not None:
            result['newest_mtime_ns'] = max(result['newest_mtime_ns'], s.st_mtime_ns)
            result['newest_ctime_ns'] = max(result['newest_ctime_ns'], s.st_ctime_ns)
            witness.update(mtime_ns=s.st_mtime_ns, ctime_ns=s.st_ctime_ns)
        result['witness_sum'] = (result['witness_sum'] + int(hashlib.sha256(api.encoded(witness)).hexdigest(), 16)) % (1 << 256)

    def origin(p):
        return 'collector' if any(p == r or r in p.parents for r in [collector_root, registration_root]) else 'baseline'

    def descend(p, parent, name, root_entry=False):
        row = {'path': str(p), 'origin': origin(p)}
        s = None
        fd = None
        try:
            s = os.stat(name, dir_fd=parent, follow_symlinks=False)
            row.update(mode=stat.S_IMODE(s.st_mode), uid=s.st_uid, gid=s.st_gid,
                logical_bytes=s.st_size, allocated_bytes=s.st_blocks * 512, device=s.st_dev, inode=s.st_ino)
            if stat.S_ISLNK(s.st_mode):
                if root_entry:
                    emit({'path': str(p), 'kind': 'symlink-root-refused', 'origin': 'baseline'}, s, False,
                         os.readlink(name, dir_fd=parent))
                    return
                row.update(kind='symlink', target=os.readlink(name, dir_fd=parent))
            elif stat.S_ISDIR(s.st_mode):
                row['kind'] = 'directory'
                fd = os.open(name, DIR_FLAGS, dir_fd=parent)
                opened = os.fstat(fd)
                if (opened.st_dev, opened.st_ino) != (s.st_dev, s.st_ino):
                    raise ValueError('directory replaced during sizing')
                with os.scandir(fd):
                    pass
            elif stat.S_ISREG(s.st_mode):
                row['kind'] = 'file'
                if row['origin'] == 'baseline':
                    readable = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
                    try:
                        opened = os.fstat(readable)
                        if (opened.st_dev, opened.st_ino) != (s.st_dev, s.st_ino):
                            raise ValueError('file replaced during sizing')
                    finally:
                        os.close(readable)
                    row['sha256'] = '0' * 64
                    result['hash_chunks'] += (s.st_size + chunk_bytes - 1) // chunk_bytes
            elif stat.S_ISSOCK(s.st_mode):
                row['kind'] = 'socket'
            elif stat.S_ISFIFO(s.st_mode):
                row['kind'] = 'fifo'
            else:
                row['kind'] = 'special'
            after = os.stat(name, dir_fd=parent, follow_symlinks=False)
            if any(getattr(s, key) != getattr(after, key) for key in ['st_dev', 'st_ino', 'st_mode', 'st_size', 'st_mtime_ns', 'st_ctime_ns']):
                raise ValueError('entry changed during sizing')
        except OSError as exc:
            if exc.errno is not None:
                exc = OSError(exc.errno, exc.strerror, str(p))
            row.update(kind='unreadable' if isinstance(exc, PermissionError) else
                'vanished' if isinstance(exc, FileNotFoundError) else 'io-error', error=str(exc))
        except BaseException:
            if fd is not None:
                os.close(fd)
            raise
        try:
            emit(row, s)
            if row['kind'] == 'directory':
                try:
                    with os.scandir(fd) as entries:
                        for entry in entries:
                            descend(p / entry.name, fd, entry.name)
                except OSError as exc:
                    if exc.errno is not None:
                        exc = OSError(exc.errno, exc.strerror, str(p))
                    emit({'path': str(p), 'origin': row['origin'], 'kind': 'unreadable' if isinstance(exc, PermissionError) else
                        'vanished' if isinstance(exc, FileNotFoundError) else 'io-error', 'error': str(exc)}, s, False)
        finally:
            if fd is not None:
                os.close(fd)

    try:
        parent = parent_fd(path)
    except FileNotFoundError as exc:
        # Missing ordinary ancestors produce a collector vanished observation.
        emit({'path': root, 'origin': origin(path), 'kind': 'vanished', 'error': str(exc)})
    else:
        try:
            descend(path, parent, path.name, True)
        finally:
            os.close(parent)
    result['witness_sum'] = '%064x' % result['witness_sum']
    return result


def scan_inventory(manifest, api):
    policy = manifest['collector']
    roots = policy['admitted_write_roots']
    if len(roots) != len(set(roots)) or type(policy['io_chunk_bytes']) is not int or policy['io_chunk_bytes'] <= 0:
        raise ValueError('invalid inventory roots/chunk size')
    return [observe_root(root, Path(policy['retained_dir']), Path(policy['registration_path']).parent,
                         policy['io_chunk_bytes'], api) for root in roots]


def measure_old(roots, api):
    files, witnesses = [], []
    for root in roots:
        # Reuse the fd traversal; old roots are separate explicit read-only scopes.
        data = observe_root(root, Path('/__no_collector__'), Path('/__no_registration__'), 65536, api)
        if set(data['by_kind']) - {'file', 'directory', 'vanished'}:
            raise ValueError('old-state is unreadable or contains symlinks/special entries')
        # A second fd walk supplies the complete bounded file list, never rglob.
        def list_files(p, parent, name):
            s = os.stat(name, dir_fd=parent, follow_symlinks=False)
            if stat.S_ISREG(s.st_mode):
                files.append({'path': str(p), 'size': s.st_size, 'mtime_ns': s.st_mtime_ns})
                if len(files) > MAX_OLD_FILES:
                    raise ValueError('old-state file list bound exceeded')
            elif stat.S_ISDIR(s.st_mode):
                fd = os.open(name, DIR_FLAGS, dir_fd=parent)
                try:
                    with os.scandir(fd) as entries:
                        for entry in entries:
                            list_files(p / entry.name, fd, entry.name)
                finally:
                    os.close(fd)
            else:
                raise ValueError('old-state unsupported entry')
        if 'vanished' in data['by_kind']:
            if data['rows'] != 1:
                raise ValueError('old-state incomplete file list')
        else:
            parent = parent_fd(Path(root))
            try:
                list_files(Path(root), parent, Path(root).name)
            finally:
                os.close(parent)
        witnesses.append(data)
    return {'roots': roots, 'files': sorted(files, key=lambda x: x['path']),
            'total_bytes': sum(x['size'] for x in files), 'witnesses': witnesses}


def measure(manifest, api, old_roots=None):
    roots = OLD_ROOTS if old_roots is None else old_roots
    first = scan_inventory(manifest, api)
    old = measure_old(roots, api)
    if first != scan_inventory(manifest, api) or old != measure_old(roots, api):
        raise ValueError('tree changed between sizing passes')
    kinds = {}
    for root in first:
        for kind, bucket in root['by_kind'].items():
            target = kinds.setdefault(kind, {'count': 0, 'encoded_path_bytes': 0, 'encoded_target_bytes': 0,
                                           'regular_file_bytes': 0, 'metadata': {}})
            for key in ['count', 'encoded_path_bytes', 'encoded_target_bytes', 'regular_file_bytes']:
                target[key] += bucket[key]
            for key, pair in bucket['metadata'].items():
                limits = target['metadata'].setdefault(key, list(pair))
                limits[0], limits[1] = min(limits[0], pair[0]), max(limits[1], pair[1])
    result = {'schema': 'R1M-sizing-v1', 'manifest_sha256': hashlib.sha256(api.encoded(manifest)).hexdigest(),
        'sizing_probe_sha256': hashlib.sha256(VERIFIED_MEMBERS['identity'] if 'VERIFIED_MEMBERS' in globals()
                                            else Path(__file__).read_bytes()).hexdigest(),
        'collector_sha256': COLLECTOR_SHA256, 'summary_max_bytes': MAX_SUMMARY_BYTES,
        'measured_at_unix_ns': time.time_ns(), 'stable_two_passes': True, 'roots': first, 'by_kind': kinds,
        'observed_row_bytes': sum(r['row_bytes'] for r in first),
        'future_collector_row_bytes': FUTURE_COLLECTOR_ROW_BYTES,
        'inventory_row_bound_bytes': sum(r['row_bytes'] for r in first) + FUTURE_COLLECTOR_ROW_BYTES,
        'hash_chunks': sum(r['hash_chunks'] for r in first),
        'walk_remaining_calls': sum(r['walk_remaining_calls'] for r in first),
        'rows': sum(r['rows'] for r in first), 'old_state': old}
    output_bytes(result)
    return result


def interpreter_identity():
    """Existing S probe entry: verified bytes in memory, no Intel file writes."""
    members = globals().get('VERIFIED_MEMBERS')
    if members is None:
        here = Path(__file__).resolve().parent
        raw_manifest = (here / 'intel_provisioning_manifest_v10.json').read_bytes()
        raw_collector = (here / 'r1j_collector.py').read_bytes()
    else:
        raw_manifest, raw_collector = members['manifest'], members['collector']
    if hashlib.sha256(raw_manifest).hexdigest() != MANIFEST_SHA256:
        raise ValueError('manifest pin differs')
    api = load_collector(raw_collector)
    result = measure(json.loads(raw_manifest), api)
    # The manifest is pinned by raw bytes, rather than a serialization assumption.
    result['manifest_sha256'] = hashlib.sha256(raw_manifest).hexdigest()
    if members is not None:
        result['dispatch_request_sha256'] = VERIFIED_HASHES['request']
    output_bytes(result)
    return result


if __name__ == '__main__':
    try:
        sys.stdout.buffer.write(output_bytes(interpreter_identity()))
    except (OSError, ValueError, RecursionError) as exc:
        sys.stderr.write(('REFUSED: ' + str(exc))[:1024] + '\n')
        sys.exit(1)
