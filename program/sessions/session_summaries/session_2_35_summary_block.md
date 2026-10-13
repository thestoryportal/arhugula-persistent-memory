# S2.35 Summary Block — Llama-vs-Qwen z-Geometry + Qwen Entanglement Probe B (COMPLETE)

**Session type:** Execution (pod-side). **Outcome:** COMPLETE — all four scope items delivered; gate #3 cleared on corrected harness; framework_finding v1.7 (additive) authored. No HALT. Engine unmodified.

## Gates
- **Engine fingerprint (LAW #1): PASS** — `sha256(memit_main.py)=5c0c706a…c78770`, `_cov_cpu`=3.
- **Known-baseline reproduction (LAW #3): PASS** — corrected Llama harness reproduces v1.5 §3: step-0 **1.569e-08 / loss 17.995** (§3 ~1.6e-08 / ~17.96); final **3.07e-05 / 10.497** ≈ canonical s224 (2.84e-05 / 10.591). Verified BEFORE the Qwen arm and Probe B (gate ordering honored).
- **Read-source-before-authoring (LAW #4): PASS** — harness authored from cat-read engine source (S2.34 + this session).
- **Science-path patch isolation (LAW #5): n/a** — no science-path source change; fix was harness-level (target string). Engine left UNMODIFIED.
- **Determinism:** seed 0; engine context-template cache forced fresh under seed.

## What was run (all on cfb-v3-001 Bo Jackson→guitar, matched band [4,5,6,7,8], z_layer 8, 25 steps, lr 0.5)
1. **Llama-3.1-8B z-trajectory** (v_loss_layer 31). Lookup index **3** (` plays`, canonical). STALL: non-monotonic, avg-prob plateaus ~1e-5, no convergence over 25 steps.
2. **Qwen2.5-7B z-trajectory** (v_loss_layer 27). Lookup index **1** (` Jackson`, true subject-last; Qwen no-BOS). CONVERGE: loss 5.54→0.049, avg-prob 5.88e-3→**0.997**, early-break @ step 11.
3. **Probe B (Qwen entanglement):** full `apply_memit_to_model` (weights restored after). Per-layer update norms front-loaded on layers 4–5 [1.95,1.80,0.74,1.05,1.33]. Same-subject biographical DRIFT (KL 2.49, college Auburn→UCLA, birth-state Mississippi→Texas, zero guitar leakage); other-entity specificity exact (KL 0.000).

## Headline findings (→ framework_finding v1.7 §X.1/§X.2)
- **Llama stall is a step-0 accessibility gap (~6 OOM) + ill-conditioned band surface**, NOT a clamp or lookup artifact (both deltas saturate the 0.75·||init|| L2 ball; Qwen converges despite the same clamp).
- **Qwen success is entity-local but attribute-NON-local:** edits drag unrelated same-subject attributes to wrong values with zero target leakage; cross-entity specificity is exact (KL 0). Localized to early band layers 4–5.
- Both consistent with the program claim: Llama architectural-invariant ceiling (now step-resolved); Qwen falsifies generality but only via attribute-entangled writes.

## Decisions (D-S235-*)
- **D-S235-1** — Proceeded under the S2.34 re-diagnosis (corrected target `" guitar"`; canonical lookup index 3/1 left untouched). Re-diagnosis empirically confirmed by gate-#3 reproduction.
- **D-S235-2** — Probe B uses full apply_memit_to_model (weight write) THEN restore from `return_orig_weights` copy. Permitted: D-S233-CAPTURE-METHOD-1 (no-weight-write) governs the z-trajectory arms only; Probe B inherently requires an applied edit. Model weights restored; no NV/engine mutation.
- **D-S235-3** — Anchor-position difference (Llama ' plays' = subject+1 via BOS double-count; Qwen ' Jackson' = subject-last) DOCUMENTED as canonical/load-bearing, NOT corrected (correcting fails gate #3 / breaks comparability).
- **D-S234-MANIFEST-1 (carry, STILL DEFERRED)** — two divergent manifests confirmed: `/workspace/reproducibility_manifest.json` and `/workspace/architecture_profile/reproducibility_manifest.json`. Per storage discipline (overwrite-in-place deny-listed; divergent+unmerged → no writes), NOT merged this session. **No manifest writes.** Manifest entries to be added on merge (see below).

## Manifest entries to record at merge (deferred — for the merge step, NOT written to either manifest)
- S2.33: HALT (target-string misdiagnosis as BOS bug). No data promoted.
- S2.34: HALT_REDIAGNOSED. Overturned S2.33; corrected fix = target leading space; engine unmodified. Artifact: architecture_profile/s234_halt_diagnostic.json.
- S2.35: COMPLETE. Llama+Qwen z-geometry + Qwen Probe B; gate #3 PASS; framework_finding v1.7 additive. Artifact: z_convergence_trace_llama_vs_qwen.json. Engine SHA 5c0c706a…c78770.

## Artifacts written (NV)
- `z_convergence_trace_llama_vs_qwen.json` — combined per-step trajectories + endpoints + gate + Probe B (PRIMARY mechanistic evidence)
- `s235_llama_trace.json`, `s235_qwen_trace.json`, `s235_probe_b_qwen.json` — raw per-arm
- `framework_finding_v1_7_additive.md` — additive finding (for human KB merge; KB not writable from pod)
- `session_2_35_summary_block.md` (this), `session_2_36_kickoff.md`
- Capture scripts: `s235_llama_capture.py`, `s235_qwen_capture.py`, `s235_probe_b.py`

## Next
See `session_2_36_kickoff.md`. STOP for human review.
