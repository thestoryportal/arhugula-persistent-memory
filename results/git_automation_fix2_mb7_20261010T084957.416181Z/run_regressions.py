"""Receipt-local runner: save one unfiltered RED/GREEN log per regression."""
import ast
import json
import os
from pathlib import Path
import subprocess
import sys

receipt = Path(__file__).resolve().parent
root = receipt.parents[1]
phase = sys.argv[1]
if phase not in ('RED', 'RED2', 'GREEN'):
    raise SystemExit('phase must be RED or GREEN')


def test_names(path):
    return {node.name for node in ast.walk(ast.parse(path.read_text()))
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')}


names = sorted(test_names(root / 'tests/test_git_automation.py') -
               test_names(receipt / 'before/tests/test_git_automation.py'))
if len(sys.argv) > 2:
    names = [name for name in names if name in sys.argv[2:]]
destination = receipt / phase
destination.mkdir()
environment = dict(os.environ, LLMDB_ROOT=str(root), TMPDIR=str(receipt / 'fixtures'),
                   PYTHONDONTWRITEBYTECODE='1', PATH='/opt/homebrew/bin:' + os.environ.get('PATH', ''))
results = []
for name in names:
    command = ['/usr/bin/python3', '-B', '-S', '-m', 'unittest', 'discover',
               '-s', 'tests', '-p', 'test_git_automation.py', '-v', '-k', name]
    result = subprocess.run(command, cwd=root, env=environment, capture_output=True, text=True, timeout=45)
    output = result.stdout + result.stderr
    log = destination / (name + '.log')
    log.write_text(output)
    expected = result.returncode == (1 if phase.startswith('RED') else 0) and 'Ran 1 test' in output
    results.append({'test': name, 'command': command, 'exit_code': result.returncode,
                    'expected': expected, 'log': str(log.relative_to(receipt))})
    print(phase, name, 'expected result' if expected else 'UNEXPECTED result', flush=True)
(destination / 'index.json').write_text(json.dumps(results, indent=2) + '\n')
print('{}: {} regressions, {} unexpected results'.format(phase, len(results), sum(not r['expected'] for r in results)))
raise SystemExit(0 if all(row['expected'] for row in results) else 1)
