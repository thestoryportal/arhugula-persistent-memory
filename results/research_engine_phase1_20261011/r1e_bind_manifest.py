"""Intel-local, reviewed-input, exclusive binding. No window or acquisition."""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys


def _load_verified(path, source):
    # Execute the bytes that were hashed, rather than re-reading the collector.
    spec = importlib.util.spec_from_file_location('r1e_binding_collector', path)
    module = importlib.util.module_from_spec(spec)
    exec(compile(source, str(path), 'exec'), module.__dict__)
    return module


def bind_manifest(v5_path, collector_path, identity_path, probe_path, bound_path,
        expected_v5, expected_collector, expected_identity):
    v5_path, collector_path, identity_path, probe_path, bound_path = map(Path,
        [v5_path, collector_path, identity_path, probe_path, bound_path])
    verified = []
    # No supplied implementation is imported until all three hashes pass.
    for path, expected in [(v5_path, expected_v5), (collector_path, expected_collector),
            (identity_path, expected_identity)]:
        source = path.read_bytes()
        if len(expected) != 64 or hashlib.sha256(source).hexdigest() != expected:
            raise ValueError('Reviewed input SHA-256 mismatch: ' + str(path))
        verified.append(source)
    if collector_path.resolve().with_name('r1e_identity_probe.py') != identity_path.resolve():
        raise ValueError('Collector must import the verified sibling identity probe')
    manifest = json.loads(verified[0])
    if 'binding_provenance' in manifest or manifest['window_seal']['core_sha256'] != 'NEEDS-FETCH':
        raise ValueError('Only an unbound v5 may be bound')
    if not all(value == 'NEEDS-FETCH' for value in manifest['collector']['interpreter']['identity'].values()):
        raise ValueError('Source interpreter identity must remain NEEDS-FETCH')
    retained = Path(manifest['collector']['retained_dir'])
    registration = Path(manifest['collector']['registration_path'])
    for path in [retained, registration.parent, registration, bound_path]:
        if path.exists() or path.is_symlink():
            raise ValueError('Binding destination/window state already exists: ' + str(path))
    # Repeat the probe hash immediately before collector import (its shared function is imported).
    if identity_path.read_bytes() != verified[2]:
        raise ValueError('Identity implementation changed before import')
    api = _load_verified(collector_path, verified[1])
    raw_probe = probe_path.read_bytes()
    observed = json.loads(raw_probe)
    actual = json.loads(api.encoded(api.interpreter_identity()))
    if actual != observed or set(actual) != set(manifest['collector']['interpreter']['identity']):
        raise ValueError('Probe does not equal running interpreter in every field')
    if 'NEEDS-FETCH' in json.dumps(actual) or not api.pin(actual['executable_sha256']) or not api.pin(actual['stdlib']['sha256']) or actual['machine'] != manifest['host']['arch']:
        raise ValueError('Incomplete identity or wrong binding host')
    manifest['collector']['interpreter']['identity'] = actual
    api.qualify_interpreter(manifest)
    manifest['window_seal']['core_sha256'] = api.core_digest(manifest)
    manifest['binding_provenance'] = {
        'v5_sha256': expected_v5, 'collector_sha256': expected_collector,
        'identity_probe_sha256': expected_identity,
        'probe_file_sha256': hashlib.sha256(raw_probe).hexdigest(),
        'probe_json': raw_probe.decode('utf-8'),
        'binder_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'utc_time': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'bound_core_sha256': manifest['window_seal']['core_sha256']}
    data = api.encoded(manifest)
    # O_EXCL forbids overwrites, including symlinks and racing publishers.
    fd = os.open(str(bound_path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    directory_fd = os.open(str(bound_path.parent), os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
    digest = hashlib.sha256(data).hexdigest()
    print(digest)
    return digest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['v5', 'collector', 'identity', 'probe', 'bound',
            'expected_v5', 'expected_collector', 'expected_identity']:
        parser.add_argument(name)
    args = parser.parse_args(argv)
    try:
        bind_manifest(args.v5, args.collector, args.identity, args.probe, args.bound,
            args.expected_v5, args.expected_collector, args.expected_identity)
        return 0
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as exc:
        print('REFUSED: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
