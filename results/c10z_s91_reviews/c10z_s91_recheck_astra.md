FIX-FIRST

The fold resolves the main budget, ceiling-provenance, deadline-transition and telemetry-timing defects. **It preserves D-C10z-budget’s approved bounds**, including the STOP rule; your four program-lead rulings are compatible with that approval. Four text/build-contract issues remain before implementation.

References below: **D** = [§9.1 draft](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_s91_draft.md), **B** = [brief v2](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/codex_c10z_build_brief_v2.md), **F** = [fold map](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_fold_map.md). **arms/read/selftest** denote `experiments/track_c/c10z_astra_{arms,read,selftest}.py`.

**Remaining BLOCKING items — exact replacement text**

1. **The prohibition on numeric C01 test fixtures contradicts the required tests.**

   D:5 explicitly prohibits numbers in “driver, reader or test code”; B:62 repeats that prohibition. But B:230 requires `C01_FIX = 7800.`, and B:309–339 requires numeric boundary fixtures. Under B:60, the builder must stop on this disagreement.

   Replace D:5’s first sentence and B:62’s final sentence with:

   > Production driver and reader code must obtain the selected C01 from validated launch provenance; they must not hard-code the benchmark-selected value. Literal contractual bounds and numeric synthetic test fixtures, including C01_FIX and boundary cases, are permitted. Tests must not treat a fixture value as the selected live ceiling.

2. **Advisor B3 remains partly open: the existing successful stage-3 fixture cannot pass the new binding check.**

   B:246 supplies a synthetic benchmark path `/x/...` and placeholder hashes. B:255–260 repairs stage-0 fixtures, but omits the successful `stage_call(3)` at selftest:1078–1080. B:153 now requires that call to verify actual benchmark bytes and source/environment identities before reaching the resident stub.

   Append to B §2F:

   > **Successful stage-3 fixture.** Update selftest:1078–1080 to use `_bench_tree` under the patched ROOT. Populate its persisted launch with the real benchmark path, record/script hashes, source/environment identities, computed ceilings and matching go selection. Set the pass record’s ceilings to the same selected values and re-seal its schedule/history before persisting it. Retain the resident stub and the existing success assertions. Do not mock out `verify_launch_binding` in this test. New stage-3 drift tests start from this valid fixture and alter only their named condition. Placeholder bindings remain permitted in reader-only fixtures that never invoke launch admission.

3. **Two acceptance instructions demand incompatible test behavior.**

   - B:388 applies “one disabled marker … letting the run complete” to every T5 case, while B:393 requires `KeyboardInterrupt` to propagate.
   - B:307 requires every HALT test to use `assertRaisesRegex`, but reader entry points return HALT dictionaries (`read:658–659`, `:689–690`). B:357–364 explicitly requires reader tests.

   Replace B:388 with:

   > (T5a–d) Ordinary telemetry I/O failures each print exactly one C10Z_TELEMETRY_DISABLED line, disable later telemetry work, preserve science records and permit normal completion. (T5e) A KeyboardInterrupt raised inside telemetry propagates from the telemetry method; assert that exception directly. T5e does not require a disabled marker or normal completion.

   Replace B:307’s first two sentences with:

   > Every refusal test verifies the HALT code and the intended detail substring. For APIs that raise R.Halt, use assertRaisesRegex. For reader APIs that return a reading, assert scientific_verdict is false, label equals the expected HALT code, and detail contains the intended substring. Keep all prerequisites valid so an earlier refusal cannot substitute for the targeted check.

4. **The live INERT claim exceeds the evidence specified, and admission does not explicitly validate that evidence’s consistency.**

   D:84 extends equality of every other count, lead, hit, hash and reading to MPS after INERT. However, D:91–96 tests **pristine A7 probe tokens and one gathered batch-logit tensor**. It does not establish resource inertness or equality throughout edited A1/A2/A7 runs. Resource differences are explicitly permitted at D:80–86.

   Also, B:282 records `control_equal`, `telemetry_equal` and `weights_unchanged`, but B:284–289 admits the record without explicitly requiring those fields to support its `INERT` verdict.

   Replace D:84 with:

   > Under the controlled stub proof (h′4), every other count, lead, hit, hash and reading is identical. On MPS, INERT establishes equality only for the pristine A7 probe tokens and gathered batch logits specified in (h′3), under the recorded source/environment identity. It is the required admission screen for telemetry-on attempts; it does not establish resource inertness or universal equality of edited-arm outputs and records. Those broader claims remain UNVERIFIED. The timing/resource exceptions and description rule remain binding.

   Replace B:287 with:

   > Validate the complete inertness-record schema and internal consistency: the schema matches, device is "mps", verdict is "INERT", and control_equal, telemetry_equal and weights_unchanged are each exactly true. Require the probe/lens counts prescribed by the complete three-pass schedule. Reject missing or contradictory evidence with HALTED-V12. Test each rejection independently.

   This retains your approved full-A7, three-pass screen and first-attempt-off ruling; it narrows the claim to what that screen measures.

**D1–D5 rulings**

| Item | Ruling |
|---|---|
| **D1 — `noceil` assertion** | **Accept.** With matching pass/launch ceilings and `stage3=None`, `read:574–575` produces `next_stage=None`; `arms:1482–1483` therefore refuses before `:1484`. The current inconsistent fixture also fails earlier once ceiling provenance is enforced. B:261–263 correctly changes the expectation to V12 and preserves the dead check. |
| **D2 — fixture-list corrections** | **Accept the corrections, reject completeness.** `stage_call(2)` reads the launch’s stage2 ceiling and the pass record (`arms:1489–1494`), so selftest:1069 does not require the new stage-0 binding. The additional Budget/history/go fixtures are real omissions. But the successful stage-3 fixture remains missing: blocker 2 above. |
| **D3 — inertness duration** | **Accept.** The benchmark spec’s 11,184–11,406 forwards per pass gives approximately **16.8–85.5 minutes for three probe passes** at 0.03–0.15 seconds/forward, before loading, hashing and extra forwards (`results/c10z_astra_benchmark_spec_v2.md:32`; D:99). “≤10 minutes” was unsupported. This remains an estimate, not a runtime cap. |
| **D4 — stronger T2 and signature adapter** | **Accept.** Full identity under controlled clocks/memory is stronger than stripping fields **within that stub test** (B:377–385); it does not establish hardware identity. Signature inspection avoids masking an implementation `TypeError` (D:59–61; B:309). The separate test-contract errors are blocker 3. |
| **D5 — resident re-hash and ledger match** | **Accept within the controlled launch workflow.** The parent validates the selected bytes before writes, passes the binding directly through the child environment, and stage 3 re-verifies it (D:20–42; `arms:1472–1475`). Program-side ledger verification is explicitly retained at D:19. A second resident read is not inherently required. However, F:23’s “within the same second” is not guaranteed by `Popen`; the justification is the trusted handoff and unchanged sources, not elapsed time. |

**Non-blocking notes**

- **Original blocker disposition:** Astra 1 is resolved by D:77–86; Astra 2 by D:44–55; Astra 3 by D:9–42, subject to D5’s stated scope; Astra 4 by D:57–73. Astra 5 receives the requested CPU checks and live admission screen, but its claim still needs blocker 4’s correction. Advisor B1/B4 are substantively resolved; B2 needs that evidence-scope correction; B3 needs the stage-3 fixture addition.

- **Budget fidelity is preserved.** D:28 retains `[7,200,10,800]` and `2·(C01+C2)≤55,800`; D:38 retains STOP/refusal handling while adding the approved drift-rebenchmark cap. These agree with prereg §9(c–d), `docs/C10Z_ASTRA_PREREG.md:457–459`, and `EXPERIMENT_RUNBOOK.md:365`. No additional ceiling authorization is needed.

- **The build remains CPU-only**, with benchmark and inertness execution deferred (B:35–38, :276). GPU availability alone does not waive the existing scheduling/go decisions in prereg §6 (`docs/C10Z_ASTRA_PREREG.md:341–344`).

- **Clarify scope evidence:** B:43–48 requires every FROZEN file’s hash to remain unchanged while allowing live-run output changes. Apply immutable-hash acceptance to frozen sources/inputs; report actual live-output changes separately. A directory listing alone cannot attribute changes to the live process.

- **Tighten the concurrency test:** B:319–322 should confirm thread T reached an instrumented deadline-lock acquisition attempt before testing that it remains blocked, and release/join both threads in `finally`. `T.is_alive()` alone can reflect delayed scheduling.

Verified prereg SHA `e2d7fa10…eca50` and its preserved prefix. Evidence: source inspection plus small standard-library probes confirming D1 and the reader’s return contract. No implementation, full suites, model or GPU execution.

🌱 Graft reported ~94,836 tokens saved (~$0.08), 1 successful call.

