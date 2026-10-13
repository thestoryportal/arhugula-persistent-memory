# D-ML-2 implementation review

Reviewer: existing GPT-6-Astra (high) review agent `/root/mathlab_build_review`, 2026-10-09. Read-only review of §14, live source, pre-edit snapshots, and RED/GREEN evidence.

**GO — D-ML-2 implementation conforms to frozen §14. No blocking code findings.**

- Step 2 is 6,540 seconds in the shell cases (`tools/run_mathlab_cpu.sh:13`), validator (`tools/mathlab_cpu_runner.py:17`), and notebook boundary (`mathlab/core.py:385`). Step 3 remains 1,800; index remains 300. Remaining 2,700 occurrences in the reviewed files are explicit rejection tests.
- `SVD_RESERVE_GIB=5` and `SOLVE_RESERVE_GIB=9` are applied before their respective operations (`mathlab/core.py:16–17,240,252,270`). Scientific arithmetic is unchanged.
- The verified prereg SHA matches `4852d1a229e186c1d054c6f1849f3c130f333738aa9dfc297bedac8cd44ad507`; exact-byte enforcement remains intact (`tools/mathlab_runtime.py:48–49`).
- Reviewed evidence establishes RED → GREEN for the amended contracts; targeted tests pass and the recorded full suite reports **62 tests, OK**. Tests exercise shell admission boundaries, validator limits, actual notebook stage cap, SVD/solve reserve calls, and hash tamper rejection.

The completed full-shape probes and newer UV fixture closeouts support isolated-cell and fixture acceptance. Their documented limitations remain: live admission/watchdog/niceness, production-data completion within 6,540 seconds, and scientific validity are **UNVERIFIED**. The report append was still pending at this review.
