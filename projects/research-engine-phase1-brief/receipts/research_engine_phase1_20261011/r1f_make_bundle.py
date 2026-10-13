"""M3-only bundle construction. Every mode writes stdout only; no disk bundle."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import shlex
import sys

HERE = Path(__file__).resolve().parent
RUNTIME = '/Library/Developer/CommandLineTools/usr/bin/python3'


def build(args):
    members = {name: (HERE / filename).read_bytes() for name, filename in [
        ('identity', 'r1f_identity_probe.py'), ('collector', 'r1f_collector.py'),
        ('binder', 'r1f_bind_manifest.py'), ('manifest', 'intel_provisioning_manifest_v6.json')]}
    members['probe'] = Path(args.probe).read_bytes() if args.probe else b'null\n'
    members['capture'] = Path(args.capture).read_bytes() if args.capture else b'null\n'
    request = {'stub_text': (HERE / 'r1f_stub.py').read_text(),
        'bootstrap_start_utc': args.bootstrap_start_utc, 'collector_argv': []}
    request['invoked_argv_prefix'] = [RUNTIME, '-I', '-B', '-c', request['stub_text']]
    if args.mode == 'bind' and (not args.probe or not args.bootstrap_start_utc):
        raise ValueError('Bind requires probe and M3 bootstrap start')
    if args.mode == 'inventory':
        if not args.capture or args.expected_anchor is None or not args.expected_capture_sha256 or args.bootstrap_bytes is None:
            raise ValueError('Inventory requires capture, trusted hash, exact anchor and bootstrap bytes')
        if hashlib.sha256(members['capture']).hexdigest() != args.expected_capture_sha256:
            raise ValueError('Complete capture SHA-256 mismatch on M3')
        capture_path = Path(args.capture)
        stderr = capture_path.with_suffix('.stderr').read_bytes()
        status = capture_path.with_suffix('.exit').read_bytes()
        if status != b'0\n' or args.bootstrap_bytes != len(members['capture']) + len(stderr) + len(status):
            raise ValueError('Bootstrap byte count/status differs from complete M3 receipts')
        request['collector_argv'] = ['inventory', '--expected-anchor', args.expected_anchor,
            '--expected-capture-sha256', args.expected_capture_sha256,
            '--bootstrap-bytes', str(args.bootstrap_bytes)]
        if args.evidence_update:
            request['evidence_update'] = json.loads(Path(args.evidence_update).read_bytes())
    members['request'] = (json.dumps(request, sort_keys=True, allow_nan=False) + '\n').encode()
    return members


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['probe', 'bind', 'inventory'])
    for name in ['probe', 'capture', 'bootstrap-start-utc', 'expected-anchor',
            'expected-capture-sha256', 'evidence-update']:
        parser.add_argument('--' + name)
    parser.add_argument('--bootstrap-bytes', type=int)
    parser.add_argument('--remote-command', action='store_true')
    parser.add_argument('--bootstrap-bytes-only', action='store_true')
    args = parser.parse_args()
    if args.bootstrap_bytes_only:
        if not args.capture or not args.expected_capture_sha256:
            raise ValueError('Bootstrap count requires the trusted capture hash')
        path = Path(args.capture)
        capture = path.read_bytes()
        if hashlib.sha256(capture).hexdigest() != args.expected_capture_sha256:
            raise ValueError('Complete capture SHA-256 mismatch on M3')
        stderr = path.with_suffix('.stderr').read_bytes()
        status = path.with_suffix('.exit').read_bytes()
        if status != b'0\n':
            raise ValueError('Binding exit status must be exactly zero')
        print(len(capture) + len(stderr) + len(status))
        return
    members = build(args)
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in members.items()}
    if args.remote_command:
        print(shlex.join(json.loads(members['request'])['invoked_argv_prefix'] +
            [args.mode, json.dumps(hashes, sort_keys=True)]))
    else:
        print(json.dumps({name: base64.b64encode(data).decode('ascii') for name, data in members.items()}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('REFUSED: ' + str(exc), file=sys.stderr, flush=True)
        sys.exit(1)
