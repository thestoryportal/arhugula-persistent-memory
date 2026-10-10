"""Static/source-only closeout; never inspect INPUT_PINS or run admission."""
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(os.environ['LLMDB_ROOT']).resolve()
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from tools import new1_construction_diag as D


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def functions(path):
    source = Path(path).read_text()
    return {node.name: ast.get_source_segment(source, node) for node in ast.parse(source).body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}


def constants(path):
    return {ast.unparse(node.targets[0]): ast.dump(node.value, include_attributes=False)
            for node in ast.parse(Path(path).read_text()).body if isinstance(node, ast.Assign)}


baseline = json.loads((HERE / 'baseline.json').read_text())
green = json.loads((HERE / 'green_third.json').read_text())
owned = {name: sha(ROOT / name) for name in baseline['owned_sha256']}
for name, expected in green['sha256'].items():
    assert owned[name] == expected, (name, 'changed since 165-test GREEN')
for name, expected in baseline['owned_sha256'].items():
    assert sha(HERE / 'before' / name) == expected, (name, 'baseline copy mismatch')
protected = {name: sha(ROOT / name) for name in baseline['protected_sha256']}
assert protected == baseline['protected_sha256'], 'protected-file drift'
prior = ROOT / baseline['prior_evidence_directory']
prior_hashes = {str(path.relative_to(prior)): sha(path) for path in prior.rglob('*') if path.is_file()}
assert prior_hashes == baseline['prior_evidence_sha256'], 'prior evidence modified/added/removed'

same_functions = {}
for name in ('tools/new1_identity_diag.py', 'tools/new1_construction_diag.py'):
    before, after = functions(HERE / 'before' / name), functions(ROOT / name)
    exempt = {'supervise', 'main'} if name.endswith('identity_diag.py') else {'main'}
    for function, body in before.items():
        if function not in exempt: assert after[function] == body, (name, function)
    same_functions[name] = [function for function in before if function not in exempt]
    release_line = '            wait_for_release()\n' if name.endswith('identity_diag.py') else '            I.wait_for_release()\n'
    assert after['main'].replace(release_line, '') == before['main'], (name, 'other main changes')
    assert set(after) - set(before) == ({'wait_for_release'} if name.endswith('identity_diag.py') else set())
    before_constants, after_constants = constants(HERE / 'before' / name), constants(ROOT / name)
    for constant, value in before_constants.items():
        if name.endswith('construction_diag.py') and constant == 'SOURCE_PINS': continue
        assert after_constants[constant] == value, (name, constant)
    assert set(after_constants) - set(before_constants) == ({'LAUNCH_S'} if name.endswith('identity_diag.py') else set())
old_construction = ast.parse((HERE / 'before/tools/new1_construction_diag.py').read_text())
new_construction = ast.parse((ROOT / 'tools/new1_construction_diag.py').read_text())
old_pins = next(node.value for node in old_construction.body if isinstance(node, ast.Assign) and ast.unparse(node.targets[0]) == 'SOURCE_PINS')
new_pins = next(node.value for node in new_construction.body if isinstance(node, ast.Assign) and ast.unparse(node.targets[0]) == 'SOURCE_PINS')
for key, value in zip(new_pins.keys, new_pins.values):
    if isinstance(key, ast.Constant) and key.value == 'tools/new1_identity_diag.py':
        value.value = baseline['owned_sha256']['tools/new1_identity_diag.py']
assert ast.dump(old_pins, include_attributes=False) == ast.dump(new_pins, include_attributes=False)
assert (D.I.DEADLINE_S, D.I.RSS_CAP_GIB, D.I.THREADS, D.I.DISK_BYTES, D.I.CLEANUP_S, D.I.LAUNCH_S) == (600, 11., 8, 1000000, 5, 5)
assert D.SOURCE_PINS['tools/new1_identity_diag.py'] == owned['tools/new1_identity_diag.py']
D.I.verify_pins(ROOT, D.SOURCE_PINS)
D.verify_historical_source()
assert 'torch' not in sys.modules and 'numpy' not in sys.modules, 'audit imported numerical dependencies'

scope_name = 'results/mathlab_staging/new1_construction_diag_scope.md'
old_scope = (HERE / 'before' / scope_name).read_bytes()
new_scope = (ROOT / scope_name).read_bytes()
assert new_scope.startswith(old_scope), 'scope was edited instead of appended'
counts = {}
for suite in ('construction_diag', 'identity_diag', 'geometry', 'supervisor'):
    path = ROOT / ('tests/test_new1_' + suite + '.py')
    tree = ast.parse(path.read_text())
    counts[suite] = sum(isinstance(node, ast.FunctionDef) and node.name.startswith('test_') for node in ast.walk(tree))
assert counts == {'construction_diag': 43, 'identity_diag': 27, 'geometry': 34, 'supervisor': 61}
log = (HERE / 'green_third.log').read_text()
assert re.search(r'Ran 165 tests in 9\.225s\s+OK\s*$', log), 'GREEN receipt mismatch'
assert green['exit_code'] == 0
diff = subprocess.run(['git', 'diff', '--check', '--', *owned], cwd=ROOT, text=True, capture_output=True)
assert diff.returncode == 0 and not diff.stdout and not diff.stderr, diff
status = subprocess.run(['git', 'status', '--porcelain=v1'], cwd=ROOT, text=True, capture_output=True, check=True)
(HERE / 'final_status.txt').write_text(status.stdout)
head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
branch = subprocess.run(['git', 'branch', '--show-current'], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
assert branch == baseline['branch']
launch = D.launch_command(owned[scope_name], owned['tools/new1_construction_diag.py'])
(HERE / 'launch_command.txt').write_text(launch + '\n')
proof = {'utc': datetime.now(timezone.utc).isoformat(), 'root': str(ROOT), 'branch': branch, 'head': head,
         'baseline_head': baseline['head'], 'owned_sha256': owned,
         'protected_sha256': protected, 'protected_unchanged_count': len(protected),
         'prior_evidence_directory': baseline['prior_evidence_directory'],
         'prior_evidence_sha256': prior_hashes, 'prior_evidence_unchanged_count': len(prior_hashes),
         'byte_identical_functions': same_functions, 'scope_prior_bytes_preserved': len(old_scope),
         'source_pins_verified_count': len(D.SOURCE_PINS), 'source_pins': D.SOURCE_PINS,
         'historical_source_verified': {'commit': D.I.HARVEST_COMMIT, 'sha256': D.I.HARVEST_SHA},
         'input_pins_rehashed': False, 'real_admission_run': False, 'numerical_dependencies_imported': False,
         'test_counts': counts, 'test_total': sum(counts.values()), 'green': green,
         'unchanged_caps': {'seconds': 600, 'rss_below_gib': 11., 'threads': 8, 'nice': 10, 'output_bytes_below': 1000000},
         'independent_launch_bound_s': 5, 'cleanup_bound_s': 5, 'terminal_recording_bound_s': 5,
         'launch_command': launch, 'launch_executed': False, 'diff_check_exit': diff.returncode}
(HERE / 'audit.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps({'source_audit': 'PASS', 'protected_unchanged': len(protected),
                  'prior_evidence_unchanged': len(prior_hashes), 'test_counts': counts,
                  'owned_sha256': owned, 'scope_prior_bytes_preserved': len(old_scope)}, indent=2))
