"""Read-only in-process binding of verified stdin members; stdout publication."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import sys


def bind_manifest():
    api = VERIFIED_COLLECTOR
    members = VERIFIED_MEMBERS
    manifest = json.loads(members['manifest'])
    if 'binding_provenance' in manifest or manifest['window_seal']['core_sha256'] != 'NEEDS-FETCH':
        raise ValueError('Only an unbound v8 may be bound')
    if not all(value == 'NEEDS-FETCH' for value in manifest['collector']['interpreter']['identity'].values()):
        raise ValueError('Source interpreter identity must remain NEEDS-FETCH')
    for path in [Path(manifest['collector']['retained_dir']), Path(manifest['collector']['registration_path']).parent]:
        if path.exists() or path.is_symlink():
            raise ValueError('Binding window state already exists: ' + str(path))
    raw_probe = members['probe']
    observed = json.loads(raw_probe.split(b'\n', 1)[1] if raw_probe.startswith(b'R1I-READY ') else raw_probe)
    raw_actual = api['encoded'](VERIFIED_PROBE['interpreter_identity']())
    actual = json.loads(raw_actual)
    if actual != observed or set(actual) != set(manifest['collector']['interpreter']['identity']):
        raise ValueError('Probe does not equal running interpreter in every field')
    if ('NEEDS-FETCH' in json.dumps(actual) or not api['pin'](actual['executable_sha256']) or
            not api['pin'](actual['stdlib']['sha256']) or actual['machine'] != manifest['host']['arch']):
        raise ValueError('Incomplete identity or wrong binding host')
    request = json.loads(members['request'])
    bootstrap = request['bootstrap_start_utc']
    api['utc_seconds'](bootstrap)
    prefix = request['invoked_argv_prefix']
    expected_prefix = [manifest['collector']['interpreter']['executable'], '-I', '-B', '-c', STUB_TEXT]
    if prefix != expected_prefix or os.path.realpath(prefix[0]) != actual['realpath']:
        raise ValueError('Invoked runtime prefix disagrees with manifest/runtime realpath')
    manifest['collector']['interpreter']['identity'] = actual
    api['qualify_interpreter'](manifest)
    manifest['window_seal']['core_sha256'] = api['core_digest'](manifest)
    manifest['binding_provenance'] = {
        'v8_sha256': VERIFIED_HASHES['manifest'], 'collector_sha256': VERIFIED_HASHES['collector'],
        'identity_probe_sha256': VERIFIED_HASHES['identity'],
        'probe_file_sha256': hashlib.sha256(raw_probe).hexdigest(), 'probe_json': raw_probe.decode('utf-8'),
        'binder_sha256': VERIFIED_HASHES['binder'],
        'utc_time': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'bound_core_sha256': manifest['window_seal']['core_sha256']}
    data = api['encoded'](manifest)
    # Receipt preserves the actual stub argv, including its -c text and trusted member pins.
    receipt = {'argv': prefix + sys.argv[1:],
        'hostname': os.uname().nodename, 'uname': list(os.uname()),
        'bootstrap_start_utc': bootstrap, 'input_sha256': dict(VERIFIED_HASHES),
        'raw_probe_output': raw_actual.decode('utf-8'),
        'bound_manifest_sha256': hashlib.sha256(data).hexdigest()}
    return {'bound_manifest_json': data.decode('utf-8'), 'binding_receipt': receipt}


def entrypoint():
    try:
        print(json.dumps(bind_manifest(), sort_keys=True, allow_nan=False), flush=True)
        return 0
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as exc:
        print('REFUSED: ' + str(exc), file=sys.stderr, flush=True)
        return 1
