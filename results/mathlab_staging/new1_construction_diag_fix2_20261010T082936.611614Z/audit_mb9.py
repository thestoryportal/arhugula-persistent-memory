"""Task 3's static comparison, extended only for Task 4's approved ownership scope."""
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

root = Path(os.environ['LLMDB_ROOT']).resolve()
here = Path(__file__).resolve().parent
sys.path.insert(0, str(root))
from tools import new1_construction_diag as D

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path): return json.loads(Path(path).read_text())
def write(path, value):
    with Path(path).open('x') as f: json.dump(value, f, indent=2); f.write('\n')
def functions(path):
    text = Path(path).read_text()
    return {n.name: ast.get_source_segment(text, n) for n in ast.parse(text).body if isinstance(n, ast.FunctionDef)}
def constants(path):
    return {ast.unparse(n.targets[0]): ast.dump(n.value, include_attributes=False)
            for n in ast.parse(Path(path).read_text()).body if isinstance(n, ast.Assign)}
def methods(path):
    text = Path(path).read_text()
    return {n.name: ast.get_source_segment(text, n) for n in ast.walk(ast.parse(text))
            if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')}
def assertions(body):
    return [ast.get_source_segment(body, n) for n in ast.walk(ast.parse(body.lstrip()))
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr.startswith('assert')]

baseline = load(here/'baseline.json'); mb9 = load(here/'mb9_baseline.json')
green = load(here/'four_suites_second.json')
owned = {p: sha(root/p) for p in mb9['sha256']}
for p, expected in green['sha256'].items(): assert owned[p] == expected, (p, 'changed after GREEN')
for p, expected in baseline['owned_sha256'].items(): assert sha(here/'before'/p) == expected
for p, expected in mb9['existing_fix2_hashes'].items(): assert sha(here/p) == expected, (p, 'prior fix2 receipt changed')
protected = {p: sha(root/p) for p in baseline['protected_sha256'] if p != 'tests/test_new1_identity_diag.py'}
assert protected == {p: s for p, s in baseline['protected_sha256'].items() if p in protected}, 'protected drift'
prior_counts = {}
for directory, expected in baseline['prior_evidence_sha256'].items():
    current = {str(p.relative_to(root/directory)): sha(p) for p in (root/directory).rglob('*') if p.is_file()}
    assert current == expected, (directory, 'prior evidence changed')
    prior_counts[directory] = len(current)

same = {}
for p in ('tools/new1_identity_diag.py', 'tools/new1_construction_diag.py'):
    before, after = functions(here/'before'/p), functions(root/p)
    exempt = {'wait_for_release', 'supervise', 'main'} if p.endswith('identity_diag.py') else {'main'}
    for name, body in before.items():
        if name not in exempt: assert after[name] == body, (p, name, 'frozen function changed')
    same[p] = [name for name in before if name not in exempt]
    before_constants, after_constants = constants(here/'before'/p), constants(root/p)
    for name, value in before_constants.items():
        if p.endswith('construction_diag.py') and name == 'SOURCE_PINS': continue
        assert after_constants[name] == value, (p, name, 'frozen constant changed')
    # Reconstruct the old entry by undoing only explicit absolute-deadline plumbing.
    prefix = '' if p.endswith('identity_diag.py') else 'I.'
    reverted = after['main'].replace('with S.hard_deadline(start+'+prefix+'DEADLINE_S-time.monotonic()):',
                                    'with S.hard_deadline('+prefix+'DEADLINE_S):')
    reverted = reverted.replace('seconds='+prefix+'DEADLINE_S, absolute_end=start+'+prefix+'DEADLINE_S)',
                                'seconds='+prefix+'DEADLINE_S-(time.monotonic()-start))')
    assert reverted == before['main'], (p, 'entry changed beyond absolute deadline')
old_text = (here/'before/tools/new1_identity_diag.py').read_text()
new_text = (root/'tools/new1_identity_diag.py').read_text()
old_output = next(n for n in ast.parse(old_text).body if isinstance(n, ast.ClassDef) and n.name == 'Output')
new_output = next(n for n in ast.parse(new_text).body if isinstance(n, ast.ClassDef) and n.name == 'Output')
assert ast.get_source_segment(old_text, old_output) == ast.get_source_segment(new_text, new_output), 'output contract changed'
# Keep result/failure field names and cap values; process identity is the actual worker.
def report_keys(text):
    tree = ast.parse(text); function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'supervise')
    updates = [n for n in ast.walk(function) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
               and isinstance(n.func.value, ast.Name) and n.func.value.id == 'value' and n.func.attr == 'update']
    failure = next(n.value for n in ast.walk(function) if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'failure' for t in n.targets) and isinstance(n.value, ast.Dict))
    return ([k.arg for k in updates[0].keywords], [k.value for k in failure.keys])
assert report_keys(old_text) == report_keys(new_text), 'report field contract changed'
old_pins, new_pins = [], []
for p, items in ((here/'before/tools/new1_construction_diag.py', old_pins), (root/'tools/new1_construction_diag.py', new_pins)):
    node = next(n.value for n in ast.parse(p.read_text()).body if isinstance(n, ast.Assign) and ast.unparse(n.targets[0]) == 'SOURCE_PINS')
    for key, value in zip(node.keys, node.values):
        if isinstance(key, ast.Constant) and key.value == 'tools/new1_identity_diag.py': value.value = 'IDENTITY_REPIN'
    items.append(ast.dump(node, include_attributes=False))
assert old_pins == new_pins, 'other source pin changed'
assert D.SOURCE_PINS['tools/new1_identity_diag.py'] == owned['tools/new1_identity_diag.py']
D.I.verify_pins(root, D.SOURCE_PINS); D.verify_historical_source()
assert (D.I.DEADLINE_S, D.I.RSS_CAP_GIB, D.I.THREADS, D.I.DISK_BYTES, D.I.CLEANUP_S, D.I.LAUNCH_S) == (600, 11., 8, 1000000, 5, 5)
assert 'torch' not in sys.modules and 'numpy' not in sys.modules

identity_path = 'tests/test_new1_identity_diag.py'
old_tests, new_tests = methods(here/'before'/identity_path), methods(root/identity_path)
assert set(old_tests) == set(new_tests) and len(old_tests) == 27
migrated = [name for name in old_tests if old_tests[name] != new_tests[name]]
assert set(migrated) == {'test_keyboard_interrupt_after_dispatch_cannot_leave_worker_alive',
                         'test_worker_cleanup_timeout_is_attempted_once_and_preserves_original_error'}
assert sha(here/'before'/identity_path) == '22bfcca9f90054b6ad9cd71d7ca4bf5f67738f8d6ee284d91b106bc946e5c699'
test_migrations = {name: {'before': old_tests[name], 'after': new_tests[name]} for name in migrated}
old_construction_tests = methods(here/'before/tests/test_new1_construction_diag.py')
new_construction_tests = methods(root/'tests/test_new1_construction_diag.py')
assert set(old_construction_tests) <= set(new_construction_tests)
changed_construction = [name for name in old_construction_tests if old_construction_tests[name] != new_construction_tests[name]]
counts = {suite: len(methods(root/('tests/test_new1_'+suite+'.py'))) for suite in ('construction_diag', 'identity_diag', 'geometry', 'supervisor')}
assert counts == {'construction_diag': 52, 'identity_diag': 27, 'geometry': 34, 'supervisor': 61}
log = (here/'four_suites_second.log').read_text()
assert green['exit_code'] == 0 and re.search(r'Ran 174 tests in [\d.]+s\s+OK\s*$', log)
assert 'ResourceWarning' not in log
old_scope = (here/'before/results/mathlab_staging/new1_construction_diag_scope.md').read_bytes()
current_scope = (root/'results/mathlab_staging/new1_construction_diag_scope.md').read_bytes()
assert current_scope.startswith(old_scope)
assert current_scope.startswith((here/'before/results/mathlab_staging/new1_construction_diag_scope.md').read_bytes())
diff = subprocess.run(['git', 'diff', '--check', '--', *owned], cwd=root, capture_output=True, text=True, check=True)
assert not diff.stdout and not diff.stderr
branch = subprocess.run(['git', 'branch', '--show-current'], cwd=root, capture_output=True, text=True, check=True).stdout.strip()
assert branch == 'worktree-c10k-route-a'
head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True, check=True).stdout.strip()
proof = {'utc': datetime.now(timezone.utc).isoformat(), 'root': str(root), 'branch': branch, 'head': head,
         'owned_sha256': owned, 'before_sha256': mb9['sha256'], 'protected_unchanged_count': len(protected),
         'protected_sha256': protected, 'prior_evidence_unchanged_counts': prior_counts,
         'existing_fix2_files_preserved_count': len(mb9['existing_fix2_hashes']),
         'byte_identical_functions': same, 'output_class_byte_identical': True, 'output_keys_identical': True,
         'entry_changes_only_absolute_deadline': True, 'scope_prior_bytes_preserved': len(old_scope),
         'identity_fixture_methods_preserved': 27, 'identity_fixture_changed_methods': migrated,
         'identity_fixture_before_sha256': sha(here/'before'/identity_path),
         'identity_fixture_after_sha256': owned[identity_path], 'identity_fixture_method_comparison': test_migrations,
         'construction_original_methods_preserved': len(old_construction_tests),
         'construction_fixture_changed_methods': changed_construction, 'test_counts': counts,
         'test_total': sum(counts.values()), 'green': green, 'source_pins': D.SOURCE_PINS,
         'historical_source': {'commit': D.I.HARVEST_COMMIT, 'sha256': D.I.HARVEST_SHA},
         'input_pins_changed': False, 'input_pins_rehashed': False, 'real_admission_run': False,
         'real_diagnostic_run': False, 'numerical_dependencies_imported': False, 'diff_check_exit': diff.returncode}
write(here/(sys.argv[1]+'.json'), proof)
print(json.dumps({k: proof[k] for k in ('protected_unchanged_count', 'prior_evidence_unchanged_counts',
                'byte_identical_functions', 'identity_fixture_before_sha256', 'identity_fixture_after_sha256', 'test_counts')}, indent=2))
