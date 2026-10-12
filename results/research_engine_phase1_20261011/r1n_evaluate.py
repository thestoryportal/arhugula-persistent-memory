"""Fixed v11 sizing rule; historical CAP replay is explicitly non-authoritative."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

from r1m_evaluate import parse_capture
from r1m_size_probe import (COLLECTOR_SHA256, OLD_ROOTS, MAX_SUMMARY_BYTES,
                           FUTURE_COLLECTOR_ROW_BYTES, FUTURE_COLLECTOR_ENTRIES)
from r1n_make_manifest_v11 import generated_bytes, RECEIPT_CAP, W1_SEAL_HEADROOM_BYTES

HERE = Path(__file__).resolve().parent
MANIFEST_SHA256 = hashlib.sha256(generated_bytes()).hexdigest()
CAP_NAME = 'r1j_probe_r1m_20261011T154940Z.json'
CAP_SHA256 = '1c330b25b5a3921b197a8d60fc12aca0d33183e0e4b9d52f0741aa382755a9ed'
CAP_ROW_BYTES = 20_048_510
DRIFT_DENOMINATOR = 5
DRIFT_FLOOR_BYTES = 1_000_000
SETUP_CAP = 2_000_000_000
DISPATCH_CAP = 2_500_000
DRIFT_LIVE_BYTES = 100_000
MAX_AGE_SECONDS = 3600
SIZING_ENVELOPE = MAX_SUMMARY_BYTES + 4096
OVERHEAD = {'registration_bytes': 65536, 'window_bytes': 65536,
            'failure_bytes': 16384, 'emergency_journal_bytes': 4096,
            'accounting_bytes': 4096, 'summary_bytes': 65536,
            'attempt_bytes': 4096, 'sizing_capture_bytes': SIZING_ENVELOPE}
EVIDENCE_SUFFIXES = ('.json', '.out', '.stderr', '.exit', '.final', '.pending')


def drift_reserve(row_bytes):
    return max(DRIFT_FLOOR_BYTES, (row_bytes + DRIFT_DENOMINATOR - 1) // DRIFT_DENOMINATOR)


def probe_pin():
    from r1n_sizing_dispatch import probe_member
    return hashlib.sha256(probe_member()).hexdigest()


def check_age(probe, now_ns):
    stamp = probe['measured_at_unix_ns']
    if type(stamp) is not int or not 0 <= now_ns - stamp <= MAX_AGE_SECONDS * 10**9:
        raise ValueError('sizing older than one hour or future-dated')


def evaluate(probe, manifest, measured_m3_bytes, omitted_m3_bytes, replay=False):
    if manifest != json.loads(generated_bytes()):
        raise ValueError('v11 manifest differs from fixed plan')
    from r1n_sizing_dispatch import verify_pins
    verify_pins()
    if replay:
        cap_raw = (HERE / CAP_NAME).read_bytes()
        if hashlib.sha256(cap_raw).hexdigest() != CAP_SHA256 or probe != parse_capture(cap_raw):
            raise ValueError('historical replay requires exact pinned CAP')
        # Same-width v11 root names preserve CAP's sizing baseline only for replay.
        expected_roots = [x.replace('-v11', '-v10') for x in manifest['collector']['admitted_write_roots']]
    else:
        if probe['manifest_sha256'] != MANIFEST_SHA256 or probe['sizing_probe_sha256'] != probe_pin():
            raise ValueError('v11 sizing source pins differ')
        expected_roots = manifest['collector']['admitted_write_roots']
    if probe['schema'] != 'R1M-sizing-v1' or probe['stable_two_passes'] is not True or probe['collector_sha256'] != COLLECTOR_SHA256:
        raise ValueError('unqualified sizing schema/stability/collector')
    if [r['root'] for r in probe['roots']] != expected_roots or probe['old_state']['roots'] != OLD_ROOTS:
        raise ValueError('sizing roots differ')
    keys = ['inventory_row_bound_bytes', 'observed_row_bytes', 'rows', 'walk_remaining_calls', 'hash_chunks']
    for key in keys:
        if type(probe[key]) is not int or probe[key] < 0:
            raise ValueError('invalid nonnegative sizing term: ' + key)
    for value in (measured_m3_bytes, omitted_m3_bytes):
        if type(value) is not int or value < 0:
            raise ValueError('invalid nonnegative M3 term')
    old_bytes = probe['old_state']['total_bytes']
    sizes = [x['size'] for x in probe['old_state']['files']]
    if any(type(x) is not int or x < 0 for x in sizes) or type(old_bytes) is not int or old_bytes < 0 or old_bytes != sum(sizes):
        raise ValueError('old-state file sizes differ')
    if probe['inventory_row_bound_bytes'] != probe['observed_row_bytes'] + FUTURE_COLLECTOR_ROW_BYTES:
        raise ValueError('inventory row bound differs')
    for key, root_key in [('observed_row_bytes', 'row_bytes'), ('rows', 'rows'),
                          ('walk_remaining_calls', 'walk_remaining_calls'), ('hash_chunks', 'hash_chunks')]:
        values = [r[root_key] for r in probe['roots']]
        if any(type(x) is not int or x < 0 for x in values) or probe[key] != sum(values):
            raise ValueError('sizing root totals differ: ' + key)
    terms = dict(OVERHEAD, old_intel_state_bytes=old_bytes,
        inventory_rows_bytes=probe['inventory_row_bound_bytes'], measured_m3_bytes=measured_m3_bytes,
        omitted_m3_bytes=omitted_m3_bytes, fresh_bind_dispatch_bytes=DISPATCH_CAP,
        inventory_dispatch_bytes=DISPATCH_CAP, drift_receipt_bytes=drift_reserve(probe['observed_row_bytes']))
    required = sum(terms.values())
    nonreceipts = sum(x['bytes'] for x in manifest['budget']['components'] if x['id'] != 'receipts')
    calls = 2 * probe['rows'] + probe['walk_remaining_calls'] + probe['hash_chunks'] + 3 * FUTURE_COLLECTOR_ENTRIES + 256
    live = calls * 9 + 65536 + DRIFT_LIVE_BYTES
    setup = nonreceipts + required
    receipt_pass, setup_pass, live_pass = required <= RECEIPT_CAP, setup <= SETUP_CAP, live <= DISPATCH_CAP
    return dict(terms=terms, required_receipt_bytes=required, receipt_cap_bytes=RECEIPT_CAP,
        nonreceipt_setup_bytes=nonreceipts, required_setup_bytes=setup, setup_cap_bytes=SETUP_CAP,
        planned_peak_bytes=manifest['budget']['planned_peak_bytes'], rows=probe['rows'],
        walk_remaining_calls=probe['walk_remaining_calls'], hash_chunks=probe['hash_chunks'],
        future_collector_entries=FUTURE_COLLECTOR_ENTRIES, fixed_live_calls=256,
        live_calls_bound=calls, live_progress_bytes=calls*9, live_non_progress_bytes=65536,
        drift_live_bytes=DRIFT_LIVE_BYTES, live_dispatch_bytes=live, dispatch_cap_bytes=DISPATCH_CAP,
        drift_rule='max(1000000, ceil(observed_row_bytes / 5))',
        receipt_pass=receipt_pass, setup_pass=setup_pass, live_pass=live_pass, sealed_policy_pass=True,
        replay_only=replay, w1_seal_headroom_bytes=W1_SEAL_HEADROOM_BYTES,
        verdict='PASS' if all((receipt_pass, setup_pass, live_pass)) else 'FAIL')


def local_accounting(manifest, directory, sizing_prefix=None, extra_receipts=()):
    directory = Path(directory)
    matched = set()
    for pattern in manifest['budget']['m3_receipt_patterns']:
        if not isinstance(pattern, str) or '/' in pattern or '..' in pattern:
            raise ValueError('unsafe M3 receipt pattern')
        matched.update(directory.glob(pattern))
    # Recognizable R1 receipt records, including all earlier rounds and sidecars.
    candidates = {p for p in directory.glob('r1*') if p.name.endswith(EVIDENCE_SUFFIXES)}
    candidates.update(Path(p) for p in extra_receipts)
    sizing = set()
    if sizing_prefix is not None:
        prefix = Path(sizing_prefix)
        sizing = set(prefix.parent.glob(prefix.name + '.*'))
    paths = matched | candidates | sizing
    if any(p.is_symlink() or not p.is_file() for p in paths):
        raise ValueError('invalid M3 receipt file')
    sizes = {p: p.stat().st_size for p in paths}
    total = sum(sizes[p] for p in sizing)
    if total > SIZING_ENVELOPE:
        raise ValueError('complete sizing set exceeds fixed envelope')
    matched -= sizing
    omitted = paths - matched - sizing
    return dict(matched_bytes=sum(sizes[p] for p in matched), omitted_bytes=sum(sizes[p] for p in omitted),
        sizing_set_bytes=total, sizing_envelope_bytes=SIZING_ENVELOPE,
        matched_files={str(p): sizes[p] for p in sorted(matched)},
        omitted_files={str(p): sizes[p] for p in sorted(omitted)},
        sizing_files={str(p): sizes[p] for p in sorted(sizing)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('capture')
    parser.add_argument('manifest')
    parser.add_argument('--replay-cap', action='store_true', help='exact historical CAP only; never chain authority')
    parser.add_argument('--extra-receipt', action='append', default=[], help='explicit evidence outside the R1 filename census')
    args = parser.parse_args()
    capture, path = Path(args.capture), Path(args.manifest)
    raw_manifest = path.read_bytes()
    if hashlib.sha256(raw_manifest).hexdigest() != MANIFEST_SHA256:
        raise ValueError('manifest pin differs')
    with capture.open('rb') as stream:
        raw = stream.read(MAX_SUMMARY_BYTES + 76)
    probe = parse_capture(raw)
    if args.replay_cap and hashlib.sha256(raw).hexdigest() != CAP_SHA256:
        raise ValueError('replay requires pinned CAP bytes')
    if not args.replay_cap:
        check_age(probe, time.time_ns())
        from r1n_sizing_dispatch import load_maker
        load_maker().qualified(capture.with_suffix(''), committed=False)
    manifest = json.loads(raw_manifest)
    info = local_accounting(manifest, path.parent,
        sizing_prefix=None if args.replay_cap else capture.with_suffix(''), extra_receipts=args.extra_receipt)
    result = evaluate(probe, manifest, info['matched_bytes'], info['omitted_bytes'], replay=args.replay_cap)
    result.update(capture_sha256=hashlib.sha256(raw).hexdigest(), evidence=info)
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0 if result['verdict'] == 'PASS' else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'verdict': 'FAIL', 'error': str(exc)[:1024]}))
        sys.exit(1)
