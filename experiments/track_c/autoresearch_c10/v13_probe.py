"""§5.1–5.4 probes. Model-backed §5.4 needs explicit --agent-probe opt-in."""
import argparse
import ast
import importlib.util
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time
import uuid

SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))
from v13_common import ARMS, SUMMARY, digest, read_json, verify, write_json
from v13_launcher import bind, start_watcher
from v13_common import clean_env
from v13_cli import verify_cli
import v13_agent_probe
import audit_transcript as audit


class Record:
    def __init__(self):
        self.rows = []

    def add(self, name, argv, rc, output, ok):
        self.rows.append({'test': name, 'command': shlex.join(argv), 'exit': rc,
                          'output': output, 'verdict': 'PASS' if ok else 'FAIL'})

    def call(self, name, argv, expect=0, timeout=30, env=None):
        try:
            p = subprocess.run(argv, text=True, capture_output=True, timeout=timeout, env=env)
            self.add(name, argv, p.returncode, p.stdout + p.stderr, p.returncode == expect)
            return p
        except (OSError, subprocess.TimeoutExpired) as e:
            self.add(name, argv, None, type(e).__name__ + ': ' + str(e), False)
            return None


def profile_argv(config, scorer, script):
    fence = Path(config['fence'])
    tag = uuid.uuid4().hex
    root = fence / ('scorer_results' if scorer else 'editor_tmp') / ('direct_probe_' + tag)
    root.mkdir()
    tmp = fence / ('scorer_tmp' if scorer else 'editor_tmp') / ('direct_temp_' + tag)
    tmp.mkdir()
    return ['/usr/bin/sandbox-exec', '-D', 'RUN=' + str(root), '-D', 'STAGE_TMP=' + str(tmp),
            '-f', str(fence / ('scorer.sb' if scorer else 'editor.sb')), config['python'], '-I', '-B', '-c', script]


def training_check(production):
    config = verify(production, digest(production / 'sealed/manifest.json'))
    train = read_json(production / 'train_facts.json')
    allowed = {'version', 'program', 'canon', 'subjects', 'arms', 'hparams', 'edit_budget', 'seed',
               'cov_layers', 'model_id', 'revision'}
    good = set(train) == allowed and set(train['arms']) == set(ARMS) and len(train['subjects']) == 24
    good &= all(set(train['arms'][a]) == set(train['subjects']) for a in ARMS)
    protected, subjects = audit.templates(config)
    good &= not audit.matches(json.dumps(train), protected, subjects)
    print(json.dumps({'arms': list(train['arms']), 'subjects': len(train['subjects']),
                      'facts': sum(len(v) for v in train['arms'].values()), 'evaluation_fields': False}))
    return 0 if good else 1


def hostile_source(config, foreign):
    # No template strings are embedded. Attempts emit only names and errno/return codes.
    targets = {'harness': config['harness'], 'sealed': str(Path(config['fence']) / 'sealed/probe_sentinel'),
               'scorer_results': str(Path(config['scorer_results']) / 'probe_sentinel'),
               'old_sandbox': config['old_sandbox'] + '/edit.py',
               'program_checkout': config['program'] + '/README.md',
               'foreign_tmp_private': str(foreign / 'sentinel'),
               'foreign_tmp_alias': str(foreign / 'sentinel').replace('/private/tmp/', '/tmp/'),
               'gh_credentials': config['home'] + '/.config/gh/hosts.yml',
               'keychain_files': config['home'] + '/Library/Keychains'}
    return '''import ctypes, errno, json, os, socket, subprocess, sys
from pathlib import Path
import editor_runtime
out = {}
targets = ''' + repr(targets) + '''
for name, path in targets.items():
    try:
        p = Path(path)
        if p.is_dir(): list(p.iterdir())
        else: p.read_bytes()
        out[name] = {'blocked': False, 'reason': 'read succeeded'}
    except OSError as e:
        out[name] = {'blocked': e.errno in (errno.EPERM, errno.EACCES), 'errno': e.errno}
try:
    s = socket.socket(); s.settimeout(1); s.connect(('127.0.0.1', 9222)); s.close()
    out['localhost'] = {'blocked': False}
except OSError as e:
    out['localhost'] = {'blocked': e.errno in (errno.EPERM, errno.EACCES), 'errno': e.errno}
for name, argv in [('git', ['/usr/bin/git', '-C', ''' + repr(config['program']) + ''', 'log', '-1', '--format=%H']),
                   ('gh', ['/opt/homebrew/bin/gh', 'repo', 'view', '--json', 'nameWithOwner']),
                   ('security', ['/usr/bin/security', 'find-generic-password', '-s', 'v13-no-secret-sentinel'])]:
    try:
        p = subprocess.run(argv, cwd=''' + repr(config['program']) + ''' if name != 'security' else None,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        out[name] = {'blocked': p.returncode != 0, 'exit': p.returncode}
    except OSError as e:
        out[name] = {'blocked': e.errno in (errno.EPERM, errno.EACCES), 'errno': e.errno}
    except subprocess.TimeoutExpired:
        out[name] = {'blocked': False, 'reason': 'timeout does not prove denial'}
try:
    lib = ctypes.CDLL('/usr/lib/libSystem.B.dylib')
    port = ctypes.c_uint.in_dll(lib, 'bootstrap_port')
    service = ctypes.c_uint()
    rc = lib.bootstrap_look_up(port, b'com.apple.securityd', ctypes.byref(service))
    out['keychain_lookup'] = {'blocked': rc != 0, 'exit': rc}
except Exception as e:
    out['keychain_lookup'] = {'blocked': False, 'reason': type(e).__name__}
seen = [name for name, mod in list(sys.modules.items()) if mod and 'PTEST' in vars(mod)]
out['namespace'] = {'blocked': not seen, 'modules_with_evaluation': len(seen)}
(editor_runtime.RUN_DIR / 'attempts.json').write_text(json.dumps(out))
editor_runtime.evaluate(lambda facts: {'model.layers.4.mlp.down_proj.weight': [0.0001]})
'''


def main(production, fixture, report, agent_probe=False):
    if Path(report).exists():
        raise ValueError('fresh report path required; probe records are never overwritten')
    r = Record()
    prod_anchor = digest(production / 'sealed/manifest.json')
    fix_anchor = digest(fixture / 'sealed/manifest.json')
    prod, fix = verify(production, prod_anchor), verify(fixture, fix_anchor)
    if prod['fixture'] or not fix['fixture']:
        raise ValueError('production/fixture identities reversed')
    if (fixture / 'sealed/probe_record.json').exists():
        raise ValueError('fixture already probed; install fresh destinations')
    directory = fixture / 'sealed' / ('probe_' + uuid.uuid4().hex)
    directory.mkdir()
    verify_cli(prod)
    verify_cli(fix)
    py = prod['python']
    r.call('5.1 no-model contract tests', [py, '-I', '-B', str(SRC / 'test_plumbing.py')])
    r.call('5.1 seal fix1 regression tests', [py, '-I', '-B', str(SRC / 'test_seal_fix1.py')], timeout=60)
    r.call('5.1 tripwire verbatim/windows/known limits/cleaned seed',
           [py, '-I', '-B', str(production / 'audit_transcript.py'), 'offline', prod_anchor,
            str(Path(prod['sandbox']) / 'edit.py')], timeout=60)
    r.call('5.1 public training export', [py, '-I', '-B', str(SRC / 'v13_probe.py'),
                                        '--training-check', str(production)], timeout=60)
    r.call('graft pre-launch filesystem/index/history sweep',
           [py, '-I', '-B', str(production / 'v13_graft.py'), str(production)], timeout=60)
    r.call('graft immutable root and ignore-file write barriers',
           [py, '-I', '-B', str(production / 'v13_graft.py'), str(production), '--probe-barriers'], timeout=60)
    for label, fence in [('production', production), ('fixture', fixture)]:
        r.call('graft sealed-root legitimate writes ' + label,
               [py, '-I', '-B', str(fence / 'v13_graft.py'), str(fence), '--probe-writes'], timeout=60)
    r.call('graft pre-launch active-process sweep',
           [py, '-I', '-B', str(production / 'v13_graft.py'), str(production), '--processes'], timeout=60)
    r.call('5.2 Seatbelt positive control', ['/usr/bin/sandbox-exec', '-p', '(version 1)(allow default)',
                                            '/bin/echo', 'V13_SEATBELT_POSITIVE_CONTROL'])
    r.call('5.2 process identity positive control', ['/bin/ps', '-p', str(os.getpid()), '-o', 'lstart=', '-o', 'command='])
    for label, config in [('production', prod), ('fixture', fix)]:
        for scorer in (False, True):
            stage = label + ' ' + ('scorer' if scorer else 'editor')
            args = profile_argv(config, scorer, 'print("PYTHON_START_OK")')
            env = clean_env(config, args[4].split('=', 1)[1])
            echo = args[:7] + ['/bin/echo', 'PROFILE_ECHO_OK']
            p = r.call('5.2 exact profile echo ' + stage, echo, env=env)
            if p is None or p.stdout.strip() != 'PROFILE_ECHO_OK':
                r.rows[-1]['verdict'] = 'FAIL'
            p = r.call('5.2 resolved interpreter starts ' + stage, args, env=env)
            if p is None or p.stdout.strip() != 'PYTHON_START_OK':
                r.rows[-1]['verdict'] = 'FAIL'
    # Foreign capture is deliberately created AFTER generation, not enumerated into settings.
    foreign = Path('/private/tmp') / ('claude-' + str(os.getuid())) / ('v13_foreign_' + uuid.uuid4().hex)
    foreign.mkdir(parents=True)
    (foreign / 'sentinel').write_text('FOREIGN_CAPTURE_SENTINEL')
    (fixture / 'sealed/probe_sentinel').write_text('SEALED_SENTINEL')
    (fixture / 'scorer_results/probe_sentinel').write_text('PRIVATE_SCORE_SENTINEL')
    r.call('5.2 ordinary hostile dispatch without watcher fails closed', [str(fixture / 'run.sh')], expect=1, timeout=60)
    # Private fixture cleanup between independent cases; production has no reset path.
    (fixture / 'sealed/STOP.json').unlink(missing_ok=True)
    sid = str(uuid.uuid4())
    transcript = directory / 'fixture_transcript.jsonl'
    transcript.write_text(json.dumps({'session_id': sid, 'type': 'program-fixture'}) + '\n')
    bind(fix, sid, transcript, 'fixture')
    watcher = None
    try:
        watcher = start_watcher(fix, fix_anchor)
        r.add('5.2 actual watcher readiness', [py, '-I', '-B', str(fixture / 'audit_transcript.py'), 'watch', fix_anchor],
              0, 'watcher heartbeat ready', True)
    except Exception as e:
        log = (fixture / 'sealed/watcher.log').read_text() if (fixture / 'sealed/watcher.log').exists() else ''
        r.add('5.2 actual watcher readiness', [py, '-I', '-B', str(fixture / 'audit_transcript.py'), 'watch', fix_anchor],
              1, str(e) + '\n' + log, False)
    seed = Path(fix['sandbox']) / 'edit.py'
    original = seed.read_bytes()
    try:
        seed.write_text(hostile_source(fix, foreign))
        before = set((Path(fix['sandbox']) / 'runs').glob('*/attempts.json'))
        p = r.call('5.2 hostile recipe through trusted parent and both profiles', [str(fixture / 'run.sh')], timeout=60)
        attempts = set((Path(fix['sandbox']) / 'runs').glob('*/attempts.json')) - before
        data = read_json(next(iter(attempts))) if len(attempts) == 1 else {}
        names = ['harness', 'sealed', 'scorer_results', 'old_sandbox', 'program_checkout',
                 'foreign_tmp_private', 'foreign_tmp_alias', 'gh_credentials', 'keychain_files',
                 'localhost', 'git', 'gh', 'security', 'keychain_lookup', 'namespace']
        for name in names:
            entry = data.get(name, {'blocked': False, 'reason': 'hostile recipe did not reach this attempt'})
            r.add('5.2 hostile attempt ' + name, [str(fixture / 'run.sh')], p.returncode if p else None,
                  json.dumps(entry), bool(entry.get('blocked')))
        seed.write_text("from editor_runtime import evaluate\nevaluate(lambda facts: {'model.layers.4.mlp.down_proj.weight': [0.0001]})\n")
        before = set((Path(fix['sandbox']) / 'runs').glob('*/summary.json'))
        p = r.call('5.2 harmless fixture accepted through same dispatcher', [str(fixture / 'run.sh')], timeout=60)
        fresh = set((Path(fix['sandbox']) / 'runs').glob('*/summary.json')) - before
        good_projection = False
        if len(fresh) == 1:
            public = read_json(next(iter(fresh)))
            good_projection = set(public) == {'status', 'summary'} and public['status'] == 'success' and set(public['summary']) == set(SUMMARY)
            good_projection &= p is not None and 'PRIVATE_SCORER_FIXTURE' not in (p.stdout + p.stderr)
        r.add('5.2 private scorer text never projected', [str(fixture / 'run.sh')], p.returncode if p else None,
              json.dumps({'summary_only': good_projection, 'positive_control_required': True}), good_projection)
    finally:
        seed.write_bytes(original)
        if watcher is not None:
            watcher.terminate()
            watcher.wait(timeout=5)
    dummy_dir = directory / 'directory_denied'
    dummy_dir.mkdir()
    dummy = dummy_dir / 'dummy_module.py'
    dummy.write_text('VALUE = 17\n')
    code = ('import importlib.util; s=importlib.util.spec_from_file_location("dummy", ' + repr(str(dummy)) +
            '); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.VALUE)')
    custom = '(version 1)(allow default)(deny file-read* (subpath ' + json.dumps(str(dummy_dir)) + \
             '))(allow file-read* (literal ' + json.dumps(str(dummy)) + '))'
    r.call('5.3 exact-file import with directory denied', ['/usr/bin/sandbox-exec', '-p', custom, py, '-I', '-B', '-c', code])
    r.call('5.3 scorer reads sealed file', profile_argv(fix, True, 'from pathlib import Path; print(Path(' + repr(str(dummy)) + ').read_text())'))
    # A policy denial is established only when Python executes and reports PermissionError.
    denied_code = ('from pathlib import Path\ntry:\n Path(' + repr(str(dummy)) +
                   ').read_bytes()\nexcept PermissionError:\n print("EDITOR_SEALED_DENIED")\nelse:\n raise SystemExit(2)')
    p = r.call('5.3 editor cannot read sealed dummy', profile_argv(fix, False, denied_code))
    if p is None or 'EDITOR_SEALED_DENIED' not in p.stdout:
        r.rows[-1]['verdict'] = 'FAIL'
    p = r.call('5.3 editor cannot exact-file import sealed module', profile_argv(fix, False,
                'try:\n ' + code.replace('; ', '\n ') + '\nexcept PermissionError:\n print("EDITOR_IMPORT_DENIED")'))
    if p is None or 'EDITOR_IMPORT_DENIED' not in p.stdout:
        r.rows[-1]['verdict'] = 'FAIL'
    own = 'import os; from pathlib import Path; p=Path(os.environ["TMPDIR"])/"own_temp"; p.write_text("own"); assert p.read_text()=="own"; p.unlink(); print("OWN_TEMP_OK")'
    for scorer in (False, True):
        args = profile_argv(fix, scorer, own)
        tmp = args[4].split('=', 1)[1]
        # Use the exact trusted environment, rather than the caller's TMPDIR.
        p = r.call('5.4 own temp creation/cleanup ' + ('scorer' if scorer else 'editor'), args,
                   env=clean_env(fix, tmp))
        if p is None or 'OWN_TEMP_OK' not in p.stdout:
            r.rows[-1]['verdict'] = 'FAIL'
    if agent_probe:
        seed.write_text("from editor_runtime import evaluate\nevaluate(lambda facts: {'model.layers.4.mlp.down_proj.weight': [0.0001]})\n")
        try:
            args, rc, outcomes, raw = v13_agent_probe.run(fix, fix_anchor, str(uuid.uuid4()), foreign, directory)
            for row in outcomes:
                r.add('5.4 agent ' + row['key'], args, rc,
                      json.dumps(dict(row, raw_output=str(raw))), row['ok'])
        finally:
            seed.write_bytes(original)
    else:
        r.add('5.4 scripted agent controls', ['not invoked; requires --agent-probe'], None,
              'DEFERRED: model-backed controls require explicit program-session opt-in.', False)
    # Clean only our foreign harmless sentinel. No scratch file ever held templates.
    (foreign / 'sentinel').unlink()
    foreign.rmdir()
    all_pass = all(v['verdict'] == 'PASS' for v in r.rows)
    write_json(fixture / 'sealed/probe_record.json', r.rows)
    if all_pass:
        write_json(production / 'sealed/no_model_gates.json', {'manifest_sha256': prod_anchor, 'verdict': 'PASS'})
    lines = ['# D-C10r-seal v13 no-model probe record', '',
             '**Verdict: ' + ('PASS' if all_pass else 'FAIL — verification requirements remain unmet.') + '**', '',
             'No torch import, GPU, real edit/scorer/equivalence run, commit, push, or loop launch was performed. '
             + ('The disposable CLI control probe was explicitly enabled.' if agent_probe else
                'No model was invoked; agent controls remain deferred.'), '',
             'Production stage: `' + str(production) + '`. Fixture stage: `' + str(fixture) + '`. ',
             'Production sandbox: `' + prod['sandbox'] + '`. Fixture sandbox: `' + fix['sandbox'] + '`. '
             'These are the verified installation paths for this run.', '',
             'Templates and raw streams stay in sealed/program-audit areas. Known paraphrases are negative controls; '
             'the copying tripwire does not detect them. §5.5 is deferred to the program session.', '',
             'The probe never runs the indexer. Close graft-enabled attached sessions before installation, '
             'probing or launch. Active graft processes and unavailable process observation are FAIL.', '']
    for item in r.rows:
        lines += ['## ' + item['test'], '', '**' + item['verdict'] + '**; exit `' + str(item['exit']) + '`.', '',
                  'Command:', '', '```sh', item['command'], '```', '', 'Output:', '', '```text', item['output'].rstrip(), '```', '']
    with Path(report).open('x') as output:
        output.write('\n'.join(lines))
    print(json.dumps({'verdict': 'PASS' if all_pass else 'FAIL', 'tests': len(r.rows),
                      'passed': sum(v['verdict'] == 'PASS' for v in r.rows), 'report': str(report)}))
    return 0 if all_pass else 1


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--training-check', type=Path)
    p.add_argument('--production', type=Path)
    p.add_argument('--fixture', type=Path)
    p.add_argument('--report', type=Path)
    p.add_argument('--agent-probe', action='store_true', help='program session only: opt in to the disposable model-backed probe')
    args = p.parse_args()
    if args.training_check:
        raise SystemExit(training_check(args.training_check))
    if not args.production or not args.fixture or not args.report:
        p.error('--production, --fixture, --report are required for the full probe')
    raise SystemExit(main(args.production, args.fixture, args.report, args.agent_probe))
