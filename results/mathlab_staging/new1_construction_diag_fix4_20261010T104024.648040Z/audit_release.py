"""Read-only FIX4 scope/evidence audit; never consume numerical inputs or admission."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(os.environ['LLMDB_ROOT'])
RECEIPT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def nodes(text):
    tree = ast.parse(text)
    result = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef): result[node.name] = ast.get_source_segment(text, node)
        elif isinstance(node, ast.ClassDef):
            result[node.name] = ast.get_source_segment(text, node)
            for item in node.body:
                if isinstance(item, ast.FunctionDef): result[node.name+'.'+item.name] = ast.get_source_segment(text,item)
    return tree, result


def main():
    baseline = json.loads((RECEIPT/'baseline.json').read_text())
    assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()==str(ROOT)
    assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()=='worktree-c10k-route-a'
    current = {p:sha(ROOT/p) for p in baseline['before']}
    assert {p:sha(ROOT/p) for p in baseline['protected']}==baseline['protected']
    assert all(sha(ROOT/p)==h for p,h in baseline['prior_receipts'].items())
    before = (RECEIPT/'before_new1_identity_diag.py').read_text()
    after = (ROOT/'tools/new1_identity_diag.py').read_text()
    old_tree, old = nodes(before); new_tree, new = nodes(after)
    allowed = {'kill_worker','watchdog','OwnedWorker','OwnedWorker.start'}
    preserved = [name for name in old if name not in allowed]
    assert all(old[name]==new[name] for name in preserved)
    assert old['supervise']==new['supervise'], 'cleanup, deadlines, error recording and emergency exits must be identical'
    assert old['Output']==new['Output']
    old_assign = [ast.dump(n) for n in old_tree.body if isinstance(n,(ast.Assign,ast.AnnAssign))]
    new_assign = [ast.dump(n) for n in new_tree.body if isinstance(n,(ast.Assign,ast.AnnAssign))]
    assert old_assign==new_assign, 'constants/pins/arithmetic input assignments changed'
    old_construct = (RECEIPT/'before_new1_construction_diag.py').read_text()
    new_construct = (ROOT/'tools/new1_construction_diag.py').read_text()
    assert old_construct.replace(baseline['before']['tools/new1_identity_diag.py'],current['tools/new1_identity_diag.py'])==new_construct
    _, construct_nodes = nodes(old_construct)
    construction_preserved = [name for name in construct_nodes if '.' not in name]
    _, before_tests = nodes((RECEIPT/'before_test_new1_construction_diag.py').read_text())
    _, after_tests = nodes((ROOT/'tests/test_new1_construction_diag.py').read_text())
    method_changes = []
    counts = {}
    added = []
    for path, original_methods in baseline['existing_methods'].items():
        _, methods = nodes((ROOT/path).read_text())
        existing = [name for name in methods if '.' in name and name.rsplit('.',1)[1].startswith('test_')]
        assert set(original_methods)<=set(existing)
        counts[path]=len(existing)
        added.extend(path+':'+name for name in existing if name not in original_methods)
        if path.endswith('test_new1_construction_diag.py'):
            method_changes = [name for name in original_methods if before_tests[name]!=after_tests[name]]
    assert sum(counts.values())==188 and len(added)==6
    assert all('.test_fix4_c' in name for name in added)
    assert set(method_changes)=={'ConstructionDiagnosticTests.test_runtime_caps_and_pins_reuse_frozen_identity_contract',
                                'ConstructionDiagnosticTests.test_stalled_launch_returns_within_bound_and_late_handle_cleans_once'}
    stalled = after_tests['ConstructionDiagnosticTests.test_stalled_launch_returns_within_bound_and_late_handle_cleans_once']
    for exact in ("'STOPPED-LAUNCH'", "self.assertLess(time.monotonic()-start, .3)",
                  'self.assertFalse(marker.exists())', "'LAUNCH_S', .05", "'CLEANUP_S', .05"):
        assert exact in stalled
    assert "assertIn(owners[0].proof['kills']" not in stalled
    scope = ROOT/'results/mathlab_staging/new1_construction_diag_scope.md'
    original_scope = (RECEIPT/'before_new1_construction_diag_scope.md').read_bytes()
    assert scope.read_bytes().startswith(original_scope)
    assert scope.read_bytes()[len(original_scope):].startswith(b'\n\n## Scope revision')
    from tools import new1_construction_diag as D
    D.I.verify_pins(ROOT,D.SOURCE_PINS)
    D.verify_historical_source()
    assert not any(name in sys.modules for name in ('torch','numpy','transformers','safetensors'))
    assert D.SOURCE_PINS['tools/new1_identity_diag.py']==current['tools/new1_identity_diag.py']
    baseline_capture = json.loads((RECEIPT/'capture_index.json').read_text())
    assert len(baseline_capture['runs'])<=200
    assert baseline_capture['source_before']==baseline['before']['tools/new1_identity_diag.py']
    assert baseline_capture['runs'][-1]['abrupt']
    reds = json.loads((RECEIPT/'red_fix4/index.json').read_text())
    greens = json.loads((RECEIPT/'green_fix4/index.json').read_text())
    assert len(reds)==len(greens)==6
    assert {tuple(r['targets']) for r in reds}=={tuple(r['targets']) for r in greens}
    assert all(r['exit']==1 and r['tests']==1 and r['completed'] for r in reds)
    assert all(r['source_sha256']['tools/new1_identity_diag.py']==baseline['before']['tools/new1_identity_diag.py'] for r in reds)
    assert all(r['exit']==0 and r['tests']==1 and r['ok'] and not r['warnings'] for r in greens)
    repetitions = {}
    tested_scope_sha=json.loads((RECEIPT/'scope_append.json').read_text())['final_sha256']
    for label,count,methods in (('sandbox_solo_20',20,1),('sandbox_full_3',3,188)):
        records = json.loads((RECEIPT/label/'index.json').read_text())
        assert 0<len(records)<=count and [r['index'] for r in records]==list(range(1,len(records)+1))
        accepted = len(records)==count and all(r['exit']==0 and r['tests']==methods and r['ok'] and not r['warnings'] and not r['timeout'] and not r['ignored_exception'] for r in records)
        if label=='sandbox_solo_20':assert accepted
        assert all({p:h for p,h in r['source_sha256'].items() if p!=str(scope.relative_to(ROOT))}=={p:h for p,h in current.items() if p!=str(scope.relative_to(ROOT))} for r in records)
        assert all(r['source_sha256'][str(scope.relative_to(ROOT))]==tested_scope_sha for r in records)
        for record in records:
            assert sha(ROOT/record['log'])==record['log_sha256']
            log = (ROOT/record['log']).read_text()
            assert bool(re.search(r'\nOK\n?$',log))==record['ok']
            assert ('ResourceWarning:' in log)==record['warnings']
            assert ('Exception ignored in' in log)==record['ignored_exception']
        repetitions[label]={'required_runs':count,'saved_runs':len(records),'accepted':accepted,
                            'methods_per_run':methods,'exit_codes':[r['exit'] for r in records],
                            'wall_s':[r['wall_s'] for r in records]}
    red_warning_observation = {r['log']:('ResourceWarning:' in (ROOT/r['log']).read_text()) for r in reds}
    assert not any(red_warning_observation.values())
    command = D.launch_command(current['results/mathlab_staging/new1_construction_diag_scope.md'],current['tools/new1_construction_diag.py'])+'\n'
    assert (RECEIPT/'launch_command.txt').read_text()==command
    assert '10-current' in command
    accepted=all(r['accepted'] for r in repetitions.values())
    report = dict(status='PASS' if accepted else 'STATIC-PASS / ACCEPTANCE-FAIL',changed_sha256=current,protected_count=len(baseline['protected']),
                  prior_receipts_unchanged=len(baseline['prior_receipts']),identity_nodes_identical=preserved,
                  construction_functions_identical=construction_preserved,supervise_byte_identical=True,
                  scope_prefix_bytes=len(original_scope),existing_methods_retained=182,counts=counts,
                  existing_method_changes=method_changes,new_methods=added,red_count=6,green_count=6,
                  repetitions=repetitions,red_actual_resource_warnings=red_warning_observation,
                  scientific_inputs_unread=True,real_admission_unrun=True,launch_unrun=True)
    print(json.dumps(report,indent=2))
    return 0 if accepted else 1


if __name__=='__main__':sys.exit(main())
