# S2.36 Kickoff — v1.7 consolidation: multi-fact generalization of the z-geometry + entanglement findings, and the deferred manifest merge

Session type: Execution (pod-side). Builds on S2.35 (COMPLETE). The S2.35 findings are single-fact (cfb-v3-001 Bo Jackson). S2.36 tests whether they generalize across the cfb-v3 set and resolves the long-deferred manifest merge.

## Read order
- session_2_35_summary_block.md (predecessor close)
- z_convergence_trace_llama_vs_qwen.json (S2.35 primary evidence)
- framework_finding_v1_7_additive.md (the additive finding to be consolidated/promoted)
- architecture_profile/s234_halt_diagnostic.json (the re-diagnosis that unblocked S2.35 — confirms lookup index canonical, target leading-space fix)
- framework_finding v1.6 §2.2 / §3.4 (Qwen convergence + entanglement threads)
- memit-patches-canonical v2.6 (P-VRAM-CPU-SOLVE; engine left patched, UNMODIFIED)
- cfb-v3 + probe-set-v3 (LOCKED)

## First actions at entry
1. Engine fingerprint gate: `sha256(memit_main.py)==5c0c706a66c385273d0a48ebbb8274a1c31bf3e101ca309e47db9cb8b6c78770`; `_cov_cpu==3`. DO NOT modify the lookup path (canonical, per D-S234/S2.35).
2. Kernel hygiene: HF_HOME=/workspace/hf_cache before HF import; sys.path+chdir ENGINE_ROOT before `from memit import`.
3. Pad-token: Llama base pad=eos; Qwen pad already <|endoftext|> 151643.
4. Hparams: Llama band override [4,5,6,7,8] v_loss_layer 31; Qwen /workspace/stage_1_sect/qwen_memit_hparams.json (band [4,5,6,7,8], v_loss_layer 27). Assert.
5. CORRECTED target discipline (LAW): every request uses `" " + object` (leading space). Replicate execute_memit:80-82 if calling compute_z directly.

## Scope
1. **Generalization of the z-geometry contrast** across cfb-v3-002..005 (Tiger Woods→piano, Deion Sanders→violin, Hakeem Olajuwon→harp [multi-token, allowlist proxy], Lindsey Vonn→flute), BOTH models. Per fact, capture step-0 accessibility (avg-prob), convergence/stall verdict, final avg-prob, init/delta norms. GATE each Llama fact against its s224 endpoint before trusting (s224 has all 5). Expectation: Llama stalls 5/5, Qwen converges 5/5 — confirm or falsify.
2. **Generalization of entanglement Probe B** across the same 5 Qwen edits: per-fact same-subject biographical drift vs cross-entity specificity, and per-layer update-norm profile. Test whether front-loading on layers 4–5 and the entity-local/attribute-nonlocal signature hold across subjects.
3. **Resolve D-S234-MANIFEST-1 (manifest merge).** Two divergent manifests: `/workspace/reproducibility_manifest.json` and `/workspace/architecture_profile/reproducibility_manifest.json`. THIS IS A LOAD-BEARING IRREVERSIBLE ACTION on reproducibility artifacts (overwrite-in-place is deny-listed). Procedure: (a) diff both; (b) author a merged UNION to a NEW path `/workspace/reproducibility_manifest_merged_s236.json` (do NOT overwrite either source); (c) write S2.33/S2.34/S2.35/S2.36 entries into the MERGED file only; (d) surface the merged path + a one-line designation request in the summary block for the human to bless as canonical. Do NOT delete or overwrite the source manifests.

## Deliverables at close
- session_2_36_summary_block.md
- z_geometry_multifact_llama_vs_qwen.json (5-fact per-model trajectories + verdicts)
- entanglement_probe_b_multifact_qwen.json (5-fact drift + per-layer profiles)
- framework_finding v1.7 FINAL (promote from additive: add the multi-fact generalization verdict; mark single-fact→N-fact)
- reproducibility_manifest_merged_s236.json (union; NOT a source overwrite) + designation request

## Carried decisions (stand)
- D-S234-1/2/3 (re-diagnosis: index canonical; target leading-space; engine untouched)
- D-S235-1/2/3 (corrected basis; Probe B = apply+restore; anchor-position documented not corrected)
- D-S233-LAYERMATCH-1, D-S233-BAND-1, D-S233-CAPTURE-METHOD-1 (z-arms no-weight-write; Probe B exempt per D-S235-2)

## Specialist routing
memit-specialist (primary), state-consistency-theorist (secondary), framework-spec-writer (close artifacts + v1.7 FINAL).

## Open decision surfaced for entry
If any Llama fact does NOT stall (converges) or any Qwen fact does NOT converge, that PARTIALLY falsifies the single-fact generalization — do not promote v1.7 FINAL; HALT and record which fact broke the pattern with its trajectory. The multi-fact arm is itself the test, not a foregone confirmation.

APPROVE-TO-PROCEED:
