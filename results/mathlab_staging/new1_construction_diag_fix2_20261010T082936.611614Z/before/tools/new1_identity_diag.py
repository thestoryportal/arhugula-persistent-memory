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
import threading
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


def wait_for_release():
    try:
        fd = int(os.environ['NEW1_IDENTITY_RELEASE_FD'])
        parent = int(os.environ['NEW1_IDENTITY_PARENT'])
        end = float(os.environ['NEW1_IDENTITY_RELEASE_BY'])
        deadline = float(os.environ['NEW1_IDENTITY_DEADLINE'])
    except (KeyError, ValueError) as error:
        raise S.Stop('INVALID-LAUNCH', 'parent release channel required') from error
    try:
        G.require(fd >= 0 and parent > 0 and math.isfinite(end) and math.isfinite(deadline) and end <= deadline,
                  'invalid release channel metadata')
        while True:
            remaining = end-time.monotonic()
            if remaining <= 0: raise S.Stop('STOPPED-LAUNCH', 'parent did not release worker within launch bound')
            if os.getppid() != parent: raise S.Stop('INVALID-LAUNCH', 'parent died before release')
            if select.select([fd], [], [], min(.1, remaining))[0]:
                if os.read(fd, 4) != b'RUN\n': raise S.Stop('INVALID-LAUNCH', 'release channel closed or invalid')
                if os.getppid() != parent or time.monotonic() >= end:
                    raise S.Stop('INVALID-LAUNCH', 'parent release arrived after cancellation')
                def guard():
                    while os.getppid() == parent and time.monotonic() < deadline:
                        time.sleep(min(.1, max(0, deadline-time.monotonic())))
                    # An independent thread terminates even while native arithmetic blocks the main thread.
                    os._exit(2)
                threading.Thread(target=guard, daemon=True).start()
                return
    finally: os.close(fd)


def supervise(command, directory, *, preflight, admission=cpu_admission, monitor=sample_rss, seconds=DEADLINE_S):
    start = time.monotonic()
    process, output, peak = None, None, 0.
    launch_thread, launch_error = None, None
    registered, cancelled = threading.Event(), threading.Event()
    ownership = threading.Lock()
    channel = [None, None]
    cleaned, cleanup_started = False, False
    def close_channel(index):
        with ownership:
            fd, channel[index] = channel[index], None
        if fd is not None: os.close(fd)
    def reap_and_close():
        nonlocal cleaned
        with ownership:
            if process is None or cleaned: return
            cleaned = True
        try:
            if process.poll() is None: S.terminate(process)
        finally:
            for pipe in (process.stdout, process.stderr):
                if pipe is not None: pipe.close()
    def spawn(end):
        nonlocal process, launch_error
        try:
            # Python signal exceptions run on the main thread, outside creation/registration.
            process = subprocess.Popen(command, cwd=ROOT, env=dict(os.environ,
                NEW1_IDENTITY_PARENT=str(os.getpid()), NEW1_IDENTITY_RELEASE_FD=str(channel[0]),
                NEW1_IDENTITY_RELEASE_BY=str(end), NEW1_IDENTITY_DEADLINE=str(start+seconds)), pass_fds=(channel[0],),
                start_new_session=True, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except BaseException as error: launch_error = error
        finally:
            registered.set()
            if cancelled.is_set():
                try: reap_and_close()
                except BaseException as error:
                    launch_error = error
                    print('INVALID-CLEANUP: late launch: ' + str(error), file=sys.stderr)
                finally: close_channel(0)
    def stop_and_close():
        nonlocal cleanup_started
        if cleanup_started: return
        cleanup_started = True
        cancelled.set()
        close_channel(1)
        try:
            with S.hard_deadline(CLEANUP_S):
                if launch_thread is not None and launch_thread.ident is not None:
                    launch_thread.join(timeout=CLEANUP_S)
                    if launch_thread.is_alive():
                        raise S.Stop('INVALID-CLEANUP', 'launch did not register within cleanup bound')
                reap_and_close()
        finally:
            if launch_thread is None or not launch_thread.is_alive(): close_channel(0)
    def pulse():
        nonlocal peak
        sample = monitor(process.pid if process is not None and process.poll() is None else None)
        rss = sample['rss_gib']
        if type(rss) not in (int, float) or not math.isfinite(rss) or rss < 0:
            raise S.Stop('INVALID-MONITORING', 'invalid RSS sample')
        peak = max(peak, rss)
        if rss >= RSS_CAP_GIB: raise S.Stop('STOPPED-RESOURCE', 'observed process-family RSS at or above 11 GiB')
        return sample
    try:
        with S.hard_deadline(seconds, heartbeat=pulse):
            output = Output(directory)
            output.record('started', deadline_s=seconds, rss_cap_gib=RSS_CAP_GIB,
                          parent_pid=os.getpid(), parent_nice=os.getpriority(os.PRIO_PROCESS, 0))
            output.record('resource', **pulse())
            preflight()
            decision = admission()
            output.record('admission', decision=decision)
            if not isinstance(decision, dict) or decision.get('allowed') is not True:
                raise S.Stop('INVALID-ADMISSION', 'fresh CPU admission refused: ' + str(decision))
            end = min(start+seconds, time.monotonic()+LAUNCH_S)
            channel[:] = os.pipe()
            launch_thread = threading.Thread(target=spawn, args=(end,), daemon=True)
            launch_thread.start()
            while not registered.wait(timeout=max(0, min(.05, end-time.monotonic()))):
                if time.monotonic() >= end:
                    if time.monotonic() >= start+seconds:
                        raise S.Stop('STOPPED-DEADLINE', 'whole-run wall-clock cap reached during launch')
                    raise S.Stop('STOPPED-LAUNCH', 'worker creation/registration exceeded launch bound')
            if launch_error is not None: raise launch_error
            output.record('worker', pid=process.pid)
            output.record('resource', **pulse())
            if time.monotonic() >= start+seconds:
                raise S.Stop('STOPPED-DEADLINE', 'whole-run wall-clock cap reached before release')
            if time.monotonic() >= end:
                raise S.Stop('STOPPED-LAUNCH', 'worker registration/checks exceeded launch bound')
            G.require(os.write(channel[1], b'RUN\n') == 4, 'worker release write incomplete')
            close_channel(1); close_channel(0)
            while True:
                try:
                    stdout, stderr = process.communicate(timeout=1)
                    break
                except subprocess.TimeoutExpired:
                    output.record('resource', **pulse())
            if process.returncode or stderr:
                raise S.Stop('INVALID-WORKER', f'exit {process.returncode}: ' + stderr.decode())
            value = S.strict_json(stdout.decode())
            if not isinstance(value, dict) or value.get('status') != 'MEASURED':
                raise S.Stop('INVALID-WORKER', 'nonempty measured scalar report required')
            value.update(elapsed_s=time.monotonic()-start, observed_peak_family_rss_gib=peak,
                         worker_pid=process.pid, caps={'deadline_s': DEADLINE_S, 'rss_gib': RSS_CAP_GIB,
                                                      'output_bytes_below': DISK_BYTES, 'threads': THREADS})
        stop_and_close()
        with S.hard_deadline(seconds-(time.monotonic()-start), heartbeat=pulse):
            output.finish(value)
        return 0
    except BaseException as error:
        cleanup_error = None
        try: stop_and_close()
        except BaseException as cleanup_failure:
            cleanup_error = str(cleanup_failure)
            print('INVALID-CLEANUP: ' + cleanup_error, file=sys.stderr)
        failure = {'status': 'INVALID', 'error': str(error),
                   'worker_pid': process.pid if process is not None else None,
                   'elapsed_s': time.monotonic()-start, 'observed_peak_family_rss_gib': peak}
        if cleanup_error is not None: failure['cleanup_error'] = cleanup_error
        try:
            with S.hard_deadline(CLEANUP_S):
                if output is not None:
                    if output.result.exists():
                        output.record('halted', **failure, result_committed=False,
                                      result_sha256=S.sha_file(output.result))
                    else:
                        output.finish(failure)
        except BaseException as recording_error:
            print('INVALID-OUTPUT: bounded terminal recording failed: ' + str(recording_error), file=sys.stderr)
        print(str(error), file=sys.stderr)
        return 130 if isinstance(error, KeyboardInterrupt) else 2
    finally:
        stop_and_close()


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
        with S.hard_deadline(DEADLINE_S):
            G.verify_file(Path(__file__), args.source_sha)
            directory = new_directory(ROOT / 'results/mathlab_staging/new1_identity_diag')
        command = [sys.executable, '-B', str(Path(__file__).resolve()), '--worker',
                   '--scope-sha', args.scope_sha, '--source-sha', args.source_sha]
        status = supervise(command, directory, preflight=lambda: verify_launch(args.scope_sha, args.source_sha),
                           seconds=DEADLINE_S-(time.monotonic()-start))
        print(str(directory))
        return status
    except (S.Stop, G.Invalid, OSError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__': sys.exit(main())
