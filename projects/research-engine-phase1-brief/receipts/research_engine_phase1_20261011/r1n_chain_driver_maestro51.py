"""MAESTRO51 driver for R1N chain C, Gate D and E (GD11 + r13 addendum). Every Intel call goes through A.load_maker(sizing=False).

usage: bind BIND_PREFIX START_UTC | gate BIND_PREFIX START_UTC | inventory BIND_PREFIX
"""
import calendar
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import r1n_sizing_dispatch as A  # noqa: E402
import r1n_evaluate as N  # noqa: E402

PROBE = HERE / 'intel_identity_probe_r1h_20261011T131105Z.json'  # direct identity probe used by every earlier bind
SIZING = HERE / 'r1j_probe_r1n_20261011T164501Z'
B_OUT = HERE / 'r1n_evaluate_20261011T164501Z.out'
EXTRAS = sorted(HERE.glob('intel_identity_probe_*'))
CONSUMED_CORE = 'a49c11de49ce325c23ce47591355e5c4e38bc55730025f91ed2cdc3e55b18792'
WINDOW = 870
MIN_REMAINING_AT_GO = 420  # declared before C: inventory + preservation + commits
REVIEWED = {  # r13 addendum (R1) full hashes and A's predecessor pins
    'r1n_make_manifest_v11.py': '1ceee5a04b2c8ae633a6a1c972c08bc76a172063217942831a1817d66d2454fb',
    'intel_provisioning_manifest_v11.json': 'daf38de28b19ba61007d87730de5382a5ade54b1338a3cd0e620a395e9be5fd7',
    'r1n_evaluate.py': '99e38c197d1387c6000940675ecc6c005c46e8f676423296567010fbdd4c70a5',
    'r1n_sizing_dispatch.py': '45a752a0bdc214b243d6831ecb1197e9247a48fb16e4292bd9e88daa57a8d8f3',
    'r1n_gate_d_checklist.md': '3732792a3d991b660cba376c2f32d0766937b6450af918d95ec24e812abd6311',
    'test_r1n_replan.py': '0c227b4e30ad905fcb5df5f3278030747f8e8dad316ca8cddde30294df8b28d9',
    'r1n_report.md': 'e62858047841e4307889ca5a18cd8e31677f77adf40019a710c961ada56beff6',
    'r1j_host_commands.sh': 'a4b52fc281030ebec2c5cefd433173d3bbe732710af12d1808fbcd7768c24542',
    **{k: v for k, v in A.PINS.items() if k != 'intel_provisioning_manifest_v11.json'},
    'intel_provisioning_manifest_v10.json': '748fc72aa49bcdb963d99b89bbc29859237d1bbd32b84b8e05fd38d07bd9df3f',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def committed(path):
    rel = Path(path).resolve().relative_to(HERE.resolve())
    out = subprocess.run(['git', '-C', str(HERE), 'cat-file', 'blob', 'HEAD:./' + str(rel)], capture_output=True)
    if out.returncode != 0:
        raise ValueError('not committed: ' + str(rel))
    return out.stdout


def ssh(command):
    out = subprocess.run(A.SSH_ARGV[:1] + ['-o', 'ConnectTimeout=10'] + A.SSH_ARGV[1:] + [command],
                         capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        raise ValueError('ssh failed: ' + out.stderr[:300])
    return out.stdout


def run_maker(argv):
    maker = A.load_maker(sizing=False)
    sys.argv = ['r1l_make_bundle.py', *argv]
    return maker.main()


def bind(prefix, start):
    return run_maker(['bind', '--dispatch-m3', '--capture-prefix', prefix, '--probe', str(PROBE),
                      '--bootstrap-start-utc', start, '--ssh-argv', *A.SSH_ARGV])


def bind_facts(prefix):
    raw = committed(prefix + '.json')
    value = json.loads(raw.split(b'\n', 1)[1] if raw.startswith(b'R1I-READY ') else raw)
    bound = json.loads(value['bound_manifest_json'])
    return raw, value, bound


def gate(prefix, start):
    checks = {}
    deadline = calendar.timegm(time.strptime(start, '%Y-%m-%dT%H:%M:%SZ')) + WINDOW
    # 1 identities
    bad = [n for n, h in REVIEWED.items() if sha((HERE / n).read_bytes()) != h or sha(committed(HERE / n)) != h]
    cap = committed(SIZING.with_suffix('.json'))
    b_result = json.loads(committed(B_OUT))
    checks[1] = (not bad and b_result['capture_sha256'] == sha(cap) == '3506fe32f9b301e92489a9fa300b1357efca54122ec37a36a77f546aaf0beefd',
                 f'mismatches={bad} N.capture_sha256={b_result["capture_sha256"][:12]} committed={sha(cap)[:12]}')
    # 2 fresh sizing: qualified, v11, not future-dated, <=3600 s old now
    final = json.loads(committed(SIZING.with_suffix('.final')))
    probe = N.parse_capture(cap)
    age = (time.time_ns() - probe['measured_at_unix_ns']) / 1e9
    N.check_age(probe, time.time_ns())
    checks[2] = (final['qualified'] is True and final['exit'] == 0 and b_result['verdict'] == 'PASS'
                 and b_result['replay_only'] is False and 0 <= age <= 3600, f'age={age:.0f}s final={final}')
    # 3 complete sizing set in committed bytes
    members = sorted(SIZING.parent.glob(SIZING.name + '.*'))
    names = sorted(p.name[len(SIZING.name):] for p in members)
    size = sum(len(committed(p)) for p in members)
    checks[3] = (names == ['.exit', '.final', '.final.pending', '.json', '.stderr'] and size <= 135168, f'{names} {size} B')
    # 4 evidence since B: everything new beyond B's census, less the bind set (charged by its reserved envelope)
    info = N.local_accounting(json.loads((HERE / 'intel_provisioning_manifest_v11.json').read_bytes()), HERE,
                              sizing_prefix=SIZING, extra_receipts=[str(p) for p in EXTRAS])
    b_ev = b_result['evidence']
    now_files = {**info['matched_files'], **info['omitted_files']}
    b_files = {**b_ev['matched_files'], **b_ev['omitted_files']}
    changed = {p: s for p, s in now_files.items() if Path(p).name not in {Path(q).name for q in b_files}}
    resized = {p: (b_files[q], now_files[p]) for p in now_files for q in b_files if Path(p).name == Path(q).name and b_files[q] != now_files[p]}
    bind_set = {p: s for p, s in changed.items() if Path(p).name.startswith(Path(prefix).name)}
    other = {p: s for p, s in changed.items() if p not in bind_set}
    other_bytes = sum(other.values()) + sum(max(0, b - a) for a, b in resized.values())
    old = ssh('stat -f "%z %m %N" /private/tmp/r1h-intel-provisioning-v7/receipts/* /private/tmp/r1h-intel-provisioning-v7/window.json /private/tmp/r1h-intel-window-registration-v7/window.jsonl')
    old_total = sum(int(line.split()[0]) for line in old.splitlines())
    drift = b_result['terms']['drift_receipt_bytes']
    checks[4] = (other_bytes + max(0, old_total - 7386341) <= drift and not resized and sum(bind_set.values()) <= 2500000,
                 f'new_since_B={other} resized={resized} bind_set={sum(bind_set.values())} B old_state_now={old_total} D(B)={drift}')
    # 5 updated demand
    demand = b_result['required_receipt_bytes'] - drift + max(drift, other_bytes + max(0, old_total - 7386341))
    checks[5] = (demand <= 42000000 and b_result['nonreceipt_setup_bytes'] + demand <= 2000000000,
                 f'receipts={demand} setup={b_result["nonreceipt_setup_bytes"] + demand}')
    # 6 fresh roots, core and anchor unused; bound core seals J11 and the fresh identity capture
    raw, value, bound = bind_facts(prefix)
    core = bound['window_seal']['core_sha256']
    roots = ssh('for d in /private/tmp/r1l-intel-provisioning-v11 /private/tmp/r1l-intel-window-registration-v11; do [ -e "$d" ] && echo "PRESENT $d" || echo "absent $d"; done')
    attempt = HERE / ('r1j_attempt_0_' + core[:12] + '.json')
    j11 = json.loads((HERE / 'intel_provisioning_manifest_v11.json').read_bytes())
    inputs = value['binding_receipt']['input_sha256']
    differ = sorted(k for k in set(j11) | set(bound) if j11.get(k) != bound.get(k))
    seals = (inputs['manifest'] == REVIEWED['intel_provisioning_manifest_v11.json'] and inputs['identity'] == A.PINS['r1j_identity_probe.py']
             and inputs['probe'] == sha(PROBE.read_bytes()) and sha(value['bound_manifest_json'].encode()) == value['binding_receipt']['bound_manifest_sha256']
             and differ == ['binding_provenance', 'collector', 'window_seal'])
    checks[6] = ('PRESENT' not in roots and core != CONSUMED_CORE and not attempt.exists() and seals
                 and bound['collector']['retained_dir'] == '/private/tmp/r1l-intel-provisioning-v11',
                 f'core={core[:12]} roots={roots.split()} seals={seals} differ={differ} attempt_absent={not attempt.exists()}')
    # 7 sealed envelopes and LIVE (from N terms and bound budget)
    t = b_result['terms']
    checks[7] = (t['registration_bytes'] == t['window_bytes'] == t['summary_bytes'] == 65536 and t['failure_bytes'] == 16384
                 and t['emergency_journal_bytes'] == t['accounting_bytes'] == t['attempt_bytes'] == 4096
                 and b_result['future_collector_entries'] == 64 and b_result['drift_live_bytes'] == 100000
                 and b_result['live_non_progress_bytes'] == 65536 and b_result['live_dispatch_bytes'] <= 2500000,
                 f'live={b_result["live_dispatch_bytes"]} calls={b_result["live_calls_bound"]}')
    # 8 time left in the bind's original window
    left = deadline - time.time()
    bind_final = json.loads(committed(prefix + '.final'))
    checks[8] = (bind_final['qualified'] is True and abs(bind_final['m3_deadline'] - deadline) < 1 and left >= MIN_REMAINING_AT_GO,
                 f'left={left:.0f}s deadline={bind_final["m3_deadline"]}')
    for k in sorted(checks):
        print(f'D{k} {"PASS" if checks[k][0] else "FAIL"} {checks[k][1]}')
    print('GATE D', 'GO' if all(v[0] for v in checks.values()) else 'STOP')
    return 0 if all(v[0] for v in checks.values()) else 1


def inventory(prefix):
    capture = prefix + '.json'
    digest = sha(committed(capture))
    maker = A.load_maker(sizing=False)
    boot = len(committed(capture)) + len(committed(prefix + '.stderr')) + len(committed(prefix + '.exit')) + len(committed(prefix + '.final'))
    sys.argv = ['r1l_make_bundle.py', 'inventory', '--dispatch-m3', '--capture', capture, '--expected-capture-sha256', digest,
                '--expected-anchor', 'none', '--bootstrap-bytes', str(boot), '--ssh-argv', *A.SSH_ARGV]
    print('INVENTORY', digest, boot, flush=True)
    return maker.main()


if __name__ == '__main__':
    mode, args = sys.argv[1], sys.argv[2:]
    raise SystemExit({'bind': bind, 'gate': gate, 'inventory': inventory}[mode](*args))
