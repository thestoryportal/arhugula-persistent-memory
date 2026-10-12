"""Verify frozen scope, all outcomes, and only the recorded owned PIDs."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
EXCLUDED = {32906,32913,32914,36233,36258,36259,37109,65807}
start = json.loads((OUT/'start_sha256.json').read_text())
candidate = json.loads((OUT/'candidate_sha256.json').read_text())
final = {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in start}
assert final == candidate, 'source identity changed after validated runs'
assert all(final[p] == start[p] for p in start if p != 'tools/test_backup_gdrive_addendum.py')
assert not (OUT/'mutation_scratch_tools').exists(), 'mutant remains'
assert json.loads((OUT/'mutation_removed.json').read_text())['scratch_removed']
original = (OUT/'original_test.py').read_text()
current = (ROOT/'tools/test_backup_gdrive_addendum.py').read_text()
first = '    def test_held_lock_refusal_cannot_overwrite_owner_heartbeat(self):'
next_test = '    def test_one_thousand_live_owner_refusals_have_bounded_storage(self):'
assert original.split(first)[0] == current.split(first)[0]
assert original.split(next_test)[1] == current.split(next_test)[1]
assert 'time.sleep(0.1)' not in current.split(first)[1].split(next_test)[0]
assert subprocess.run(['git','rev-parse','--show-toplevel'],cwd=str(ROOT),capture_output=True,text=True,check=True).stdout.strip() == str(ROOT)
assert subprocess.run(['git','branch','--show-current'],cwd=str(ROOT),capture_output=True,text=True,check=True).stdout.strip() == 'worktree-c10k-route-a'
assert json.loads((OUT/'red_arm_iv/four_arm_counts.json').read_text()) == {'iv':{'pass':0,'fail':10}}
counts = json.loads((OUT/'green_four_arms/four_arm_counts.json').read_text())
assert counts == {arm:{'pass':10,'fail':0} for arm in ['i','ii','iii','iv']}
assert json.loads((OUT/'mutation/arm_iii/run_01/result.json').read_text()) == {'testsRun':1,'failures':1,'errors':0,'skipped':0,'success':False,'alive':[]}
full = json.loads((OUT/'full_addendum_final/arm_iii/run_01/result.json').read_text())
assert full == {'testsRun':134,'failures':0,'errors':0,'skipped':14,'success':True,'alive':[]}, full
selection = json.loads((OUT/'full_addendum_final/arm_iii/run_01/suite_selection.json').read_text())
assert selection['native_classes_excluded'] == ['LauncherTest'] and selection['real_rclone_disabled']
for phase, errors in [('full_addendum',2),('full_addendum_symlink_capture',1)]:
    result = json.loads((OUT/phase/'arm_iii/run_01/result.json').read_text())
    assert result == {'testsRun':134,'failures':0,'errors':errors,'skipped':14,'success':False,'alive':[]}
owned = set()
for path in OUT.rglob('started_processes.json'):
    for record in json.loads(path.read_text()):
        assert not record['alive'], path
        owned.add(record['pid'])
for path in OUT.rglob('descendants.json'):
    value = json.loads(path.read_text())
    assert value['positive_control'], path
    owned.add(value['runner_pid'])
    for record in value['observed']:
        assert not record['alive_after_runner_exit'], path
        owned.add(record['pid'])
for path in OUT.glob('*matrix.log'):
    match = re.search(r'^matrix controller pid=(\d+)$',path.read_text(),re.M)
    assert match, path
    owned.add(int(match.group(1)))
assert owned and not owned.intersection(EXCLUDED)
alive = []
for pid in sorted(owned):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        continue
    alive.append(pid)
(OUT/'final_process_clearance.json').write_text(json.dumps({'owned_pid_count':len(owned),'owned_pids':sorted(owned),'alive':alive,'excluded_pids_not_inspected_or_signalled':sorted(EXCLUDED),'observation':'Every run has a successful own-runner child-observation positive control. All recorded direct Popen subprocesses, fixture child PIDs, descendants, and matrix controllers checked by exact PID.'},indent=2)+'\n')
assert not alive, 'recorded owned process remains: '+repr(alive)
(OUT/'final_sha256.json').write_text(json.dumps(final,indent=2)+'\n')
for arm in counts:
    logs = []
    for number in range(1,11):
        run = OUT/'green_four_arms'/('arm_'+arm)/('run_%02d'%number)
        result = json.loads((run/'result.json').read_text())
        assert result == {'testsRun':1,'failures':0,'errors':0,'skipped':0,'success':True,'alive':[]}
        assertion = json.loads((run/'assertion.json').read_text())
        assert assertion['same_bytes'] and not assertion['changed_fields']
        logs.append('RUN %02d\n'%number+(run/'test.log').read_text())
    (OUT/'green_four_arms'/('arm_'+arm+'.log')).write_text('\n'.join(logs))
(OUT/'acceptance.json').write_text(json.dumps({'status':'DONE','four_arm_counts':counts,'full_addendum':full,'full_passed':full['testsRun']-full['skipped'],'owned_pid_count':len(owned),'alive':alive,'protected_tools_unchanged':True,'only_named_test_changed':True,'mutant_removed':True,'prior_collector_error_counts':[2,1]},indent=2)+'\n')
print(json.dumps({'four_arm_counts':counts,'full_addendum':full,'full_passed':full['testsRun']-full['skipped'],'recorded_owned_pids_checked':len(owned),'alive':alive},sort_keys=True))
