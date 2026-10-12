#!/usr/bin/env python3
"""D-NEW1-b identity diagnostic. Build permission does not authorize launch."""
import os, sys
LLMDB_ROOT = os.environ.get('LLMDB_ROOT', '/workspace')
import argparse
from contextlib import ExitStack
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import select
import subprocess
import signal
import hmac
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import new1_geometry as G
from tools import new1_supervisor as S

DEADLINE_S, RSS_CAP_GIB, THREADS, DISK_BYTES = 600, 11., 8, 1000000
CLEANUP_S = 5
LAUNCH_S = 5
SCOPE = ROOT / 'results/mathlab_staging/new1_identity_diag_scope.md'
SOURCE_PINS = {
    'tools/new1_geometry.py': '018ce4d97f817ecd816a4fd3fb47316e78fda7007984449e93f423d0eb1f4a5e',
    'tools/new1_supervisor.py': 'a69d410724b65a5dbacaf8e34fc45b73c9f545daf54eda9b6cfeb150e344557b',
    'memit_dry_run/memit/util/runningstats.py': '7b3a05de007733ec3243c13362d3c24b6cb9c09f32eedbcf36de02c98a49ac97',
    'experiments/track_c/c10e_bandknob.py': '1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695',
    'results/mathlab_staging/new1_b_identity_diag_authorization.md': 'daa41ea90df6a1ed1a73c4f03289f6f384dc97756f6b4ba93d4766535aad05c1',
    'results/mathlab_staging/new1_b_halt_astra.md': '9b4c5e90079bb52f7aef6824d2ace3fae292e6a0cf91d5ba62000589c5f2b5be',
}
HARVEST_COMMIT = '6ea8e7c07156133667a8d6d28364f759ba1d7a31'
HARVEST_SHA = '9dbc58afef1aa290d5e01622d3324b052e3f19169bfeb8d38ad19148cfe869bb'
CACHE = next(p for p in G.PINNED if p.endswith('model.layers.4.mlp.down_proj_float32_mom2_t100_100000.npz'))
CAPTURE, MANIFEST = str(G.H / 'inloop_A7_coined_coined.pt'), str(G.H / 'manifest.json')
INPUT_PINS = {p: G.PINNED[p] for p in (CACHE, CAPTURE, MANIFEST)}


def verify_pins(root, pins):
    for path, expected in pins.items(): G.verify_file(Path(root) / path, expected)


def verify_launch(scope_sha, source_sha):
    G.verify_file(Path(__file__), source_sha)
    G.verify_file(SCOPE, scope_sha)
    verify_pins(ROOT, SOURCE_PINS)
    historical = subprocess.run(['git', 'show', HARVEST_COMMIT + ':tools/mathlab_harvest.py'],
                                cwd=ROOT, capture_output=True, timeout=5, check=True).stdout
    G.require(hashlib.sha256(historical).hexdigest() == HARVEST_SHA, 'historical harvest source SHA mismatch')
    G.require(Path(LLMDB_ROOT).resolve() == ROOT, 'LLMDB_ROOT must equal this worktree')
    G.require(os.environ.get('LLMDB_DEVICE') == 'cpu' and os.environ.get('CUDA_VISIBLE_DEVICES') == '',
              'CPU environment required')
    G.require(all(os.environ.get(k) == str(THREADS) for k in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS')),
              'eight OMP/MKL threads required')
    G.require(os.getpriority(os.PRIO_PROCESS, 0) == 10, 'nice 10 required')
    verify_pins(ROOT, INPUT_PINS)


def normalization_paths(moment, count):
    import numpy as np
    torch = G.torch_module()
    G.require(moment.dtype == np.float32 and moment.ndim == 2 and moment.shape[0] == moment.shape[1],
              'covariance shape/dtype')
    G.require(count.shape == () and count.dtype == np.int64 and int(count) > 0,
              'moment count must be positive scalar int64')
    G.finite(torch.from_numpy(moment))
    values = {'A': torch.from_numpy(np.divide(moment, count, dtype=np.float32)),
              'B': torch.from_numpy(moment) / int(count)}
    for value in values.values(): G.finite(value)
    return values


def maximum_difference(A, B):
    G.finite(A); G.finite(B)
    G.require(A.shape == B.shape, 'normalized covariance shape mismatch')
    return max(float((A[i:i+256].double() - B[i:i+256].double()).abs().max())
               for i in range(0, len(A), 256))


def probe_metrics(actual, reference):
    G.finite(actual); G.finite(reference)
    G.require(actual.ndim == 1 and actual.shape == reference.shape, 'probe shape mismatch')
    norm = float(reference.double().norm())
    G.require(norm > 0, 'captured probe has zero norm')
    residual = actual.double() - reference.double()
    absolute = float(residual.norm())
    relative = absolute / norm
    G.require(math.isfinite(relative), 'nonfinite probe relative error')
    return {'relative_error': relative, 'absolute_l2_residual': absolute,
            'max_absolute_residual': float(residual.abs().max()),
            'actual_l2_norm': float(actual.double().norm()), 'captured_l2_norm': norm,
            'match': 'MATCH' if relative <= 1e-6 else 'NO-MATCH'}


def path_report(C, expected_allowed, expected_sha, probes):
    torch = G.torch_module(); G.finite(C)
    G.require(C.dtype == torch.float32 and C.ndim == 2 and C.shape[0] == C.shape[1], 'native fp32 covariance required')
    G.require(len(probes) == 4, 'four captured probes required')
    U, s, Vh = torch.linalg.svd(C, full_matrices=False)
    G.finite(U); G.finite(s)
    idx = (s < .005).nonzero(as_tuple=True)[0]
    P = U[:, idx] @ U[:, idx].T
    allowed, excluded = len(idx), int((s >= .005).sum())
    del U, s, Vh, idx
    digest = G.tensor_sha(P)
    metrics = [{'seed': j, **probe_metrics(
        P @ torch.randn(C.shape[0], generator=torch.Generator().manual_seed(j)), reference)}
        for j, reference in enumerate(probes)]
    all_match = all(item['match'] == 'MATCH' for item in metrics)
    return {'excluded_count': excluded, 'allowed_count': allowed, 'projector_sha256': digest,
            'captured_allowed_count': expected_allowed, 'count_matches': allowed == expected_allowed,
            'captured_projector_sha256': expected_sha, 'projector_sha_matches': digest == expected_sha,
            'probes': metrics, 'max_probe_relative_error': max(p['relative_error'] for p in metrics),
            'all_probes_match_1e6': all_match,
            'matches_capture_gate': allowed == expected_allowed and (digest == expected_sha or all_match)}


def measure():
    import numpy as np
    torch = G.torch_module()
    torch.set_num_threads(THREADS)
    with ExitStack() as stack:
        bound = {p: stack.enter_context(G.bound_input(ROOT / p, sha)) for p, sha in INPUT_PINS.items()}
        with np.load(bound[CACHE], allow_pickle=False) as data:
            values = normalization_paths(data['mom2.mom2'], data['mom2.count'])
        G.require(values['A'].shape == (11008, 11008), 'L4 covariance dimensions changed')
        manifest = S.strict_json(bound[MANIFEST].read_text())
        bundle = torch.load(bound[CAPTURE], map_location='cpu', weights_only=True, mmap=True)
        count, digest = bundle['l4.Pi_null_n'], bundle['l4.Pi_sha256']
        G.require(count.dtype == torch.int64 and count.shape == () and 0 <= int(count) <= 11008,
                  'captured projector count metadata invalid')
        G.require(digest.dtype == torch.uint8 and digest.shape == (32,), 'captured projector SHA metadata invalid')
        probes = [bundle[f'l4.Pi_probe{j}'].clone() for j in range(4)]
        for probe in probes:
            G.require(probe.dtype == torch.float32 and probe.shape == (11008,), 'captured probe dtype/shape invalid')
            G.finite(probe)
        hashes = {key: G.tensor_sha(C) for key, C in values.items()}
        difference = maximum_difference(values['A'], values['B'])
        expected_allowed, expected_sha = int(count), bytes(digest.tolist()).hex()
        del bundle, count, digest
        paths = {}
        for key in ('A', 'B'):
            C = values.pop(key)
            paths[key] = path_report(C, expected_allowed, expected_sha, probes)
            del C
    return {'status': 'MEASURED', 'purpose': 'identity diagnostic only; no prediction verdict',
            'layer': 4, 'normalized_C_sha256': hashes, 'max_absolute_normalized_C_difference': difference,
            'paths': paths, 'input_pins': INPUT_PINS, 'source_pins': SOURCE_PINS,
            'provenance': {'torch_version': torch.__version__, 'numpy_version': np.__version__,
                'get_num_threads': torch.get_num_threads(), 'backend': torch.__config__.show(),
                'device': 'cpu', 'dtype': 'float32', 'svd_driver': 'CPU default, full_matrices=False',
                'nice': os.getpriority(os.PRIO_PROCESS, 0),
                'captured_torch_version': manifest.get('torch_version'), 'captured_threads': 'UNKNOWN',
                'historical_harvest_commit': HARVEST_COMMIT, 'historical_harvest_sha256': HARVEST_SHA},
            'limitations': 'Four probes are sampled discrepancies, not full subspace distance or behavioral evidence.'}


def family_rss(inventory, root_pid, worker_pid=None):
    rows = {}
    try:
        for line in inventory.splitlines():
            pid, parent, rss = map(int, line.split())
            if pid <= 0 or parent < 0 or rss < 0 or pid in rows: raise ValueError('invalid or duplicate process row')
            rows[pid] = parent, rss
        if root_pid not in rows: raise ValueError('parent absent from inventory')
        family = {root_pid}
        while True:
            expanded = family | {p for p, (parent, _) in rows.items() if parent in family}
            if expanded == family: break
            family = expanded
        if worker_pid is not None and worker_pid not in family: raise ValueError('live worker absent from family inventory')
        return {'rss_gib': sum(rows[p][1] for p in family) / (1 << 20), 'process_count': len(family)}
    except (ValueError, TypeError) as error:
        raise S.Stop('INVALID-MONITORING', str(error)) from error


def sample_rss(worker_pid=None):
    try:
        proc = subprocess.run(['/bin/ps', '-axo', 'pid=,ppid=,rss='], capture_output=True, text=True, timeout=1)
        if proc.returncode or not proc.stdout.strip(): raise ValueError(proc.stderr or 'empty process inventory')
        return family_rss(proc.stdout, os.getpid(), worker_pid)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        raise S.Stop('INVALID-MONITORING', str(error)) from error


def new_directory(base):
    base = Path(base)
    base.mkdir(parents=True, exist_ok=True)
    directory = base / ('identity_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'))
    directory.mkdir()
    return directory


class Output:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.receipt = self.directory / 'receipt.jsonl'
        self.result = self.directory / 'result.json'
        if self.result.exists(): raise FileExistsError(self.result)
        with self.receipt.open('xb'): pass

    def check_size(self, extra):
        size = sum(p.stat().st_size for p in self.directory.iterdir() if p.is_file())
        if size + extra >= DISK_BYTES: raise S.Stop('STOPPED-DISK', 'combined output must be below 1000000 bytes')

    def record(self, kind, **value):
        data = (json.dumps({'utc': datetime.now(timezone.utc).isoformat(), 'kind': kind, **value},
                           allow_nan=False) + '\n').encode()
        self.check_size(len(data) + (8192 if kind not in ('terminal', 'halted') else 0))
        with self.receipt.open('ab') as out:
            out.write(data); out.flush(); os.fsync(out.fileno())

    def finish(self, value):
        self.check_size(len((json.dumps(value, indent=2, allow_nan=False) + '\n').encode()) + 1024)
        proof = S.durable_json(self.result, value)
        self.record('terminal', status=value['status'], result_sha256=proof['sha256'])


def cpu_admission():
    from tools import mathlab_admit
    return mathlab_admit.probe('cpu')


def read_frame(fd, limit, end, parent):
    data = bytearray()
    while True:
        remaining = end-time.monotonic()
        if remaining <= 0: raise S.Stop('STOPPED-LAUNCH', 'release frame/EOF deadline reached')
        if os.getppid() != parent: raise S.Stop('INVALID-LAUNCH', 'guardian died before release')
        if not select.select([fd], [], [], min(.01, remaining))[0]: continue
        chunk = os.read(fd, limit+1-len(data))
        if not chunk: return bytes(data)
        data.extend(chunk)
        if len(data) > limit: raise S.Stop('INVALID-LAUNCH', 'release frame exceeds bound')


def release_frame(secret):
    return b'RUN '+secret.hex().encode()+b'\n'


def wait_for_release():
    fds = []
    try:
        for key in ('NEW1_IDENTITY_AUTH_FD', 'NEW1_IDENTITY_RELEASE_FD'):
            fd = int(os.environ[key])
            if fd < 3 or fd in fds: raise ValueError('invalid private descriptor')
            fds.append(fd)
        parent = int(os.environ['NEW1_IDENTITY_PARENT'])
        end = float(os.environ['NEW1_IDENTITY_RELEASE_BY'])
        deadline = float(os.environ['NEW1_IDENTITY_DEADLINE'])
        if parent != os.getppid() or not math.isfinite(end) or not math.isfinite(deadline) or end > deadline:
            raise ValueError('invalid registration metadata')
        secret = read_frame(fds[0], 32, end, parent)
        frame = read_frame(fds[1], 69, end, parent)
        if len(secret) != 32 or not hmac.compare_digest(frame, release_frame(secret)):
            raise S.Stop('INVALID-LAUNCH', 'private registration secret/release mismatch')
        if os.getppid() != parent or time.monotonic() >= end:
            raise S.Stop('INVALID-LAUNCH', 'release arrived after cancellation')
    except (KeyError, ValueError) as error:
        raise S.Stop('INVALID-LAUNCH', 'authenticated parent registration/release required') from error
    finally:
        for fd in fds: os.close(fd)


def keep_descriptors(keep):
    for name in os.listdir('/dev/fd'):
        fd = int(name)
        if fd > 2 and fd not in keep:
            try: os.close(fd)
            except OSError as error:
                # listdir's own descriptor has closed since the snapshot.
                if error.errno != 9: raise


def kill_worker(pid):
    try: os.killpg(pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        # A group signal can be refused while the owned PID remains signalable.
        try: os.kill(pid, signal.SIGKILL)
        except ProcessLookupError: pass


def watchdog(owner, command, parent, work_end, absolute_end):
    p = owner.channels
    pid, status, kills, error = None, None, 0, None
    events = p['events'][1]
    def send(value):
        try: os.write(events, (json.dumps(value, allow_nan=False)+'\n').encode())
        except BrokenPipeError:
            if os.getppid() == parent: raise
    def kill():
        nonlocal kills
        if pid is not None and status is None and kills == 0:
            kill_worker(pid); kills = 1
    try:
        signal.setitimer(signal.ITIMER_REAL, 0)
        for sig in (signal.SIGINT, signal.SIGALRM): signal.signal(sig, signal.SIG_IGN)
        signal.pthread_sigmask(signal.SIG_SETMASK, [])
        os.setsid()
        pid = os.fork()
        if pid == 0:
            try:
                for sig in (signal.SIGINT, signal.SIGALRM): signal.signal(sig, signal.SIG_DFL)
                os.setsid()
                null = os.open(os.devnull, os.O_RDONLY)
                os.dup2(null, 0); os.dup2(p['stdout'][1], 1); os.dup2(p['stderr'][1], 2)
                os.write(p['ready'][1], b'READY\n'); os.close(p['ready'][1])
                env = dict(os.environ, NEW1_IDENTITY_PARENT=str(os.getppid()),
                    NEW1_IDENTITY_AUTH_FD=str(p['auth'][0]), NEW1_IDENTITY_RELEASE_FD=str(p['release'][0]),
                    NEW1_IDENTITY_RELEASE_BY=str(owner.launch_end), NEW1_IDENTITY_DEADLINE=str(work_end))
                for fd in (p['auth'][0], p['release'][0]): os.set_inheritable(fd, True)
                keep_descriptors({p['auth'][0], p['release'][0]})
                os.chdir(ROOT); os.execvpe(command[0], command, env)
            except BaseException as failure:
                os.write(2, ('INVALID-LAUNCH: '+str(failure)+'\n').encode()); os._exit(2)
        keep_descriptors({p['control'][0], events, p['ready'][0]})
        null = os.open(os.devnull, os.O_RDWR)
        for fd in (0, 1, 2): os.dup2(null, fd)
        if null > 2: os.close(null)
        send({'event': 'registered', 'pid': pid})
        ack, ack_fd = bytearray(), p['ready'][0]
        while status is None:
            watch = [p['control'][0]] + ([ack_fd] if ack_fd is not None else [])
            readable, _, _ = select.select(watch, [], [], .005)
            if ack_fd in readable:
                chunk = os.read(ack_fd, 8-len(ack)); ack.extend(chunk)
                if len(ack) > 6: raise S.Stop('INVALID-LAUNCH', 'registration exceeds bound')
                if not chunk:
                    if ack != b'READY\n': raise S.Stop('INVALID-LAUNCH', 'worker group registration missing')
                    send({'event': 'ready', 'pid': pid}); os.close(ack_fd); ack_fd = None
            # Drain the pre-exec ACK before observing a fast worker's exit.
            if ack_fd is None:
                reaped, value = os.waitpid(pid, os.WNOHANG)
                if reaped == pid:
                    status = value; break
            if p['control'][0] in readable:
                os.read(p['control'][0], 1); kill()
            if os.getppid() != parent or time.monotonic() >= work_end: kill()
            if time.monotonic() >= absolute_end: os._exit(2)
    except BaseException as failure:
        error = str(failure)
    finally:
        kill()
        while pid is not None and status is None:
            reaped, value = os.waitpid(pid, os.WNOHANG)
            if reaped == pid: status = value; break
            if time.monotonic() >= absolute_end: os._exit(2)
            time.sleep(min(.005, max(0, absolute_end-time.monotonic())))
        send({'event': 'reaped', 'pid': pid, 'code': os.waitstatus_to_exitcode(status) if status is not None else None,
              'kills': kills, 'error': error})
        os._exit(0 if error is None else 2)


class OwnedWorker:
    def __init__(self, launch_end):
        self.launch_end = launch_end
        self.channels = {}
        self.streams = {}
        self.buffers = {key: bytearray() for key in ('stdout', 'stderr', 'events')}
        self.pid = self.worker_pid = self.returncode = self.proof = None
        self.ready = self.stopping = False

    def close_fd(self, key, index):
        previous = signal.pthread_sigmask(signal.SIG_BLOCK, [])
        try:
            signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGINT, signal.SIGALRM])
            pair = self.channels[key]
            if pair[index] is not None:
                os.close(pair[index]); pair[index] = None
        finally: signal.pthread_sigmask(signal.SIG_SETMASK, previous)

    def start(self, command, work_end, absolute_end):
        previous = signal.pthread_sigmask(signal.SIG_BLOCK, [])
        try:
            signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGINT, signal.SIGALRM])
            for key in ('control', 'events', 'ready', 'auth', 'release', 'stdout', 'stderr'):
                self.channels[key] = list(os.pipe())
            parent = os.getpid()
            self.pid = os.fork()
            if self.pid == 0:
                try: watchdog(self, command, parent, work_end, absolute_end)
                finally: os._exit(2)
            for key in self.channels:
                if key == 'ready': self.close_fd(key, 0); self.close_fd(key, 1)
                else: self.close_fd(key, 0 if key in ('control', 'auth', 'release') else 1)
            for key in ('stdout', 'stderr', 'events'):
                fd = self.channels[key][0]; os.set_blocking(fd, False); self.streams[fd] = key
        finally:
            # All descriptors and the raw kernel PID belong to this object before delivery.
            signal.pthread_sigmask(signal.SIG_SETMASK, previous)

    def request_stop(self):
        self.stopping = True
        for key in ('auth', 'release', 'control'):
            if key in self.channels: self.close_fd(key, 1)

    def step(self, seconds):
        readable = select.select(list(self.streams), [], [], max(0, seconds))[0] if self.streams else []
        previous = signal.pthread_sigmask(signal.SIG_BLOCK, [])
        try:
            signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGINT, signal.SIGALRM])
            for fd in readable:
                key = self.streams[fd]; data = os.read(fd, 4096)
                if not data:
                    self.close_fd(key, 0); del self.streams[fd]; continue
                if self.stopping and key != 'events': continue
                self.buffers[key].extend(data)
                if key != 'events' and sum(len(self.buffers[k]) for k in ('stdout', 'stderr')) >= DISK_BYTES//2:
                    raise S.Stop('STOPPED-DISK', 'worker scalar streams exceed memory bound')
                if key == 'events':
                    if len(self.buffers[key]) > 4096: raise S.Stop('INVALID-LAUNCH', 'watchdog receipts exceed bound')
                    while b'\n' in self.buffers[key]:
                        line, _, rest = self.buffers[key].partition(b'\n'); self.buffers[key][:] = rest
                        item = S.strict_json(line.decode())
                        if item['event'] == 'registered':
                            G.require(self.worker_pid is None and type(item['pid']) is int and item['pid'] > 0,
                                      'duplicate or invalid worker registration')
                            self.worker_pid = item['pid']
                        elif item['event'] == 'ready':
                            G.require(item['pid'] == self.worker_pid and not self.ready, 'group registration mismatch')
                            self.ready = True
                        elif item['event'] == 'reaped':
                            G.require(item['pid'] == self.worker_pid and self.proof is None and item['kills'] in (0, 1),
                                      'worker reaping identity mismatch')
                            self.proof = item
                        else: raise S.Stop('INVALID-LAUNCH', 'unknown watchdog receipt')
            if self.pid is not None and self.returncode is None:
                pid, status = os.waitpid(self.pid, os.WNOHANG)
                if pid == self.pid: self.returncode = os.waitstatus_to_exitcode(status)
        finally: signal.pthread_sigmask(signal.SIG_SETMASK, previous)

    def release(self):
        G.require(self.ready and self.proof is None and not self.stopping, 'unregistered worker cannot be released')
        secret = os.urandom(32)
        G.require(os.write(self.channels['auth'][1], secret) == 32, 'private secret write incomplete')
        self.close_fd('auth', 1)
        frame = release_frame(secret)
        G.require(os.write(self.channels['release'][1], frame) == len(frame), 'release write incomplete')
        self.close_fd('release', 1)

    def close(self):
        for key, pair in self.channels.items():
            for index in range(len(pair)): self.close_fd(key, index)
        self.streams.clear()


def check_enforcement():
    mask = signal.pthread_sigmask(signal.SIG_BLOCK, [])
    if mask.intersection((signal.SIGALRM, signal.SIGINT)):
        raise S.Stop('INVALID-ENFORCEMENT', 'caller blocks SIGALRM or SIGINT')
    return mask


def supervise(command, directory, *, preflight, admission=cpu_admission, monitor=sample_rss,
              seconds=DEADLINE_S, absolute_end=None):
    caller_mask = check_enforcement()
    if signal.getitimer(signal.ITIMER_REAL)[0]:
        raise S.Stop('INVALID-ENFORCEMENT', 'a pre-existing alarm cannot be replaced')
    deferred = []
    phase, busy = None, False
    def on_signal(number, frame):
        nonlocal busy
        closing = False
        if phase is not None:
            cursor = frame
            while cursor is not None:
                if cursor.f_code is deadline_until.__exit__.__code__ and cursor.f_locals['self'] is phase:
                    closing = True; break
                cursor = cursor.f_back
        if number == signal.SIGINT or phase is None or closing:
            deferred.append(number); return
        # An injected signal leaves the scheduled OS timer armed; keep that deadline intact.
        if signal.getitimer(signal.ITIMER_REAL)[0] > 0:
            deferred.append(number); return
        try:
            if phase.alarm_error is not None: raise phase.alarm_error
            remaining = phase.limit-time.monotonic()
            if remaining <= 0 or phase.heartbeat is None:
                raise S.Stop('STOPPED-DEADLINE', 'whole-run wall-clock cap reached')
            if busy: raise S.Stop('INVALID-MONITORING', 'recursive resource watchdog')
            busy = True
            signal.setitimer(signal.ITIMER_REAL, remaining)
            try: phase.heartbeat()
            finally: busy = False
            remaining = phase.limit-time.monotonic()
            if remaining <= 0: raise S.Stop('STOPPED-DEADLINE', 'whole-run wall-clock cap reached')
            signal.setitimer(signal.ITIMER_REAL, min(S.SAMPLE_S, remaining))
        except BaseException as error:
            if phase.alarm_error is None: phase.alarm_error = error
            remaining = end-time.monotonic()
            if remaining <= 0:
                os._exit(2)
            # Active callback cleanup remains timed until the owning context actually exits.
            signal.setitimer(signal.ITIMER_REAL, min(.01, remaining))
            raise phase.alarm_error
    class deadline_until:
        def __init__(self, limit, heartbeat=None):
            self.limit, self.heartbeat, self.alarm_error = limit, heartbeat, None

        def __enter__(self):
            nonlocal phase
            try:
                mask = signal.pthread_sigmask(signal.SIG_BLOCK, [])
                try:
                    signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGINT, signal.SIGALRM])
                    G.require(phase is None, 'nested deadline phase')
                    phase = self
                    remaining = self.limit-time.monotonic()
                    if remaining <= 0: raise S.Stop('STOPPED-DEADLINE', 'whole-run wall-clock cap reached')
                    signal.setitimer(signal.ITIMER_REAL, min(S.SAMPLE_S, remaining) if self.heartbeat else remaining)
                finally: signal.pthread_sigmask(signal.SIG_SETMASK, mask)
            except BaseException:
                self.__exit__(*sys.exc_info()); raise
            return self

        def __exit__(self, kind, error, traceback):
            nonlocal phase
            clearing = False
            mask = signal.pthread_sigmask(signal.SIG_BLOCK, [])
            try:
                signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGINT, signal.SIGALRM])
            finally:
                try:
                    clearing = True
                    if phase is self:
                        signal.setitimer(signal.ITIMER_REAL, 0); phase = None
                finally: signal.pthread_sigmask(signal.SIG_SETMASK, mask)
            if error is None and time.monotonic() >= self.limit:
                raise S.Stop('STOPPED-DEADLINE', 'whole-run wall-clock cap reached')
            return False
    previous = {sig: signal.getsignal(sig) for sig in (signal.SIGINT, signal.SIGALRM)}
    try:
        mask = signal.pthread_sigmask(signal.SIG_BLOCK, [])
        try:
            signal.pthread_sigmask(signal.SIG_BLOCK, list(previous))
            for sig in previous: signal.signal(sig, on_signal)
        finally: signal.pthread_sigmask(signal.SIG_SETMASK, mask)
        start = time.monotonic(); end = start+seconds if absolute_end is None else absolute_end
        reserve = min(2*CLEANUP_S, max(0, end-start)/2)
        work_end, reap_end = end-reserve, end-reserve/2
        owner, output, peak = None, None, 0.
        cleanup_complete = False
        def check_cancel():
            if signal.SIGINT in deferred: raise KeyboardInterrupt("supervisor interrupted")
            if deferred: raise S.Stop("INVALID-CANCELLED", "alarm received outside active deadline phase")
        def pulse():
            nonlocal peak
            check_cancel()
            pid = owner.worker_pid if owner is not None and owner.proof is None else None
            sample = monitor(pid); rss = sample['rss_gib']
            if type(rss) not in (int, float) or not math.isfinite(rss) or rss < 0:
                raise S.Stop('INVALID-MONITORING', 'invalid RSS sample')
            peak = max(peak, rss)
            if rss >= RSS_CAP_GIB: raise S.Stop('STOPPED-RESOURCE', 'observed process-family RSS at or above 11 GiB')
            return sample
        def stop_and_close(limit):
            nonlocal cleanup_complete
            if cleanup_complete: return
            if owner is not None:
                owner.request_stop()
                while owner.pid is not None and (owner.returncode is None or owner.proof is None):
                    if time.monotonic() >= limit: raise S.Stop('STOPPED-DEADLINE', 'reserved worker/guardian reaping bound reached')
                    owner.step(min(.005, limit-time.monotonic()))
                    if owner.returncode is not None and not owner.streams and owner.proof is None:
                        raise S.Stop('INVALID-CLEANUP', 'guardian exit lacks worker reaping proof')
                owner.close()
            cleanup_complete = True
        def cleanup(limit):
            stop_and_close(limit)
        try:
            with deadline_until(work_end, heartbeat=pulse):
                output = Output(directory)
                output.record('started', deadline_s=seconds, rss_cap_gib=RSS_CAP_GIB,
                              parent_pid=os.getpid(), parent_nice=os.getpriority(os.PRIO_PROCESS, 0))
                output.record('resource', **pulse()); preflight()
                decision = admission(); output.record('admission', decision=decision)
                if not isinstance(decision, dict) or decision.get('allowed') is not True:
                    raise S.Stop('INVALID-ADMISSION', 'fresh CPU admission refused: '+str(decision))
            launch_end = min(work_end, time.monotonic()+LAUNCH_S)
            owner = OwnedWorker(launch_end)
            try:
                with deadline_until(launch_end, heartbeat=pulse):
                    owner.start(command, work_end, end)
                    check_cancel()
                    while not owner.ready:
                        owner.step(min(.005, max(0, launch_end-time.monotonic())))
                        check_cancel()
                        if owner.proof is not None: raise S.Stop('INVALID-WORKER', 'worker exited before registration')
                    output.record('worker', pid=owner.worker_pid); output.record('resource', **pulse())
                    if time.monotonic() >= launch_end: raise S.Stop('STOPPED-LAUNCH', 'registration checks exceeded launch bound')
                    check_cancel()
                    owner.release()
            except S.Stop as error:
                if error.code == 'STOPPED-DEADLINE' and launch_end < work_end:
                    raise S.Stop('STOPPED-LAUNCH', 'worker creation/registration exceeded launch bound') from error
                raise
            with deadline_until(work_end, heartbeat=pulse):
                while owner.proof is None or owner.streams:
                    owner.step(min(.02, max(0, work_end-time.monotonic())))
                    check_cancel()
                if time.monotonic() >= work_end:
                    raise S.Stop('STOPPED-DEADLINE', 'whole-run work reserve reached')
                stdout, stderr = bytes(owner.buffers['stdout']), bytes(owner.buffers['stderr'])
                if owner.proof['code'] or stderr or owner.proof['error']:
                    raise S.Stop('INVALID-WORKER', f"exit {owner.proof['code']}: "+stderr.decode())
                value = S.strict_json(stdout.decode())
                if not isinstance(value, dict) or value.get('status') != 'MEASURED':
                    raise S.Stop('INVALID-WORKER', 'nonempty measured scalar report required')
                value.update(elapsed_s=time.monotonic()-start, observed_peak_family_rss_gib=peak,
                             worker_pid=owner.worker_pid, caps={'deadline_s': DEADLINE_S, 'rss_gib': RSS_CAP_GIB,
                             'output_bytes_below': DISK_BYTES, 'threads': THREADS})
            cleanup(min(reap_end, time.monotonic()+CLEANUP_S))
            if deferred: raise S.Stop('INVALID-CANCELLED', 'interrupt deferred until confirmed reaping')
            if owner.returncode: raise S.Stop('INVALID-WORKER', 'guardian did not exit normally')
            with deadline_until(end, heartbeat=pulse):
                output.finish(value)
                check_cancel()
            return 0
        except BaseException as error:
            cleanup_error = None
            try: cleanup(min(reap_end, time.monotonic()+CLEANUP_S))
            except BaseException as failure:
                cleanup_error = str(failure)
                try: cleanup(end)
                except BaseException:
                    # No terminal receipt or Python return can claim unconfirmed ownership.
                    os._exit(2)
            failure = {'status': 'INVALID', 'error': str(error), 'worker_pid': owner.worker_pid if owner else None,
                       'elapsed_s': time.monotonic()-start, 'observed_peak_family_rss_gib': peak}
            if cleanup_error is not None: failure['cleanup_error'] = cleanup_error
            try:
                with deadline_until(min(end, time.monotonic()+CLEANUP_S)):
                    if output is not None:
                        if output.result.exists():
                            output.record('halted', **failure, result_committed=False, result_sha256=S.sha_file(output.result))
                        else: output.finish(failure)
                    print(str(error), file=sys.stderr)
            except BaseException as recording_error:
                try:
                    with deadline_until(end):
                        print('INVALID-OUTPUT: bounded terminal recording failed: '+str(recording_error), file=sys.stderr)
                        print(str(error), file=sys.stderr)
                except BaseException:
                    os._exit(2)
            return 130 if isinstance(error, KeyboardInterrupt) else 2


    finally:
        try:
            signal.pthread_sigmask(signal.SIG_BLOCK, list(previous))
        finally:
            try:
                signal.setitimer(signal.ITIMER_REAL, 0)
                phase = None
                for sig, handler in previous.items(): signal.signal(sig, handler)
            finally: signal.pthread_sigmask(signal.SIG_SETMASK, caller_mask)


def main(argv=None):
    start = time.monotonic()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope-sha', required=True)
    parser.add_argument('--source-sha', required=True)
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        if args.worker:
            G.require(os.environ.get('NEW1_IDENTITY_PARENT') == str(os.getppid()), 'only the diagnostic parent may dispatch')
            wait_for_release()
            verify_launch(args.scope_sha, args.source_sha)
            value = measure()
            value.update(scope_sha256=args.scope_sha, diagnostic_source_sha256=args.source_sha)
            data = json.dumps(value, allow_nan=False)
            G.require(len(data.encode()) < DISK_BYTES // 2, 'worker scalar report too large')
            print(data)
            return 0
        check_enforcement()
        with S.hard_deadline(start+DEADLINE_S-time.monotonic()):
            G.verify_file(Path(__file__), args.source_sha)
            directory = new_directory(ROOT / 'results/mathlab_staging/new1_identity_diag')
        command = [sys.executable, '-B', str(Path(__file__).resolve()), '--worker',
                   '--scope-sha', args.scope_sha, '--source-sha', args.source_sha]
        status = supervise(command, directory, preflight=lambda: verify_launch(args.scope_sha, args.source_sha),
                           seconds=DEADLINE_S, absolute_end=start+DEADLINE_S)
        print(str(directory))
        return status
    except (S.Stop, G.Invalid, OSError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__': sys.exit(main())
