**FIX-FIRST.** The budget formula, approved bounds and write-qualification ruling are faithfully carried into §9. The launch-input approach is reasonable, but its provenance checks and telemetry guarantees need correction before building.

I verified both hashes: the first **105,436 bytes** retain `38f8b68c…b072`; the amended file hashes to `e2d7fa10…eca50`. References below use paths relative to W; the supplied brief is cited by section because it has no supplied file location.

**BLOCKING — exact fixes**

1. **Telemetry’s unchanged-reading guarantee conflicts with the frozen timing gates.**

   §9(h) charges telemetry against deadlines while promising that no label or reading can differ (`docs/C10Z_ASTRA_PREREG.md:475–476`). But the proposed placement remains inside the per-write wall-clock interval: it begins at `c10z_astra_arms.py:706`, includes `arm_hook`, and ends after restoration at `:692–695`. The reader adds `EXCEEDS-TTL` above 3,600 seconds and changes continuation eligibility (`c10z_astra_read.py:571–576`).

   Consequently, an otherwise identical write taking 3,599 seconds can cross W2 with telemetry enabled. Deadline expiration and later projections can also change. Placing telemetry after `round_guard` protects that round’s recorded interval; it does **not** protect W2 or attempt deadlines.

   **Fix:** revise §9(h) before implementation to distinguish:
   - numerical/state noninterference under controlled, identical timing;
   - actual elapsed-time and resource effects, which remain subject to unchanged W2/V11/V13 gates.

   Explicitly state that timing-induced qualifier/HALT differences invalidate an *identical-reading* claim. Do not subtract telemetry time from W2 or deadlines. If unchanged readings under real execution remain an absolute requirement, the proposed inline telemetry cannot satisfy it.

2. **The new reader range check loses the old exact-ceiling invariant.**

   The existing `==5400.` verifies one specific C01 (`c10z_astra_read.py:499–505`). An interval check would accept, for example, a pass recording **10,800** when its launch selected **7,200**. `read_directory` currently checks attempt/PID and artifact bindings, but never compares launch ceilings with pass ceilings (`:662–688`). Process-pair validation likewise lacks ceiling equality (`:649–656`).

   This also departs from v3’s explicit `==C01` requirement (`results/c10z_astra_budget_proposal_v3.md:161–165`).

   **Fix:** retain the range check **and** require exact equality to the benchmark-bound launch C01. Bind the selected benchmark identity and computed ceilings into immutable attempt provenance; validate:
   - pass ceilings against launch/provenance;
   - projection-history ceilings against the same values;
   - identical selected ceilings across processes;
   - `None` expansion ceilings only where that expansion was not authorized.

   Add reader tests for **in-range mismatches**, not just out-of-range numbers.

3. **Recomputation plus a newly recorded hash does not authenticate the selected benchmark.**

   §9(b) records the benchmark hash at launch (`docs/C10Z_ASTRA_PREREG.md:455`). Brief §2B compares derived values and the benchmark script SHA, but neither binds the record to the digest selected before the go record. Today’s go validation checks decision fields and approval booleans only (`c10z_astra_arms.py:1342–1361`).

   A substituted record with altered measurements, matching recomputed `derived`, and the current script SHA can therefore pass the proposed checks. Script identity alone also misses changes to reused driver helpers: the benchmark explicitly depends on those helpers (`results/c10z_astra_benchmark_spec_v2.md:17–29`).

   **Fix:** put the selected benchmark digest, script/source identity and computed ceilings into the go record, matching the ledger selection. Stage 0 must:
   - read bytes once, hash and parse those same bytes;
   - compare against that prior selection;
   - validate mandatory evidence and measurement consistency;
   - validate identities of the reused timing/population code and relevant environment.

   Carry that binding through resident/process-2 admission before writes or model import. Add substitution, helper-drift and changed-record tests. An older benchmark need not be rejected merely for age; define staleness through the approved identity/compatibility contract.

4. **The required idle-fix RED evidence is underspecified, and the concurrency assertion cannot prove locking.**

   v3 test (vi) claims today’s `enter()` performs discard-before-add, but today’s removal is in `Session.stage1` (`c10z_astra_arms.py:1259`); `enter()` only installs/adds (`:106–110`). The specified sampling “during `enter(2)`” can miss the original gap.

   I ran small model-free probes against today’s code:
   - literal fresh-Budget mutation sampling returned `[5400.0]`, with no `None`;
   - the literal 1,000-transition stress probe observed neither `None` nor `KeyError`.

   These are counterexamples to guaranteed RED under those literal interpretations, not a test of the complete proposed harness. Furthermore, after install-before-remove is implemented, removing `deadline()`’s lock can still satisfy “no `None`/`KeyError`”; M3 needs a lock-specific assertion (`results/c10z_astra_budget_proposal_v3.md:132–141`).

   **Fix:** specify the schedule explicitly:
   - drive real `Session.stage1`;
   - observe its return and the idle interval before entry;
   - sample both mutations across the complete handoff;
   - add an event/barrier-controlled test proving `deadline()` cannot complete while another thread holds the transition lock.

   Define a baseline adapter for the old Budget signature/C01 so failures demonstrate the intended defect rather than a constructor error or premature projection failure. Require named assertion failures, not merely a nonzero suite exit.

5. **The on/off proof is insufficient for the extra model forwards.**

   No-grad and no new hooks are useful restrictions, but input-tensor hashes and science-forward counts do not establish unchanged RNG, buffers, model mode, allocator state or subsequent outputs. Existing scientific records include actual RSS and MPS allocation measurements (`c10z_astra_arms.py:390–394`), so “only timing fields differ” is also too strong.

   The stub-only proof in §9(h) establishes plumbing, not live LAW#5 inertness (`docs/C10Z_ASTRA_PREREG.md:474–476`).

   **Fix:** extend CPU tests to check model parameters/buffers, RNG state, mode, hook registry and subsequent science outputs across telemetry calls. Keep the **entire** logit-lens calculation—including norm/head—under no-grad. Label live numerical/resource inertness **UNVERIFIED**, with a controlled on/off validation required before telemetry-enabled scientific use. That future validation is outside this no-model build.

**Advisories and brief corrections**

- **A — amendment fidelity:** §9(a)–(g) correctly preserves the formula, `[7,200,10,800]` bounds, 55,800-second nominal total, no-fallback choice, idle-time transition and limited write-qualification ruling. These agree with `results/c10z_astra_budget_proposal_v3.md:65–81`, `:175–203`, and `EXPERIMENT_RUNBOOK.md:364–365`. The override precedence is explicit at prereg `:451`; the substantive contradiction is telemetry’s guarantee, identified above.

- **B — launch-input design:** prefer a bound launch input over editing reviewed code after benchmarking. With blockers 2–3 fixed, it can preserve exact selected-ceiling enforcement. Bounds alone cannot.

- **C — logit-lens indexing:** explicitly prescribe `hidden_states[l+1][:,-1,:]` for band layers 4–8. Installed Qwen2 saves the residual **before** each decoder layer, then appends the final normalized state (`.venv/lib/python3.11/site-packages/transformers/models/qwen2/modeling_qwen2.py:532–570`; use the actual installed version-directory path). Add a distinguishable-layer stub test, plus top-5 ID/text/probability assertions.

- **D — test-first coverage:** the brief clearly requires test-list-first, RED/GREEN, round trips, refusal tests and mutation checks. Its enumerated boundary cases do not consistently include both interior neighbours. Expand the matrix explicitly. Also isolate each gate so another rejection cannot mask its removal.

  In particular, with the stated formula and minima, valid `C01≤10,800` already implies `C2≤17,100`, hence total ≤55,800 (`budget_proposal_v3.md:65–81`). **M7 therefore needs an injected derived-ceiling result to exercise the independent total validator**; an ordinary formula-valid fixture cannot exceed that total while passing C01.

- **D — literal instruction conflicts:** add an explicit precedence exception for replacing v3’s `==C01` implementation with the corrected provenance-bound design. Clarify that the benchmark may call the approved read-only population/batch helpers; spec v2 requires them (`benchmark_spec_v2.md:17–29`). Scope “never `cd`” to build commands, since the required verbatim wrapper contains `cd` (`budget_proposal_v3.md:226`). Reconcile the mandated interpreter/`-B` convention with the wrapper’s `-I` invocation at `:232` and brief §3.5’s `python3`.

- **D — scope:** the write allowlist and C10U/V/W, engine, prereg, tracker and git exclusions are tight. `git status --short` alone cannot detect further changes to an already-modified file. Record content fingerprints/diffs as well, and attribute concurrent C10V changes without touching them. Mutation restoration should execute in `finally`.

- **D — telemetry test details:** T2 must exclude telemetry files from the on/off file-set comparison and control nondeterministic identities/timestamps. Test writer initialization, append, flush and fsync failures separately. Define how round-start markers coexist with the “all calls after `round_guard`” placement rule.

**E — before build:** resolve blockers 1–5 in the amendment/brief, then build against the corrected contract. No additional operator budget authorization is needed for the already-approved bounds.

Review evidence consists of source inspection, hash verification and small standard-library/model-free probes. No files were edited, no full suites were run, and no model/GPU or live telemetry behavior was tested.

