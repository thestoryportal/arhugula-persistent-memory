"""C-GENERATED and C-TWINS audit area: generated views and twins are fresh.

Loaded by icm21_check.area(), which injects the checker's Unverified class.
SPEC.md:494-538. Freshness is decided by the generators in their read-only
--check mode, not by a file search or a second renderer. The generators run
are the ones in this checkout, beside this file, pointed at the audited root
through LLMDB_ROOT: the audited tree supplies data, never executable code.
The audit never runs --write, so a stale view or twin is reported, never
repaired. Stale output is FAIL, even when another generator cannot decide; a
generator that cannot run or decide is UNVERIFIED only when nothing is stale.
"""
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys


PRD_IDS = {'C-GENERATED': 'ICM-R8', 'C-TWINS': 'ICM-R11'}
CODE = Path(__file__).resolve().parents[1]
LABVIZ_APP = 'code/apps/labviz'
# Generator script; the stdout pattern that names one stale output; the root paths
# its --check compares (catalogs and sources, then generated views or twins).
GENERATORS = {
    'C-GENERATED': (('code/state/build_index.py', re.compile(r'Drift: (\S+)'),
                     ('_index/path-map.tsv', '_index/anchor-map.tsv',
                      'program/program_state.json', '_index/experiments.md',
                      '_index/projects.md', '_index/evidence.md', '_index/checkpoints.md')),
                    ('code/state/render_state.py', re.compile(r'\[STALE \] (\S+)'),
                     ('program/program_state.json', 'program/STATUS.md',
                      '_index/program-state.md', 'program/scorecard.md'))),
    'C-TWINS': (('code/agents/twins.py',
                 re.compile(r'((?:map/)?(?:AGENTS|routing)\.md): (?:missing|differs from )'),
                 ('CLAUDE.md', 'AGENTS.md', 'routing.md',
                  'map/CLAUDE.md', 'map/AGENTS.md', 'map/routing.md')),),
}
# build_index.py also compares the LabViz map, from the relocations, in a root that holds LabViz.
LABVIZ_PATHS = ('_index/icm21-path-map.tsv', LABVIZ_APP + '/results_moves.json')
TIMEOUT_SECONDS = 300


def generator(script):
    """This checkout's copy of a generator; script is its root-relative name."""
    return CODE / Path(script).relative_to('code')


def run_check(root, script):
    """Run this checkout's generator --check against root; -E keeps PYTHONPATH from
    importing audited-tree code, -B keeps bytecode out of both trees."""
    environment = {key: value for key, value in os.environ.items()
                   if not key.startswith('GIT_')}
    environment.update(LLMDB_ROOT=str(root))
    try:
        return subprocess.run([sys.executable, '-EB', str(generator(script)), '--check'],
                              cwd=root, env=environment, capture_output=True,
                              timeout=TIMEOUT_SECONDS)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise Unverified(script + ' --check did not run: '  # noqa: F821 -- injected
                         + type(error).__name__) from error


def compared(root, script, paths):
    """The root paths one generator's --check compares."""
    if script == 'code/state/build_index.py' and (root / LABVIZ_APP).is_dir():
        paths = paths + LABVIZ_PATHS
    return [str(root / path) for path in paths]


def stale_outputs(root, script, pattern, coverage):
    """Return the stale outputs one generator names; raise Unverified when it cannot decide."""
    if not generator(script).is_file():
        raise Unverified('Absent generator: ' + script)  # noqa: F821 -- injected
    result = run_check(root, script)
    stale = sorted(set(pattern.findall(result.stdout.decode('utf-8', 'replace'))))
    coverage['inspected'].extend(str(root / relative) for relative in stale)
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
    undecided = []
    for script, pattern, paths in GENERATORS[check_id]:
        coverage['inspected'].extend(compared(root, script, paths))
        try:
            stale = stale_outputs(root, script, pattern, coverage)
        except Unverified as error:  # noqa: F821 -- injected
            undecided.append(str(error))
            continue
        for relative in stale:
            path = str(root / relative)
            reason = 'Stale or missing generated output of ' + script + ': ' + relative
            identity = check_id + '\n' + path + '\n' + reason
            findings.append({'id': 'F-' + check_id[2:] + '-'
                                   + hashlib.sha256(identity.encode()).hexdigest(),
                             'status': 'FAIL', 'prd_ids': [PRD_IDS[check_id]],
                             'paths': [path], 'evidence': [], 'reason': reason,
                             'previous_finding': None, 'resolution_receipt': None})
    if findings:
        return 'FAIL', '; '.join([f['reason'] for f in findings] + undecided), findings
    if undecided:
        raise Unverified('; '.join(undecided))  # noqa: F821 -- injected
    scripts = ', '.join(script for script, _, _ in GENERATORS[check_id])
    return 'PASS', 'Outputs match their generators (' + scripts + ' --check; read-only)', []
