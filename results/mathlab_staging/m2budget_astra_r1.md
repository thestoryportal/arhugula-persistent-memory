FIX-FIRST

Reviewer: GPT-6-Astra (high)

**BLOCKING**

1. **The workload counts are correct; the timing model is incomplete.** [core.py:230](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/mathlab/core.py:230) confirms 5 projector calls, 35 complete `solve()` calls, 36 harvest loads (**1 clean + 30 in-loop + 5 weights**) and 5 covariance loads. Each solve includes fp32/fp64 solves **and conditioning**, so those diagnostics are counted. Hashing, comparisons and persistence lack explicit accounting.

   Replace §14’s arithmetic total and “48 %” forecast with:

   > Using the displayed timings without intermediate rounding: 394.75 + 5,114.55 + 72 + 25 + 30 = 5,636.30 s; ×1.15 = 6,481.745 s; ceiling to a whole minute = 6,540 s. This is a partial workload estimate. Additional untimed work includes file/tensor hashing, covariance decoding, 30 projector comparisons (up to 120 fallback matvecs), update norms/relative errors, five rounding comparisons, five approximation comparisons, and 30 update saves with hashes (2.52 GiB of update payload), plus event output and memory waits. These costs compete for the remaining allowance; their coverage is UNVERIFIED. The 6,540-s deadline is a provisional spending cap, not demonstrated completion feasibility. No reliable completed-solve percentage is established for the old deadline.

2. **Matching functions/shapes does not establish representative timing.** The [probe:20](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/verification_scripts/mathlab_peak_probe.py:20) uses **zero covariance**, identity P and random K/r. Zero-covariance SVD can substantially understate real-covariance decomposition time.

   Append after the single-sample caveat:

   > The probe uses the notebook’s actual projector and solve functions, torch 2.8.0, eight CPU threads, native fp32 operands and production dimensions; solve includes its fp64 diagnostics. Operand spectra, conditioning and cache/I/O state are not production-representative. The probe also does not reproduce the runner’s nice-10 scheduling. Shared-machine contention can change either way. The ×1.15 factor follows the C10Y pre-cast budgeting convention, not an empirically validated uncertainty margin. Neither ×1.15 nor a larger factor is established as sufficient by these records; production completion feasibility remains UNVERIFIED.

**ADVISORY**

- **Reserve:** 4→5 GiB follows §6’s raise rule: completed projector `ru_maxrss` is **4.60878 GiB**; solve is **8.08434 GiB**, below 9. No further numerical raise follows from these measurements. They do not establish whole-notebook peak memory. Original 30-second records remain incomplete lower bounds.
- **Timing consistency:** 78.95 s is supervisor elapsed; 146.13 s is worker elapsed. Worker projector time is 77.71 s; supervisor solve time is 146.84 s. Label the mixed basis or standardize it; either choice still rounds to 6,540 s.
- **Implementation coverage:** update the shell case table, `mathlab_cpu_runner.py:17`, `core.py:384`, SVD admission and tests; repin the amended prereg SHA without weakening verification. The frozen base hash matches.
- **Boundaries/authority:** science, gates, diagnostics and non-reinterpretation remain intact. Authority is correctly cited at `EXPERIMENT_RUNBOOK.md:386`; record D-ML-2 there before spending. C10Y establishes the rounding convention, not margin adequacy.

No probes rerun; no files changed.

🌱 graft: 1 failed call; savings unavailable.

