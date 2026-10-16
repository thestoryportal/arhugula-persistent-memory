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
QUEUE = 'program/program_state.json'
# Wire type of each bound manifest input; references holds one ReferenceRow per line.
# Executor has none: icm21_check.WIRE_TYPES omits ExecutorEvidence, so validate_wire refuses it.
INPUTS = {'registries': 'Registries', 'references': 'ReferenceRow', 'repairs': 'RepairSet',
          'executor': None, 'coverage': 'CoverageArtifact'}
# A final target's line suffix: a comma list of lines or ASCII/en-dash ranges.
LINES = re.compile(r':([0-9]+(?:[-–][0-9]+)?(?:,[0-9]+(?:[-–][0-9]+)?)*)$')
# A line anchor (#L<n> or #L<a>-L<b>) names lines, not a heading.
LINE_ANCHOR = re.compile(r'L([0-9]+)(?:-L([0-9]+))?')


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
    # Only the final unittest summary counts; an earlier summary-shaped line never does.
    summary = next((line.strip() for line in reversed(lines) if line.startswith('Ran ')), '')
    passed = (tail == 'INDEX CLEAN' if kind == 'index' else
              tail == 'OK' and re.fullmatch(r'Ran [1-9][0-9]* tests? in [0-9.]+s', summary))
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


def identity(argv):
    """The one argv that runs a concrete adapter: ReaderControls aliases share one run."""
    return next((known for known, kind in ADAPTERS.items() if kind == ADAPTERS.get(argv)), argv)


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


def sibling(name):
    """A module beside this file, loaded by path like every area."""
    path = Path(__file__).parent / (name + '.py')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def target_problem(root, target, headings):
    """Why a final target, its anchor or its line suffix does not resolve beneath root."""
    path, anchor, lines = target, None, None
    match = LINES.search(target)
    if '#' in target:
        path, anchor = target.split('#', 1)
        line_anchor = LINE_ANCHOR.fullmatch(anchor)
        if line_anchor:
            anchor, lines = None, '-'.join(part for part in line_anchor.groups() if part)
    elif match:
        path, lines = target[:match.start()], match.group(1)
    base = Path(root).resolve()
    file = (base / path).resolve()
    if not file.is_relative_to(base) or not file.exists():
        return 'final target ' + path + ' is absent beneath the root'
    if anchor is None and lines is None:
        return None
    if not file.is_file():
        return 'final target ' + path + ' is not a file'
    text = file.read_bytes().decode('utf-8', 'replace').splitlines()
    if anchor is not None:
        if anchor not in {slug for _, slug in headings(text)}:
            return 'anchor #' + anchor + ' is no heading of ' + path
        return None
    for part in lines.split(','):
        first, _, last = part.replace('–', '-').partition('-')
        if not 1 <= int(first) <= int(last or first) <= len(text):
            return 'line ' + part + ' is outside ' + path + ' (' + str(len(text)) + ' lines)'
    return None


def queue_status(root, records):
    """Every queue item's artifact locator resolves to its stated kind (SPEC.md:608). Read only."""
    try:
        state = json.loads((Path(root) / QUEUE).read_bytes())
    except OSError as error:
        return 'UNVERIFIED', QUEUE + ' unreadable: ' + str(error)
    try:
        for item in state['work_queue']['items']:
            records.artifact_cells(item, root)
    except (ValueError, KeyError, TypeError) as error:
        return 'FAIL', QUEUE + ': ' + str(error)
    return 'PASS', ''


def repair_status(root, entry, row, repairs, admitted):
    """A current reader passes only with an exact owned repair of an executor-admitted plan."""
    named = [repair for repair in repairs if row['id'] in repair['reference_ids']
             and entry['id'] in repair['reader_ids']]
    source = str(Path(root) / row['repair_path'])
    other = [repair['id'] for repair in named if repair['source'] != source]
    if other:
        return 'FAIL', row['id'] + ': repair ' + ', '.join(other) + ' edits a source other than ' + source
    if not any((repair['plan_id'], repair['plan_sha256']) in admitted for repair in named):
        return 'UNVERIFIED', row['id'] + ': no admitted repair bound to ' + entry['id']
    return 'PASS', ''


def row_status(root, entry, row, context):
    try:
        for consumer in dict.fromkeys((row['consumer'], row['consumer_final'])):
            final = context['resolve'](consumer, row['reference'])
            if final != row['final_target']:
                return 'FAIL', row['id'] + ': resolves away from its final target'
            problem = target_problem(root, final, context['headings'])
            if problem:
                return 'FAIL', row['id'] + ': ' + problem
    except ValueError as error:
        return 'FAIL', row['id'] + ': ' + str(error)
    if row['owner'] != entry['owner']:
        return 'FAIL', row['id'] + ': owner ' + row['owner'] + ' differs from ' + entry['owner']
    if row['role'] != 'current-reader':
        if row['id'] in context['bound']:
            return 'FAIL', row['id'] + ': repair rewrites frozen ' + row['role']
        return 'PASS', ''
    return repair_status(root, entry, row, context['repairs'], context['admitted'])


def unverified_reader(registry_id):
    """A required registry ID with no reader entry has a missing result: UNVERIFIED."""
    return {'registry_id': registry_id, 'checks': [{
        'id': 'C-REFERENCES', 'status': 'UNVERIFIED', 'prd_ids': PRD_IDS['C-REFERENCES'],
        'argv': [], 'exit_code': None, 'stdout_sha256': None, 'stderr_sha256': None,
        'findings': [], 'reason': 'Required registry ID has no reader registry entry'}]}


def reader_check(root, entry, check_id, rows, runs, producers, context):
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
        argv = identity(tuple(argv))
        status, reason, run = runs[argv]
        statuses.append(status)
        reasons.append(reason)
    if check_id == 'C-QUEUE':
        status, reason = queue_status(root, context['records'])
        statuses.append(status)
        reasons.extend([reason] if reason else [])
    for row in rows:
        status, reason = row_status(root, entry, row, context)
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


def bound_inputs(root, manifest):
    """Each bound input, digest-checked and validated against its wire type."""
    checker = sibling('icm21_check')
    schema = checker.audit_schema()
    values = {}
    for key, name in INPUTS.items():
        path, data = read_bound(root, manifest[key])
        if key == 'references':
            values['references_binding'] = {'path': str(path), 'sha256': sha(data)}
            values[key] = [json.loads(line) for line in data.decode('utf-8').splitlines()
                           if line.strip()]
            for row in values[key]:
                checker.validate_wire(name, row, schema, {})
        else:
            values[key] = json.loads(data)
            if name is not None:
                checker.validate_wire(name, values[key], schema, {})
    return values


def dispatch(root, manifest):
    """(ReferenceResults, complete captured adapter output bytes keyed by sha256). Writes nothing."""
    root = Path(root)
    values = bound_inputs(root, manifest)
    registries, rows = values['registries'], values['references']
    repairs = values['repairs']['repairs']
    coverage = values['coverage']['coverage']
    readers = sorted(registries['reader_registry'], key=lambda entry: entry['id'])
    reader_ids = {entry['id'] for entry in readers}
    every = [entry['id'] for entry in readers + registries['loader_registry']]
    if len(every) != len(set(every)):
        raise ValueError('duplicate registry ID')
    if len({row['id'] for row in rows}) != len(rows):
        raise ValueError('duplicate reference ID')
    missing = set(coverage['required_registry_ids']) - reader_ids
    owned = owned_rows(readers, rows)
    context = {'bound': repair_readers(repairs, rows, reader_ids), 'repairs': repairs,
               'admitted': {(operation['operation_id'], operation['plan']['sha256'])
                            for operation in values['executor']['operations']},
               'records': sibling('llmdb_records'), 'resolve': None, 'headings': None}
    if rows:
        resolver = sibling('resolve_path')
        binding = {'references': values['references_binding']}
        context['resolve'] = lambda consumer, spelling: resolver.resolve_reference(
            consumer, spelling, binding)
        context['headings'] = resolver.heading_entries
    # Refuse every producer conflict before any adapter runs.
    producers = {}
    for entry in readers:
        if len(set(entry['check_ids'])) != len(entry['check_ids']):
            raise ValueError(entry['id'] + ': duplicate check ID')
        argv = entry['adapter_argv']
        if entry['status'] != 'SPECIFIED' or argv is None:
            continue
        for check_id in entry['check_ids']:
            if producers.setdefault(check_id, tuple(argv)) != tuple(argv):
                raise ValueError(check_id + ': two adapters produce one check')
    runs = {}
    for argv in map(identity, producers.values()):
        if argv not in runs:
            runs[argv] = (run_adapter(root, argv) if argv in ADAPTERS else
                          ('UNVERIFIED', 'Not a concrete adapter; it does not run', None))
    outputs = {sha(data): data for _, _, run in runs.values() if run
               for data in (run.stdout, run.stderr)}
    results = [{'registry_id': entry['id'],
                'checks': [reader_check(root, entry, check_id,
                                        owned.get((entry['id'], check_id), []),
                                        runs, producers, context)
                           for check_id in entry['check_ids']]}
               for entry in readers]
    results += [unverified_reader(registry_id) for registry_id in missing]
    return ({'schema_version': 1,
             'readers': sorted(results, key=lambda reader: reader['registry_id'])}, outputs)


def check_references(root, manifest):
    return dispatch(root, manifest)[0]
