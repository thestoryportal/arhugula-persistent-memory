"""Run the handoff's exact acceptance commands; retain unfiltered logs and source identity."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone

receipt = Path(__file__).resolve().parent
root = receipt.parents[1]
names = ('tools/git_hygiene.py', 'tools/git_merge_gate.py', 'tests/test_git_automation.py')
environment = dict(os.environ, LLMDB_ROOT=str(root), TMPDIR=str(receipt / 'fixtures'),
                   PATH='/opt/homebrew/bin:' + os.environ.get('PATH', ''), PYTHONDONTWRITEBYTECODE='1')

def git(*args):
    return subprocess.run(['git', *args], cwd=root, env=environment, capture_output=True,
                          text=True, check=True).stdout.strip()

def hashes():
    return {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names}

assert git('branch', '--show-current') == 'worktree-c10k-route-a'
rows = []
commands = (
    ('git_automation', ['/usr/bin/python3', '-B', '-S', '-m', 'unittest', 'discover',
                        '-s', 'tests', '-p', 'test_git_automation.py', '-v']),
    ('model_free', ['/usr/bin/python3', '-B', '-S', '-m', 'unittest', '-v',
                    'tools.test_c10w_p2_gate', 'tools.test_dashboard_live', 'tools.test_dashboard_gpu_detector']),
)
for label, command in commands:
    source = hashes()
    head = git('rev-parse', 'HEAD')
    print('START', label, flush=True)
    started = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(command, cwd=root, env=environment, capture_output=True, text=True, timeout=240)
    output = result.stdout + result.stderr
    log = receipt / ('mb10_' + label + '.log')
    log.write_text(output)
    log.with_suffix('.exit').write_text(str(result.returncode) + '\n')
    counts = re.findall(r'^Ran (\d+) tests? in ', output, re.MULTILINE)
    count = int(counts[-1]) if counts else None
    valid = result.returncode == 0 and count is not None and output.rstrip().endswith('OK') and source == hashes()
    row = {'suite': label, 'command': command, 'started_utc': started,
           'exit_code': result.returncode, 'tests_run': count, 'passed': valid,
           'head_before': head, 'head_after': git('rev-parse', 'HEAD'), 'source_sha256': source,
           'log': log.name, 'environment': {k: environment[k] for k in ('LLMDB_ROOT', 'TMPDIR', 'PATH')}}
    rows.append(row)
    (receipt / 'mb10_acceptance.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(label, 'tests=' + str(count), 'exit=' + str(result.returncode), 'verified=' + str(valid), flush=True)
    if not valid:
        print('Acceptance failed; inspect', log, flush=True)
        raise SystemExit(1)
