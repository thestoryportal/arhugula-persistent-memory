FIX-FIRST

**BLOCKING**

1. **Benchmark omits `torch.no_grad()`.** `benchmark_spec.md:68–71` specifies forwards without it; the driver uses it at `arms:553`, `:593`, `:483`. `.eval()` does not disable autograd. **Fix:** wrap warm-up and timed probe/batch forwards in `torch.no_grad()`; assert gradients are disabled in the stub tests. Append each generated token exactly as `arms:557` does. Otherwise this does not time the same computation.

2. **The proposed deadline transition still has a gap.** `proposal_v2.md:98` removes stage01 before installing stage2; `arms:109` samples a new clock afterward. An in-memory implementation accepted check-time **7,199**, entry-time **7,201**, with C01 **7,200**, and exposed `deadline() == None` during transition. **Fix:** use one captured entry timestamp, validate it against stage01, and install stage2 before removing stage01, with synchronized deadline-state access. Update the early-removal stub at `selftest:1286`.

   Actual model-free probes: **(i)–(iii) fail today; (iv) already passes.** For every stipulated `e<C01`, `e+C2<C01+C2+60`, even on today’s code. Keep (iv) as an invariant test; add clock-crossing and transition-interleaving regressions.

3. **The claimed hard worst case is not established.** `arms:1410–1423` performs heartbeat I/O before checking expiry, then acquires `publication_lock` and writes diagnostics before exiting. The 0.1-second wait is not an upper bound on watchdog latency. **Fix:** either provide independently enforced termination that cannot wait on these writes, or explicitly describe nominal deadlines with unbounded/unmeasured termination overrun.

   With a correct transition, the tighter nominal two-process supremum is **2·(C01+C2)**; adding 60 seconds is conservative slack, not the attained maximum. `proposal_v2.md:146` must consequently withdraw “never more than” and replace “can no longer sit idle” with “idle waiting counts against the first-phase deadline.”

4. **The statistical guarantee is false.** `proposal_v2.md:55` says p95 exceeds the mean for every right-skewed distribution. Counterexample: **99 samples of 1 and one of 10,000 → p95=1, mean=100.99**. The 1.25 multiplier likewise proves no coverage of hours-long slowdowns. **Fix:** call this a prospective sizing heuristic; include the measured mean in `max(p95, mean, eval_s/1392)` and retain the explicit possibility of HALTED-BUDGET.

5. **Formula and fallback contradict their stated basis.** `proposal_v2.md:66` lacks the advertised 7,200 floor: **t*=0.030 gives C01=6,900**. All six displayed table rows do reproduce. **Fix:** specify `max(7200, R(...))` or withdraw the range/floor claims.

   `:123` also treats raw anchor **t=0.117** as already safety-adjusted **t***. Applying 1.25 gives **t*=0.14625**, hence **10,800 / 16,800 / 27,660** at minimum overhead. Keep **9,600 / 14,400 / 24,060** only as explicitly discretionary fallback caps, without claiming they satisfy the same safety-adjusted formula. Add a fallback-specific amendment text; `:138` currently requires a nonexistent benchmark artifact.

6. **CAPPED measurements can silently become smaller fallback budgets.** `benchmark_spec.md:56` falls back for every non-COMPLETE record, while `:70`, `:116` accept CAPPED as usable. This discards measured slowness and can bypass STOP. **Fix:** derive from both COMPLETE and usable CAPPED records; INVALID/incomplete mandatory evidence must refuse derivation. Fallback requires the explicitly chosen no-benchmark path. Set final status before computing `derived` (`:75`).

7. **The benchmark lifecycle cannot guarantee its acceptance contract.** `benchmark_spec.md:62` starts the watchdog only after preflight; `:64` permits skipping the before-hash phase, while `:73` requires comparison against it. Optional work can consume the reserve needed for verification. **Fix:** start supervision before potentially blocking preflight, make before/after hashes mandatory for usable results, reserve their completion time, and leave interrupted runs unusable. A fake-clock exit test does not establish a hard 600-second process bound.

**ADVISORY**

- Prior dispositions: **Astra-1, Astra-4a/4b and advisor-B2 are resolved in the proposal’s intended flow**. Astra-2 remains unresolved; Astra-3/advisor-B1 are only partially resolved because of the benchmark and sizing defects above.
- Probe population construction, forward-count ranges, stage-2 timing window, model/dtype and synchronization mechanism match the cited code. Batched observation and synthetic SVD timings remain proxies; their overhead multipliers are unmeasured.
- `proposal_v2.md:173–175` treats missing/unexpected `next_stage` as successful termination. Validate the reading and accept only explicit `null` or integer `2`; malformed state should exit nonzero.
- §F’s write-qualification caveats match `prereg:343`. Say “allowed up to three hours,” not “needs … at most three”; completion remains unproven.
- Read-only, model-free probes completed. No GPU/model execution or full selftest run.

🌱 graft saved ~80,574 tokens (~$0.05), 1 successful call.