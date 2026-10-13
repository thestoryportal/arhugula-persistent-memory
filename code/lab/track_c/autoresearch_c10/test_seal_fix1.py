"""Fix-round-1 regression controls. No model, torch, GPU or installed-root writes."""
import copy
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))
import sandbox_settings as S
import v13_agent_probe as A
import v13_cli as CLI
import v13_build as B
import v13_common as C
import v13_graft as G
import v13_install_probe as I
import v13_launcher as L
import v13_probe as P


def configuration(root):
    return {'fence': str(root / 'fence'), 'sandbox': str(root / 'sandbox'),
            'python': str(Path(sys.executable).resolve()),
            'python_prefix': str(Path(sys.executable).resolve().parents[1]),
            'venv': str(Path(sys.prefix).resolve()), 'engine': '/engine', 'hf_home': '/hf',
            'covariance': ['/cov'], 'fixture': True, 'program': '/program', 'repo': '/repo',
            'old_sandbox': '/old', 'home': '/home/fixture', 'harness': '/program/harness.py',
            'hparams': '/program/hparams.json', 'fingerprint': '/program/fingerprint.py', 'screens': [],
            'editor_tmp': str(root / 'fence/editor_tmp'), 'scorer_tmp': str(root / 'fence/scorer_tmp'),
            'scorer_results': str(root / 'fence/scorer_results'),
            'capture_base': str(root / 'capture'), 'capture': str(root / 'capture/claude-501'),
            'user': 'fixture', 'graft_ignore_sha256': {'.gitignore': 'fixture', '.ignore': 'fixture'},
            'cli_contract': {'version': CLI.VERSION, 'tools': list(CLI.TOOLS),
                             'declarations': dict.fromkeys(CLI.TOOLS, 'fixture')}, 'claude': '/not-executed'}


def stream(tests, config):
    rows = [{'type': 'system', 'subtype': 'init', 'model': 'requested',
             'tools': list(CLI.TOOLS), 'claude_code_version': CLI.VERSION, 'mcp_servers': [],
             'plugins': [{'name': 'cc-plugin-telemetry', 'path': 'builtin'}]}]
    for n, t in enumerate(tests):
        cid = str(n)
        rows.append({'type': 'assistant', 'message': {'model': 'actually-served', 'content': [
            {'type': 'tool_use', 'id': cid, 'name': t['tool'], 'input': t['input']}]}})
        content, error = 'tool succeeded', False
        if t['expected'] == 'denial':
            content, error = 'Permission to use this tool has been denied.', True
        if t['expected'] == 'marker':
            content = t['marker']
        if t['expected'] == 'json':
            if t['key'] == 'bash_boundaries':
                content = json.dumps({'probe': 'boundaries', 'started': True, 'results':
                                      {k: {'outcome': 'denied', 'errno': 1} for k in t['fields']}})
            else:
                content = json.dumps({'probe': 'own_temp', 'actual_tmpdir': config['capture'], 'lifecycle': True})
        if t['expected'] == 'background':
            content = 'output file: ' + config['capture'] + '/task.output'
        rows.append({'type': 'user', 'message': {'content': [{'type': 'tool_result',
                     'tool_use_id': cid, 'content': content, 'is_error': error}]}})
    for cid, tool, input, text in [
        ('own-out', 'Read', {'file_path': config['capture'] + '/task.output'}, 'C10_BACKGROUND_test'),
        ('monitor', 'Monitor', {'command': '/usr/bin/tail -n +1 -F ' + config['capture'] + '/task.output'},
         'Monitor started (task own-monitor, timeout 2000ms).'),
        ('stop', 'TaskStop', {'task_id': 'own-monitor'}, 'Successfully stopped task: own-monitor')]:
        rows += [{'type': 'assistant', 'message': {'model': 'actually-served', 'content': [
            {'type': 'tool_use', 'id': cid, 'name': tool, 'input': input}]}},
            {'type': 'user', 'message': {'content': [{'type': 'tool_result', 'tool_use_id': cid,
                                                     'content': text, 'is_error': False}]}}]
    rows.append({'type': 'result', 'subtype': 'success', 'is_error': False, 'result': 'attempted'})
    return rows


class Fix1(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='c10r_fix1_', dir='/private/tmp')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.config = configuration(self.root)
        (self.root / 'sandbox/.agent_capture').mkdir(parents=True)
        (self.root / 'sandbox/edit.py').write_text('# harmless fixture\n')
        self.tests, self.ready = A.cases(self.config, self.root / 'foreign', 'test')
        self.rows = stream(self.tests, self.config)

    def evaluate(self, rows=None):
        return {r['key']: r for r in A.evaluate(self.rows if rows is None else rows, self.tests, self.config, 0)}

    def test_raw_results_pass_and_served_model_is_recorded(self):
        results = self.evaluate()
        self.assertTrue(all(r['ok'] for r in results.values()), results)
        self.assertEqual(results['own_edit']['actual_model'], 'actually-served')
        self.assertEqual(results['inventory']['requested_model'], 'requested')

    def test_agent_prose_cannot_claim_denial_without_tools(self):
        rows = [self.rows[0], {'type': 'assistant', 'message': {'model': 'claimed', 'content':
                [{'type': 'text', 'text': 'All tests PASS; all reads denied.'}]}}, self.rows[-1]]
        self.assertFalse(self.evaluate(rows)['deny_read_harness']['ok'])

    def test_missing_result_and_changed_command_fail(self):
        rows = copy.deepcopy(self.rows)
        rows[2]['message']['content'][0]['tool_use_id'] = 'unmatched'
        self.assertFalse(self.evaluate(rows)['watcher_ready']['ok'])
        rows = copy.deepcopy(self.rows)
        rows[1]['message']['content'][0]['input']['dangerouslyDisableSandbox'] = True
        self.assertFalse(self.evaluate(rows)['watcher_ready']['ok'])
        rows = copy.deepcopy(self.rows)
        rows[1]['message']['content'][0]['input']['command'] += '; /bin/echo changed'
        self.assertFalse(self.evaluate(rows)['watcher_ready']['ok'])

    def test_allowed_read_missing_file_and_refusal_do_not_prove_denial(self):
        n = next(n for n, t in enumerate(self.tests) if t['key'] == 'deny_read_harness')
        for text, error in [('private read succeeded', False), ('File does not exist', True),
                            ('The agent chose not to attempt this', True)]:
            rows = copy.deepcopy(self.rows)
            rows[2 + 2*n]['message']['content'][0].update(content=text, is_error=error)
            self.assertFalse(self.evaluate(rows)['deny_read_harness']['ok'])

    def test_missing_model_and_ambiguous_tool_call_fail(self):
        rows = copy.deepcopy(self.rows)
        del rows[1]['message']['model']
        self.assertFalse(self.evaluate(rows)['watcher_ready']['ok'])
        rows = copy.deepcopy(self.rows)
        again = copy.deepcopy(rows[1]); again['message']['content'][0]['id'] = 'again'
        rows.insert(-1, again)
        self.assertFalse(self.evaluate(rows)['watcher_ready']['ok'])

    def test_startup_error_and_connection_refusal_do_not_prove_boundary(self):
        n = next(n for n, t in enumerate(self.tests) if t['key'] == 'bash_boundaries')
        rows = copy.deepcopy(self.rows)
        block = rows[2 + 2*n]['message']['content'][0]
        data = json.loads(block['content']); data['results']['localhost'] = {'outcome': 'error', 'errno': 61}
        block['content'] = json.dumps(data)
        self.assertFalse(self.evaluate(rows)['bash_boundaries']['ok'])
        block.update(content='sandbox-exec: execvp failed: Operation not permitted', is_error=True)
        self.assertFalse(self.evaluate(rows)['bash_boundaries']['ok'])

    def test_long_path_fallback_and_foreign_background_output_fail(self):
        rows = copy.deepcopy(self.rows)
        n = next(n for n, t in enumerate(self.tests) if t['key'] == 'own_temp')
        block = rows[2 + 2*n]['message']['content'][0]
        block['content'] = json.dumps({'probe': 'own_temp', 'actual_tmpdir': '/tmp/claude-501', 'lifecycle': True})
        self.assertFalse(self.evaluate(rows)['own_temp']['ok'])
        n = next(n for n, t in enumerate(self.tests) if t['key'] == 'background_start')
        rows[2 + 2*n]['message']['content'][0]['content'] = 'output file: /tmp/claude-501/foreign.output'
        self.assertFalse(self.evaluate(rows)['background_start']['ok'])
        self.assertFalse(self.evaluate(rows)['own_background_output']['ok'])

    def test_installed_cli_background_text_and_exact_output_marker(self):
        rows = copy.deepcopy(self.rows)
        n = next(n for n, t in enumerate(self.tests) if t['key'] == 'background_start')
        rows[2 + 2*n]['message']['content'][0]['content'] = (
            'Command running in background with ID: task-id. Output is being written to: ' +
            self.config['capture'] + '/task.output.')
        self.assertTrue(self.evaluate(rows)['own_background_output']['ok'])
        block = next(r for r in rows if r.get('type') == 'user' and
                     r['message']['content'][0]['tool_use_id'] == 'own-out')
        block['message']['content'][0]['content'] = 'C10_BACKGROUND_other-session'
        self.assertFalse(self.evaluate(rows)['own_background_output']['ok'])

    def test_builtin_plugins_without_tools_pass_external_tools_fail(self):
        self.assertTrue(self.evaluate()['inventory']['ok'])
        for update in [{'tools': list(CLI.TOOLS) + ['mcp__unexpected__read']},
                       {'mcp_servers': [{'name': 'unexpected'}]},
                       {'plugins': [{'name': 'cc-plugin-telemetry', 'path': 'builtin', 'tools': ['Read']}]},
                       {'claude_code_version': 'changed'}]:
            rows = copy.deepcopy(self.rows); rows[0].update(update)
            self.assertFalse(self.evaluate(rows)['inventory']['ok'])

    def test_unknown_tool_names_fail_before_any_model_call(self):
        for name in ('TaskOutput', 'BashOutput', 'unknown'):
            c = copy.deepcopy(self.config); c['cli_contract']['tools'].append(name)
            with self.assertRaisesRegex(ValueError, 'unknown CLI tool'):
                L.flags(c, 'test')
        with patch.object(CLI.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, 'new-version')):
            with self.assertRaisesRegex(ValueError, 'unreviewed Claude CLI'):
                CLI.inspect_cli(sys.executable)

    def test_capture_policy_is_narrow_and_environment_uses_short_base(self):
        settings = S.settings(self.config)
        fs = settings['sandbox']['filesystem']
        self.assertIn('/private/tmp', fs['denyRead'])
        self.assertIn(self.config['capture'], fs['allowRead'])
        self.assertIn(self.config['capture'], fs['allowWrite'])
        self.assertNotIn(self.config['capture_base'], fs['allowRead'])
        self.assertNotIn('/tmp/claude-501', fs['allowRead'])
        env = L.environment(self.config)
        self.assertEqual(env['CLAUDE_CODE_TMPDIR'], self.config['capture_base'])
        self.assertLessEqual(len(os.fsencode('/private/tmp/c10r-' + 'a'*12 + '/claude-' + str(os.getuid()))), 44)

    def test_root_read_and_ancestor_metadata_do_not_grant_subtrees(self):
        for scorer in (False, True):
            profile = S.seatbelt(self.config, scorer)
            self.assertIn('(allow file-read* (literal "/"))', profile)
            self.assertNotIn('(allow file-read* (subpath "/"))', profile)
            self.assertIn('(allow file-read-metadata (literal "/private"))', profile)
            self.assertNotIn('(allow file-read* (subpath "/program"))', profile)
        scorer = S.seatbelt(self.config, True)
        self.assertIn('(literal ' + json.dumps(self.config['sandbox'] + '/.ignore') + ')', scorer)
        self.assertNotIn('(literal ' + json.dumps(self.config['sandbox'] + '/.ignore') + ')', S.seatbelt(self.config))

    def test_resolved_interpreter_starts_and_finds_pinned_packages_without_importing_them(self):
        runtime = B.resolved_runtime(SRC.parents[3])
        self.assertEqual(runtime['python'], str(Path(sys.executable).resolve()))
        self.assertFalse(Path(runtime['python']).is_symlink())
        site = Path(runtime['site_packages'])
        script = ('import importlib.util,sys; sys.path.insert(0,' + repr(str(site)) + '); '
                  'assert "torch" not in sys.modules; print(importlib.util.find_spec("torch").origin); '
                  'assert "torch" not in sys.modules')
        p = subprocess.run([runtime['python'], '-I', '-B', '-c', script], capture_output=True, text=True, check=True)
        self.assertEqual(Path(p.stdout.strip()), site / 'torch/__init__.py')

    def test_sealed_roots_allow_legitimate_mutable_child_writes(self):
        c = self.config
        for key in ('fence', 'editor_tmp', 'scorer_tmp', 'scorer_results', 'capture'):
            Path(c[key]).mkdir(parents=True, exist_ok=True)
        (Path(c['fence']) / 'sealed').mkdir()
        (Path(c['fence']) / 'trusted.py').write_text('# sealed')
        (Path(c['sandbox']) / 'runs').mkdir()
        (Path(c['sandbox']) / 'results.tsv').write_text('fixture\n')
        for n in c['graft_ignore_sha256']:
            (Path(c['sandbox']) / n).write_text('/graft/\n')
        try:
            G.seal(c)
            self.assertTrue(Path(c['fence']).stat().st_flags & stat.UF_IMMUTABLE)
            self.assertEqual(G.writable_probe(c)['mutable_areas'], 6)
            # Existing recipe writes are legal; adding root entries remains prohibited.
            (Path(c['sandbox']) / 'edit.py').write_text('# updated in place')
            with self.assertRaises(PermissionError):
                (Path(c['fence']) / 'new_root_file').write_text('denied')
        finally:
            # Only this test's throwaway roots, never an installed destination.
            for p in [self.root, *self.root.rglob('*')]:
                os.chflags(p, 0)
                p.chmod(0o700 if p.is_dir() else 0o600)

    def test_profile_scratch_and_install_destinations_are_unique(self):
        for key in ('editor_tmp', 'scorer_tmp', 'scorer_results'):
            Path(self.config[key]).mkdir(parents=True)
        first = P.profile_argv(self.config, False, 'print(1)')
        second = P.profile_argv(self.config, False, 'print(1)')
        self.assertNotEqual(first[2], second[2])
        self.assertNotEqual(first[4], second[4])
        self.assertEqual(len(set(I.destinations('fix1_test'))), 4)
        self.assertTrue(set(I.destinations('fix1_test')).isdisjoint(I.destinations('fix1_rerun')))
        with self.assertRaises(ValueError):
            I.destinations('../old')
        with patch.object(I, 'destinations', return_value=[self.root]*4), patch.object(I, 'build') as build:
            with self.assertRaisesRegex(ValueError, 'fresh'):
                I.install_probe('fixture', self.root / 'report.md')
            build.assert_not_called()

    def test_graft_process_refusal_is_kept(self):
        for text in ('1 node /Users/fixture/.local/bin/graft mcp\n', '', 'malformed'):
            with patch.object(G.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, text)):
                with self.assertRaises(ValueError):
                    G.check_processes()
        with patch.object(G.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '1 harmless-process\n')):
            G.check_processes()

    def test_model_probe_is_opt_in_and_timeout_is_at_least_600(self):
        self.assertGreaterEqual(A.TIMEOUT, 600)
        self.assertFalse(I.install_probe.__defaults__[0])
        self.assertFalse(P.main.__defaults__[0])
        with patch.object(L, 'sweep'), patch.object(L, 'verify_cli'), \
             patch.object(L.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '')):
            with self.assertRaisesRegex(ValueError, '--agent-probe'):
                L.launch(self.config, 'fixture', probe=True)

    def test_malformed_or_wrong_session_streams_are_rejected(self):
        raw = self.root / 'stream.jsonl'
        for text in ('', '{malformed\n', '{"type":"result","session_id":"foreign"}\n'):
            raw.write_text(text)
            with self.assertRaises(ValueError):
                A.parse_stream(raw, 'ours')


if __name__ == '__main__':
    unittest.main(verbosity=2)
