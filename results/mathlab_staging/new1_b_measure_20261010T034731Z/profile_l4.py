#!/usr/bin/env python3
"""One-layer CPU spending measurement; never a NEW1 worker or run authority."""
import argparse
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

DIRECTORY = Path(__file__).resolve().parent
ROOT = DIRECTORY.parents[2]
INPUT = Path('/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.4.mlp.down_proj_float32_mom2_t100_100000.npz')
INPUT_SHA = 'f6ae787454e5bae9eff52155ac699386351246b03e60ab68d728335b0c9a5b58'
PREREG_SHA = '216e8cfab513f0b555d8ae7908bd629e99e3b848cd2b43c054690962572cf771'
GEOMETRY_SHA = '3234b7f16b25d151d86ec508577abd42c1163a5b2b5318761b11b28675c2df67'
DEADLINE = 900
START = time.monotonic()


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def high_water(who=resource.RUSAGE_SELF):
    raw = resource.getrusage(who).ru_maxrss
    value = int(raw if sys.platform == 'darwin' else raw * 1024)
    return {'ru_maxrss_raw': raw, 'ru_maxrss_units': 'bytes' if sys.platform == 'darwin' else 'KiB',
            'peak_rss_bytes': value, 'peak_rss_GiB': value / 2**30,
            'source': 'getrusage process high-water; not sampled RSS'}


def emit(kind, **values):
    record = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'kind': kind,
              'pid': os.getpid(), 'elapsed_s': time.monotonic() - START,
              'process_high_water': high_water(), **values}
    with (DIRECTORY / 'receipt.jsonl').open('a') as stream:
        stream.write(json.dumps(record, allow_nan=False) + '\n')
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps(record, allow_nan=False), flush=True)


def validity(C, U, s, Vh, block=256, progress=None):
    """Frozen Frobenius formulas, plus V orthogonality, all float64 products."""
    import torch
    assert all(t.dtype == torch.float64 and t.device.type == 'cpu' for t in (C, U, s, Vh))
    d = C.shape[0]
    denominator = sum(float(C[:, j:j+block].square().sum()) for j in range(0, d, block))
    assert denominator > 0 and math.isfinite(denominator)
    errors = dict.fromkeys(('symmetry', 'svd', 'psd', 'orthogonality_U', 'orthogonality_V'), 0.)
    for j in range(0, d, block):
        end = min(d, j + block)
        reference = C[:, j:end]
        errors['symmetry'] += float((reference - C[j:end, :].T).square().sum())
        reconstructed = torch.zeros_like(reference)
        psd = torch.zeros_like(reference)
        orth_U = torch.empty_like(reference)
        orth_V = torch.empty_like(reference)
        for k in range(0, d, block):
            stop = min(d, k + block)
            scaled = U[:, k:stop] * s[k:stop]
            reconstructed += scaled @ Vh[k:stop, j:end]
            psd += scaled @ U[j:end, k:stop].T
            orth_U[k:stop] = U[:, k:stop].T @ U[:, j:end]
            orth_V[k:stop] = Vh[k:stop, :] @ Vh[j:end, :].T
        errors['svd'] += float((reference - reconstructed).square().sum())
        errors['psd'] += float((reference - psd).square().sum())
        rows = torch.arange(j, end)
        columns = torch.arange(end-j)
        orth_U[rows, columns] -= 1
        orth_V[rows, columns] -= 1
        errors['orthogonality_U'] += float(orth_U.square().sum())
        errors['orthogonality_V'] += float(orth_V.square().sum())
        if progress and ((j // block + 1) % 8 == 0 or end == d):
            progress(end, d)
    errors = {key: math.sqrt(value / (d if key.startswith('orthogonality_') else denominator))
              for key, value in errors.items()}
    assert all(math.isfinite(value) for value in errors.values())
    return errors


def configure():
    assert Path(os.environ['LLMDB_ROOT']).resolve() == ROOT.resolve()
    sys.path.insert(0, str(ROOT))
    import torch
    torch.set_num_threads(8)
    torch.set_num_interop_threads(1)
    assert torch.get_num_threads() == 8
    return torch


def spectrum_summary(s):
    allowed = s < .005
    def boundary(j):
        a, b = float(s[j-1]), float(s[j])
        relative = (a-b) / max(a, b, 1e-12 * float(s[0]))
        return {'index': j, 'upper': a, 'lower': b, 'relative_gap': relative,
                'frozen_gap_rule_pass': relative > 1e-4}
    return {'dtype': str(s.dtype), 'allowed_lt_0_005': int(allowed.sum()),
            'excluded_ge_0_005': int((~allowed).sum()),
            'min_abs_distance_from_real_0_005': float((s.double()-.005).abs().min()),
            'top_boundary': boundary(1024), 'bottom_boundary': boundary(len(s)-1024),
            'cutoff_boundary': boundary(int((~allowed).sum())) if 0 < int((~allowed).sum()) < len(s) else None}


def smoke():
    torch = configure()
    Q = torch.tensor([[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]], dtype=torch.float64) / 2
    s = torch.tensor([4., 3., 2., 1.], dtype=torch.float64)
    C = (Q * s) @ Q.T
    result = validity(C, Q, s, Q.T, block=2)
    assert all(value <= 1e-14 for value in result.values())
    Cbad = torch.diag(torch.tensor([4., 3., 2., -1.], dtype=torch.float64))
    result_bad = validity(Cbad, torch.eye(4, dtype=torch.float64), s,
                          torch.diag(torch.tensor([1., 1., 1., -1.], dtype=torch.float64)), block=2)
    assert result_bad['svd'] == 0 and result_bad['psd'] > 1e-5
    print(json.dumps({'smoke': 'PASS', 'rotated_PSD_errors': result, 'indefinite_errors': result_bad,
                      'real_inputs_read': False, 'SVD_calls': 0}), flush=True)


def worker():
    torch = configure()
    import numpy as np
    from tools import new1_geometry as G
    assert sha(ROOT/'tools/new1_geometry.py') == GEOMETRY_SHA
    assert sha(ROOT/'docs/NEW1_ADAPTER_GEOMETRY_PREREG.md') == PREREG_SHA
    assert G.PINNED[str(INPUT)] == INPUT_SHA
    emit('worker_started', torch_version=torch.__version__, numpy_version=np.__version__,
         threads=torch.get_num_threads(), interop_threads=torch.get_num_interop_threads(),
         torch_config=torch.__config__.show(), device='cpu', layer=4, nice_applied=False, scheduling_limit='sandbox denied os.nice(10) before any numerical import; no priority change attempted in this profile',
         input=str(INPUT), input_sha256=INPUT_SHA, prereg_sha256=PREREG_SHA,
         geometry_sha256=GEOMETRY_SHA, harness_sha256=sha(__file__),
         svd_driver='torch.linalg.svd CPU default, full_matrices=False; no driver override or retries',
         status_scope='Standalone spending measurement; no NEW1 dispatch or prediction verdict',
         native_basis_retained_through_double_checks=True,
         cross_projector_certification='UNVERIFIED; not measured in this bounded profile',
         frozen_thresholds={'symmetry': 1e-6, 'svd': 1e-5, 'psd': 1e-5, 'orthogonality_U': 1e-5},
         extra_diagnostic_threshold={'orthogonality_V': 1e-5})
    initial_stat = INPUT.stat()
    assert sha(INPUT) == INPUT_SHA
    C32 = G.load_covariance(INPUT)
    assert tuple(C32.shape) == (11008, 11008) and C32.dtype == torch.float32 and C32.device.type == 'cpu'
    emit('native_svd_started', shape=list(C32.shape), input_dtype=str(C32.dtype),
         normalization='G.load_covariance: np.divide(mom2.mom2,mom2.count,dtype=np.float32); no recentering or trace normalization')
    begin = time.monotonic()
    U32, s32, Vh32 = torch.linalg.svd(C32, full_matrices=False)
    native_wall = time.monotonic() - begin
    native = spectrum_summary(s32)
    emit('native_svd_finished', wall_s=native_wall, spectrum=native)
    del Vh32
    C64 = C32.double()
    del C32
    emit('float64_svd_started', shape=list(C64.shape), input_dtype=str(C64.dtype))
    begin = time.monotonic()
    U64, s64, Vh64 = torch.linalg.svd(C64, full_matrices=False)
    double_wall = time.monotonic() - begin
    double = spectrum_summary(s64)
    crossings = ((s32 < .005) != (s64 < .005)).nonzero(as_tuple=True)[0].tolist()
    emit('float64_svd_finished', wall_s=double_wall, spectrum=double, native_spectrum=native,
         cutoff_counts_equal=native['allowed_lt_0_005'] == double['allowed_lt_0_005'],
         indexed_cutoff_crossings=crossings)
    begin = time.monotonic()
    emit('validity_checks_started', block_columns=256)
    errors = validity(C64, U64, s64, Vh64,
                      progress=lambda done, total: emit('validity_progress', columns_checked=done, columns_total=total))
    checks_wall = time.monotonic() - begin
    gates = {key: value <= (1e-6 if key == 'symmetry' else 1e-5) for key, value in errors.items()}
    emit('validity_checks_finished', wall_s=checks_wall, errors=errors, gate_comparisons=gates,
         fifth_error_scope='V orthogonality extra diagnostic; not an additional adopted frozen gate')
    assert tuple(U32.shape) == tuple(U64.shape) == (11008, 11008)
    after_stat = INPUT.stat()
    assert (initial_stat.st_dev, initial_stat.st_ino, initial_stat.st_size, initial_stat.st_mtime_ns) == (after_stat.st_dev, after_stat.st_ino, after_stat.st_size, after_stat.st_mtime_ns)
    assert sha(INPUT) == INPUT_SHA
    assert sha(ROOT/'docs/NEW1_ADAPTER_GEOMETRY_PREREG.md') == PREREG_SHA
    emit('measurement_complete', native_svd_wall_s=native_wall, float64_svd_wall_s=double_wall,
         checks_wall_s=checks_wall, timed_pair_and_checks_s=native_wall+double_wall+checks_wall,
         errors=errors, gate_comparisons=gates, cutoff_counts_equal=native['allowed_lt_0_005'] == double['allowed_lt_0_005'],
         native_spectrum=native, float64_spectrum=double, indexed_cutoff_crossings=crossings,
         input_sha256_after=INPUT_SHA, numerical_interpretation='L4 covariance validity only; no prediction or projector-certification result')


def launch():
    assert not (DIRECTORY/'receipt.jsonl').exists(), 'One-shot profile receipt already exists; no rerun'
    emit('measurement_launch', deadline_s=DEADLINE, LLMDB_ROOT=os.environ.get('LLMDB_ROOT'),
         harness_sha256=sha(__file__), cpu_admission='UNVERIFIED: /bin/ps denied; baseline.json records explicit standalone measurement authorization')
    child = subprocess.Popen([sys.executable, '-B', str(Path(__file__).resolve()), '--worker'],
                             cwd=ROOT, start_new_session=True)
    try:
        code = child.wait(timeout=max(.001, DEADLINE - (time.monotonic()-START)))
    except subprocess.TimeoutExpired:
        os.killpg(child.pid, signal.SIGTERM)
        try:
            child.wait(timeout=2)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.wait()
        emit('measurement_timeout', deadline_s=DEADLINE, child_returncode=child.returncode,
             child_process_high_water=high_water(resource.RUSAGE_CHILDREN))
        return 124
    emit('measurement_process_exit', child_returncode=code,
         child_process_high_water=high_water(resource.RUSAGE_CHILDREN))
    return code


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args()
    try:
        if args.smoke:
            smoke()
        elif args.worker:
            worker()
        else:
            sys.exit(launch())
    except Exception as error:
        if not args.smoke:
            emit('measurement_failure', exception_type=type(error).__name__, message=str(error))
        raise
