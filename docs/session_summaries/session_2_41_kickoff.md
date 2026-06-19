# S2.41 Kickoff — calibrate the same-subject-locality metric, then MODEL × CORPUS cross (disambiguate H-MODEL vs H-PROBE)

Session type: Calibration + decisive disambiguation. Selected by the S2.40 Gate A HALT. Gate A showed the canonical clean MEMIT model (GPT-J) drifts HIGH on same-subject attributes (2.48) — same regime as Qwen-cfb-v3 (2.45) — so the same-subject drift metric has NO calibrated clean floor and v1.8's "model axis is cleaner" routing is undercut. S2.41 does NOT run the model-hunt. It (a) anchors the drift scale, then (b) runs the one experiment that separates model-effect from probe-effect.

## Read order
- session_2_40_summary_block.md + framework_finding_v1_9_additive.md (Gate A HALT; the reopened framing)
- architecture_profile/s240_halt_diagnostic.json (decisive-next-experiment spec + the two hypotheses)
- s240_gptj_positive_control.json (GPT-J high-drift data + the 5 CounterFact facts/probes) ; s239_qwen_cfb_v4_proberun.json (the cfb-v4 facts/probes)
- framework_finding_v1_8_additive.md (the cfb-v4 low-drift result now reopened) + framework_finding_v1_7_consolidated.md (v1.7.1/.3/.4 still reopened)

## First actions at entry
1. Engine fingerprint gate: `5c0c706a…c78770`, `_cov_cpu==3`. Engine UNMODIFIED.
2. Kernel hygiene; HF_HOME on NV before HF import; `os.chdir(ENGINE_ROOT)` before `from memit …`; pad-token; target `" "+object`. Both GPT-J-6B and Qwen2.5-7B are now cached (no downloads).

## The question
Why does Qwen-cfb-v4 read LOW same-subject drift (0.20) when both GPT-J (any corpus tested) and Qwen-cfb-v3 read HIGH (~2.5)? Two hypotheses Gate A cannot separate:
- **H-MODEL:** Qwen2.5-7B is genuinely more same-subject-local than GPT-J (real, valuable → Qwen leads for multi-field LLM-as-DB).
- **H-PROBE:** cfb-v4's specific subjects/targets/probes are drift-resistant (artifact → v1.8's "corpus artifact" verdict is itself not robust).

## Arms (in order; A gates B)
- **GATE-CAL — calibrated drift floor/ceiling (do FIRST).** On BOTH models, measure same-subject drift for (i) a NULL/identity edit (re-assert the model's CURRENT top-1 value as target_new — expected near-zero drift = the true floor), and (ii) a destructive control. Establish a per-model normalized drift scale so absolute KL can be read as clean-vs-broken. GATE: the null-edit floor must be ≈0 on both models; if a null edit already drifts high, the metric/harness is broken at a deeper level → HALT.
  - **Adopt the 2601.17343 protocol formally** (Liu et al. 2026, "Are We Evaluating the Edit Locality … Properly?"): our pre/post behavioral-deviation KL IS their endorsed metric. Add their two refinements: (a) a **percentage-scaled** locality figure for interpretability; (b) the **regularizer-sensitivity check** — sweep the MEMIT essence-KL `kl_factor` and confirm the drift metric MOVES with it (existing GT/token-match metrics fail this; ours should pass). If the metric is insensitive to `kl_factor`, it is not measuring what we think → HALT. (See `s240_literature_scan.md`.)
- **ARM X1 — MODEL × CORPUS cross on IDENTICAL probes (the decisive experiment).** Four cells, same probe batteries both ways: {GPT-J, Qwen} × {cfb-v4 facts, CounterFact/Gate-A facts}. Report normalized same-subject drift per cell.
  - If Qwen reads LOW on BOTH corpora and GPT-J HIGH on BOTH → **H-MODEL** (Qwen is the locality lead; revive a *calibrated* model-hunt).
  - If BOTH models read LOW on cfb-v4 and HIGH on CounterFact → **H-PROBE** (cfb-v4 drift-resistant; v1.8 reopened-and-falsified; the entanglement is real and general).
  - Mixed → partial; document the interaction.
- **ARM X2 (conditional) — mechanism of any model gap.** Only if H-MODEL: is Qwen's lower drift from edit geometry (front-loading/update norms) or from sharper/more-robust attribute encoding? Tie to z_convergence_trace + v1.7.2 front-loading.
- **ARM X4 (within-MEMIT mechanism fix; literature-motivated) — boundary-layer / computed-residual.** BLUE (arXiv 2502.03748) finds, on our exact layer sets, that the front-loaded FIRST critical layer contributes <0.1 to the edit while the LAST contributes ~1.0 — i.e. our v1.7.2 L4 large-norm write is low-contribution + error-inducing, and error grows with batch size + sequence length (the DB regime). TEST: re-run the same-subject Probe-B battery with the distributed early-layer residual suppressed (update only first+last critical layers with the directly-computed residual). Read: does same-subject drift drop vs canonical MEMIT? This is the first *fix* attempt for the failure mode, not just a description. Isolate the source change against a known-ceiling Llama result first (LAW #5). NOTE: BLUE's own specificity is only "comparable" — do not assume a drift reduction; measure it.
- **ARM X3 (conditional next-MECHANISM; see Open framing) — GRACE with learned scope.** If X1→H-PROBE. Use BalancEdit's (arXiv 2505.01343) learned per-fact influence-scope (positive/negative sampling) instead of a hand-tuned ε — this answers the ε-calibration caveat directly.

## Benchmarks (external-validity, from s240_literature_scan.md)
- Keep cfb-v4 + CounterFact-canonical as the controlled in-house pair. ADD **RippleEdits** (Cohen/Yao et al.) as the external anchor — it is the named benchmark for the "Ripple Effect in the Same Entity," i.e. exactly our same-subject failure mode. **MQuAKE** (multi-hop) for portability/does-the-model-reason-with-the-edit; **KnowEdit/CounterFact+** optional for breadth. Situate methods in the survey taxonomy (2406.01436): MEMIT/ROME = parameter-modifying/locate-and-edit; GRACE = parameter-preserving/additional-params.

## Deliverables
- session_2_41_summary_block.md; s241_drift_calibration.json (GATE-CAL, incl. kl_factor-sensitivity); s241_model_corpus_cross.json (ARM X1 — the disambiguation); s241_blue_boundary_layer.json (ARM X4, if run); framework_finding v1.10 additive (calibrated metric + H-MODEL/H-PROBE verdict + any BLUE-fix result); session_2_42_kickoff.md.

## Do-NOT (carried halt discipline)
- Do NOT run a model-hunt (old Arm M2) or re-derive Qwen viability (old Arm M1) until the same-subject-locality metric is calibrated (GATE-CAL) and the model-vs-probe question is settled (ARM X1). The S2.40 M1 harness `s240_qwen_cfb_v4_viability.py` stays staged; re-use it only AFTER the metric is anchored.
- Do NOT treat ANY multi-field viability verdict as established: v1.7.1/.3/.4 AND v1.8's resolution are all reopened.

## Carried decisions
- D-S240R-1..5; D-S239R-1..5; D-S234-* (MANIFEST-1 RESOLVED); D-S233-LAYERMATCH-1/BAND-1/CAPTURE-METHOD-1.

## Primary-source grounding for the HALT (MEMIT paper, Meng et al. ICLR 2023; arXiv 2210.07229)
Verified against the paper directly (see framework_finding_v1_9_additive §2.5): MEMIT's own specificity metric, Neighborhood Success, is CROSS-ENTITY — *"prompts about distinct but semantically-related subjects"* (for the MJ→baseball edit the paper probes Kobe/Magic, never other facts about Jordan); zsRE specificity is *"a randomly-sampled unrelated fact."* The paper edits GPT-J/GPT-NeoX up to 10,000 facts and reports GPT-J NS=83.5 (clean) — but NEVER measures same-subject/different-attribute preservation. So Gate A did not contradict the paper: it reproduced GPT-J's cross-entity cleanliness (KL≈0) and measured a NEW axis the paper omits, on which MEMIT-GPT-J fails. This is *why* GATE-CAL is needed — there is no literature-anchored clean floor for the same-subject axis; we must build one. Reuse the paper's NS definition as the (already-calibrated) cross-entity control alongside the new same-subject floor.

## Open framing for the record
The deepest possibility, kept open: same-subject multi-field locality is generically poor under MEMIT-class subject-token editing (GPT-J confirms it on the canonical case; the lineage named it "essence drift" in ROME (arXiv 2202.05262) — "a nuanced form of bleedover, hard to detect quantitatively" — controlled only by a single `"{subject} is a"` KL term that MEMIT inherits (`kl_factor`) and that Gate A shows is insufficient; MEMIT itself measures only cross-entity NS). If ARM X1 returns H-PROBE, the LLM-as-DB multi-field write likely needs a different write MECHANISM, not a different base model — a Workstream-level reframe.

### Concrete next-mechanism arm (conditional, if X1 → H-PROBE): GRACE
The weight-preserving alternative is already scaffolded on-NV at `grace_dry_run/` — GRACE ("Aging with GRACE", Hartvigsen et al., NeurIPS 2023, arXiv **2211.11031** — NOTE: not 2305.14129, which is an unrelated same-named code-edit paper). GRACE stores edits in a discrete key-value codebook gated by ε-ball deferral and **leaves base weights frozen**, so same-subject other-attribute locality holds **by construction** (a non-matching prompt runs the unedited model). This directly targets the failure mode MEMIT-class weight editing cannot escape. Proposed ARM X3 (only if H-PROBE): run the Probe-B same-subject battery against a GRACE edit on the cfb-v4 + CounterFact facts; expected near-zero same-subject drift validates the mechanism, and the read shifts from "which model is local" to "weight-integration vs retrieval-patch" for the LLM-as-DB write layer. Caveat to test: ε sizing — too large risks false-positive bleed (incl. same-subject), too small misses paraphrases; characterize the ε/generalization/locality trade-off, do not assume it.

APPROVE-TO-PROCEED:
