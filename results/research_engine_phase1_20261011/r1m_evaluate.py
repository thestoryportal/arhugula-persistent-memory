"""Frozen local sizing rule. Exit 0 PASS; exit 1 FAIL. Stdlib only."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import sys

from r1m_size_probe import (COLLECTOR_SHA256, MANIFEST_SHA256, MAX_SUMMARY_BYTES,
                            OLD_ROOTS, FUTURE_COLLECTOR_ROW_BYTES, FUTURE_COLLECTOR_ENTRIES)

RECEIPT_CAP = 18000000
SETUP_CAP = 2000000000
DISPATCH_CAP = 2500000
DRIFT_RECEIPT_BYTES = 1000000
DRIFT_LIVE_BYTES = 100000
MAX_AGE_SECONDS = 3600
OVERHEAD = {'registration_bytes': 65536, 'window_bytes': 65536,
            'failure_bytes': 16384, 'emergency_journal_bytes': 4096,
            'accounting_bytes': 4096, 'summary_bytes': 65536,
            'attempt_bytes': 4096, 'sizing_capture_bytes': MAX_SUMMARY_BYTES + 4096}
FIXED_LIVE_CALLS = 256
LIVE_NON_PROGRESS_BYTES = 65536


def parse_capture(raw):
    if len(raw) > MAX_SUMMARY_BYTES + 75:
        raise ValueError('summary bound exceeded')
    if raw.startswith(b'R1I-READY '):
        lines = raw.splitlines()
        if len(lines) != 2 or not re.fullmatch(b'R1I-READY [0-9a-f]{64}', lines[0]):
            raise ValueError('sizing transport framing differs')
        result = json.loads(lines[1])
        if result.get('dispatch_request_sha256') != lines[0][len(b'R1I-READY '):].decode('ascii'):
            raise ValueError('sizing request pin differs')
        if len(lines[1]) + 1 > MAX_SUMMARY_BYTES:
            raise ValueError('summary bound exceeded')
        return result
    return json.loads(raw)


def evaluate(probe, manifest, measured_m3_bytes, fixture=False):
    if probe['schema'] != 'R1M-sizing-v1' or probe['stable_two_passes'] is not True:
        raise ValueError('unqualified sizing schema/stability')
    expected = hashlib.sha256((json.dumps(manifest, sort_keys=True, allow_nan=False)+'\n').encode()).hexdigest() if fixture else MANIFEST_SHA256
    if probe['manifest_sha256'] != expected or probe['collector_sha256'] != COLLECTOR_SHA256:
        raise ValueError('sizing source pins differ')
    if probe['sizing_probe_sha256'] != hashlib.sha256((Path(__file__).resolve().parent/'r1m_size_probe.py').read_bytes()).hexdigest():
        raise ValueError('sizing probe pin differs')
    if [r['root'] for r in probe['roots']] != manifest['collector']['admitted_write_roots']:
        raise ValueError('sizing roots differ')
    if not fixture and probe['old_state']['roots'] != OLD_ROOTS:
        raise ValueError('old-state roots differ')
    for key in ['inventory_row_bound_bytes', 'observed_row_bytes', 'rows', 'walk_remaining_calls', 'hash_chunks']:
        if type(probe[key]) is not int or probe[key] < 0:
            raise ValueError('invalid nonnegative sizing term: ' + key)
    old_bytes = probe['old_state']['total_bytes']
    if type(old_bytes) is not int or old_bytes < 0 or old_bytes != sum(x['size'] for x in probe['old_state']['files']):
        raise ValueError('old-state file sizes differ')
    if probe['inventory_row_bound_bytes'] != probe['observed_row_bytes'] + FUTURE_COLLECTOR_ROW_BYTES:
        raise ValueError('inventory row bound differs')
    for key, root_key in [('observed_row_bytes', 'row_bytes'), ('rows', 'rows'),
                          ('walk_remaining_calls', 'walk_remaining_calls'), ('hash_chunks', 'hash_chunks')]:
        if probe[key] != sum(r[root_key] for r in probe['roots']):
            raise ValueError('sizing root totals differ: ' + key)
    if type(measured_m3_bytes) is not int or measured_m3_bytes < 0:
        raise ValueError('invalid measured M3 term')
    terms = dict(OVERHEAD, old_intel_state_bytes=old_bytes,
        inventory_rows_bytes=probe['inventory_row_bound_bytes'], measured_m3_bytes=measured_m3_bytes,
        fresh_bind_dispatch_bytes=DISPATCH_CAP, inventory_dispatch_bytes=DISPATCH_CAP,
        drift_receipt_bytes=DRIFT_RECEIPT_BYTES)
    required = sum(terms.values())
    nonreceipts = sum(x['bytes'] for x in manifest['budget']['components'] if x['id'] != 'receipts')
    live_calls = (2 * probe['rows'] + probe['walk_remaining_calls'] + probe['hash_chunks'] +
                  3 * FUTURE_COLLECTOR_ENTRIES + FIXED_LIVE_CALLS)
    live = live_calls * len(b'R1I-LIVE\n') + LIVE_NON_PROGRESS_BYTES + DRIFT_LIVE_BYTES
    setup = nonreceipts + required
    sealed_ok = (manifest['collector']['receipt_limit_bytes'] == RECEIPT_CAP and
        [x['bytes'] for x in manifest['budget']['components'] if x['id']=='receipts'] == [RECEIPT_CAP] and
        manifest['budget']['setup_cap_bytes'] == SETUP_CAP and
        manifest['budget']['max_dispatch_receipt_bytes'] == DISPATCH_CAP and
        manifest['budget']['planned_peak_bytes'] == nonreceipts + RECEIPT_CAP)
    receipt_pass, setup_pass, live_pass = required <= RECEIPT_CAP, setup <= SETUP_CAP, live <= DISPATCH_CAP
    return dict(terms=terms, required_receipt_bytes=required, receipt_cap_bytes=RECEIPT_CAP,
        nonreceipt_setup_bytes=nonreceipts, required_setup_bytes=setup, setup_cap_bytes=SETUP_CAP,
        rows=probe['rows'], walk_remaining_calls=probe['walk_remaining_calls'], hash_chunks=probe['hash_chunks'],
        future_collector_entries=FUTURE_COLLECTOR_ENTRIES, fixed_live_calls=FIXED_LIVE_CALLS,
        live_calls_bound=live_calls, live_progress_bytes=live_calls*9,
        live_non_progress_bytes=LIVE_NON_PROGRESS_BYTES, drift_live_bytes=DRIFT_LIVE_BYTES,
        live_dispatch_bytes=live, dispatch_cap_bytes=DISPATCH_CAP,
        receipt_pass=receipt_pass, setup_pass=setup_pass, live_pass=live_pass, sealed_policy_pass=sealed_ok,
        verdict='PASS' if all([receipt_pass, setup_pass, live_pass, sealed_ok]) else 'FAIL')


def local_receipts(manifest, directory):
    paths = set()
    for pattern in manifest['budget']['m3_receipt_patterns']:
        if not isinstance(pattern, str) or '/' in pattern or '..' in pattern:
            raise ValueError('unsafe M3 pattern')
        paths.update(directory.glob(pattern))
    if any(p.is_symlink() or not p.is_file() for p in paths):
        raise ValueError('invalid M3 receipt file')
    return sum(p.stat().st_size for p in paths)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('capture')
    parser.add_argument('manifest')
    args = parser.parse_args()
    capture, path = Path(args.capture), Path(args.manifest)
    with capture.open('rb') as stream:
        raw = stream.read(MAX_SUMMARY_BYTES + 76)
    manifest_raw = path.read_bytes()
    if hashlib.sha256(manifest_raw).hexdigest() != MANIFEST_SHA256:
        raise ValueError('manifest pin differs')
    manifest, probe = json.loads(manifest_raw), parse_capture(raw)
    import time
    age = time.time_ns() - probe['measured_at_unix_ns']
    if not 0 <= age <= MAX_AGE_SECONDS * 1000000000:
        raise ValueError('sizing older than one hour or future-dated')
    result = evaluate(probe, manifest, local_receipts(manifest, path.parent))
    result['capture_sha256'] = hashlib.sha256(raw).hexdigest()
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0 if result['verdict'] == 'PASS' else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'verdict': 'FAIL', 'error': str(exc)[:1024]}))
        sys.exit(1)
