#!/usr/bin/env python3
"""UNRUN CPU resource timer for one preserved A7 layer; stdout only.

Times frozen pre-cast controls (b), (c), (d), and the CPU portion of (e).
The MPS repeat is explicitly NOT-MEASURED. No scientific reading or dispatch.
Run only after MAESTRO authorizes CPU contention; this file authorizes no run.
References: c10y_precast_diag.py controls and c10y_directdw_arms.py factor_solve.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent / "bulk/c10y_precast_diag/20261009T225619Z"
OFFLOAD = Path.home() / "Backups/memit_offload/c10y_precast_20261009T225619Z"
DEFAULT_STEM = "controls_A7_coined_coined_L4_control_inputs"
PACKET_NAME = re.compile(r"(?:controls_A7_coined_coined_L[4-8]_control_inputs|operands_A7_coined_coined_L[4-8]_A)")


def peak_rss_bytes():
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(rss if sys.platform == "darwin" else rss * 1024)


def emit(phase, seconds, **fields):
    rss = peak_rss_bytes()
    print(json.dumps({"phase": phase, "seconds": seconds,
                      "peak_rss_bytes": rss, "peak_rss_gib": rss / 2**30,
                      "peak_rss_scope": "process-lifetime high-water", **fields}), flush=True)


def packet_paths(argument):
    if argument is None:
        candidates = [directory / (DEFAULT_STEM + ".pt") for directory in (RUN, OFFLOAD)]
        packet = next((p for p in candidates if p.is_file()), None)
        if packet is None:
            raise FileNotFoundError("Pass a preserved A7 layer .pt or .json path; default packet not found")
    else:
        packet = Path(argument).expanduser().resolve()
    if packet.suffix not in (".pt", ".json") or not PACKET_NAME.fullmatch(packet.stem):
        raise ValueError("Expected an A7 recipe-A operands or control_inputs layer packet")
    if packet.suffix == ".json":
        metadata = packet
        candidates = [packet.with_suffix(".pt"), OFFLOAD / (packet.stem + ".pt"), RUN / (packet.stem + ".pt")]
        sidecar = next((p for p in candidates if p.is_file()), None)
    else:
        sidecar = packet
        candidates = [packet.with_suffix(".json"), RUN / (packet.stem + ".json"), OFFLOAD / (packet.stem + ".json")]
        metadata = next((p for p in candidates if p.is_file()), None)
    if sidecar is None or metadata is None or not sidecar.is_file() or not metadata.is_file():
        raise FileNotFoundError("Both the packet and matching JSON metadata are required")
    return sidecar, metadata


def load_inputs(sidecar, metadata, torch):
    meta = json.loads(metadata.read_text())
    expected = meta.get("artifacts", {}).get(sidecar.name)
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ValueError("Missing packet SHA-256 binding in metadata")
    with sidecar.open("rb") as handle:
        observed = hashlib.file_digest(handle, "sha256").hexdigest()
        if observed != expected:
            raise ValueError("Packet SHA-256 differs from preserved metadata")
        handle.seek(0)
        before = os.fstat(handle.fileno())
        stored = torch.load(handle, map_location="cpu", weights_only=True)
        after = os.fstat(handle.fileno())
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise ValueError("Packet changed while being loaded")
    packet = {}
    for name in ("K32", "R", "P", "C", "M", "Q", "B", "X"):
        ref = meta.get(name)
        if name == "X" and ref is None:
            continue
        if not isinstance(ref, dict) or ref.get("tensor_artifact") != sidecar.name:
            raise ValueError("Missing or cross-packet tensor: " + name)
        value = stored[ref["key"]]
        if (not isinstance(value, torch.Tensor) or value.device.type != "cpu"
                or str(value.dtype) != ref["dtype"] or list(value.shape) != ref["shape"]
                or value.dtype != torch.float32 or not bool(torch.isfinite(value).all())):
            raise ValueError("Invalid CPU-fp32 tensor metadata/value: " + name)
        packet[name] = value
    packet["L2"] = float(meta["L2"])
    if not math.isfinite(packet["L2"]):
        raise ValueError("Nonfinite L2")
    n, count = packet["K32"].shape
    out, residual_count = packet["R"].shape
    if (n, count, out, residual_count) != (11008, 24, 2048, 24):
        raise ValueError("Packet is not the preserved full-size 24-request A7 layer")
    for name, shape in {"P": (n, n), "C": (n, n), "M": (n, n),
                        "Q": (n, count), "B": (n, out), "X": (n, count)}.items():
        if name in packet and tuple(packet[name].shape) != shape:
            raise ValueError("Invalid shape for " + name)
    return packet, expected


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", nargs="?", help="A7 recipe-A/control_inputs .pt or .json, including an offloaded path")
    parser.add_argument("--threads", type=int, help="Explicit CPU thread count; otherwise retain PyTorch defaults")
    args = parser.parse_args(argv)
    if args.threads is not None and args.threads < 1:
        parser.error("--threads must be positive")
    sidecar, metadata = packet_paths(args.packet)
    started = time.perf_counter()
    import torch  # Deliberately no driver, harness, tokenizer or model import.
    if args.threads is not None:
        torch.set_num_threads(args.threads)
    with torch.no_grad():
        packet, digest = load_inputs(sidecar, metadata, torch)
        emit("load_hash_and_validate", time.perf_counter() - started,
             packet=str(sidecar), metadata=str(metadata), packet_sha256=digest,
             torch_version=torch.__version__, threads=torch.get_num_threads(), device="cpu")
        k, r, p, c = (packet[name] for name in ("K32", "R", "P", "C"))
        m, q, b = (packet[name] for name in ("M", "Q", "B"))
        l2, n = packet["L2"], k.shape[0]
        totals = {}

        def timed(name, operation):
            start = time.perf_counter()
            value = operation()
            elapsed = time.perf_counter() - start
            totals[name] = elapsed
            emit(name, elapsed, status="MEASURED_CPU", output_shapes=[list(x.shape) for x in value])
            del value

        def factor32():
            # Same assembly/solve as the frozen factor_solve, without importing it.
            matrix = p @ (k @ k.T + c) + l2 * torch.eye(n, dtype=torch.float32, device="cpu")
            return torch.linalg.solve(matrix, p @ k)

        if "X" in packet:
            x = packet["X"]
            emit("common_factor32_preparation", 0.0, status="ALREADY_PERSISTED", included_in_core=False)
        else:
            start = time.perf_counter()
            x = factor32()
            totals["common_factor32_preparation"] = time.perf_counter() - start
            emit("common_factor32_preparation", totals["common_factor32_preparation"], status="MEASURED_CPU")

        def control_b():
            return (r.double() @ x.double().T,)

        def control_c():
            k64, r64, p64, c64 = k.double(), r.double(), p.double(), c.double()
            matrix = p64 @ (k64 @ k64.T + c64) + l2 * torch.eye(n, dtype=torch.float64, device="cpu")
            rhs_q = p64 @ k64
            rhs_b = rhs_q @ r64.T
            direct = torch.linalg.solve(matrix, rhs_b)
            factor = torch.linalg.solve(matrix, rhs_q)
            return direct.T, r64 @ factor.T

        def control_d():
            matrix = m.double()
            direct = torch.linalg.solve(matrix, b.double())
            factor = torch.linalg.solve(matrix, q.double())
            return direct.T, r.double() @ factor.T

        def control_e_cpu():
            direct_repeat = torch.linalg.solve(m, b)
            factor_repeat = factor32()
            return direct_repeat.T, r @ factor_repeat.T, r @ x.T

        for name, operation in (("b_promoted_fp32_factors_product64", control_b),
                                ("c_promote_before_assembly_solve64_products", control_c),
                                ("d_saved_assembled32_systems_solve64_products", control_d),
                                ("e_exact_input_cpu_repeats", control_e_cpu)):
            timed(name, operation)
        emit("e_mps_product_repeat", None, status="NOT_MEASURED_CPU_ONLY")
        emit("summary", sum(totals.values()), status="CPU_CORE_ONLY",
             measured_cpu_core_s=sum(v for key, v in totals.items() if key != "common_factor32_preparation"),
             estimated_five_layer_cpu_core_s=5 * sum(v for key, v in totals.items() if key != "common_factor32_preparation"),
             five_layer_value_is_extrapolation=True, whole_arm_C_ctrl="UNMEASURED",
             omitted=["MPS products/repeats", "realizations", "all-pair/column statistics",
                      "conditioning/residuals", "durable output writes and gate evaluation"],
             scientific_reading="NOT_PERFORMED", source_files_written=False)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        emit("error", None, status="ERROR", error_type=type(error).__name__, detail=str(error))
        raise
