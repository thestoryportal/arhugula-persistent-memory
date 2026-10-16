"""C-REFERENCES dispatcher area of icm21_check.py (WIRE-CONTRACTS.md:61-79,178-220).

One call dispatches each reader once. Each concrete adapter runs at most once.
A null-adapter reader checks its owned ReferenceRows through the pure resolver
and consumes a concrete adapter's result for the same check ID.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess


PYTHON = '.venv/bin/python'
# The only two concrete adapters (plan Step 16 out); any other argv never runs.
ADAPTERS = {
    (PYTHON, '-B', 'code/state/build_index.py', '--check'): 'index',
    (PYTHON, '-B', '-m', 'unittest', 'code.tests.test_icm21.ReaderControls'): 'unittest',
    (PYTHON, '-B', '-m', 'unittest', 'test_icm21.ReaderControls'): 'unittest',
}
# PRD trace of each reader check from SPEC.md:608-623.
PRD_IDS = {'C-QUEUE': ['ICM-R1'], 'C-REFERENCES': ['ICM-R6', 'ICM-R13'],
           'C-LABVIZ': ['ICM-R6'], 'C-GENERATED': ['ICM-R8']}
TIMEOUT = 600


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_bound(root, binding):
    path = root / binding['path']
    data = path.read_bytes()
    if sha(data) != binding['sha256']:
        raise ValueError(binding['path'] + ': sha256 differs from the reference manifest')
    return path, data


def run_adapter(root, argv):
    """(status, reason, completed process or None) of one concrete adapter."""
    if not (root / PYTHON).is_file():
        return 'UNVERIFIED', 'Adapter interpreter absent: ' + PYTHON, None
    environment = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    environment.update(LLMDB_ROOT=str(root), PYTHONPATH='code:code/tests',
                       PYTHONDONTWRITEBYTECODE='1')
    try:
        run = subprocess.run(list(argv), cwd=root, env=environment, capture_output=True,
                             timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return 'FAIL', 'Adapter timed out after ' + str(TIMEOUT) + ' s', None
    kind = ADAPTERS[argv]
    text = (run.stdout if kind == 'index' else run.stderr).decode('utf-8', 'replace')
    lines = text.strip().splitlines()
    tail = lines[-1].strip() if lines else 'no output'
    if run.returncode != 0:
        return 'FAIL', 'Adapter exit ' + str(run.returncode) + ': ' + tail, run
    # Exit 0 alone does not decide: require the clean marker; skipped tests are unproven.
    passed = (tail == 'INDEX CLEAN' if kind == 'index' else
              tail == 'OK' and re.search(r'^Ran [1-9][0-9]* tests? in ', text, re.M))
    return ('PASS' if passed else 'UNVERIFIED'), tail, run


def owned_rows(readers, rows):
    """Exactly one reader check owns each row: its consumer path and its check ID."""
    by_path = {}
    for entry in readers:
        if entry['path'] in by_path:
            raise ValueError('duplicate reader path: ' + entry['path'])
        by_path[entry['path']] = entry
    owned = {}
    for row in rows:
        owners = {by_path[path]['id'] for path in (row['consumer'], row['consumer_final'])
                  if path in by_path and row['check_id'] in by_path[path]['check_ids']}
        if len(owners) != 1:
            raise ValueError(row['id'] + ': no single owning reader for ' + row['check_id'])
        owned.setdefault((owners.pop(), row['check_id']), []).append(row)
    return owned


def repair_readers(repairs, rows, reader_ids):
    """Reference ID -> reader IDs that an admitted repair binds to it."""
    known = {row['id'] for row in rows}
    bound = {}
    for repair in repairs:
        if not repair['reader_ids'] or not repair['reference_ids']:
            raise ValueError(repair['id'] + ': unbound repair')
        if not (set(repair['reference_ids']) <= known and set(repair['reader_ids']) <= reader_ids):
            raise ValueError(repair['id'] + ': repair binds an unknown reference or reader')
        for reference_id in repair['reference_ids']:
            bound.setdefault(reference_id, set()).update(repair['reader_ids'])
    return bound


def load_resolver():
    """The pure resolver beside this file, loaded by path like every area."""
    path = Path(__file__).parent / 'resolve_path.py'
    spec = importlib.util.spec_from_file_location('resolve_path', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.resolve_reference


def row_status(entry, row, resolve, bound):
    try:
        for consumer in dict.fromkeys((row['consumer'], row['consumer_final'])):
            if resolve(consumer, row['reference']) != row['final_target']:
                return 'FAIL', row['id'] + ': resolves away from its final target'
    except ValueError as error:
        return 'FAIL', row['id'] + ': ' + str(error)
    if row['owner'] != entry['owner']:
        return 'FAIL', row['id'] + ': owner ' + row['owner'] + ' differs from ' + entry['owner']
    if row['role'] != 'current-reader':
        if row['id'] in bound:
            return 'FAIL', row['id'] + ': repair rewrites frozen ' + row['role']
        return 'PASS', ''
    if entry['id'] not in bound.get(row['id'], ()):
        return 'UNVERIFIED', row['id'] + ': no admitted repair bound to ' + entry['id']
    return 'PASS', ''


def reader_check(entry, check_id, rows, runs, producers, resolve, bound):
    if check_id not in PRD_IDS:
        raise ValueError(entry['id'] + ': no reader check ' + check_id)
    statuses, reasons, argv, run = [], [], None, None
    if entry['status'] == 'UNVERIFIED':
        statuses.append('UNVERIFIED')
        reasons.append('Registry hold ' + str(entry['hold_id']))
    else:
        argv = entry['adapter_argv']
        argv = producers.get(check_id) if argv is None else argv
    if argv is not None:
        status, reason, run = runs[tuple(argv)]
        statuses.append(status)
        reasons.append(reason)
    for row in rows:
        status, reason = row_status(entry, row, resolve, bound)
        statuses.append(status)
        reasons.extend([reason] if reason else [])
    if not statuses:
        statuses, reasons = ['UNVERIFIED'], ['No adapter result or owned reference rows']
    status = ('FAIL' if 'FAIL' in statuses else
              'UNVERIFIED' if 'UNVERIFIED' in statuses else 'PASS')
    return {'id': check_id, 'status': status, 'prd_ids': PRD_IDS[check_id],
            'argv': list(argv or []), 'exit_code': run.returncode if run else None,
            'stdout_sha256': sha(run.stdout) if run else None,
            'stderr_sha256': sha(run.stderr) if run else None, 'findings': [],
            'reason': '; '.join(reasons) or str(len(rows)) + ' owned rows resolve'}


def check_references(root, manifest):
    root = Path(root)
    registries = json.loads(read_bound(root, manifest['registries'])[1])
    references, raw = read_bound(root, manifest['references'])
    rows = [json.loads(line) for line in raw.decode('utf-8').splitlines() if line.strip()]
    repairs = json.loads(read_bound(root, manifest['repairs'])[1])['repairs']
    coverage = json.loads(read_bound(root, manifest['coverage'])[1])['coverage']
    read_bound(root, manifest['executor'])
    readers = sorted(registries['reader_registry'], key=lambda entry: entry['id'])
    reader_ids = {entry['id'] for entry in readers}
    every = [entry['id'] for entry in readers + registries['loader_registry']]
    if len(every) != len(set(every)):
        raise ValueError('duplicate registry ID')
    if len({row['id'] for row in rows}) != len(rows):
        raise ValueError('duplicate reference ID')
    unknown = set(coverage['required_registry_ids']) - reader_ids
    if unknown:
        raise ValueError('unknown required reader ID: ' + ', '.join(sorted(unknown)))
    owned = owned_rows(readers, rows)
    bound = repair_readers(repairs, rows, reader_ids)
    resolve = None
    if rows:
        resolver = load_resolver()
        binding = {'references': {'path': str(references), 'sha256': sha(raw)}}
        resolve = lambda consumer, spelling: resolver(consumer, spelling, binding)
    runs, producers = {}, {}
    for entry in readers:
        if len(set(entry['check_ids'])) != len(entry['check_ids']):
            raise ValueError(entry['id'] + ': duplicate check ID')
        argv = entry['adapter_argv']
        if entry['status'] != 'SPECIFIED' or argv is None:
            continue
        argv = tuple(argv)
        if argv not in runs:
            runs[argv] = (run_adapter(root, argv) if argv in ADAPTERS else
                          ('UNVERIFIED', 'Not a concrete adapter; it does not run', None))
        for check_id in entry['check_ids']:
            if producers.setdefault(check_id, argv) != argv:
                raise ValueError(check_id + ': two adapters produce one check')
    return {'schema_version': 1, 'readers': [
        {'registry_id': entry['id'],
         'checks': [reader_check(entry, check_id, owned.get((entry['id'], check_id), []),
                                 runs, producers, resolve, bound)
                    for check_id in entry['check_ids']]}
        for entry in readers]}
