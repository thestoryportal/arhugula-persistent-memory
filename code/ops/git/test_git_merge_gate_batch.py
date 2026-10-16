"""Batch mode of git_merge_gate: fixture git repositories in temp dirs and a stub `gh` on PATH.

No test touches the real remote: origin is a bare repository inside the test's temp dir.
"""
from contextlib import redirect_stderr, redirect_stdout
import fcntl
import importlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

LANE = Path(__file__).resolve().parents[3]

STUB = r'''#!PYTHON -B
"""Stub gh: serves PR, ref, workflow-run and check-run inventories from GH_STUB_STATE and the fixture origin."""
import json, os, subprocess, sys, urllib.parse
path = os.environ['GH_STUB_STATE']
with open(path) as handle:
    state = json.load(handle)
args = sys.argv[1:]
with open(path + '.log', 'a') as handle:
    handle.write(json.dumps(args) + '\n')


def git(*command):
    result = subprocess.run(['git', '--git-dir', state['remote'], *command], capture_output=True, text=True)
    return result


def master():
    return git('rev-parse', 'refs/heads/master').stdout.strip()


def move(ref, sha):
    if git('update-ref', 'refs/heads/' + ref, sha).returncode:
        sys.exit('stub: update-ref failed')


def contains(sha, tip):
    return git('merge-base', '--is-ancestor', sha, tip).returncode == 0


def save():
    with open(path, 'w') as handle:
        json.dump(state, handle)


def show(value):
    print(json.dumps(value))


def pr_value(number):
    pr = state['prs'][number]
    merged = (pr['state'] == 'OPEN' and not pr.get('never_merged') and isinstance(pr['head'], str)
              and contains(pr['head'], master()))
    return {'number': pr.get('number', int(number)), 'state': 'MERGED' if merged else pr['state'], 'isDraft': pr.get('draft', False),
            'isCrossRepository': pr.get('cross', False), 'headRefName': pr['ref'], 'headRefOid': pr['head'],
            'baseRefName': pr.get('base', 'master'), 'baseRefOid': state['base'], 'mergeable': 'MERGEABLE',
            'mergeCommit': {'oid': master()} if merged else None}


def phase(key):
    spec = state['ci'][key]
    if spec.startswith('PENDING:'):
        return 'PASS' if state['counts'].get(key, 0) > int(spec.split(':')[1]) else 'PENDING'
    return spec


def run(identity, sha, branch, kind, attempt=1, event='push'):
    status = 'in_progress' if kind == 'PENDING' else 'completed'
    conclusion = None if kind == 'PENDING' else ('success' if kind == 'PASS' else 'failure')
    return {'id': identity, 'head_sha': sha, 'head_branch': branch, 'event': event, 'name': 'CI',
            'status': status, 'conclusion': conclusion, 'run_attempt': attempt,
            'html_url': 'https://github.com/o/r/actions/runs/%d' % identity, 'updated_at': '2026-10-16T08:00:00Z'}


def runs(sha):
    rows = []
    for index, key in enumerate(sorted(state['ci'])):
        run_sha, branch = key.split('|')
        if run_sha == sha:
            rows.append(run(1000 + 10 * index, sha, branch, phase(key)))
    for extra in state.get('extra_runs', []):
        if extra['sha'] == sha:
            rows.append(run(extra['id'], sha, extra['branch'], extra['kind'], extra.get('attempt', 1),
                            extra.get('event', 'push')))
    if state.get('master_ci') and master() == sha:
        rows.append(run(5000, sha, 'master', state['master_ci']))
    return rows


def checks(sha):
    return [{'id': row['id'] + 1, 'name': 'cpu', 'head_sha': sha, 'status': row['status'],
             'conclusion': row['conclusion'], 'updated_at': row['updated_at'],
             'html_url': row['html_url'] + '/job/%d' % (row['id'] + 1)} for row in runs(sha)]


def effects(trigger):
    for effect in state['effects']:
        if effect['on'] == trigger and not effect.get('done'):
            effect['seen'] = effect.get('seen', 0) + 1
            if effect['seen'] == effect.get('nth', 1):
                effect['done'] = True
                if effect['do'] == 'move':
                    move(effect['ref'], effect['to'])
                elif effect['do'] == 'pr-set':
                    state['prs'][effect['pr']][effect['field']] = effect['to']
                elif effect['do'] == 'set':
                    state[effect['key']] = effect['to']
                elif effect['do'] == 'add-run':
                    state.setdefault('extra_runs', []).append(effect['run'])


if args[:2] == ['pr', 'view']:
    value = pr_value(args[2])
    show({field: value[field] for field in args[args.index('--json') + 1].split(',')})
elif args[:1] == ['api']:
    url = urllib.parse.urlsplit(args[1])
    query = urllib.parse.parse_qs(url.query)
    page = int(query.get('page', ['1'])[0])
    if url.path.endswith('/pulls'):
        show([] if page > 1 else [{'head': {'ref': pr['ref']}} for number, pr in sorted(state['prs'].items())
                                   if pr_value(number)['state'] == 'OPEN'])
        effects('pulls')
    elif url.path.endswith('/git/ref/heads/master'):
        show({'object': {'sha': state.get('api_master') or master()}})
        effects('master-ref')
        if state.get('master_ci_served'):
            effects('master-ref-after-master-ci')
    elif url.path.endswith('/actions/runs'):
        sha, branch = query['head_sha'][0], query.get('branch', [None])[0]
        key = sha + '|' + str(branch)
        state['counts'][key] = state['counts'].get(key, 0) + 1
        if 'runs_payload' in state:
            show(state['runs_payload'])
        else:
            rows = [row for row in runs(sha) if branch in (None, row['head_branch']) and
                    query.get('event', [row['event']])[0] == row['event']]
            show({'workflow_runs': rows})
            if branch == 'master' and rows and all(row['conclusion'] == 'success' for row in rows):
                state['master_ci_served'] = True
        effects('master-runs' if branch == 'master' else 'candidate-runs')
    elif '/check-runs' in url.path:
        sha = url.path.split('/')[-2]
        rows = checks(sha)
        if query['filter'] == ['latest']:
            rows = rows[-1:] if rows else []
        show({'check_runs': [] if page > 1 else rows})
    elif url.path.endswith('/statuses'):
        show([])
    else:
        sys.exit('stub gh: unexpected api endpoint ' + args[1])
else:
    sys.exit('stub gh: unexpected command ' + ' '.join(args))
save()
'''


class Clock:
    def __init__(self):
        self.now = 0

    def __call__(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


def git(root, *args, check=True):
    result = subprocess.run(['git', *args], cwd=root, capture_output=True, text=True, timeout=30)
    if check and result.returncode:
        raise AssertionError(' '.join(args) + ': ' + result.stderr)
    return result.stdout.strip()


class BatchTests(unittest.TestCase):
    candidate = 'land/20261016T150000Z'

    def setUp(self):
        sys.path.insert(0, str(LANE / 'code'))
        self.addCleanup(sys.path.remove, str(LANE / 'code'))
        self.H = importlib.import_module('ops.git.git_hygiene')
        self.M = importlib.import_module('ops.git.git_merge_gate')
        temp = tempfile.TemporaryDirectory(prefix='merge-gate-batch-')
        self.addCleanup(temp.cleanup)
        self.home = Path(temp.name).resolve()
        self.remote, self.root = self.home / 'remote.git', self.home / 'clone'
        git(self.home, 'init', '--bare', '--initial-branch=master', str(self.remote))
        git(self.home, 'clone', str(self.remote), str(self.root))
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        (self.root / 'base.txt').write_text('base\n')
        for relative in ('code/memit/engine_fingerprint.py', 'code/memit/vendor/memit/memit_main.py'):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((LANE / relative).read_bytes())
        self.git('add', '.')
        self.git('commit', '-m', 'base')
        self.git('push', 'origin', 'master')
        self.base = self.git('rev-parse', 'HEAD')
        self.heads = {21: self.pr_branch('tk/T901', 'a.txt', 'a\n'), 22: self.pr_branch('tk/T902', 'b.txt', 'b\n')}
        self.refs = {21: 'tk/T901', 22: 'tk/T902'}
        stub_dir = self.home / 'bin'
        stub_dir.mkdir()
        stub = stub_dir / 'gh'
        stub.write_text(STUB.replace('PYTHON', sys.executable))
        stub.chmod(0o755)
        self.state_path = self.home / 'gh-state.json'
        self.state = {'remote': str(self.remote), 'base': self.base, 'ci': {}, 'counts': {}, 'effects': [],
                      'master_ci': 'PASS',
                      'prs': {str(n): {'ref': self.refs[n], 'head': self.heads[n], 'state': 'OPEN'} for n in self.heads}}
        environment = mock.patch.dict(os.environ, {'PATH': str(stub_dir) + os.pathsep + os.environ['PATH'],
                                                   'GH_STUB_STATE': str(self.state_path)})
        environment.start()
        self.addCleanup(environment.stop)
        inventory = mock.patch.object(self.H, 'cwd_inventory', return_value={})
        inventory.start()
        self.addCleanup(inventory.stop)
        self.clock = Clock()

    def git(self, *args, check=True):
        return git(self.root, *args, check=check)

    def pr_branch(self, name, filename, text, start='master'):
        self.git('checkout', '-q', '-b', name, start)
        (self.root / filename).parent.mkdir(parents=True, exist_ok=True)
        (self.root / filename).write_text(text)
        self.git('add', '.')
        self.git('commit', '-q', '-m', name)
        self.git('checkout', '-q', 'master')
        self.git('push', 'origin', name)
        return self.git('rev-parse', name)

    def replace_pr(self, number, name, filename, text):
        old = self.refs[number]
        self.git('push', 'origin', '--delete', old)
        self.git('branch', '-q', '-D', old)
        self.heads[number], self.refs[number] = self.pr_branch(name, filename, text), name
        self.state['prs'][str(number)].update(head=self.heads[number], ref=name)

    def build(self, order=(21, 22), extra_commit=False, name=None):
        """The train's construction: origin/master, then each PR head merged with --no-ff in order."""
        self.git('checkout', '-q', '--detach', 'origin/master')
        for number in order:
            self.git('merge', '-q', '--no-ff', '-m', 'land #%d' % number, self.heads[number])
        if extra_commit:
            (self.root / 'extra.txt').write_text('extra\n')
            self.git('add', 'extra.txt')
            self.git('commit', '-q', '-m', 'extra')
        sha = self.git('rev-parse', 'HEAD')
        self.git('push', '-f', 'origin', 'HEAD:refs/heads/' + (name or self.candidate))  # fixture origin only
        self.git('checkout', '-q', 'master')
        return sha

    def commit_tree(self, tree, *parents):
        args = ['commit-tree', tree, '-m', 'hand-made candidate commit']
        for parent in parents:
            args += ['-p', parent]
        return self.git(*args)

    def push_candidate(self, sha):
        self.git('push', 'origin', sha + ':refs/heads/' + self.candidate)

    def ci(self, sha, kind='PASS', branch=None):
        self.state['ci'][sha + '|' + (branch or self.candidate)] = kind

    def effect(self, **effect):
        self.state['effects'].append(effect)

    def gate(self, numbers=(21, 22), dry_run=True, candidate=None, wait_s=30):
        self.state_path.write_text(json.dumps(self.state))
        repo = self.H.Repo(self.root, self.H.Deadline(600, clock=self.clock, sleep=self.clock.sleep))
        report = self.M.batch_gate(repo, self.H.Gh(repo, 'o/r'), candidate or self.candidate, list(numbers),
                                   dry_run=dry_run, wait_s=wait_s)
        report['command_evidence'] = repo.commands
        return report

    def gh_calls(self):
        log = Path(str(self.state_path) + '.log')
        return [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []

    def remote_refs(self):
        return git(self.remote, 'for-each-ref', '--format=%(refname) %(objectname)')

    def remote_tip(self, branch):
        return git(self.remote, 'rev-parse', '--verify', '--quiet', 'refs/heads/' + branch, check=False)

    def objects(self, git_dir):
        return sorted(str(p.relative_to(git_dir)) for p in (git_dir / 'objects').rglob('*') if p.is_file())

    def pushes(self, report):
        return [row['command'] for row in report['command_evidence'] if 'push' in row['command']]

    def assert_refused(self, report, check, text, pushes=0):
        self.assertFalse(report['ok'], report['errors'])
        self.assertEqual(report['status'], 'REFUSED')
        self.assertFalse(report['merged'])
        self.assertEqual(report['checks'][check]['status'], 'FAIL', report['checks'])
        self.assertIn(text, report['checks'][check]['reason'])
        self.assertEqual(len(self.pushes(report)), pushes)

    def assert_landed_with_failure(self, report, check, text, sha):
        self.assertFalse(report['ok'])
        self.assertTrue(report['merged'])
        self.assertEqual(report['status'], 'MERGED_WITH_FAILURE')
        self.assertEqual(report['merge_sha'], sha)
        self.assertEqual(report['checks'][check]['status'], 'FAIL', report['checks'])
        self.assertIn(text, report['checks'][check]['reason'])
        self.assertEqual(self.remote_tip(self.candidate), sha, 'candidate branch must be kept')

    # ---- PASS and no mutation ----

    def test_dry_run_passes_and_changes_nothing(self):
        sha = self.build()
        self.ci(sha)
        refs, local = self.remote_refs(), self.git('for-each-ref')
        objects = self.objects(self.root / '.git'), self.objects(self.remote)
        report = self.gate()
        self.assertTrue(report['ok'], report['errors'])
        self.assertEqual(report['status'], 'DRY_RUN_PASS')
        self.assertEqual((report['candidate_sha'], report['master_sha']), (sha, self.base))
        self.assertEqual(report['heads'], [self.heads[21], self.heads[22]])
        for name in ('push', 'pr_merged', 'master_ci', 'candidate_delete'):
            self.assertEqual(report['checks'][name]['status'], 'WOULD-RUN')
        self.assertEqual((refs, local), (self.remote_refs(), self.git('for-each-ref')))
        self.assertEqual(objects, (self.objects(self.root / '.git'), self.objects(self.remote)))
        self.assertEqual(self.pushes(report), [])

    def test_every_batch_git_call_disables_fsmonitor_lazy_fetch_and_optional_locks(self):
        sha = self.build()
        self.ci(sha)
        with mock.patch.object(self.H.Repo, 'run', autospec=True, side_effect=self.H.Repo.run) as run:
            report = self.gate()
        self.assertTrue(report['ok'], report['errors'])
        batch = [c for c in run.call_args_list if c.args[1][:3] == ['git', '-c', 'core.fsmonitor=false']]
        self.assertGreaterEqual(len(batch), 6)
        for call in batch:
            self.assertEqual(call.args[1][3], '--no-optional-locks')
            self.assertEqual(call.kwargs['env']['GIT_NO_LAZY_FETCH'], '1')
            self.assertEqual(call.kwargs['env']['GIT_NO_REPLACE_OBJECTS'], '1')
        local = [c for c in batch if 'merge-tree' in c.args[1]]
        network = [c for c in batch if 'ls-remote' in c.args[1]]
        self.assertTrue(local and network)
        for call in local:
            self.assertEqual((call.kwargs['env']['GIT_CONFIG_GLOBAL'], call.kwargs['env']['GIT_CONFIG_NOSYSTEM']), (os.devnull, '1'))
        for call in network:  # the credential helper lives in user config
            self.assertNotIn('GIT_CONFIG_GLOBAL', call.kwargs['env'])
            self.assertNotIn('GIT_CONFIG_NOSYSTEM', call.kwargs['env'])

    def test_ambiguous_ls_remote_output_is_refused(self):
        sha = self.build()
        self.ci(sha)
        self.git('push', 'origin', sha + ':refs/fixture/refs/heads/master')  # ls-remote patterns match ref tails
        self.assert_refused(self.gate(), 'stable', 'ls-remote output malformed or ambiguous')

    # ---- request and PR checks ----

    def test_candidate_name_and_pr_list_are_validated_before_any_call(self):
        self.build()
        for candidate, numbers in (('feature/x', (21,)), ('land/../x', (21,)), ('land/', (21,)),
                                   ('land/a/b', (21,)), ('land/x', ()), ('land/x', (21, 21)), ('land/x', (0,))):
            with self.subTest(candidate=candidate, numbers=numbers):
                report = self.gate(numbers, candidate=candidate)
                self.assert_refused(report, 'request', 'candidate must be')
                self.assertEqual(report['checks']['prs']['status'], 'NOT-RUN')
        self.assertEqual(self.gh_calls(), [])

    def test_pr_must_be_open_same_repository_and_target_master(self):
        sha = self.build()
        self.ci(sha)
        for field, value in (('state', 'CLOSED'), ('cross', True), ('base', 'release')):
            with self.subTest(field=field):
                original = dict(self.state['prs']['22'])
                self.state['prs']['22'][field] = value
                self.assert_refused(self.gate(), 'prs', 'PR 22 must exist, be OPEN, be same-repository and target master')
                self.state['prs']['22'] = original
        self.assertTrue(self.gate()['ok'])

    def test_draft_pr_is_refused_before_any_candidate_work(self):
        sha = self.build()
        self.ci(sha)
        self.state['prs']['22']['draft'] = True
        refs = self.remote_refs()
        report = self.gate(dry_run=False)
        self.assert_refused(report, 'prs', 'PR 22 is a draft')
        for name in ('branches', 'fingerprint', 'candidate', 'ci', 'stable', 'push'):
            self.assertEqual(report['checks'][name]['status'], 'NOT-RUN', name)
        self.assertEqual(refs, self.remote_refs())
        self.assertFalse([call for call in self.gh_calls() if call[:2] == ['pr', 'ready']])

    def test_malformed_pr_head_sha_and_wrong_pr_number_are_refused(self):
        self.build()
        for value in ('not-a-sha', None):
            with self.subTest(head=value):
                self.state['prs']['21']['head'] = value
                self.assert_refused(self.gate(), 'prs', 'PR 21 head SHA missing or malformed')
        self.state['prs']['21'].update(head=self.heads[21], number=99)
        self.assert_refused(self.gate(), 'prs', 'PR 21 must exist')
        self.assert_refused(self.gate(('21',)), 'request', 'candidate must be')

    # ---- hygiene ----

    def test_extra_branch_is_refused_and_candidate_is_the_only_expected_extra(self):
        sha = self.build()
        self.ci(sha)
        self.assertTrue(self.gate()['ok'])
        self.build(name='land/other')
        self.assert_refused(self.gate(), 'branches', 'extra branches remain')

    def test_hygiene_evidence_must_be_complete(self):
        sha = self.build()
        self.ci(sha)
        with mock.patch.object(self.H, 'cwd_inventory', side_effect=self.H.Refusal('lsof inventory empty')):
            self.assert_refused(self.gate(), 'branches', 'hygiene evidence incomplete')

    def test_candidate_branch_must_exist_on_origin(self):
        self.assert_refused(self.gate(candidate='land/missing'), 'branches', 'candidate branch land/missing is not on origin')

    # ---- engine fingerprint ----

    def test_candidate_engine_change_is_refused(self):
        engine = 'code/memit/vendor/memit/memit_main.py'
        self.replace_pr(22, 'tk/T903', engine, (self.root / engine).read_text() + '# changed\n')
        sha = self.build()
        self.ci(sha)
        self.assert_refused(self.gate(), 'fingerprint', 'committed candidate engine fingerprint failed')

    # ---- candidate structure and tree ----

    def test_candidate_on_an_older_master_is_refused(self):
        sha = self.build()
        self.ci(sha)
        (self.root / 'later.txt').write_text('later\n')
        self.git('add', 'later.txt')
        self.git('commit', '-q', '-m', 'master moved')
        self.git('push', 'origin', 'master')
        self.assert_refused(self.gate(), 'candidate', 'does not start at current origin/master')

    def test_wrong_order_missing_pr_and_extra_commit_are_refused(self):
        cases = ((dict(order=(22, 21)), 'is not a two-parent merge of PR head'),
                 (dict(order=(21,)), 'is not a two-parent merge of PR head'),
                 (dict(extra_commit=True), 'is not a two-parent merge of PR head'))
        for build, text in cases:
            with self.subTest(**build):
                sha = self.build(**build)
                self.ci(sha)
                self.assert_refused(self.gate(), 'candidate', text)

    def test_tree_that_differs_from_the_recomputed_merge_is_refused_without_writing_objects(self):
        first = self.build(order=(21,), name='land/scratch')
        self.git('push', 'origin', '--delete', 'land/scratch')
        self.git('checkout', '-q', '--detach', first)
        (self.root / 'b.txt').write_text('evil\n')
        self.git('add', 'b.txt')
        tree = self.git('write-tree')
        self.git('checkout', '-q', '-f', 'master')
        sha = self.commit_tree(tree, first, self.heads[22])
        self.push_candidate(sha)
        self.ci(sha)
        objects = self.objects(self.root / '.git')
        self.assert_refused(self.gate(), 'candidate', 'tree differs from origin/master with the PR heads merged in order')
        self.assertEqual(objects, self.objects(self.root / '.git'))

    def test_conflicting_heads_are_refused(self):
        self.replace_pr(22, 'tk/T904', 'a.txt', 'other\n')
        first = self.build(order=(21,), name='land/scratch')
        self.git('push', 'origin', '--delete', 'land/scratch')
        sha = self.commit_tree(self.git('rev-parse', first + '^{tree}'), first, self.heads[22])
        self.push_candidate(sha)
        self.ci(sha)
        self.assert_refused(self.gate(), 'candidate', 'conflicts')

    def test_replace_refs_do_not_change_what_the_gate_sees(self):
        sha = self.build()
        self.ci(sha)
        self.git('replace', '--graft', sha, self.base)
        self.assertEqual(self.git('rev-list', '--parents', '-n', '1', sha).split()[1:], [self.base])
        report = self.gate()
        self.assertTrue(report['ok'], report['errors'])

    # ---- candidate CI ----

    def test_candidate_ci_must_complete_with_success_on_the_exact_sha_and_branch(self):
        sha = self.build()
        for kind, branch, text in (('FAIL', None, 'terminal conclusion is not success'),
                                   ('PENDING', None, 'bounded wait expired'),
                                   ('PASS', 'land/other', 'bounded wait expired')):
            with self.subTest(kind=kind, branch=branch):
                self.state['ci'] = {}
                self.ci(sha, kind, branch)
                report = self.gate()
                self.assert_refused(report, 'ci', text)
                if kind == 'FAIL':
                    self.assertNotIn('bounded wait expired', report['checks']['ci']['reason'])
        self.state['ci'] = {}
        self.ci(sha, 'PENDING:2')
        report = self.gate()
        self.assertTrue(report['ok'], report['errors'])
        self.assertGreater(self.clock.now, 0)

    def test_failing_run_of_another_event_on_the_candidate_is_refused(self):
        sha = self.build()
        self.ci(sha)
        self.state['extra_runs'] = [{'sha': sha, 'branch': self.candidate, 'kind': 'FAIL', 'id': 900, 'event': 'workflow_dispatch'}]
        self.assert_refused(self.gate(), 'ci', 'terminal conclusion is not success')

    def test_ci_for_another_push_branch_is_not_candidate_evidence(self):
        sha = self.build()
        self.state['ci'] = {}
        self.ci(sha)
        self.state_path.write_text(json.dumps(self.state))
        evidence = self.M.candidate_evidence(self.H.Gh(self.H.Repo(self.root, self.H.Deadline(60)), 'o/r'), sha, self.candidate)
        self.assertEqual(self.M.ci_state(evidence, sha, post=True, push_branch=self.candidate)[0], 'PASS')
        self.assertEqual(self.M.ci_state(evidence, sha, post=True, push_branch='land/other'),
                         ('FAIL', 'required CI workflow on the exact SHA is missing'))
        self.assertEqual(self.M.ci_state(evidence, sha, post=True)[1], 'required CI workflow on the exact SHA is missing')

    def test_malformed_or_capped_run_inventory_is_refused(self):
        sha = self.build()
        self.ci(sha)
        for payload, text in (({'workflow_runs': 'x'}, 'workflow run inventory malformed'),
                              ({'workflow_runs': [{}] * 100}, 'workflow run list is capped')):
            with self.subTest(text=text):
                self.state['runs_payload'] = payload
                self.assert_refused(self.gate(), 'ci', text)

    # ---- stability before the push ----

    def test_moved_pr_head_master_or_candidate_before_push_is_refused(self):
        for do, extra, text in (('pr-set', dict(pr='22', field='head', to='1' * 40), 'PR 22 moved'),
                                ('pr-set', dict(pr='22', field='state', to='CLOSED'), 'PR 22 moved'),
                                ('pr-set', dict(pr='22', field='base', to='release'), 'PR 22 moved'),
                                ('pr-set', dict(pr='22', field='cross', to=True), 'PR 22 moved'),
                                ('set', dict(key='api_master', to='UNRELATED'), 'origin/master or the candidate branch moved'),
                                ('move', dict(ref='master', to='UNRELATED'), 'origin/master or the candidate branch moved'),
                                ('move', dict(ref=self.candidate, to='BASE'), 'origin/master or the candidate branch moved')):
            with self.subTest(do=do, ref=extra.get('ref'), field=extra.get('field'), key=extra.get('key')):
                self.git('push', '-q', '-f', 'origin', self.base + ':refs/heads/master')
                self.git('fetch', '-q', 'origin')
                sha = self.build()
                self.state['ci'] = {}
                self.ci(sha)
                unrelated = self.commit_tree(self.git('rev-parse', self.base + '^{tree}'), self.base)
                self.git('push', '-f', 'origin', unrelated + ':refs/fixture/unrelated')  # outside refs/heads: not a branch
                target = {'UNRELATED': unrelated, 'BASE': self.base}.get(extra['to'], extra['to'])
                self.state['effects'] = [dict(on='candidate-runs', do=do, **dict(extra, to=target))]
                original = dict(self.state['prs']['22'])
                report = self.gate(dry_run=False)
                self.state['prs']['22'] = original
                self.state.pop('api_master', None)
                self.assert_refused(report, 'stable', text)
                self.assertEqual(report['checks']['push']['status'], 'NOT-RUN')

    def test_origin_master_moved_while_the_github_api_lags_is_refused(self):
        sha = self.build()
        self.ci(sha)
        unrelated = self.commit_tree(self.git('rev-parse', self.base + '^{tree}'), self.base)
        self.git('push', 'origin', unrelated + ':refs/fixture/unrelated')
        self.effect(on='candidate-runs', do='move', ref='master', to=unrelated)
        self.effect(on='candidate-runs', do='set', key='api_master', to=self.base)
        self.assert_refused(self.gate(), 'stable', 'origin/master or the candidate branch moved')

    # ---- apply ----

    def test_apply_fast_forwards_master_confirms_merged_waits_for_ci_and_deletes_only_the_candidate(self):
        sha = self.build()
        self.ci(sha)
        report = self.gate(dry_run=False)
        self.assertTrue(report['ok'], report['errors'])
        self.assertEqual(report['status'], 'MERGED')
        self.assertTrue(report['merged'])
        self.assertEqual(report['merge_sha'], sha)
        self.assertEqual(self.remote_tip('master'), sha)
        self.assertEqual(self.remote_tip(self.candidate), '')
        self.assertEqual((self.remote_tip('tk/T901'), self.remote_tip('tk/T902')), (self.heads[21], self.heads[22]))
        self.assertEqual(self.git('rev-parse', 'master'), self.base, 'local branches untouched')
        self.assertEqual([row['state'] for row in report['checks']['pr_merged']['evidence']], ['MERGED', 'MERGED'])
        self.assertEqual(report['checks']['master_ci']['evidence']['sha'], sha)
        pushes = self.pushes(report)
        self.assertEqual(len(pushes), 2)
        land, delete = pushes
        self.assertEqual(land[-3:], ['push', 'origin', sha + ':refs/heads/master'])
        self.assertFalse(any(arg.startswith(('-f', '--force', '+', '--mirror')) for arg in land[land.index('push'):]))
        self.assertEqual(delete[-4:], ['push', 'origin', '--delete', self.candidate])
        calls = [' '.join(c) for c in self.gh_calls()]
        master_ci = max(i for i, c in enumerate(calls) if 'branch=master' in c)
        merged = max(i for i, c in enumerate(calls) if c.startswith('pr view'))
        self.assertLess(merged, master_ci)

    def test_apply_refuses_when_origin_advertises_a_moved_master_at_push_time(self):
        sha = self.build()
        self.ci(sha)
        first = self.git('rev-parse', sha + '^1')
        self.effect(on='candidate-runs', nth=2, do='move', ref='master', to=first)
        report = self.gate(dry_run=False)
        self.assert_refused(report, 'push', 'origin/master moved or unexpected update', pushes=1)
        self.assertEqual(self.remote_tip('master'), first)
        self.assertEqual(self.remote_tip(self.candidate), sha)

    def test_each_recheck_inside_the_lock_refuses_a_change_before_push(self):
        stray = self.base
        for trigger, nth, effect, text in (('master-ref', 1, dict(ref='master', to='UNRELATED'), 'origin/master or the candidate branch moved'),
                                           ('pulls', 2, dict(ref='master', to='UNRELATED'), 'origin/master or the candidate branch moved'),
                                           ('master-ref', 2, dict(ref='stray', to=stray), 'extra branches remain')):
            with self.subTest(trigger=trigger, nth=nth, ref=effect['ref']):
                self.git('push', '-q', '-f', 'origin', self.base + ':refs/heads/master')
                self.git('push', '-q', 'origin', '--delete', 'stray', check=False)
                self.git('fetch', '-q', '--prune', 'origin')
                sha = self.build()
                self.state['ci'] = {}
                self.ci(sha)
                unrelated = self.commit_tree(self.git('rev-parse', self.base + '^{tree}'), self.base)
                self.git('push', '-f', 'origin', unrelated + ':refs/fixture/unrelated')
                self.state['effects'] = [dict(on=trigger, nth=nth, do='move', **dict(effect, to=unrelated if effect['to'] == 'UNRELATED' else effect['to']))]
                report = self.gate(dry_run=False)
                self.assert_refused(report, 'push', text)
                self.assertEqual(report['checks']['stable']['status'], 'PASS')

    def test_final_candidate_ci_failure_is_refused_before_push(self):
        sha = self.build()
        self.ci(sha)
        self.effect(on='master-ref', nth=3, do='add-run',
                    run={'sha': sha, 'branch': self.candidate, 'kind': 'FAIL', 'id': 4000, 'attempt': 2})
        self.assert_refused(self.gate(dry_run=False), 'push', 'final candidate CI refused')
        self.assertEqual(self.remote_tip('master'), self.base)

    def test_original_pre_push_hook_still_runs(self):
        sha = self.build()
        self.ci(sha)
        hook = self.root / '.git' / 'hooks' / 'pre-push'
        hook.write_text('#!/bin/sh\necho "repository pre-push hook refused" >&2\nexit 1\n')
        hook.chmod(0o755)
        self.assert_refused(self.gate(dry_run=False), 'push', 'repository pre-push hook refused', pushes=1)
        self.assertEqual(self.remote_tip('master'), self.base)

    def test_push_that_does_not_move_master_is_reported(self):
        sha = self.build()
        self.ci(sha)
        with mock.patch.object(self.M, 'push_master'):
            report = self.gate(dry_run=False)
        self.assert_landed_with_failure(report, 'push', 'origin/master is not the candidate after the push', sha)

    def test_github_master_ref_must_show_the_candidate_and_pr_heads_must_hold(self):
        for trigger, nth, effect, text in (('candidate-runs', 2, dict(do='set', key='api_master', to='BASE'), 'GitHub master ref does not show the candidate yet'),
                                           ('master-ref', 4, dict(do='pr-set', pr='22', field='head', to='1' * 40), 'PR 22 head changed after the push')):
            with self.subTest(trigger=trigger):
                self.git('push', '-q', '-f', 'origin', self.base + ':refs/heads/master')
                self.git('fetch', '-q', 'origin')
                self.state.pop('api_master', None)
                self.state['prs']['22']['head'] = self.heads[22]
                sha = self.build()
                self.state['ci'] = {}
                self.ci(sha)
                self.state['effects'] = [dict(on=trigger, nth=nth, **dict(effect, to=self.base if effect['to'] == 'BASE' else effect['to']))]
                self.assert_landed_with_failure(self.gate(dry_run=False), 'pr_merged', text, sha)

    def test_master_moving_during_master_ci_keeps_the_candidate(self):
        sha = self.build()
        self.ci(sha)
        self.effect(on='master-runs', do='set', key='api_master', to=self.base)
        self.assert_landed_with_failure(self.gate(dry_run=False), 'master_ci', 'master moved during post-merge verification', sha)

    def test_final_candidate_ci_evidence_change_is_refused_before_push(self):
        sha = self.build()
        self.ci(sha)
        self.effect(on='master-ref', nth=3, do='add-run',
                    run={'sha': sha, 'branch': self.candidate, 'kind': 'PASS', 'id': 4000, 'attempt': 2})
        report = self.gate(dry_run=False)
        self.assert_refused(report, 'push', 'CI evidence changed before push')
        self.assertEqual(self.remote_tip('master'), self.base)

    def test_apply_holds_the_git_automation_lock(self):
        sha = self.build()
        self.ci(sha)
        with (self.root / '.git' / 'git_automation.lock').open('a') as handle:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            report = self.gate(dry_run=False)
        self.assertFalse(report['ok'])
        self.assertFalse(report['merged'])
        self.assertIn('another git automation invocation is active', ' '.join(report['errors']))
        self.assertEqual(self.remote_tip('master'), self.base)

    def test_pr_that_never_shows_merged_keeps_the_candidate(self):
        sha = self.build()
        self.ci(sha)
        self.state['prs']['22']['never_merged'] = True
        self.assert_landed_with_failure(self.gate(dry_run=False), 'pr_merged', 'PR 22 does not show MERGED', sha)

    def test_master_ci_failure_after_push_keeps_the_candidate(self):
        sha = self.build()
        self.ci(sha)
        self.state['master_ci'] = 'FAIL'
        self.assert_landed_with_failure(self.gate(dry_run=False), 'master_ci', 'terminal conclusion is not success', sha)

    def test_candidate_is_kept_when_master_no_longer_contains_it(self):
        sha = self.build()
        self.ci(sha)
        self.effect(on='master-ref-after-master-ci', do='move', ref='master', to=self.base)
        report = self.gate(dry_run=False)
        self.assert_landed_with_failure(report, 'candidate_delete', 'origin/master does not contain the candidate', sha)
        self.assertEqual(self.remote_tip('master'), self.base)

    def test_push_error_after_master_moved_reports_merged(self):
        sha = self.build()
        self.ci(sha)
        original = self.M.push_master
        def push_then_fail(*args):
            original(*args)
            raise self.H.Refusal('connection reset after the ref update')
        with mock.patch.object(self.M, 'push_master', side_effect=push_then_fail):
            report = self.gate(dry_run=False)
        self.assert_landed_with_failure(report, 'push', 'connection reset after the ref update', sha)

    def test_push_error_with_unreadable_origin_reports_both_errors(self):
        sha = self.build()
        self.ci(sha)
        attempted, original = [], self.M.remote_tips
        def push(*args):
            attempted.append(args)
            raise self.H.Refusal('push rejected')
        def tips(*args):
            if attempted:
                raise self.H.Refusal('ls-remote failed')
            return original(*args)
        with mock.patch.object(self.M, 'push_master', side_effect=push), \
             mock.patch.object(self.M, 'remote_tips', side_effect=tips):
            report = self.gate(dry_run=False)
        self.assert_refused(report, 'push', 'push rejected; push outcome unverified: ls-remote failed')
        self.assertEqual(len(attempted), 1)

    # ---- CLI and CI trigger ----

    def run_cli(self, *argv):
        self.state_path.write_text(json.dumps(self.state))
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, 'argv', ['git_merge_gate.py', *argv]), \
             mock.patch.dict(os.environ, {'LLMDB_ROOT': str(self.root)}), \
             mock.patch.object(self.H, 'repository_name', return_value='o/r'), \
             redirect_stdout(out), redirect_stderr(err):
            code = self.M.main()
        return code, out.getvalue(), err.getvalue()

    def test_cli_batch_mode(self):
        sha = self.build()
        self.ci(sha)
        code, out, err = self.run_cli('--batch', '--candidate', self.candidate, '21', '22', '--dry-run')
        report = json.loads(out)
        self.assertEqual((code, report['status'], report['batch'], report['pr_numbers']), (0, 'DRY_RUN_PASS', True, [21, 22]))
        self.assertIn('PASS: bounded merge gate complete', err)
        code, out, err = self.run_cli('--batch', '--candidate', 'land/missing', '21', '--dry-run')
        self.assertEqual((code, json.loads(out)['status']), (1, 'REFUSED'))
        self.assertIn('REFUSE: branches:', err)
        code, out, err = self.run_cli('--batch', '--candidate', self.candidate, '21', '22', '--apply', '--ci-wait', '0')
        self.assertEqual((code, json.loads(out)['status']), (1, 'REFUSED'))
        self.assertIn('CI wait must be finite', err)
        for argv in (('--batch', '--candidate', self.candidate, '21'),
                     ('--batch', '--candidate', self.candidate, '21', '--apply', '--dry-run'),
                     ('--batch', '21', '--dry-run')):
            with self.subTest(argv=argv), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
                self.run_cli(*argv)
            self.assertEqual(raised.exception.code, 2)
        self.assertEqual(self.remote_tip('master'), self.base)

    def test_ci_workflow_runs_on_push_to_land_branches(self):
        text = (LANE / '.github/workflows/ci.yml').read_text()
        push = re.search(r'^on:\n  push:\n    branches: \[([^\]]*)\]\n', text, re.M)
        self.assertIsNotNone(push, 'on.push.branches flow list not found')
        self.assertEqual([b.strip().strip('"\'') for b in push.group(1).split(',')], ['master', 'land/**'])
        self.assertRegex(text, r'\n  pull_request:\n    branches: \[master\]\n')


if __name__ == '__main__':
    unittest.main()
