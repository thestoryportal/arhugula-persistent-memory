FIX-FIRST

Reviewer: GPT-6-Astra (high)

**BLOCKING**

- **B1 — 300-second wait can admit late.** `tools/new1_supervisor.py:206–217` checks memory before wait expiry. Synthetic reproduction admitted SVD at **301 s**. **Fix:** enforce an absolute cell deadline across probes and persistence; recheck before granting admission. Add a late-success regression.
- **B2 — failed closeout retains prediction verdicts.** `tools/new1_supervisor.py:343–365` publishes predictions before finding persistence completes. Injected `finding.json` failure produced **HALTED with all four PASS/FAIL gates still exposed by `fold()`**, violating §6’s no-verdict rule. **Fix:** make verdict visibility conditional on durable successful terminal completion and absence of a halt; treat earlier outcomes as provisional. Test I/O failure and deadline expiry throughout publication.
- **B3 — missing registered contrasts.** `tools/new1_geometry.py:370–386` records fractions but omits §3’s explicit per-layer **top/bottom D−M differences**. **Fix:** persist both differences with their respective bin-validity flags; assert their values in the synthetic layer test.

**ADVISORY**

- **56/56 supplied tests passed** in 2.562 s; they are non-vacuous but miss B1/B2. No real geometry ran.
- Reviewed admission, resource thresholds, family accounting, CPU execution, fixed statistics and primary/secondary separation otherwise match the frozen contract. All **20 declared pins** match the prereg; production payloads were not revalidated.
- Recorded launch command’s arguments, prereg SHA and installed runtime versions match. Actual admission and full-workload feasibility remain **UNVERIFIED**.
- `tools/new1_geometry.py:111` repeatedly promotes the entire covariance basis to float64. Convert selected ≤256-column blocks instead to reduce allocation pressure.

🌱 graft reported ~237,391 tokens saved (~$0.12), 1 successful call.

