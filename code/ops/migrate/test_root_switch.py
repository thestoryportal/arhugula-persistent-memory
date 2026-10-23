"""T416 dependency regression: a failed PAUSE must restore its start state.

This prerequisite uses the real executor and recovery path. The command fixture
returns an error for bootout of an absent service instead of treating it as a
successful mutation. No deployment command or real repository is touched.
"""
from contextlib import redirect_stderr, redirect_stdout
import csv
import errno
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import fault_kit

from ops.migrate import fdsafe, root_manifest, root_switch, switch_exec, switch_recover
from ops.migrate.root_switch_core import Launchd


FAKE = '''import os
from pathlib import Path
import sys

root = Path(sys.argv[1])
verb = sys.argv[2]
state = root / 'agent'
if verb == '-axo':
    print(str(os.getpid()) + ' fixture-probe')
    sys.exit(0)
current = state.read_text()
if verb == 'print':
    if current == 'loaded':
        print('fixture agent loaded')
        sys.exit(0)
    print('Could not find service', file=sys.stderr)
    sys.exit(113)
if verb == 'bootout':
    if current == 'unloaded':
        print('Could not find service', file=sys.stderr)
        sys.exit(113)
    state.write_text('unloaded')
    sys.exit(0)
if verb == 'bootstrap':
    state.write_text('loaded')
    sys.exit(0)
raise RuntimeError('unexpected command: ' + repr(sys.argv))
'''


class PauseRecoveryPrerequisite(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.run = self.root / 'run'
        self.run.mkdir()
        self.command = self.root / 'command.py'
        self.command.write_text(FAKE)
        self.agent = self.root / 'agent'

    def arguments(self, action):
        command = (sys.executable, str(self.command), str(self.root))
        return {
            'LAUNCHD': dict(command=command, domain='fixture', service='agent',
                            plist=str(self.root / 'agent.plist')),
            'QUIESCE': dict(command=command, clock=lambda: 0, sleep=self.no_wait,
                            timeout=0, interval=1),
        }[action.kind]

    def no_wait(self, duration):
        self.fail('empty fixture process table must not require a wait')

    def exercise(self, start):
        self.agent.write_text(start)
        failure = None
        try:
            switch_exec.execute((Launchd(start, 'unloaded'),), str(self.run),
                                effect_arguments=self.arguments)
        except fdsafe.Refusal as exc:
            failure = str(exc)
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            code = switch_recover.recover(str(self.run / 'journal'),
                                          effect_arguments=self.arguments)
        self.assertEqual(self.agent.read_text(), start)
        self.assertEqual(code, 1, f'PAUSE: {failure}; recovery: {stderr.getvalue()}')

    def test_loaded_start_round_trip_control(self):
        self.exercise('loaded')


COMMAND = '''import json, os, shutil, sys
from pathlib import Path
base = Path(sys.argv[1])
mode, args = sys.argv[2], sys.argv[3:]
options = json.loads((base / 'options').read_text())
if mode == 'git':
    if args[-2:] == ['rev-parse', 'HEAD']:
        print(options['head'])
    elif args[-2:] == ['status', '--porcelain']:
        print(' M tracked' if options['dirty'] else '', end='')
    else:
        raise RuntimeError(args)
elif mode == 'process':
    print(str(os.getppid()) + ' fixture-switch')
    print(str(os.getpid()) + ' fixture-probe')
    if options['busy']:
        print('999 fixture-writer')
elif mode == 'reader':
    print('fixture-version')
elif mode == 'backup':
    table = Path(os.environ['BACKUP_PAIRS'])
    rows = [line.split('\\t') for line in table.read_text().splitlines()[1:]]
    for i, (backend, source, destination, excludes) in enumerate(rows):
        assert backend == 'ssd'
        src, dst = Path(source), Path(destination)
        assert src.is_relative_to(base) and dst.is_relative_to(base)
        rules = []
        for rule in Path(table.parent / excludes).read_text().splitlines():
            parts = tuple(rule.removeprefix('/').removesuffix('/').split('/'))
            if (any(c in rule for c in '*?[]\\\\ \t') or
                    any(p in ('', '.', '..') for p in parts) or
                    (not rule.startswith('/') and len(parts) != 1)):
                raise RuntimeError('unsupported exclude rule: ' + repr(rule))
            rules.append((rule.startswith('/'), rule.endswith('/'), parts))

        def inventory(root):
            found = {}
            def walk(folder):
                for p in sorted(folder.iterdir()):
                    rel = p.relative_to(root)
                    directory = p.is_dir() and not p.is_symlink()
                    if any((rel.parts == parts if anchored else rel.name == parts[0])
                           and (not dir_only or directory)
                           for anchored, dir_only, parts in rules):
                        continue
                    found[rel] = p
                    if directory:
                        walk(p)
                    elif not (p.is_symlink() or p.is_file()):
                        raise RuntimeError('unsupported file kind: ' + str(p))
            walk(root)
            return found

        def content(p):
            if p.is_symlink():
                return ('link', os.readlink(p), p.lstat().st_mode)
            if p.is_dir():
                return ('directory',)
            return ('file', p.read_bytes(), p.stat().st_mode)

        sources, targets = inventory(src), inventory(dst)
        for rel, p in targets.items():
            if p.is_dir() and not p.is_symlink():
                continue
            if rel not in sources or content(p) != content(sources[rel]):
                archive = dst / '.deleted' / options['stamp'] / rel
                archive.parent.mkdir(parents=True, exist_ok=True)
                if archive.exists() or archive.is_symlink():
                    raise RuntimeError('archive collision: ' + str(archive))
                p.rename(archive)
        for rel, p in sources.items():
            target = dst / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if p.is_symlink():
                if not target.is_symlink():
                    target.symlink_to(os.readlink(p))
                shutil.copystat(p, target, follow_symlinks=False)
            elif p.is_dir():
                target.mkdir(exist_ok=True)
            else:
                shutil.copy2(p, target)
        for rel, p in reversed(tuple(sources.items())):
            if p.is_dir() and not p.is_symlink():
                shutil.copystat(p, dst / rel)
        (dst / '.last_success').write_text(options['stamp'])
        if options['backup_fail'] and len(rows) == 2 and i == 0:
            sys.exit(7)
else:
    raise RuntimeError(mode)
'''


class RootSwitchTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.m = self.base / 'P' / 'arhugula-persistent-memory'
        self.r = self.base / 'arhugula-persistent-memory'
        self.home = self.base / 'home'
        self.run = self.base / 'run'
        self.dest = self.base / 'backup'
        self.pdest = self.dest / 'P'
        self.rdest = self.dest / 'arhugula-persistent-memory'
        self.project = self.base / 'projects' / 'M'
        self.project_new = self.base / 'projects' / 'R'
        for p in (self.m, self.home, self.run, self.pdest, self.project,
                  self.base / 'tools', self.base / 'ready'):
            p.mkdir(parents=True, exist_ok=True)
        self.rows = []
        self.authorities = []
        self.put(self.m / 'payload', b'ignored payload\0\xff', 0o600)
        self.put(self.project / 'record', b'history', 0o600)
        self.repair(self.m / 'launcher.sh', '#!/bin/bash\n# ' + str(self.m) + '\n', 0o755)
        for name in ('a', 'b'):
            lane = self.base / ('lane-' + name)
            lane.mkdir()
            gitdir = self.m / '.git' / 'worktrees' / name / 'gitdir'
            self.put(gitdir, (str(lane / '.git') + '\n').encode(), 0o644)
            self.repair(lane / '.git', 'gitdir: ' + str(gitdir.parent) + '\n')
            self.rows.append(('CHECK', str(gitdir.relative_to(self.m)), 'gitdir'))
        schemas = {
            'claude.json': (json.dumps({'projects': {str(self.m): {}}}), 'claude-project'),
            'plugins.json': (json.dumps({'plugins': {'x': [{'projectPath': str(self.m)}]}}), 'plugins-project'),
            'settings.json': (json.dumps({'permissions': {'allow': ['Read(' + str(self.m) + '/**)']}}), 'settings-rules'),
            'config.toml': ('[projects."' + str(self.m) + '"]\n', 'codex-project'),
            'agent.plist': ('<plist>' + str(self.m) + '</plist>', 'plist'),
        }
        for name, (data, kind) in schemas.items():
            self.repair(self.home / name, data, 0o600)
            self.rows.append(('CHECK', str(self.home / name), kind))
        self.repair(self.m / 'deployed.sh', '#!/bin/bash\n# ' + str(self.m) + '\n', 0o755)
        self.put(self.home / 'deployed.sh', b'old deployment\n', 0o755)
        self.rows += [('INSTALL', 'deployed.sh', str(self.home / 'deployed.sh')),
                      ('CHECK', 'executables', 'exec-bit'), ('CHECK', 'shells', 'shell-syntax'),
                      ('RENAME', str(self.project), str(self.project_new)),
                      ('RENAME', str(self.pdest / self.m.name), str(self.rdest)),
                      ('STOP', 'fixture-writer')]
        self.excludes = self.home / 'exclude'
        self.put(self.excludes, b'/.deleted/\n/.last_success\n', 0o644)
        header = 'reader\tsource\tdestination\texcludes\n'
        before = header + f'ssd\t{self.m.parent}\t{self.pdest}\texclude\n'
        after = header + f'ssd\t{self.r}\t{self.rdest}\texclude\nssd\t{self.m.parent}\t{self.pdest}\texclude\n'
        self.table = self.home / 'pairs.tsv'
        self.put(self.table, before.encode(), 0o644)
        self.rows.append(('REPLACE', str(self.table), before, after, 1))
        self.put(self.m.parent / 'other', b'parent bytes', 0o600)
        shutil.copytree(self.m, self.pdest / self.m.name)
        self.put(self.pdest / 'other', b'old parent bytes', 0o600, authoritative=False)
        self.put(self.pdest / 'obsolete', b'archive me', 0o644, authoritative=False)
        self.registry = self.base / 'registry.tsv'
        with self.registry.open('w', newline='') as stream:
            csv.writer(stream, delimiter='\t', lineterminator='\n').writerows(self.rows)
        self.authorities.append(self.registry)
        self.put(self.base / 'agent', b'loaded', 0o644, authoritative=False)
        self.put(self.base / 'launch.py', FAKE.encode(), 0o644, authoritative=False)
        self.put(self.base / 'command.py', COMMAND.encode(), 0o644, authoritative=False)
        self.options = dict(head='a' * 40, dirty=False, busy=False, backup_fail=False, stamp='fixture-stamp')
        self.save_options()
        def command(mode):
            return [sys.executable, str(self.base / 'command.py'), str(self.base), mode]
        launch = dict(command=[sys.executable, str(self.base / 'launch.py'), str(self.base)],
                      domain='fixture', service='agent', plist=str(self.home / 'agent.plist'))
        recovery = dict(LAUNCHD=launch, QUIESCE=dict(command=command('process'), timeout=0, interval=1),
                        RESYNC_P=dict(command=command('backup'), table=str(self.table), env={}, timeout=10),
                        BACKUP_COMPARE=dict(displaced=[[str(self.pdest), 'other',
                            __import__('hashlib').sha256(b'old parent bytes').hexdigest()],
                            [str(self.pdest), 'obsolete', __import__('hashlib').sha256(b'archive me').hexdigest()]]))
        self.config = dict(m=str(self.m), r=str(self.r), home=str(self.home), run=str(self.run),
                           registry=str(self.registry), tools=str(self.base / 'tools'), ready=str(self.base / 'ready'),
                           pinned_sha='a' * 40, git=command('git'), process=command('process'),
                           python=sys.executable, recovery=recovery,
                           backup=dict(command=command('backup'), table=str(self.table), env={}, timeout=10),
                           pairs=[['ssd', str(self.r), str(self.rdest), str(self.excludes)],
                                  ['ssd', str(self.m.parent), str(self.pdest), str(self.excludes)]],
                           stamp='fixture-stamp', parent_backup=str(self.pdest),
                           scan_roots=[str(self.home / name) for name in ()],
                           reader_commands={key: command('reader') for key in ('plutil', 'bash', 'zsh', 'git')})
        # Disjoint scans include home configuration, the renamed project folder,
        # and each linked worktree. Keep project outside the home scan boundary.
        self.config['scan_roots'] = [str(self.home), str(self.project), str(self.base / 'lane-a'), str(self.base / 'lane-b')]
        self.config_path = self.base / 'config.json'
        self.start = self.snapshot()

    def put(self, path, data, mode, authoritative=True):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(mode)
        if authoritative:
            self.authorities.append(path)

    def repair(self, path, data, mode=0o644):
        self.put(path, data.encode(), mode)
        key = str(path.relative_to(self.m)) if path.is_relative_to(self.m) else str(path)
        self.rows.append(('REPLACE', key, str(self.m), str(self.r), data.count(str(self.m))))

    def save_options(self):
        (self.base / 'options').write_text(json.dumps(self.options))

    def snapshot(self):
        return {str(p): (p.read_bytes(), p.stat().st_mode & 0o7777) for p in self.authorities}

    def call(self, mode='--run', seam=lambda *args: None):
        self.config_path.write_text(json.dumps(self.config))
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = root_switch.main([mode, '--config', str(self.config_path)], seam=seam)
        return code, out.getvalue() + err.getvalue()

    def assert_restored(self, code, text):
        self.assertEqual(code, 1, text)
        self.assertNotIn('PASS', text)
        self.assertEqual(self.snapshot(), self.start)
        self.assertFalse(self.r.exists())
        self.assertEqual((self.base / 'agent').read_text(), 'loaded')
        self.assert_content_equal(self.m, self.pdest / self.m.name)

    def assert_content_equal(self, source, destination):
        def content(root):
            with fdsafe.hold_root(str(root)) as held:
                leaves = root_manifest.build_manifest(str(root), held.fd)['leaves']
            return {str(Path(leaf['source']).relative_to(root)):
                    tuple(leaf[key] for key in ('kind', 'bytes', 'sha256', 'mode', 'link_text'))
                    for leaf in leaves}
        self.assertEqual(content(source), content(destination))

    def fake_backup(self, table=None):
        return subprocess.run(self.config['backup']['command'],
                              env=dict(os.environ, BACKUP_PAIRS=str(table or self.table)),
                              capture_output=True, text=True, timeout=10)

    def test_fake_resync_archives_nested_metadata_and_preserves_anchored_metadata(self):
        src, dst = self.base / 'fake-source', self.base / 'fake-dest'
        src.mkdir()
        dst.mkdir()
        nested = {'sub/.deleted/x': (b'nested deleted', 0o600),
                  'sub/.last_success': (b'nested stamp', 0o640),
                  '.deleted-sibling': (b'prefix is not a component', 0o644),
                  '.last_success-sibling': (b'prefix is not a component', 0o644),
                  'changed': (b'old', 0o600)}
        for rel, (data, mode) in nested.items():
            self.put(dst / rel, data, mode, authoritative=False)
        self.put(dst / '.deleted/old/keep', b'keep archive', 0o600, authoritative=False)
        self.put(dst / '.last_success', b'previous stamp', 0o600, authoritative=False)
        self.put(src / '.last_success', b'excluded source stamp', 0o644, authoritative=False)
        self.put(src / '.deleted/no-copy', b'excluded source archive', 0o644, authoritative=False)
        self.put(src / 'changed', b'new', 0o755, authoritative=False)
        (src / 'link').symlink_to('missing-target')
        (dst / 'link').symlink_to('old-target')
        table = self.home / 'fake-pairs.tsv'
        table.write_text(f'reader\tsource\tdestination\texcludes\nssd\t{src}\t{dst}\texclude\n')
        result = self.fake_backup(table)
        self.assertEqual(result.returncode, 0, result.stderr)
        archive = dst / '.deleted/fixture-stamp'
        for rel, (data, mode) in nested.items():
            self.assertEqual((archive / rel).read_bytes(), data)
            self.assertEqual((archive / rel).stat().st_mode & 0o7777, mode)
            if rel != 'changed':
                self.assertFalse((dst / rel).exists())
        self.assertEqual((dst / '.deleted/old/keep').read_bytes(), b'keep archive')
        self.assertFalse((dst / '.deleted/no-copy').exists())
        self.assertFalse((archive / '.last_success').exists())
        self.assertEqual((dst / '.last_success').read_text(), 'fixture-stamp')
        self.assertEqual((dst / '.last_success').stat().st_mode & 0o7777, 0o600)
        self.assertEqual((dst / 'changed').read_bytes(), b'new')
        self.assertEqual((dst / 'changed').stat().st_mode & 0o7777, 0o755)
        self.assertTrue((dst / 'link').is_symlink())
        self.assertEqual(os.readlink(dst / 'link'), 'missing-target')
        self.assertEqual(os.readlink(archive / 'link'), 'old-target')

    def test_fake_rejects_unsupported_rules_before_copying(self):
        self.excludes.write_text('**/wildcard\n')
        before = (self.pdest / 'other').read_bytes()
        result = self.fake_backup()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('unsupported exclude rule', result.stderr)
        self.assertEqual((self.pdest / 'other').read_bytes(), before)

    def test_invalid_configuration_is_a_read_only_refusal(self):
        original = self.config.copy()
        cases = [('extra', True, 'configuration keys'), ('git', [], 'empty command'),
                 ('process', [], 'empty command'), ('stamp', '', 'empty stamp'),
                 ('backup', {}, 'expected command'), ('reader_commands', [], 'expected object'),
                 ('pairs', [], 'both SSD pairs'), ('run', str(self.m), 'inside an input root'),
                 ('m', str(self.m) + '/', 'canonical absolute path'),
                 ('scan_roots', ['relative'], 'canonical absolute path')]
        for key, value, message in cases:
            with self.subTest(key=key, value=value):
                self.config = dict(original, **{key: value})
                code, text = self.call('--dry-run')
                self.assertEqual(code, 2, text)
                self.assertIn(message, text)
                self.assertEqual(self.snapshot(), self.start)
                self.assertEqual(list(self.run.iterdir()), [])
        self.config = original

    def test_invalid_json_and_missing_config_are_distinct_refusals(self):
        for content, message in (('{', 'invalid configuration JSON'), (None, 'ENOENT')):
            path = self.base / ('invalid.json' if content is not None else 'absent.json')
            if content is not None:
                path.write_text(content)
            err = io.StringIO()
            with redirect_stderr(err):
                code = root_switch.main(['--dry-run', '--config', str(path)])
            self.assertEqual(code, 2)
            self.assertIn(message, err.getvalue())

    def test_unexpected_read_and_stage_errors_are_not_reclassified(self):
        with fault_kit.raise_unexpected('read', 1, RuntimeError):
            with self.assertRaisesRegex(RuntimeError, 'fault_kit'):
                self.call('--dry-run')
        def seam(point, item):
            if point == 'stage':
                raise RuntimeError('unexpected fixture stage error')
        with self.assertRaisesRegex(RuntimeError, 'unexpected fixture stage error'):
            self.call(seam=seam)

    def test_process_probe_refusals_name_the_observation(self):
        cases = [('import sys; sys.exit(7)', 'command exit 7'),
                 ('import sys; sys.stdout.buffer.write(bytes([255]))', 'not UTF-8'),
                 ('print("0 invalid")', 'malformed process line'),
                 ('print("123 unrelated")', 'does not list its own caller pid')]
        for program, message in cases:
            with self.subTest(program=program):
                self.config['process'] = [sys.executable, '-c', program]
                code, text = self.call('--dry-run')
                self.assertEqual(code, 2, text)
                self.assertIn(message, text)
                self.assertEqual(self.snapshot(), self.start)

    def test_command_missing_and_timeout_are_distinct_refusals(self):
        self.config['process'] = [str(self.base / 'missing-command')]
        code, text = self.call('--dry-run')
        self.assertEqual(code, 2, text)
        self.assertIn('ENOENT', text)
        # [LAW:behavior-not-structure] Inject the command boundary's documented
        # timeout directly; no clock, sleep or product function is replaced.
        with patch('subprocess.run', side_effect=subprocess.TimeoutExpired('fixture', 10)):
            code, text = self.call('--dry-run')
        self.assertEqual(code, 2, text)
        self.assertIn('ETIMEDOUT', text)

    def test_missing_install_source_names_the_source(self):
        (self.m / 'deployed.sh').rename(self.m / 'saved-source')
        code, text = self.call('--dry-run')
        self.assertEqual(code, 2, text)
        self.assertIn('deployed.sh', text)
        self.assertIn('INSTALL source absent', text)

    def test_measured_repair_counts_reach_the_post_scan(self):
        self.rows = [(*row[:4], 'measured') if row[0] == 'REPLACE' and row[1] == 'launcher.sh'
                     else row for row in self.rows]
        with self.registry.open('w', newline='') as stream:
            csv.writer(stream, delimiter='\t', lineterminator='\n').writerows(self.rows)
        code, text = self.call()
        self.assertEqual(code, 0, text)
        report = json.loads((self.run / 'post-readers.json').read_text())
        pre = json.loads((self.run / 'pre-readers.json').read_text())
        self.assertEqual(pre['measured_counts'], [[0, 1]])
        self.assertEqual(report['findings'], [])
        self.assertIn(str(self.project_new), report['scan_roots'])

    def test_unavailable_reader_command_rolls_back(self):
        self.config['reader_commands']['plutil'] = []
        code, text = self.call()
        self.assert_restored(code, text)
        self.assertIn('READER_CHECKS', text)
        self.assertIn('explicit reader command unavailable', (self.run / 'checks.tsv').read_text())

    def test_changed_success_stamp_rolls_back(self):
        self.config['stamp'] = 'different-stamp'
        code, text = self.call()
        self.assert_restored(code, text)
        self.assertIn('differs from run stamp', text)

    def test_non_utf8_stamp_is_never_silently_replaced(self):
        self.config['stamp'] = '\ud800'
        # [LAW:no-silent-failure] Invalid stamp bytes cannot enter the transaction.
        code, text = self.call()
        self.assertEqual(code, 2, text)
        self.assertIn('stamp is not UTF-8', text)
        self.assertNotIn('PASS', text)
        self.assertEqual(self.snapshot(), self.start)
        self.assertEqual(list(self.run.iterdir()), [])
        self.assertEqual((self.base / 'agent').read_text(), 'loaded')

    def test_post_scan_failure_rolls_back_and_names_it(self):
        def seam(point, item):
            if point == 'stage' and item == 'ROOT_READERS':
                (self.home / 'unregistered').write_text(str(self.m))
        code, text = self.call(seam=seam)
        self.assert_restored(code, text)
        self.assertIn('root_readers exit 1', text)

    def test_conservation_failure_rolls_back(self):
        def seam(point, item):
            if point == 'stage' and item == 'MANIFEST_R':
                (self.r / 'extra').write_bytes(b'unregistered bytes')
        code, text = self.call(seam=seam)
        self.assertEqual(code, 1, text)
        self.assertIn('CONSERVATION:', text)
        self.assertNotIn('PASS', text)
        self.assertEqual((self.m / 'extra').read_bytes(), b'unregistered bytes')
        self.assertEqual(self.snapshot(), self.start)

    def test_process_whitespace_and_command_tail_are_preserved(self):
        self.config['process'] = [sys.executable, '-c',
            'import os; print(str(os.getppid()) + "\\tfixture-switch"); '
            'print("987 arbitrary prefix fixture-writer suffix")']
        code, text = self.call('--dry-run')
        self.assertEqual(code, 1, text)
        self.assertIn('STOP fixture-writer: (987,)', text)

    def test_parent_backup_repo_archive_is_refused(self):
        def seam(point, item):
            if point == 'done' and item.action.kind == 'BACKUP_RUN':
                path = self.pdest / '.deleted/extra' / self.r.name / 'unexpected'
                self.put(path, b'wrongly archived', 0o600, authoritative=False)
        code, text = self.call(seam=seam)
        self.assert_restored(code, text)
        self.assertIn('repo archived under parent backup', text)

    def test_lock_and_ready_markers_fail_preconditions(self):
        (self.base / 'tools/active.lock').write_bytes(b'held')
        (self.base / 'ready/marker').write_bytes(b'ready')
        code, text = self.call()
        self.assert_restored(code, text)
        self.assertIn('L/tools lock:', text)
        self.assertIn('ready marker:', text)
        self.assertNotIn('\nPAUSE\n', text)

    def test_ordinary_tools_entry_is_not_a_lock(self):
        (self.base / 'tools/readme').write_bytes(b'not a lock')
        code, text = self.call('--dry-run')
        self.assertEqual(code, 0, text)

    def test_moved_probe_directory_is_refused(self):
        tools = self.base / 'tools'
        identity = tools.stat().st_ino
        with fault_kit.rename_and_rebind('scandir', 1, str(tools), when='after',
                match=lambda fd: isinstance(fd, int) and os.fstat(fd).st_ino == identity):
            code, text = self.call('--dry-run')
        self.assertEqual(code, 2, text)
        self.assertIn('is held at', text)
        self.assertEqual(self.snapshot(), self.start)

    def test_created_recovery_config_close_error_is_loud(self):
        with fault_kit.inject_oserror('close', 1, errno.EIO,
                match=lambda fd: fdsafe.live_path(fd, 'close probe') == str(self.run / 'recovery.json')):
            code, text = self.call()
        self.assertEqual(code, 2, text)
        self.assertIn('EIO', text)
        self.assertIn('recovery.json', text)
        self.assertEqual(self.snapshot(), self.start)

    def test_stopped_recovery_after_resume_passes_pause_not_held_through(self):
        def seam(point, item):
            if point == 'done' and isinstance(item.action, Launchd) and item.action.to_state == 'loaded':
                records = switch_exec.read_journal(str(self.run)).records
                preimage = next(record.action.pre.preimage for record in records
                                if hasattr(record, 'action') and record.action.kind == 'REPLACE')
                Path(preimage).write_bytes(b'changed preimage')
                raise fdsafe.Refusal('RESUME', 'EIO: fixture stop after resume')
        code, text = self.call(seam=seam)
        self.assertEqual(code, 3, text)
        self.assertIn('missing or changed preimage', text)
        self.assertIn('agent loaded; pause not held; no inverse applied', text)
        self.assertEqual((self.base / 'agent').read_text(), 'loaded')
        self.assertNotIn('PASS', text)

    def test_run_order_and_authoritative_modes(self):
        events = []
        code, text = self.call(seam=lambda point, item: events.append(item) if point == 'stage' else None)
        self.assertEqual(code, 0, text)
        self.assertEqual(events, ['PRECONDITIONS', 'PAUSE', 'QUIESCE', 'MANIFEST_M', 'MOVE', 'REPAIR',
                                  'MANIFEST_R', 'CONSERVATION', 'ROOT_READERS', 'READER_CHECKS',
                                  'BACKUP_RUN', 'RESUME'])
        self.assertEqual(text.splitlines(), events + ['PASS'])
        self.assertFalse(self.m.exists())
        self.assertEqual((self.base / 'agent').read_text(), 'loaded')
        for path, (data, mode) in self.start.items():
            new = path.replace(str(self.m), str(self.r)).replace(str(self.project), str(self.project_new))
            expected = data.replace(str(self.m).encode(), str(self.r).encode())
            if path == str(self.registry):
                expected = data
            if path == str(self.table):
                expected = self.rows[-1][3].encode()
            if path == str(self.home / 'deployed.sh'):
                expected = (self.r / 'deployed.sh').read_bytes()
            self.assertEqual(Path(new).read_bytes(), expected, new)
            self.assertEqual(Path(new).stat().st_mode & 0o7777, mode, new)
        for dst in (self.pdest, self.rdest):
            self.assertEqual((dst / '.last_success').read_text(), 'fixture-stamp')
        self.assertFalse(any(self.m.name in p.parts for p in (self.pdest / '.deleted').rglob('*')))

    def test_unloaded_start_stops_at_pause_with_service_and_no_later_stage(self):
        (self.base / 'agent').write_text('unloaded')
        events = []
        code, text = self.call(seam=lambda point, item: events.append(item) if point == 'stage' else None)
        self.assertEqual(code, 3, text)
        self.assertIn('PAUSE', text)
        self.assertIn('fixture/agent', text)
        self.assertNotIn('PASS', text)
        self.assertEqual(events, ['PRECONDITIONS', 'PAUSE'])
        self.assertEqual((self.base / 'agent').read_text(), 'unloaded')
        self.assertEqual(self.snapshot(), self.start)

    def test_failed_precondition_rolls_back_without_move(self):
        self.options['dirty'] = True
        self.save_options()
        code, text = self.call()
        self.assert_restored(code, text)
        self.assertIn('PRECONDITIONS', text)
        self.assertIn('dirty', text)

    def test_failed_deploy_restores_bytes_and_modes(self):
        def seam(point, item):
            if point == 'intent' and item.direction == 'forward' and item.action.kind == 'INSTALL':
                raise fdsafe.Refusal('deploy', 'EIO: fixture deploy failure')
        code, text = self.call(seam=seam)
        self.assert_restored(code, text)
        self.assertIn('REPAIR', text)

    def test_failed_resume_check_restores_and_resyncs(self):
        def seam(point, item):
            if point == 'mutation' and item.direction == 'forward' and isinstance(item.action, Launchd) and item.action.to_state == 'loaded':
                raise fdsafe.Refusal('RESUME', 'EIO: fixture check failure')
        code, text = self.call(seam=seam)
        self.assert_restored(code, text)
        self.assertEqual((self.pdest / self.m.name / 'payload').read_bytes(), (self.m / 'payload').read_bytes())
        self.assertEqual((self.pdest / '.deleted' / 'fixture-stamp' / 'other').read_bytes(), b'old parent bytes')
        self.assertEqual((self.pdest / '.deleted' / 'fixture-stamp' / 'obsolete').read_bytes(), b'archive me')

    def test_backup_failure_after_first_pair_restores_and_resyncs(self):
        self.options['backup_fail'] = True
        self.save_options()
        code, text = self.call()
        self.assert_restored(code, text)
        self.assertIn('BACKUP_RUN', text)
        self.assertEqual((self.pdest / 'other').read_bytes(), b'parent bytes')
        self.assertEqual((self.pdest / '.deleted' / 'fixture-stamp' / 'obsolete').read_bytes(), b'archive me')
        self.assertEqual((self.pdest / '.deleted' / 'fixture-stamp' / 'other').read_bytes(), b'old parent bytes')

    def test_newer_work_is_kept_and_recovery_exits_three(self):
        def seam(point, item):
            if point == 'stage' and item == 'CONSERVATION':
                (self.r / 'launcher.sh').write_bytes(b'newer work')
                raise fdsafe.Refusal('newer', 'EIO: stop')
        code, text = self.call(seam=seam)
        self.assertEqual(code, 3, text)
        self.assertEqual((self.r / 'launcher.sh').read_bytes(), b'newer work')
        self.assertNotIn('PASS', text)
        self.assertEqual((self.base / 'agent').read_text(), 'unloaded')

    def test_dry_run_is_read_only(self):
        before = {str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
        code, text = self.call('--dry-run')
        self.assertEqual(code, 0, text)
        after = {str(p): p.read_bytes() for p in self.base.rglob('*') if p.is_file() and p != self.config_path}
        self.assertEqual(after, before)
        self.assertEqual(self.snapshot(), self.start)

    def test_copied_code_runs_with_external_python(self):
        import ast
        import importlib.util
        copied = self.run / 'code'
        self.assertFalse(Path(sys.executable).is_relative_to(self.m))
        pending = ['ops.migrate.root_switch']
        seen = set()
        while pending:
            name = pending.pop()
            if name in seen:
                continue
            seen.add(name)
            origin = Path(importlib.util.find_spec(name).origin)
            target = copied.joinpath(*name.split('.')).with_suffix('.py')
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origin, target)
            tree = ast.parse(origin.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith('ops.migrate'):
                    if node.module == 'ops.migrate':
                        pending.extend(node.module + '.' + alias.name for alias in node.names)
                    else:
                        pending.append(node.module)
        self.config_path.write_text(json.dumps(self.config))
        result = subprocess.run([sys.executable, '-B', '-m', 'ops.migrate.root_switch', '--run',
                                 '--config', str(self.config_path)], cwd=self.run,
                                env=dict(os.environ, PYTHONPATH=str(copied)), capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(self.m.exists())
        self.assertTrue(self.r.exists())
        self.assertIn('PASS', result.stdout)


if __name__ == '__main__':
    unittest.main()
