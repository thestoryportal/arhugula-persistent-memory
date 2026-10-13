"""One refusal-writer mutation in owned scratch tools; always remove scratch."""
import difflib
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
SCRATCH = OUT/'mutation_scratch_tools'
SCRATCH.mkdir()
pins = json.loads((OUT/'candidate_sha256.json').read_text())
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest() == h for p,h in pins.items())
shell = (ROOT/'tools/backup_gdrive.sh').read_text()
line = '  [ "$LOCK_OWNED" = 1 ] || target="$(/usr/bin/dirname "$HEARTBEAT")/refusals/latest-refusal.json"\n'
assert shell.count(line) == 1
mutant = shell.replace(line, '')
(OUT/'mutation.patch').write_text(''.join(difflib.unified_diff(shell.splitlines(True), mutant.splitlines(True), fromfile='original/tools/backup_gdrive.sh', tofile='scratch/tools/backup_gdrive.sh')))
(SCRATCH/'backup_gdrive.sh').write_text(mutant)
(SCRATCH/'backup_gdrive_status.py').write_bytes((ROOT/'tools/backup_gdrive_status.py').read_bytes())
command = [sys.executable, '-B', str(OUT/'run_matrix.py'), 'mutation', 'iii']
env = dict(os.environ, LLMDB_ROOT=str(ROOT), PYTHONDONTWRITEBYTECODE='1', MB30_PIN_FILE='candidate_sha256.json', MB30_ITERATIONS='1', MB30_MUTANT_BACKUP=str(SCRATCH/'backup_gdrive.sh'))
try:
    with (OUT/'mutation_matrix.log').open('w') as log:
        proc = subprocess.Popen(command, cwd=str(ROOT), env=env, stdout=log, stderr=subprocess.STDOUT)
        rc = proc.wait()
    assert rc == 0, 'mutation runner error; inspect mutation_matrix.log'
    result = json.loads((OUT/'mutation/arm_iii/run_01/result.json').read_text())
    assertion = json.loads((OUT/'mutation/arm_iii/run_01/assertion.json').read_text())
    test_log = (OUT/'mutation/arm_iii/run_01/test.log').read_text()
    assert result['testsRun'] == 1 and result['failures'] == 1 and result['errors'] == 0
    assert not result['success'] and not result['alive'] and not assertion['same_bytes']
    assert 'AssertionError:' in test_log and 'a non-owner cannot publish over the active owner' in test_log
    (OUT/'mutation_result.json').write_text(json.dumps({'controller_pid':proc.pid,'result':result,'assertion':assertion,'expected_assertion':'a non-owner cannot publish over the active owner'},indent=2)+'\n')
    print('MUTATION CAUGHT: fixed test fails at full heartbeat byte equality', flush=True)
finally:
    for path in SCRATCH.iterdir():
        assert path.name in {'backup_gdrive.sh','backup_gdrive_status.py'}
        path.unlink()
    SCRATCH.rmdir()
    unchanged = {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() == h for p,h in pins.items()}
    (OUT/'mutation_removed.json').write_text(json.dumps({'scratch_removed':not SCRATCH.exists(),'candidate_pins_unchanged':unchanged},indent=2)+'\n')
    assert all(unchanged.values())
