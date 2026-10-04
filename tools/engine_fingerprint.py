#!/usr/bin/env python3
"""LAW#1 engine fingerprint gate for the vendored MEMIT engine.

Exit 0 when the science-path file matches the recorded state; exit 1 with a
diff-ready message otherwise. Run before any dispatch:

    python3 tools/engine_fingerprint.py

[LAW:single-enforcer] the expected hash lives here and nowhere else; prose
elsewhere points at this script rather than restating the value.

Fingerprint history (memit/memit_main.py sha256):
  5c0c706a…c78770  P-1..P-7 + S2.31 CPU-solve. The RunPod 4090 era; every
                   result in CORPUS/ through 2026-06-27 ran under this hash.
  e6ac7e18…164b51  + P-8 device neutrality (D-HW-1, 2026-10-03): CUDA literals
                   replaced by the model's device; float64 operands moved to CPU
                   before the cast (MPS has no float64). Inertness: LAW#3
                   reproduction of CORPUS/20 (C2) and CORPUS/14 (A1) on the M3 Pro.
"""
from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

LLMDB_ROOT = Path(os.environ.get("LLMDB_ROOT") or Path(__file__).resolve().parents[1])
MEMIT_MAIN = LLMDB_ROOT / "memit_dry_run" / "memit" / "memit" / "memit_main.py"

EXPECTED_SHA256 = "e6ac7e186ee4ea5834f1127ce6f4031eef21fc52c8effa474876b80bda164b51"
POD_ERA_SHA256 = "5c0c706a66c385273d0a48ebbb8274a1c31bf3e101ca309e47db9cb8b6c78770"
EXPECTED_COV_CPU_SITES = 3


def main() -> int:
    source = MEMIT_MAIN.read_bytes()
    actual_sha = hashlib.sha256(source).hexdigest()
    actual_sites = source.count(b"_cov_cpu")
    ok = actual_sha == EXPECTED_SHA256 and actual_sites == EXPECTED_COV_CPU_SITES
    status = "PASS" if ok else "FAIL"
    print(f"engine fingerprint {status}: {MEMIT_MAIN}")
    print(f"  sha256   {actual_sha}  (expected {EXPECTED_SHA256}; pod-era {POD_ERA_SHA256[:8]}…)")
    print(f"  _cov_cpu {actual_sites}  (expected {EXPECTED_COV_CPU_SITES})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
