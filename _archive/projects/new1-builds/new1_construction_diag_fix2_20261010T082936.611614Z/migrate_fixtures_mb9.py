"""Fixture migration only; retain each original test method and its behavior."""
from pathlib import Path
import ast

def replace_method(source, name, body):
    start = source.index('    def ' + name + '(')
    end = source.find('\n    def ', start+1)
    class_end = source.find('\nclass ', start+1)
    main = source.find("\nif __name__", start+1)
    end = min(p for p in (end, class_end, main, len(source)) if p >= 0)
    return source[:start] + body.rstrip() + '\n\n' + source[end:].lstrip('\n')

identity = Path('tests/test_new1_identity_diag.py')
source = identity.read_text()
source = replace_method(source, 'test_keyboard_interrupt_after_dispatch_cannot_leave_worker_alive', '''    def test_keyboard_interrupt_after_dispatch_cannot_leave_worker_alive(self):
        seen, owners = [], []
        original = self.D.OwnedWorker.start
        def capture(owner, *args):
            owners.append(owner); return original(owner, *args)
        def interrupted(pid):
            if pid:
                seen.append(pid)
                raise KeyboardInterrupt('fixture interrupt')
            return {'rss_gib': .1, 'process_count': 1}
        with mock.patch.object(self.D.OwnedWorker, 'start', new=capture):
            try:
                status, _, result = self.run_fixture('import time; time.sleep(30)', monitor=interrupted, seconds=.2)
            except KeyboardInterrupt:
                self.fail('the interrupted diagnostic left cleanup to its caller')
        self.assertNotEqual(status, 0)
        self.assertEqual(result['status'], 'INVALID')
        self.assertEqual(len(seen), 1)
        with self.assertRaises(ProcessLookupError): os.kill(seen[0], 0)
        self.assertIsNotNone(owners[0].returncode)
        self.assertEqual(owners[0].proof['pid'], seen[0])
        self.assertTrue(all(fd is None for pair in owners[0].channels.values() for fd in pair))
''')
source = replace_method(source, 'test_worker_cleanup_timeout_is_attempted_once_and_preserves_original_error', '''    def test_worker_cleanup_timeout_is_attempted_once_and_preserves_original_error(self):
        owners = []
        original_start = self.D.OwnedWorker.start
        original_kill = self.D.kill_worker
        def capture(owner, *args):
            owners.append(owner); return original_start(owner, *args)
        def delayed_kill(pid):
            time.sleep(.08)
            return original_kill(pid)
        def failing_monitor(pid):
            if pid: raise self.D.G.Invalid('fixture original diagnostic error')
            return {'rss_gib': .1, 'process_count': 1}
        start = time.monotonic()
        with mock.patch.object(self.D.OwnedWorker, 'start', new=capture), \\
             mock.patch.object(self.D, 'kill_worker', new=delayed_kill), \\
             mock.patch.object(self.D, 'CLEANUP_S', .05):
            try:
                status, _, result = self.run_fixture('import time; time.sleep(30)', monitor=failing_monitor, seconds=1)
            except self.D.S.Stop as error:
                self.fail('cleanup error replaced the original error and skipped its receipt: ' + str(error))
        self.assertNotEqual(status, 0)
        self.assertEqual(result['error'], 'fixture original diagnostic error')
        self.assertIn('STOPPED-DEADLINE', result['cleanup_error'])
        self.assertEqual(owners[0].proof['kills'], 1, 'worker group killed exactly once')
        self.assertEqual(owners[0].proof['pid'], result['worker_pid'])
        self.assertIsNotNone(owners[0].returncode, 'guardian reaped before terminal return')
        with self.assertRaises(ChildProcessError): os.waitpid(owners[0].pid, os.WNOHANG)
        with self.assertRaises(ProcessLookupError): os.kill(result['worker_pid'], 0)
        self.assertLess(time.monotonic() - start, .2)
        self.assertTrue(all(fd is None for pair in owners[0].channels.values() for fd in pair))
''')
assert sum(n.name.startswith('test_') for n in ast.walk(ast.parse(source)) if isinstance(n, ast.FunctionDef)) == 27
identity.write_text(source)

construction = Path('tests/test_new1_construction_diag.py')
source = construction.read_text()
source = replace_method(source, 'reap_fixture', '''    @contextlib.contextmanager
    def owned_fixture(self, delay=0, interrupt=False):
        owners = []; original = self.D.I.OwnedWorker.start
        def start(owner, *args):
            owners.append(owner); original(owner, *args)
            if interrupt: os.kill(os.getpid(), signal.SIGINT)
            if delay: time.sleep(delay)
        with mock.patch.object(self.D.I.OwnedWorker, 'start', new=start):
            yield owners
        for owner in owners:
            self.assertIsNotNone(owner.returncode, 'guardian not reaped before terminal return')
            self.assertIsNotNone(owner.proof, 'worker reaping proof missing')
            with self.assertRaises(ChildProcessError): os.waitpid(owner.pid, os.WNOHANG)
            with self.assertRaises(ProcessLookupError): os.kill(owner.worker_pid, 0)
            self.assertTrue(all(fd is None for pair in owner.channels.values() for fd in pair))

    def reap_fixture(self, children):
        for child in children:
            if child.poll() is None: os.killpg(child.pid, signal.SIGKILL)
            child.communicate(timeout=1)
''')
replacements = {
'test_real_watchdog_late_popen_handle_is_owned_killed_and_reaped': '''    def test_real_watchdog_late_popen_handle_is_owned_killed_and_reaped(self):
        with tempfile.TemporaryDirectory() as temp, self.owned_fixture(delay=.2) as owners:
            directory = self.D.new_directory(Path(temp))
            status, result = self.run_fixture([sys.executable, '-B', '-c', 'import time;time.sleep(30)'], directory, seconds=.05)
            self.assertEqual(status, 2)
            self.assertIn('STOPPED-DEADLINE', result['error'])
            self.assertEqual(len(owners), 1)
            with self.assertRaises(ProcessLookupError): os.kill(owners[0].worker_pid, 0)
            self.assertEqual(result['worker_pid'], owners[0].worker_pid)
''',
'test_deadline_during_registration_never_releases_worker_arithmetic': '''    def test_deadline_during_registration_never_releases_worker_arithmetic(self):
        with tempfile.TemporaryDirectory() as temp, self.owned_fixture(delay=.2) as owners:
            marker = Path(temp)/'arithmetic'; directory = self.D.new_directory(Path(temp)/'runs')
            status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)], directory, seconds=.05)
            self.assertEqual(status, 2)
            self.assertFalse(marker.exists())
            with self.assertRaises(ProcessLookupError): os.kill(owners[0].worker_pid, 0)
''',
'test_launch_has_its_own_bound_while_whole_run_budget_remains': '''    def test_launch_has_its_own_bound_while_whole_run_budget_remains(self):
        with tempfile.TemporaryDirectory() as temp, self.owned_fixture(delay=.2) as owners:
            marker = Path(temp)/'arithmetic'; directory = self.D.new_directory(Path(temp)/'runs')
            with mock.patch.object(self.D.I, 'LAUNCH_S', .05):
                status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)], directory, seconds=2)
            self.assertEqual(status, 2)
            self.assertIn('STOPPED-LAUNCH', result['error'])
            self.assertFalse(marker.exists())
            with self.assertRaises(ProcessLookupError): os.kill(owners[0].worker_pid, 0)
''',
'test_worker_exits_promptly_when_release_never_arrives_or_pipe_closes': '''    def test_worker_exits_promptly_when_release_never_arrives_or_pipe_closes(self):
        for close in (False, True):
            with self.subTest(close=close), tempfile.TemporaryDirectory() as temp:
                marker = Path(temp)/'arithmetic'; end = time.monotonic()+.15
                owner = self.D.I.OwnedWorker(end)
                owner.start([sys.executable, '-B', '-c', self.gated_fixture(marker)], time.monotonic()+1)
                try:
                    if close: owner.close_fd('auth', 1); owner.close_fd('release', 1)
                    limit = time.monotonic()+1
                    while (owner.proof is None or owner.returncode is None or owner.streams) and time.monotonic()<limit:
                        owner.step(.005)
                    self.assertIsNotNone(owner.proof)
                    self.assertNotEqual(owner.proof['code'], 0)
                    self.assertFalse(marker.exists())
                    self.assertIn(b'LAUNCH', owner.buffers['stderr'])
                finally: owner.request_stop(); owner.close()
''',
'test_worker_exits_on_parent_death_even_with_another_writer_open': '''    def test_worker_exits_on_parent_death_even_with_another_writer_open(self):
        self.assertTrue(hasattr(self.D.I, 'wait_for_release'), 'worker release/liveness guard missing')
        with tempfile.TemporaryDirectory() as temp:
            marker = Path(temp)/'arithmetic'
            code = self.gated_fixture(marker)
            parent_code = ('import os,sys,time,json;from tools import new1_identity_diag as I;'
                'end=time.monotonic()+4;owner=I.OwnedWorker(end);'
                f'owner.start([sys.executable,"-B","-c",{code!r}],end+1);'
                '\\nwhile not owner.ready:owner.step(.005)\\n'
                'keeper=os.fork();'
                '\\nif keeper==0:\\n os.close(1);os.close(2);time.sleep(.8);os._exit(0)\\n'
                'print(json.dumps({"worker":owner.worker_pid,"keeper":keeper}),flush=True);time.sleep(.2);'
                'assert owner.proof is None,"worker exited before parent death"')
            parent = subprocess.Popen([sys.executable, '-B', '-c', parent_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = parent.communicate(timeout=2)
            self.assertEqual(parent.returncode, 0, stderr)
            value = json.loads(stdout); os.kill(value['keeper'], 0)
            limit = time.monotonic()+.5
            while time.monotonic()<limit:
                try: os.kill(value['worker'], 0)
                except ProcessLookupError: break
                time.sleep(.005)
            with self.assertRaises(ProcessLookupError): os.kill(value['worker'], 0)
            self.assertFalse(marker.exists())
''',
'test_keyboard_interrupt_during_popen_registration_cleans_without_release': '''    def test_keyboard_interrupt_during_popen_registration_cleans_without_release(self):
        previous = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, signal.default_int_handler)
        try:
            with tempfile.TemporaryDirectory() as temp, self.owned_fixture(interrupt=True) as owners:
                marker = Path(temp)/'arithmetic'; directory = self.D.new_directory(Path(temp)/'runs')
                status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)], directory, seconds=2)
                self.assertEqual(status, 130)
                self.assertFalse(marker.exists())
                with self.assertRaises(ProcessLookupError): os.kill(owners[0].worker_pid, 0)
        finally: signal.signal(signal.SIGINT, previous)
''',
'test_stalled_launch_returns_within_bound_and_late_handle_cleans_once': '''    def test_stalled_launch_returns_within_bound_and_late_handle_cleans_once(self):
        with tempfile.TemporaryDirectory() as temp, self.owned_fixture(delay=2) as owners:
            marker = Path(temp)/'arithmetic'; directory = self.D.new_directory(Path(temp)/'runs')
            start = time.monotonic()
            with mock.patch.object(self.D.I, 'LAUNCH_S', .05), mock.patch.object(self.D.I, 'CLEANUP_S', .05):
                status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)], directory, seconds=.8)
            self.assertEqual(status, 2)
            self.assertIn('STOPPED-LAUNCH', result['error'])
            self.assertLess(time.monotonic()-start, .3)
            self.assertFalse(marker.exists())
            self.assertEqual(owners[0].proof['kills'], 1)
            self.assertIsNotNone(owners[0].returncode)
            self.assertTrue(all(fd is None for pair in owners[0].channels.values() for fd in pair))
''',
'test_already_exited_unreleased_worker_is_reaped_without_group_signal': '''    def test_already_exited_unreleased_worker_is_reaped_without_group_signal(self):
        with tempfile.TemporaryDirectory() as temp, self.owned_fixture() as owners:
            marker = Path(temp)/'arithmetic'; directory = self.D.new_directory(Path(temp)/'runs')
            with mock.patch.object(self.D.I, 'release_frame', return_value=b'bad'):
                status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)], directory, seconds=1)
            self.assertEqual(status, 2)
            self.assertEqual(owners[0].proof['code'], 2)
            self.assertEqual(owners[0].proof['kills'], 0, 'already exited worker must be reaped without signalling its group')
            self.assertFalse(marker.exists())
            with self.assertRaises(ProcessLookupError): os.kill(owners[0].worker_pid, 0)
''',
'test_released_worker_exits_on_parent_death_while_main_is_blocked': '''    def test_released_worker_exits_on_parent_death_while_main_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            marker = Path(temp)/'released'
            worker = ('import time;from pathlib import Path;from tools import new1_identity_diag as I;'
                'I.wait_for_release();' + f'Path({str(marker)!r}).write_text("released");time.sleep(5)')
            parent_code = ('import sys,time;from pathlib import Path;from tools import new1_identity_diag as I;'
                'end=time.monotonic()+3;owner=I.OwnedWorker(end);'
                f'owner.start([sys.executable,"-B","-c",{worker!r}],end+1);'
                '\\nwhile not owner.ready:owner.step(.005)\\n'
                'owner.release();print(owner.worker_pid,flush=True);limit=time.monotonic()+1;'
                f'\\nwhile not Path({str(marker)!r}).exists() and time.monotonic()<limit:time.sleep(.005)\\n'
                f'assert Path({str(marker)!r}).exists(),"worker never received release"')
            parent = subprocess.Popen([sys.executable, '-B', '-c', parent_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = parent.communicate(timeout=2)
            self.assertEqual(parent.returncode, 0, stderr)
            self.assertEqual(marker.read_text(), 'released')
            pid = int(stdout); limit = time.monotonic()+.5
            while time.monotonic()<limit:
                try: os.kill(pid, 0)
                except ProcessLookupError: break
                time.sleep(.005)
            with self.assertRaises(ProcessLookupError): os.kill(pid, 0)
''',
'test_released_worker_has_independent_whole_deadline_while_main_is_blocked': '''    def test_released_worker_has_independent_whole_deadline_while_main_is_blocked(self):
        end = time.monotonic()+.3; owner = self.D.I.OwnedWorker(end)
        code = ('import time;from tools import new1_identity_diag as I;I.wait_for_release();'
                'print("RELEASED",flush=True);time.sleep(5)')
        owner.start([sys.executable, '-B', '-c', code], end)
        try:
            while not owner.ready: owner.step(.005)
            owner.release()
            while owner.proof is None or owner.returncode is None or owner.streams: owner.step(.005)
            self.assertEqual(bytes(owner.buffers['stdout']).strip(), b'RELEASED')
            self.assertEqual(owner.proof['code'], -signal.SIGKILL)
            self.assertEqual(owner.proof['kills'], 1)
        finally: owner.close()
'''}
for name, body in replacements.items(): source = replace_method(source, name, body)
# Strengthen the saved four reproductions with ownership proofs; preserve their names.
source = source.replace("children = []; original = self.I.subprocess.Popen; injected = []", "owners = []; original = self.I.OwnedWorker.start; injected = []")
source = source.replace("def capture(*args, **kwargs):\n            child = original(*args, **kwargs); children.append(child); return child", "def capture(owner, *args):\n            owners.append(owner); return original(owner, *args)")
source = source.replace("mock.patch.object(self.I.subprocess, 'Popen', new=capture)", "mock.patch.object(self.I.OwnedWorker, 'start', new=capture)")
source = source.replace("                if children:\n                    self.assertIsNotNone(children[0].returncode, 'child was not reaped before terminal return')", "                self.assertIsNotNone(owners[0].returncode, 'guardian was not reaped before terminal return')\n                self.assertEqual(owners[0].proof['pid'], result['worker_pid'])\n                with self.assertRaises(ChildProcessError): os.waitpid(owners[0].pid, os.WNOHANG)")
source = source.replace("            for child in children:\n                if child.poll() is None: os.killpg(child.pid, signal.SIGKILL)\n                child.communicate(timeout=1)\n\n    def test_r2_stalled", "\n    def test_r2_stalled")
construction.write_text(source)
