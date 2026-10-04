#!/usr/bin/env python3
"""LAW#1 engine fingerprint gate for the vendored MEMIT engine.

Exit 0 when the science-path file matches the recorded UNMODIFIED state;
exit 1 with a diff-ready message otherwise. Run before any dispatch:

    python3 tools/engine_fingerprint.py

[LAW:single-enforcer] the expected hash lives here and nowhere else; prose
elsewhere points at this script rather than restating the value.
"""
from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

LLMDB_ROOT = Path(os.environ.get("LLMDB_ROOT", Path(__file__).resolve().parents[1]))
MEMIT_MAIN = LLMDB_ROOT / "memit_dry_run" / "memit" / "memit" / "memit_main.py"

# memit_main.py after P-1..P-7 + the S2.31 CPU-solve patch (3 `_cov_cpu` sites).
EXPECTED_SHA256 = "5c0c706a66c385273d0a48ebbb8274a1c31bf3e101ca309e47db9cb8b6c78770"
EXPECTED_COV_CPU_SITES = 3


def main() -> int:
    source = MEMIT_MAIN.read_bytes()
    actual_sha = hashlib.sha256(source).hexdigest()
    actual_sites = source.count(b"_cov_cpu")
    ok = actual_sha == EXPECTED_SHA256 and actual_sites == EXPECTED_COV_CPU_SITES
    status = "PASS" if ok else "FAIL"
    print(f"engine fingerprint {status}: {MEMIT_MAIN}")
    print(f"  sha256   {actual_sha}  (expected {EXPECTED_SHA256})")
    print(f"  _cov_cpu {actual_sites}  (expected {EXPECTED_COV_CPU_SITES})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
