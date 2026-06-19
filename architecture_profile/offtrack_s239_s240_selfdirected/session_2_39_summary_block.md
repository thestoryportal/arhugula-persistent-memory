# S2.39 Summary Block — surgical-knob test (regularization frontier); viability escape route falsified (COMPLETE)

**Type:** Execution/analysis (pod-side). **Outcome:** COMPLETE. Decision-relevant negative result → v1.7.3 additive. Engine UNMODIFIED. Manifest canonical (resolved post-S2.38).

## Gate
- Engine fingerprint (LAW #1): PASS (`5c0c706a…c78770`, _cov_cpu=3). No science-path patch (hparam sweep only; legitimate config exploration, not engine source change).

## Arm run (chosen per "pick per budget" + the live LLM-as-Database viability question)
**Qwen regularization (mom2_update_weight) sweep** on Bo Jackson→guitar, full band — tests whether a config separates edit expression from same-subject biographical entanglement (the "surgical write knob" escape route I proposed when assessing Qwen viability).
- Swept {3750,7500,15000(canon),30000,60000}; z identical across sweep, only solve update magnitude varies.
- **Result: NO surgical point.** Expression (P 0.87→0.80) and drift (KL 2.09→1.69) fall together; drift/expression ratio ~flat (2.41→2.13, ~12% over 16×); **2/3 biographical attributes flip at EVERY setting**; specificity KL=0 throughout.
- **Cross-fact r=0.90 (v1.7.1) does NOT yield a within-fact tradeoff** — expression and entanglement are coupled, not tunable apart.

→ framework_finding **v1.7.3 additive**: the surgical-knob escape route is falsified for this knob; Qwen's "not viable for multi-field relational" verdict is not rescued by regularization tuning.

## Decisions (D-S239-*)
- **D-S239-1** — Ran the regularization frontier sweep (most decision-relevant to the viability question) in lieu of the broader Qwen multi-fact single-layer / Llama-3.2-3B arms listed in the S2.39 kickoff. Those remain optional/deferred.
- **D-S239-2** — mom2_update_weight sweep is a hparam exploration (not an engine/science-path change); gate #5 N/A.
- Carried: D-S238-1/2; D-S237-*; D-S236-*; D-S235-*; D-S234-* (MANIFEST-1 RESOLVED); D-S233-LAYERMATCH-1/BAND-1/CAPTURE-METHOD-1.

## Artifacts (NV)
- `s239_qwen_reg_sweep.json`
- `framework_finding_v1_7_3_additive.md` (for human KB merge — append to the v1.7 consolidation)
- `session_2_39_summary_block.md` (this), `session_2_40_kickoff.md`
- script: `s239_qwen_reg_sweep.py`

## Outstanding human-gated item (carried)
- **KB merge:** v1.7 FINAL + v1.7.1 + v1.7.2 + **v1.7.3** into project-knowledge. `framework_finding_v1_7_consolidated.md` exists (FINAL+1.7.1+1.7.2); v1.7.3 to be appended. Pod cannot write KB.
- Manifest: RESOLVED (canonical installed post-S2.38; cosmetic status string `…pending_install` may be corrected if the canonical write path is unblocked).

## Next
See `session_2_40_kickoff.md`. STOP for human review.
