#!/usr/bin/env python3
"""D-NEW1-b four-construction diagnostic; MAESTRO3 owns the real launch."""
import os, sys
LLMDB_ROOT = os.environ['LLMDB_ROOT']
import argparse
from contextlib import ExitStack
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import new1_identity_diag as I
G, S = I.G, I.S

SCOPE = ROOT / 'results/mathlab_staging/new1_construction_diag_scope.md'
DIMENSION = 11008
CACHE, CAPTURE, MANIFEST, INPUT_PINS = I.CACHE, I.CAPTURE, I.MANIFEST, I.INPUT_PINS
SOURCE_PINS = {**I.SOURCE_PINS,
    'tools/new1_identity_diag.py': '1161503c55346fb5d47bbed462ec3de3b17698b0b94752dfef4d7bf4d0e2ff8a',
    'results/mathlab_staging/new1_construction_diag_authorization.md': 'e7c445af835248b6722e04449f4f6a88a41c4d39f03fc6da41841c8ea23254f5',
    'results/mathlab_staging/new1_identity_diag_astra.md': 'cdc1a94a3a361aa1d26e363b67eb02c694e1425fc0576542ddf8810000912f20',
    'tools/mathlab_admit.py': 'bd3b6312ce3edcb599591c3559e85adfb13bb45c13e26942ee2eec9aacfe2abc',
    'tools/mathlab_runtime.py': '416b597c1309f7dcabb065749e05da9ce28743b1d16c9791ae1eed527a4a72c5',
    'tools/mathlab_events.py': '53b2ea18ea8a363136e967c25bb0e8a94f88a63070f3921a3b996e2287459f5f',
    'docs/NEW1_ADAPTER_GEOMETRY_PREREG.md': '1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f',
}
CONSTRUCTIONS = (('list_shared', 'list', 'shared'), ('list_separate', 'list', 'separate'),
                 ('long_shared', 'long', 'shared'), ('long_separate', 'long', 'separate'))


def verify_historical_source():
    historical = subprocess.run(['git', 'show', I.HARVEST_COMMIT + ':tools/mathlab_harvest.py'],
                                cwd=ROOT, capture_output=True, timeout=5, check=True).stdout
    G.require(hashlib.sha256(historical).hexdigest() == I.HARVEST_SHA, 'historical harvest source SHA mismatch')


def verify_launch(scope_sha, source_sha):
    G.verify_file(Path(__file__), source_sha)
    G.verify_file(SCOPE, scope_sha)
    I.verify_pins(ROOT, SOURCE_PINS)
    verify_historical_source()
    G.require(Path(LLMDB_ROOT).resolve() == ROOT, 'LLMDB_ROOT must equal this worktree')
    G.require(os.environ.get('LLMDB_DEVICE') == 'cpu' and os.environ.get('CUDA_VISIBLE_DEVICES') == '',
              'CPU environment required')
    G.require(all(os.environ.get(k) == str(I.THREADS) for k in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS')),
              'eight OMP/MKL threads required')
    G.require(os.getpriority(os.PRIO_PROCESS, 0) == 10, 'nice 10 required')
    I.verify_pins(ROOT, INPUT_PINS)


def tensor_facts(value):
    return {'sha256': G.tensor_sha(value), 'shape': list(value.shape), 'dtype': str(value.dtype),
            'device': str(value.device), 'stride': list(value.stride()),
            'storage_offset': value.storage_offset(), 'storage_bytes': value.untyped_storage().nbytes()}


def same_storage(left, right):
    # Storage identity distinguishes separate empty allocations whose data pointers are both zero.
    return left.untyped_storage()._cdata == right.untyped_storage()._cdata


def capture_arguments(d, expected_allowed, expected_sha, probes):
    torch = G.torch_module()
    G.require(type(expected_allowed) is int and 0 <= expected_allowed <= d, 'captured count invalid')
    G.require(isinstance(expected_sha, str) and re.fullmatch('[0-9a-f]{64}', expected_sha), 'captured SHA invalid')
    G.require(len(probes) == 4, 'four captured probes required')
    for probe in probes:
        G.require(isinstance(probe, torch.Tensor) and probe.dtype == torch.float32 and probe.shape == (d,),
                  'captured probe dtype/shape invalid')
        G.finite(probe)
        G.require(float(probe.double().norm()) > 0, 'captured probe has zero norm')


def capture_metadata(bundle, d):
    torch = G.torch_module()
    needed = ['l4.Pi_null_n', 'l4.Pi_sha256', *[f'l4.Pi_probe{j}' for j in range(4)]]
    G.require(isinstance(bundle, dict) and all(key in bundle for key in needed), 'missing L4 capture metadata')
    count, digest = bundle['l4.Pi_null_n'], bundle['l4.Pi_sha256']
    G.require(isinstance(count, torch.Tensor) and count.dtype == torch.int64 and count.shape == () and
              count.device.type == 'cpu', 'captured count metadata invalid')
    G.require(isinstance(digest, torch.Tensor) and digest.dtype == torch.uint8 and digest.shape == (32,) and
              digest.device.type == 'cpu', 'captured SHA metadata invalid')
    probes = [bundle[f'l4.Pi_probe{j}'].clone() for j in range(4)]
    expected_allowed, expected_sha = int(count), bytes(digest.tolist()).hex()
    capture_arguments(d, expected_allowed, expected_sha, probes)
    return expected_allowed, expected_sha, probes


def decompose(C, expected_allowed, expected_sha, probes):
    torch = G.torch_module()
    G.require(C.dtype == torch.float32 and C.ndim == 2 and C.shape[0] == C.shape[1] and len(C) > 0,
              'native fp32 square covariance required')
    G.finite(C)
    capture_arguments(len(C), expected_allowed, expected_sha, probes)
    facts = tensor_facts(C)
    U, s, Vh = torch.linalg.svd(C, full_matrices=False)
    G.finite(U); G.finite(s)
    del Vh
    return U, s, facts


def native_signature(U, s, mask, idx, index_list):
    return {'U': tensor_facts(U), 's': tensor_facts(s), 'mask': tensor_facts(mask),
            'indices_long': tensor_facts(idx), 'indices_list_count': len(index_list),
            'indices_list_sha256': hashlib.sha256(json.dumps(index_list, separators=(',', ':')).encode()).hexdigest()}


def projector_report(U, index, style, expected_allowed, expected_sha, probes, excluded):
    torch = G.torch_module()
    left = U[:, index]
    right = left.T if style == 'shared' else U[:, index].T
    P = left @ right
    actual_allowed = len(index)
    gate = G.projector_matches(P, actual_allowed, expected_allowed, expected_sha, probes)
    digest = G.tensor_sha(P)
    metrics = [{'seed': j, **I.probe_metrics(
        P @ torch.randn(P.shape[0], generator=torch.Generator().manual_seed(j)), reference)}
        for j, reference in enumerate(probes)]
    report = {'allowed_count': actual_allowed, 'excluded_count': excluded,
              'captured_allowed_count': expected_allowed, 'captured_excluded_count': len(U)-expected_allowed,
              'count_matches': actual_allowed == expected_allowed,
              'projector_sha256': digest, 'captured_projector_sha256': expected_sha,
              'projector_sha_matches': digest == expected_sha, 'matches_capture_gate': bool(gate),
              'probes': metrics, 'all_probes_match_1e6': all(p['match'] == 'MATCH' for p in metrics),
              'max_probe_relative_error': max(p['relative_error'] for p in metrics),
              'left': tensor_facts(left), 'right': tensor_facts(right),
              'operands_share_storage': same_storage(left, right),
              'left_shares_U_storage': same_storage(left, U), 'right_shares_U_storage': same_storage(right, U),
              'right_equals_left_transpose_bytes': G.tensor_sha(left.T) == G.tensor_sha(right),
              'gather_count': 1 if style == 'shared' else 2}
    del P, left, right
    return report


def compare_native(U, s, covariance_facts, expected_allowed, expected_sha, probes):
    mask = s < .005
    idx = mask.nonzero(as_tuple=True)[0]
    index_list = idx.tolist()
    before = native_signature(U, s, mask, idx, index_list)
    excluded = int((s >= .005).sum())
    rows = []
    for name, index_kind, style in CONSTRUCTIONS:
        row = projector_report(U, index_list if index_kind == 'list' else idx, style,
                               expected_allowed, expected_sha, probes, excluded)
        rows.append({'construction': name, 'index_kind': index_kind, 'gather_style': style, **row})
    after = native_signature(U, s, mask, idx, index_list)
    G.require(before == after, 'native operands mutated during construction comparison')
    return {'normalized_covariance': covariance_facts, 'native_before': before, 'native_after': after,
            'captured_probe_sha256': [G.tensor_sha(probe) for probe in probes], 'constructions': rows}


def construction_reports(C, expected_allowed, expected_sha, probes):
    U, s, facts = decompose(C, expected_allowed, expected_sha, probes)
    return compare_native(U, s, facts, expected_allowed, expected_sha, probes)


def measure():
    import numpy as np
    torch = G.torch_module()
    torch.set_num_threads(I.THREADS)
    G.require(torch.get_num_threads() == I.THREADS, 'eight torch threads required')
    with ExitStack() as stack:
        bound = {p: stack.enter_context(G.bound_input(ROOT / p, sha)) for p, sha in INPUT_PINS.items()}
        manifest = S.strict_json(bound[MANIFEST].read_text())
        cache = manifest.get('covariances', {}).get('4', {})
        G.require(cache.get('path') == CACHE and cache.get('sha256') == INPUT_PINS[CACHE],
                  'manifest L4 cache identity mismatch')
        bundle = torch.load(bound[CAPTURE], map_location='cpu', weights_only=True, mmap=True)
        expected_allowed, expected_sha, probes = capture_metadata(bundle, DIMENSION)
        del bundle
        C = G.load_covariance(bound[CACHE])
        G.require(C.shape == (DIMENSION, DIMENSION), 'L4 covariance dimensions changed')
        U, s, facts = decompose(C, expected_allowed, expected_sha, probes)
        del C
        report = compare_native(U, s, facts, expected_allowed, expected_sha, probes)
        del U, s, probes
    return {'status': 'MEASURED', 'purpose': 'construction diagnostic only; no prediction verdict',
            'layer': 4, **report, 'input_pins': INPUT_PINS, 'source_pins': SOURCE_PINS,
            'provenance': {'torch_version': torch.__version__, 'numpy_version': np.__version__,
                'get_num_threads': torch.get_num_threads(), 'backend': torch.__config__.show(),
                'device': 'cpu', 'dtype': 'float32', 'svd_driver': 'CPU default, full_matrices=False',
                'nice': os.getpriority(os.PRIO_PROCESS, 0), 'captured_threads': 'UNKNOWN',
                'captured_torch_version': manifest.get('torch_version'),
                'historical_harvest_commit': I.HARVEST_COMMIT, 'historical_harvest_sha256': I.HARVEST_SHA},
            'limitations': 'Four probes are sampled discrepancies, not full subspace distance or behavioral evidence; '
                           'the original worker float64/check interval and allocation history are untested.'}


def new_directory(base):
    base = Path(base)
    base.mkdir(parents=True, exist_ok=True)
    directory = base / ('construction_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'))
    directory.mkdir()
    return directory


def launch_command(scope_sha, source_sha):
    for digest in (scope_sha, source_sha):
        G.require(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest), 'launch SHA invalid')
    probe = ('import os,sys;current=os.getpriority(os.PRIO_PROCESS,0);'
             'sys.exit("starting niceness exceeds 10") if current>10 else None;print(10-current)')
    return ('new1_nice_increment=$(LLMDB_ROOT="$PWD" .venv/bin/python -B -c ' + shlex.quote(probe) +
            ') || exit "$?"\n'
            'LLMDB_ROOT="$PWD" LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES=\'\' OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 '
            'PYTHONDONTWRITEBYTECODE=1 /usr/bin/nice -n "$new1_nice_increment" .venv/bin/python -B '
            'tools/new1_construction_diag.py --scope-sha ' + scope_sha + ' --source-sha ' + source_sha)


def main(argv=None):
    start = time.monotonic()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope-sha', required=True)
    parser.add_argument('--source-sha', required=True)
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        if args.worker:
            G.require(os.environ.get('NEW1_IDENTITY_PARENT') == str(os.getppid()),
                      'only the diagnostic parent may dispatch')
            I.wait_for_release()
            verify_launch(args.scope_sha, args.source_sha)
            value = measure()
            value.update(scope_sha256=args.scope_sha, diagnostic_source_sha256=args.source_sha)
            data = json.dumps(value, allow_nan=False)
            G.require(len(data.encode()) < I.DISK_BYTES // 2, 'worker scalar report too large')
            print(data)
            return 0
        with S.hard_deadline(start+I.DEADLINE_S-time.monotonic()):
            G.verify_file(Path(__file__), args.source_sha)
            directory = new_directory(ROOT / 'results/mathlab_staging/new1_construction_diag')
        command = [sys.executable, '-B', str(Path(__file__).resolve()), '--worker',
                   '--scope-sha', args.scope_sha, '--source-sha', args.source_sha]
        status = I.supervise(command, directory, preflight=lambda: verify_launch(args.scope_sha, args.source_sha),
                             seconds=I.DEADLINE_S, absolute_end=start+I.DEADLINE_S)
        print(str(directory))
        return status
    except (S.Stop, G.Invalid, OSError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__': sys.exit(main())
