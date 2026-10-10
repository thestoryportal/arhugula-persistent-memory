"""CPU-only detector and experiment/status-bar integration controls."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
import shutil
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dashboard_live as L
import dashboard_experiment as X
import dashboard_mathlab as M

TOOLS = Path(__file__).resolve().parent
UTC = '20261009T230000Z'
EVENTS = 'results/mathlab_staging/runs/harvest_20261009T230000Z_101'
CPU_EVENTS = 'results/mathlab_staging/runs/m2_fixture'
NOW = datetime(2026, 10, 9, 20, 0, tzinfo=timezone.utc).timestamp()
CASES = [
    ('bash tools/run_mathlab_harvest.sh results/mathlab/admission.json', 'Math-lab harvest', 3600, None),
    ('python3 -B tools/mathlab_harvest.py --admission a.json --run-dir ' + EVENTS, 'Math-lab harvest', 3600, None),
    ('python3 -B tools/run_c10z_v7_diag.py --utc ' + UTC, 'C10Z V7 probe', 3060, 'results/c10z_v7_diagnostic/' + UTC),
    ('python3 -B experiments/track_c/c10z_v7_diag.py --utc ' + UTC, 'C10Z V7 probe', 3060, 'results/c10z_v7_diagnostic/' + UTC),
    ('bash tools/run_c10y_precast_diag.sh --utc ' + UTC, 'C10Y pre-cast', 2820, 'results/c10y_precast_diag/' + UTC),
    ('python3 -B experiments/track_c/c10y_precast_diag.py --utc ' + UTC + ' --worker', 'C10Y pre-cast', 2820, 'results/c10y_precast_diag/' + UTC),
]


def plain(text):
    return re.sub(r'\033\[[0-9;]*[A-Za-z]', '', text)


class SharedGPUDetector(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for rel in ('tools/run_mathlab_harvest.sh', 'tools/run_c10z_v7_diag.py', 'tools/run_c10y_precast_diag.sh',
                    'tools/run_mathlab_cpu.sh', 'tools/mathlab_cpu_runner.py',
                    'experiments/track_c/c10z_astra_benchmark.py'):
            target = self.root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text((TOOLS.parent / rel).read_text())
        self.addCleanup(patch.stopall)
        patch.object(L, 'ROOT', str(self.root)).start()
        patch.object(X, 'ROOT', str(self.root)).start()

    def response(self, inventory, code=0):
        return subprocess.CompletedProcess(['/bin/ps'], code, inventory, 'fixture denial' if code else '')

    def state(self, inventory, code=0):
        with patch.object(L.subprocess, 'run', return_value=self.response(inventory, code)), \
             patch.object(L.time, 'monotonic', return_value=10000):
            return L.gpu_state()

    def cpu_stream(self, sample_offset=0, terminal=None, purpose='experiment', kind='cpu', allowed=True,
                   deadline_offset=6528):
        def event(event_type, offset=0, **fields):
            ts = datetime.fromtimestamp(NOW + offset, timezone.utc).isoformat()
            return dict(ts=ts, schema=1, run_id='m2_fixture', type=event_type, **fields)
        stream = [event('run_started', -12, step=2, title='CPU reproduction', pid=777,
                        deadline_ts=datetime.fromtimestamp(NOW + deadline_offset, timezone.utc).isoformat(), purpose=purpose),
                  event('admission', -11, allowed=allowed, reasons=[] if allowed else ['refused']),
                  event('gate_result', -11, gate_id='admission', plain_words='Recorded admission',
                        observed={'kind': kind, 'allowed': allowed}, bar='allowed', comparison='meets', passed=allowed),
                  event('stage_started', -10, stage='reproduction', plain_words='Replay saved inputs', cap_s=2700)]
        if terminal == 'halted':
            stream.append(event('halted', -1, reason='resource halt', diagnostic_path='halt.json'))
        elif terminal == 'finished':
            stream.append(event('run_finished', -1, outcome='PASS', summary='CPU run finished'))
        stream.append(event('resource_sample', sample_offset, avail_gib=20., floor_gib=6., rss_gib=5., cpu_pct=100.))
        path = self.root / CPU_EVENTS / 'events.jsonl'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(''.join(json.dumps(e) + '\n' for e in stream))
        return path

    def attempt_record(self, pid=101, closed=False, process=1, requested=None, origins=None):
        out = self.root / 'results/c10z_astra_attempt4'
        out.mkdir(parents=True, exist_ok=True)
        ceilings = {'stage01': 7200, 'stage2': 18000, 'stage3': 24000}
        record = dict(pid=pid, closed=closed, process=process, requested=requested, completed=0,
                      origins=origins or {'stage01': 9900}, ceilings=ceilings,
                      launch=dict(ceilings, go={'ceilings': ceilings}))
        (out / 'run.json').write_text(json.dumps(record))
        return out

    def real_bar(self, inventory='', code=1):
        for rel in ('tools/dashboard_bar.sh', 'tools/dashboard_live.py', 'tools/mathlab_events.py'):
            shutil.copyfile(TOOLS.parent / rel, self.root / rel)
        bin_dir = self.root / 'bin'; bin_dir.mkdir()
        wrapper = bin_dir / 'python3'
        wrapper.write_text('#!/usr/bin/python3 -B\n'
                           'import os, runpy, subprocess, sys, time\nfrom unittest.mock import patch\n'
                           'time.time = lambda: float(os.environ["FIXTURE_NOW"])\n'
                           'sys.path.insert(0, os.path.dirname(sys.argv[2]))\n'
                           'entry=sys.argv[2]; sys.argv=sys.argv[2:]\n'
                           'with patch.object(subprocess, "run", return_value=subprocess.CompletedProcess([], int(os.environ["FIXTURE_CODE"]), os.environ["FIXTURE_PS"], "fixture denied")):\n'
                           '    runpy.run_path(entry, run_name="__main__")\n')
        wrapper.chmod(0o755)
        tmux = bin_dir / 'tmux'; tmux.write_text('#!/bin/sh\nprintf "WORKING\\n"\n'); tmux.chmod(0o755)
        env = dict(os.environ, PATH=str(bin_dir) + ':' + os.environ.get('PATH', ''),
                   FIXTURE_NOW=str(NOW), FIXTURE_CODE=str(code), FIXTURE_PS=inventory,
                   PYTHONDONTWRITEBYTECODE='1')
        result = subprocess.run(['/bin/bash', str(self.root / 'tools/dashboard_bar.sh')], env=env,
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        return plain(result.stdout)

    def test_denied_inventory_keeps_recorded_CPU_visible_in_real_bar_and_110_by_40_experiment(self):
        path = self.cpu_stream(); before = path.read_bytes()
        with self.subTest(path='shared state'), patch.object(L.time, 'time', return_value=NOW):
            state = self.state('', 1)
            self.assertTrue(state['unavailable'])
            self.assertEqual(state.get('jobs'), [])
            jobs = state.get('cpu_jobs', [])
            self.assertEqual(len(jobs), 1, 'fresh admitted CPU activity must survive denied process inventory')
            self.assertFalse(jobs[0]['process_verified'])
            self.assertEqual(jobs[0]['pids'], [], 'event PID does not prove notebook liveness')
            self.assertEqual(jobs[0]['cap_s'], 6540)
        with self.subTest(path='experiment'), patch.object(L.time, 'time', return_value=NOW), \
             patch.object(L.subprocess, 'run', return_value=self.response('', 1)), \
             patch.object(X, 'machine', side_effect=AssertionError('recorded activity must not probe machine')):
            lines = X.render(110, 40)
            text = plain('\n'.join(lines))
            for value in ('GPU UNAVAILABLE', 'Math-lab step 2', '6540s', CPU_EVENTS, 'process unverified', 'Output: unavailable'):
                self.assertIn(value, text)
            self.assertLessEqual(len(lines), 40)
            self.assertTrue(all(len(plain(line)) <= 110 for line in lines))
        with self.subTest(path='real bar'):
            visible = self.real_bar()[:144]
            for value in ('GPU unavailable', 'CPU recorded', 'Math-lab step 2', '6540s', CPU_EVENTS):
                self.assertIn(value, visible)
        self.assertEqual(path.read_bytes(), before)

    def test_CPU_launchers_runners_uv_and_notebook_workers_are_separate_from_GPU_jobs(self):
        commands = [
            ('bash tools/run_mathlab_cpu.sh mathlab/m2_solve_repro.py 6540', 2, 6540),
            ('python3 -B tools/mathlab_cpu_runner.py mathlab/m2_solve_repro.py 6540 --run-dir ' + CPU_EVENTS, 2, 6540),
            ('uv run --script mathlab/m2_solve_repro.py', 2, 6540),
            ('python3 mathlab/m2_solve_repro.py', 2, 6540),
            ('bash tools/run_mathlab_cpu.sh mathlab/m3_calibration.py 1800', 3, 1800),
            ('uv run --script mathlab/m3_calibration.py', 3, 1800),
            ('python3 tools/mathlab_admit.py --kind cpu --step 2 --deadline-s 6540 --run-dir ' + CPU_EVENTS, 2, 6540),
            ('nice -n 10 /opt/homebrew/bin/timeout -k 30 6540 uv run --script mathlab/m2_solve_repro.py', 2, 6540),
        ]
        for command, step, cap in commands:
            with self.subTest(command=command):
                state = self.state('101 1 00:12 ' + command + '\n')
                self.assertEqual(state['jobs'], [])
                self.assertIsNone(state['running'], 'CPU activity never occupies the GPU')
                jobs = state.get('cpu_jobs', [])
                self.assertEqual(len(jobs), 1)
                self.assertEqual(jobs[0]['name'], 'Math-lab step ' + str(step))
                self.assertEqual(jobs[0]['cap_s'], cap)
                self.assertTrue(jobs[0]['process_verified'])
                self.assertEqual(jobs[0]['etime'], '00:12')
                self.assertIsNone(jobs[0]['output_dir'])

    def test_CPU_parent_timeout_and_uv_worker_are_one_verified_process_family(self):
        inventory = ('101 1 01:02 python3 tools/mathlab_cpu_runner.py mathlab/m2_solve_repro.py 6540 --run-dir ' + CPU_EVENTS + '\n'
                     '102 101 00:45 timeout -k 30 6540 uv run --script mathlab/m2_solve_repro.py\n'
                     '103 102 00:30 uv run --script mathlab/m2_solve_repro.py\n'
                     '104 103 00:20 python3 mathlab/m2_solve_repro.py\n')
        jobs = self.state(inventory).get('cpu_jobs', [])
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]['pids'], ['101', '102', '103', '104'])
        self.assertEqual(jobs[0]['etime'], '01:02')
        self.assertEqual(jobs[0]['run_dir'], str(self.root / CPU_EVENTS))

    def test_transparent_wrappers_keep_GPU_jobs_and_exact_benchmark_output(self):
        output = self.root / 'results/benchmark with space'
        cases = [('caffeinate -i env -u C10Z_TELEMETRY python3 -B experiments/track_c/c10z_astra_benchmark.py --out ' + repr(str(output)), 'C10Z benchmark', 600, output),
                 ('python3 experiments/track_c/c10z_astra_benchmark.py --worker --out ' + repr(str(output)) + ' --t0 100', 'C10Z benchmark', 600, output),
                 ('caffeinate -i env python3 tools/run_c10z_v7_diag.py --utc ' + UTC, 'C10Z V7 probe', 3060, self.root / 'results/c10z_v7_diagnostic' / UTC)]
        for command, name, cap, out in cases:
            with self.subTest(command=command):
                jobs = self.state('101 1 00:12 ' + command + '\n')['jobs']
                self.assertEqual(len(jobs), 1)
                self.assertEqual((jobs[0]['name'], jobs[0]['cap_s'], jobs[0]['output_dir']), (name, cap, str(out)))

    def test_new_wrappers_prompts_inline_modules_and_temp_copies_are_not_jobs(self):
        for command in ('uv run reviewer.py --prompt "--script mathlab/m2_solve_repro.py"',
                        'uv run echo --script mathlab/m2_solve_repro.py',
                        'uv run --script /private/tmp/mathlab/m2_solve_repro.py',
                        'env python3 -cpass experiments/track_c/c10z_astra_benchmark.py --out x',
                        'caffeinate -i bash -c "uv run --script mathlab/m2_solve_repro.py"',
                        'env python3 -m unittest experiments/track_c/c10z_astra_benchmark.py',
                        'python3 experiments/track_c/c10z_astra_benchmark_selftest.py'):
            with self.subTest(command=command):
                state = self.state('101 1 00:12 ' + command + '\n')
                self.assertEqual(state['jobs'], [])
                self.assertEqual(state.get('cpu_jobs', []), [])

    def test_native_selftests_and_help_do_not_claim_GPU_jobs(self):
        for command in ('python3 experiments/track_c/c10z_astra_arms.py --selftest',
                        'python3 experiments/track_c/c10z_v7_diag.py --selftest',
                        'python3 tools/run_c10z_v7_diag.py --help',
                        'python3 experiments/track_c/c10z_astra_benchmark.py --help'):
            with self.subTest(command=command):
                state = self.state('101 1 00:12 ' + command + '\n')
                self.assertEqual(state['jobs'], [])
                self.assertEqual(state.get('cpu_jobs', []), [])

    def test_benchmark_and_CPU_caps_read_sources_without_importing_native_jobs(self):
        (self.root / 'experiments/track_c/c10z_astra_benchmark.py').write_text('def supervise(worker_cmd, out, cap_s=321.):\n    raise RuntimeError("never import")\n')
        cpu = self.root / 'tools/run_mathlab_cpu.sh'
        cpu.write_text(cpu.read_text().replace('m2_solve_repro.py:6540', 'm2_solve_repro.py:4321'))
        bench = self.state('101 1 00:12 python3 experiments/track_c/c10z_astra_benchmark.py --out results/b\n')['jobs']
        self.assertEqual(len(bench), 1)
        self.assertEqual(bench[0]['cap_s'], 321)
        cpu_jobs = self.state('101 1 00:12 uv run --script mathlab/m2_solve_repro.py\n').get('cpu_jobs', [])
        self.assertEqual(len(cpu_jobs), 1)
        self.assertEqual(cpu_jobs[0]['cap_s'], 4321)
        self.assertNotIn('torch', sys.modules)
        self.assertNotIn('transformers', sys.modules)

    def test_attempt_launcher_stage_and_resident_use_explicit_output_and_bound_budget(self):
        out = self.attempt_record()
        for command in ('bash tools/run_c10z_attempt.sh', 'bash tools/run_c10z_stage.sh 0',
                        'python3 -B experiments/track_c/c10z_astra_arms.py 0'):
            with self.subTest(command=command), patch.object(L.time, 'monotonic', return_value=10000):
                jobs = self.state('101 1 02:00 env C10Z_OUT_DIR=' + str(out) + ' ' + command + '\n')['jobs']
                self.assertEqual(len(jobs), 1)
                self.assertEqual(jobs[0]['name'], 'C10Z attempt 4')
                self.assertEqual(jobs[0]['output_dir'], str(out))
                self.assertEqual(jobs[0]['cap_s'], 7200)
                self.assertEqual(jobs[0]['elapsed_s'], 100)
                self.assertIn('recorded', L.job_summary(jobs[0]).lower())

    def test_stage2_requested_without_published_origin_has_no_invented_active_cap(self):
        self.attempt_record(requested=2)
        jobs = self.state('101 1 02:00 python3 experiments/track_c/c10z_astra_arms.py 0\n')['jobs']
        self.assertEqual(len(jobs), 1)
        self.assertIsNone(jobs[0]['cap_s'])
        self.assertEqual(jobs[0].get('selected_caps', {}).get('stage2'), 18000)
        with patch.object(L.subprocess, 'run', return_value=self.response('101 1 02:00 python3 experiments/track_c/c10z_astra_arms.py 0\n')), \
             patch.object(L.time, 'monotonic', return_value=10000):
            text = plain('\n'.join(X.render(110, 40)))
        self.assertIn('budget unavailable', text.lower())
        self.assertIn('18000s', text)

    def test_process2_recorded_earlier_stage01_deadline_beats_stage3(self):
        self.attempt_record(process=2, origins={'stage01': 9900, 'stage3': 9900})
        with patch.object(L.time, 'monotonic', return_value=10000):
            jobs = self.state('101 1 02:00 python3 experiments/track_c/c10z_astra_arms.py 3\n')['jobs']
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]['cap_s'], 7200)
        self.assertEqual(jobs[0]['budget_scope'], 'stage01')
        self.assertEqual(jobs[0]['selected_caps']['stage3'], 24000)
        self.assertIn('recorded', L.job_summary(jobs[0]).lower())

    def test_process2_record_is_bound_from_its_actual_nested_output(self):
        out = self.attempt_record(process=2, origins={'stage01': 9900, 'stage3': 9900})
        worker = out / 'process2'; worker.mkdir()
        (out / 'run.json').rename(worker / 'run.json')
        jobs = self.state('101 1 02:00 python3 experiments/track_c/c10z_astra_arms.py _resident 2\n')['jobs']
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]['name'], 'C10Z attempt 4')
        self.assertEqual(jobs[0]['output_dir'], str(worker))
        self.assertEqual((jobs[0]['cap_s'], jobs[0]['budget_scope']), (7200, 'stage01'))

    def test_malformed_attempt_snapshots_show_unavailable_without_crashing_or_guessing(self):
        for field, value in (('origins', []), ('ceilings', []), ('ceilings', {'stage01': True}),
                             ('origins', {'stage01': 'bad'}), ('launch', 'bad')):
            with self.subTest(field=field, value=value):
                out = self.attempt_record()
                record = json.loads((out / 'run.json').read_text()); record[field] = value
                (out / 'run.json').write_text(json.dumps(record))
                job = self.state('101 1 02:00 python3 experiments/track_c/c10z_astra_arms.py 0\n')['jobs'][0]
                self.assertIsNone(job['cap_s'])
                self.assertIn('budget unavailable', job.get('budget_note', '').lower())

    def test_conflicting_observer_env_closed_and_ambiguous_records_never_invent_output(self):
        out = self.attempt_record(closed=True)
        with patch.dict(os.environ, {'C10Z_OUT_DIR': str(out)}):
            jobs = self.state('101 1 02:00 bash tools/run_c10z_attempt.sh\n')['jobs']
        self.assertEqual(len(jobs), 1)
        self.assertIsNone(jobs[0]['output_dir'])
        self.assertIsNone(jobs[0]['cap_s'])
        self.attempt_record(closed=False)
        other = self.root / 'results/c10z_astra_attempt_other'; other.mkdir()
        shutil.copyfile(out / 'run.json', other / 'run.json')
        jobs = self.state('101 1 02:00 bash tools/run_c10z_attempt.sh\n')['jobs']
        self.assertIsNone(jobs[0]['output_dir'], 'two PID matches cannot establish unique output provenance')

    def test_reused_PID_with_older_open_record_cannot_supply_output(self):
        self.attempt_record(origins={'stage01': 9000})
        command='101 1 00:12 python3 experiments/track_c/c10z_astra_arms.py 0\n'
        job=self.state(command)['jobs'][0]
        self.assertIsNone(job['output_dir'])
        self.assertIsNone(job['cap_s'])
        out=self.attempt_record(origins={'stage01': 9995})
        job=self.state(command)['jobs'][0]
        self.assertEqual(job['output_dir'], str(out), 'positive process-age binding must still work')

    def test_older_launcher_cannot_rescue_a_reused_resident_PID_record(self):
        self.attempt_record(origins={'stage01': 9000})
        inventory = ('100 1 20:00 bash tools/run_c10z_attempt.sh\n'
                     '101 100 00:12 python3 experiments/track_c/c10z_astra_arms.py 0\n')
        job = self.state(inventory)['jobs'][0]
        self.assertEqual(job['pids'], ['100', '101'])
        self.assertIsNone(job['output_dir'])
        self.assertIsNone(job['cap_s'])
        out = self.attempt_record(origins={'stage01': 9995})
        job = self.state(inventory)['jobs'][0]
        self.assertEqual(job['output_dir'], str(out))
        self.assertEqual(job['cap_s'], 7200)

    def test_independent_attempt_families_keep_conflicting_explicit_dirs_and_go_caps(self):
        go = self.root / 'go.json'; go.write_text(json.dumps({'ceilings': {'stage01': 7200, 'stage2': 18000, 'stage3': 24000}}))
        out1=self.root / 'results/c10z_astra_attempt4'; out2=self.root / 'results/c10z_astra_attempt5'
        inventory=('101 1 01:02 env C10Z_OUT_DIR=' + str(out1) + ' C10Z_GO_RECORD=' + str(go) + ' bash tools/run_c10z_attempt.sh\n'
                   '201 1 02:03 env C10Z_OUT_DIR=' + str(out2) + ' C10Z_GO_RECORD=' + str(go) + ' bash tools/run_c10z_attempt.sh\n')
        jobs=self.state(inventory)['jobs']
        self.assertEqual(len(jobs), 2)
        self.assertEqual([j['output_dir'] for j in jobs], [str(out1), str(out2)])
        self.assertTrue(all(j['cap_s'] is None and j['selected_caps']['stage01']==7200 for j in jobs))

    def test_nested_env_ignore_environment_clears_outer_output_and_go_bindings(self):
        old = self.root / 'results/old'
        new = self.root / 'results/c10z_astra_attempt4'
        go = self.root / 'go.json'
        go.write_text(json.dumps({'ceilings': {'stage01': 7200, 'stage2': 18000, 'stage3': 24000}}))
        prefix = '101 1 00:12 env C10Z_OUT_DIR=' + str(old) + ' C10Z_GO_RECORD=' + str(go)
        for flag in ('-i', '--ignore-environment'):
            with self.subTest(flag=flag):
                job = self.state(prefix + ' env ' + flag + ' python3 experiments/track_c/c10z_astra_arms.py 0\n')['jobs'][0]
                self.assertIsNone(job['output_dir'])
                self.assertIsNone(job['go_path'])
                self.assertEqual(job['selected_caps'], {})
                job = self.state(prefix + ' env ' + flag + ' C10Z_OUT_DIR=' + str(new) + ' C10Z_GO_RECORD=' + str(go) +
                                 ' python3 experiments/track_c/c10z_astra_arms.py 0\n')['jobs'][0]
                self.assertEqual(job['output_dir'], str(new))
                self.assertEqual(job['selected_caps']['stage01'], 7200)

    def test_stale_future_expired_halted_finished_admission_and_wrong_kind_do_not_claim_CPU_activity(self):
        cases=[dict(sample_offset=-61), dict(sample_offset=60), dict(deadline_offset=-1),
               dict(terminal='halted'), dict(terminal='finished'), dict(purpose='admission'),
               dict(kind='harvest'), dict(allowed=False)]
        for case in cases:
            with self.subTest(case=case), patch.object(L.time, 'time', return_value=NOW):
                self.cpu_stream(**case)
                state=self.state('', 1)
                self.assertTrue(state['unavailable'])
                self.assertEqual(state.get('cpu_jobs', []), [])

    def test_malformed_CPU_stream_is_refused_and_explained(self):
        path=self.cpu_stream(); path.write_text(path.read_text() + '{broken}\n')
        with patch.object(L.time, 'time', return_value=NOW):
            state=self.state('', 1)
        self.assertEqual(state.get('cpu_jobs', []), [])
        self.assertTrue(state.get('cpu_record_errors'), 'broken provenance must be visible')

    def test_recorded_CPU_accepts_actual_publisher_microsecond_timestamps(self):
        path = self.cpu_stream()
        events = [json.loads(line) for line in path.read_text().splitlines()]
        for event in events:
            for key in ('ts', 'deadline_ts'):
                if key in event:
                    event[key] = datetime.fromisoformat(event[key]).replace(microsecond=125000).isoformat()
        path.write_text(''.join(json.dumps(event) + '\n' for event in events))
        with patch.object(L.time, 'time', return_value=NOW + .25):
            jobs, errors = L.recorded_cpu_jobs()
        self.assertEqual(errors, [])
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]['cap_s'], 6540)

    def test_GPU_and_CPU_jobs_are_both_visible_without_CPU_changing_GPU_occupancy(self):
        inventory=('101 1 00:12 python3 tools/run_c10z_v7_diag.py --utc ' + UTC + '\n'
                   '201 1 00:34 uv run --script mathlab/m3_calibration.py\n')
        state=self.state(inventory)
        self.assertEqual(state['running'], ('c10z', 'v7-diag', '00:12'))
        self.assertEqual(len(state['jobs']), 1)
        self.assertEqual(len(state.get('cpu_jobs', [])), 1)
        with patch.object(L.subprocess, 'run', return_value=self.response(inventory)):
            lines=X.render(110, 40)
        text=plain('\n'.join(lines))
        for value in ('C10Z V7 probe', 'Math-lab step 3', '3060s', '1800s'):
            self.assertIn(value, text)
        self.assertLessEqual(len(lines), 40)
        self.assertTrue(all(len(plain(line)) <= 110 for line in lines))

    def test_six_launcher_and_worker_aliases_show_named_job_elapsed_cap_and_exact_namespace(self):
        for command, name, cap, output in CASES:
            with self.subTest(command=command):
                state = self.state('101 1 00:12 ' + command + '\n')
                jobs = state.get('jobs', [])
                self.assertEqual(len(jobs), 1, 'running GPU job vanished from the shared detector')
                job = jobs[0]
                self.assertEqual(job['name'], name)
                self.assertEqual(job['etime'], '00:12')
                self.assertEqual(job['elapsed_s'], 12)
                self.assertEqual(job['cap_s'], cap)
                self.assertEqual(job['output_dir'], str(self.root / output) if output else None)
                self.assertEqual(job['pids'], ['101'])
                if '--run-dir' in command:
                    self.assertEqual(job['run_dir'], str(self.root / EVENTS))

    def test_parent_worker_and_admission_share_one_job_with_original_elapsed(self):
        inventory = ('101 1 01:02 bash tools/run_mathlab_harvest.sh a.json\n'
                     '102 101 00:45 python3 tools/mathlab_admit.py --kind harvest --run-dir ' + EVENTS + ' --deadline-s 3600\n'
                     '201 1 02:03 python3 tools/run_c10z_v7_diag.py --utc ' + UTC + '\n'
                     '202 201 00:30 python3 tools/run_c10z_v7_diag.py --worker --utc ' + UTC + '\n'
                     '301 1 03:04 bash tools/run_c10y_precast_diag.sh --utc ' + UTC + '\n'
                     '302 301 00:20 python3 experiments/track_c/c10y_precast_diag.py --utc ' + UTC + ' --worker\n')
        jobs = self.state(inventory).get('jobs', [])
        self.assertEqual(len(jobs), 3, 'one job per live run; wrappers must not hide or double-count workers')
        self.assertEqual([(j['name'], j['etime'], j['pids']) for j in jobs],
                         [('Math-lab harvest', '01:02', ['101', '102']),
                          ('C10Z V7 probe', '02:03', ['201', '202']),
                          ('C10Y pre-cast', '03:04', ['301', '302'])])
        self.assertEqual(jobs[0]['run_dir'], str(self.root / EVENTS))

    def test_prompts_inline_code_modules_and_temporary_copies_do_not_claim_gpu(self):
        commands = ['codex --prompt "python3 tools/mathlab_harvest.py --run-dir x"',
                    'python3 tools/reviewer.py --prompt "experiments/track_c/c10z_v7_diag.py --utc ' + UTC + '"',
                    'python3 tools/reviewer.py --prompt "experiments/track_c/c10w_oracle_arms.py p2-eval"',
                    'python3 -c "print(\'tools/run_c10z_v7_diag.py --utc ' + UTC + '\')"',
                    'bash -c "python3 tools/mathlab_harvest.py --run-dir x"',
                    'python3 -m unittest tools/run_c10z_v7_diag.py --utc ' + UTC,
                    'python3 -cpass tools/run_c10z_v7_diag.py --utc ' + UTC,
                    'python3 -munittest tools/run_c10z_v7_diag.py --utc ' + UTC,
                    'python3 experiments/track_c/c10z_v7_diag_selftest.py',
                    'python3 /private/tmp/tools/mathlab_harvest.py --run-dir x',
                    'python3 /tmp/experiments/track_c/c10z_v7_diag.py --utc ' + UTC,
                    'python3 tools/test_dashboard_gpu_detector.py']
        for command in commands:
            with self.subTest(command=command):
                state = self.state('101 1 00:12 ' + command + '\n')
                self.assertIsNone(state['running'])
                self.assertEqual(state.get('jobs', []), [])

    def test_unrelated_same_namespace_process_families_are_two_competing_jobs(self):
        inventory = ('101 1 01:02 python3 tools/run_c10z_v7_diag.py --utc ' + UTC + '\n'
                     '102 101 00:45 python3 tools/run_c10z_v7_diag.py --worker --utc ' + UTC + '\n'
                     '201 1 02:03 python3 tools/run_c10z_v7_diag.py --utc ' + UTC + '\n'
                     '202 201 00:30 python3 tools/run_c10z_v7_diag.py --worker --utc ' + UTC + '\n')
        jobs = self.state(inventory).get('jobs', [])
        self.assertEqual(len(jobs), 2, 'matching output paths do not establish common process ownership')
        self.assertEqual([j['pids'] for j in jobs], [['101', '102'], ['201', '202']])

    def test_quoted_run_directory_is_preserved_as_exact_token(self):
        path = '/Volumes/memit/observations with space/harvest'
        command = "python3 tools/mathlab_harvest.py --run-dir '" + path + "'"
        jobs = self.state('101 1 00:12 ' + command + '\n').get('jobs', [])
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]['run_dir'], path)

    def test_bash_long_option_does_not_turn_script_into_inline_code(self):
        jobs = self.state('101 1 00:12 bash --norc tools/run_c10y_precast_diag.sh --utc ' + UTC + '\n').get('jobs', [])
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]['name'], 'C10Y pre-cast')

    def test_caps_are_read_from_current_launcher_source_without_importing_jobs(self):
        (self.root / 'tools/run_c10z_v7_diag.py').write_text('CAP_SECONDS = 321\nraise RuntimeError("must never import")\n')
        jobs = self.state('101 1 00:12 python3 tools/run_c10z_v7_diag.py --utc ' + UTC + '\n').get('jobs', [])
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]['cap_s'], 321)
        self.assertNotIn('torch', sys.modules)
        self.assertNotIn('transformers', sys.modules)

    def test_harvest_events_directory_never_becomes_an_inferred_artifact_directory(self):
        stale = self.root / 'results/mathlab/harvest_20991231T235959Z'
        stale.mkdir(parents=True)
        (stale / 'manifest.json').write_text('{}')
        jobs = self.state('101 1 00:12 ' + CASES[1][0] + '\n').get('jobs', [])
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]['run_dir'], str(self.root / EVENTS))
        self.assertIsNone(jobs[0]['output_dir'])

    def test_denied_empty_and_malformed_inventory_are_unavailable_never_idle(self):
        for code, inventory in ((1, ''), (0, ''), (0, ' \n'), (0, 'not a process inventory\n')):
            with self.subTest(code=code, inventory=inventory):
                state = self.state(inventory, code)
                self.assertTrue(state.get('unavailable'), 'failed visibility must never be GPU idle')
        with patch.object(L.subprocess, 'run', side_effect=PermissionError('process inventory denied')):
            try:
                state = L.gpu_state()
            except OSError as error:
                self.fail('shared detector must return unavailable rather than crash: ' + str(error))
        self.assertIn('denied', state['unavailable'])

    def test_experiment_110_by_40_shows_each_new_job_without_unrelated_c10_logs(self):
        for command, name, cap, output in CASES:
            with self.subTest(command=command), \
                 patch.object(L.subprocess, 'run', return_value=self.response('101 1 00:12 ' + command + '\n')), \
                 patch.object(X, 'machine', return_value=' Machine fixture; no GPU access'):
                lines = X.render(110, 40)
                text = plain('\n'.join(lines))
                self.assertIn(name, text)
                self.assertIn('00:12', text)
                self.assertIn(str(cap) + 's', text)
                self.assertIn(output or 'Output: unavailable', text)
                if '--run-dir' in command:
                    self.assertIn(EVENTS, text)
                self.assertNotIn('61/72', text)
                self.assertLessEqual(len(lines), 40)
                self.assertTrue(all(len(plain(line)) <= 110 for line in lines))

    def test_experiment_denied_inventory_is_visible_at_110_by_40(self):
        with patch.object(L.subprocess, 'run', side_effect=PermissionError('process inventory denied')):
            try:
                text = plain('\n'.join(X.render(110, 40)))
            except OSError as error:
                self.fail('headless experiment must show unavailable: ' + str(error))
        self.assertIn('GPU UNAVAILABLE', text)
        self.assertIn('denied', text)
        self.assertNotIn('GPU IDLE', text)

    def test_legacy_driver_and_job_worker_keep_stage_pid_and_run_label(self):
        inventory = ('101 1 01:02 python3 experiments/track_c/c10w_oracle_arms.py p2-eval\n'
                     '102 101 00:30 python3 experiments/track_c/c10w_oracle_arms.py _job --job behavior --block F --replicate 0 --kind mint1 --seed 1\n')
        state = self.state(inventory)
        self.assertEqual(state['running'], ('c10w', 'p2-eval', '01:02'))
        with patch.object(L.subprocess, 'run', return_value=self.response(inventory)):
            top, pids, label = X.running()
        self.assertEqual(top, state['running'])
        self.assertEqual(pids, ['101', '102'])
        self.assertEqual(label, 'behavior_F_r0_mint1_s1')

    def legacy_logs(self):
        logs = self.root / 'results/c10w_oracle_logs'
        logs.mkdir(parents=True)
        finished = logs / 'behavior_F_r0_mint1_s1.log'
        finished.write_text('BEHAVIOR mint1: raw=27 binding=27\nSTAGE_EXIT=0\n')
        current = logs / 'p2-eval.log'
        current.write_text('step 7 loss 0.5\nLegacy worker progress marker\n')
        os.utime(finished, (NOW - 20, NOW - 20))
        os.utime(current, (NOW - 10, NOW - 10))
        (logs / 'fixture_started.json').write_text(json.dumps({'plan': ['first', 'second', 'third']}))

    def legacy_render(self, inventory):
        with patch.object(L.subprocess, 'run', return_value=self.response(inventory)), \
             patch.object(L.time, 'time', return_value=NOW), \
             patch.object(X, 'machine', return_value=' Machine fixture; no GPU probe'):
            lines = X.render(110, 40)
        self.assertLessEqual(len(lines), 40)
        self.assertTrue(all(len(plain(line)) <= 110 for line in lines))
        return plain('\n'.join(lines))

    def assert_legacy_details(self, text):
        for expected in ('stage p2-eval', 'PROGRESS', '1 of 3 runs', 'FINISHED RUNS',
                         '27/72', 'NOW', 'training step 7', 'Legacy worker progress marker'):
            self.assertIn(expected, text)

    def test_worker_only_inventory_is_busy_in_all_three_consumers(self):
        self.legacy_logs()
        inventory = ('102 1 00:30 python3 experiments/track_c/c10w_oracle_arms.py _job '
                     '--job behavior --block F --replicate 0 --kind mint1 --seed 1\n')
        with self.subTest(consumer='shared state'):
            self.assertEqual(self.state(inventory)['running'], ('c10w', '_job', '00:30'))
        with self.subTest(consumer='real status bar'):
            text = self.real_bar(inventory, 0)
            self.assertIn('Step 5', text)
            self.assertIn('stage _job', text)
            self.assertNotIn('idle', text.split('   │')[0])
        with self.subTest(consumer='experiment'):
            text = self.legacy_render(inventory)
            self.assertIn('RUNNING', text)
            self.assertIn('stage _job', text)
            self.assertNotIn('GPU IDLE', text)
        with self.subTest(consumer='MathLab'), patch.object(M, 'ROOT', str(self.root)), \
             patch.object(L.subprocess, 'run', return_value=self.response(inventory)):
            text = plain('\n'.join(M.render(110, 40)))
            self.assertIn('GPU in use by Step 5 (c10w)', text)
            self.assertIn('_job', text)
            self.assertNotIn('GPU free', text)

    def test_legacy_experiment_fixture_contains_progress_results_and_logs(self):
        self.legacy_logs()
        self.assert_legacy_details(self.legacy_render(
            '101 1 01:02 python3 experiments/track_c/c10w_oracle_arms.py p2-eval\n'))

    def test_legacy_worker_without_logs_keeps_GPU_and_CPU_activity_visible(self):
        text = self.legacy_render(
            '102 1 00:30 python3 experiments/track_c/c10w_oracle_arms.py _job --job behavior\n'
            '201 1 00:12 uv run --script mathlab/m2_solve_repro.py\n')
        for expected in ('GPU RUNNING', 'stage _job', 'No experiment logs found',
                         'CPU RUNNING', 'Math-lab step 2', '6540s'):
            self.assertIn(expected, text)
        self.assertNotIn('GPU IDLE', text)

    def test_legacy_experiment_details_survive_concurrent_CPU_process(self):
        self.legacy_logs()
        text = self.legacy_render(
            '101 1 01:02 python3 experiments/track_c/c10w_oracle_arms.py p2-eval\n'
            '201 1 00:12 uv run --script mathlab/m2_solve_repro.py\n')
        self.assert_legacy_details(text)
        for expected in ('CPU RUNNING', 'Math-lab step 2', '00:12', '6540s', 'Output: unavailable'):
            self.assertIn(expected, text)

    def test_legacy_experiment_details_survive_recorded_CPU_activity(self):
        self.legacy_logs()
        self.cpu_stream()
        text = self.legacy_render('101 1 01:02 python3 experiments/track_c/c10w_oracle_arms.py p2-eval\n')
        self.assert_legacy_details(text)
        for expected in ('CPU RECORDED', 'Math-lab step 2', '6540s', CPU_EVENTS, 'process unverified'):
            self.assertIn(expected, text)

    def test_legacy_experiment_details_survive_CPU_record_error(self):
        self.legacy_logs()
        with self.cpu_stream().open('a') as f:
            f.write('{malformed event\n')
        text = self.legacy_render('101 1 01:02 python3 experiments/track_c/c10w_oracle_arms.py p2-eval\n')
        self.assert_legacy_details(text)
        self.assertIn('CPU records unavailable:', text)
        self.assertNotIn('CPU RECORDED', text)

    def test_real_status_bar_keeps_job_metadata_within_existing_150_cell_budget(self):
        bin_dir = self.root / 'bin'
        bin_dir.mkdir()
        wrapper = bin_dir / 'python3'
        wrapper.write_text('#!/usr/bin/python3 -B\n'
                           'import os, runpy, subprocess, sys\n'
                           'from unittest.mock import patch\n'
                           'sys.path.insert(0, os.path.dirname(sys.argv[2]))\n'
                           'entry = sys.argv[2]; sys.argv = sys.argv[2:]\n'
                           'with patch.object(subprocess, "run", return_value=subprocess.CompletedProcess([], 0, os.environ["GPU_FIXTURE"], "")):\n'
                           '    runpy.run_path(entry, run_name="__main__")\n')
        wrapper.chmod(0o755)
        tmux = bin_dir / 'tmux'
        tmux.write_text('#!/bin/sh\nprintf "WORKING\\nASKING\\nACTIVE\\nIDLE\\n"\n')
        tmux.chmod(0o755)
        for index in (1, 2, 4):
            command, name, cap, output = CASES[index]
            inventory = '101 1 00:12 ' + command + '\n'
            env = dict(os.environ, PATH=str(bin_dir) + ':' + os.environ.get('PATH', ''), GPU_FIXTURE=inventory,
                       PYTHONDONTWRITEBYTECODE='1')
            result = subprocess.run(['/bin/bash', str(TOOLS / 'dashboard_bar.sh')], env=env,
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            # team_dashboard.sh reserves 150 cells for the bar plus its six-cell clock.
            visible = plain(result.stdout)[:144]
            self.assertIn(name, visible)
            self.assertIn('00:12', visible)
            self.assertIn(str(cap) + 's', visible)
            self.assertIn(output or EVENTS, visible)
            if index == 1:
                self.assertIn('output unavailable', visible)


if __name__ == '__main__':
    unittest.main()
