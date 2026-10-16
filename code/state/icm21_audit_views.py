"""C-GENERATED and C-TWINS audit area: generated views and twins are fresh.

Loaded by icm21_check.area(), which injects the checker's Unverified class.
SPEC.md:494-538. Freshness is decided by the root's own generators in their
read-only --check mode, not by a file search or a second renderer. The audit
never runs --write, so a stale view or twin is reported, never repaired.
Stale output is FAIL; a generator that cannot run or decide is UNVERIFIED.
"""
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys


PRD_IDS = {'C-GENERATED': 'ICM-R8', 'C-TWINS': 'ICM-R11'}
# Generator script, then the stdout pattern that names one stale output.
GENERATORS = {
    'C-GENERATED': (('code/state/build_index.py', re.compile(r'Drift: (\S+)')),
                    ('code/state/render_state.py', re.compile(r'\[STALE \] (\S+)'))),
    'C-TWINS': (('code/agents/twins.py',
                 re.compile(r'((?:map/)?(?:AGENTS|routing)\.md): (?:missing|differs from )')),),
}
TIMEOUT_SECONDS = 300


def run_check(root, script):
    """Run one generator's --check against root without writing bytecode."""
    environment = {key: value for key, value in os.environ.items()
                   if not key.startswith('GIT_')}
    environment.update(LLMDB_ROOT=str(root), PYTHONDONTWRITEBYTECODE='1')
    try:
        return subprocess.run([sys.executable, '-B', str(root / script), '--check'],
                              cwd=root, env=environment, capture_output=True,
                              timeout=TIMEOUT_SECONDS)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise Unverified(script + ' --check did not run: '  # noqa: F821 -- injected
                         + type(error).__name__) from error


def stale_outputs(root, script, pattern, coverage):
    """Return the stale outputs one generator names; raise Unverified when it cannot decide."""
    if not (root / script).is_file():
        raise Unverified('Absent generator: ' + script)  # noqa: F821 -- injected
    coverage['inspected'].append(str(root / script))
    result = run_check(root, script)
    stale = sorted(set(pattern.findall(result.stdout.decode('utf-8', 'replace'))))
    if result.returncode == 0 and not stale:
        return []
    if result.returncode == 1 and stale:
        return stale
    tail = (result.stdout + result.stderr).decode('utf-8', 'replace').strip()[-400:]
    raise Unverified(script + ' --check exited ' + str(result.returncode)  # noqa: F821
                     + ' without a freshness decision: ' + tail)


def check(check_id, root, mode, config, coverage):
    root = Path(root)
    findings = []
    for script, pattern in GENERATORS[check_id]:
        for relative in stale_outputs(root, script, pattern, coverage):
            path = str(root / relative)
            reason = 'Stale or missing generated output of ' + script + ': ' + relative
            identity = check_id + '\n' + path + '\n' + reason
            findings.append({'id': 'F-' + check_id[2:] + '-'
                                   + hashlib.sha256(identity.encode()).hexdigest(),
                             'status': 'FAIL', 'prd_ids': [PRD_IDS[check_id]],
                             'paths': [path], 'evidence': [], 'reason': reason,
                             'previous_finding': None, 'resolution_receipt': None})
    if findings:
        return 'FAIL', '; '.join(f['reason'] for f in findings), findings
    scripts = ', '.join(script for script, _ in GENERATORS[check_id])
    return 'PASS', 'Outputs match their generators (' + scripts + ' --check; read-only)', []
