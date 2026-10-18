"""Caller-owned roots and observations at the real moves CLI boundary."""
import errno
import fcntl
import json
import os
import subprocess
import sys
import unittest

import fault_kit as FK
from test_icm21_moves_cli import MovesCase, SCRIPT, CODE, dumps, named


class CallerInputs(MovesCase):
    def setUp(self):
        super().setUp()
        self.fx.entry['roots'] = {
            'sources': [move['source'] for move in self.fx.moves],
            'targets': [move['target'] for move in self.fx.moves]}
        self.fx.entry.pop('run_units', None)
        self.fx.publish()
        self.runs = self.fx.path('run-units.json')
        self.runs.write_bytes(dumps([]))

    def argv(self, stage='pre', roots=True, runs=True):
        argv = self.fx.argv(stage)
        # [LAW:one-source-of-truth] Each case supplies its own caller evidence.
        for flag in ('--admitted-root', '--run-units'):
            while flag in argv:
                index = argv.index(flag)
                del argv[index:index + 2]
        if roots:
            argv += ['--admitted-root', str(self.fx.root)]
        if runs:
            argv += ['--run-units', str(self.runs)]
        return argv

    def refusal(self, argv, path, reason):
        code, result = self.main(argv)
        self.assertEqual(code, 2, result)
        self.assertEqual(sorted(result), ['reason', 'status'])
        self.assertEqual(result['status'], 'UNVERIFIED')
        self.assertIn(str(path), result['reason'])
        self.assertIn(reason, result['reason'])

    def test_build_plan_shape_passes(self):
        self.assertEqual(self.main(self.argv()), (0, {
            'status': 'PASS', 'stage': 'pre', 'entry': 'E-1', 'findings': []}))

    def test_missing_admitted_root_refuses(self):
        self.refusal(self.argv(roots=False), '--admitted-root', 'required')

    def test_post_refuses_admitted_root(self):
        self.refusal(self.argv('post', runs=False), '--admitted-root', 'refused')

    def test_post_refuses_run_units(self):
        self.refusal(self.argv('post', roots=False), '--run-units', 'refused')

    def test_non_list_run_units_refuses(self):
        for value in ({}, None, 'path', 3, True):
            with self.subTest(value=value):
                self.runs.write_bytes(dumps(value))
                self.refusal(self.argv(), self.runs, 'list of path strings')

    def test_non_string_run_unit_refuses(self):
        for value in (None, 3, {}, [], True):
            with self.subTest(value=value):
                self.runs.write_bytes(dumps([str(self.fx.root), value]))
                self.refusal(self.argv(), self.runs, 'list of path strings')

    def test_run_unit_around_source_fails(self):
        self.runs.write_bytes(dumps([str(self.fx.root)]))
        code, result = self.main(self.argv())
        self.assertEqual(code, 1, result)
        self.assertIn('move splits run unit ' + str(self.fx.root), self.reasons(result))

    def test_missing_run_units_stays_unverified(self):
        self.fx.entry['run_units'] = []
        self.fx.publish()
        code, result = self.main(self.argv(runs=False))
        self.assertEqual(code, 2, result)
        self.assertEqual(set(self.reasons(result)),
                         {'run_units not supplied: run splitting unchecked'})

    def test_entry_observations_cannot_override_caller(self):
        self.fx.entry['run_units'] = [str(self.fx.root)]
        self.fx.publish()
        self.assertEqual(self.main(self.argv())[0], 0)

    def test_repeated_roots_are_all_used(self):
        argv = self.argv(roots=False)
        argv += ['--admitted-root', str(self.fx.decoy),
                 '--admitted-root', str(self.fx.root)]
        self.assertEqual(self.main(argv)[0], 0)

    def test_caller_root_restriction_fails(self):
        argv = self.argv(roots=False)
        argv += ['--admitted-root', str(self.fx.decoy)]
        code, result = self.main(argv)
        self.assertEqual(code, 1, result)
        self.assertIn('target escapes every admitted root: ' + self.fx.moves[0]['target'],
                      self.reasons(result))

    def test_run_units_fifo_refuses_under_timeout(self):
        with FK.fifo_in_place(self.runs, timeout=3):
            self.refusal(self.argv(), self.runs, 'is not a regular file')

    def test_run_units_symlink_swap_refuses(self):
        with FK.swap_for_symlink('open', 1, self.runs, self.fx.decoy / 'file',
                                 match=named(self.runs.name)):
            self.refusal(self.argv(), self.runs, '[ELOOP]')

    def test_run_units_open_eio_refuses(self):
        with FK.inject_oserror('open', 1, errno.EIO, match=named(self.runs.name)):
            self.refusal(self.argv(), self.runs, '[EIO]')

    def test_run_units_read_eio_refuses(self):
        def run_fd(fd, *args):
            return os.fsdecode(fcntl.fcntl(fd, fcntl.F_GETPATH, bytes(1024))
                               .split(b'\0', 1)[0]) == str(self.runs)
        with FK.inject_oserror('read', 1, errno.EIO, match=run_fd):
            self.refusal(self.argv(), self.runs, '[EIO]')

    def test_script_pass_and_refusal(self):
        environment = dict(os.environ, PYTHONPATH=str(CODE), PYTHONDONTWRITEBYTECODE='1')
        for roots, expected in ((True, 0), (False, 2)):
            done = subprocess.run([sys.executable, '-B', str(SCRIPT)] + self.argv(roots=roots),
                                  capture_output=True, env=environment, timeout=30)
            self.assertEqual(done.returncode, expected, done.stderr)
            self.assertEqual(done.stderr, b'')
            self.assertEqual(done.stdout.count(b'\n'), 1)
            self.assertEqual(json.loads(done.stdout)['status'],
                             'PASS' if roots else 'UNVERIFIED')


if __name__ == '__main__':
    unittest.main()
