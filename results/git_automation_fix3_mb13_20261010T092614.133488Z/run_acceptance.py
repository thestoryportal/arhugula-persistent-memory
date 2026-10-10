import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(os.environ['LLMDB_ROOT']).resolve()
RECEIPT = Path(__file__).resolve().parent
FILES = ['tools/git_merge_gate.py', 'tools/git_hygiene.py', 'tests/test_git_automation.py']


def snapshot():
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
    return {'head': head, 'files': {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in FILES}}


commands = [
    ('git_automation', ['/usr/bin/python3', '-B', '-S', '-m', 'unittest', 'discover',
                        '-s', 'tests', '-p', 'test_git_automation.py', '-v'], 104),
    ('model_free', ['/usr/bin/python3', '-B', '-S', '-m', 'unittest', '-v',
                    'tools.test_c10w_p2_gate', 'tools.test_dashboard_live', 'tools.test_dashboard_gpu_detector'], 80),
    ('diff_check', ['git', 'diff', '--check', '--', *FILES], None),
]
rows = []
environment = dict(os.environ, LLMDB_ROOT=str(ROOT), TMPDIR=str(RECEIPT / 'fixtures'),
                   PATH='/opt/homebrew/bin:' + os.environ['PATH'], PYTHONDONTWRITEBYTECODE='1')
for label, command, expected in commands:
    before = snapshot()
    result = subprocess.run(command, cwd=ROOT, env=environment, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, timeout=600)
    log = RECEIPT / (label + '.log')
    log.write_text(result.stdout)
    log.with_suffix('.exit').write_text(str(result.returncode) + '\n')
    match = re.search(r'^Ran (\d+) tests? in ', result.stdout, re.MULTILINE)
    count = int(match.group(1)) if match else None
    after = snapshot()
    valid = result.returncode == 0 and before['files'] == after['files']
    if expected is not None:
        valid = valid and count == expected and '\nOK\n' in result.stdout
    rows.append({'label': label, 'command': command, 'count': count, 'exit': result.returncode,
                 'before': before, 'after': after, 'log': log.name,
                 'resource_warnings': result.stdout.count('ResourceWarning:'), 'validated': valid})
    (RECEIPT / 'acceptance.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(label, 'count=' + str(count), 'exit=' + str(result.returncode), 'VALID' if valid else 'INVALID', flush=True)
    if not valid:
        print(result.stdout, flush=True)
        sys.exit(1)
