"""Generate v11 from pinned v10; no provisioning and no existing-file overwrite."""
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SOURCE = 'intel_provisioning_manifest_v10.json'
TARGET = 'intel_provisioning_manifest_v11.json'
SOURCE_SHA256 = '748fc72aa49bcdb963d99b89bbc29859237d1bbd32b84b8e05fd38d07bd9df3f'
RECEIPT_CAP = 38_000_000
FAILURE_EXTRA = 16_384


def generated_bytes():
    raw = (HERE / SOURCE).read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('v10 source pin differs')
    m = json.loads(raw)
    for row in m['budget']['components']:
        if row['id'] == 'retained_failure_extra':
            row.update(bytes=FAILURE_EXTRA, basis='COLLECTOR-FAILURE-BOUND',
                       evidence='r1j_collector.py:701-726; intel_provisioning_manifest_v10.json:1456-1460')
        if row['id'] == 'receipts':
            row['bytes'] = RECEIPT_CAP
    m['collector']['receipt_limit_bytes'] = RECEIPT_CAP
    m['budget']['planned_peak_bytes'] = sum(x['bytes'] for x in m['budget']['components'])
    m['budget']['margin_bytes'] = m['budget']['setup_cap_bytes'] - m['budget']['planned_peak_bytes']
    if m['budget']['margin_bytes'] < 0:
        raise ValueError('v11 exceeds unchanged setup cap')
    for field in ('probe_tmp',):
        m['paths'][field] = m['paths'][field].replace('-v10', '-v11')
    for field in ('retained_dir', 'registration_path'):
        m['collector'][field] = m['collector'][field].replace('-v10', '-v11')
    m['collector']['admitted_write_roots'] = [x.replace('-v10', '-v11') for x in m['collector']['admitted_write_roots']]
    m['collector']['child_contract']['allowed_write_roots'] = [x.replace('-v10', '-v11') for x in m['collector']['child_contract']['allowed_write_roots']]
    return (json.dumps(m, indent=2, allow_nan=False) + '\n').encode()


def changed_paths(old, new, path=''):
    if isinstance(old, dict) and isinstance(new, dict) and old.keys() == new.keys():
        return {k: v for key in old for k, v in changed_paths(old[key], new[key], path + '/' + key).items()}
    if isinstance(old, list) and isinstance(new, list) and len(old) == len(new):
        return {k: v for i, (a, b) in enumerate(zip(old, new)) for k, v in changed_paths(a, b, path + '/' + str(i)).items()}
    return {} if old == new else {path: [old, new]}


def main():
    target = Path(sys.argv[1]) if len(sys.argv) == 2 else HERE / TARGET
    if len(sys.argv) > 2:
        raise ValueError('usage: r1n_make_manifest_v11.py [new-output-path]')
    raw = generated_bytes()
    if target.exists():
        if target.is_symlink() or target.read_bytes() != raw:
            raise ValueError('existing output differs; never overwrite')
    else:
        with target.open('xb') as stream:
            stream.write(raw)
    print(json.dumps(changed_paths(json.loads((HERE / SOURCE).read_bytes()), json.loads(raw)), sort_keys=True))


if __name__ == '__main__':
    main()
