"""P-8 (2026-10-03, D-HW-1) — device neutrality for the science path.

The engine was written against a CUDA literal. On the M3 Pro the model lives on MPS and
the float64 solve on CPU (MPS has no float64). This module is the single place the
accelerator is named; engine and harness both import it.

[LAW:one-source-of-truth] one resolver, one cache-release table.
[LAW:dataflow-not-control-flow] backend differences are table lookups, not branches.
"""
import os
import torch

# Ordered by preference; the first available accelerator wins. "cpu" always exists.
_PROBES = (("cuda", torch.cuda.is_available), ("mps", torch.backends.mps.is_available))
_RELEASE = {"cuda": torch.cuda.empty_cache, "mps": torch.mps.empty_cache, "cpu": lambda: None}


def resolve_device() -> torch.device:
    """Harness entry point: LLMDB_DEVICE overrides; otherwise first available accelerator."""
    forced = os.environ.get("LLMDB_DEVICE")
    picked = forced or next((name for name, ok in _PROBES if ok()), "cpu")
    return torch.device(picked)


def device_of(model) -> torch.device:
    """Engine entry point: the model already knows where it lives."""
    return next(model.parameters()).device


def empty_cache(device) -> None:
    """Release the accelerator's cached allocations; a no-op on CPU."""
    _RELEASE[torch.device(device).type]()
