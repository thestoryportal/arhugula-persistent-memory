# LARQL Integration Assessment (T2.4) — load-bearing findings
_2026-06-17. Status: LARQL toolchain built + characterized; clean end-to-end inference NOT yet achieved on this Linux/CPU pod. This is the high-value deliverable of the T2.4 effort — the characterization, not a pass._

## What LARQL is, mechanically (verified from source)
- **Write engine is two-tier:** `INSERT` = **L1 feature ALLOCATION** ("Feature F8821@L26 allocated") — additive, collision-free by construction (add-a-neuron model). `COMPACT MAJOR` = **L2 MEMIT consolidation** — `crates/larql-lql/src/executor/compact.rs` calls `memit_solve(keys,targets,λ)`, `ΔW = Tᵀ(KKᵀ+λI)⁻¹K`; `crates/larql-inference/src/forward/memit.rs` is the same MEMIT algorithm we tested (null-space/covariance solve, cites Meng et al.).
- **=> Our entire editing validation (collision findings, preserve-sampling, AlphaEdit recipe, thresholds) maps onto LARQL's `COMPACT` step (= the spec's compaction/compile-to-weights), NOT onto incremental `INSERT`.** Not the wrong mechanism — correctly scoped to consolidation. Model-specific *calibration* still per-model.
- Read/query: LQL `WALK`/`DESCRIBE` (browse-level, feature traces), `INFER`/`run` (inference-level, generation). Overlays = `.vlp` patches on a frozen base; `COMPILE` bakes into standard safetensors/GGUF.

## Model support — ASYMMETRIC (verified from docs/source/tests)
- **Gemma-3-4B: thoroughly DEMONSTRATED.** 141 result/bench mentions; production `gemma3-4b-q4k-v2.vindex`; FR-routing benchmarks (FR1/FR2/FR3, 20 facts @L26, distractor-safe), MEMIT compaction validated. Chris's primary/production model.
- **Qwen: code-only, NOT demonstrated end-to-end.** `qwen.rs` handler exists (Qwen2/2.5 attn Q/K/V bias; Qwen3 qk-norm; Qwen-MoE). `test_architectures.rs` has Qwen **arch-DETECTION** unit tests only (asserts family + tensor keys) — NOT inference/results. 29 doc mentions, **0** run/infer/results examples. Qwen-VL explicitly "design-only".
- **Our empirical Qwen2.5-0.5B run = garbage** (`run`→token salad, `INFER`→`);;` 21%). Extracted vindex correctly detected `family: qwen2` but `weight_manifest.json` had **0 bias tensors** → likely the extractor declares bias keys (unit test passes) but never WRITES them (path never exercised end-to-end). Consistent with a latent bug in an unvalidated path.

## THE load-bearing unknown: CPU-backend correctness (product-critical)
- I have **never seen LARQL produce clean inference on ANYTHING** here (Qwen→garbage; published Gemma vindex = **browse-only**, no inference weights, can't generate).
- So Qwen garbage is **confounded**: Qwen-bug vs **CPU-backend-bug**. Chris develops/benchmarks on **Metal** (`larql-compute-metal`); this pod is **Linux CPU**.
- **Deployment target is the operator's Intel CPU.** If LARQL's CPU forward pass is immature/incorrect, that is a deployment risk for the WHOLE spec, independent of model. **Bigger than Qwen-vs-Gemma.**
- Cheap discriminators (no multi-GB extracts): `larql parity --backends reference,cpu` (CPU-vs-reference numerical diff, works w/o Metal); `cargo test -p larql-inference` (CPU forward-pass tests); tinymodel fixture. (Running.)

## Decision framework (per advisor)
- **Do NOT pick Path A (debug Qwen extraction):** unbounded debugging of an unvalidated path in someone else's Rust.
- **Do NOT pay the Gemma re-run cost yet:** if CPU backend is the problem, re-running the whole suite on Gemma is also wasted.
- **Sequence:** (1) confirm CPU-backend correctness cheaply (parity/tests). (2) If CPU correct → model decision: Gemma (proven) is the safe stack; requires local inference-level Gemma extract (gated HF + heavy) + re-running editing suite on Gemma (methodology transfers; numbers/hparams/calibration redone; newer-transformers env). (3) "LARQL reads Qwen cleanly ⇒ all gates" is NECESSARY-NOT-SUFFICIENT — still must prove LARQL `COMPACT` reproduces locality/durability.
- **Scope reality:** validating LARQL end-to-end is a substantial SEPARATE effort gated on CPU-backend maturity + model pivot — not a quick "remaining GPU test."

## Artifacts (in /workspace)
larql CLI: external_prior_art/larql/target/release/larql. Logs: larql_convert*.log, larql_qwen_all_test.log, larql_inference_tests.log, larql_gemma_*.log. Vindexes: /dev/shm/qwen05*.vindex (Qwen, garbage inference), hf_cache/...gemma-3-4b-it-vindex* (browse-only).

## KEYSTONE TEST (2026-06-17): Qwen3-0.6B positive control
Rationale: confirmed bug = missing ATTENTION BIAS; Qwen2/2.5 have bias, **Qwen3 has none (qk-norm instead)** → Qwen3 sidesteps the bug. Qwen3-0.6B is ungated + LARQL's own documented example. Clean "Paris" ⇒ (1) CPU backend works end-to-end [resolves deployment-CPU unknown], (2) LARQL Qwen-family viable, (3) Qwen2.5 garbage = definitively the bias bug. Garbage ⇒ deeper LARQL-CPU/extraction problem (major spec risk). Script: larql_qwen3_poc.sh → larql_qwen3_poc.log.
Decision tree after: clean → (a) write-science transfer test (INSERT→COMPACT→read reproduces locality/durability), (b) model decision Qwen3 vs Qwen2.5+biasfix vs Gemma, (c) confirm on operator Intel CPU.
CPU-correctness so far: larql-inference unit tests PASS (14/14, 0 fail) → primitives correct; but NO end-to-end positive control yet (this test provides it). Qwen2.5 --level all STILL garbage + 0 bias → bias bug confirmed across levels (not a level issue).

## ✅ KEYSTONE RESULT (2026-06-17): POSITIVE CONTROL CLEAN
Qwen3-0.6B via LARQL on Linux CPU: `run "The capital of France is"` → "**Paris**. The capital of Italy is Rome. ..." (coherent, correct); `INFER TOP 5` → **1. Paris 65.64%**. qk_norm extracted (56 entries), bias=0 (correct for Qwen3).
**PROVES: (1) LARQL CPU backend correct end-to-end [deployment-CPU risk CLEARED], (2) LARQL Qwen-family viable, (3) Qwen2.5 garbage = definitively the missing-bias extraction bug (controlled differential).**
**=> Viable CPU-local path DEMONSTRATED: Qwen3 + LARQL on CPU. Gemma pivot NO LONGER REQUIRED. Same family as our Qwen2.5 editing validation → science transfers with recalibration.**
OPEN: LARQL WRITE path (INSERT→COMPACT/MEMIT) on Qwen3 not yet tested (clean reads necessary-not-sufficient); re-run editing suite on chosen Qwen3 size; confirm on operator Intel CPU.
NEXT: write-science transfer test — LQL INSERT fact → INFER (L1 read) → COMPACT MAJOR (L2 MEMIT) → INFER (survives + locality).

## ⚠️ CRITICAL (2026-06-17): LARQL's IN-WEIGHT write paths fail on Qwen3; only retrieval-override works
Tested LARQL's write engine on the working Qwen3-0.6B vindex:
- **INSERT MODE=knn (default)** = post-logits KNN retrieval override (Architecture B). WORKS but: (a) NOT in-weight (sidecar after logits; `model_top1` unchanged), (b) **cross-entity collision at N=1** — 1 fact (France→Berlin) makes Italy & Spain ALSO return Berlin (cos 0.92-0.93). = Chris's documented "legacy KNN unsafe at scale, 0/20 distractor-safe."
- **INSERT MODE=compose** = "constellation" install (trace-guided gate+up+down, gate_scale=30) directly into FFN. **CORRUPTS the model** → garbage (ệc/aseña/utsche) for ALL queries.
- **COMPACT MAJOR** (L1→L2 MEMIT) = "No edge metadata available for MEMIT solve" → **did not run**. MEMIT-via-CLI flow incomplete.
- LARQL's MEMIT is doc-validated only on **TinyStories-115M in Python**, not real models via the Rust CLI.
**=> LARQL's DEMONSTRATED/working write = retrieval-augmentation (KNN), NOT the spec's in-weight thesis. LARQL's in-weight write paths are immature/buggy on a real model (Qwen3).**
KEY DISTINCTION: in-weight MEMIT editing as an APPROACH is VALIDATED — by OUR raw-engine experiments on Qwen2.5 (Tiers 1-2 all pass). It is LARQL's TOOL IMPLEMENTATION of the in-weight write that fails here.
CANDIDATE ARCHITECTURE (decouple write from serve): WRITE = our validated MEMIT pipeline (edit weights offline/GPU) → SERVE/QUERY = LARQL (extract vindex from edited weights; read works on Qwen3/CPU). Avoids LARQL's immature in-weight write. UNTESTED: does LARQL read reflect externally-MEMIT-edited weights.
Caveats: default hparams (compose gate_scale=30 may be miscalibrated → corruption possibly tunable); COMPACT metadata flow may be a usage gap; Qwen3-0.6B tiny.

## ✅✅ DECOUPLE ARCHITECTURE CONFIRMED END-TO-END (2026-06-17)
Test: edited Qwen3-0.6B weights via OUR minimal MEMIT (rank-one down_proj L14, France→Berlin; transformers 5.12.1 for Qwen3) → saved standard safetensors → LARQL `convert safetensors-to-vindex --level all` → `run`/`INFER`.
RESULT: LARQL serves OUR edit — `INFER "The capital of France is"` → **Berlin 99.43%** (Paris 0.16%), via **walk FFN (weights), NOT knn_override sidecar**. Edit is genuinely in-weight and LARQL reflects it on CPU.
(Italy→Berlin bleed = MY crude rank-one edit's cross-entity collision, no preserve-sampling — LARQL faithfully serving bled weights; our FULL recipe controls this per Tiers 1-2.)
**=> VIABLE, HIGH-CERTAINTY, CPU-LOCAL PATH DEMONSTRATED: WRITE = our validated MEMIT/AlphaEdit pipeline (offline GPU) → SERVE = LARQL on CPU (vindex+LQL). Bypasses LARQL's immature native in-weight write (COMPACT/MEMIT).**
SPEC IMPLICATION: this is a spec AMENDMENT (spec-as-written = LARQL does in-weight write; viable path = our pipeline writes, LARQL serves). Operator decision.
REMAINING for full implementation on this path: (1) re-run our FULL recipe (AlphaEdit+preserve-sampling, calibrated) on Qwen3 → clean multi-fact locality end-to-end (not crude-edit bleed); covariances+hparams for Qwen3 (transformers 5.12.1 now supports it); (2) confirm on operator Intel CPU; (3) multi-fact/scale via the decoupled pipeline.
Artifacts: s245_decouple_edit.py, larql_decouple_serve.sh/.log, /dev/shm/qwen3_edited(.vindex).

## OPTION A vs B — evidenced comparison (2026-06-18)
PORT: transformers 4.51.0 = Qwen3 + engine both work (5.x broke engine nethook; 4.45 lacked Qwen3). Qwen3 covariances computed (s246). Recipe ports to Qwen3 NO recalibration: single-fact smoke expressed post_p=0.85, same-entity 92.8%, cross-entity 96.2%.
OPTION A (our pipeline -> merge -> LARQL serve) — EVIDENCED CLEAN (A1-A3 done):
- A2 multi-fact (6 capitals + preserve-sampling) on Qwen3: edited retention 83% (5/6; Germany under-expressed), CONTROL cross-entity loc 98.75%/top1 100% (vs crude s245 ~0), same-entity 90.5%.
- A3 decoupled serve: LARQL serves the 5/6 edits cleanly (France->Berlin 79%, Japan->Cairo, Italy->Oslo, Poland->Nairobi) AND controls preserved (Greece->Athens, Egypt->Cairo, China->Beijing). Clean multi-fact locality end-to-end on CPU.
- Remaining: A4 scale, A5 tiers on Qwen3.
OPTION B (LARQL-native overlay/governance) — STRUCTURE EXISTS, IMPLEMENTATION IMMATURE:
- Overlay SERVE on frozen base (APPLY PATCH): WORKS (France->Berlin served, base unmodified).
- Native INSTALL (COMPOSE, tuned ALPHA=0.3): installs target but BLEEDS (Italy->Berlin 39.8%) + corrupts (Spain->garbage) — no preserve-sampling. (Default gate_scale=30 corruption was MIScalibration, confirmed; but even tuned it bleeds.)
- Rollback (REMOVE PATCH): FAILS — patch registers "(unnamed)", REMOVE-by-path can't match. Governance rollback not working as driven.
- => Clean, governed B requires LARQL engineering (preserve-sampling in overlay install + patch-naming/rollback fix, or inject our decomposed clean-ΔW as overlay slots). OUT OF VALIDATION SCOPE. B cannot be fully cleanly evidenced without LARQL dev — that is the finding.
NET: Option A is clean + working (bounded remaining); Option B's governance structure is real but its clean-install + rollback are immature in LARQL.

## FINAL EVIDENCE SUMMARY (2026-06-18) — both options characterized
OPTION A (our pipeline -> merge -> LARQL serve) — FULLY EVIDENCED on Qwen3 (A1-A5):
- A1 covariances/recipe ported (transformers 4.51); A2 multi-fact edit clean (controls 100% top1); A3 LARQL serves edits + preserves controls (CPU); A4 scale retention 94% + ppl flat (control-loc = coverage knob, model-size dependent); A5 CRUD (INS 6/6, UPD 5/6, DEL 6/6) + compaction 100%->100% PASS.
- VERDICT: clean, working, CPU-local decoupled path. COST: spec amendment (our pipeline does MEMIT, not LARQL's native write); produces MERGED weights (re-extract per write batch — no incremental overlay; loses overlay-governance).
OPTION B (LARQL-native overlay/governance) — CHARACTERIZED, IMMATURE:
- Overlay SERVE on frozen base works; native INSTALL bleeds (no preserve-sampling) + corrupts; rollback (REMOVE) fails (unnamed patch). COMPOSE corruption = miscalibration (tunable) but clean+governed B needs LARQL dev (preserve-sampling in overlay install + rollback fix, or decompose our clean-ΔW into slots). OUT OF VALIDATION SCOPE.
- VERDICT: governance structure real; clean+governed implementation gated on LARQL engineering.
D1 (operator Intel CPU): pod Linux-CPU PROXY PASSED (LARQL serves Qwen3 cleanly on CPU); final confirmation needs operator hardware.
THE DECISION (operator's): governance NOT essential -> Option A is ready (fully evidenced, clean, CPU-local). Governance essential -> Option B requires LARQL development. Spec-as-written (LARQL native write) = the immature link.

## CORRECTION (2026-06-18) — overlooked no-code solutions found (user challenge)
I overstated B's failures. Re-investigation found:
- **ROUTE VERIFY fixes the cross-entity collision, NO CODE.** `INFER "..." ROUTE VERIFY` → France keeps edit (Berlin via knn_override), Italy→Rome, Spain→Madrid (bleed GONE; verify/abstain router abstains for distractors). My "B bleeds, needs code" was WRONG.
- **Rollback works by construction, NO CODE.** Base is frozen + overlay is a separate .vlp; serve base alone → France→Paris (original). REMOVE-command failure was a usage/naming detail, not a governance-property failure.
- **=> Spec's L1 cache tier (KNN overlay + ROUTE VERIFY) is FULLY VIABLE NO-CODE: governed (frozen base/separable overlay/rollback/append-only-incremental) + collision-safe. BUT it is RETRIEVAL (post-logits sidecar), not in-weight.**
- **L2 in-weight commit (COMPACT/MEMIT) genuinely blocked:** "No edge metadata available for MEMIT solve" persists even with BEGIN PATCH + relation + MODE=COMPOSE (3 L1 edges recognized). The COMPOSE->L1->COMPACT metadata flow is incomplete = real LARQL code gap.
REVISED VERDICT: spec's TWO-TIER write maps cleanly — L1 (governed retrieval cache, ROUTE VERIFY, NO CODE, works now) + L2 (in-weight MEMIT compile, needs LARQL metadata-flow fix). In-weight durability (L2) needs code; governed queryable storage (L1) does NOT. Option A (our-pipeline write + LARQL serve) remains the no-code IN-WEIGHT path (merged, no overlay-governance). Three viable shapes now, each with a clear tradeoff.

## COMPILE finding (2026-06-18) — bakes overlay->weights, but gated on COMPOSE quality
COMPILE CURRENT INTO VINDEX works (no code): "Down overrides baked: 1 (1 layer touched)" — bakes overlay down-overrides into standard down_proj (in-weight). Tested code path (compile_into_vindex_with_down_overrides_bakes_them). BUT it baked the CORRUPTED COMPOSE install (gate_scale=30) -> compiled vindex serves garbage (ệc). So COMPILE is only as good as the COMPOSE install. COMPOSE install = the bottleneck (corrupts default / bleeds, no preserve-sampling; ROUTE VERIFY is KNN-router-only, doesn't fix COMPOSE). MEMIT ΔW (dense low-rank delta) doesn't map directly to COMPILE's per-feature down-overrides, so injecting our clean ΔW as overrides isn't direct.
## COMPLETE MAP OF VIABLE SHAPES (after exhausting no-code avenues)
1. L1 GOVERNED RETRIEVAL CACHE (KNN overlay + ROUTE VERIFY + rollback-by-base): NO-CODE, governed, collision-safe, queryable, incremental. NOT in-weight (post-logits retrieval).
2. OPTION A — CLEAN IN-WEIGHT, MERGED (our pipeline + LARQL serve): NO-CODE, in-weight, clean locality (preserve-sampling). MERGED weights (no overlay-governance; re-extract per write-batch).
3. L2 IN-WEIGHT GOVERNED OVERLAY (COMPOSE->COMPILE): COMPILE works no-code, but COMPOSE install unclean -> needs LARQL code (preserve-sampling in COMPOSE) OR a ΔW->down-override decomposer. The spec's FULL vision (in-weight + governed overlay + clean) = this, and it's the one needing LARQL work.
RESIDUAL BLOCKER (precise): clean+governed+in-weight via LARQL native is gated on COMPOSE install quality (preserve-sampling). You can have in-weight+clean (A, merged) OR governed+queryable+collision-safe (L1, retrieval) NO-CODE today; the union (all three) needs the one LARQL improvement.

## ✅✅✅ BOUNDED BRIDGE SOLVED (2026-06-18) — clean + in-weight + governed, NO LARQL code
Method: Python .vlp generator (s252b_build_vlp_full.py) writes OUR proven-clean edited down_proj columns (A2, preserve-sampling) as base64-f32 `down_vector` UPDATE ops (full band L4-8, 15360 ops, 81MB .vlp) -> LARQL `APPLY PATCH` (governed overlay on FROZEN base) -> `COMPILE CURRENT INTO VINDEX` (bakes 15360 down-overrides into down_proj, in-weight). Bypasses LARQL's flawed COMPOSE install entirely; uses only existing LARQL commands.
RESULT (serve bridged vindex): France->Berlin 79%, Japan->Cairo 66%, Italy->Oslo 81%, Poland->Nairobi 96% (edits); Greece->Athens, Egypt->Cairo, China->Beijing (controls PRESERVED); rollback (base alone) -> France->Paris (frozen base intact). = EXACTLY our clean A3 result, now GOVERNED (separable .vlp overlay, frozen base, rollbackable) + IN-WEIGHT (COMPILE-baked, walk-FFN not knn sidecar).
KEY INSIGHTS (user-driven): (1) don't route through COMPOSE (no null-space/preserve-sampling); inject our clean ΔW directly. (2) .vlp = JSON w/ base64-f32 down_vector slots (Python-writable). (3) DIFF gives the changed-feature/layer list but only metadata (no vectors) -> we fill the real vectors. (4) full-band override needed (dense ΔW; 4414 label-flippers insufficient -> partial; 15360 full-band -> exact). (5) COMPILE bakes overrides->weights.
=> OVERTURNS "Option B needs LARQL dev". The spec's FULL VISION (clean + in-weight + governed overlay) is ACHIEVABLE NO-LARQL-CODE via .vlp-injection of our pipeline's clean ΔW + APPLY + COMPILE.
CAVEAT (efficiency, not viability): overlay is band-sized (81MB) — dense per-feature storage of a low-rank (rank~6) ΔW. A low-rank/changed-only .vlp would be ~tiny; that's an optional LARQL format enhancement, NOT a blocker. ALSO: ROUTE VERIFY gives a SEPARATE no-code L1 governed-retrieval path. Two governed paths now exist.
