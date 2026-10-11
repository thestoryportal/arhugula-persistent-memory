import time
PROCESS_START_MONOTONIC = time.monotonic()

import base64
import hashlib
import json
import sys


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ('probe', 'bind', 'inventory'):
        raise ValueError('usage: MODE EXPECTED_MEMBER_HASHES_JSON')
    mode = sys.argv[1]
    expected = json.loads(sys.argv[2])
    bundle = json.load(sys.stdin)
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
    namespaces = {}
    for name in ('identity', 'collector', 'binder'):
        fresh = {'__name__': 'r1h_' + name, 'PROCESS_START_MONOTONIC': PROCESS_START_MONOTONIC, 'VERIFIED_MEMBERS': verified,
            'VERIFIED_HASHES': expected, 'VERIFIED_PROBE': namespaces.get('identity'),
            'VERIFIED_COLLECTOR': namespaces.get('collector'), 'STUB_TEXT': stub_text}
        exec(compile(verified[name], '<r1h:' + name + '>', 'exec'), fresh)
        namespaces[name] = fresh
        if mode == 'probe':
            print(json.dumps(fresh['interpreter_identity'](), sort_keys=True, allow_nan=False), flush=True)
            return 0
    if mode == 'bind':
        return namespaces['binder']['entrypoint']()
    request = json.loads(verified['request'])
    return namespaces['collector']['entrypoint'](request['collector_argv'])


try:
    sys.exit(main())
except (ValueError, TypeError, KeyError, OSError) as error:
    print('REFUSED: ' + str(error), file=sys.stderr, flush=True)
    sys.exit(1)
