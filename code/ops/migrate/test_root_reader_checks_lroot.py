"""T430: sibling ROOT authority, exit status, and bounded reader commands."""
import csv
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from ops.migrate import root_reader_checks as checks, root_switch
import test_root_switch as switch_tests


class LRootChecks(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.root = str(self.base / 'root')
        self.old = str(self.base / 'old')
        self.home = str(self.base / 'home')
        self.root_file = self.base / 'ROOT'
        self.script = self.base / 'suite.sh'
        self.text = '#!/bin/zsh\n: "${0:A:h}/ROOT"\n'
        self.calls = []

    def run_suite(self, kind, body='exit 0\n', runner=checks.run_command):
        self.script.write_text(self.text + body)

        def record(command):
            self.calls.append(command)
            return runner(command)

        return checks.perform(checks.Probe(kind, str(self.script)), checks.Effects(record),
                              self.root, self.old, self.home)

    def next_action(self, kind, observations):
        return checks.advance(checks.Probe(kind, str(self.script)), observations,
                              self.root, self.old, self.home)

    def valid_reads(self):
        return (checks.File(self.text.encode(), 0o644),
                checks.File((self.root + '\n').encode(), 0o644))

    def reject_root(self, content):
        self.root_file.write_bytes(content)
        for kind in ('test-ship', 'test-train'):
            with self.subTest(kind=kind):
                result = self.run_suite(kind)
                self.assertEqual(result.status, 'FAIL')
                self.assertIn(str(self.root_file), result.detail)
                self.assertEqual(self.calls, [])
        return result

    def test_wrong_root_never_runs(self):
        result = self.reject_root((self.old + '\n').encode())
        self.assertIn(self.old, result.detail)

    def test_two_lines_never_run(self):
        self.reject_root((self.root + '\nextra\n').encode())

    def test_missing_newline_never_runs(self):
        self.reject_root(self.root.encode())

    def test_non_utf8_root_names_path(self):
        self.reject_root(b'\xff')

    def test_root_content_detail_is_bounded(self):
        result = self.reject_root(b'x' * 201 + b'END')
        self.assertIn('x' * 200, result.detail)
        self.assertNotIn('x' * 201, result.detail)
        self.assertNotIn('END', result.detail)

    def test_missing_root_never_runs(self):
        for kind in ('test-ship', 'test-train'):
            with self.subTest(kind=kind):
                result = self.run_suite(kind)
                self.assertEqual(result.status, 'UNAVAILABLE')
                self.assertIn(str(self.root_file), result.detail)
                self.assertEqual(self.calls, [])

    def test_non_utf8_script_never_runs(self):
        for kind in ('test-ship', 'test-train'):
            with self.subTest(kind=kind):
                result = self.next_action(kind, (checks.File(self.text.encode() + b'#\xff', 0o644),))
                self.assertIsInstance(result, checks.Result)
                self.assertEqual(result.status, 'FAIL')

    def test_unencodable_expected_root_surfaces(self):
        for kind in ('test-ship', 'test-train'):
            with self.subTest(kind=kind), self.assertRaises(UnicodeEncodeError):
                checks.advance(checks.Probe(kind, str(self.script)), self.valid_reads(),
                               '/bad\ud800', self.old, self.home)

    def test_runner_unexpected_exception_surfaces(self):
        with patch.object(checks.subprocess, 'run', side_effect=RuntimeError('unexpected runner error')):
            with self.assertRaisesRegex(RuntimeError, 'unexpected runner error'):
                checks.run_command(checks.Command(('fixture',), ()))

    def test_ambient_l_root_file_is_overridden(self):
        self.root_file.write_text(self.root + '\n')
        ambient = self.base / 'ambient'
        ambient.write_text(self.old + '\n')
        for kind in ('test-ship', 'test-train'):
            with self.subTest(kind=kind), patch.dict(os.environ, L_ROOT_FILE=str(ambient)):
                result = self.run_suite(kind, 'printf "%s" "$L_ROOT_FILE"\n')
                self.assertEqual(result, checks.Result('PASS', 'exit 0: ' + str(self.root_file)))
                self.assertEqual(dict(self.calls[-1].env)['L_ROOT_FILE'], str(self.root_file))

    def test_subprocess_exit_statuses(self):
        self.root_file.write_text(self.root + '\n')
        for kind in ('test-ship', 'test-train'):
            for code, body in ((0, 'exit 0'), (1, 'exit 1'), (2, 'exit 2'), (-15, 'kill -TERM $$')):
                with self.subTest(kind=kind, code=code):
                    result = self.run_suite(kind, body + '\n')
                    self.assertEqual(result.status, 'PASS' if code == 0 else 'FAIL')
                    self.assertIn('exit ' + str(code) + ':', result.detail)

    def test_status_depends_only_on_returncode(self):
        # [LAW:behavior-not-structure] Cross the status domain with misleading output.
        for kind in ('test-ship', 'test-train'):
            for code in range(-64, 256):
                for data in (b'', b'x', b'PASS case_a\n', b'FAIL case_b\n', b'OK\n',
                             b'Ran 1 test in 0.1s\n\nOK\n', b'0 failed\n'):
                    with self.subTest(kind=kind, code=code, data=data):
                        result = self.next_action(kind, self.valid_reads() + (checks.Output(code, data),))
                        self.assertEqual(result.status, 'PASS' if code == 0 else 'FAIL')
                        self.assertEqual(result.detail, 'exit ' + str(code) + ': ' + data.decode())

    def test_comment_is_not_override(self):
        self.root_file.write_text(self.root + '\n')
        self.text = '#!/bin/zsh\n  # ${0:A:h}/ROOT\n'
        for kind in ('test-ship', 'test-train'):
            with self.subTest(kind=kind):
                result = self.run_suite(kind)
                self.assertEqual(result, checks.Result('UNAVAILABLE', 'no ROOT override in ' + str(self.script)))
                self.assertEqual(self.calls, [])

    def test_env_root_forms_are_not_override(self):
        self.root_file.write_text(self.root + '\n')
        for form in ('${ROOT:-/old}', '${ROOT}', '${ROOT:?}', '$ROOT/', '$ROOT"', '$ROOT '):
            self.text = '#!/bin/zsh\n: ' + form + '\n'
            for kind in ('test-ship', 'test-train'):
                with self.subTest(kind=kind, form=form):
                    result = self.run_suite(kind)
                    self.assertEqual(result.status, 'UNAVAILABLE')
                    self.assertEqual(self.calls, [])

    def test_commands_have_timeout_and_no_root_env(self):
        cases = [('test-ship', self.valid_reads(), 600), ('test-train', self.valid_reads(), 600),
                 ('plist', (checks.File(b'<plist/>', 0o644),), 10),
                 ('shell-syntax', self.valid_reads()[:1], 10),
                 ('venv-prefix', (), 10), ('console-version', (), 10), ('lane-status', (), 10)]
        for kind, observations, timeout in cases:
            with self.subTest(kind=kind):
                command = self.next_action(kind, observations)
                self.assertIsInstance(command, checks.Command)
                self.assertEqual(command.timeout, timeout)
                self.assertNotIn('ROOT', dict(command.env))
                expected = {'HOME': self.home, 'PYTHONDONTWRITEBYTECODE': '1', 'GIT_OPTIONAL_LOCKS': '0'}
                if kind in ('test-ship', 'test-train'):
                    expected['L_ROOT_FILE'] = str(self.root_file)
                self.assertEqual(dict(command.env), expected)

    def test_standalone_timeout_is_unavailable(self):
        command = checks.Command((sys.executable, '-B', '-c', 'import time; time.sleep(2)'), (), timeout=1)
        def advance(probe, observations, root, old, home):
            return command if not observations else checks.Result('PASS', 'finished')
        with patch.object(checks, 'advance', advance):
            result = checks.perform(checks.Probe('test-ship', str(self.script)),
                                    checks.Effects(checks.run_command), self.root, self.old, self.home)
        self.assertEqual(result.status, 'UNAVAILABLE')
        self.assertIn('ETIMEDOUT', result.detail)
        self.assertIn('1 s', result.detail)
        self.assertIn(sys.executable, result.detail)

    def test_fourth_effect_raises(self):
        effects = []
        def observe(action):
            effects.append(action)
            return checks.File(b'', 0)
        with patch.object(checks, 'advance', return_value=checks.Read(str(self.script))):
            with self.assertRaisesRegex(RuntimeError, 'three observations'):
                checks.perform(checks.Probe('test-ship', str(self.script)),
                               observe, self.root, self.old, self.home)
        self.assertEqual(len(effects), 3)

    def test_switch_reader_checks_forward_timeouts(self):
        fixture = switch_tests.RootSwitchTests()
        self.addCleanup(fixture.doCleanups)
        fixture.setUp()
        tools = fixture.base / 'tools'
        (tools / 'ROOT').write_text(str(fixture.r) + '\n')
        for kind in ('test-ship', 'test-train'):
            script = tools / (kind + '.sh')
            script.write_text(self.text + 'exit 0\n')
            script.chmod(0o755)
            fixture.rows.append(('CHECK', str(script), kind))
        with fixture.registry.open('w', newline='') as stream:
            csv.writer(stream, delimiter='\t', lineterminator='\n').writerows(fixture.rows)
        fixture.config['reader_commands']['zsh'] = ['zsh']
        with patch.object(root_switch, '_command', wraps=root_switch._command) as command:
            code, text = fixture.call()
        self.assertEqual(code, 0, text)
        self.assertIn('READER_CHECKS', text)
        for kind in ('test-ship', 'test-train'):
            calls = [call for call in command.call_args_list if call.args[0][-1] == str(tools / (kind + '.sh'))]
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0].kwargs.get('timeout'), 600)
        plutil = [call for call in command.call_args_list if call.args[0][-2:] == ('-lint', '-')]
        self.assertEqual(len(plutil), 1)
        self.assertEqual(plutil[0].kwargs.get('timeout'), 10)


class MovedParentChecks(unittest.TestCase):
    def attack(self, kind, filename):
        import errno
        import io
        import json
        import fault_kit

        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        base = Path(temporary.name).resolve()
        root = base / 'unit'
        tools = root / 'tools'
        tools.mkdir(parents=True)
        marker = base / 'suite-ran'
        script = tools / 'suite.sh'
        script.write_text("#!/bin/bash\n: '${0:A:h}/ROOT'\nprintf ran > " + str(marker) + "\n")
        (tools / 'ROOT').write_text(str(root) + '\n')
        (tools / 'project.json').write_text(json.dumps({'projects': {str(root): {}}}))
        lane = root / 'lane'
        lane.mkdir()
        (lane / '.git').write_text('gitdir: ' + str(tools) + '\n')
        (tools / 'gitdir').write_text(str(lane / '.git') + '\n')
        probe = script if kind in ('test-ship', 'test-train') else tools / filename
        target = tools / filename
        registry = base / 'registry'
        registry.write_text('CHECK\t' + str(probe.relative_to(root)) + '\t' + kind + '\n')
        out = base / 'receipt'
        outside = base / 'displaced-tools'
        real_read = os.read
        live = checks.fdsafe.live_path
        reads = []
        fault = None

        def match(fd, *args, **kwargs):
            try:
                return live(fd, str(target)) == str(target)
            except checks.fdsafe.Refusal as exc:
                if exc.errno == errno.EBADF:
                    return False
                raise

        def observe_read(fd, count):
            # [LAW:behavior-not-structure] Prove bytes came from outside the unit.
            if fault is not None and fault.parked is not None and not reads:
                os.rename(fault.parked, outside)
                location = live(fd, str(target))
                data = real_read(fd, count)
                reads.append((location, data))
                return data
            return real_read(fd, count)

        with patch.object(os, 'read', observe_read):
            with fault_kit.rename_and_rebind('read', 1, tools, match=match) as fault:
                code = checks.main(['--root', str(root), '--old-root', str(base / 'old'),
                                    '--registry', str(registry), '--out', str(out)],
                                   home=str(base), stderr=io.StringIO())
        self.assertEqual(fault.fired, 1)
        self.assertEqual(len(reads), 1)
        self.assertFalse(checks.fdsafe.inside(str(root), reads[0][0]))
        self.assertTrue(reads[0][1])
        rows = list(csv.DictReader(io.StringIO(out.read_text()), delimiter='\t'))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['status'], 'UNAVAILABLE')
        self.assertIn('ESTALE', rows[0]['detail'])
        self.assertNotEqual(code, 0)
        self.assertFalse(marker.exists())

    def test_root_ship_moved_outside(self):
        self.attack('test-ship', 'ROOT')

    def test_root_train_moved_outside(self):
        self.attack('test-train', 'ROOT')

    def test_script_moved_outside(self):
        self.attack('test-ship', 'suite.sh')

    def test_claude_project_moved_outside(self):
        self.attack('claude-project', 'project.json')

    def test_gitdir_moved_outside(self):
        self.attack('gitdir', 'gitdir')


if __name__ == '__main__':
    unittest.main()
