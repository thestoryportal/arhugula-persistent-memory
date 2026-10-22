"""T415: fixture-only reader checks; no real home, git or workflow runs."""
import ast
import contextlib
import csv
import errno
import io
import inspect
import json
import os
from pathlib import Path
import plistlib
import stat
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import fault_kit
from ops.migrate import root_reader_checks as checks


class Readers(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name).resolve()
        self.root = self.base / 'root'
        self.root.mkdir()
        self.home = self.base / 'home'
        self.home.mkdir()
        self.old = str(self.base / 'old')
        self.registry = self.base / 'registry.tsv'
        self.out = self.base / 'receipt.tsv'
        self.calls = []
        self.reply = (0, b'version 1\n')

    def file(self, path, data, mode=0o644):
        p = Path(path)
        if not p.is_absolute():
            p = self.root / p
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data.encode() if isinstance(data, str) else data)
        p.chmod(mode)
        return str(p)

    def runner(self, command):
        self.calls.append(command)
        self.assertEqual(dict(command.env)['HOME'], str(self.home))
        self.assertEqual(dict(command.env)['PYTHONDONTWRITEBYTECODE'], '1')
        if command.argv[0] == 'plutil' or (command.argv[0] in ('bash', 'zsh') and '-n' in command.argv):
            result = subprocess.run(command.argv, input=command.stdin, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, check=False)
            return checks.Output(result.returncode, result.stdout)
        return checks.Output(*self.reply)

    def run_rows(self, rows, expected=0, runner=None):
        stream = io.StringIO(newline='')
        csv.writer(stream, delimiter='\t', lineterminator='\n').writerows(rows)
        self.registry.write_text(stream.getvalue())
        before = self.snapshot()
        err = io.StringIO()
        status = checks.main(['--root', str(self.root), '--old-root', self.old,
                              '--registry', str(self.registry), '--out', str(self.out)],
                             home=str(self.home), runner=runner or self.runner, stderr=err)
        self.assertEqual(status, expected, err.getvalue())
        self.assertEqual(self.snapshot(), before)
        result = list(csv.reader(io.StringIO(self.out.read_text()), delimiter='\t'))
        self.assertEqual(result[0], ['path', 'check', 'status', 'detail'])
        self.assertEqual(len(result)-1, sum(row[0] == 'CHECK' for row in rows))
        return result[1:]

    def snapshot(self):
        return {str(p.relative_to(self.base)): (stat.S_IMODE(p.lstat().st_mode),
                p.read_bytes() if p.is_file() else None)
                for folder in (self.root, self.home) for p in [folder, *folder.rglob('*')]}

    def single(self, kind, data, expected='PASS', path='reader', mode=0o644):
        p = self.file(path, data, mode)
        rows = self.run_rows([['CHECK', p, kind]], int(expected != 'PASS'))
        self.assertEqual(rows[0][2], expected)
        return rows[0]

    def test_claude_pass(self):
        self.single('claude-project', json.dumps({'projects': {str(self.root): {}}}))

    def test_claude_missing(self):
        self.single('claude-project', '{"projects": {}}', 'FAIL')

    def test_claude_parent_is_not_root(self):
        self.single('claude-project', json.dumps({'projects': {str(self.base): {}}}), 'FAIL')

    def test_claude_wrong_schema(self):
        self.single('claude-project', json.dumps({'projects': [str(self.root)]}), 'FAIL')

    def test_plugins_pass(self):
        self.single('plugins-project', json.dumps({'version': 2, 'plugins': {'x': [
            {'scope': 'project', 'projectPath': str(self.root)}]}}))

    def test_plugins_wrong_path(self):
        self.single('plugins-project', json.dumps({'plugins': {'x': [
            {'projectPath': str(self.root)+'x'}]}}), 'FAIL')

    def test_plugins_unrelated_nested_key(self):
        self.single('plugins-project', json.dumps({'other': {'projectPath': str(self.root)}}), 'FAIL')

    def test_settings_pass(self):
        self.single('settings-rules', json.dumps({'permissions': {'allow': [
            'Bash(cd '+str(self.root)+' && ls)', 'Read('+str(self.root)+'/**)', 'Bash(ls:*)']}}))

    def test_settings_old_even_with_new(self):
        self.single('settings-rules', json.dumps({'permissions': {'allow': [
            'Read('+self.old+'/**)', 'Read('+str(self.root)+'/**)']}}), 'FAIL')

    def test_settings_parent(self):
        self.single('settings-rules', json.dumps({'permissions': {'allow': [
            'Read('+str(self.base)+'/**)']}}), 'FAIL')

    def test_settings_prefix(self):
        self.single('settings-rules', json.dumps({'permissions': {'allow': [
            'Read('+str(self.root)+'x/**)']}}), 'FAIL')

    def test_settings_count_from_registry(self):
        p = self.file('settings', json.dumps({'permissions': {'allow': ['Read('+str(self.root)+'/**)']}}))
        self.run_rows([['REPLACE', p, self.old, str(self.root), '2'], ['CHECK', p, 'settings-rules']], 1)

    def test_settings_old_shell_delimiter(self):
        self.single('settings-rules', json.dumps({'permissions': {'allow': [
            'Bash(cd '+self.old+'; ls)', 'Read('+str(self.root)+'/**)']}}), 'FAIL')

    def test_settings_count_exact_occurrences(self):
        p = self.file('settings', json.dumps({'permissions': {'allow': [
            'Bash(echo '+str(self.root)+' '+str(self.root)+'-sibling)']}}))
        self.run_rows([['REPLACE', p, self.old, str(self.root), '2'], ['CHECK', p, 'settings-rules']], 1)

    def test_toml_pass(self):
        self.single('codex-project', '[projects."'+str(self.root)+'"]\ntrust_level="trusted"\n')

    def test_toml_parse_error(self):
        self.single('codex-project', '[projects.', 'FAIL')

    def test_toml_parent(self):
        self.single('codex-project', '[projects."'+str(self.base)+'"]\n', 'FAIL')

    def test_json_parse_error(self):
        self.single('claude-project', '{', 'FAIL')

    def test_bad_utf8(self):
        self.single('claude-project', b'\xff', 'FAIL')

    def test_plist_pass_real_plutil(self):
        self.single('plist', plistlib.dumps({'Label': 'fixture'}))

    def test_plist_broken_real_plutil(self):
        self.single('plist', '<plist><dict>', 'FAIL')

    def test_exec_pass(self):
        p = self.file('teamdash', '#!/bin/bash\n', 0o755)
        self.run_rows([['REPLACE', p, 'old', 'new', '1'], ['CHECK', 'executables', 'exec-bit']])

    def test_exec_0600(self):
        p = self.file('teamdash', '#!/bin/bash\n', 0o600)
        rows = self.run_rows([['REPLACE', p, 'old', 'new', '1'], ['CHECK', 'executables', 'exec-bit']], 1)
        self.assertIn(p, rows[0][3])

    def test_exec_every_launcher_and_install(self):
        a = self.file('.venv/bin/hf', '#!/python\n', 0o755)
        b = self.file(self.home/'bin/backup.sh', '#!/bin/bash\n', 0o600)
        self.run_rows([['REPLACE', a, 'old', 'new', '1'], ['INSTALL', 'src', b],
                       ['CHECK', 'executables', 'exec-bit']], 1)

    def test_activation_is_not_launcher(self):
        a = self.file('.venv/bin/activate', 'export PATH=x', 0o644)
        b = self.file('.venv/bin/hf', '#!/python\n', 0o755)
        self.run_rows([['REPLACE', a, 'x', 'y', '1'], ['REPLACE', b, 'x', 'y', '1'],
                       ['CHECK', 'executables', 'exec-bit']])

    def shell(self, source, expected=0):
        p = self.file('tools/tool.sh', source, 0o755)
        return self.run_rows([['REPLACE', p, 'old', 'new', '1'],
                              ['CHECK', 'shell-scripts', 'shell-syntax']], expected)

    def test_bash_syntax_pass(self):
        self.shell('#!/bin/bash\necho ok\n')
        self.assertEqual(self.calls[0].argv, ('bash', '-n'))

    def test_bash_syntax_fail(self):
        self.shell('#!/bin/bash\nif then\n', 1)

    def test_zsh_syntax_pass(self):
        self.shell('#!/usr/bin/env zsh\nprint ok\n')
        self.assertEqual(self.calls[0].argv, ('zsh', '-n'))

    def test_zsh_syntax_fail(self):
        self.shell('#!/bin/zsh\nif then\n', 1)

    def test_unknown_shell_unavailable(self):
        self.assertEqual(self.shell('#!/bin/fish\n', 1)[0][2], 'UNAVAILABLE')

    def test_malformed_shebang_continues(self):
        p = self.file('bad.sh', '#!/bin/bash "\n')
        rows = self.run_rows([['REPLACE', p, 'x', 'y', '1'], ['CHECK', 'shell-scripts', 'shell-syntax'],
                              ['CHECK', 'x', 'unknown']], 1)
        self.assertEqual(rows[0][2], 'FAIL')

    def test_check_only_scripts_are_executable_members(self):
        p = self.file('test_train.sh', '#!/bin/bash\nROOT=${ROOT:-/old}\n', 0o600)
        rows = self.run_rows([['CHECK', p, 'test-train'], ['CHECK', 'executables', 'exec-bit']], 1)
        self.assertEqual(rows[1][2], 'FAIL')

    def test_python_not_shell(self):
        p = self.file('.venv/bin/hf', '#!/usr/bin/python\nnot shell', 0o755)
        q = self.file('ok.sh', '#!/bin/bash\ntrue\n')
        self.run_rows([['REPLACE', p, 'a', 'b', '1'], ['REPLACE', q, 'a', 'b', '1'],
                       ['CHECK', 'shell-scripts', 'shell-syntax']])
        self.assertEqual(len(self.calls), 1)

    def test_gitdir_pass(self):
        lane = self.file(self.base/'lane/.git', 'placeholder\n')
        gitdir = self.file('.git/worktrees/lane/gitdir', lane+'\n')
        self.file(lane, 'gitdir: '+str(Path(gitdir).parent)+'\n')
        self.run_rows([['CHECK', '.git/worktrees/lane/gitdir', 'gitdir']])

    def test_gitdir_wrong_roundtrip(self):
        lane = self.file(self.base/'lane/.git', 'gitdir: wrong\n')
        p = self.file('.git/worktrees/lane/gitdir', lane+'\n')
        result = self.run_rows([['CHECK', p, 'gitdir']], 1)
        self.assertIn('gitdir: wrong', result[0][3])
        self.assertIn(lane, result[0][3])

    def test_gitdir_multiline(self):
        self.single('gitdir', '/fake/.git\nextra\n', 'FAIL')

    def test_gitdir_noncanonical_continues(self):
        p = self.file('.git/worktrees/lane/gitdir', str(self.base)+'/../lane/.git\n')
        rows = self.run_rows([['CHECK', p, 'gitdir'], ['CHECK', 'x', 'unknown']], 1)
        self.assertEqual(rows[0][2], 'FAIL')

    def test_gitdir_requires_dot_git_file(self):
        gitdir = self.root/'.git/worktrees/lane/gitdir'
        other = self.file(self.base/'lane/not-git', 'gitdir: '+str(gitdir.parent)+'\n')
        self.file(gitdir, other+'\n')
        self.run_rows([['CHECK', str(gitdir), 'gitdir']], 1)

    def test_lane_status_command(self):
        p = self.file(self.base/'lane/.git', 'gitdir: unused\n')
        self.run_rows([['REPLACE', p, 'old', 'new', '1'], ['CHECK', 'lane-worktrees', 'lane-status']])
        self.assertEqual(self.calls[0].argv, ('git', '--no-optional-locks', '-C', str(Path(p).parent), 'status', '--porcelain'))
        self.assertEqual(dict(self.calls[0].env)['GIT_OPTIONAL_LOCKS'], '0')

    def test_lane_status_failure(self):
        self.reply = (128, b'fatal: broken lane\n')
        p = self.file(self.base/'lane/.git', 'gitdir: unused\n')
        rows = self.run_rows([['REPLACE', p, 'old', 'new', '1'], ['CHECK', 'lane-worktrees', 'lane-status']], 1)
        self.assertIn('fatal: broken lane', rows[0][3])

    def test_venv_pass(self):
        self.reply = (0, (str(self.root/'.venv')+'\n').encode())
        self.run_rows([['CHECK', '.venv/bin/python', 'venv-prefix']])
        self.assertEqual(self.calls[0].argv, (str(self.root/'.venv/bin/python'), '-B', '-c', 'import sys; print(sys.prefix)'))

    def test_venv_wrong_prefix(self):
        self.reply = (0, (str(self.root/'.venv')+'x\n').encode())
        self.run_rows([['CHECK', '.venv/bin/python', 'venv-prefix']], 1)

    def test_console_pass(self):
        self.run_rows([['CHECK', '.venv/bin/hf', 'console-version']])
        self.assertEqual(self.calls[0].argv, (str(self.root/'.venv/bin/hf'), '--version'))

    def test_console_empty(self):
        self.reply = (0, b' \n')
        self.run_rows([['CHECK', '.venv/bin/hf', 'console-version']], 1)

    def test_console_nonzero(self):
        self.reply = (3, b'version 1')
        self.run_rows([['CHECK', '.venv/bin/hf', 'console-version']], 1)

    def test_ship_no_root(self):
        self.single('test-ship', '#!/bin/bash\ntrue\n', 'UNAVAILABLE')
        self.assertEqual(self.calls, [])

    def test_train_root_override(self):
        p = self.file('test_train.sh', '#!/bin/bash\nROOT=${ROOT:-/old}\n')
        self.run_rows([['CHECK', p, 'test-train']])
        self.assertEqual(dict(self.calls[0].env)['ROOT'], str(self.root))
        self.assertEqual(self.calls[0].argv, ('bash', '-c', '#!/bin/bash\nROOT=${ROOT:-/old}\n', p))

    def test_ship_rootish_not_override(self):
        self.single('test-ship', '#!/bin/bash\nROOTISH=1\n# ROOT\n', 'UNAVAILABLE')

    def test_root_assignment_discards_override(self):
        self.single('test-ship', '#!/bin/bash\nROOT=/old\necho "$ROOT"\n', 'UNAVAILABLE')
        self.assertEqual(self.calls, [])

    def test_unknown_class_and_duplicate_rows(self):
        rows = self.run_rows([['CHECK', 'x', 'new-class'], ['CHECK', 'x', 'new-class']], 1)
        self.assertTrue(all(r[2] == 'UNAVAILABLE' and 'new-class' in r[3] for r in rows))

    def test_empty_group_not_pass(self):
        self.run_rows([['CHECK', 'executables', 'exec-bit']], 1)

    def test_missing_reader_and_continues(self):
        rows = self.run_rows([['CHECK', 'missing', 'claude-project'], ['CHECK', 'x', 'future']], 1)
        self.assertEqual([r[2] for r in rows], ['UNAVAILABLE', 'UNAVAILABLE'])
        self.assertIn('ENOENT', rows[0][3])

    def test_missing_command(self):
        def missing(command):
            raise FileNotFoundError(errno.ENOENT, 'missing executable')
        rows = self.run_rows([['CHECK', '.venv/bin/hf', 'console-version']], 1, missing)
        self.assertIn('ENOENT', rows[0][3])

    def refusal(self, args=None):
        err = io.StringIO()
        argv = args if args is not None else ['--root', str(self.root), '--old-root', self.old,
            '--registry', str(self.registry), '--out', str(self.out)]
        self.assertEqual(checks.main(argv, home=str(self.home), runner=self.runner, stderr=err), 2)
        self.assertEqual(len(err.getvalue().splitlines()), 1)
        return err.getvalue()

    def test_unreadable_registry(self):
        self.assertIn('ENOENT', self.refusal())

    def test_bad_registry(self):
        self.registry.write_text('bad\n')
        self.assertIn('EINVAL', self.refusal())

    def test_bad_arguments(self):
        self.assertIn('EINVAL', self.refusal([]))

    def test_out_inside_root(self):
        self.registry.write_text('CHECK\tx\tfuture\n')
        self.out = self.root/'receipt'
        self.assertIn(str(self.out), self.refusal())
        self.assertFalse(self.out.exists())

    def test_out_exists(self):
        self.registry.write_text('CHECK\tx\tfuture\n')
        self.out.write_bytes(b'keep')
        self.assertIn('EEXIST', self.refusal())
        self.assertEqual(self.out.read_bytes(), b'keep')

    def test_short_writes(self):
        with fault_kit.one_byte_writes():
            self.run_rows([['CHECK', 'x', 'future']], 1)

    def test_registry_symlink_swap(self):
        self.registry.write_text('CHECK\tx\tfuture\n')
        target = self.file('target', 'CHECK\tx\tfuture\n')
        with fault_kit.swap_for_symlink('open', 1, self.registry, target,
                match=lambda path, *a, **k: path == self.registry.name):
            self.assertIn('ELOOP', self.refusal())

    def test_registry_fifo(self):
        self.registry.write_text('CHECK\tx\tfuture\n')
        with fault_kit.fifo_in_place(self.registry):
            self.assertIn(str(self.registry), self.refusal())

    def test_registry_parent_rebind(self):
        folder = self.base/'regdir'
        folder.mkdir()
        self.registry = folder/'registry'
        self.registry.write_text('CHECK\tx\tfuture\n')
        with fault_kit.rename_and_rebind('fcntl.F_GETPATH', 2, folder):
            self.assertIn(str(folder), self.refusal())

    def test_os_errors(self):
        self.registry.write_text('CHECK\tx\tfuture\n')
        for name in ('open', 'read', 'fstat', 'close', 'fcntl.F_GETPATH'):
            with self.subTest(name=name), fault_kit.inject_oserror(name, 1, errno.EIO):
                self.assertIn('EIO', self.refusal())

    def test_unexpected_errors_propagate(self):
        self.registry.write_text('CHECK\tx\tfuture\n')
        with fault_kit.raise_unexpected('read', 1, RuntimeError):
            with self.assertRaisesRegex(RuntimeError, 'unexpected'):
                self.refusal()

    def test_pure_part_ast_allowlist(self):
        source = inspect.getsource(checks).partition('# I/O shell:')[0]
        tree = ast.parse(source)
        names = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
        names.update(alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names)
        self.assertEqual(names, {'__future__', 'csv', 'io', 'json', 'shlex', 'tomllib', 'dataclasses',
                                'pathlib', 'typing', 'ops.migrate', 'ops.migrate.root_readers_core'})
        calls = {node.func.attr for node in ast.walk(tree)
                 if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}
        self.assertFalse(calls & {'open', 'stat', 'read_bytes', 'getenv', 'run', 'time', 'monotonic', 'resolve'})

    def test_receipt_tail_and_single_physical_row(self):
        self.reply = (4, b'prefix'+b'x'*2100+b'\nlast\ttail')
        rows = self.run_rows([['CHECK', '.venv/bin/hf', 'console-version']], 1)
        detail = json.loads(rows[0][3])
        self.assertEqual(detail, 'exit 4: '+self.reply[1].decode()[-2000:])
        self.assertEqual(len(self.out.read_text().splitlines()), 2)

    def test_no_checks_refuses(self):
        self.registry.write_text('# empty\n')
        self.assertIn('no CHECK', self.refusal())

    def test_non_utf8_registry_refuses(self):
        self.registry.write_bytes(b'\xff')
        self.assertIn('EINVAL', self.refusal())

    def test_relative_root_refuses(self):
        self.assertIn('EINVAL', self.refusal(['--root', 'relative', '--old-root', self.old,
            '--registry', str(self.registry), '--out', str(self.out)]))

    def test_path_escape_refuses(self):
        self.registry.write_text('CHECK\t../outside\tclaude-project\n')
        self.assertIn('EINVAL', self.refusal())

    def test_home_tilde(self):
        self.file(self.home/'.claude.json', json.dumps({'projects': {str(self.root): {}}}))
        self.run_rows([['CHECK', '~/.claude.json', 'claude-project']])

    def test_non_object_config(self):
        self.single('claude-project', '[]', 'FAIL')

    def test_settings_schema(self):
        self.single('settings-rules', '{"permissions":{"allow":[1]}}', 'FAIL')

    def test_all_group_members_checked(self):
        a = self.file('a.sh', '#!/bin/bash\ntrue\n', 0o755)
        b = self.file('b.sh', '#!/bin/bash\nif then\n', 0o755)
        self.run_rows([['REPLACE', a, 'x', 'y', '1'], ['REPLACE', b, 'x', 'y', '1'],
                       ['CHECK', 'shell-scripts', 'shell-syntax']], 1)
        self.assertEqual(len(self.calls), 2)

    def test_output_write_error_keeps_partial(self):
        self.registry.write_text('CHECK\tx\tfuture\n')
        with fault_kit.inject_oserror('write', 1, errno.ENOSPC):
            self.assertIn('ENOSPC', self.refusal())
        self.assertTrue(self.out.exists())

    def test_output_parent_rebound_into_root(self):
        folder = self.base/'outdir'
        folder.mkdir()
        self.out = folder/'receipt'
        self.registry.write_text('CHECK\tx\tfuture\n')
        def moved(fd, data):
            folder.rename(self.root/'moved')
            return real(fd, data)
        from unittest.mock import patch
        real = os.write
        with patch.object(os, 'write', moved):
            self.assertIn('inside root', self.refusal())
        self.assertTrue((self.root/'moved/receipt').exists())

    def test_real_command_boundary(self):
        command = checks.Command(('bash', '-c', 'printf "%s" "$ROOT:$HOME:$PYTHONDONTWRITEBYTECODE"'),
                                 (('ROOT', str(self.root)), ('HOME', str(self.home)),
                                  ('PYTHONDONTWRITEBYTECODE', '1')))
        output = checks.run_command(command)
        self.assertEqual(output, checks.Output(0, (str(self.root)+':'+str(self.home)+':1').encode()))
        output = checks.run_command(checks.Command(('bash', '-n'), (), b'if then\n'))
        self.assertNotEqual(output.code, 0)
        self.assertTrue(output.data)

    def test_command_cannot_inherit_another_git_directory(self):
        with patch.dict(os.environ, GIT_DIR=str(self.base/'unrelated')):
            output = checks.run_command(checks.Command(('bash', '-c', 'printf "%s" "${GIT_DIR-unset}"'), ()))
        self.assertEqual(output, checks.Output(0, b'unset'))

    def test_command_preserves_non_git_environment(self):
        with patch.dict(os.environ, T415_SENTINEL='preserved'):
            output = checks.run_command(checks.Command(('bash', '-c', 'printf "%s" "$T415_SENTINEL"'), ()))
        self.assertEqual(output, checks.Output(0, b'preserved'))

    def test_path_operand_boundaries(self):
        for left in ('', ' ', '\t', '\n', '"', "'", '(', ':', '=', ';', '&', '|', '<', '>'):
            for right in ('', '/', ' ', '\t', '\n', '"', "'", ')', ':', '*', ';', '&', '|', '<', '>'):
                with self.subTest(left=left, right=right):
                    self.assertEqual(checks.path_count(left+'/root'+right, '/root'), 1)
        for text in ('/rooted', 'prefix/root', '/parent/root', '/roo', '/ro ot'):
            self.assertEqual(checks.path_count(text, '/root'), 0)
        self.assertEqual(checks.path_count('/root /root /rooted', '/root'), 2)

    def test_canonical_boundaries(self):
        for path in (None, 1, '', 'x', '/x/', '/x//y', '/x/./y', '/x/../y', '/x\0', '/x\n', '/x\r', '/x\t'):
            with self.subTest(path=path), self.assertRaises(checks.fdsafe.Refusal):
                checks.canonical(path)
        self.assertEqual(checks.canonical('/'), '/')
        self.assertEqual(checks.canonical('/x/y'), '/x/y')

    def test_group_status_precedence(self):
        self.assertEqual(checks.combine([checks.Result('UNAVAILABLE', 'a'), checks.Result('FAIL', 'b')]),
                         checks.Result('FAIL', 'a | b'))
        self.assertEqual(checks.combine([checks.Result('PASS', 'a'), checks.Result('UNAVAILABLE', 'b')]).status,
                         'UNAVAILABLE')

    def test_shell_empty_shebang(self):
        self.assertEqual(self.shell('#!\n', 1)[0][2], 'UNAVAILABLE')

    def test_shell_no_shebang(self):
        self.assertEqual(self.shell('true\n', 1)[0][2], 'UNAVAILABLE')

    def test_shell_missing_hashbang_with_interpreter_text(self):
        self.assertIsNone(checks.shell_name('xx/bin/bash\n'))

    def test_export_discards_root_override(self):
        self.single('test-ship', '#!/bin/bash\nexport ROOT=/old\necho "$ROOT"\n', 'UNAVAILABLE')
        self.assertEqual(self.calls, [])

    def test_default_stderr_is_stderr(self):
        err, out = io.StringIO(), io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
            self.assertEqual(checks.main([], home=str(self.home), runner=self.runner), 2)
        self.assertEqual(out.getvalue(), '')
        self.assertIn('arguments', err.getvalue())

    def test_home_default_uses_fixture_environment(self):
        p = self.file(self.home/'.claude.json', json.dumps({'projects': {str(self.root): {}}}))
        self.registry.write_text('CHECK\t~/.claude.json\tclaude-project\n')
        with patch.dict(os.environ, HOME=str(self.home)):
            self.assertEqual(checks.main(['--root', str(self.root), '--old-root', self.old,
                '--registry', str(self.registry), '--out', str(self.out)], runner=self.runner), 0)
        self.assertIn('PASS', self.out.read_text())

    def test_refusal_errno_tag(self):
        self.registry.write_text('CHECK\tx\tfuture\n')
        with fault_kit.inject_oserror('read', 1, errno.EIO):
            self.assertNotIn('EINVAL', self.refusal())
        self.out = self.root/'forbidden'
        self.assertTrue(self.refusal().rstrip().endswith('[EINVAL]'))

    def test_registry_rebind_after_hold(self):
        folder = self.base/'regdir'
        folder.mkdir()
        self.registry = folder/'registry'
        self.registry.write_text('CHECK\tx\tfuture\n')
        with fault_kit.rename_and_rebind('scandir', 1, folder):
            self.assertIn('ESTALE', self.refusal())

    def test_unknown_argument_refuses_at_parser(self):
        self.registry.write_text('CHECK\tx\tfuture\n')
        error = self.refusal(['--root', str(self.root), '--old-root', self.old,
            '--registry', str(self.registry), '--out', str(self.out), '--bogus'])
        self.assertIn('arguments', error)
        self.assertIn('unrecognized arguments', error)

    def test_parser_library_unexpected_failure(self):
        with patch.object(json, 'loads', side_effect=RuntimeError('parser failure')):
            with self.assertRaisesRegex(RuntimeError, 'parser failure'):
                checks.schema_result(checks.Probe('claude-project', 'x'), '{}', str(self.root), self.old)

    def test_decode_unexpected_type_surfaces(self):
        with self.assertRaises(AttributeError):
            checks.advance(checks.Probe('claude-project', 'x'), (checks.File(None, 0),),
                           str(self.root), self.old, str(self.home))

    def test_shebang_library_unexpected_failure(self):
        with patch.object(checks.shlex, 'split', side_effect=RuntimeError('shell parser failure')):
            with self.assertRaisesRegex(RuntimeError, 'shell parser failure'):
                checks.advance(checks.Probe('shell-syntax', 'x.sh'), (checks.File(b'#!/bin/bash\n', 0),),
                               str(self.root), self.old, str(self.home))

    def test_runner_unexpected_failure(self):
        def broken(command):
            raise RuntimeError('runner failed')
        with self.assertRaisesRegex(RuntimeError, 'runner failed'):
            checks.perform(checks.Probe('console-version', 'x'), checks.Effects(broken),
                           str(self.root), self.old, str(self.home))

    def test_bad_home_refuses(self):
        self.registry.write_text('CHECK\tx\tfuture\n')
        err = io.StringIO()
        self.assertEqual(checks.main(['--root', str(self.root), '--old-root', self.old,
            '--registry', str(self.registry), '--out', str(self.out)],
            home='relative', runner=self.runner, stderr=err), 2)
        self.assertIn('relative', err.getvalue())

    def test_bad_utf8_in_valid_json(self):
        data = json.dumps({'projects': {str(self.root): {}}, 'other': 'BAD'}).encode().replace(b'BAD', b'\xff')
        self.single('claude-project', data, 'FAIL')

    def test_bad_utf8_in_registry_comment(self):
        self.registry.write_bytes(b'#\xff\nCHECK\tx\tfuture\n')
        self.assertIn('EINVAL', self.refusal())


    def test_shell_with_argument(self):
        self.assertEqual(self.shell('#!/bin/bash -e\ntrue\n')[0][2], 'PASS')

    def test_root_expansion_in_comment_is_not_override(self):
        self.single('test-ship', '#!/bin/bash\n# ${ROOT}\ntrue\n', 'UNAVAILABLE')
        self.assertEqual(self.calls, [])

    def test_root_override_followed_by_command(self):
        self.single('test-train', '#!/bin/bash\nROOT=${ROOT:-/old}\necho "$ROOT"\n')
        self.assertEqual(len(self.calls), 1)

    def test_stop_row_is_not_a_reader(self):
        p = self.file('teamdash', '#!/bin/bash\n', 0o755)
        self.run_rows([['CHECK', 'executables', 'exec-bit'], ['STOP', 'claude'],
                       ['REPLACE', p, 'old', 'new', '1']])

    def test_lane_status_excludes_non_git_repairs(self):
        p = self.file(self.base/'lane/.git', 'gitdir: unused\n')
        q = self.file('code/x.txt', 'old')
        self.run_rows([['REPLACE', p, 'old', 'new', '1'], ['REPLACE', q, 'old', 'new', '1'],
                       ['CHECK', 'lane-worktrees', 'lane-status']])
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0].argv[3], str(Path(p).parent))

    def test_cli_entrypoint_refuses_bad_arguments(self):
        import sys
        result = subprocess.run([sys.executable, '-B', checks.__file__, '--bogus'],
                                env=dict(os.environ, HOME=str(self.home)),
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(result.stdout, '')
        self.assertIn('arguments', result.stderr)
        self.assertIn('EINVAL', result.stderr)

    def bounded_workflow_runner(self, command):
        result = subprocess.run(command.argv, input=command.stdin,
                                env=dict(os.environ, **dict(command.env)),
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=2)
        return checks.Output(result.returncode, result.stdout)

    def workflow_attack(self, kind, attack):
        # [LAW:behavior-not-structure] The shell must execute the bytes the reader saw.
        script = self.file(kind+'.sh', '#!/bin/bash\nROOT=${ROOT:?}\nprintf "checked-safe\\n"\n')
        target = self.file(self.base/(kind+'-outside.sh'),
                           '#!/bin/bash\nprintf "outside-ran\\n"\n'
                           'printf "changed\\n" > "$ROOT/attack-marker"\n')

        def script_fd(fd):
            try:
                return checks.fdsafe.live_path(fd, script) == script
            except checks.fdsafe.Refusal as exc:
                if exc.errno == errno.EBADF:
                    return False
                raise

        fault = (fault_kit.swap_for_symlink('close', 1, script, target, match=script_fd)
                 if attack == 'swap' else
                 fault_kit.fifo_in_place(script, name='close', n=1, match=script_fd, timeout=5))
        with fault as fired:
            result = checks.perform(checks.Probe(kind, script), checks.Effects(self.bounded_workflow_runner),
                                    str(self.root), self.old, str(self.home))
        self.assertEqual(fired.fired, 1)
        self.assertFalse((self.root/'attack-marker').exists())
        self.assertEqual(result, checks.Result('PASS', 'exit 0: checked-safe\n'))

    def test_workflow_symlink_swap_uses_checked_bytes(self):
        for kind in ('test-ship', 'test-train'):
            with self.subTest(kind=kind):
                self.workflow_attack(kind, 'swap')

    def test_workflow_fifo_swap_uses_checked_bytes(self):
        for kind in ('test-ship', 'test-train'):
            with self.subTest(kind=kind):
                self.workflow_attack(kind, 'fifo')

    def test_workflow_zero_is_script_path(self):
        for kind in ('test-ship', 'test-train'):
            with self.subTest(kind=kind):
                script = self.file(kind+'.sh', '#!/bin/bash\nROOT=${ROOT:?}\nprintf "%s" "$0"\n')
                result = checks.perform(checks.Probe(kind, script), checks.Effects(self.bounded_workflow_runner),
                                        str(self.root), self.old, str(self.home))
                self.assertEqual(result, checks.Result('PASS', 'exit 0: '+script))

    def test_workflow_nul_fails_with_path_without_running(self):
        for kind in ('test-ship', 'test-train'):
            with self.subTest(kind=kind):
                script = self.file(kind+'.sh', '#!/bin/bash\nROOT=${ROOT:?}\n#\0\n')
                result = checks.perform(checks.Probe(kind, script), checks.Effects(self.runner),
                                        str(self.root), self.old, str(self.home))
                self.assertEqual(result.status, 'FAIL')
                self.assertIn(script, result.detail)
                self.assertIn('NUL', result.detail)
                self.assertEqual(self.calls, [])


if __name__ == '__main__':
    unittest.main()
