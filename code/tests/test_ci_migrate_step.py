"""CI runs every code/ops/migrate suite on macOS (PLAN.md Step 213).

The fdsafe tools need fcntl.F_GETPATH, which only macOS has, so the step lives in its own workflow,
migrate-macos.yml, which runs only when code/ops/migrate or that file changes; ci.yml stays untouched
(CONTRACT-GAPS-2026-10-18.md gap 2, MAESTRO ruling 2026-10-18). This file sits in code/tests, outside
the folder the step discovers, so the step never runs it.
"""
import copy
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(os.environ['LLMDB_ROOT'])
WORKFLOW = ROOT / '.github/workflows/migrate-macos.yml'
CI = '.github/workflows/ci.yml'
MIGRATE = ROOT / 'code/ops/migrate'
DISCOVER = "-m unittest discover -s code/ops/migrate -p 'test_*.py'"
PIP = 'python3 -m pip install duckdb==1.5.6 markdown-it-py==3.0.0'  # duckdb: Step 270's pin; markdown-it-py: ci.yml's pin (state/resolve_path.py imports it)
PATHS = ['code/ops/migrate/**', '.github/workflows/migrate-macos.yml']
NAMED_SUITES = {
    201: 'test_unit_manifest.py', 205: 'test_dup_find.py', 206: 'test_registry_match.py',
    207: 'test_reader_find.py', 208: 'test_admitted_list.py', 209: 'test_move_unit_plan.py',
    210: 'test_move_unit_run.py', 211: 'test_path_map_rows.py', 212: 'test_record_split.py',
    216: 'test_dup_find_core.py', 217: 'test_move_plan_core.py', 218: 'test_move_run_core.py',
    271: 'test_ledger_db.py', 272: 'test_ledger_db_core.py',
}
# Counts tests the way discover loads them: each file is a top-level module of the start folder.
COUNTER = (
    'import importlib, json, sys, unittest\n'
    'sys.path.insert(0, sys.argv[1])\n'
    'loader = unittest.TestLoader()\n'
    'print(json.dumps({n: loader.loadTestsFromModule(importlib.import_module(n[:-3])).countTestCases()'
    ' for n in sys.argv[2:]}))\n'
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def triggers(workflow):
    # PyYAML reads the bare key `on` as the YAML 1.1 boolean True.
    return workflow[True]


def migrate_step(workflow, ci):
    """Return (job, discover line) of the one step that runs the migrate suites, or fail the test.

    ci is the parsed ci.yml: the migrate workflow copies its branch filters and its cpu job's
    checkout and setup-python steps.
    """
    require(workflow['name'] == 'migrate-macos', f"workflow name is {workflow['name']!r}")
    require(sorted(triggers(workflow)) == ['pull_request', 'push'], f'events are {sorted(triggers(workflow))!r}')
    for event, on in triggers(workflow).items():
        require(on.get('paths') == PATHS, f"{event} paths are {on.get('paths')!r}")
        require(on.get('branches') == triggers(ci)[event]['branches'], f'{event} branches differ from ci.yml')
    found = [(job, step) for job in workflow['jobs'].values() for step in job['steps']
             if 'code/ops/migrate' in step.get('run', '')]
    require(len(found) == 1, f'expected one migrate step, found {len(found)}')
    job, step = found[0]
    require(list(workflow['jobs']) == ['migrate-macos'], f"jobs are {list(workflow['jobs'])!r}")
    require(job.get('runs-on') == 'macos-14', f"runs-on is {job.get('runs-on')!r}")
    require(job.get('timeout-minutes') == 8, f"timeout-minutes is {job.get('timeout-minutes')!r}")
    for where, mapping in (('job', job), ('step', step)):
        for key in ('if', 'continue-on-error'):
            require(key not in mapping, f'{where} has {key}:')
    checkout_setup = [s for s in ci['jobs']['cpu']['steps'] if 'uses' in s]
    require(job['steps'] == checkout_setup + [step], 'job steps are not checkout, setup-python, migrate')
    lines = [line.strip() for line in step['run'].splitlines() if line.strip()]
    require(len(lines) == 2 and lines[0] == PIP, f'run is not {PIP!r} then the discover: {lines!r}')
    require(DISCOVER in lines[1], f'discover line lacks {DISCOVER!r}: {lines[1]!r}')
    return job, lines[1]


def migrate_files():
    return sorted(p.name for p in MIGRATE.glob('test_*.py'))


class MigrateStepTest(unittest.TestCase):
    def setUp(self):
        self.workflow = yaml.safe_load(WORKFLOW.read_text())
        self.ci = yaml.safe_load((ROOT / CI).read_text())

    def test_workflow_has_the_migrate_step(self):
        job, line = migrate_step(self.workflow, self.ci)
        self.assertEqual(job['runs-on'], 'macos-14')
        self.assertIn(DISCOVER, line)

    def test_checker_refuses_each_broken_step(self):
        def broken(change):
            doc = copy.deepcopy(self.workflow)
            job, step = next((j, s) for j in doc['jobs'].values() for s in j['steps']
                             if 'code/ops/migrate' in s.get('run', ''))
            change(doc, job, step)
            return doc

        cases = {
            'step if': lambda d, j, s: s.update({'if': 'false'}),
            'job if': lambda d, j, s: j.update({'if': 'false'}),
            'step continue-on-error': lambda d, j, s: s.update({'continue-on-error': True}),
            'job continue-on-error': lambda d, j, s: j.update({'continue-on-error': True}),
            'linux runner': lambda d, j, s: j.update({'runs-on': 'ubuntu-24.04'}),
            'other macos runner': lambda d, j, s: j.update({'runs-on': 'macos-15'}),
            'no markdown-it pin': lambda d, j, s: s.update({'run': s['run'].replace(' markdown-it-py==3.0.0', '')}),
            'narrowed pattern': lambda d, j, s: s.update({'run': s['run'].replace("'test_*.py'", "'test_f*.py'")}),
            'no pip pin': lambda d, j, s: s.update({'run': s['run'].replace(PIP + '\n', '')}),
            'other pin': lambda d, j, s: s.update({'run': s['run'].replace('1.5.6', '1.5.5')}),
            'extra step': lambda d, j, s: j['steps'].insert(0, {'run': 'true'}),
            'no setup-python': lambda d, j, s: j['steps'].pop(1),
            'second migrate step': lambda d, j, s: d['jobs'].update({'again': {**j, 'steps': [dict(s)]}}),
            'no push paths': lambda d, j, s: triggers(d)['push'].pop('paths'),
            'no pull_request paths': lambda d, j, s: triggers(d)['pull_request'].pop('paths'),
            'third glob': lambda d, j, s: triggers(d)['push']['paths'].append('code/**'),
            'no timeout': lambda d, j, s: j.pop('timeout-minutes'),
            'other timeout': lambda d, j, s: j.update({'timeout-minutes': 30}),
            'other branches': lambda d, j, s: triggers(d)['pull_request'].update({'branches': ['main']}),
            'other name': lambda d, j, s: d.update({'name': 'CI'}),
        }
        for name, change in cases.items():
            with self.subTest(name), self.assertRaises(AssertionError):
                migrate_step(broken(change), self.ci)

    def test_ci_yml_is_untouched(self):
        head = subprocess.run(['git', 'show', f'HEAD:{CI}'], cwd=ROOT, capture_output=True, check=True).stdout
        self.assertEqual((ROOT / CI).read_bytes(), head)

    def test_step_runs_every_migrate_test(self):
        _, line = migrate_step(self.workflow, self.ci)
        shim = tempfile.TemporaryDirectory()
        self.addCleanup(shim.cleanup)
        # The step's python3 is setup-python's in CI; here it is this interpreter, which has duckdb.
        python3 = Path(shim.name) / 'python3'
        python3.write_text(f'#!/bin/sh\nexec {shlex.quote(sys.executable)} "$@"\n')
        python3.chmod(0o755)
        env = dict(os.environ, PATH=f'{shim.name}:{os.environ["PATH"]}')
        run = subprocess.run(['/bin/sh', '-c', line], cwd=ROOT, env=env, capture_output=True, text=True,
                             timeout=900)
        self.assertEqual(run.returncode, 0, run.stderr[-3000:])
        ran = re.findall(r'^Ran (\d+) tests? in [0-9.]+s$', run.stderr, re.MULTILINE)
        self.assertEqual(len(ran), 1, run.stderr[-3000:])
        self.assertRegex(run.stderr.rstrip().splitlines()[-1], r'^OK( \(.*\))?$')

        count = subprocess.run(
            [sys.executable, '-B', '-c', COUNTER, str(MIGRATE), *migrate_files()], cwd=ROOT,
            env=dict(os.environ, PYTHONPATH='code/tests:code', LLMDB_ROOT=str(ROOT)),
            capture_output=True, text=True, timeout=300)
        self.assertEqual(count.returncode, 0, count.stderr[-3000:])
        per_file = json.loads(count.stdout)
        self.assertEqual(sorted(per_file), migrate_files())
        self.assertGreater(sum(per_file.values()), 0)
        self.assertEqual(int(ran[0]), sum(per_file.values()), per_file)

    def test_named_suites_are_among_the_files_found(self):
        found = migrate_files()
        self.assertNotIn(Path(__file__).name, found)
        missing = {step: name for step, name in NAMED_SUITES.items() if name not in found}
        self.assertEqual(missing, {}, 'named suites not found in code/ops/migrate')


if __name__ == '__main__':
    unittest.main()
