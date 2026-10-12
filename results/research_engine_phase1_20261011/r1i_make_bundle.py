"""M3-only bundle construction. Build modes emit stdout only; dispatch preserves M3 receipts; no disk bundle."""
import argparse
import base64
import hashlib
import json
import datetime
import math
import os
import re
import subprocess
import selectors
import time
from pathlib import Path
import shlex
import sys

HERE = Path(__file__).resolve().parent
RUNTIME = '/Library/Developer/CommandLineTools/usr/bin/python3'


def build(args):
    members = {name: (HERE / filename).read_bytes() for name, filename in [
        ('identity', 'r1i_identity_probe.py'), ('collector', 'r1i_collector.py'),
        ('binder', 'r1i_bind_manifest.py'), ('manifest', 'intel_provisioning_manifest_v8.json')]}
    members['probe'] = Path(args.probe).read_bytes() if args.probe else b'null\n'
    members['capture'] = Path(args.capture).read_bytes() if args.capture else b'null\n'
    request = {'stub_text': (HERE / 'r1i_stub.py').read_text(),
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
        final = qualified(capture_path.with_suffix(''), committed=True)
        if status != b'0\n' or args.bootstrap_bytes != len(members['capture']) + len(stderr) + len(status) + len(final):
            raise ValueError('Bootstrap byte count/status differs from complete M3 receipts')
        request['collector_argv'] = ['inventory', '--expected-anchor', args.expected_anchor,
            '--expected-capture-sha256', args.expected_capture_sha256,
            '--bootstrap-bytes', str(args.bootstrap_bytes),
            '--m3-receipt-bytes', str(getattr(args, 'm3_receipt_bytes', 0))]
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
    for record in HERE.glob('r1i_attempt_*.json'):
        attempt = json.loads(record.read_bytes())
        prefix = Path(attempt['capture_prefix'])
        out, err, status, final = [prefix.with_suffix(x) for x in ('.json', '.stderr', '.exit', '.final')]
        if not all(x.is_file() for x in (out, err, status, final)):
            continue
        if status.read_bytes() != b'0\n':
            continue
        try:
            candidate = last_anchor(out.read_bytes(), status.read_bytes())
        except ValueError:
            continue
        if candidate == (core, anchor):
            qualified(prefix, attempt.get('m3_deadline'), committed=True)
            for path in (record, out, err, status, final):
                committed_bytes(path)
            return
    raise ValueError('No committed zero-exit successor anchor; operator-reviewed recovery required')


def publication(raw):
    return json.loads(raw.split(b'\n', 1)[1] if raw.startswith(b'R1I-READY ') else raw)


def qualified(prefix, deadline=None, committed=False):
    paths = [prefix.with_suffix(x) for x in ('.json', '.stderr', '.exit', '.final')]
    if committed:
        values = [committed_bytes(path) for path in paths]
    else:
        values = [path.read_bytes() for path in paths]
    raw = values[-1]
    if b'REFUSED: final receipt persistence failed' in values[1]:
        raise ValueError('Failed final persistence; operator-reviewed recovery required')
    try:
        value = json.loads(raw)
        if set(value) != {'exit', 'qualified', 'm3_deadline', 'm3_qualified_at'}:
            raise ValueError('Final receipt fields differ')
        if raw != (json.dumps(value, sort_keys=True, allow_nan=False)+'\n').encode():
            raise ValueError('Final receipt is partial or noncanonical')
        if type(value['exit']) is not int or value['exit'] != 0 or value['qualified'] is not True or values[2] != b'0\n':
            raise ValueError('Final receipt and exit must qualify zero')
        for key in ('m3_deadline', 'm3_qualified_at'):
            if type(value[key]) not in (int,float) or not math.isfinite(value[key]):
                raise ValueError('Invalid final timestamp')
        if value['m3_qualified_at'] > value['m3_deadline'] or deadline is not None and value['m3_deadline'] != deadline:
            raise ValueError('Final receipt exceeds or differs from deadline')
    except (TypeError, KeyError, json.JSONDecodeError) as exc:
        raise ValueError('Unknown final outcome; operator-reviewed recovery required') from exc
    return raw


def receipt_usage(manifest):
    # Existing receipts themselves are the ledger, including retained failures.
    paths = set()
    for pattern in manifest['budget']['m3_receipt_patterns']:
        if not isinstance(pattern,str) or '/' in pattern or '..' in pattern:
            raise ValueError('Unsafe receipt pattern')
        paths.update(HERE.glob(pattern))
    if any(path.is_symlink() or not path.is_file() for path in paths):
        raise ValueError('Invalid M3 receipt file')
    return sum(path.stat().st_size for path in paths)


def exchange(args, remote, bundle, request_hash, deadline, margin, out, err, output_limit, now):
    process = subprocess.Popen(args.ssh_argv + [remote], stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)
    ready = False
    sent_go = False
    first_line = bytearray()
    pending = memoryview(bundle + b'\n')
    rc = None
    with selectors.DefaultSelector() as selector:
        for stream, name, events in ((process.stdin,'input',selectors.EVENT_WRITE),
                (process.stdout,'stdout',selectors.EVENT_READ), (process.stderr,'stderr',selectors.EVENT_READ)):
            os.set_blocking(stream.fileno(),False)
            selector.register(stream,events,name)
        try:
            while selector.get_map():
                left = deadline - now()
                if left <= 0:
                    raise ValueError('M3 hard deadline')
                for key, _ in selector.select(min(left,1)):
                    stream, name = key.fileobj, key.data
                    if name == 'input':
                        if pending:
                            try:
                                count = os.write(stream.fileno(),pending)
                            except BlockingIOError:
                                continue
                            pending = pending[count:]
                            if pending:
                                continue
                            selector.unregister(stream)
                            if ready:
                                selector.register(stream,selectors.EVENT_WRITE,'go')
                    elif name == 'go':
                        # This reading follows READY and immediately precedes the GO write.
                        args.remaining_seconds = deadline - now() - margin
                        if not math.isfinite(args.remaining_seconds) or args.remaining_seconds <= 0:
                            raise ValueError('M3 deadline exhausted at GO')
                        go = ('R1I-GO '+str(args.remaining_seconds)+'\n').encode()
                        try:
                            count = os.write(stream.fileno(),go)
                        except BlockingIOError:
                            continue
                        if count != len(go):
                            raise ValueError('Partial GO/disconnection')
                        sent_go = True
                        selector.unregister(stream)
                    else:
                        data = os.read(stream.fileno(),65536)
                        if not data:
                            selector.unregister(stream)
                            continue
                        used = os.fstat(out.fileno()).st_size + os.fstat(err.fileno()).st_size
                        if used + len(data) > output_limit:
                            raise ValueError('M3 dispatch receipt output bound exceeded')
                        (out if name == 'stdout' else err).write(data)
                        if name == 'stdout' and not ready:
                            first_line.extend(data)
                            if b'\n' in first_line:
                                line, rest = bytes(first_line).split(b'\n',1)
                                if line != b'R1I-READY '+request_hash.encode() or rest:
                                    raise ValueError('READY must be first and only pre-GO stdout line')
                                ready = True
                                if not pending:
                                    selector.register(process.stdin,selectors.EVENT_WRITE,'go')
                if not any(key.data in ('stdout','stderr') for key in selector.get_map().values()):
                    break
            rc = process.wait(timeout=max(0,deadline-now()))
            if not ready or not sent_go:
                raise ValueError('EOF before READY/GO')
        except (OSError,ValueError,subprocess.TimeoutExpired) as exc:
            process.kill()
            process.wait()
            err.write(('REFUSED: '+str(exc)+'; operator-reviewed recovery required\n').encode()[:1024])
            rc = 124
        finally:
            for stream in (process.stdin,process.stdout,process.stderr):
                stream.close()
    return rc


def dispatch(args, now=time.time):
    manifest = json.loads((HERE/'intel_provisioning_manifest_v8.json').read_bytes())
    budget = manifest['budget']
    margin = budget['transit_margin_seconds']
    bound = budget['max_dispatch_receipt_bytes']
    if type(margin) not in (int,float) or not math.isfinite(margin) or margin <= 0 or type(bound) is not int or bound <= 4096:
        raise ValueError('Invalid sealed dispatch bounds')
    limit = [row['bytes'] for row in budget['components'] if row['id']=='receipts']
    if limit != [manifest['collector']['receipt_limit_bytes']]:
        raise ValueError('Single receipt allowance differs')
    used = receipt_usage(manifest)
    if limit[0] - used < bound:
        raise ValueError('Insufficient remaining receipt allowance before dispatch')
    capture = Path(args.capture).read_bytes() if args.capture else None
    attempt_path = None
    duration = budget.get('time_total_s',870)
    if args.mode == 'inventory':
        if not re.fullmatch(r'[0-9a-f]{64}', args.expected_capture_sha256 or '') or hashlib.sha256(capture).hexdigest() != args.expected_capture_sha256:
            raise ValueError('Complete capture SHA-256 mismatch on M3')
        value = publication(capture)
        core = json.loads(value['bound_manifest_json'])['window_seal']['core_sha256']
        if args.expected_anchor == 'none':
            seq, head = '0', core
        elif re.fullmatch(r'(0|[1-9][0-9]*):[0-9a-f]{64}', args.expected_anchor or ''):
            seq, head = args.expected_anchor.split(':')
        else:
            raise ValueError('Exact anchor required')
        attempt_path = HERE/('r1i_attempt_'+seq+'_'+head[:12]+'.json')
        if attempt_path.exists() or attempt_path.is_symlink():
            raise ValueError('Anchor already consumed; operator-reviewed recovery required; never retry')
        committed = committed_bytes(args.capture)
        if hashlib.sha256(committed).hexdigest() != args.expected_capture_sha256:
            raise ValueError('Committed capture hash differs from supplied authority')
        bootstrap = value['binding_receipt']['bootstrap_start_utc']
        deadline = datetime.datetime.strptime(bootstrap,'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc).timestamp()+duration
        qualified(Path(args.capture).with_suffix(''),deadline,committed=True)
        require_anchor(args.expected_anchor,core)
        prefix = HERE/('r1i_inventory_'+seq+'_'+head[:12])
        args.capture_prefix = str(prefix)
        args.m3_receipt_bytes = used - args.bootstrap_bytes + bound
        if args.m3_receipt_bytes < 0:
            raise ValueError('Bootstrap receipts absent from measured allowance')
    else:
        prefix = Path(args.capture_prefix)
        if prefix.resolve().parent != HERE.resolve() or not prefix.name.startswith('r1i_'+args.mode+'_') or '..' in prefix.name:
            raise ValueError('Capture prefix must be a new safe M3 RE path')
        start = datetime.datetime.strptime(args.bootstrap_start_utc,'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc).timestamp() if args.mode=='bind' else now()
        deadline = start + duration
    if deadline <= now():
        raise ValueError('M3 bootstrap deadline exhausted before ssh')
    members = build(args)
    hashes = {name:hashlib.sha256(raw).hexdigest() for name,raw in members.items()}
    remote = shlex.join(json.loads(members['request'])['invoked_argv_prefix']+[args.mode,json.dumps(hashes,sort_keys=True)])
    bundle = json.dumps({name:base64.b64encode(raw).decode('ascii') for name,raw in members.items()},sort_keys=True).encode()
    if attempt_path is not None:
        record = {'anchor':args.expected_anchor,'core_sha256':core,'capture_sha256':args.expected_capture_sha256,
            'capture_prefix':str(prefix),'m3_deadline':deadline}
        exclusive_record(attempt_path,(json.dumps(record,sort_keys=True)+'\n').encode())
    paths = [prefix.with_suffix(x) for x in ('.json','.stderr','.exit')]
    if prefix.with_suffix('.final').exists() or prefix.with_suffix('.final').is_symlink():
        raise ValueError('Existing final receipt; never retry')
    opened=[]
    try:
        for path in paths:
            fd=os.open(str(path),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            opened.append(os.fdopen(fd,'wb',buffering=0))
        syncdir(prefix.parent)
        out,err,status=opened
        output_limit=bound-4096-(attempt_path.stat().st_size if attempt_path is not None else 0)
        try:
            rc=exchange(args,remote,bundle,hashes['request'],deadline,margin,out,err,output_limit,now)
        except OSError as exc:
            rc=125
            err.write(('REFUSED: ssh failed: '+str(exc)+'\n').encode()[:1024])
        if rc==0:
            if args.mode=='inventory':
                try:
                    successor_core,successor=last_anchor(paths[0].read_bytes(),b'0\n')
                    if successor_core != core:
                        raise ValueError('Successor core differs')
                except ValueError as exc:
                    rc=125; err.write(('REFUSED: '+str(exc)+'\n').encode()[:1024])
            else:
                try:
                    value=publication(paths[0].read_bytes())
                    if not isinstance(value,dict) or not value:
                        raise ValueError('Empty/malformed capture')
                except ValueError as exc:
                    rc=125; err.write(('REFUSED: '+str(exc)+'\n').encode()[:1024])
        os.fsync(out.fileno()); os.fsync(err.fileno()); syncdir(prefix.parent)
        if now()>deadline:
            rc=124; err.write(b'REFUSED: M3 end past bootstrap deadline\n')
        # Exactly one status write. Zero is provisional until committed final qualification.
        status.write(('%d\n'%rc).encode())
        for stream in opened: os.fsync(stream.fileno())
        syncdir(prefix.parent)
        qualified_at=now()
        if rc==0:
            if qualified_at>deadline:
                rc=124
            else:
                final={'exit':0,'qualified':True,'m3_deadline':deadline,'m3_qualified_at':qualified_at}
                try:
                    exclusive_record(prefix.with_suffix('.final'),(json.dumps(final,sort_keys=True,allow_nan=False)+'\n').encode())
                except OSError:
                    # Retained failed-final bytes must stay disqualified even when committed.
                    err.write(b'REFUSED: final receipt persistence failed; operator-reviewed recovery required\n')
                    os.fsync(err.fileno()); syncdir(prefix.parent)
                    raise
    finally:
        for stream in opened: stream.close()
    if rc!=0:
        print('REFUSED: capture failed; operator-reviewed recovery required: '+str(prefix),file=sys.stderr)
        return rc
    if args.mode=='inventory':
        print('R1H-SUCCESSOR '+successor+' '+str(paths[0]),flush=True)
        print('R1H-ATTEMPT '+str(attempt_path),flush=True)
    else:
        raw=paths[0].read_bytes()
        print('R1H-CAPTURE '+str(paths[0])+' '+hashlib.sha256(raw).hexdigest(),flush=True)
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
        final = qualified(path.with_suffix(''),committed=True)
        print(len(capture) + len(stderr) + len(status) + len(final))
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
