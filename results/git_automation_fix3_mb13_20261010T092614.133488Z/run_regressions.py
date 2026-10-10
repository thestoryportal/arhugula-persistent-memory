"""Save one raw stdlib unittest log per regression; never invoke live APIs."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

RECEIPT = Path(__file__).resolve().parent
ROOT = Path(os.environ['LLMDB_ROOT']).resolve()


def names(path):
    return {node.name + '.' + method.name
            for node in ast.parse(path.read_text()).body if isinstance(node, ast.ClassDef)
            for method in node.body if isinstance(method, ast.FunctionDef) and method.name.startswith('test_')}


mode = sys.argv[1]
assert mode in ('RED', 'GREEN')
added = names(ROOT / 'tests/test_git_automation.py') - names(RECEIPT / 'before_snapshot/tests/test_git_automation.py')
inventory = 'Contracts.test_evidence_adapter_preserves_attempt_dates_and_complete_inventories'
historical = {inventory, 'AutomationTests.test_older_in_progress_run_in_final_read_only_refuses_merge',
              'AutomationTests.test_rest_adapters_through_gate_keep_merge_receipt_and_head_guard',
              'AutomationTests.test_rest_adapter_higher_attempt_in_final_read_refuses_through_gate'}
index = []
for test in sorted(added | {inventory}):
    source = 'r2_snapshot' if mode == 'RED' and test in historical else 'current'
    code = """
import importlib.util, pathlib, sys, unittest
root, snapshot, name = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
sys.path.insert(0, str(root / 'tests'))
sys.path.insert(0, str(root))
if snapshot != 'current':
    import tools
    for leaf in ('git_hygiene', 'git_merge_gate'):
        full = 'tools.' + leaf
        spec = importlib.util.spec_from_file_location(full, pathlib.Path(snapshot) / 'tools' / (leaf + '.py'))
        module = importlib.util.module_from_spec(spec)
        sys.modules[full] = module
        setattr(tools, leaf, module)
        spec.loader.exec_module(module)
suite = unittest.defaultTestLoader.loadTestsFromName('test_git_automation.' + name)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
"""
    snapshot = str(RECEIPT / source) if source != 'current' else source
    command = ['/usr/bin/python3', '-B', '-S', '-c', code, str(ROOT), snapshot, test]
    result = subprocess.run(command, cwd=ROOT, env=dict(os.environ, LLMDB_ROOT=str(ROOT),
                            TMPDIR=str(RECEIPT / 'fixtures'), PYTHONDONTWRITEBYTECODE='1'),
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=60)
    log = RECEIPT / mode / (test + '.log')
    log.write_text(result.stdout)
    (log.with_suffix('.exit')).write_text(str(result.returncode) + '\n')
    valid = result.returncode == (1 if mode == 'RED' else 0) and 'Ran 1 test' in result.stdout
    if mode == 'RED':
        valid = valid and 'AssertionError:' in result.stdout and 'FAILED (failures=' in result.stdout
        valid = valid and 'ERROR:' not in result.stdout and 'non-list' not in result.stdout
        if test.endswith('test_rest_adapters_through_gate_keep_merge_receipt_and_head_guard'):
            valid = valid and 'AssertionError: 0 != 1' in result.stdout
        if test.endswith('test_rest_adapter_higher_attempt_in_final_read_refuses_through_gate'):
            valid = valid and 'AssertionError: True is not false' in result.stdout
    else:
        valid = valid and '\nOK\n' in result.stdout
    index.append({'test': test, 'source': source, 'command': command, 'exit': result.returncode,
                  'log': str(log.relative_to(RECEIPT)), 'sha256': hashlib.sha256(log.read_bytes()).hexdigest(),
                  'validated': valid})
    (RECEIPT / mode / 'index.json').write_text(json.dumps(index, indent=2) + '\n')
    print(mode, test, 'exit=' + str(result.returncode), 'VALID' if valid else 'INVALID', flush=True)
    if not valid:
        print(result.stdout, flush=True)
        sys.exit(1)
print(str(len(index)) + ' ' + mode + ' logs validated')
