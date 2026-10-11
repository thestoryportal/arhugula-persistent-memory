"""M3-only bundle construction. Every mode writes stdout only; no disk bundle."""
import argparse
import base64
import hashlib
import json
import datetime
import math
import os
import re
import subprocess
import time
from pathlib import Path
import shlex
import sys

HERE = Path(__file__).resolve().parent
RUNTIME = '/Library/Developer/CommandLineTools/usr/bin/python3'


def build(args):
    members = {name: (HERE / filename).read_bytes() for name, filename in [
        ('identity', 'r1h_identity_probe.py'), ('collector', 'r1h_collector.py'),
        ('binder', 'r1h_bind_manifest.py'), ('manifest', 'intel_provisioning_manifest_v7.json')]}
    members['probe'] = Path(args.probe).read_bytes() if args.probe else b'null\n'
    members['capture'] = Path(args.capture).read_bytes() if args.capture else b'null\n'
    request = {'stub_text': (HERE / 'r1h_stub.py').read_text(),
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
        if args.remaining_seconds is None or not math.isfinite(args.remaining_seconds) or args.remaining_seconds <= 0:
            raise ValueError('Inventory requires a positive M3 remaining budget')
        request['collector_argv'] = ['inventory', '--remaining-seconds', str(args.remaining_seconds), '--expected-anchor', args.expected_anchor,
            '--expected-capture-sha256', args.expected_capture_sha256,
            '--bootstrap-bytes', str(args.bootstrap_bytes)]
        if args.evidence_update:
            request['evidence_update'] = json.loads(Path(args.evidence_update).read_bytes())
    members['request'] = (json.dumps(request, sort_keys=True, allow_nan=False) + '\n').encode()
    return members



def syncdir(path):
    fd = os.open(str(path), os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def exclusive_record(path, data):
    # Even a short/failed write leaves the exclusive name consumed.
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        syncdir(path.parent)


def committed_bytes(path):
    path = Path(path)
    relative = path.resolve().relative_to(HERE.resolve())
    spec = 'HEAD:./' + str(relative)
    check = subprocess.run(['git', '-C', str(HERE), 'cat-file', '-e', spec], capture_output=True)
    if check.returncode != 0:
        raise ValueError('Capture/anchor receipt is not committed: ' + str(path))
    result = subprocess.run(['git', '-C', str(HERE), 'cat-file', 'blob', spec], capture_output=True)
    if result.returncode != 0 or not result.stdout and path.stat().st_size != 0:
        raise ValueError('Committed receipt cannot be read: ' + str(path))
    if result.stdout != path.read_bytes():
        raise ValueError('Committed bytes differ from preserved receipt: ' + str(path))
    return result.stdout


def last_anchor(stdout, status):
    if status != b'0\n':
        raise ValueError('Consumed anchor has failed/unknown capture; operator-reviewed recovery required')
    lines = [x for x in stdout.decode('utf-8').splitlines() if x.startswith('R1H-ANCHOR ')]
    if not lines or not re.fullmatch(r'R1H-ANCHOR [0-9a-f]{64} (0|[1-9][0-9]*) [0-9a-f]{64}', lines[-1]):
        raise ValueError('Consumed anchor has no successor; operator-reviewed recovery required')
    _, core, seq, head = lines[-1].split()
    return core, seq + ':' + head


def require_anchor(anchor, core):
    if anchor == 'none':
        return
    # Successors come only from complete, zero-exit, git-preserved captures.
    for record in HERE.glob('r1h_attempt_*.json'):
        attempt = json.loads(record.read_bytes())
        prefix = Path(attempt['capture_prefix'])
        out, err, status = [prefix.with_suffix(x) for x in ('.json', '.stderr', '.exit')]
        if not all(x.is_file() for x in (out, err, status)):
            continue
        if status.read_bytes() != b'0\n':
            continue
        try:
            candidate = last_anchor(out.read_bytes(), status.read_bytes())
        except ValueError:
            continue
        if candidate == (core, anchor):
            for path in (record, out, err, status):
                committed_bytes(path)
            return
    raise ValueError('No committed zero-exit successor anchor; operator-reviewed recovery required')


def dispatch(args, now=time.time):
    # Only the M3 wall clock computes the global deadline; Intel gets a duration.
    capture = Path(args.capture).read_bytes() if args.capture else None
    deadline = None
    attempt_path = None
    if args.mode == 'inventory':
        if not re.fullmatch(r'[0-9a-f]{64}', args.expected_capture_sha256 or ''):
            raise ValueError('Trusted capture SHA-256 required')
        if hashlib.sha256(capture).hexdigest() != args.expected_capture_sha256:
            raise ValueError('Complete capture SHA-256 mismatch on M3')
        publication = json.loads(capture)
        core = json.loads(publication['bound_manifest_json'])['window_seal']['core_sha256']
        if args.expected_anchor == 'none':
            seq, head = '0', core
        elif re.fullmatch(r'(0|[1-9][0-9]*):[0-9a-f]{64}', args.expected_anchor or ''):
            seq, head = args.expected_anchor.split(':')
        else:
            raise ValueError('Exact anchor required')
        attempt_path = HERE / ('r1h_attempt_' + seq + '_' + head[:12] + '.json')
        if attempt_path.exists() or attempt_path.is_symlink():
            raise ValueError('Anchor already consumed; operator-reviewed recovery required; never retry')
        committed = committed_bytes(args.capture)
        if hashlib.sha256(committed).hexdigest() != args.expected_capture_sha256:
            raise ValueError('Committed capture hash differs from supplied authority')
        require_anchor(args.expected_anchor, core)
        bootstrap = publication['binding_receipt']['bootstrap_start_utc']
        deadline = datetime.datetime.strptime(bootstrap, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc).timestamp() + 870
        args.remaining_seconds = deadline - now() - 5
        if not math.isfinite(args.remaining_seconds) or args.remaining_seconds <= 0:
            raise ValueError('M3 bootstrap deadline exhausted before ssh')
        prefix = HERE / ('r1h_inventory_' + seq + '_' + head[:12])
        args.capture_prefix = str(prefix)
    else:
        prefix = Path(args.capture_prefix)
        if prefix.resolve().parent != HERE.resolve() or '..' in prefix.name or prefix.name.startswith('.'):
            raise ValueError('Capture prefix must be a new safe M3 RE path')
        if args.mode == 'bind':
            deadline = datetime.datetime.strptime(args.bootstrap_start_utc, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc).timestamp() + 870
    members = build(args)
    hashes = {name: hashlib.sha256(value).hexdigest() for name, value in members.items()}
    remote = shlex.join(json.loads(members['request'])['invoked_argv_prefix'] + [args.mode, json.dumps(hashes, sort_keys=True)])
    bundle = json.dumps({name: base64.b64encode(value).decode('ascii') for name, value in members.items()}, sort_keys=True).encode()
    if attempt_path is not None:
        record = {'anchor': args.expected_anchor, 'core_sha256': core,
            'capture_sha256': args.expected_capture_sha256, 'capture_prefix': str(prefix),
            'remaining_seconds': args.remaining_seconds, 'm3_deadline': deadline}
        exclusive_record(attempt_path, (json.dumps(record, sort_keys=True) + '\n').encode())
    # All three names are reserved before ssh; failed reservation consumes inventory.
    paths = [prefix.with_suffix(x) for x in ('.json', '.stderr', '.exit')]
    opened = []
    try:
        for path in paths:
            fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            opened.append(os.fdopen(fd, 'wb', buffering=0))
        syncdir(prefix.parent)
        out, err, status = opened
        timeout = deadline - now() if deadline is not None else 870
        if timeout <= 0:
            rc = 124
            err.write(b'REFUSED: M3 deadline before ssh; operator-reviewed recovery required\n')
        else:
            try:
                result = subprocess.run(args.ssh_argv + [remote], input=bundle, stdout=out, stderr=err, timeout=timeout)
                rc = result.returncode
            except subprocess.TimeoutExpired:
                rc = 124
                err.write(b'REFUSED: M3 hard timeout; operator-reviewed recovery required\n')
            except OSError as exc:
                rc = 125
                err.write(('REFUSED: ssh failed: ' + str(exc) + '\n').encode())
        if args.mode == 'inventory' and rc == 0:
            os.fsync(out.fileno())
            try:
                successor_core, successor = last_anchor(paths[0].read_bytes(), b'0\n')
                if successor_core != core:
                    raise ValueError('Successor core differs')
            except ValueError as exc:
                rc = 125
                err.write(('REFUSED: ' + str(exc) + '\n').encode())
        # Measure completion after the payload companions are synced on M3.
        os.fsync(out.fileno())
        os.fsync(err.fileno())
        syncdir(prefix.parent)
        if deadline is not None and now() > deadline:
            rc = 124
            err.write(b'REFUSED: M3 end past bootstrap deadline\n')
        status.write(('%d\n' % rc).encode())
        for stream in opened:
            os.fsync(stream.fileno())
        syncdir(prefix.parent)
        if rc == 0 and deadline is not None and now() > deadline:
            rc = 124
            err.write(b'REFUSED: M3 deadline during final receipt persistence\n')
            status.seek(0)
            status.truncate()
            status.write(b'124\n')
            for stream in opened:
                os.fsync(stream.fileno())
            syncdir(prefix.parent)
    finally:
        for stream in opened:
            stream.close()
    if rc != 0:
        print('REFUSED: capture failed; operator-reviewed recovery required: ' + str(prefix), file=sys.stderr)
        return rc
    if args.mode == 'inventory':
        print('R1H-SUCCESSOR ' + successor + ' ' + str(paths[0]), flush=True)
        print('R1H-ATTEMPT ' + str(attempt_path), flush=True)
    else:
        raw = paths[0].read_bytes()
        value = json.loads(raw)
        if not isinstance(value, dict) or not value:
            raise ValueError('Empty/malformed capture')
        print('R1H-CAPTURE ' + str(paths[0]) + ' ' + hashlib.sha256(raw).hexdigest(), flush=True)
    return 0

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['probe', 'bind', 'inventory'])
    for name in ['probe', 'capture', 'bootstrap-start-utc', 'expected-anchor',
            'expected-capture-sha256', 'evidence-update']:
        parser.add_argument('--' + name)
    parser.add_argument('--bootstrap-bytes', type=int)
    parser.add_argument('--remaining-seconds', type=float)
    parser.add_argument('--dispatch-m3', action='store_true')
    parser.add_argument('--capture-prefix')
    parser.add_argument('--ssh-argv', nargs=argparse.REMAINDER)
    parser.add_argument('--remote-command', action='store_true')
    parser.add_argument('--bootstrap-bytes-only', action='store_true')
    args = parser.parse_args()
    if args.dispatch_m3:
        if not args.ssh_argv or args.ssh_argv[0] != 'ssh':
            raise ValueError('Explicit ssh argv required')
        return dispatch(args)
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
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('REFUSED: ' + str(exc), file=sys.stderr, flush=True)
        sys.exit(1)
