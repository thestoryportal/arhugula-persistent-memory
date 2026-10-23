"""Fresh-process recovery fixtures; commands never reach deployment paths."""
import json
import contextlib
import io
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import unittest
from hashlib import sha256
from unittest.mock import patch

import fault_kit

from ops.migrate import switch_exec, switch_effects, switch_journal_core as journal
from ops.migrate import switch_recover, fdsafe
from ops.migrate.root_switch_core import (
    Absent, BackupPair, BackupRun, FileState, Install, Launchd, Quiesce, Rename, Replace,
)


def command(root, kind):
    return (sys.executable, '-B', str(Path(__file__).resolve()), '--fake', str(root), kind)


def effects(root, action):
    if isinstance(action, Launchd):
        return dict(command=command(root, 'agent'), domain='fixture', service='agent',
                    plist=str(root / 'agent.plist'))
    if isinstance(action, Quiesce):
        return dict(command=command(root, 'processes'), clock=lambda: 0,
                    sleep=lambda seconds: None, timeout=0, interval=1)
    if isinstance(action, (BackupRun, journal.ResyncP)):
        table = root / ('forward.tsv' if isinstance(action, BackupRun) else 'inverse.tsv')
        return dict(command=command(root, 'backup'), table=str(table),
                    env=dict(os.environ, FIXTURE_ROOT=str(root)), timeout=5)
    if isinstance(action, journal.BackupCompare):
        return dict(displaced=((str(root / 'D'), 'repo/file', sha256(b'start').hexdigest()),))
    raise AssertionError(action)


def fake(root, kind, argv):
    root = root.resolve(strict=True)
    if kind == 'agent':
        expected = {'print': ['fixture/agent'], 'bootout': ['fixture/agent'],
                    'bootstrap': ['fixture', str(root / 'agent.plist')]}
        assert argv[1:] == expected[argv[0]], argv
        state = root / 'agent'
        if argv[0] == 'print':
            (root / 'observed').write_text('yes')
            if state.read_text() == 'loaded':
                print('fixture agent loaded')
                return 0
            print('Could not find service', file=sys.stderr)
            return 113
        state.write_text({'bootout': 'unloaded', 'bootstrap': 'loaded'}[argv[0]])
        with (root / 'events').open('a') as stream:
            stream.write(argv[0] + '\n')
        return 0
    if kind == 'processes':
        live = (root / 'live').read_text()
        if live:
            assert (root / 'agent').read_text() == 'unloaded'
            with (root / 'events').open('a') as stream:
                stream.write('drain-live\n')
            print(live)
        return 0
    if kind == 'backup':
        rows = Path(os.environ['BACKUP_PAIRS']).read_text().splitlines()[1:]
        for index, row in enumerate(rows, 1):
            _, source, destination, _ = row.split('\t')
            src, dst = Path(source), Path(destination)
            assert src.is_relative_to(root) and dst.is_relative_to(root)
            dst.mkdir(parents=True, exist_ok=True)
            for path in sorted(src.rglob('*')):
                if not path.is_file():
                    continue
                target = dst / path.relative_to(src)
                if target.exists() and target.read_bytes() != path.read_bytes():
                    archive = dst / '.deleted' / 'fixture-stamp' / path.relative_to(src)
                    archive.parent.mkdir(parents=True, exist_ok=True)
                    # Keep earlier displaced versions when the inverse runs.
                    if not archive.exists():
                        shutil.copy2(target, archive)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)
            (dst / '.last_success').write_text('fixture-stamp')
            kill = (root / 'kill').read_text()
            expected = ('resync' if len(rows) == 1 else 'backup') + str(index)
            if kill == expected:
                os.kill(os.getppid(), signal.SIGKILL)
                return 0
        return 0
    raise AssertionError(kind)


def driver(root, operation):
    run = str(root / 'run')
    if operation == 'recover':
        (root / 'observed').write_text('no')
        children = []
        ticks = [0]
        race = (root / 'race').read_text()
        def wait(seconds):
            ticks[0] += seconds
            with (root / 'events').open('a') as stream:
                stream.write('wait\n')
            if race == 'finish':
                children[0].communicate(b'finish', timeout=5)
                (root / 'live').write_text('')
        def arguments(action):
            values = effects(root, action)
            if (isinstance(action, Launchd) and race != 'none' and not children
                    and (root / 'observed').read_text() == 'yes'):
                # The fake agent starts its child after print, before bootout.
                child = subprocess.Popen((sys.executable, '-B', '-c',
                    'import os; os.write(1,b"ready\\n"); os.read(0,100)'),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                children.append(child)
                import select
                if not select.select([child.stdout], [], [], 5)[0]:
                    raise AssertionError('child did not become ready')
                assert child.stdout.readline() == b'ready\n'
                (root / 'live').write_text(f'{child.pid} fixture-rsync')
                with (root / 'events').open('a') as stream:
                    stream.write('child-start\n')
            if isinstance(action, Quiesce):
                values.update(clock=lambda: ticks[0], sleep=wait, timeout=2)
            return values
        try:
            return switch_recover.recover(str(root / 'run/journal'), effect_arguments=arguments)
        finally:
            for child in children:
                if child.poll() is None:
                    child.kill()
                child.communicate(timeout=5)
    old = FileState(b'start', sha256(b'start').hexdigest(), 0o755, run + '/pre/unused')
    pairs = (BackupPair('ssd', str(root / 'P'), str(root / 'D'), str(root / 'exclude')),
             BackupPair('ssd', str(root / 'P/repo'), str(root / 'D/repo'), str(root / 'exclude')))
    actions = (Launchd('loaded', 'unloaded'), Quiesce(),
               Replace(str(root / 'P/repo/file'), old, b'changed', 0o755),
               BackupRun(pairs), Launchd('unloaded', 'loaded'))
    def seam(point, intent):
        kill = (root / 'kill').read_text()
        if point == 'mutation' and isinstance(intent.action, Launchd):
            name = 'pause' if intent.action.to_state == 'unloaded' else 'resume'
            if kill == name:
                os.kill(os.getpid(), signal.SIGKILL)
    switch_exec.execute(actions, run, effect_arguments=lambda action: effects(root, action), seam=seam)
    return 0


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        root = self.root
        (root / 'run').mkdir()
        (root / 'P/repo').mkdir(parents=True)
        (root / 'D/repo').mkdir(parents=True)
        (root / 'P/repo/file').write_bytes(b'start')
        (root / 'P/repo/file').chmod(0o755)
        (root / 'D/repo/file').write_bytes(b'start')
        (root / 'D/repo/file').chmod(0o755)
        (root / 'exclude').write_text('.deleted/\n.last_success\n')
        (root / 'agent').write_text('loaded')
        (root / 'kill').write_text('none')
        (root / 'race').write_text('none')
        (root / 'live').write_text('')
        (root / 'events').write_text('')
        header = 'reader\tsource\tdestination\texcludes\n'
        parent = f'ssd\t{root}/P\t{root}/D\texclude\n'
        child = f'ssd\t{root}/P/repo\t{root}/D/repo\texclude\n'
        (root / 'forward.tsv').write_text(header + parent + child)
        (root / 'inverse.tsv').write_text(header + parent)

    def run_child(self, operation):
        child = subprocess.Popen((sys.executable, '-B', str(Path(__file__).resolve()),
                                  '--driver', str(self.root), operation),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        def cleanup():
            if child.poll() is None:
                child.kill()
            child.communicate(timeout=5)
        self.addCleanup(cleanup)
        stdout, stderr = child.communicate(timeout=10)
        return child.returncode, stdout + stderr

    def kill_forward(self, point):
        (self.root / 'kill').write_text(point)
        code, output = self.run_child('forward')
        self.assertEqual(code, -signal.SIGKILL, output)
        (self.root / 'kill').write_text('none')

    def restored(self, backup):
        code, output = self.run_child('recover')
        self.assertEqual(code, 1, output)
        self.assertNotIn('Traceback', output)
        self.assertEqual((self.root / 'P/repo/file').read_bytes(), b'start')
        self.assertEqual((self.root / 'P/repo/file').stat().st_mode & 0o7777, 0o755)
        self.assertEqual((self.root / 'agent').read_text(), 'loaded')
        displaced = ((str(self.root / 'D'), 'repo/file', sha256(b'start').hexdigest()),) if backup else ()
        result = switch_effects.backup_compare(journal.BackupCompare((BackupPair(
            'ssd', str(self.root / 'P'), str(self.root / 'D'), str(self.root / 'exclude')),)),
            displaced=displaced)
        self.assertEqual(result.exit_code, 0, result.stopped)

    def fix3_call(self, expected):
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            code = switch_recover.recover(str(self.root / "run/journal"),
                effect_arguments=lambda a: effects(self.root, a))
        self.assertEqual(code, 3, output.getvalue())
        self.assertEqual(output.getvalue(), expected + "\n")

    def fix3_rebind(self):
        run = self.root / "run"
        parked = self.root / "parked-run"
        run.rename(parked)
        shutil.copytree(parked, run)
        return f"{str(run)!r}: is held at {parked}, not at {run}"

    def test_fix3_start_read_checks_before_parse(self):
        path = self.root / "run/journal"
        path.write_bytes(b"bad JSON\n")
        real = fdsafe.read_named
        expected = []
        def read(parent, name):
            data = real(parent, name)
            expected.append(self.fix3_rebind())
            return data
        with patch.object(fdsafe, "read_named", side_effect=read), \
                patch.object(switch_recover, "_parse", wraps=switch_recover._parse) as parse:
            run = path.parent
            self.fix3_call(f"{str(run)!r}: is held at {self.root / 'parked-run'}, not at {run}")
        self.assertEqual(len(expected), 1)
        parse.assert_not_called()
        self.assertEqual(path.read_bytes(), b"bad JSON\n")
        self.assertEqual((self.root / "P/repo/file").read_bytes(), b"start")

    def test_fix3_second_preimage_checks_before_read(self):
        run = self.root / "run"
        targets = (self.root / "P/repo/file", self.root / "D/repo/file")
        pre = FileState(b"start", sha256(b"start").hexdigest(), 0o755, str(run / "unused"))
        switch_exec.execute(tuple(Replace(str(p), pre, b"changed", 0o755) for p in targets), str(run))
        original = (run / "journal").read_bytes()
        real = switch_exec.preimage_hash
        reads = []
        def read(path):
            reads.append(path)
            value = real(path)
            if len(reads) == 1:
                self.fix3_rebind()
            return value
        with patch.object(switch_exec, "preimage_hash", side_effect=read):
            self.fix3_call(f"{str(run)!r}: is held at {self.root / 'parked-run'}, not at {run}")
        self.assertEqual(reads, [str(run / "pre/1")])
        self.assertEqual((run / "journal").read_bytes(), original)
        self.assertEqual([p.read_bytes() for p in targets], [b"changed", b"changed"])

    def test_fix3_repair_read_binds_identical_replacement(self):
        self.kill_forward("backup1")
        path = self.root / "run/journal"
        with path.open("ab") as stream:
            stream.write(b"[")
        original = path.read_bytes()
        inode = path.stat().st_ino
        real = switch_exec._file
        fired = []
        def read(parent, name):
            value = real(parent, name)
            if parent.path == str(path.parent) and name == "journal" and not fired:
                replacement = path.with_name("replacement")
                replacement.write_bytes(original)
                replacement.chmod(path.stat().st_mode & 0o7777)
                replacement.replace(path)
                fired.append(path.stat().st_ino)
            return value
        with patch.object(switch_exec, "_file", side_effect=read), \
                patch.object(switch_exec, "_create", wraps=switch_exec._create) as create:
            self.fix3_call(f"{str(path.parent)!r}: ESTALE: journal identity changed")
        self.assertEqual(len(fired), 1)
        self.assertNotEqual(fired[0], inode)
        create.assert_not_called()
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual((self.root / "P/repo/file").read_bytes(), b"changed")

    def test_fix3_final_read_checks_before_parse(self):
        path = self.root / "run/journal"
        path.write_bytes(b"")
        execute = switch_exec.execute
        def changed(*args, **kwargs):
            result = execute(*args, **kwargs)
            replacement = path.with_name("replacement")
            replacement.write_bytes(b"bad JSON\n")
            replacement.replace(path)
            return result
        with patch.object(switch_exec, "execute", side_effect=changed), \
                patch.object(switch_recover, "_parse", wraps=switch_recover._parse) as parse:
            self.fix3_call(f"{str(path.parent)!r}: ESTALE: journal identity changed")
        self.assertEqual(parse.call_count, 1)
        self.assertEqual(path.read_bytes(), b"bad JSON\n")
        self.assertEqual((self.root / "P/repo/file").read_bytes(), b"start")

    def test_fix3_final_preimage_containment_before_read(self):
        from dataclasses import replace
        self.kill_forward("backup1")
        path = self.root / "run/journal"
        outside = self.root / "outside-run"
        outside.write_bytes(b"start")
        execute = switch_exec.execute
        read = os.read
        reads = []
        def changed(*args, **kwargs):
            result = execute(*args, **kwargs)
            records = switch_exec.read_journal(str(path.parent)).records
            records = tuple(replace(r, action=replace(r.action,
                pre=replace(r.action.pre, preimage=str(outside))))
                if isinstance(r, journal.Intent) and r.direction == "forward"
                and isinstance(r.action, Replace) else r for r in records)
            path.write_text("".join(journal.encode(r) for r in records))
            return result
        def tracked(fd, *args):
            if os.fstat(fd).st_ino == outside.stat().st_ino:
                reads.append(fd)
            return read(fd, *args)
        with patch.object(switch_exec, "execute", side_effect=changed), \
                patch.object(os, "read", side_effect=tracked):
            self.fix3_call(f"{str(outside)!r}: EINVAL: preimage outside run folder")
        self.assertEqual(reads, [])
        self.assertEqual(outside.read_bytes(), b"start")
        self.assertEqual((self.root / "P/repo/file").read_bytes(), b"start")

    def fix3_final_record(self, mode):
        from dataclasses import replace
        path = self.root / "run/journal"
        path.write_bytes(b"")
        execute = switch_exec.execute
        saved = []
        def changed(*args, **kwargs):
            result = execute(*args, **kwargs)
            records = switch_exec.read_journal(str(path.parent)).records
            modified = []
            for record in records:
                if isinstance(record, journal.Intent):
                    if mode == "direction":
                        record = replace(record, direction="forward")
                    elif mode == "key":
                        record = replace(record, key="other-key")
                elif mode in ("missing", "not-applied"):
                    record = replace(record, outcome="not-applied")
                modified.append(record)
            data = "".join(journal.encode(r) for r in modified).encode("ascii")
            path.write_bytes(data)
            saved.append(data)
            return result
        with patch.object(switch_exec, "execute", side_effect=changed):
            self.fix3_call(f"{str(path.parent)!r}: EIO: inverse quiesce:1 has no verified done record")
        self.assertEqual(path.read_bytes(), saved[0])
        self.assertEqual((self.root / "P/repo/file").read_bytes(), b"start")

    def test_fix3_final_done_must_be_applied(self):
        self.fix3_final_record("not-applied")

    def test_fix3_final_done_must_exist(self):
        self.fix3_final_record("missing")

    def test_fix3_final_direction_must_be_inverse(self):
        self.fix3_final_record("direction")

    def test_fix3_final_key_must_match(self):
        self.fix3_final_record("key")

    def test_fix3_inverse_backup_creates_no_keys(self):
        pair = BackupPair("ssd", "/P", "/D", "/exclude")
        intent = journal.Intent(1, "inverse", "backup", BackupRun((pair,)), journal.NoIdentity())
        parsed = journal.parse(journal.encode(intent) + journal.encode(journal.Done(1, journal.NoIdentity())))
        state = journal.recover(parsed, None, {})
        self.assertEqual(state.status, 0)
        for action in (journal.ResyncP((pair,)), journal.BackupCompare((pair,))):
            with self.subTest(kind=action.kind):
                with self.assertRaises(fdsafe.Refusal) as caught:
                    switch_recover._keys(state, "/run", (action,), 1)
                self.assertEqual(str(caught.exception), f"{action.kind!r}: EINVAL: inverse has no journal key")

    def test_fix3_before_repair_does_not_read_replacement(self):
        self.kill_forward("backup1")
        path = self.root / "run/journal"
        with path.open("ab") as stream:
            stream.write(b"[")
        original = path.read_bytes()
        recover_state = switch_recover.recover_state
        read = os.read
        replaced = []
        reads = []
        def changed(*args, **kwargs):
            result = recover_state(*args, **kwargs)
            replacement = path.with_name("replacement")
            replacement.write_bytes(original)
            replacement.chmod(path.stat().st_mode & 0o7777)
            replacement.replace(path)
            replaced.append(path.stat().st_ino)
            return result
        def tracked(fd, *args):
            if replaced and os.fstat(fd).st_ino == replaced[0]:
                reads.append(fd)
            return read(fd, *args)
        with patch.object(switch_recover, "recover_state", side_effect=changed), \
                patch.object(os, "read", side_effect=tracked):
            self.fix3_call(f"{str(path.parent)!r}: ESTALE: journal identity changed")
        self.assertEqual(len(replaced), 1)
        self.assertEqual(reads, [])
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual((self.root / "P/repo/file").read_bytes(), b"changed")

    def fix2_stderr(self, expected, *, journal_path=None):
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            code = switch_recover.main(['--journal', str(
                journal_path or self.root / 'run/journal')])
        self.assertEqual(code, 3, output.getvalue())
        self.assertEqual(output.getvalue(), expected + '\n')

    def fix2_config(self, config, expected):
        (self.root / 'run/recovery.json').write_text(json.dumps(config))
        self.fix2_stderr(expected)

    def test_fix2_nonascii_journal(self):
        (self.root / 'run/journal').write_bytes(b'\xff')
        self.fix2_config(self.config(),
            f"{str(self.root / 'run')!r}: EILSEQ: non-ASCII journal")

    def test_fix2_journal_name(self):
        (self.root / 'run/recovery.json').write_text(json.dumps(self.config()))
        other = self.root / 'run/other'
        other.write_bytes(b'')
        self.fix2_stderr(f'{str(other)!r}: EINVAL: executor journal must be named journal',
                         journal_path=other)

    def test_fix2_invalid_json(self):
        path = self.root / 'run/recovery.json'
        for raw in (b'{', b'\xff'):
            path.write_bytes(raw)
            self.fix2_stderr(f'{str(path)!r}: EINVAL: invalid effect configuration')

    def test_fix2_missing_kind(self):
        for kind in ('LAUNCHD', 'QUIESCE', 'RESYNC_P', 'BACKUP_COMPARE'):
            config = self.config()
            del config[kind]
            self.fix2_config(config, f'{kind!r}: EINVAL: missing effect kind key')

    def test_fix2_config_object(self):
        self.fix2_config([], "'recovery.json': EINVAL: expected effect argument object")

    def test_fix2_unknown_kind(self):
        config = self.config()
        config['UNKNOWN'] = {}
        self.fix2_config(config, "'UNKNOWN': EINVAL: unknown effect kind key")

    def test_fix2_kind_object(self):
        config = self.config()
        config['LAUNCHD'] = []
        self.fix2_config(config, "'LAUNCHD': EINVAL: expected effect argument object")

    def test_fix2_extra_key(self):
        config = self.config()
        config['LAUNCHD']['extra'] = 'no'
        self.fix2_config(config, "'LAUNCHD.extra': EINVAL: extra key")

    def test_fix2_missing_key(self):
        config = self.config()
        del config['LAUNCHD']['domain']
        self.fix2_config(config, "'LAUNCHD.domain': EINVAL: missing key")

    def test_fix2_empty_argv(self):
        config = self.config()
        config['LAUNCHD']['command'] = []
        self.fix2_config(config, "'LAUNCHD.command': EINVAL: empty argv")

    def test_fix2_string(self):
        config = self.config()
        config['LAUNCHD']['domain'] = 17
        self.fix2_config(config, "'LAUNCHD.domain': EINVAL: expected string without NUL")

    def test_fix2_numeric_type(self):
        config = self.config()
        config['QUIESCE']['timeout'] = True
        self.fix2_config(config, "'QUIESCE.timeout': EINVAL: wrong numeric value type")

    def test_fix2_numeric_conversion(self):
        for kind, key in (('QUIESCE', 'timeout'), ('QUIESCE', 'interval'),
                          ('RESYNC_P', 'timeout')):
            config = self.config()
            config[kind][key] = 10**400
            self.fix2_config(config, f"'{kind}.{key}': EINVAL: numeric conversion failed: "
                             'int too large to convert to float')

    def test_fix2_finite(self):
        config = self.config()
        config['QUIESCE']['timeout'] = float('inf')
        self.fix2_config(config, "'QUIESCE.timeout': EINVAL: expected finite number")

    def test_fix2_environment(self):
        config = self.config()
        config['RESYNC_P']['env'] = []
        self.fix2_config(config, "'RESYNC_P.env': EINVAL: expected environment object")

    def test_fix2_array(self):
        config = self.config()
        config['LAUNCHD']['command'] = 'not argv'
        self.fix2_config(config, "'LAUNCHD.command': EINVAL: expected array")

    def test_fix2_array_length(self):
        config = self.config()
        config['BACKUP_COMPARE']['displaced'] = [['a', 'b']]
        self.fix2_config(config, "'BACKUP_COMPARE.displaced': EINVAL: wrong array length")

    def test_fix2_agent(self):
        self.kill_forward('pause')
        with patch.object(switch_effects, '_run', return_value=
                subprocess.CompletedProcess((), 9, '', 'fixture-denied')):
            self.fix2_config(self.config(),
                "'fixture/agent': EIO: launchctl print: 9 fixture-denied")

    def fix2_repair_change(self, suffix, expected):
        self.kill_forward('pause')
        path = self.root / 'run/journal'
        with path.open('ab') as stream:
            stream.write(b'[')
        real = switch_recover.recover_state
        def change(*args, **kwargs):
            state = real(*args, **kwargs)
            with path.open('ab') as stream:
                stream.write(suffix)
            return state
        with patch.object(switch_recover, 'recover_state', side_effect=change):
            self.fix2_config(self.config(), f'{str(path)!r}: {expected}')

    def test_fix2_repair_nonascii(self):
        self.fix2_repair_change(b'\xff', 'EILSEQ: non-ASCII journal')

    def test_fix2_repair_changed(self):
        self.fix2_repair_change(b'"', 'ESTALE: journal changed before repair')

    def test_fix2_archive_collision(self):
        self.kill_forward('pause')
        path = self.root / 'run/journal'
        with path.open('ab') as stream:
            stream.write(b'[')
        archive = path.parent / ('journal.torn-' + sha256(path.read_bytes()).hexdigest())
        archive.write_bytes(b'other')
        self.fix2_config(self.config(), f'{str(archive)!r}: ESTALE: torn-journal archive differs')

    def test_fix2_journal_identity(self):
        (self.root / 'run/journal').write_bytes(b'')
        path = self.root / 'run/journal'
        real = switch_exec.execute
        def replace(*args, **kwargs):
            result = real(*args, **kwargs)
            path.rename(path.with_name('parked-journal'))
            path.write_bytes(path.with_name('parked-journal').read_bytes())
            return result
        with patch.object(switch_exec, 'execute', side_effect=replace):
            self.fix2_config(self.config(),
                f'{str(path.parent)!r}: ESTALE: journal identity changed')

    def test_fix2_done_record(self):
        path = self.root / 'run/journal'
        path.write_bytes(b'')
        real = switch_exec.execute
        def lose(*args, **kwargs):
            result = real(*args, **kwargs)
            path.write_bytes(b'')
            return result
        with patch.object(switch_exec, 'execute', side_effect=lose):
            self.fix2_config(self.config(),
                f'{str(path.parent)!r}: EIO: inverse quiesce:1 has no verified done record')

    def test_fix2_preimage_outside(self):
        from dataclasses import replace
        self.kill_forward('backup1')
        path = self.root / 'run/journal'
        outside = self.root / 'outside'
        outside.write_bytes(b'start')
        records = switch_exec.read_journal(str(path.parent)).records
        changed = tuple(replace(record, action=replace(record.action,
            pre=replace(record.action.pre, preimage=str(outside))))
            if isinstance(record, journal.Intent) and isinstance(record.action, Replace)
            else record for record in records)
        path.write_text(''.join(journal.encode(record) for record in changed))
        self.fix2_config(self.config(), f'{str(outside)!r}: EINVAL: preimage outside run folder')

    def test_fix2_inverse_key(self):
        # [LAW:behavior-not-structure] Exercise the planner/key disagreement refusal
        # at its boundary; ordinary planner output cannot produce this state.
        state = journal.RecoveryState((), (), None, (), 0)
        action = Rename(str(self.root / 'P'), str(self.root / 'other'))
        def disagreement(*args, **kwargs):
            return switch_recover._keys(state, str(self.root / 'run'), (action,), 0)
        with patch.object(switch_recover, 'recover', side_effect=disagreement):
            self.fix2_config(self.config(), "'RENAME': EINVAL: inverse has no journal key")

    def test_fix2_malformed_journal(self):
        (self.root / 'run/journal').write_bytes(b'not JSON\n')
        self.fix2_config(self.config(), "'line 1': EINVAL: malformed JSON")

    def test_fix1_rebind_review_probe(self):
        self.kill_forward('backup1')
        run = self.root / 'run'
        output = io.StringIO()
        with contextlib.redirect_stderr(output), fault_kit.rename_and_rebind('close', 2, run):
            code = switch_recover.recover(str(run / 'journal'),
                effect_arguments=lambda a: effects(self.root, a))
        self.assertEqual(code, 3, output.getvalue())
        self.assertIn(str(run), output.getvalue())
        self.assertEqual(list(run.iterdir()), [])

    def test_fix1_large_integer_review_probe(self):
        self.bad_configuration('QUIESCE', 'timeout', lambda v: v.update(timeout=10**400))

    def test_fix1_large_integer_interval(self):
        self.bad_configuration('QUIESCE', 'interval', lambda v: v.update(interval=10**400))

    def test_fix1_large_integer_resync_timeout(self):
        self.bad_configuration('RESYNC_P', 'timeout', lambda v: v.update(timeout=10**400))

    def test_fix1_keyboard_interrupt_propagates(self):
        with patch.object(fdsafe, 'hold_root', side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                switch_recover.main(['--journal', str(self.root / 'run/journal')])

    def test_fix1_unexpected_effect_cli(self):
        self.kill_forward('backup1')
        (self.root / 'run/recovery.json').write_text(json.dumps(self.config()))
        script = """import os, sys
import fault_kit
from ops.migrate import switch_effects, switch_recover
real = switch_effects.execute
def fail(*args, **kwargs):
    with fault_kit.raise_unexpected('fstat', 1, RuntimeError):
        os.fstat(2)
    return real(*args, **kwargs)
switch_effects.execute = fail
sys.exit(switch_recover.main(sys.argv[1:]))
"""
        result = subprocess.run((sys.executable, '-B', '-c', script, '--journal',
            str(self.root / 'run/journal')), capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertEqual(result.stderr, 'switch_recover: unexpected RuntimeError: '
                         'fault_kit: unexpected RuntimeError from fstat\n')

    def rebound_step(self, module, name, *, torn=False, populated=False):
        self.kill_forward('backup1')
        run = self.root / 'run'
        if torn:
            with (run / 'journal').open('ab') as stream:
                stream.write(b'[')
        real = getattr(module, name)
        fired = []
        replacement = []
        def contents():
            return {str(p.relative_to(run)): (p.read_bytes(), p.stat().st_mode)
                    for p in run.rglob('*') if p.is_file()}
        def rebound(*args, **kwargs):
            value = real(*args, **kwargs)
            if not fired:
                with fault_kit.rename_and_rebind('fstat', 1, run) as attack:
                    os.fstat(2)
                if populated:
                    shutil.copytree(attack.parked, run, dirs_exist_ok=True)
                replacement.append(contents())
                fired.append(True)
            return value
        output = io.StringIO()
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(module, name, side_effect=rebound))
            if name == 'parse':
                stack.enter_context(patch.object(switch_exec, 'parse', side_effect=rebound))
            stack.enter_context(contextlib.redirect_stderr(output))
            code = switch_recover.recover(str(run / 'journal'),
                effect_arguments=lambda a: effects(self.root, a))
        self.assertEqual(fired, [True])
        self.assertEqual(code, 3, output.getvalue())
        self.assertIn(str(run), output.getvalue())
        self.assertEqual(contents(), replacement[0])
        if not populated:
            self.assertEqual(list(run.iterdir()), [])

    def test_fix1_populated_before_preimage(self):
        self.rebound_step(switch_recover, 'parse', populated=True)

    def test_fix1_populated_after_preimage(self):
        self.rebound_step(switch_exec, 'preimage_hash', populated=True)

    def test_fix1_populated_after_observation(self):
        self.rebound_step(switch_exec, 'observe', populated=True)

    def test_fix1_populated_before_repair(self):
        self.rebound_step(switch_recover, 'recover_state', torn=True, populated=True)

    def test_fix1_populated_before_receipt(self):
        self.rebound_step(switch_recover, '_repair', torn=True, populated=True)

    def test_fix1_populated_after_receipt(self):
        self.rebound_step(switch_exec, 'append_receipt', populated=True)

    def test_fix1_populated_before_execute(self):
        self.rebound_step(switch_recover.switch_inverse_core, 'plan', populated=True)

    def test_fix1_populated_before_final_verification(self):
        self.rebound_step(switch_exec, 'execute', populated=True)

    def test_fix1_populated_before_receipt_without_repair(self):
        self.rebound_step(switch_recover, 'recover_state', populated=True)

    def test_fix1_first_read_is_authoritative(self):
        self.kill_forward('backup1')
        path = self.root / 'run/journal'
        real = fdsafe.read_named
        fired = []
        def truncate_after_read(parent, name):
            raw = real(parent, name)
            if name == 'journal' and not fired:
                path.write_bytes(b'')
                fired.append(True)
            return raw
        output = io.StringIO()
        with patch.object(fdsafe, 'read_named', side_effect=truncate_after_read), \
                contextlib.redirect_stderr(output):
            code = switch_recover.recover(str(path), effect_arguments=lambda a: effects(self.root, a))
        self.assertEqual(fired, [True])
        self.assertEqual(code, 3, output.getvalue())
        self.assertIn(str(path.parent), output.getvalue())
        self.assertEqual(path.read_bytes(), b'')
        self.assertEqual((self.root / 'P/repo/file').read_bytes(), b'changed')

    def test_fix1_rebind_before_preimage(self):
        self.rebound_step(switch_recover, 'parse')

    def test_fix1_rebind_after_preimage(self):
        self.rebound_step(switch_exec, 'preimage_hash')

    def test_fix1_rebind_after_observation(self):
        self.rebound_step(switch_exec, 'observe')

    def test_fix1_rebind_before_repair(self):
        self.rebound_step(switch_recover, 'recover_state', torn=True)

    def test_fix1_rebind_before_receipt(self):
        self.rebound_step(switch_recover, '_repair', torn=True)

    def test_fix1_rebind_after_receipt(self):
        self.rebound_step(switch_exec, 'append_receipt')

    def test_fix1_rebind_before_execute(self):
        self.rebound_step(switch_recover.switch_inverse_core, 'plan')

    def test_fix1_rebind_before_final_verification(self):
        self.rebound_step(switch_exec, 'execute')

    def test_fix1_rebind_after_final_verification(self):
        real = switch_exec._check_journal
        finished = []
        execute = switch_exec.execute
        def finish(*args, **kwargs):
            result = execute(*args, **kwargs)
            finished.append(True)
            return result
        def check(parsed):
            result = real(parsed)
            if finished:
                with fault_kit.rename_and_rebind('fstat', 1, self.root / 'run'):
                    os.fstat(2)
            return result
        self.kill_forward('backup1')
        output = io.StringIO()
        with patch.object(switch_exec, 'execute', side_effect=finish), \
                patch.object(switch_exec, '_check_journal', side_effect=check), \
                contextlib.redirect_stderr(output):
            code = switch_recover.recover(str(self.root / 'run/journal'),
                effect_arguments=lambda a: effects(self.root, a))
        self.assertEqual(code, 3, output.getvalue())
        self.assertIn(str(self.root / 'run'), output.getvalue())
        self.assertEqual(list((self.root / 'run').iterdir()), [])

    def test_fix1_final_requires_executed_done_records(self):
        self.kill_forward('backup1')
        execute = switch_exec.execute
        path = self.root / 'run/journal'
        def lost_receipts(*args, **kwargs):
            before = path.read_bytes()
            result = execute(*args, **kwargs)
            path.write_bytes(before)
            return result
        output = io.StringIO()
        with patch.object(switch_exec, 'execute', side_effect=lost_receipts), \
                contextlib.redirect_stderr(output):
            code = switch_recover.recover(str(path), effect_arguments=lambda a: effects(self.root, a))
        self.assertEqual(code, 3, output.getvalue())
        self.assertIn(str(path.parent), output.getvalue())

    def changed_journal(self, missing):
        self.kill_forward('backup1')
        path = self.root / 'run/journal'
        real = switch_exec.execute
        def change(*args, **kwargs):
            result = real(*args, **kwargs)
            path.rename(path.with_name('parked-journal'))
            if not missing:
                path.write_bytes(path.with_name('parked-journal').read_bytes())
            return result
        output = io.StringIO()
        with patch.object(switch_exec, 'execute', side_effect=change), \
                contextlib.redirect_stderr(output):
            code = switch_recover.recover(str(path), effect_arguments=lambda a: effects(self.root, a))
        self.assertEqual(code, 3, output.getvalue())
        self.assertIn(str(path.parent), output.getvalue())

    def test_fix1_missing_journal_after_execute(self):
        self.changed_journal(True)

    def test_fix1_replaced_journal_after_execute(self):
        self.changed_journal(False)

    def test_kill_during_first_backup_pair(self):
        self.kill_forward('backup1')
        self.restored(True)

    def test_kill_during_second_backup_pair(self):
        self.kill_forward('backup2')
        self.restored(True)

    def test_kill_after_pause_mutation(self):
        self.kill_forward('pause')
        self.restored(False)

    def test_kill_after_resume_mutation(self):
        self.kill_forward('resume')
        self.restored(True)

    def test_kill_during_resync_restarts(self):
        self.kill_forward('backup1')
        (self.root / 'kill').write_text('resync1')
        code, output = self.run_child('recover')
        self.assertEqual(code, -signal.SIGKILL, output)
        (self.root / 'kill').write_text('none')
        self.restored(True)

    def test_racing_child_drains_after_unload(self):
        self.kill_forward('resume')
        (self.root / 'race').write_text('finish')
        (self.root / 'events').write_text('')
        self.restored(True)
        self.assertEqual((self.root / 'events').read_text().splitlines(),
                         ['child-start', 'bootout', 'drain-live', 'wait', 'bootstrap'])

    def test_racing_child_at_deadline_is_named_and_pause_stays(self):
        self.kill_forward('resume')
        (self.root / 'race').write_text('stuck')
        code, output = self.run_child('recover')
        self.assertEqual(code, 3, output)
        self.assertIn((self.root / 'live').read_text(), output)
        self.assertEqual((self.root / 'agent').read_text(), 'unloaded')
        self.assertEqual((self.root / 'P/repo/file').read_bytes(), b'changed')
        self.assertEqual((self.root / 'events').read_text().count('wait\n'), 2)

    def test_torn_done_keeps_original_and_restores(self):
        self.kill_forward('pause')
        path = self.root / 'run/journal'
        with path.open('ab') as stream:
            stream.write(journal.encode(journal.Done(1, journal.AgentIdentity('unloaded'))).encode()[:12])
        original = path.read_bytes()
        self.restored(False)
        self.assertEqual((self.root / 'run' / ('journal.torn-' + sha256(original).hexdigest())).read_bytes(), original)
        self.assertFalse(switch_exec.read_journal(str(self.root / 'run')).truncated)

    def test_torn_intent_keeps_original_without_claiming_mutation(self):
        self.kill_forward('pause')
        run = str(self.root / 'run')
        switch_exec.append_receipt(run, journal.Done(1, journal.AgentIdentity('unloaded')))
        path = self.root / 'run/journal'
        item = journal.Intent(2, 'forward', 'forward:2', Quiesce(), journal.NoIdentity())
        with path.open('ab') as stream:
            stream.write(journal.encode(item).encode()[:17])
        original = path.read_bytes()
        self.restored(False)
        self.assertEqual((self.root / 'run' / ('journal.torn-' + sha256(original).hexdigest())).read_bytes(), original)

    def test_complete_last_record_without_lf_is_repaired(self):
        self.kill_forward('pause')
        path = self.root / 'run/journal'
        with path.open('ab') as stream:
            stream.write(journal.encode(journal.Done(1, journal.AgentIdentity('unloaded'))).encode()[:-1])
        original = path.read_bytes()
        self.restored(False)
        self.assertEqual((self.root / 'run' / ('journal.torn-' + sha256(original).hexdigest())).read_bytes(), original)

    def test_journal_changed_during_repair_is_kept(self):
        self.kill_forward('pause')
        run = str(self.root / 'run')
        path = self.root / 'run/journal'
        with path.open('ab') as stream:
            stream.write(b'[')
        parsed = switch_exec.read_journal(run)
        changed = path.read_bytes() + b'"'
        path.write_bytes(changed)
        with self.assertRaises(fdsafe.Refusal) as caught:
            self.repair(run, parsed)
        self.assertEqual(caught.exception.path, str(path))
        self.assertEqual(path.read_bytes(), changed)

    def repair(self, run, parsed):
        with fdsafe.hold_root(run) as parent:
            identity = switch_recover._inode(fdsafe._scan(parent, 'journal').st)
            return switch_recover._repair(parent, identity, parsed)

    def config(self):
        return {kind: values for kind, values in (
            ('LAUNCHD', effects(self.root, Launchd('loaded', 'unloaded'))),
            ('QUIESCE', dict(command=command(self.root, 'processes'), timeout=0, interval=1)),
            ('RESYNC_P', dict(command=command(self.root, 'backup'), table=str(self.root / 'inverse.tsv'),
                              env=dict(os.environ, FIXTURE_ROOT=str(self.root)), timeout=5)),
            ('BACKUP_COMPARE', dict(displaced=((str(self.root / 'D'), 'repo/file', sha256(b'start').hexdigest()),))),)}

    def cli(self):
        return subprocess.run((sys.executable, '-B', '-m', 'ops.migrate.switch_recover',
            '--journal', str(self.root / 'run/journal')), capture_output=True, text=True, timeout=10)

    def test_cli_uses_same_recovery_path(self):
        self.kill_forward('resume')
        (self.root / 'run/recovery.json').write_text(json.dumps(self.config()))
        result = self.cli()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertEqual((self.root / 'P/repo/file').read_bytes(), b'start')
        self.assertEqual((self.root / 'agent').read_text(), 'loaded')

    def test_cli_refuses_bad_or_missing_configuration(self):
        self.kill_forward('pause')
        result = self.cli()
        self.assertEqual(result.returncode, 3, result.stderr)
        for value in ('{', '[]', '{}', '{"LAUNCHD":[]}'):
            (self.root / 'run/recovery.json').write_text(value)
            result = self.cli()
            self.assertEqual(result.returncode, 3, result.stderr)
            self.assertNotIn('Traceback', result.stderr)
            if value == '[]':
                self.assertIn('expected effect argument object', result.stderr)
                self.assertIn("'recovery.json': EINVAL:", result.stderr)

    def test_missing_journal_refuses(self):
        code, output = self.run_child('recover')
        self.assertEqual(code, 3, output)
        self.assertIn('journal', output)

    def test_alternate_journal_name_refuses(self):
        self.kill_forward('pause')
        (self.root / 'run/other').write_bytes((self.root / 'run/journal').read_bytes())
        self.assertEqual(switch_recover.recover(str(self.root / 'run/other'),
            effect_arguments=lambda action: effects(self.root, action)), 3)

    def test_agent_observation_refuses_unknown_command_result(self):
        self.kill_forward('pause')
        for code, stdout, stderr in ((0, '', ''), (113, '', 'other'), (9, '', 'Could not find service')):
            with self.subTest(code=code, stdout=stdout, stderr=stderr):
                with patch.object(switch_effects, '_run', return_value=subprocess.CompletedProcess((), code, stdout, stderr)):
                    self.assertEqual(switch_recover.recover(str(self.root / 'run/journal'),
                        effect_arguments=lambda action: effects(self.root, action)), 3)

    def test_torn_archive_collision_refuses_and_keeps_inputs(self):
        self.kill_forward('pause')
        path = self.root / 'run/journal'
        with path.open('ab') as stream:
            stream.write(b'[')
        original = path.read_bytes()
        archive = self.root / 'run' / ('journal.torn-' + sha256(original).hexdigest())
        archive.write_bytes(b'other')
        code, output = self.run_child('recover')
        self.assertEqual(code, 3, output)
        self.assertIn(str(archive), output)
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(archive.read_bytes(), b'other')

    def test_torn_archive_reused_after_interruption_and_short_writes(self):
        self.kill_forward('pause')
        path = self.root / 'run/journal'
        with path.open('ab') as stream:
            stream.write(b'[')
        original = path.read_bytes()
        archive = self.root / 'run' / ('journal.torn-' + sha256(original).hexdigest())
        archive.write_bytes(original)
        with fault_kit.one_byte_writes():
            code = switch_recover.recover(str(path), effect_arguments=lambda action: effects(self.root, action))
        self.assertEqual(code, 1)
        self.assertEqual(archive.read_bytes(), original)
        self.assertFalse(switch_exec.read_journal(str(self.root / 'run')).truncated)

    def test_nonascii_repair_refuses(self):
        self.kill_forward('pause')
        path = self.root / 'run/journal'
        parsed = switch_exec.read_journal(str(path.parent))
        with path.open('ab') as stream:
            stream.write(b'\xff')
        with self.assertRaisesRegex(fdsafe.Refusal, 'EILSEQ: non-ASCII journal') as caught:
            self.repair(str(path.parent), parsed)
        self.assertEqual(caught.exception.path, str(path))

    def test_malformed_repair_keeps_parser_refusal(self):
        self.kill_forward('pause')
        path = self.root / 'run/journal'
        parsed = switch_exec.read_journal(str(path.parent))
        with path.open('ab') as stream:
            stream.write(b'not JSON\n')
        with self.assertRaisesRegex(fdsafe.Refusal, 'EINVAL: malformed JSON'):
            self.repair(str(path.parent), parsed)

    def test_main_unexpected_read_error_surfaces(self):
        (self.root / 'run/recovery.json').write_text('{}')
        with fault_kit.raise_unexpected('read', 1, RuntimeError):
            with contextlib.redirect_stderr(io.StringIO()) as output:
                self.assertEqual(switch_recover.main(['--journal', str(self.root / 'run/journal')]), 3)
            self.assertEqual(output.getvalue(), 'switch_recover: unexpected RuntimeError: '
                             'fault_kit: unexpected RuntimeError from read\n')

    def test_main_json_recursion_error_surfaces(self):
        (self.root / 'run/recovery.json').write_text('[' * 2000 + '0' + ']' * 2000)
        with contextlib.redirect_stderr(io.StringIO()) as output:
            self.assertEqual(switch_recover.main(['--journal', str(self.root / 'run/journal')]), 3)
        self.assertRegex(output.getvalue(), r'^switch_recover: unexpected RecursionError: '
                         r'maximum recursion depth exceeded[^\n]*\n$')

    def test_preimage_outside_run_refuses_without_reading_it(self):
        from dataclasses import replace
        self.kill_forward('backup1')
        run = str(self.root / 'run')
        records = switch_exec.read_journal(run).records
        outside = self.root / 'outside'
        outside.write_bytes(b'start')
        changed = tuple(replace(record, action=replace(record.action,
            pre=replace(record.action.pre, preimage=str(outside))))
            if isinstance(record, journal.Intent) and isinstance(record.action, Replace)
            else record for record in records)
        (self.root / 'run/journal').write_text(''.join(journal.encode(record) for record in changed))
        code, output = self.run_child('recover')
        self.assertEqual(code, 3, output)
        self.assertIn('outside run folder', output)

    def test_rename_observation_and_inverse(self):
        src, dst = self.root / 'P', self.root / 'renamed'
        def stop(point, intent):
            if point == 'mutation':
                raise InterruptedError('fixture interruption')
        with self.assertRaises(InterruptedError):
            switch_exec.execute((Rename(str(src), str(dst)),), str(self.root / 'run'), seam=stop)
        self.restored(False)
        self.assertFalse(dst.exists())

    def test_completed_inverse_is_not_applied_twice(self):
        self.kill_forward('backup1')
        self.restored(True)
        before = switch_exec.read_journal(str(self.root / 'run')).records
        self.restored(True)
        after = switch_exec.read_journal(str(self.root / 'run')).records
        self.assertEqual(tuple(r for r in after if isinstance(r, journal.Intent) and not isinstance(r.action, Quiesce)),
                         tuple(r for r in before if isinstance(r, journal.Intent) and not isinstance(r.action, Quiesce)))

    def test_w17_newer_work_during_inverse_is_stopped(self):
        self.kill_forward('backup1')
        path = self.root / 'P/repo/file'
        real = os.replace
        fired = []
        def write_during_replace(src, dst, **kwargs):
            if dst == 'file' and not fired:
                fired.append(True)
                path.write_bytes(b'newer at rename')
            return real(src, dst, **kwargs)
        with patch.object(os, 'replace', side_effect=write_during_replace):
            code = switch_recover.recover(str(self.root / 'run/journal'),
                effect_arguments=lambda action: effects(self.root, action))
        self.assertEqual(code, 3)
        self.assertEqual(fired, [True])
        self.assertEqual(path.read_bytes(), b'newer at rename')
        self.assertIsInstance(switch_exec.read_journal(str(self.root / 'run')).records[-1], journal.Intent)

    def test_journal_symlink_swap_refuses(self):
        self.kill_forward('pause')
        path = self.root / 'run/journal'
        target = self.root / 'other'
        target.write_bytes(b'untouched')
        with fault_kit.swap_for_symlink('open', 1, path, target, match=lambda name, *a, **kw: name == 'journal'):
            code = switch_recover.recover(str(path), effect_arguments=lambda action: effects(self.root, action))
        self.assertEqual(code, 3)
        self.assertEqual(target.read_bytes(), b'untouched')

    def test_journal_fifo_refuses(self):
        self.kill_forward('pause')
        path = self.root / 'run/journal'
        parked = self.root / 'run/parked'
        path.rename(parked)
        os.mkfifo(path)
        code, output = self.run_child('recover')
        self.assertEqual(code, 3, output)

    def test_run_rebind_refuses(self):
        self.kill_forward('pause')
        run = self.root / 'run'
        with fault_kit.rename_and_rebind('read', 1, run):
            code = switch_recover.recover(str(run / 'journal'),
                effect_arguments=lambda action: effects(self.root, action))
        self.assertEqual(code, 3)

    def test_torn_write_faults_refuse(self):
        self.kill_forward('pause')
        path = self.root / 'run/journal'
        with path.open('ab') as stream:
            stream.write(b'[')
        original = path.read_bytes()
        with fault_kit.inject_oserror('write', 1, fault_kit.ERRNOS[0]):
            code = switch_recover.recover(str(path), effect_arguments=lambda action: effects(self.root, action))
        self.assertEqual(code, 3)
        self.assertEqual(path.read_bytes(), original)

    def test_newer_file_is_kept_and_named(self):
        self.kill_forward('backup1')
        target = self.root / 'P/repo/file'
        target.write_bytes(b'newer work')
        code, output = self.run_child('recover')
        self.assertEqual(code, 3, output)
        self.assertIn(str(target), output)
        self.assertEqual(target.read_bytes(), b'newer work')
        self.assertEqual((self.root / 'agent').read_text(), 'unloaded')

    def test_corrupt_preimage_stops_before_inverse(self):
        self.kill_forward('backup1')
        preimage = self.root / 'run/pre/3'
        preimage.write_bytes(b'corrupt')
        before = (self.root / 'run/journal').read_bytes()
        code, output = self.run_child('recover')
        self.assertEqual(code, 3, output)
        self.assertIn(str(preimage), output)
        self.assertEqual((self.root / 'run/journal').read_bytes(), before)

    def snapshot(self):
        return {str(path.relative_to(self.root)): (path.read_bytes(), path.stat().st_mode)
                for path in self.root.rglob('*') if path.is_file()
                and path.name != 'observed'}

    def test_corrupt_preimage_after_resume_reports_pause_not_held_without_mutation(self):
        self.kill_forward('resume')
        (self.root / 'run/pre/3').write_bytes(b'corrupt')
        before = self.snapshot()
        code, output = self.run_child('recover')
        self.assertEqual(code, 3, output)
        self.assertIn('missing or changed preimage', output)
        self.assertIn('forward:5: agent loaded; pause not held; no inverse applied', output)
        self.assertNotIn('Traceback', output)
        self.assertEqual((self.root / 'agent').read_text(), 'loaded')
        self.assertEqual(self.snapshot(), before)

    def test_corrupt_preimage_before_resume_keeps_agent_and_every_target(self):
        self.kill_forward('backup1')
        (self.root / 'run/pre/3').write_bytes(b'corrupt')
        before = self.snapshot()
        code, output = self.run_child('recover')
        self.assertEqual(code, 3, output)
        self.assertIn('missing or changed preimage', output)
        self.assertNotIn('pause not held', output)
        self.assertNotIn('Traceback', output)
        self.assertEqual((self.root / 'agent').read_text(), 'unloaded')
        self.assertEqual(self.snapshot(), before)

    def test_incomplete_effect_configuration_is_not_success(self):
        self.kill_forward('pause')
        (self.root / 'run/recovery.json').write_text('{"LAUNCHD":{}}')
        result = self.cli()
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def bad_configuration(self, kind, key, change):
        self.kill_forward('resume')
        config = self.config()
        change(config[kind])
        (self.root / 'run/recovery.json').write_text(json.dumps(config))
        before = self.snapshot()
        result = self.cli()
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertIn(kind, result.stderr)
        self.assertIn(key, result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_launchd_configuration_missing_key(self):
        self.bad_configuration('LAUNCHD', 'domain', lambda v: v.pop('domain'))

    def test_launchd_configuration_extra_key(self):
        self.bad_configuration('LAUNCHD', 'extra', lambda v: v.update(extra='no'))

    def test_launchd_configuration_wrong_type(self):
        self.bad_configuration('LAUNCHD', 'domain', lambda v: v.update(domain=17))

    def test_backup_configuration_missing_key(self):
        self.bad_configuration('RESYNC_P', 'table', lambda v: v.pop('table'))

    def test_backup_configuration_extra_key(self):
        self.bad_configuration('RESYNC_P', 'extra', lambda v: v.update(extra='no'))

    def test_backup_configuration_wrong_type(self):
        self.bad_configuration('RESYNC_P', 'env', lambda v: v.update(env=[]))

    def test_configuration_nested_shapes_refuse_before_observation(self):
        self.kill_forward('resume')
        (self.root / 'observed').write_text('not observed by recovery')
        cases = (
            ('LAUNCHD', 'command', []), ('LAUNCHD', 'command', 'not argv'),
            ('LAUNCHD', 'command', [7]), ('LAUNCHD', 'service', None),
            ('LAUNCHD', 'plist', 'nul\0path'),
            ('QUIESCE', 'timeout', True), ('QUIESCE', 'timeout', None),
            ('QUIESCE', 'interval', '1'), ('QUIESCE', 'interval', float('inf')),
            ('QUIESCE', 'timeout', float('nan')),
            ('RESYNC_P', 'timeout', False), ('RESYNC_P', 'table', []),
            ('RESYNC_P', 'env', {'bad': 1}), ('RESYNC_P', 'env', {'nul\0': ''}),
            ('BACKUP_COMPARE', 'displaced', {}), ('BACKUP_COMPARE', 'displaced', ['bad']),
            ('BACKUP_COMPARE', 'displaced', [['a', 'b']]),
            ('BACKUP_COMPARE', 'displaced', [['a', 'b', 'c', 'd']]),
            ('BACKUP_COMPARE', 'displaced', [['a', 'b', 3]]),
        )
        for kind, key, value in cases:
            config = self.config()
            config[kind][key] = value
            (self.root / 'run/recovery.json').write_text(json.dumps(config))
            before = self.snapshot()
            result = self.cli()
            self.assertEqual(result.returncode, 3, (kind, key, value, result.stderr))
            self.assertIn(kind + '.' + key, result.stderr)
            self.assertNotIn('Traceback', result.stderr)
            self.assertEqual(self.snapshot(), before)
            self.assertEqual((self.root / 'observed').read_text(), 'not observed by recovery')

    def test_configuration_kind_missing_extra_and_nonobject(self):
        self.kill_forward('pause')
        for kind in ('LAUNCHD', 'QUIESCE', 'RESYNC_P', 'BACKUP_COMPARE', 'UNKNOWN'):
            config = self.config()
            if kind == 'UNKNOWN':
                config[kind] = {}
            else:
                del config[kind]
            (self.root / 'run/recovery.json').write_text(json.dumps(config))
            before = self.snapshot()
            result = self.cli()
            self.assertEqual(result.returncode, 3, result.stderr)
            self.assertIn(kind, result.stderr)
            self.assertEqual(self.snapshot(), before)
        config = self.config()
        config['BACKUP_COMPARE'] = []
        (self.root / 'run/recovery.json').write_text(json.dumps(config))
        result = self.cli()
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertIn('BACKUP_COMPARE', result.stderr)

    def test_configuration_nullable_backup_timeout_and_float_budget(self):
        self.kill_forward('resume')
        config = self.config()
        config['RESYNC_P']['timeout'] = None
        config['QUIESCE'].update(timeout=0.0, interval=1.0)
        (self.root / 'run/recovery.json').write_text(json.dumps(config))
        result = self.cli()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual((self.root / 'P/repo/file').read_bytes(), b'start')

    def test_unknown_agent_observation_names_refusal(self):
        self.kill_forward('pause')
        before = self.snapshot()
        output = io.StringIO()
        with contextlib.redirect_stderr(output), patch.object(switch_effects, '_run',
                return_value=subprocess.CompletedProcess((), 9, '', 'fixture-denied')):
            code = switch_recover.recover(str(self.root / 'run/journal'),
                effect_arguments=lambda action: effects(self.root, action))
        self.assertEqual(code, 3)
        self.assertIn('launchctl print: 9 fixture-denied', output.getvalue())
        self.assertEqual(self.snapshot(), before)

    def test_noncanonical_journal_refuses_before_mutation(self):
        self.kill_forward('pause')
        before = self.snapshot()
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            code = switch_recover.recover(str(self.root) + '/run/../run/journal',
                effect_arguments=lambda action: effects(self.root, action))
        self.assertEqual(code, 3)
        self.assertIn("'journal': EINVAL: invalid absolute path", output.getvalue())
        self.assertEqual(self.snapshot(), before)

    def test_agent_observation_requires_both_exit_and_output(self):
        self.kill_forward('pause')
        before = self.snapshot()
        for rc, stdout, stderr in ((9, 'loaded', 'denied'),
                                   (9, '', 'Could not find service'), (113, '', 'other')):
            output = io.StringIO()
            with contextlib.redirect_stderr(output), patch.object(switch_effects, '_run',
                    return_value=subprocess.CompletedProcess((), rc, stdout, stderr)):
                code = switch_recover.recover(str(self.root / 'run/journal'),
                    effect_arguments=lambda action: effects(self.root, action))
            self.assertEqual(code, 3)
            self.assertIn(f'launchctl print: {rc} {stderr}', output.getvalue())
            self.assertEqual(self.snapshot(), before)

    def repair_close_failure(self, archive_close):
        self.kill_forward('pause')
        path = self.root / 'run/journal'
        with path.open('ab') as stream:
            stream.write(b'[')
        original = path.read_bytes()
        archive = path.parent / ('journal.torn-' + sha256(original).hexdigest())
        target = archive if archive_close else path
        # The newly written journal is O_WRONLY; the preliminary reader is O_RDONLY.
        import fcntl
        def matches(fd):
            return (fdsafe.live_path(fd, 'fixture') == str(target)
                    and fcntl.fcntl(fd, fcntl.F_GETFL) & os.O_ACCMODE == os.O_WRONLY)
        parsed = switch_exec.read_journal(str(path.parent))
        with fault_kit.inject_oserror('close', 1, fault_kit.ERRNOS[0], match=matches):
            with self.assertRaises(fdsafe.Refusal) as caught:
                self.repair(str(path.parent), parsed)
        self.assertEqual(caught.exception.path, str(target))
        self.assertIn('[EIO]', str(caught.exception))
        self.assertEqual(archive.read_bytes(), original)

    def test_torn_archive_close_error_is_named(self):
        self.repair_close_failure(True)

    def test_repaired_journal_close_error_is_named(self):
        self.repair_close_failure(False)

    def test_configuration_parent_rebind_is_named(self):
        self.kill_forward('pause')
        run = self.root / 'run'
        path = run / 'recovery.json'
        path.write_text(json.dumps(self.config()))
        output = io.StringIO()
        with contextlib.redirect_stderr(output), fault_kit.rename_and_rebind(
                'close', 1, run,
                match=lambda fd: fdsafe.live_path(fd, 'fixture') == str(path)):
            code = switch_recover.main(['--journal', str(run / 'journal')])
        self.assertEqual(code, 3)
        self.assertIn('is held at', output.getvalue())

    def test_stopped_torn_journal_is_not_repaired(self):
        self.kill_forward('resume')
        (self.root / 'run/pre/3').write_bytes(b'corrupt')
        with (self.root / 'run/journal').open('ab') as stream:
            stream.write(b'[')
        before = self.snapshot()
        code, output = self.run_child('recover')
        self.assertEqual(code, 3, output)
        self.assertIn('missing or changed preimage', output)
        self.assertIn('pause not held', output)
        self.assertEqual(self.snapshot(), before)

    def test_empty_journal_recovers_without_torn_archive(self):
        (self.root / 'run/journal').write_bytes(b'')
        self.restored(False)
        self.assertEqual(list((self.root / 'run').glob('journal.torn-*')), [])

    def test_complete_journal_recovers_without_torn_archive(self):
        self.kill_forward('pause')
        self.restored(False)
        self.assertEqual(list((self.root / 'run').glob('journal.torn-*')), [])

    def test_repeated_rename_inverses_keep_distinct_keys(self):
        src, dst = str(self.root / 'P'), str(self.root / 'renamed')
        switch_exec.execute((Rename(src, dst), Rename(dst, src), Rename(src, dst)),
                            str(self.root / 'run'))
        self.restored(False)

    def test_completed_backup_key_is_not_reused_for_identical_pair(self):
        code, output = self.run_child('forward')
        self.assertEqual(code, 0, output)
        run = str(self.root / 'run')
        action = next(r.action for r in switch_exec.read_journal(run).records
                      if isinstance(r, journal.Intent) and isinstance(r.action, BackupRun))
        switch_exec.execute((action,), run, effect_arguments=lambda a: effects(self.root, a))
        def stop(point, item):
            if point == 'done' and item.key == 'resync:6':
                raise InterruptedError('fixture resync completed')
        with self.assertRaises(InterruptedError):
            switch_recover.recover(run + '/journal',
                effect_arguments=lambda a: effects(self.root, a), seam=stop)
        self.restored(True)

    def test_stopped_after_resume_inverse_does_not_claim_pause_absent(self):
        code, output = self.run_child('forward')
        self.assertEqual(code, 0, output)
        def stop(point, item):
            if point == 'done' and item.key == 'undo:5':
                raise InterruptedError('fixture resume inverse completed')
        with self.assertRaises(InterruptedError):
            switch_recover.recover(str(self.root / 'run/journal'),
                effect_arguments=lambda a: effects(self.root, a), seam=stop)
        (self.root / 'run/pre/3').write_bytes(b'corrupt')
        before = self.snapshot()
        code, output = self.run_child('recover')
        self.assertEqual(code, 3, output)
        self.assertIn('missing or changed preimage', output)
        self.assertNotIn('pause not held', output)
        self.assertEqual(self.snapshot(), before)

    def test_final_verification_detects_preimage_changed_after_last_receipt(self):
        self.kill_forward('backup1')
        def corrupt(point, item):
            if point == 'done' and isinstance(item.action, Launchd):
                (self.root / 'run/pre/3').write_bytes(b'corrupt')
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            code = switch_recover.recover(str(self.root / 'run/journal'),
                effect_arguments=lambda action: effects(self.root, action), seam=corrupt)
        self.assertEqual(code, 3)
        self.assertIn('missing or changed preimage', output.getvalue())

    def test_install_absent_moves_into_undone(self):
        target = self.root / 'new'
        run = str(self.root / 'run')
        switch_exec.execute((Install(str(target), Absent(), b'installed', 0o755),), run)
        self.restored(False)
        self.assertFalse(target.exists())
        self.assertEqual((self.root / 'run/undone/1').read_bytes(), b'installed')

    def test_pending_pre_is_closed_without_inverse(self):
        target = self.root / 'new'
        def stop(point, intent):
            if point == 'intent':
                raise InterruptedError('fixture interruption')
        with self.assertRaises(InterruptedError):
            switch_exec.execute((Install(str(target), Absent(), b'installed', 0o755),),
                                str(self.root / 'run'), seam=stop)
        self.restored(False)
        records = switch_exec.read_journal(str(self.root / 'run')).records
        self.assertEqual(records[1].outcome, 'not-applied')
        self.assertFalse(target.exists())

    def test_read_faults_refuse(self):
        self.kill_forward('pause')
        for target in ('open', 'read', 'fstat', 'close', fault_kit.GETPATH):
            for err in fault_kit.ERRNOS:
                with self.subTest(target=target, errno=err):
                    with fault_kit.inject_oserror(target, 1, err):
                        self.assertEqual(switch_recover.recover(str(self.root / 'run/journal'),
                            effect_arguments=lambda action: effects(self.root, action)), 3)

    def test_unexpected_read_errors_surface(self):
        self.kill_forward('pause')
        for exception in fault_kit.UNEXPECTED:
            with fault_kit.raise_unexpected('read', 1, exception):
                with self.assertRaises(exception):
                    switch_recover.recover(str(self.root / 'run/journal'),
                        effect_arguments=lambda action: effects(self.root, action))


if __name__ == '__main__':
    if sys.argv[1:2] == ['--fake']:
        sys.exit(fake(Path(sys.argv[2]), sys.argv[3], sys.argv[4:]))
    if sys.argv[1:2] == ['--driver']:
        sys.exit(driver(Path(sys.argv[2]), sys.argv[3]))
    unittest.main()
