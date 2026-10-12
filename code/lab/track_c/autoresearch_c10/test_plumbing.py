"""No-model tests for v13's serialization, trust boundaries and static contracts."""
import ast
import copy
import json
import os
import signal
import stat
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))
import v13_common as C
import audit_transcript as A
import sandbox_settings as P
import v13_graft as G
from v13_build import cleaned

SUMMARY = {'heldout_full': 7, 'canon': 7, 'first_token': 40, 'A1': 69, 'A2': 69,
           'L1_flips': 0, 'frame_flips': 1, 'described_as': 90.38, 'L3': 30,
           'ppl_post': 21.506, 'law5_ok': True, 'scope_ok': True, 'dw_total': 88.974,
           'edit_seconds': 0.0, 'score_seconds': 0.0, 'guards': 'ok'}


class Boundaries(unittest.TestCase):
    def test_projection_is_exact_and_private(self):
        out = C.projection({'summary': SUMMARY, 'private': 'hidden'})
        self.assertEqual(tuple(out), C.SUMMARY)
        self.assertNotIn('private', out)

    def test_projection_rejects_malformed_and_oracle_fields(self):
        for k, v in [('heldout_full', True), ('canon', 72), ('dw_total', float('nan')),
                     ('guards', 'failed:phrase'), ('law5_ok', 1), ('described_as', 101)]:
            s = dict(SUMMARY, **{k: v})
            with self.subTest(k=k), self.assertRaises(ValueError):
                C.projection({'summary': s})
        with self.assertRaises(ValueError):
            C.projection({'summary': dict(SUMMARY, per_template=[1])})

    def test_json_rejects_duplicate_keys_and_nan(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'x'
            for text in ('{"a":1,"a":2}', '{"a":NaN}'):
                p.write_text(text)
                with self.assertRaises(ValueError):
                    C.read_json(p)

    def test_snapshot_rejects_symlink_and_hardlink(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = root / 'source'
            source.write_bytes(b'harmless')
            link = root / 'symlink'
            link.symlink_to(source)
            with self.assertRaises(OSError):
                C.snapshot(link, root / 'out')
            os.link(source, root / 'hardlink')
            with self.assertRaises(ValueError):
                C.snapshot(source, root / 'out')
            (root / 'hardlink').unlink()
            C.snapshot(source, root / 'out')
            self.assertEqual((root / 'out').read_bytes(), b'harmless')

    def test_manifest_rejects_changed_helper(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'sealed').mkdir()
            f = root / 'helper'
            f.write_text('safe')
            C.write_json(root / 'sealed/config.json', {'v': 13})
            C.write_json(root / 'sealed/manifest.json', {str(f): C.digest(f)})
            anchor = C.digest(root / 'sealed/manifest.json')
            self.assertEqual(C.verify(root, anchor), {'v': 13})
            f.write_text('changed')
            with self.assertRaises(ValueError):
                C.verify(root, anchor)

    def test_environment_drops_credentials_and_harness_overrides(self):
        c = {'home': '/home/fixture', 'user': 'fixture', 'hf_home': '/cache', 'program': '/program'}
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'sentinel', 'MODEL_ID': 'override',
                                     'PYTHONPATH': '/malicious', 'LD_PRELOAD': '/malicious'}):
            env = C.clean_env(c, '/own', '/run')
        self.assertFalse(set(env) & {'ANTHROPIC_API_KEY', 'MODEL_ID', 'PYTHONPATH', 'LD_PRELOAD'})
        self.assertEqual(env['HF_HUB_OFFLINE'], '1')
        for name in ('GRAFT_NO_REFRESH', 'GRAFT_NO_GITIGNORE', 'GRAFT_NO_IGNORE'):
            self.assertEqual(env[name], '1')

    def test_graft_files_and_processes_are_identified(self):
        for path in ('graft/.cache/ask-index.json', 'runs/a/graft/INDEX.md', 'x/ask-index.json'):
            self.assertTrue(G.forbidden(path))
        self.assertFalse(G.forbidden('v13_graft.py'))
        for cmd in ('graft ask x', 'node /node_modules/@nanonets/graft/dist/cli.js build',
                    'node /node_modules/@nanonets/graft/dist/claude/sync-run.js'):
            self.assertIsNotNone(G.GRAFT_PROCESS.search(cmd))
        self.assertIsNone(G.GRAFT_PROCESS.search('python -I v13_graft.py fence'))

    def test_graft_root_barrier_and_completed_score_freeze(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            score = root / 'score'
            score.mkdir()
            (score / 'score.json').write_text('{"fixture":true}')
            try:
                G.freeze(score)
                with self.assertRaises(PermissionError):
                    (score / 'graft').mkdir()
                with self.assertRaises(PermissionError):
                    (score / 'score.json').write_text('changed')
                self.assertEqual((score / 'score.json').read_text(), '{"fixture":true}')
            finally:
                for p in [score, *score.rglob('*')]:
                    os.chflags(p, 0)
                    p.chmod(0o700 if p.is_dir() else 0o600)

    def test_graft_sweep_catches_late_cache_and_tracked_index(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            sb, fence = root / 'sandbox', root / 'fence'
            sb.mkdir(); fence.mkdir(); (fence / 'scorer_results').mkdir()
            for name in ('.gitignore', '.ignore'):
                (sb / name).write_text('/graft/\n')
            (sb / 'edit.py').write_text('harmless')
            (sb / 'runs').mkdir()
            subprocess.run(['/usr/bin/git', '-C', str(sb), 'init', '-q'], check=True)
            c = {'sandbox': str(sb), 'fence': str(fence), 'graft_ignore_sha256':
                 {n: C.digest(sb / n) for n in ('.gitignore', '.ignore')}}
            try:
                G.seal(c)
                self.assertEqual(G.sweep(c)['tracked_graft_cache'], 0)
                self.assertEqual(G.barrier_probe(c)['graft_directory_creation_denied'], 2)
                late = fence / 'scorer_results/graft'
                late.mkdir()
                with self.assertRaisesRegex(ValueError, 'artifact present'):
                    G.sweep(c)
                late.rmdir()
                # A tracked path is rejected even when its working-tree cache has gone.
                cache = sb / 'runs/graft/ask-index.json'
                cache.parent.mkdir(); cache.write_text('{}')
                subprocess.run(['/usr/bin/git', '-C', str(sb), 'add', '-f', str(cache)], check=True)
                cache.unlink(); cache.parent.rmdir()
                with self.assertRaisesRegex(ValueError, 'tracked'):
                    G.sweep(c)
            finally:
                for p in [sb, fence, *sb.rglob('*'), *fence.rglob('*')]:
                    if p.exists():
                        os.chflags(p, 0)
                        p.chmod(0o700 if p.is_dir() else 0o600)

    def test_absolute_fp16_payload_contract(self):
        half = lambda x: struct.unpack('e', struct.pack('e', x))[0]
        base, after = half(.5), half(.0001)
        delta = half(after - base)
        self.assertNotEqual(half(base + delta), after)
        # The runtime saves absolute values; the scorer copy restores after exactly.
        self.assertEqual(struct.pack('e', after), struct.pack('e', half(after)))
        runtime = (SRC / 'editor_runtime.py').read_text()
        scorer = (SRC / 'scorer.py').read_text()
        self.assertIn('w[n].detach().cpu().clone()', runtime)
        self.assertIn('w[n].copy_(t.to(w[n].device, w[n].dtype))', scorer)
        self.assertIn('weights_only=True', scorer)

    def test_scorer_measurement_and_setup_bodies_unchanged(self):
        old = subprocess.run(['/usr/bin/git', 'show',
                              '9feae02^:experiments/track_c/autoresearch_c10/prepare.py'],
                             text=True, capture_output=True, check=True).stdout
        def funcs(s):
            return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(s).body
                    if isinstance(n, ast.FunctionDef)}
        before, after = funcs(old), funcs((SRC / 'scorer.py').read_text())
        for name in ('_score', '_measure', '_frame_probe', '_fingerprint', '_reference_ok', '_law5', 'setup_checks'):
            self.assertEqual(before[name], after[name], name)

    def test_runtime_has_no_harness_or_scorer_import(self):
        tree = ast.parse((SRC / 'editor_runtime.py').read_text())
        names = []
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                names += [a.name for a in n.names]
            elif isinstance(n, ast.ImportFrom):
                names.append(n.module)
        self.assertFalse(any('c10e' in n or 'scorer' in n or 'prepare' in n for n in names if n))
        engine = SRC.parents[2] / 'code/memit/vendor'
        for f in engine.rglob('*.py'):
            text = f.read_text()
            self.assertNotIn('PTEST', text, str(f))
            self.assertNotIn('c10e_bandknob', text, str(f))

    def test_kill_refuses_changed_identity_without_signalling(self):
        with patch.object(C, 'identity', return_value='other'), patch.object(C.os, 'killpg') as kill:
            with self.assertRaises(ValueError):
                C.stop_stage({'pid': 987654, 'identity': 'expected'}, {})
            kill.assert_not_called()

    def test_kill_traverses_descendants_and_ignores_unrelated_jobs(self):
        dead = set()
        def command(argv, **kwargs):
            text = '100 1\n101 100\n102 101\n999 1\n' if argv[0] == '/bin/ps' else 'p0\nn/engine\n'
            return subprocess.CompletedProcess(argv, 0, stdout=text)
        def kill(pid, sig):
            if sig == 0 and pid in dead:
                raise ProcessLookupError()
            if sig in (signal.SIGTERM, signal.SIGKILL):
                dead.add(pid)
        def killgroup(pid, sig):
            dead.add(pid)
        c = {'sandbox': '/sandbox', 'engine': '/engine', 'fence': '/fence'}
        with patch.object(C, 'identity', side_effect=lambda p: 'born:' + str(p)), \
             patch.object(C.os, 'getpgid', return_value=100), \
             patch.object(C.subprocess, 'run', side_effect=command), \
             patch.object(C.os, 'kill', side_effect=kill) as singles, \
             patch.object(C.os, 'killpg', side_effect=killgroup) as groups:
            C.stop_stage({'pid': 100, 'identity': 'born:100'}, c)
        terminated = [v.args[0] for v in singles.call_args_list if v.args[1] == signal.SIGTERM]
        self.assertEqual(terminated, [102, 101])
        self.assertNotIn(999, [v.args[0] for v in singles.call_args_list])
        groups.assert_called_once_with(100, signal.SIGTERM)

    def test_policy_profiles_are_separate_and_parametrized(self):
        c = {'fence': '/fence', 'sandbox': '/sandbox', 'venv': '/venv', 'python_prefix': '/python',
             'python': '/python/bin/python3', 'graft_ignore_sha256': {'.ignore': 'fixture'},
             'program': '/program',
             'engine': '/engine', 'hf_home': '/hf', 'covariance': ['/cov'], 'fixture': False,
             'harness': '/program/harness.py', 'hparams': '/program/hp.json',
             'fingerprint': '/program/fingerprint.py', 'screens': ['/program/screen.json'],
             'editor_tmp': '/fence/editor_tmp', 'scorer_tmp': '/fence/scorer_tmp',
             'scorer_results': '/fence/scorer_results'}
        editor, scorer = P.seatbelt(c), P.seatbelt(c, True)
        for profile in (editor, scorer):
            self.assertIn('(deny network*)', profile)
            self.assertIn('(param "STAGE_TMP")', profile)
            self.assertIn('(param "RUN")', profile)
            self.assertIn('(deny mach-lookup', profile)
        self.assertNotIn('(literal "/program/harness.py")', editor)
        self.assertIn('(literal "/program/harness.py")', scorer)
        self.assertNotIn('(allow file-read* (subpath "/fence"))', editor)
        self.assertLess(scorer.index('(deny file-write* (subpath "/fence"))'),
                        scorer.index('(allow file-write* (subpath (param "RUN")))'))

    def test_gpu_gate_covers_new_and_busy_job_names(self):
        for name in ('editor_bootstrap.py', 'scorer.py', 'c10s_sharedz_sweep.py',
                     'check_equivalence.py', 'c10r_exp2_location_control.py'):
            self.assertIsNotNone(C.GPU_JOBS.search(name), name)

    def test_audit_missing_malformed_and_wrong_session_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'sealed/archive').mkdir(parents=True)
            harness = SRC.parents[2] / 'code/lab/track_c/c10e_bandknob.py'
            c = {'fence': str(root), 'sandbox': '/fixture', 'capture': '/capture',
                 'editor_tmp': '/edit_tmp', 'scorer_tmp': '/score_tmp', 'scorer_results': '/private',
                 'harness': str(harness), 'harness_sha256': C.digest(harness)}
            path = root / 'sealed/transcript.jsonl'
            b = {'fence': str(root), 'sandbox': '/fixture', 'captures': ['/capture', '/edit_tmp', '/score_tmp'],
                 'scorer_results': '/private', 'session_id': 'fixture-session', 'transcript': str(path)}
            with self.assertRaises(ValueError):
                A.scan_bound(c, b)
            path.write_text('{malformed\n')
            with self.assertRaises(ValueError):
                A.scan_bound(c, b)
            path.write_text('{"session_id":"other","type":"test"}\n')
            with self.assertRaises(ValueError):
                A.scan_bound(c, b)
            path.write_text('{"session_id":"fixture-session","type":"test"}\n')
            self.assertEqual(A.scan_bound(c, b), 1)
            b['captures'] = ['/foreign']
            with self.assertRaises(ValueError):
                A.scan_bound(c, b)

    def test_audit_checks_archives_from_all_sessions(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            archive = root / 'sealed/archive/run'
            archive.mkdir(parents=True)
            harness = SRC.parents[2] / 'code/lab/track_c/c10e_bandknob.py'
            c = {'fence': str(root), 'sandbox': '/fixture', 'capture': '/capture',
                 'editor_tmp': '/edit_tmp', 'scorer_tmp': '/score_tmp', 'scorer_results': '/private',
                 'harness': str(harness), 'harness_sha256': C.digest(harness)}
            path = root / 'sealed/transcript.jsonl'
            path.write_text('{"session_id":"new","type":"test"}\n')
            b = {'fence': str(root), 'sandbox': '/fixture', 'captures': ['/capture', '/edit_tmp', '/score_tmp'],
                 'scorer_results': '/private', 'session_id': 'new', 'transcript': str(path)}
            protected, _ = A.templates(c)
            # Protected scratch content is written only inside this fence's sealed area.
            recipe = archive / 'edit.py'
            recipe.write_text(repr(protected[0]))
            C.write_json(archive / 'identity.json', {'session_id': 'old', 'sha256': C.digest(recipe)})
            with self.assertRaises(ValueError):
                A.scan_bound(c, b)
            # TemporaryDirectory removes this protected scratch before returning.

    def test_parent_missing_watcher_records_a_latched_stop(self):
        source = (SRC / 'dispatch.py').read_text()
        fn = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'audit_ready')
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'sealed').mkdir()
            scope = {'FENCE': root, 'CONFIG': {'fence': str(root)}, 'read_json': C.read_json,
                     'identity': C.identity, 'Path': Path, 'time': __import__('time')}
            exec(compile(ast.Module(body=[fn], type_ignores=[]), 'dispatch-audit-unit', 'exec'), scope)
            with self.assertRaises(FileNotFoundError):
                scope['audit_ready']()
            self.assertEqual(C.read_json(root / 'sealed/STOP.json')['status'], 'HALTED')

    def test_inert_bootstrap_handoff_marker_precedes_recipe(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            run = root / 'run'
            run.mkdir()
            for name in ('fixture_editor_bootstrap.py', 'fixture_editor_runtime.py'):
                (root / name).write_text((SRC / name).read_text())
            C.write_json(root / 'train_facts.json', {'canon': 'canonical {}', 'subjects': ['fiction'],
                         'arms': {a: {'fiction': 'training'} for a in C.ARMS}})
            (run / 'edit.py').write_text("import os\nos.close(int(os.environ['C10_READY_FD']))\n"
                                        "from editor_runtime import evaluate\n"
                                        "evaluate(lambda facts: {'model.layers.4.mlp.down_proj.weight':[0.0001]})\n")
            rd, wr = os.pipe()
            started = time.monotonic()
            try:
                p = subprocess.Popen([sys.executable, '-I', '-B', str(root / 'fixture_editor_bootstrap.py')],
                                     env={'PATH': '/usr/bin:/bin', 'C10_RUN_DIR': str(run), 'C10_READY_FD': str(wr)},
                                     pass_fds=(wr,), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                os.close(wr)
                packet = os.read(rd, 8)
                stdout, stderr = p.communicate(timeout=10)
                self.assertEqual(p.returncode, 0, stderr.decode())
                self.assertEqual(len(packet), 8)
                stamp = struct.unpack('!d', packet)[0]
                self.assertLessEqual(started, stamp)
                self.assertLessEqual(stamp, time.monotonic())
                C.validate_handoff(run)
            finally:
                os.close(rd)


if __name__ == '__main__':
    unittest.main(verbosity=2)
