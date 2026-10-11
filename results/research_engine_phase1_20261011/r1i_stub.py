import time
PROCESS_START_MONOTONIC = time.monotonic()

import base64
import hashlib
import json
import sys
import os
import math
import select

PENDING = b''


def read_line(deadline=None):
    global PENDING
    while b'\n' not in PENDING:
        left = None if deadline is None else deadline - time.monotonic()
        if left is not None and left <= 0:
            raise ValueError('Pre-GO cap expired')
        if not select.select([sys.stdin.fileno()], [], [], left)[0]:
            raise ValueError('Pre-GO cap expired')
        data = os.read(sys.stdin.fileno(), 65536)
        if not data:
            raise ValueError('Stdin EOF before GO')
        PENDING += data
    line, PENDING = PENDING.split(b'\n', 1)
    return line


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ('probe', 'bind', 'inventory'):
        raise ValueError('usage: MODE EXPECTED_MEMBER_HASHES_JSON')
    mode = sys.argv[1]
    expected = json.loads(sys.argv[2])
    bundle = json.loads(read_line())
    names = {'identity', 'collector', 'binder', 'manifest', 'probe', 'capture', 'request'}
    if set(bundle) != names or set(expected) != names:
        raise ValueError('Exact complete member set required')
    verified = {}
    # Complete verification precedes the first compile, including on probe paths.
    for name in sorted(names):
        source = base64.b64decode(bundle[name], validate=True)
        if not isinstance(expected[name], str) or len(expected[name]) != 64 or hashlib.sha256(source).hexdigest() != expected[name]:
            raise ValueError('Member SHA-256 mismatch: ' + name)
        verified[name] = source
    stub_text = json.loads(verified['request'])['stub_text']
    if not isinstance(stub_text, str) or not stub_text:
        raise ValueError('Exact stub command text required in verified request')
    manifest = json.loads(verified['manifest'])
    cap = manifest['budget']['pre_go_cap_seconds']
    if type(cap) not in (int, float) or not math.isfinite(cap) or cap <= 0:
        raise ValueError('Invalid sealed pre-GO cap')
    if time.monotonic() - PROCESS_START_MONOTONIC >= cap:
        raise ValueError('Pre-GO cap expired')
    print('R1I-READY ' + expected['request'], flush=True)
    go = read_line(PROCESS_START_MONOTONIC + cap).decode('ascii').split(' ')
    if len(go) != 2 or go[0] != 'R1I-GO':
        raise ValueError('Malformed GO')
    budget = float(go[1])
    limit = min(manifest['budget']['clock_seconds'], manifest['budget'].get('time_total_s', manifest['budget']['clock_seconds']))
    if not math.isfinite(budget) or not 0 < budget <= limit:
        raise ValueError('Invalid GO budget')

    def check_time():
        if time.monotonic() - PROCESS_START_MONOTONIC >= budget:
            raise ValueError('Intel monotonic budget expired')

    def transport_check():
        check_time()
        if PENDING or select.select([sys.stdin.fileno()], [], [], 0)[0]:
            raise ValueError('Stdin disconnected or unexpected data after GO')
        # A flushed progress byte sequence detects a closed stdout before any effect.
        try:
            print('R1I-LIVE', flush=True)
        except OSError as exc:
            raise ValueError('Stdout disconnected after GO') from exc

    namespaces = {}
    for name in ('identity', 'collector', 'binder'):
        fresh = {'__name__': 'r1i_' + name, 'PROCESS_START_MONOTONIC': PROCESS_START_MONOTONIC, 'VERIFIED_MEMBERS': verified,
            'VERIFIED_HASHES': expected, 'VERIFIED_PROBE': namespaces.get('identity'),
            'VERIFIED_COLLECTOR': namespaces.get('collector'), 'STUB_TEXT': stub_text}
        check_time()
        fresh['TRANSPORT_CHECK'] = transport_check
        exec(compile(verified[name], '<r1i:' + name + '>', 'exec'), fresh)
        namespaces[name] = fresh
        if mode == 'probe':
            print(json.dumps(fresh['interpreter_identity'](), sort_keys=True, allow_nan=False), flush=True)
            return 0
    if mode == 'bind':
        return namespaces['binder']['entrypoint']()
    request = json.loads(verified['request'])
    return namespaces['collector']['entrypoint'](request['collector_argv'] + ['--remaining-seconds', str(budget)])


try:
    sys.exit(main())
except (ValueError, TypeError, KeyError, OSError) as error:
    print('REFUSED: ' + str(error), file=sys.stderr, flush=True)
    sys.exit(1)
