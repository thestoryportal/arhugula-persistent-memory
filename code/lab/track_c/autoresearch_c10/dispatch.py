"""Trusted two-stage parent. No agent-controlled mode, path, or scorer argument."""
import hashlib
import importlib.util
import os
import math
from pathlib import Path
import struct
import subprocess
import sys
import time
import uuid

FENCE = Path(__file__).resolve().parent
ANCHOR = sys.argv[1]
if len(sys.argv) != 2:
    raise SystemExit('invalid trusted dispatch invocation')
# Verify every trusted helper before importing it (including startup dependency code).
import json as _json
import hashlib as _hashlib
_mpath = FENCE / 'sealed/manifest.json'
if _hashlib.sha256(_mpath.read_bytes()).hexdigest() != ANCHOR:
    raise SystemExit('trusted manifest mismatch')
for _path, _sha in _json.loads(_mpath.read_text()).items():
    _h = _hashlib.sha256()
    with open(_path, 'rb') as _stream:
        for _block in iter(lambda: _stream.read(1024 * 1024), b''):
            _h.update(_block)
    if _h.hexdigest() != _sha:
        raise SystemExit('trusted closure mismatch')
sys.path.insert(0, str(FENCE))
from v13_common import (ARMS, SUMMARY, clean_env, digest, gpu_exclusive, identity,
                        projection, read_json, snapshot, stop_stage, validate_handoff,
                        verify, write_json)
CONFIG = verify(FENCE, ANCHOR)
from v13_graft import freeze, sweep


def audit_ready():
    binding = {'session_id': 'unbound'}
    try:
        binding = read_json(FENCE / 'sealed/binding.json')
        heartbeat = read_json(FENCE / 'sealed/heartbeat.json')
        if (heartbeat['session_id'] != binding['session_id'] or heartbeat['status'] != 'ok'
                or time.time() - heartbeat['time'] > 10
                or identity(binding['watcher_pid']) != binding['watcher_identity']
                or not Path(binding['transcript']).is_file()
                or (FENCE / 'sealed/STOP.json').exists()):
            raise ValueError('audit unavailable')
        sweep(CONFIG)
        return binding
    except Exception as e:
        import audit_transcript as audit
        # The controller records the stop even when the watcher itself is missing.
        audit.stop(CONFIG, binding, 'parent audit unavailable: ' + type(e).__name__)
        raise


def stage(name, argv, cwd, env, log, timeout, run_deadline):
    ready_read = ready_write = None
    ready = bytearray()
    started = time.monotonic()
    if started >= run_deadline:
        raise TimeoutError('run timeout before stage start')
    if name == 'editor':
        ready_read, ready_write = os.pipe()
        os.set_blocking(ready_read, False)
        env = dict(env, C10_READY_FD=str(ready_write))
    with open(log, 'wb') as output:
        try:
            p = subprocess.Popen(argv, cwd=cwd, env=env, stdout=output, stderr=output,
                                 start_new_session=True, pass_fds=() if ready_write is None else (ready_write,))
        except BaseException:
            if ready_read is not None:
                os.close(ready_read)
                os.close(ready_write)
            raise
        if ready_write is not None:
            os.close(ready_write)
        record = None
        try:
            # Wait until sandbox-exec has replaced itself, or the short fixture exits.
            time.sleep(.15)
            if p.poll() is None:
                record = {'pid': p.pid, 'identity': identity(p.pid), 'stage': name,
                          'allowed_cwd': [str(cwd)], 'argv': argv}
                write_json(FENCE / 'sealed' / (name + '.pid.json'), record)
            deadline = min(started + timeout, run_deadline)
            while p.poll() is None:
                audit_ready()
                if ready_read is not None:
                    try:
                        ready.extend(os.read(ready_read, 8 - len(ready)))
                    except BlockingIOError:
                        pass
                    if len(ready) == 8:
                        stamp = struct.unpack('!d', ready)[0]
                        if not math.isfinite(stamp) or not started <= stamp <= time.monotonic():
                            raise ValueError('invalid editor start marker')
                        # A pipe delivers the trusted bootstrap's first marker before
                        # recipe code runs; the recipe cannot erase or extend it.
                        deadline = min(deadline, stamp + 2700)
                        os.close(ready_read)
                        ready_read = None
                if time.monotonic() >= deadline:
                    raise TimeoutError('stage timeout')
                time.sleep(.25)
            if p.returncode != 0:
                raise ValueError(name + ' stage failed')
        except BaseException:
            if p.poll() is None:
                if record is None:
                    raise ValueError('live stage has no verified identity')
                stop_stage(record, CONFIG)
                p.wait(timeout=5)
            raise
        finally:
            if p.poll() is not None:
                (FENCE / 'sealed' / (name + '.pid.json')).unlink(missing_ok=True)
            if ready_read is not None:
                os.close(ready_read)


def main():
    run_deadline = time.monotonic() + 7200
    sweep(CONFIG)
    audit_ready()
    if not CONFIG['fixture']:
        # A program-controlled equivalence driver may be this parent's ancestor.
        binding = read_json(FENCE / 'sealed/binding.json')
        ignore = {os.getpid(), os.getppid(), binding['watcher_pid']}
        if binding.get('role') == 'law3':
            if identity(binding['driver_pid']) != binding['driver_identity']:
                raise ValueError('LAW#3 driver identity changed')
            ignore.add(binding['driver_pid'])
        gpu_exclusive(ignore)
    run_id = time.strftime('%Y%m%d-%H%M%S') + '_nocommit_' + uuid.uuid4().hex
    root = Path(CONFIG['sandbox'])
    if root.is_symlink() or str(root.resolve()) != str(root):
        raise ValueError('sandbox root is not canonical')
    runs = root / 'runs'
    if runs.is_symlink():
        raise ValueError('invalid run root')
    runs.mkdir(exist_ok=True)
    run = runs / run_id
    run.mkdir()
    archive = FENCE / 'sealed/archive' / run_id
    private = FENCE / 'scorer_results' / run_id
    archive.mkdir(parents=True)
    private.mkdir(parents=True)
    snapshot(root / 'edit.py', archive / 'edit.py')
    write_json(archive / 'identity.json', {'sha256': digest(archive / 'edit.py'),
                                         'run_id': run_id, 'session_id': audit_ready()['session_id']})
    # Check the exact archived source through the program-side watcher code.
    spec = importlib.util.spec_from_file_location('_program_audit', FENCE / 'audit_transcript.py')
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    audit.scan_bound(CONFIG, audit_ready())
    snapshot(archive / 'edit.py', run / 'edit.py')
    os.chmod(run / 'edit.py', 0o444)
    editor_tmp = FENCE / 'editor_tmp' / run_id
    scorer_tmp = FENCE / 'scorer_tmp' / run_id
    editor_tmp.mkdir()
    scorer_tmp.mkdir()
    try:
        runtime = 'fixture_editor_bootstrap.py' if CONFIG['fixture'] else 'editor_bootstrap.py'
        stage('editor', ['/usr/bin/sandbox-exec', '-D', 'RUN=' + str(run),
                         '-D', 'STAGE_TMP=' + str(editor_tmp), '-f', str(FENCE / 'editor.sb'),
                         CONFIG['python'], '-I', '-B', '-X', 'pycache_prefix=' + str(editor_tmp / 'pycache'),
                         str(FENCE / runtime)], root,
              clean_env(CONFIG, editor_tmp, run), run / 'editor.log', 7200, run_deadline)
        audit.scan_bound(CONFIG, audit_ready())
        sweep(CONFIG)
        if digest(run / 'edit.py') != digest(archive / 'edit.py'):
            raise ValueError('recipe snapshot changed')
        for name in ['edits.json', *[a + '.pt' for a in ARMS]]:
            snapshot(run / name, private / name)
        validate_handoff(private)
        write_json(private / 'input_hashes.json', {n: digest(private / n) for n in
                                                  ['edits.json', *[a + '.pt' for a in ARMS]]})
        scorer = 'fixture_scorer.py' if CONFIG['fixture'] else 'scorer.py'
        stage('scorer', ['/usr/bin/sandbox-exec', '-D', 'RUN=' + str(private),
                         '-D', 'STAGE_TMP=' + str(scorer_tmp), '-f', str(FENCE / 'scorer.sb'),
                         CONFIG['python'], '-I', '-B', '-X', 'pycache_prefix=' + str(scorer_tmp / 'pycache'),
                         str(FENCE / scorer), ANCHOR, str(private)],
              FENCE, clean_env(CONFIG, scorer_tmp), private / 'scorer.log', 3600, run_deadline)
        audit.scan_bound(CONFIG, audit_ready())
        sweep(CONFIG)
        public = {'status': 'success', 'summary': projection(read_json(private / 'score.json'))}
        write_json(run / 'summary.json', public)
        print('status: success')
        for k in SUMMARY:
            value = public['summary'][k]
            print(k + ': ' + (str(value).lower() if isinstance(value, bool) else str(value)))
    except BaseException as e:
        write_json(private / 'failure.json', {'type': type(e).__name__, 'detail': str(e)})
        write_json(run / 'summary.json', {'status': 'failure'})
        print('status: failure')
        return 1
    finally:
        freeze(private)
        freeze(archive)
    return 0


if __name__ == '__main__':
    lock = FENCE / 'sealed/run.lock'
    fd = None
    try:
        fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        raise SystemExit(main())
    except Exception:
        # No scorer text, exception content, or phrase membership leaks to the agent.
        print('status: failure')
        raise SystemExit(1)
    finally:
        if fd is not None:
            os.close(fd)
            lock.unlink()
